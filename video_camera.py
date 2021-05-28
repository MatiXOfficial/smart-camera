import cv2
from datetime import datetime
import numpy as np
import time
from time import perf_counter
from gpio_devices import GPIODevices

class VideoCamera:

    def __init__(self, model, config, email_connection):
        self.vc = cv2.VideoCapture(0)
        self.current_jpeg = None
        self.model = model
        self.config = config
        self.email_connection = email_connection
        self.last_email_epoch = 0
        
        self.gpio_devices = GPIODevices(config)
        
    def update_model(self, model):
        self.model = model
        
    def get_frame(self):
        ret, frame = self.vc.read()
        frame, is_reco = self.__reco_faces(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return frame, jpeg.tobytes(), is_reco
    
    def __reco_faces(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
        faces = self.model.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
        return frame, (len(faces) > 0)

    def save_video(self, frames, elapsed_time, name=None):
        if name is None:
            name = f'./videos/{datetime.now()}.avi'
        print(f'Saving {len(frames)} frames to {name}')
        video_writer = cv2.VideoWriter(name, cv2.VideoWriter_fourcc(*'DIVX'), len(frames) / elapsed_time, (640, 480))
        for frame in frames:
            video_writer.write(frame)
        video_writer.release()

    def __del__(self):
        self.vc.release()
        cv2.destroyAllWindows()
        
    def generate(self):  # to be run on a separate thread
        frames_before = []
        frames_after = []
        
        frame_neg_counter = 0
        recording = False
        
        while True:
            frame, jpeg, is_reco = self.get_frame()
            self.current_jpeg = jpeg
            if is_reco:
                frame_neg_counter = 0
                if not recording:  # start a recording
                    self.gpio_devices.start()
                    recording = True
                    start_time = perf_counter()
            
            # recording
            if not recording: 
                frames_before += [frame]
                if len(frames_before) > self.config.n_frames_before:
                    frames_before.pop(0)
            else:
                frames_after += [frame]
                frame_neg_counter += 1
                if frame_neg_counter > self.config.n_frames_after:  # save the recording
                    end_time = perf_counter()
                    self.gpio_devices.stop()
                    elapsed_time = end_time - start_time
                    self.save_video(frames_before + frames_after, elapsed_time)
                    recording = False
                    
                    # send email
                    if (time.time() - self.last_email_epoch) > self.config.email_interval:
                        self.last_email_epoch = time.time()
                        ret, jpeg = cv2.imencode('.jpg', frames_after[0])
                        print("Sending email...")
                        self.email_connection.send_email(jpeg.tobytes())
                        
                    # clear
                    frames_before, frames_after = [], []
                    
    def yield_jpeg(self):  # to be run on a separate thread
        while True:
            time.sleep(0.1)
            yield (b'--frame\r\n'
                        b'Content-Type: image/jpeg\r\n\r\n' + self.current_jpeg + b'\r\n\r\n')

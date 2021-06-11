import cv2
from flask import Flask, render_template, render_template_string, Response, send_from_directory, url_for, request
import threading
import os

from video_camera import VideoCamera
from config import Config
from email_connection import EmailConnection


models = {
    'face': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'),
    'body': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_fullbody.xml'),
    'smile': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml'),
    'lower body': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_lowerbody.xml'),
    'upper body': cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_upperbody.xml')
}

config = Config()
video_camera = VideoCamera(models[config.model_name], config, EmailConnection(config))

app = Flask(__name__)
    
@app.route('/')
def index():
    return render_template_string("""
<html>
<body>

<h1> Live broadcast </h1>
<img id="bg" src="{{{{ url_for('trap_cam') }}}}">

<div>
<h1> Settings </h1>
{configuration}
<div/>


<h1> Recorded videos </h1>
{videos_list}

</body>
</html>
""".format(videos_list=get_videos_list_html(), configuration=get_configuration_html()))
    
    
@app.route('/videos/<name>')
def get_video(name):
    return send_from_directory(directory='videos', filename=name)
          
               
@app.route('/trap_cam')
def trap_cam():
	return Response(video_camera.yield_jpeg(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')
        
@app.route('/config_change')
def change_config():
    interval = request.args.get('interval')
    n_frames_before = request.args.get('frames_before')
    n_frames_after = request.args.get('frames_after')
    model_name = request.args.get('model')
    
    global models
    global config
    global video_camera
    
    if interval: 
        config.email_interval = int(interval)
    if n_frames_before: 
        config.n_frames_before = int(n_frames_before)
    if n_frames_after: 
        config.n_frames_after = int(n_frames_after)
    if model_name in models.keys():
        config.model_name = model_name
        video_camera.model = models[model_name]
        
    print(f'Updated the config: {config}')
    return index()
    
def get_videos_list_html():
    if not os.path.exists('./videos'):
        os.mkdir('./videos')
    files = os.listdir('./videos')
    files.sort(reverse=True)
    result = "<ul>\n"
    for file in files:
        file_link_name = file.replace(" ", "%20")
        result += f"<li><a href=/videos/{file_link_name}>{file[:-11]}</a></li>\n"
    result += "</ul>"
    return result

def get_configuration_html():
    global config
    return f"""
<form action="/config_change">
    {get_models_choice_html()}<br>
    <label for="interval">Email Interval [s]</label><br>
    <input type="number" id="interval" name="interval" value="{config.email_interval}"><br><br>
    <label for="frames_before">Number of frames before an event</label><br>
    <input type="number" id="frames_before" name="frames_before" value="{config.n_frames_before}"><br><br>
    <label for="frames_after">Number of frames after the event</label><br>
    <input type="number" id="frames_after" name="frames_after" value="{config.n_frames_after}"><br><br>
    <input type="submit" value="Submit">
<form/>
    """
    
def get_models_choice_html():
    global config
    global models
    result = ''
    for name in models.keys():
        if name == config.model_name:
            result += f'<input type="radio" id="{name}" name="model" value="{name}" checked> <label for="{name}">{name}</label><br>'
        else:
            result += f'<input type="radio" id="{name}" name="model" value="{name}"> <label for="{name}">{name}</label><br>'
    return result
    


if __name__ == '__main__':
	threading.Thread(target=video_camera.generate, daemon=True).start()
	app.run(host='localhost')

import json

class Config:
    
    def __init__(self, path='./config.json'):
        try:
            with open('config.json') as file:
                data = json.load(file)
            
            self.n_frames_before = data['n_frames_before']
            self.n_frames_after = data['n_frames_after']
            self.email_interval = data['email_interval']
            self.model_name = data['model_name']
        except Exception as err:
            print(err)
            exit()
            
    def __str__(self):
        result  = f'n_frames_before = {self.n_frames_before}, '
        result += f'n_frames_after = {self.n_frames_after}, '
        result += f'email_interval = {self.email_interval}, '
        result += f'model_name = {self.model_name}'
        return result

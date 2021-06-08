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
            
            self.led_gpio_pin = data['led_gpio_pin']
            self.buzzer_gpio_pin = data['buzzer_gpio_pin']

            self.email_from = data['email_from']
            self.email_from_password = data['email_from_password']
            self.email_to = data['email_to']
        except Exception as err:
            print("Config error: " + err.msg)
            exit()
            
    def __str__(self):
        result  = f'n_frames_before = {self.n_frames_before}, '
        result += f'n_frames_after = {self.n_frames_after}, '
        result += f'email_interval = {self.email_interval}, '
        result += f'model_name = {self.model_name}, '
        result += f'led_gpio_pin = {self.led_gpio_pin}, '
        result += f'buzzer_gpio_pin = {self.buzzer_gpio_pin}, '
        result += f'email_from = {self.email_from}, '
        result += f'email_to = {self.email_to}'
        return result

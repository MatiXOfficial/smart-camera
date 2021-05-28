from gpiozero import LED
import time
import threading

class GPIODevices:
	
	def __init__(self, config):
		self.led = LED(config.led_gpio_pin)
		self.buzzer = LED(config.buzzer_gpio_pin)
		
		self.is_on = False
		
	def start(self):
		self.is_on = True
		threading.Thread(target=self._led_thread, daemon=True).start()
		threading.Thread(target=self._buzzer_thread, daemon=True).start()
		
	def stop(self):
		self.is_on = False
		
	def _device_on(self, device):
		if not self.is_on:
			raise IOError()
		device.on()
		
	def _device_off(self, device):
		device.off()
		if not self.is_on:
			raise IOError()
			
	def _led_thread(self):
		try:
			while True:
				self._device_on(self.led)
				time.sleep(0.2)
				self._device_off(self.led)
				time.sleep(0.1)
		except IOError:
			pass
			
	def _buzzer_thread(self):
		try:
			while True:
				self._device_on(self.buzzer)
				time.sleep(0.1)
				self._device_off(self.buzzer)
				time.sleep(0.1)
				self._device_on(self.buzzer)
				time.sleep(0.1)
				self._device_off(self.buzzer)
				time.sleep(0.1)
				self._device_on(self.buzzer)
				time.sleep(0.1)
				self._device_off(self.buzzer)
				time.sleep(0.1)
				self._device_on(self.buzzer)
				time.sleep(0.1)
				self._device_off(self.buzzer)
				time.sleep(1)
		except IOError:
			pass
		
	

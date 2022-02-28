import time
import I2C_LCD_driver
import RPi.GPIO as GPIO

class RaspberryOutputWriter:
	def __init__(self, led_ports=(5, 6, 13, 19, 26)):
		self.lcd = I2C_LCD_driver.lcd()


		self.lcd.lcd_clear()
		self.write_to_screen(level=5, points=0)

		self.led_ports = led_ports

		# Initialize LEDs		
		GPIO.setmode(GPIO.BCM)
		GPIO.setwarnings(False)
		
		for led_port in led_ports:
			GPIO.setup(led_port, GPIO.OUT)

		for led_port in led_ports:
			GPIO.output(led_port, GPIO.HIGH)

	def write_to_screen(self, level, points):
		self.lcd.lcd_display_string("Level: {}".format(level), 1, 0)
		self.lcd.lcd_display_string("Points: {}".format(points), 2, 0)

	def set_leds_based_on_health(self, health):
		n = health // 20 if health > 0 else 0
		
		for led_port in self.led_ports:
			GPIO.output(led_port, GPIO.LOW)

		#if n == 1:
		#	self.start_blinking()
		#	return

		for led_port in self.led_ports[:n]:
			GPIO.output(led_port, GPIO.HIGH)

	def start_blinking(self):
		led_port = self.led_ports[0]

		while True:
			GPIO.output(led_port, GPIO.HIGH)
			time.sleep(0.25)
			GPIO.output(led_port, GPIO.LOW)
			time.sleep(0.25)


			
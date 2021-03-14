import Jetson.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
modes = GPIO.getmode()


print(GPIO.JETSON_INFO, GPIO.VERSION)
import Jetson.GPIO as GPIO
import time


def main():

    PWM_PIN_1 = 32
    PWM_PIN_2 = 33
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PWM_PIN_1,GPIO.OUT,initial = GPIO.HIGH)
    GPIO.setup(PWM_PIN_2,GPIO.OUT,initial = GPIO.HIGH)


    p1 = GPIO.PWM(PWM_PIN_1,100)
    p2 = GPIO.PWM(PWM_PIN_2,100)

    val  = 100
    incr = 1
    p1.start(val)
    p2.start(val)

    print("Running PWM w/ BOARD pin {} {}".format(PWM_PIN_1,PWM_PIN_2))

    try:
        while True:
            time.sleep(0.25)
            if val >= 100:
                incr = -incr
            if val <= 0:
                incr = -incr
            val += incr
            p1.ChangeDutyCycle(val)
            p2.ChangeDutyCycle(val)
            


    finally:
        p1.stop()
        p2.stop()
        GPIO.cleanup()



if __name__ == '__main__':
    main()
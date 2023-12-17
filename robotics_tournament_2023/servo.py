import wiringpi
class Servo:
    def __init__(self,pin):
        self.pin = pin

    def attach(self):
        wiringpi.pinMode(self.pin, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pwmSetMode(pin=self.pin,mode=wiringpi.GPIO.PWM_MODE_MS)
        wiringpi.pwmSetClock(pin=self.pin,divisor=240)
        wiringpi.pwmSetRange(self.pin,range=2000)

    def move_angle(self,angle):
        pulse = 50 + angle*(180 / 200)
        print("servo",pulse)
        wiringpi.pwmWrite(pin=self.pin, value=int(pulse))


if __name__ == '__main__':
    wiringpi.wiringPiSetup()  
    servo1 = Servo(2)
    servo1.attach()
    servo1.move_angle(90)
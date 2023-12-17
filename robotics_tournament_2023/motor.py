import wiringpi
class Motor:
    def __init__(self):
        pass
    def MoveContinue(self,speed):
        pass
    def stop(self):
        pass

class Motor_gpio(Motor):
    def __init__(self,pin1,pin2):
        self.pin1 = pin1
        self.pin2 = pin2
        wiringpi.pinMode(self.pin1, wiringpi.GPIO.OUTPUT)
        wiringpi.pinMode(self.pin2, wiringpi.GPIO.OUTPUT)
        self.stop()
    def MoveContinue(self,speed):
        if speed > 0:
            wiringpi.digitalWrite(self.pin1,1)
            wiringpi.digitalWrite(self.pin2,0)
        else:
            wiringpi.digitalWrite(self.pin1,0)
            wiringpi.digitalWrite(self.pin2,1)

    def stop(self):
        wiringpi.digitalWrite(self.pin1,1)
        wiringpi.digitalWrite(self.pin2,1)
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
    def MoveContinue(self,speed):
        pass
    def stop(self):
        pass
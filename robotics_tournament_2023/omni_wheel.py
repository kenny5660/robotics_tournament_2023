from robotics_tournament_2023.kangaroo_x2  import Kangaroo_x2, Kangaroo_x2_Motor
import math

class omni_wheel_3:
    def __init__(self,motorA,motorB,motorC,radius) -> None:
        self.motorA = motorA
        self.motorB = motorB
        self.motorC = motorC
        self.radius = radius
        
    def move(self,velocity,rot_speed):
        velocity_x = velocity[0]
        velocity_y = velocity[1]
        motorA_speed = -0.5*velocity_x+math.sqrt(3)*0.5*velocity_y + self.radius*rot_speed
        motorB_speed = -0.5*velocity_x-math.sqrt(3)*0.5*velocity_y + self.radius*rot_speed
        motorC_speed = velocity_x + self.radius*rot_speed
        self.motorA.MoveContinue(motorA_speed)
        self.motorB.MoveContinue(motorB_speed)
        self.motorC.MoveContinue(motorC_speed)

    def stop(self):
        self.motorA.stop()
        self.motorB.stop()
        self.motorC.stop()


if __name__ == '__main__':
    serial = pyserial.Serial( 'COM10', 115200)
    kanga_1 = Kangaroo_x2(130,serial)
    kanga_2 = Kangaroo_x2(135,serial)
    motorA = Kangaroo_x2_Motor(kanga_1,0,1000)
    motorB = Kangaroo_x2_Motor(kanga_1,1,1000)
    motorC = Kangaroo_x2_Motor(kanga_2,0,1000)
    omni = omni_wheel_3(motorA,motorB,motorC,radius=60)#100mm
    omni.move((0,100),0)
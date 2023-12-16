from robotics_tournament_2023.kangaroo_x2  import Kangaroo_x2, Kangaroo_x2_Motor
import math
import serial as pyserial
class omni_wheel_3:
    def __init__(self,motorA,motorB,motorC,radius) -> None:
        self.motorA = motorA
        self.motorB = motorB
        self.motorC = motorC
        self.radius = radius
        
    def move(self,velocity,rot_speed):
        velocity_x = float(velocity[0])
        velocity_y = float(velocity[1])
        motorA_speed = -0.5*velocity_x+math.sqrt(3)*0.5*velocity_y + self.radius*rot_speed
        motorB_speed = -0.5*velocity_x-math.sqrt(3)*0.5*velocity_y + self.radius*rot_speed
        motorC_speed = velocity_x + self.radius*rot_speed

        print(motorA_speed)
        print(motorB_speed)
        print(motorC_speed)
        self.motorA.MoveContinue(motorA_speed)
        self.motorB.MoveContinue(motorB_speed)
        self.motorC.MoveContinue(motorC_speed)

    def stop(self):
        self.motorA.stop()
        self.motorB.stop()
        self.motorC.stop()


if __name__ == '__main__':
    serial = pyserial.Serial( 'COM7', 115200)
    kanga_130 = Kangaroo_x2(130,serial)
    kanga_135 = Kangaroo_x2(135,serial)
    motorA = Kangaroo_x2_Motor(kanga_130, '1', 3,inverted=False)
    motorB = Kangaroo_x2_Motor(kanga_130, '2', 3,inverted=True)
    motorC = Kangaroo_x2_Motor(kanga_135, '1', 3,inverted=False)
    omni = omni_wheel_3(motorA,motorB,motorC,radius=60)#100mm
    omni.move((360,0),0)
from robotics_tournament_2023.kangaroo_x2  import Kangaroo_x2, Kangaroo_x2_Motor
import math
import serial as pyserial
import time

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

    def move2(self,deg,speed,rot_speed):
        deg = deg - 30
        theta1, theta2, theta3 = 150.0, 270.0, 30.0
        motorA_speed = math.sin((deg-theta1)*(math.pi/180.0)) 
        motorB_speed = math.sin((deg-theta2)*(math.pi/180.0))
        motorC_speed = math.sin((deg-theta3)*(math.pi/180.0))

        motorA_speed *= speed
        motorB_speed *= speed
        motorC_speed *= speed

        motorA_speed += self.radius*rot_speed
        motorB_speed += self.radius*rot_speed
        motorC_speed += self.radius*rot_speed

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
    serial = pyserial.Serial( '/dev/ttyS2', 115200)
    kanga_130 = Kangaroo_x2(130,serial)
    kanga_135 = Kangaroo_x2(135,serial)
    motorA = Kangaroo_x2_Motor(kanga_130, '1', 3,inverted=False)
    motorB = Kangaroo_x2_Motor(kanga_130, '2', 3,inverted=True)
    motorC = Kangaroo_x2_Motor(kanga_135, '1', 3,inverted=False)
    omni = omni_wheel_3(motorA,motorB,motorC,radius=1)#100mm
    # omni.move((-360,0),0)
    omni.move2(0,500,0)
    time.sleep(2)
    omni.stop()
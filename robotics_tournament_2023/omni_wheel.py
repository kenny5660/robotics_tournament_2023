from robotics_tournament_2023.kangaroo_x2  import Kangaroo_x2


class omni_wheel_3:
    def __init__(self,motorA,motorB,motorC) -> None:
        pass


if __name__ == '__main__':
    serial = pyserial.Serial( 'COM10', 115200)
    kanga_1 = Kangaroo_x2(130,serial)
    kanga_2 = Kangaroo_x2(135,serial)
    kanga_1.CmdStart(0)
    kanga_1.CmdMoveSpeed(0,Kangaroo_x2.kMoveTypeSpeed,100)
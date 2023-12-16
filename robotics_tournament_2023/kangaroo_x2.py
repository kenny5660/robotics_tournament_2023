import serial as pyserial
from robotics_tournament_2023.motor import Motor
import time
class Kangaroo_x2:
    kCmdStart = 32
    kCmdHome = 34
    kCmdMove = 36
    kCmdGet = 35
    kCmdGetReply = 67
    
    kMoveTypePos = 1
    kMoveTypeSpeed = 2
    kMoveTypeIncPos = 65
    kMoveTypeIncSpeed = 66

    def __init__(self, addr, serial) -> None:
        self.addr = addr
        self.serial = serial

    def bitpackNumber(number):
        i = 0
        buffer = bytearray(range(5))
        if number < 0 : 
            number = -number 
            number <<= 1 
            number |= 1
        else: 
            number <<= 1

        while i < 5:
            buffer[i] = (number & 0x3f) 
            if number >= 0x40 :  
                buffer[i] |= 0x40 
            else:
                buffer[i] |= 0x00 
            i += 1; 
            number >>= 6; 
            if number == 0 : 
                break
        return i , buffer
    
    def crc14(data, length):
        crc = 0x3fff
        for i in range(length):
            crc ^= data[i] & 0x7f
            for bit in range(7):
                if (crc & 1) > 0: 
                    crc >>= 1 
                    crc ^= 0x22f0
                else:
                    crc >>= 1
        return (crc ^ 0x3fff) & 0xffff
    
    def CmdStart (self, chnl):
        data_packet = bytearray((0,1,2,3,4,5,6,7))
        data_packet[0] = self.addr
        data_packet[1] = Kangaroo_x2.kCmdStart
        data_packet[2] = 2; #length
        data_packet[3] = ord(chnl)
        data_packet[4] = 0
        crc = Kangaroo_x2.crc14(data_packet, 5)
        data_packet[5] = crc & 0x7F
        data_packet[6] = crc >> 7 & 0x7F
        self.serial.write(data_packet)

    def CmdHome (self, chnl):
        data_packet = bytearray(range(7))
        data_packet[0] = self.addr
        data_packet[1] = Kangaroo_x2.kCmdHome
        data_packet[2] = 2; #length
        data_packet[3] = ord(chnl)
        data_packet[4] = 0
        crc = Kangaroo_x2.crc14(data_packet, 5)
        data_packet[5] = crc & 0x7F
        data_packet[6] = crc >> 7 & 0x7F
        self.serial.write(data_packet)
    
    def CmdMoveSpeed(self, chnl, type, speed):
        data_packet = bytearray(range(13))
        bitpack_Value = bytearray(range(5))
        data_packet[0] = self.addr
        data_packet[1] = Kangaroo_x2.kCmdMove
        data_packet[3] = ord(chnl)
        data_packet[4] = 0; #//flags
        data_packet[5] = type   #type
        lengthValue, bitpack_Value = Kangaroo_x2.bitpackNumber(speed)
        for i in range(lengthValue):
            data_packet[6 + i] = bitpack_Value[i]

        data_packet[2] = 3 + lengthValue
        crc = Kangaroo_x2.crc14(data_packet, 6 + lengthValue)
        data_packet[6 + lengthValue] = crc & 0x7F
        data_packet[7 + lengthValue] = crc >> 7 & 0x7F
        self.serial.write(data_packet[:8 + lengthValue])


class Kangaroo_x2_Motor(Motor):
    def __init__(self, kangaroo_drv,chnl,counts_per_deg,inverted = False) -> None:
        super().__init__()
        self.kangaroo_drv = kangaroo_drv
        self.chnl = chnl
        self.counts_per_deg = counts_per_deg
        if inverted:
            self.inverted_coef =  -1
        else:
            self.inverted_coef =  1
        self.kangaroo_drv.CmdStart(chnl)

    def MoveContinue(self, speed):
        speed *= self.inverted_coef*self.counts_per_deg
        speed = max(-2000, min(2000, speed))
        self.kangaroo_drv.CmdMoveSpeed(self.chnl, Kangaroo_x2.kMoveTypeSpeed, int(speed))
    
    def stop(self):
        self.kangaroo_drv.CmdMoveSpeed(self.chnl, Kangaroo_x2.kMoveTypeSpeed, 0)

if __name__ == '__main__':
    #serial = pyserial.Serial( '/dev/ttyS2', 115200)
    serial = pyserial.Serial( 'COM7', 115200)
    kanga_130 = Kangaroo_x2(130,serial)
    kanga_135 = Kangaroo_x2(135,serial)
    motorA = Kangaroo_x2_Motor(kanga_130, '1', 3,inverted=False)
    motorB = Kangaroo_x2_Motor(kanga_130, '2', 3,inverted=True)
    motorC = Kangaroo_x2_Motor(kanga_135, '1', 3,inverted=False)

    motorA.MoveContinue(360)
    motorB.MoveContinue(360)
    motorC.MoveContinue(360)
    time.sleep(2)
    motorA.stop()
    motorB.stop()
    motorC.stop()

    
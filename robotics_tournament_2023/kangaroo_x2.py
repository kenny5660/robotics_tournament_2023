import serial as pyserial


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
        buffer = bytes(range(5))
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
                if (crc & 1): 
                    crc >>= 1 
                    crc ^= 0x22f0
                else:
                    crc >>= 1
        return (crc ^ 0x3fff) & 0xffff
    
    def CmdStart (self, chnl):
        data_packet = bytes((0,1,2,3,4,5,6,7))
        data_packet[0] = self.addr
        data_packet[1] = Kangaroo_x2.kCmdStart
        data_packet[2] = 2; #length
        data_packet[3] = chnl
        data_packet[4] = 0
        crc = Kangaroo_x2.crc14(data_packet, 5)
        data_packet[5] = crc & 0x7F
        data_packet[6] = crc >> 7 & 0x7F
        self.serial.write(data_packet, 7)

    def CmdStart (self, chnl):
        data_packet = bytes((0,1,2,3,4,5,6,7))
        data_packet[0] = self.addr
        data_packet[1] = Kangaroo_x2.kCmdHome
        data_packet[2] = 2; #length
        data_packet[3] = chnl
        data_packet[4] = 0
        crc = Kangaroo_x2.crc14(data_packet, 5)
        data_packet[5] = crc & 0x7F
        data_packet[6] = crc >> 7 & 0x7F
        self.serial.write(data_packet, 7);	
    
    def CmdMoveSpeed(self, chnl, type, speed):
        data_packet = bytes(range(13))
        bitpack_Value = bytes(range(5))
        data_packet[0] = self.addr
        data_packet[1] = Kangaroo_x2.kCmdMove
        data_packet[3] = chnl
        data_packet[4] = 0; #//flags
        data_packet[5] = type   #type
        lengthValue, bitpack_Value = Kangaroo_x2.bitpackNumber(speed)
        for i in range(lengthValue):
            data_packet[6 + i] = bitpack_Value[i]

        data_packet[2] = 3 + lengthValue
        crc = Kangaroo_x2.crc14(data_packet, 6 + lengthValue)
        data_packet[6 + lengthValue] = crc & 0x7F
        data_packet[7 + lengthValue] = crc >> 7 & 0x7F
        self.serial.write(data_packet, 8 + lengthValue)


if __name__ == '__main__':
    serial = pyserial.Serial( 'COM10', 115200)
    kanga_1 = Kangaroo_x2(130,serial)
    kanga_2 = Kangaroo_x2(135,serial)
    kanga_1.CmdStart(0)
    kanga_1.CmdMoveSpeed(0,Kangaroo_x2.kMoveTypeSpeed,100)
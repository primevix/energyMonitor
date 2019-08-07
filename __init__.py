import serial
import time
import struct

class PZEM:
    
    readVoltageBytes 	= 	[0xB0,0xC0,0xA8,0x01,0x01,0x00,0x1A]
    readCurrentBytes 	= 	[0XB1,0xC0,0xA8,0x01,0x01,0x00,0x1B]
    readPowerBytes 	= 	[0XB2,0xC0,0xA8,0x01,0x01,0x00,0x1C]
    readRegPowerBytes 	= 	[0XB3,0xC0,0xA8,0x01,0x01,0x00,0x1D]
    setAddrBytes 	=	[0xB4,0xC0,0xA8,0x01,0x01,0x00,0x1E]

    def __init__(self, com="/dev/ttyUSB0", timeout=10.0):  

        self.ser = serial.Serial(
		port=com,
		baudrate=9600,
		parity=serial.PARITY_NONE,
		stopbits=serial.STOPBITS_ONE,
		bytesize=serial.EIGHTBITS,
		timeout = timeout
	)
        if self.ser.isOpen():
            self.ser.close()
            print("Serial abierto")
        self.ser.open()

    def checkChecksum(self,_tuple):
        _list = list(_tuple)
        _checksum = _list[-1]
        _list.pop()
        _sum = sum(_list)
        if _checksum == _sum%256:
            return True
        else:
            raise Exception("Wrong cheksum")

    def isReady(self):
        self.ser.write(serial.to_bytes(self.setAddrBytes))
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B",rcv)
            if(self.checkChecksum(unpacked)):
                return True
        else:
            raise serial.SerialTimeoutException("Timeout setting address")
            

    def readVoltage(self):
        self.ser.write(serial.to_bytes(self.readVolatgeBytes))
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B",rcv)
            if(self.checkChecksum(unpacked)):
                tension = unpacked[2]+unpacked[3]/10.0
                return tension
        else:
            raise serial.SerialTimeoutException("Timeout reading tension")

    def readCurrent(self):
        self.ser.write(serial.to_bytes(self.readCurrentBytes))
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpaked = struct.unpack("!7B",rcv)
            if(self.checkChecksum(unpacked)):
                current = unpacket[2]+unpacked[3]/100.0
        else:
            raise serial.SerialTimeoutException("Timeout reading current")

    def readPower(self):
        self.ser.write(serial.to_bytes(self.readPowerBytes))
        rcv = self.ser.read(7)
        if len(rcv) == 7:
            unpacked = struct.unpack("!7B",rcv)
            if(self.checkChecsum(unpacked)):
                power = unpacked[1]*256+unpacked[2]
                return power
        else:
            raise serial.SerialTimeoutException("Timeout reading power")
    
    def readAll(self):
        if(self.isReady()):
            return(self.readVoltage(),self.readCurrent(),self.readPower(),eradregPower())

    def close(self):
        self.ser.close()


                
if __name__ == "__main__":
    sensor = PZEM()
    try:
        print("Checking readiness")
        print(sensor.isReady())
        print("Reading voltage")
        print(sensor.readVoltage())
        print("Reading Current")
        print(sensor.readCurrent())
        print("Reading power")
        print(sensor.readPower())
        print("reading registered power")
        print(sensor.readRegPower())
        print("reading all")
        print(sensor.readAll())
    finally:
        sensor.close()

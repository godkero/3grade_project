from serial import Serial 

from serial.serialutil import Timeout

class SerialModule(Serial):

    def __init__(self,portStr = None ,baud_rate = 9600):
        super().__init__(port = portStr ,baudrate= baud_rate)
        self.start = False
        self.buf = []
        self.countingBuf = 0
        self.READ_END_FLAG = False

    def send_protocol(self,char):
        self.write(char.encode())
        
    def read_data(self):
        
        self.buf = []
        self.countingBuf = 0
        self.flush()
        eof = "e"
        start = "s"

        while not self.READ_END_FLAG:
            try:
                    line = self.readline()
            except Exception as e: 
                print(e)

            str = line.decode('utf-8').strip('\r\n')
            
            if str == start:
                self.start = True 
            elif str == eof:
                self.start == False 
                break 
            else :
                if self.start == True:
                    try:
                        floatline  = float(str)/1024.0*5.0
                        self.countingBuf +=1
                        self.buf.append(floatline)
                    except: 
                        break           
        return self.buf

class Control:

    def __init__(self,size,strPort,baudrate):
        self.strPort = strPort
        self.baudrate = baudrate
        self.ser = None
        

    def set_serial_port(self,port):
        self.strPort = port
        print(self.strPort)

    def set_serial_baudrate(self,baudrate):
        self.baudrate = baudrate
        print(self.baudrate)

    def connect(self):
        self.ser = SerialModule(
            portStr = self.strPort,
            baud_rate = self.baudrate
            )
    def is_disconneted(self):
        if self.ser == None :
            return True
        return False
        
    def disconnect(self):
        self.ser.close()

    def read_end(self):
        self.ser.READ_END_FLAG  = True
        print("send read_end")

    def read_start(self):
        self.ser.READ_END_FLAG = False
        print("send read_start") 
#recevie to Arduino data
    def get_data(self):
        return  self.ser.read_data()

# send to Arduino protocol
    def write_start(self):
        try:
            self.ser.send_protocol("A")

        except:
            print("connect error")
    def write_stop(self):
        try:
            self.ser.send_protocol("B")
        except:
            print("connect error")
    def write_data(self,char):
        try:
            self.ser.send_protocol(char)
        except:
            print("connect error")
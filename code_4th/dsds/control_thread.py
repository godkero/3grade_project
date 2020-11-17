import threading

from serial.serialutil import SerialException
from .UIPanel import UIPanel
import time
import sys, traceback



class MainControl(UIPanel):
    def __init__(self,parent,left):
        UIPanel.__init__(self,parent = parent , left = left)
        
        self.STOP_FLAG_read = False
        self.lock = threading.Lock()
    
    #daemon thread - just read and display    
    def read_th(self):
        while not self.STOP_FLAG_read:
            try:
                self.left.set_data(self.con.get_data())
                self.textValue.SetLabel(str('%.2f' %self.left.get_volt_max()))
                self.textfrequncy.SetLabel(self.left.get_fmax())
                self.left.animate()
            except SerialException as e:
                # self.STOP_FLAG_read = True
                print("serial error")
                break
            except Exception as e:
                if self.con.is_disconneted():
                    return 
                print("read thread error")
                print(e)
        print("5")
        return 
    
    
    #when click stop init ui panel
    def init_when_stop(self):
        #sampleRate init
        self.sampleFreCount = 0
        self.textSampleFre.SetLabel(str("8.928(kHz)"))#8.982khz
        # x-scale init
        self.PERIOD_COUNT = 0
        self.left.divideIndex = 1
        # Trigger init
        self.setTriggerCount = 0
        self.textTrigger.SetLabel(str("Default"))
        self.TrigValCount = 0
        self.textTrigVal.SetLabel(str("trigVal : 1V")) 
        # fft_ac : dominant frequency
        self.fftmodeBut.SetLabel(str("DC"))
        self.left.fft_ac = False



    # click event override
    def OnStartClick(self,event):
        val = self.togglebuttonStart.GetValue()
        if(val == True):
            try:
                # click start logic
                self.STOP_FLAG_read = False
                self.con.connect()
                self.con.read_start()
                self.togglebuttonStart.SetLabel("stop")
            except:
                self.togglebuttonStart.SetLabel("start")
                self.togglebuttonStart.SetValue(False)
                self.SerialErrorMessage() 
            
          
    
            try:    
                time.sleep(1)
                self.con.write_start()
                self.read_thread = threading.Thread(target = self.read_th,daemon= True)
                self.read_thread.start()

                # self.read_thread.start()    
            except Exception as e:
                print("start click error",e)

        else:
            try:
                # click stop logic
                self.STOP_FLAG_read = True

                # thread join logic
                print("in")
                self.con.read_end()
                self.read_thread.join(2)
                print("read_close()")
                self.con.ser.cancel_read()
                print("out")
                self.con.write_stop()
                
                self.con.disconnect()
                self.init_when_stop()
                self.togglebuttonStart.SetLabel("Start")
                self.togglebuttonStart.SetValue(False) 
                print("end succes")
            except Exception as e:
                print("stop click error", e)
                self.togglebuttonStart.SetLabel("Stop")
                self.togglebuttonStart.SetValue(True)

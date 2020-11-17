import wx
from code_4th.SerialModule import Control
from code_4th.DrawPanel import GraphPanel

class UIPanel(wx.Panel):
    def __init__(self,parent,left):
        wx.Panel.__init__(self,parent = parent,size = (200,700))

        self.con = Control(size = 1024,strPort = "COM1",baudrate ="9600")
        
        self.left = left

        #useful flags
        self.sampleFreCount =0
        self.IS_DC_INCLUDE = True
        self.PERIOD_COUNT = 0  
        self.setTriggerCount = 0
        self.TrigValCount = 0
        self.ylim_count = 0

        """
        UI Design 
        """
        titleFont = wx.Font(12, wx.DEFAULT, wx.DEFAULT, wx.BOLD)
        subFont = wx.Font(11, wx.DEFAULT, wx.DEFAULT, wx.NORMAL)

        # start, stop
        self.togglebuttonStart = wx.ToggleButton(self, id = -1, label = "Start",
                                        pos = (10,10),size =(100,50))
        self.togglebuttonStart.Bind(wx.EVT_TOGGLEBUTTON, self.OnStartClick)

        #Voltage Peek
        textVoltage = wx.StaticText(self, -1, "Analog Inputs Peek",pos = (10,80),size = (160,30))
        textVoltage.SetFont(titleFont)

        textPeek = wx.StaticText(self,-1,"Vpeek(V) =",pos = (10,110), size =(100,30))
        self.textValue = wx.StaticText(self,label="",pos = (80,110),size = (80,30))
        self.textValue.SetFont(subFont)
        self.textValue.SetLabel(str("0(V)"))

        #frequency Peek
        textFrequency = wx.StaticText(self, -1, "Dominant Freqency(Hz)",pos = (10,140),size = (160,30))
        textFrequency.SetFont(titleFont)

        self.textfrequncy = wx.StaticText(self,label="",pos = (10,170),size = (80,30))
        self.textfrequncy.SetFont(subFont)
        self.textfrequncy.SetLabel(str("0(Hz)"))

        ##peek frequency top, bottom 에서 가져와야되


        self.statictextSampleFre = wx.StaticText(self,label="",pos = (10,250),size = (80,30))
        self.statictextSampleFre.SetLabel(str("SampleRate"))

        self.textSampleFre = wx.StaticText(self,label="",pos = (10,280),size = (80,30))
        self.textSampleFre.SetLabel(str("8.928(kHz)"))

        self.statictextTrigger = wx.StaticText(self,label="",pos = (10,310),size = (80,30))
        self.statictextTrigger.SetLabel(str("Trigger mode"))


        self.textTrigger = wx.StaticText(self,label="",pos = (10,340),size = (80,30))
        self.textTrigger.SetLabel(str("Defult"))



        self.sampleRatebut = wx.Button(self, -1, "Set SampleFrequency", pos =(10,400),size = (140,40))
        self.sampleRatebut.Bind(wx.EVT_BUTTON, self.SetSampleRate)


        self.periodBut = wx.Button(self, -1, "Set period", pos =(10,450),size = (140,40))
        self.periodBut.Bind(wx.EVT_BUTTON, self.SetXlim)
        self.triggerBut = wx.Button(self, -1, "Set trigger", pos =(10,500),size = (140,40))
        self.triggerBut.Bind(wx.EVT_BUTTON, self.SetTrigger)

        self.fftmodeBut =wx.ToggleButton(self, -1, label = "DC", pos =(10,550),size = (140,40))
        self.fftmodeBut.Bind(wx.EVT_TOGGLEBUTTON, self.SetMode)

        self.fftylimBut = wx.Button(self, -1, " set ymax:=4", pos =(150,550),size = (140,40))
        self.fftylimBut.Bind(wx.EVT_BUTTON, self.set_fft_ylim)

        self.trigValbut = wx.Button(self, -1, "Set trigVal", pos =(10,600),size = (140,40))
        self.trigValbut.Bind(wx.EVT_BUTTON, self.SetTrigVal)

        self.textTrigVal = wx.StaticText(self,label="",pos = (90,310),size = (80,30))
        self.textTrigVal.SetLabel(str("trigVal : 1V"))
       

    

    def SetMode(self,event):

        val = self.fftmodeBut.GetValue()
        if val == True:
            self.fftmodeBut.SetLabel(str("AC"))
            self.left.fft_ac = True
        else :
            self.fftmodeBut.SetLabel(str("DC"))
            self.left.fft_ac = False



    def SerialErrorMessage(self):
        wx.MessageBox("Serial Communication is not working!","info",wx.OK |wx.ICON_INFORMATION)

    def set_fft_ylim(self,evnet):
        if not self.con.is_disconneted():

            if self.ylim_count <3:
                self.ylim_count +=1
            else:
                self.ylim_count = 0
            try:
                if self.ylim_count == 0:
                    self.left.ax2_y_max = 4
                    self.fftylimBut.SetLabel(str("set ymax:=4"))
                elif self.ylim_count == 1:
                    self.left.ax2_y_max = 3
                    self.fftylimBut.SetLabel(str("set ymax:=3"))
                elif self.ylim_count == 2:
                    self.left.ax2_y_max = 2
                    self.fftylimBut.SetLabel(str("set ymax:=2"))
                elif self.ylim_count == 3:
                    self.left.ax2_y_max = 1
                    self.fftylimBut.SetLabel(str("set ymax:=1"))
            except: 
                print("fft_ylim button error")
        else: 
            self.SerialErrorMessage()        	



    def SetSampleRate(self, event):
        # serial communication
        if not self.con.is_disconneted() :


            if self.sampleFreCount <5:
                self.sampleFreCount+=1
            else:
                self.sampleFreCount = 0
            try :
            #set staticText
                if self.sampleFreCount == 0:
                    self.con.write_data('S')
                    self.textSampleFre.SetLabel(str("8.928(kHz)"))#8.982khz

                    self.left.sample_frequency = 8.928 * 1000.0 
                    self.left.sample_period = 0.000112
                elif self.sampleFreCount == 1:
                    self.con.write_data('R')
                    self.textSampleFre.SetLabel(str("17.842(kHz)"))
                    self.left.sample_frequency = 17.842 * 1000.0
                    self.left.sample_period = 0.000056
                elif self.sampleFreCount == 2:
                    self.con.write_data('Q')
                    self.textSampleFre.SetLabel(str("34.038(kHz)"))
                    self.left.sample_frequency = 34.038 * 1000.0
                    self.left.sample_period = 0.0000293
                elif self.sampleFreCount == 3:
                    self.con.write_data('P')
                    self.textSampleFre.SetLabel(str("62.5(kHz)"))
                    self.left.sample_frequency = 62.5 * 1000.0
                    self.left.sample_period = 0.000016
                elif self.sampleFreCount == 4:
                    self.con.write_data('O')
                    self.textSampleFre.SetLabel(str("117.1088(kHz)"))
                    self.left.sample_frequency = 117.1088 * 1000.0
                    self.left.sample_period = 0.000008539
                elif self.sampleFreCount == 5:
                    self.con.write_data('M')
                    self.textSampleFre.SetLabel(str("185.1048(kHz)"))
                    self.left.sample_frequency = 185.1048 * 1000.0
                    self.left.sample_period = 0.0000054
            except: 
                print("Sending error")	
        else: 
            self.SerialErrorMessage()



    def SetXlim(self, event):
        # calculating 1/(samplerate/sample)=period 
        # want to see low domain 
        # just show little array and throw away last
        if self.PERIOD_COUNT <5:
            self.PERIOD_COUNT+=1
        else :
            self.PERIOD_COUNT = 0

        if self.PERIOD_COUNT == 0:
            self.left.divideIndex = 1

        elif self.PERIOD_COUNT == 1:
            self.left.divideIndex = 2

        elif self.PERIOD_COUNT == 2:
            self.left.divideIndex = 4

        elif self.PERIOD_COUNT == 3:
            self.left.divideIndex = 8

        elif self.PERIOD_COUNT == 4:
            self.left.divideIndex = 16

        elif self.PERIOD_COUNT == 5:
            self.left.divideIndex = 32
            
        print("setXlim")

    def SetTrigger(self,event):
        # serial communication
        if not self.con.is_disconneted() :
        # 	self.con.set_set_trigger()
            if self.setTriggerCount <2:
                self.setTriggerCount+=1
            else:
                self.setTriggerCount = 0
            
            try :
                if self.setTriggerCount == 0:
                    self.con.write_data('D')
                    self.textTrigger.SetLabel(str("Default"))

                elif self.setTriggerCount == 1:
                    self.con.write_data('E')
                    self.textTrigger.SetLabel(str("Pose Edge"))

                elif self.setTriggerCount == 2:
                    self.con.write_data('F')
                    self.textTrigger.SetLabel(str("Nega Edge"))

            except :
                print("setTrigger error")
        else: 
            self.SerialErrorMessage()

    def OnStartClick(self, event):
        val = self.togglebuttonStart.GetValue()
        if (val == True):
            self.togglebuttonStart.SetLabel("Stop")
        try:
        # thread start 
            self.con.connect()
            
        except Exception as e : 
            if not self.con.is_disconneted(): 
                self.con.ser.cancel_read()
                self.con.disconnect()
                print("Serial Port Error")
                
            self.togglebuttonStart.SetLabel("Start")
            self.togglebuttonStart.SetValue(False)
            self.SerialErrorMessage()
            print(e)
                
        else:
            self.togglebuttonStart.SetLabel("Start")
            self.con.ser.cancel_read()
            self.con.disconnect()
        
    def SetTrigVal(self,event) :
        if not self.con.is_disconneted()  :
            if self.TrigValCount <3 :
                    self.TrigValCount +=1
            else : 
                self.TrigValCount = 0
            
            try : 
                if self.TrigValCount == 0 :
                    self.con.write_data('G')
                    self.textTrigVal.SetLabel(str("trigVal : 1V")) 
            
                if self.TrigValCount == 1 :
                    self.con.write_data('H')
                    self.textTrigVal.SetLabel(str("trigVal : 2V"))

                if self.TrigValCount == 2 :
                    self.con.write_data('I')
                    self.textTrigVal.SetLabel(str("trigVal : 3V"))
        
                if self.TrigValCount == 3 :
                    self.con.write_data('J')
                    self.textTrigVal.SetLabel(str("trigVal : 4V"))

                print("setTrigVal")            

            except : 
                print("setTrigVal error")
        else: 
            self.SerialErrorMessage()


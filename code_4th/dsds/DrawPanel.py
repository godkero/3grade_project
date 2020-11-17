import wx
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np

class GraphPanel(wx.Panel):
    def __init__(self,parent,sampleSize = 100, sampleRate = 100):
        wx.Panel.__init__(self,parent = parent,size = (900,700))
        
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)

        plt.style.use("dark_background")
        self.fig = plt.figure(figsize = (9,6))
        

        self.ax1 = self.fig.add_subplot(2,1,1)
        self.ax2 = self.fig.add_subplot(2,1,2)
        # sample_frequency
        self.canvas = FigureCanvas(self,-1,self.fig)  
        self.v_sizer.Add(self.canvas,1,flag = wx.EXPAND )
        self.SetSizer(self.v_sizer)
        self.v_max = 0
        self.f_max = 0

        self.indexSize = sampleSize
        self.ax1_xdata = []#np.linspace([0,self.indexSize],self.indexSize+1)[0:-1]
        self.ax1_ydata = []#np.zeros(self.indexSize)

        self.ax2_xdata = []#np.linspace(0,self.indexSize,self.indexSize+1)[0:-1]
        self.ax2_ydata = []#np.zeros(self.indexSize)
        self.tmp = []
        #first label

        self.ax2_y_max = 4
        
        self.ax1.set_xlabel("T(time)")
        self.ax1.set_ylabel("Voltage")

        self.ax2.set_xlabel("f(frequency)")
        self.ax2.set_ylabel("Amptiude")

        self.ax1.set_title("Wavefrom",fontsize= 14)
        self.ax2.set_title("Spectrum", fontsize= 14)

        self.ax1.grid(True)
        self.ax2.grid(True)
        
        self.ax1.set_ylim([0,5.2])
        self.ax2.set_ylim([0,self.ax2_y_max])
        
        self.line1, = self.ax1.plot([],[])
        self.line2, = self.ax2.plot([],[])
        self.sample_frequency = 8.9*1000.0
        self.sample_period = 0.0001124 #8.9khz
        self.fft_ac = False
        self.divideIndex = 1

        self.fig.tight_layout()
        self.Fit()



    def set_sample_size(self, samplesize):
        self.indexSize = samplesize        
        

    def fft(self,ydata):
        
        #fft logic
        
        try:
            # if you want to fft with only ac signal

            # if self.fft_ac == True:
            #     ydata = ydata - np.average(ydata)
        
            fft = np.fft.fft(ydata , n = self.indexSize)/len(ydata)
            fft_mag = abs(fft)
            fft_mag = fft_mag[range(int(len(fft)/2))]
        except Exception as e:
            print(e)
            ydata[:-1] = 0
            fft_mag = ydata
            
        return fft_mag


    def set_data(self,ydata):
        
        self.ax1.cla()
        self.ax2.cla()

        x_len = float(len(ydata))
        ori_ydata = ydata
        
        self.ax1_ydata = ydata[:int(x_len/self.divideIndex)]
        self.ax1_xdata = np.linspace(0,len(self.ax1_ydata),len(self.ax1_ydata)+1)[0:-1]
        
        # time graph t-domain
        self.ax1_xdata = self.ax1_xdata * self.sample_period
        if self.ax1_xdata[-1]<=1.0:
            self.ax1_xdata = self.ax1_xdata*1000
            self.ax1.set_xlabel("T(ms)")
            if self.ax1_xdata[-1]<=1.0:
                self.ax1_xdata = self.ax1_xdata*1000
                self.ax1.set_xlabel("T(us)")
        else :
            self.ax1.set_xlabel("T(s)")

        self.ax1.set_xlim([self.ax1_xdata[0],self.ax1_xdata[-1]]) 
        
        # freuqency graph f-domain
        
        self.ax2_ydata = self.fft(ori_ydata)
        self.ax2_xdata = np.linspace(0,len(self.ax2_ydata),len(self.ax2_ydata)+1)[0:-1]
        
        # set frequency x-axis
         
        self.ax2_xdata = self.ax2_xdata * (self.sample_frequency) /512.0
        self.tmp = self.ax2_xdata  

        if self.ax2_xdata[-1]>1000.0:

            self.ax2_xdata = self.ax2_xdata /1000.0
            self.ax2.set_xlabel("f(kHz)")
            
            if self.ax2_xdata[-1]>1000.0:
                self.ax2_xdata = self.ax2_xdata/ 1000.0
                self.ax2.set_xlabel("f(Mhz)")
                
        else:   
            self.ax2.set_xlabel("f(Hz)")
         

        self.ax2.set_xlim([self.ax2_xdata[0],self.ax2_xdata[-1]])

        self.__get_frequency_info()
        

        try:
            v_max = max(self.ax1_ydata[0:-1])
        except:
            v_max = 0
        
        self.set_volt_max(v_max)
        # if you want annotation max index
        # index_of_maximum = np.where(self.ax1_xdata == self.v_max)

        
    def get_volt_max(self):
        return self.v_max

    def set_volt_max(self,vmax):
        self.v_max = vmax

    def __get_frequency_info(self):
        
        if self.fft_ac:
            f_value = max(self.ax2_ydata[1:-1]) 
        else :
            f_value = max(self.ax2_ydata[0:-1])
        # if you want annotiton where frequency max 
        f_max = 0
        f_max_index =[]
        try:
            index_of_maxmium = np.where(self.ax2_ydata == f_value)
            
            
            f_max = self.tmp[index_of_maxmium]
            f_max_index = f_max
            self.fre_str ="(Hz)"
            if f_max_index >1000.0:
                f_max_index = f_max_index/1000
                self.fre_str ="(KHz)"
                if f_max_index>1000.0*1000.0:
                    f_max_index = f_max_index/1000
                    self.fre_str ="(MHz)"
            self.f_max = str('%.2f' %float(f_max_index))
            print("최대값", f_max)
           
        except Exception as e:
            print("frequency info error")
        try:
            text = "frequency={:.2f}".format(f_max_index[0]) 
            text += self.fre_str
            self.ax2.annotate(text, xy=(f_max[0]/1000,f_value),
                xytext=(f_max[0]/1000, f_value+0.2),
            arrowprops=dict(arrowstyle="->",connectionstyle="angle,angleA=0,angleB=30"))
        except Exception as e:
            print("annotation error",e)     
        self.f_max +=self.fre_str
    
    def get_fmax(self):
        return self.f_max

    def animate(self):
        try:
            self.animate_info()
            self.line1, = self.ax1.plot(self.ax1_xdata,self.ax1_ydata,'r')
            self.line2, = self.ax2.plot(self.ax2_xdata,self.ax2_ydata,'r')
            
            self.ax1.relim()
            self.ax1.autoscale_view()
            self.ax2.relim()
            self.ax2.autoscale_view()
            
            self.canvas.draw()
            
            self.canvas.flush_events()
        except:
            print("error in animate")
    
    def animate_info(self):
        
        self.ax1.set_ylabel("Voltage")
        self.ax2.set_ylabel("Amptiude")

        self.ax1.set_title("Wavefrom",fontsize= 14)
        self.ax2.set_title("Spectrum", fontsize= 14)

        self.ax1.set_ylim([0,5.2])
        self.ax2.set_ylim([0,float(self.ax2_y_max)])
        self.ax1.grid(True)
        self.ax2.grid(True)
        
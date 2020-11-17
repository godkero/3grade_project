import wx
from code_4th.DrawPanel import GraphPanel
from code_4th.control_thread import MainControl

class Main(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(
			self, parent = None, title = "HappyWave with youngK",
			style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE,
			size = (1200,800)	
			)
		self.initUI()
		self.initMENU()
		self.Show()

######
	def initUI(self):
		
		v_sizer = wx.BoxSizer(wx.VERTICAL)
		h_sizer = wx.BoxSizer(wx.HORIZONTAL)
		
		self.leftPanel = GraphPanel(parent = self, sampleSize= 512)		
		self.rightPanel = MainControl(parent = self, left =self.leftPanel)
		
		self.leftPanel.SetBackgroundColour('#45049')

		# v_sizer.Add(self.topPanel,proportion = 1,flag = wx.EXPAND)
		# v_sizer.Add(self.bottomPanel,proportion = 1,flag = wx.EXPAND)
		
		h_sizer.Add(self.leftPanel,proportion = 3,flag = wx.EXPAND )
		h_sizer.Add(self.rightPanel,proportion = 1,flag = wx.EXPAND)
		
		self.SetSizer(h_sizer)
		self.Fit()
		self.Centre()
		


# init menubar
	def initMENU(self):
		self.port = "COM1"
		self.rate = "9600"
		self.CreateStatusBar()
		self.menuBar = wx.MenuBar()

		portmenu = wx.Menu()
		portmenu.Append(99,"&PORT1",kind = wx.ITEM_RADIO)
		portmenu.Append(100,"&PORT2",kind = wx.ITEM_RADIO)
		portmenu.Append(101,"&PORT3",kind = wx.ITEM_RADIO)
		portmenu.Append(102,"&PORT4",kind = wx.ITEM_RADIO)
		portmenu.Append(103,"&PORT5",kind = wx.ITEM_RADIO)
		portmenu.Append(104,"&PORT6",kind = wx.ITEM_RADIO)
		portmenu.Append(105,"&PORT7",kind = wx.ITEM_RADIO)
		portmenu.Append(106,"&PORT8",kind = wx.ITEM_RADIO)
		portmenu.Append(107,"&PORT9",kind = wx.ITEM_RADIO)
		portmenu.Append(108,"&PORT10",kind = wx.ITEM_RADIO)
		portmenu.Append(109,"&PORT11",kind = wx.ITEM_RADIO)
		
		ratemenu = wx.Menu()
		ratemenu.Append(111,"&9600",kind = wx.ITEM_RADIO)
		ratemenu.Append(112,"&19200",kind = wx.ITEM_RADIO)
		ratemenu.Append(113,"&38400",kind = wx.ITEM_RADIO)
		ratemenu.Append(114,"&57600",kind = wx.ITEM_RADIO)
		ratemenu.Append(115,"&74880",kind = wx.ITEM_RADIO)
		ratemenu.Append(116,"&115200",kind = wx.ITEM_RADIO)
		ratemenu.Append(117,"&230400",kind = wx.ITEM_RADIO)
	
		helpmenu = wx.Menu()
		helpmenu.Append(130,"&help")

		self.menuBar.Append(portmenu,"&port")
		self.menuBar.Append(ratemenu,"&Baudrate")	
		self.menuBar.Append(helpmenu,"&Help")
		self.SetMenuBar(self.menuBar)
	# menu event handler 
		self.Bind(wx.EVT_MENU,self.setPORT1,id=99)
		self.Bind(wx.EVT_MENU,self.setPORT2,id=100)
		self.Bind(wx.EVT_MENU,self.setPORT3,id=101)
		self.Bind(wx.EVT_MENU,self.setPORT4,id=102)
		self.Bind(wx.EVT_MENU,self.setPORT5,id=103)
		self.Bind(wx.EVT_MENU,self.setPORT6,id=104)
		self.Bind(wx.EVT_MENU,self.setPORT7,id=105)
		self.Bind(wx.EVT_MENU,self.setPORT8,id=106)
		self.Bind(wx.EVT_MENU,self.setPORT9,id=107)
		self.Bind(wx.EVT_MENU,self.setPORT10,id=108)
		self.Bind(wx.EVT_MENU,self.setPORT11,id=109)

		self.Bind(wx.EVT_MENU,self.setRate1,id=111)
		self.Bind(wx.EVT_MENU,self.setRate2,id=112)
		self.Bind(wx.EVT_MENU,self.setRate3,id=113)
		self.Bind(wx.EVT_MENU,self.setRate4,id=114)
		self.Bind(wx.EVT_MENU,self.setRate5,id=115)
		self.Bind(wx.EVT_MENU,self.setRate6,id=116)
		self.Bind(wx.EVT_MENU,self.setRate7,id=117)

		self.Bind(wx.EVT_MENU,self.helpContent,id=130)


	def helpContent(self,event):
		print("help")



# baudrate handler
	def setRate1(self,event):
		self.rate = 9600
		print(self.rate)
		self.rightPanel.con.set_serial_baudrate(self.rate)
	def setRate2(self,event):
		self.rate = 19200
		print(self.rate)
		self.rightPanel.con.set_serial_baudrate(self.rate)
	def setRate3(self,event):
		self.rate = 38400
		print(self.rate)
		self.rightPanel.con.set_serial_baudrate(self.rate)
	def setRate4(self,event):
		self.rate = 57600
		print(self.rate)
		self.rightPanel.con.set_serial_baudrate(self.rate)
	def setRate5(self,event):
		self.rate = 74880
		print(self.rate)
		self.rightPanel.con.set_serial_baudrate(self.rate)
	def setRate6(self,event):
		self.rate = 115200
		print(self.rate)
		self.rightPanel.con.set_serial_baudrate(self.rate)
	def setRate7(self,event):
		self.rate = 230400
		print(self.rate)
		self.rightPanel.con.set_serial_baudrate(self.rate)

# port number handler
	def setPORT1(self,event):
		self.port = "COM1"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT2(self,event):
		self.port = "COM2"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT3(self,event):
		self.port = "COM3"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT4(self,event):
		self.port = "COM4"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT5(self,event):
		self.port = "COM5"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT6(self,event):
		self.port = "COM6"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT7(self,event):
		self.port = "COM7"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT8(self,event):
		self.port = "COM8"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)	
	def setPORT9(self,event):
		self.port = "COM9"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)
	def setPORT10(self,event):
		self.port = "COM10"
		self.rightPanel.con.set_serial_port(self.port)
		print(self.port)
	def setPORT11(self,event):
		self.port = "COM11"
		print(self.port)
		self.rightPanel.con.set_serial_port(self.port)



if __name__ =="__main__":
	app = wx.App(False)
	frame = Main()
	app.MainLoop()
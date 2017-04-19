# coding=utf-8
from Tkinter import *
from SerialHelp import *
import serial.tools.list_ports 
import tkFont
from config import *
class testerUI(Frame):
	"""tester UI With Tkinter"""
	def __init__(self, parent,root):
		Frame.__init__(self, parent)
		
		#串口读取选择界面
		self.portNameList = self.getPortList()
		self.currentPort=StringVar(self)
		self.currentPort.set(self.portNameList[0])
		
		#串口
		self.signalSerial = SerialHelper(self.currentPort.get())
		self.signalSerial.thresholdValue = 16
		self.createWidgets()
		
		self.IDS={}
		ctime = time.time()
		self.IDS["00000000"]=ctime
		self.repeat =0
	def createWidgets(self):
		rowHeight = 2
		rowWidth = 10
		
		row=0
		#状态标识
		self.signalButton = Button(self,text=" ",bg="grey",height=rowHeight)
		self.signalButton.grid(row=row,column=0,sticky=W+E)
		
		def changeSignalPort(event):
			if self.signalSerial.alive:
				self.signalSerial.stop()
			
			self.signalSerial.port = self.currentPort.get()
			self.signalSerial.start()
			thread_read = threading.Thread(target=self.getSingnalData)
			thread_read.setDaemon(False)
			thread_read.start()
		
		self.portNames = OptionMenu(self,self.currentPort,*self.portNameList,command=changeSignalPort)
		self.portNames.grid(row=row,column=1,sticky=W+E+N+S)

		#模块类型
		moduleName = PM.keys()
		self.module=StringVar()
		self.module.set(moduleName[0])
		def changeModel(event):
			self.moduleParam = eval(PM[self.module.get()])
			self.rightType = self.moduleParam['TYPE']
			self.rightNum = self.moduleParam['NUM']
		
		modules = OptionMenu(self,self.module,*moduleName,command=changeModel)
		modules.grid(row=row,column=2,sticky=W+E+N+S)
		
		
		#第二行
		row += 1
		Label(self,text=u'ID: ',height=rowHeight).grid(row=row,column=0,sticky=E)
		self.ID = StringVar()
		self.IDEntry=Entry(self,textvariable=self.ID,state=["readonly"])
		self.IDEntry.grid(row=row,column=1,sticky=W+E+N+S)
		
		self.quantity = StringVar()
		Label(self,textvariable=self.quantity,fg="red").grid(row=row,column=2,sticky=W+E+N+S)

		#第三行
		row += 1
		Label(self,text=u'Type: ',height=rowHeight).grid(row=row,column=0,sticky=E)
		self.type = StringVar()
		self.typeEntry=Entry(self,textvariable=self.type,state=["readonly"])
		self.typeEntry.grid(row=row,column=1,sticky=W+E+N+S)
		
		self.typeDescription = StringVar()
		Label(self,textvariable=self.typeDescription).grid(row=row,column=2,sticky=W+E+N+S)

		#第四行
		row += 1
		Label(self,text=u'Num: ',height=rowHeight).grid(row=row,column=0,sticky=E)
		self.num = StringVar()
		self.numEntry=Entry(self,textvariable=self.num,state=["readonly"])
		self.numEntry.grid(row=row,column=1,sticky=W+E+N+S)
		
		self.numDescription = StringVar()
		Label(self,textvariable=self.numDescription).grid(row=row,column=2,sticky=W+E+N+S)
		#第五行
		row += 1
		Label(self,text=u'RSSI: ',height=rowHeight).grid(row=row,column=0)
		self.RSSI = StringVar()
		self.RSSIEntry=Entry(self ,textvariable=self.RSSI,width=10,state=["readonly"])
		self.RSSIEntry.grid(row= row,column=1,sticky=W+E+N+S)

		self.signalArea = StringVar()
		self.signalArea.set("35")
		self.signalAreaEntry = Entry(self, textvariable = self.signalArea,width=10).grid(row=row,column=2,sticky=W+E+N+S)

		#第六行
		row += 1
		Label(self,text=u'次数: ',height=rowHeight).grid(row=row,column=0,sticky=E)
		self.times = StringVar()
		self.timesEntry=Entry(self,textvariable=self.times,state=["readonly"])
		self.timesEntry.grid(row=row,column=1,sticky=W+E+N+S)
		
		self.timesDescription = StringVar()
		Label(self,textvariable=self.timesDescription).grid(row=row,column=2,sticky=W+E+N+S)
		
		changeModel('<Button>')
		changeSignalPort('<Button>')

	#获取串口列表，并返回list
	def getPortList(self):
		portList = list(serial.tools.list_ports.comports())
		portNameList = []
		for port in portList:
			portNameList.append(str(port[0]))
		return portNameList

	#获取串口数据
	def getSingnalData(self):
	   while self.signalSerial.alive:
			try:
				number = self.signalSerial.l_serial.inWaiting()
				if number>=8:
					self.signalSerial.receive_data += self.signalSerial.l_serial.read(number)
					self.signalSerial.l_serial.flushInput()
					self.signalSerial.receive_data = str(binascii.b2a_hex(self.signalSerial.receive_data))
					#print self.signalSerial.receive_data
					if self.signalSerial.thresholdValue != len(self.signalSerial.receive_data):
						self.signalSerial.receive_data = ""
						
					else:
						receiveRSSI = int(self.signalSerial.receive_data[12:14],16)
						setRSSI = int(str(self.signalArea.get()))
						if receiveRSSI < setRSSI:
							self.updateUI(self.signalSerial.receive_data)
						self.signalSerial.receive_data = ""

			except Exception as e:
				logging.error(e)
				#串口断线后重启
				while(1):
					time.sleep(0.5)
					self.signalSerial.stop()
					self.signalSerial.start()
					port = self.currentPort.get()
					print port
					if self.signalSerial.alive:
						break


	#更新显示数据
	def updateUI(self, singnalData):
		currentID = singnalData[0:8]
		currentTime = time.time()
		self.IDEntry['fg']='blue'
		self.ID.set(currentID)
		
		#重复检测
		if currentID in self.IDS.keys():
			if currentTime-self.IDS[currentID]>5:
				self.repeat += 1
				self.quantity .set("重复"+str(self.repeat))
				print self.repeat,currentID,currentTime
		else:
			self.IDS[currentID]=currentTime
		
		testType = singnalData[8:10]
		self.type.set(testType)
		if testType == self.rightType:
			self.typeEntry['fg']='blue'
		else:
			self.typeEntry['fg']='red'
		
		testNum = singnalData[10:12]
		self.num.set(testNum)
		
		if testNum in self.rightNum.keys():
			self.numEntry['fg']='blue'
			self.numDescription.set(self.rightNum[testNum])
		else:
			self.numEntry['fg']='red'	
			self.numDescription.set("")
		 
		self.RSSI.set(int(singnalData[12:14],16))
		self.RSSIEntry['fg']='blue'
		
		self.times.set(singnalData[14:16])
		if int(self.times.get()) >= 2:
			self.timesEntry['fg']='blue'
		else:
			self.timesEntry['fg']='red'

		self.blink()
		
	def blink(self):
		self.signalButton['bg']='green'
		time.sleep(0.1)
		self.signalButton['bg']='grey'    


if __name__ == '__main__':
	root=Tk()
	root.geometry('800x480')  
	root.title("领普科技信号测试仪V0.1")

	#修改默认字体大小

	font=('Verdane',17,'bold')
	root.option_add("*Font", font)
	
	container = Frame(root)
	tester = testerUI(root,container)
	tester.grid(row=0, column=0, sticky="nsew")

		#[x]关闭窗口
	def closeWindow():
		tester.signalSerial.stop()
		root.destroy()

	root.protocol('WM_DELETE_WINDOW', closeWindow) # root is your root window
	root.mainloop()

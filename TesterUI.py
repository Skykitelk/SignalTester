# coding=utf-8
from Tkinter import *
from SerialHelp import *
import serial.tools.list_ports 
import tkFont
class testerUI(object):
    """tester UI With Tkinter"""
    def __init__(self, root):
        frame = Frame(root)
        root.geometry('400x300')
        root.title("领普科技信号测试仪V0.1")

        #修改默认字体大小
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        root.option_add("*Font", default_font)
        # grid 6*5布局
        #串口读取选择界面
        self.portNameList = self.getPortList()
        self.currentPort=StringVar(root)
        self.currentPort.set(self.portNameList[0])
        self.portNames = OptionMenu(root,self.currentPort,*self.portNameList)
        self.portNames.grid(row=0,columnspan=3,sticky=W)

        #开始测试按钮
        self.startButton = Button(root,text="开始测试")
        self.startButton.grid(row=0,column=2,columnspan=2,sticky=E+W)
        #UI界面
        Label(root,text=u'ID: ').grid(row=1,column=0,sticky=E)
        self.ID = StringVar()
        self.IDEntry=Entry(root,textvariable=self.ID).grid(row=1,column=1,columnspan=2,sticky=W+E)

        Label(root,text=u'Type: ').grid(row=2,column=0,sticky=E)
        self.type = StringVar()
        self.typeEntry=Entry(root,textvariable=self.type).grid(row=2,column=1,columnspan=2,sticky=W+E)

        Label(root,text=u'Num: ').grid(row=3,column=0,sticky=E)
        self.num = StringVar()
        self.numEntry=Entry(root,textvariable=self.num).grid(row=3,column=1,columnspan=2,sticky=W+E)

        Label(root,text=u'RSSI: ').grid(row=4,column=0,sticky=E)
        self.RSSI = StringVar()
        self.RSSIEntry=Entry(root,textvariable=self.RSSI,width=10).grid(row=4,column=1,sticky=W+E)

        self.signalArea = StringVar()
        self.signalArea.set("50")
        self.signalAreaEntry = Entry(root, textvariable = self.signalArea,width=10).grid(row=4,column=2,sticky=W+E)

        Label(root,text=u'次数: ').grid(row=5,column=0,sticky=E)
        self.times = StringVar()
        self.timesEntry=Entry(root,textvariable=self.times).grid(row=5,column=1,columnspan=2,sticky=W+E)

        #状态标识
        self.signalButton = Button(root,text=" ",bg="grey")
        self.signalButton.grid(row=6,column=0,columnspan=5,sticky=W+E)

        #串口
        self.signalSerial = SerialHelper(self.currentPort.get())
        

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
                time.sleep(0.01)
                number = self.signalSerial.l_serial.inWaiting()
                if number:
                    self.signalSerial.receive_data += self.signalSerial.l_serial.read(number)
                    self.signalSerial.receive_data = str(binascii.b2a_hex(self.signalSerial.receive_data))
                    print self.signalSerial.receive_data
                    
                    if self.signalSerial.thresholdValue < len(self.signalSerial.receive_data):
                        self.signalSerial.receive_data = ""
                    else:
                        receiveRSSI = int(self.signalSerial.receive_data[12:14],16)
                        setRSSI = int(str(self.signalArea.get()))
                        if receiveRSSI < setRSSI:
                            self.updateUI(self.signalSerial.receive_data)
                        self.signalSerial.receive_data = ""
            except Exception as e:
                logging.error(e) 

    #更新显示数据
    def updateUI(self, singnalData):
        self.ID.set(singnalData[0:8])
        self.type.set(singnalData[8:10])
        self.num.set(singnalData[10:12])
        self.RSSI.set(int(singnalData[12:14],16))
        self.times.set(singnalData[14:16])
        self.blink()

    def blink(self):
        self.signalButton['bg']='green'
        time.sleep(0.1)
        self.signalButton['bg']='grey'

if __name__ == '__main__':
    root=Tk()
    tester = testerUI(root)
    #tester.signalSerial.start()
    thread_read = threading.Thread(target=tester.getSingnalData)
    thread_read.setDaemon(False)
    thread_read.start()

    def changeSignalPort(event):
        tester.signalSerial.stop()
        tester.signalSerial.port = tester.currentPort.get()
        tester.signalSerial.start()
        thread_read = threading.Thread(target=tester.getSingnalData)
        thread_read.setDaemon(False)
        thread_read.start()
    tester.startButton.bind('<Button>',changeSignalPort)
    tester.signalSerial.start()
    root.mainloop()
# coding=utf-8
from Tkinter import *
from SerialHelp import *
import serial.tools.list_ports 
import tkFont
class testerUI(object):
    """tester UI With Tkinter"""
    def __init__(self, root):
        frame = Frame(root)
        root.geometry('500x300')
        root.title("领普科技信号测试仪V0.1")

        #修改默认字体大小
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        root.option_add("*Font", default_font)
        
        self.portNameList = self.getPortList()
        self.currentPort=StringVar(root)
        self.currentPort.set(self.portNameList[0])
        self.portNames = OptionMenu(root,self.currentPort,*self.portNameList)#, command = self.changeSignalPort())
        self.portNames.grid(row=0,columnspan=3)
        
        
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
                number = self.signalSerial.l_serial.inWaiting()
                if number:
                    self.signalSerial.receive_data += self.signalSerial.l_serial.read(number)
                    if self.signalSerial.thresholdValue < len(self.signalSerial.receive_data):
                        self.signalSerial.receive_data = ""
                    else:                        
                        self.signalSerial.receive_data = str(binascii.b2a_hex(self.signalSerial.receive_data))
                        print self.signalSerial.receive_data
                        receiveRSSI = int(self.signalSerial.receive_data[26:28],16)
                        setRSSI = int(str(self.signalArea.get()))
                        if receiveRSSI < setRSSI:
                            self.updateUI(self.signalSerial.receive_data)
                        self.signalSerial.receive_data = ""
            except Exception as e:
                logging.error(e) 

    #更新显示数据
    def updateUI(self, singnalData):
        self.ID.set(singnalData[14:22])
        self.type.set(singnalData[22:24])
        self.num.set(singnalData[24:26])
        self.RSSI.set(int(singnalData[26:28],16))

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
    tester.portNames.bind('<Button-1>',changeSignalPort)
    tester.signalSerial.start()
    root.mainloop()
# coding=utf-8
from Tkinter import *
from SerialHelp import *
#from ttk import *
import tkFont
class testerUI(object):
    """tester UI With Tkinter"""
    def __init__(self, root):
        frame = Frame(root)
        #root.geometry('600x300')
        root.title("领普科技信号测试仪V0.1")
        v=StringVar(root)
        root.option_add("*Font","宋体")
        root.option_add("*FontSize","50")
        v.set("G1模块")
        
        modules = OptionMenu(root,v,"G1模块","G2模块","K3模块","K4模块").grid(row=0,columnspan=2)
       
        #UI界面
        Label(root,text=u'ID: ').grid(row=1,column=0)
        self.ID = StringVar()
        self.IDEntry=Entry(root,textvariable=self.ID).grid(row=1,column=1)

        Label(root,text=u'Type: ').grid(row=2,column=0)
        self.type = StringVar()
        self.typeEntry=Entry(root,textvariable=self.type).grid(row=2,column=1)

        Label(root,text=u'Num: ').grid(row=3,column=0)
        self.num = StringVar()
        self.numEntry=Entry(root,textvariable=self.num).grid(row=3,column=1)

        Label(root,text=u'RSSI: ').grid(row=4,column=0)
        self.RSSI = StringVar()
        self.RSSIEntry=Entry(root,textvariable=self.RSSI).grid(row=4,column=1)

        Label(root,text=u'次数: ').grid(row=5,column=0)
        self.times = StringVar()
        self.timesEntry=Entry(root,textvariable=self.times).grid(row=5,column=1)

        #串口
        self.signalSerial = SerialHelper("COM5")

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
                        self.updateUI(self.signalSerial.receive_data)

            except Exception as e:
                logging.error(e) 

    def updateUI(self, singnalData):

        self.ID.set(singnalData[14:22])
        self.type.set(singnalData[22:24])
        self.num.set(singnalData[24:26])
        self.RSSI.set(int(singnalData[26:28],16))

if __name__ == '__main__':
    root=Tk()
    tester = testerUI(root)
    tester.signalSerial.start()
    thread_read = threading.Thread(target=tester.getSingnalData)
    thread_read.setDaemon(False)
    thread_read.start()
    root.mainloop()
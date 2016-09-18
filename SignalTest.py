# coding=utf-8
from Tkinter import *
# from ttk import *
from SerialHelp import *
from PySqlite import *
import serial.tools.list_ports
from SerialHelp import *


class SignalTest(Frame):

    '''主页'''

    def __init__(self, parent, root):
        Frame.__init__(self, parent)

        self.createWidgets()

        # 串口
        
        self.signalSerial = SerialHelper(Port=self.signalPort.get())
        
        self.powerSerial = SerialHelper(Port=self.powerPort.get())

        # 数据库
        host = 'sqlite.db'
        self.table = 'PowerModelSignal'
        self.sqlite = PySqlite(host)
        # self.sqlite.drop(self.table)
        values = {"SN": 'char(10)', "ID": 'char(10) UNIQUE', "type": 'char(3)', "num": 'char(3)', "signalTimes": 'char(3)',
        "PMState": 'int', 'testTime': 'char(15)'}
        self.sqlite.create(self.table, values, 'DBID')

    def createWidgets(self):
        # 串口读取选择界面
        self.portNameList = self.getPortList()
        self.portNameList.append("COMx")

        # 信号串口
        Label(self, text=u'选择信号串口：').grid(row=1, column=3, sticky=W)
        self.signalPort = StringVar(self)
        self.signalPort.set(self.portNameList[1])
        SignalPortName = OptionMenu(self, self.signalPort, *self.portNameList)
        SignalPortName.grid(row=2, column=3, columnspan=1, sticky=E)

        # 电量串口
        Label(self, text=u'选择发电量串口：').grid(row=4, column=3, sticky=W)
        self.powerPort = StringVar(self)
        self.powerPort.set(self.portNameList[0])
        powerPortName = OptionMenu(self, self.powerPort, *self.portNameList)
        powerPortName.grid(row=5, column=3, columnspan=1, sticky=E)


        # UI界面
        Label(self, text=u'ID: ').grid(row=1, column=0, sticky=E)
        self.ID = StringVar()
        IDEntry = Entry(self, textvariable=self.ID).grid(
            row=1, column=1, columnspan=2, sticky=W+E)

        Label(self, text=u'Type: ').grid(row=2, column=0, sticky=E)
        self.type = StringVar()
        typeEntry = Entry(self, textvariable=self.type).grid(
            row=2, column=1, columnspan=2, sticky=W+E)

        Label(self, text=u'Num: ').grid(row=3, column=0, sticky=E)
        self.num = StringVar()
        numEntry = Entry(self, textvariable=self.num).grid(
            row=3, column=1, columnspan=2, sticky=W+E)

        Label(self, text=u'RSSI: ').grid(row=4, column=0, sticky=E)
        self.RSSI = StringVar()
        RSSIEntry = Entry(self, textvariable=self.RSSI, width=10).grid(
            row=4, column=1, sticky=W+E)

        self.signalArea = StringVar()
        self.signalArea.set("50")
        signalAreaEntry = Entry(self, textvariable=self.signalArea, width=10).grid(
            row=4, column=2, sticky=W+E)

        Label(self, text=u'次数: ').grid(row=5, column=0, sticky=E)
        self.times = StringVar()
        timesEntry = Entry(self, textvariable=self.times).grid(
            row=5, column=1, columnspan=2, sticky=W+E)

        Label(self, text=u'发电量: ').grid(row=6, column=0, sticky=E)
        self.power = StringVar()
        powerEntry = Entry(self, textvariable=self.power).grid(
            row=6, column=1, columnspan=2, sticky=W+E)

        # 状态标识

        # # ttk设置label颜色
        # style = Style()
        # style.configure("BW.TLabel", foreground="black", background="red")
        # signalButton = Button(self, text=" ", style="BW.TLabel")

        self.signalButton = Button(
            self, text="开始测试", background="grey", command=self.changeSignalPort)
        self.signalButton.grid(row=0, column=0, columnspan=5, sticky=W+E)

    # 获取串口列表，并返回list
    def getPortList(self):
        portList = list(serial.tools.list_ports.comports())
        portNameList = []
        for port in portList:
            portNameList.append(str(port[0]))
        return portNameList

    def getsignalData(self):
        while self.signalSerial.alive or self.powerSerial.alive:
            try:
                if self.signalSerial.alive:
                    time.sleep(0.15)
                    signalnumber = self.signalSerial.l_serial.inWaiting()
                    if signalnumber:
                        self.signalSerial.receive_data += self.signalSerial.l_serial.read(signalnumber)
                        self.signalSerial.receive_data =str(binascii.b2a_hex(self.signalSerial.receive_data)) 
                else:
                    signalnumber = 0
                       

                if self.powerSerial.alive:
                    powernumber = self.powerSerial.l_serial.inWaiting()
                    if powernumber:
                        self.powerSerial.receive_data += self.powerSerial.l_serial.read(powernumber)
                        self.powerSerial.receive_data = str(binascii.b2a_hex(self.powerSerial.receive_data))
                else:
                    powernumber=0

                if signalnumber or powernumber:
                    if 16 != len(self.signalSerial.receive_data):
                        self.signalSerial.receive_data=""
                    if 4 != len(self.powerSerial.receive_data):
                        self.powerSerial.receive_data=""
                    if self.signalSerial.receive_data !="" or self.powerSerial.receive_data !="" :
                        if self.signalSerial.receive_data=="":
                            receiveRSSI=0
                        else:
                            receiveRSSI=int(self.signalSerial.receive_data[12:14], 16)
                        setRSSI=int(str(self.signalArea.get()))
                        if receiveRSSI > setRSSI:
                            self.signalSerial.receive_data=""
                        self.updateUI(self.signalSerial.receive_data,self.powerSerial.receive_data)
                        self.signalSerial.receive_data=""
                        self.powerSerial.receive_data=""
            except Exception as e:
                logging.error(e)

  



    # 更新显示数据
    def updateUI(self, signalData, powerData):
        if signalData=="":
            signalData="0000000000000000"
        if powerData=="":
            powerData="0000"

        ID=signalData[0:8]
        sType=signalData[8:10]
        num=signalData[10:12]
        RSSI=int(signalData[12:14], 16)
        times=signalData[14:16]
        power=round(float(int(powerData[0:4],16))/147.0,2)

        self.ID.set(ID)
        self.type.set(sType)
        self.num.set(num)
        self.RSSI.set(RSSI)
        self.times.set(times)
        self.power.set(power)
        self.blink()
        now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

        value={'ID': ID, 'type': sType, 'num': num,
                 'signalTimes': times, 'testTime': now}
        self.sqlite.insert(self.table, value)

    def blink(self):
        self.signalButton['bg']='green'
        time.sleep(0.1)
        self.signalButton['bg']='grey'

    def changeSignalPort(self):
        if self.signalSerial.port!="COMx":
            self.signalSerial.stop()
        if self.signalSerial.port!="COMx":
            self.powerSerial.stop()
        print 'stop'
        self.signalSerial.port=self.signalPort.get()
        self.powerSerial.port = self.powerPort.get()
        print 'start'
        self.testStart()

    def testStart(self):
        try:

            if self.signalSerial.port!="COMx":
                self.signalSerial.start()
            if self.powerSerial.port!="COMx":
                self.powerSerial.start()
        except Exception as e:
            logging.error(e)
             
        thread_read=threading.Thread(target=self.getsignalData) 
        thread_read.setDaemon(False)
        thread_read.start()

    def testStop(self):
        if self.signalSerial.port!="COMx":
            self.signalSerial.stop()
        if self.powerSerial.port!="COMx":
            self.powerSerial.stop()
        self.sqlite.close()
if __name__ == '__main__':
    root=Tk()
    container=Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    tester=SignalTest(container, root)
    tester.grid(row=0, column=0, sticky="nsew")

    #[x]关闭窗口
    def closeWindow():
        tester.testStop()
        root.destroy()

    root.protocol('WM_DELETE_WINDOW', closeWindow)  # root is your root window
    tester.testStart()
    root.mainloop()

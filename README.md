# SignalTester
射频信号测试程序，tkinter，串口通信
##功能
可以自动读取COM口（需要点击一下）
可以设置接收范围
##433mHZ字符截断规则
singalData = 55000707017a0000036003022044000000000000cf
self.ID.set(singnalData[14:22])
self.type.set(singnalData[22:24])
self.num.set(singnalData[24:26])
self.RSSI.set(int(singnalData[26:28],16))
# SignalTester
射频信号测试程序，tkinter，串口通信   
##功能
可以自动读取COM口（需要点击一下）   
可以设置接收范围   
##433mHZ字符截断规则
	```
	singalData = 00 03 A1 35 02 20 1B 01 
	self.ID.set(singnalData[0:8])   
	self.type.set(singnalData[8:10])   
	self.num.set(singnalData[10:12])   
	self.RSSI.set(int(singnalData[12:14],16))
	self.times.set(signalData[14:16])
	``` 

#更新日志
## v0.1
初始化版本  

## v0.2 20160817
* 王辰梦简化字段  
* 增加测试按钮  

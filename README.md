# SignalTester
射频信号测试程序，tkinter，串口通信   
##功能
* 配合USB接收器，显示射频信号信息，带接收到的次数
* 可以自动读取COM口（需要点击一下）   
* 可以设置接收范围   

##字符截断规则
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

## v0.3 20161109
* 从power分支（发电量）切换到master分支
* 简化功能，优化稳定性。仅仅测试信号（不测发电量）
* bug：快按程序会暂停，按开始又OK

## v0.4 20161215
* 修正快按程序会死掉的情况

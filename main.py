#!/usr/bin/env
# coding=utf-8
# Copyright By Yangzhan 20160908
from Tkinter import *
from ttk import *
import tkFont

import serial.tools.list_ports

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from SignalTest import *
from QueryPage import *

class App(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        # self.iconbitmap(default="kankan_01.ico")
        self.wm_title("领普信号测试软件")

        # 修改默认字体大小
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=15)
        self.option_add("*Font", default_font)
        
        self.createWidgets()

    def createWidgets(self):
        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SignalTest, QueryPage, AboutPage):
            frame = F(container, self)
            self.frames[F] = frame
            # 四个页面的位置都是 grid(row=0, column=0), 位置重叠，只有最上面的可见！！
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(SignalTest)

    def addMenu(self, Menu):
        tkMenu(self)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()  # 切换，提升当前 Frame z轴顺序（使可见）！！此语句是本程序的点睛之处


class tkMenu():

    """docstring for tkMenu"""

    def __init__(self, root):
        menubar = Menu(root)
        menubar.add_command(
            label="测试", command=lambda: root.show_frame(SignalTest))
        menubar.add_command(
            label="查询", command=lambda: root.show_frame(QueryPage))
        menubar.add_command(label="说明", command=lambda: root.show_frame(AboutPage))

        root.config(menu=menubar)




class AboutPage(Frame):

    '''说明页'''

    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        Label(self, text="领普信号测试软件V0.2说明").pack(pady=10, padx=10)
        
        quote = """
        1.可以同时测量信号与发电量，也可以单独测其中一个
        2.如果信号与发电量没有显示，换串口号重新点击测试
        2.任何问题可以联系杨展
        ————————————————————————————
        V0.2更新日志：
        1.增加测发电量功能
        """
        labelText = Label(self, text=quote, justify="left").pack()


if __name__ == '__main__':
    app = App()
    app.addMenu(tkMenu)

    app.frames[SignalTest].testStart()

    def closeWindow():
        app.frames[SignalTest].testStop()    
        app.destroy()
    app.protocol('WM_DELETE_WINDOW', closeWindow)
    app.mainloop()

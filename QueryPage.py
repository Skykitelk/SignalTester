#!/usr/bin/env
# coding=utf-8
# Copyright By Yangzhan 20160908
from Tkinter import *
from ttk import *
from PySqlite import *


class QueryPage(Frame):

    '''第二页'''

    def __init__(self, parent, root):
        Frame.__init__(self, parent)
        

        # 数据库
        host = 'sqlite.db'
        self.table = 'PowerModelSignal'
        self.sqlite = PySqlite(host)
        
        self.values = {"SN": 'char(10)', "ID": 'char(10) UNIQUE', "type": 'char(3)', "num": 'char(3)', "signalTimes": 'char(3)',
        "PMState": 'int', 'testTime': 'char(15)'}
        self.createWidgets()
    def createWidgets(self):
        label = Label(self, text="查询")
        label.pack(pady=10, padx=10)

        columns=self.values.keys()
        tree = Treeview(self, show="headings", columns=columns)
        for i in range(len(columns)):
        	tree.heading(columns[i],text=columns[i])
        allData = self.sqlite.selectAll(self.table)
        print allData
        for i in range(len(allData)):
        	value=allData[i]
         	tree.insert('', i, values=value)
        tree.pack()
        
if __name__ == '__main__':
    root = Tk()
    container = Frame(root)
    container.pack(side="top", fill="both", expand=True)
    container.grid_rowconfigure(0, weight=1)
    container.grid_columnconfigure(0, weight=1)

    query = QueryPage(container, root)
    query.grid(row=0, column=0, sticky="nsew")

    root.mainloop()

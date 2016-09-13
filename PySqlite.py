# coding=utf-8
# copyRight By YangZhan 2016-09-06
import sqlite3


class PySqlite(object):

    """发电模块的sqlite模型 """

    def __init__(self, host):
        try:
            self.con = sqlite3.connect(host,check_same_thread=False)
            self.cur = self.con.cursor()
        except:
            print('数据库连接失败!')

    def query(self, sql):
        print sql
        try:
            self.cur.execute(sql)
            self.con.commit
        except sqlite3.Error, e:
            print e
            self.con.rollback()

    def create(self, table, value, main):
        """
        value：字典作为字段名和类型
        main：自增主键名
        """
        sql = 'create table if not exists '+table+' ('
        if main != False:
            sql += main+' INTEGER PRIMARY KEY AUTOINCREMENT,'
        name = []
        ztype = []
        for n in value.keys():
            name.append(n)
        for n in value.values():
            ztype.append(n)
        i = 0
        while i < len(value):
            if i == len(value)-1:
                sql += name[i]+' '+ztype[i].upper()+')'
            else:
                sql += name[i]+' '+ztype[i].upper()+','
            i += 1
        self.query(sql)

    def insert(self,table, value):
        """value为字典"""
        sql = 'replace into '+table+'('
        i = 0
        for n in value.keys():
            i = i+1
            if i != len(value):
                sql = sql+n+','
            else:
                sql = sql+n+')values('
        i = 0
        for n in value.values():
            i = i+1
            if i != len(value):
                sql = sql+"'"+n+"'"+','
            else:
                sql = sql+"'"+n+"'"+')'
        self.query(sql)

    def update(self,table, cname, cvalue, name, value):
        sql = 'update '+table+' set '+name+"='" + \
            value+"' where "+cname+"='"+cvalue+"'"
        self.query(sql)

    def select(self,table, name, vname, vvalue):
        sql = 'select '+name+' from '+table+' where '+vname+"='"+vvalue+"'"
        self.query(sql)
        rows = self.cur.fetchall()
        return rows

    def selectRange(self,table,name,vname,vvalueMin,vvalueMax):
        sql = 'select '+name+' from '+table+' where '+vname+">='"+vvalueMin+"'"+' and '+vname+"<='"+vvalueMax+"'"
        self.query(sql)
        rows = self.cur.fetchall()
        return rows

    def selectAll(self,table):
        sql = 'select * from ' +table
        self.query(sql)
        rows = self.cur.fetchall()
        return rows

    def delete(self,table, vname, vvalue, commit=True):
        sql = 'DELETE  FROM  '+table+' WHERE  '+vname+"='"+vvalue+"'"
        self.query(sql)

    def drop(self,table):
        sql = 'drop table if exists  '+table
        self.query(sql)

    def close(self):
        self.cur.close()
        self.con.commit()
        self.con.close()

if __name__ == '__main__':
    table = 'PowerModelTest'
    host = 'sqliteDB'
    sqlite = PySqlite(host)

    sqlite.drop(table)

    values = {"SN": 'int', "pressForce": 'int', "pressPoint": 'float', "reboundForce": 'int', "reboundPoint": 'float',
             "power": 'float', "magneticFlux": 'float', "signalTimes": 'int', "PMState": 'int'}
    sqlite.create(table,values,'ID')
    insertValue = {'SN':'644723742','pressForce':'190','power':'4.5'}
    sqlite.insert(table,insertValue)

    print sqlite.select(table,'*','pressForce','200')
    sqlite.update(table, cname='SN', cvalue='644723742', 
        name='magneticFlux', value='18.5')

    #print sqlite.selectAll(table)
    print sqlite.selectRange(table,'*','pressForce','180','195')

    sqlite.close()

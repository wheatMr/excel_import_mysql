# -*- coding: UTF-8 -*-
import xlrd
import demjson
import linecache
import MySQLdb


data = xlrd.open_workbook('datasheet.xls')
table = data.sheet_by_name(u'Sheet1')#通过名称获取
rows =table.nrows
cols =table.ncols

#创建本地json文件
# html = requests.get("http://api.fixer.io/2015-05-01?base=USD")
# a_josn = html.text
# with open('test03.txt', 'a') as f:
#     f.write('\n'+a_josn)

#定义不同货币对应年份的汇率
def exchange_RMB(year,price_unit):
    for i in range(1,rows):
        x= linecache.getline('test03.txt',i)
        price_exchange_CNY= demjson.decode(x)
        return price_exchange_CNY['rates']['CNY']

#在线获取
# def exchange_RMB(year,price_unit): #取到不同货币对应年份5月1号相应人民币的汇率
#     URL = 'http://api.fixer.io/'+str(year)+'-05-01?base='+price_unit
#     print URL
#     price_exchange= requests.get(URL)
#     text = price_exchange.text
#     x= linecache.getline('test03.txt',i)
#     print(x)
#     price_exchange_CNY= demjson.decode(text)
#     return price_exchange_CNY['rates']['CNY']



year_price2016 = table.row_values(0).index(u'2016年（价格）')# 从表头中取到“2016年（价格）”字段所在位置
year_price2015 = table.row_values(0).index(u'2015年（价格）')
unit = table.row_values(0).index(u'单位')


#数据转换
row_list = []
for i in range(1,rows):
    row_data = table.row_values(i)
    row_list.append(row_data)
    if row_data[unit] =='USD':
        new_USD_2016 = float(row_data[year_price2016])*exchange_RMB(2016,'USD')
        row_data[year_price2016]=new_USD_2016
        row_data[unit]='RMB'
        new_USD_2015=float(row_data[year_price2015])*exchange_RMB(2015,'USD')
        row_data[year_price2015]=new_USD_2015
        row_data[unit]='RMB'
    elif row_data[unit] =='EUR':
        new_EUR_2016=float(row_data[year_price2016])*exchange_RMB(2016,'EUR')
        row_data[year_price2016]=new_EUR_2016
        row_data[unit]='RMB'
        new_EUR_2015=float(row_data[year_price2015])*exchange_RMB(2015,'EUR')
        row_data[year_price2015]=new_EUR_2015
        row_data[unit]='RMB'
row_list[0][1]='耐克'
row_list[1][1]='苹果'



database = MySQLdb.connect (host="192.168.50.13", user = "root", passwd = "liang", db = "liang") #建立一个MySQL连接

# 清空表数据
cursor = database.cursor()# 获得游标对象
truncate_data= "truncate table PRODUCT_HISTOR;truncate table PRODUCT_INFO"
cursor.execute(truncate_data)
cursor.close()

cursor = database.cursor()
for row_numb in range(0,rows-1):

    row_list[row_numb].insert(-1,row_numb+1)#list中插入ID
    row_list[row_numb].insert(-4,'2015')
    row_list[row_numb].insert(-3,'2016')

    PRODUCT_HISTOR_2016=row_list[row_numb][-4:]
    PRODUCT_HISTOR_2015=row_list[row_numb][-6:-4]+row_list[row_numb][-2:]

    cursor.executemany(
      """INSERT INTO PRODUCT_INFO (category, brand, model, place_of_origin)
      VALUES (%s, %s, %s, %s)""",[tuple(row_list[row_numb][0:4])]
    )
    cursor.executemany(
      """INSERT INTO PRODUCT_HISTOR (year,prince,product_id,unit)
      VALUES (%s, %s,%s,%s)""",[tuple(PRODUCT_HISTOR_2015)]
    )
    cursor.executemany(
      """INSERT INTO PRODUCT_HISTOR (year,prince, product_id,unit)
      VALUES (%s, %s,%s,%s)""",[tuple(PRODUCT_HISTOR_2016)]
    )
cursor.close()
database.commit()
database.close()






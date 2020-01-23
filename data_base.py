# -*- coding: utf-8
import pymysql
from time import sleep

mysql = {'host': 'host',
         'user': 'user',
         'passwd': 'pass',
         'db': 'dbname'}

def get_photo_from_office():
    print('Trying to connect...')
    myDB = pymysql.connect(host=mysql['host'],port=3306,user=mysql['user'],passwd=mysql['passwd'],db=mysql['dbname'])
    cursor = myDB.cursor()

    cursor.execute("UPDATE `trigger` SET checkpoint='on';")
    print(myDB.commit(), ' and going to sleep for 14 seconds')
    sleep(14)
    cursor.execute("SELECT photo_id FROM `trigger`;")
    photo_id = cursor.fetchone()
    sql = "SELECT time, temperature, humidity, photo FROM `info` WHERE id = %s;"
    cursor.execute(sql, photo_id)
    myresult = cursor.fetchone()
    print(myresult)
    cursor.close()
    myDB.close()
    filename = 'msqlpics/raspberry_' + str(myresult[0])
    outfile=open(filename,'wb')
    outfile.write(myresult[3])
    outfile.close()
    time = myresult[0]
    temperature = myresult[1]
    humidity = myresult[2]
    print(time, temperature, humidity, filename)
    return time, temperature, humidity, filename


# def set_reboot():
#     myDB = pymysql.connect(host="79.111.246.189",port=3306,user="pi",passwd="matrega",db="office")
#     cursor = myDB.cursor()
#     cursor.execute("UPDATE `trigger` SET set_reboot='on';")
#     myDB.commit()
#     cursor.close()
#     myDB.close()
#     sleep(80)
#     myDB = pymysql.connect(host="79.111.246.189",port=3306,user="pi",passwd="matrega",db="office")
#     cursor = myDB.cursor()
#     cursor.execute("SELECT time FROM `reboot`;")
#     reboot_time = cursor.fetchone()
#     log_time = str(reboot_time[0])
#     cursor.close()
#     myDB.close()
#     time = 'Перезагрузка прошла успешно в ' + log_time
#     return time

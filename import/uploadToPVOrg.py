import sqlite3
import sys
import requests
import time

def main():
  conn = sqlite3.connect('..\\dB\\test.db')
  c = conn.cursor()
  to_upload = c.execute('SELECT max_time,power_kWh,max_power_kW FROM day_data WHERE uploaded=0;').fetchall()
  for data in to_upload:
    url='http://pvoutput.org/service/r2/addoutput.jsp?key=d4c306fcdc6ad0158a5cb0a29eaf819ba127a833&sid=17596'
    max_time = data[0]
    power_kWh = data[1]
    max_power_kW = data[2]
    d = max_time[0:4]+max_time[5:7]+max_time[8:10]
    g = str(1000 * power_kWh)
    pp = str(max_power_kW*1000)
    pt = max_time[11:16]
    url = url + '&d='+d+'&g='+g+'&pp='+pp+'&pt='+pt
    print url
    r = requests.get(url)
    if r.status_code == 200:
      q = 'UPDATE day_data set uploaded=1 where date="'+max_time[0:10]+'";'
      c.execute(q)
    else:
      print 'FAILED '+str(r.status_code)
      conn.commit()
      conn.close()
      exit(1)
    time.sleep(1)
  conn.commit()
  conn.close()

if __name__ == "__main__":
  main()
  

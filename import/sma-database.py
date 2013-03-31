import sqlite3
import sys
import requests
import time
import re

class sma_database:
  def __init__(self, filename):
    self._filename = filename

  def __enter__(self):
    self._conn = sqlite3.connect(self._filename)
    return self

  def commit(self):
    self._conn.commit()

  def __exit__(self, type, value, traceback):
    self._conn.close()

  def calculate_day_data(self):
    c = self._conn.cursor()
    times = c.execute('SELECT time FROM five_minute_data WHERE processed IS NULL;').fetchall()
    last_date = ''
    for time in times:
      date = time[0][0:10]
      if date != last_date:
        print date
        timeConstraint = "time BETWEEN '" + date + " 00:00:00' " + \
                         "AND '" + date + " 23:55:00';"
        where = "WHERE " + timeConstraint
        sumd = c.execute("SELECT SUM(power_kWh) FROM five_minute_data " + where).fetchone()[0]
        maxd = c.execute("SELECT MAX(total_power_kWh) FROM five_minute_data " + where).fetchone()[0]
        count = c.execute("SELECT COUNT(power_kWh) FROM five_minute_data " + where).fetchone()[0]
        max_power_kW = c.execute('SELECT MAX(power_kW) FROM five_minute_data '+where).fetchone()[0]
        max_time = c.execute('SELECT time FROM five_minute_data WHERE power_kW = '+str(max_power_kW)+' AND '+timeConstraint).fetchone()[0]
        res = c.execute('SELECT complete,total_power_kWh,max_power_kW,max_time FROM day_data WHERE date="'+date+'";').fetchone()
        if res is None:
          cmd = "INSERT INTO day_data VALUES ('"+date+"', "+str(maxd)+", "+str(sumd)+", "
          if count >= 200 :
            cmd = cmd + "1, "
          else:
            cmd = cmd + "0, "
          cmd = cmd + str(max_power_kW) +", '"+max_time+"', 0, NULL);"
          print cmd
          c.execute(cmd)
        elif res[1] != maxd:
          cmd = 'UPDATE day_data SET total_power_kWh='+str(maxd)+', power_kWh='+str(sumd)+', max_power_kW='+str(max_power_kW)+', max_time="'+max_time+'", processed=NULL WHERE date="'+date+'";'
          print cmd
          c.execute(cmd)
        c.execute('UPDATE five_minute_data SET processed=1 '+where)
      last_date = date

  def update_max_times(self):
    c = self._conn.cursor()
    dates = c.execute('SELECT date FROM day_data WHERE max_power_kW IS NULL;').fetchall()
    for date in dates:
      timeConstraint = 'time BETWEEN "'+date[0]+' 00:00:00" AND "'+date[0]+' 23:55:00"'
      c.execute('SELECT MAX(power_kW) FROM five_minute_data WHERE '+timeConstraint)
      max_power_kW = c.fetchone()[0]
      c.execute('SELECT time FROM five_minute_data WHERE power_kW = '+str(max_power_kW)+' AND '+timeConstraint)
      time = c.fetchone()[0]
      q='UPDATE day_data SET max_power_kW='+str(max_power_kW)+', max_time="'+time+'" WHERE date="'+date[0]+'";'
      print q
      c.execute(q)

  def calculate_month_data(self):
    c = self._conn.cursor()
    dates = c.execute('SELECT date FROM day_data WHERE processed IS NULL;').fetchall()
    last_month = ''
    for date in dates:
      month = date[0][0:7]+'-01'
      if month != last_month:
        where = "WHERE date BETWEEN '" + month + \
                "' AND date('"+month+"','+1 month', '-1 day');"
        sumd = c.execute("SELECT SUM(power_kWh) FROM day_data " + where).fetchone()[0]
        maxd = c.execute("SELECT MAX(total_power_kWh) FROM day_data " + where).fetchone()[0]
        count = c.execute("SELECT COUNT(power_kWh) FROM day_data " + where).fetchone()[0]
        insert = "INSERT INTO month_data VALUES ('"+month+"', "+str(maxd)+", "+str(sumd)+", 1, null);"
        if c.execute('SELECT * from month_data WHERE date="'+month+'";').fetchone() is not None:
          insert = 'UPDATE month_data SET total_power_kWh='+str(maxd)+',power_kWh='+str(sumd)+', processed=NULL WHERE date="'+month+'";'
        print insert
        c.execute(insert)
        c.execute('UPDATE day_data SET processed=1 '+where);
      last_month = month

  def calculate_year_data(self):
    c = self._conn.cursor()
    dates = c.execute('SELECT date FROM month_data WHERE processed IS NULL;').fetchall()
    last_year = ''
    for date in dates:
      year = date[0][0:4]+'-01-01'
      if year != last_year:
        where = "WHERE date BETWEEN '" + year + \
                "' AND date('"+year+"','+1 year', '-1 day');"
        sumd = c.execute("SELECT SUM(power_kWh) FROM month_data " + where).fetchone()[0]
        maxd = c.execute("SELECT MAX(total_power_kWh) FROM month_data " + where).fetchone()[0]
        count = c.execute("SELECT COUNT(power_kWh) FROM month_data " + where).fetchone()[0]
        insert = "INSERT INTO year_data VALUES ("+year+", "+str(maxd)+", "+str(sumd)+", 1);"
        if c.execute('SELECT * from year_data WHERE date='+year+';').fetchone() is not None:
          insert = 'UPDATE year_data SET total_power_kWh='+str(maxd)+',power_kWh='+str(sumd)+' WHERE date='+year+';'
        print insert
        c.execute(insert)
        c.execute('UPDATE month_data SET processed=1 '+where);
      last_year = year

  def upload_day_data(self):
    c = self._conn.cursor()
    to_upload = c.execute('SELECT max_time,power_kWh,max_power_kW FROM day_data WHERE uploaded=0 AND complete=1;').fetchall()
    for data in to_upload:
      url='http://pvoutput.org/service/r2/addoutput.jsp?key=d4c306fcdc6ad0158a5cb0a29eaf819ba127a833&sid=17596'
      print data
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
        return
      time.sleep(1)

  def import_data(self, filename):
    p = re.compile("^(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)\s+total=([0-9.]+)\s+Kwh\s+current=(\d+)\s+Watts\s+togo=\d+\s+i=\d+\s+crc=\d+")
    c = self._conn.cursor()
    with open(filename, 'r') as f:
      line = f.readline()
      old_date=''
      while line:
        m = p.match(line)
        if m is not None:
          year = m.group(3)
          month = '%02d' % int(m.group(2))
          day = '%02d' % int(m.group(1))
          hour = m.group(4)
          minute = m.group(5)
          second = m.group(6)
          total_power_kWh = m.group(7)
          power_kW = float(m.group(8))/1000
          date = year+'-'+month+'-'+day
          time = date+' '+hour+':'+minute+':'+second
          c.execute('SELECT * from five_minute_data WHERE time="'+time+'";')
          res = c.fetchone()
          if res is None:
            # New piece of data
            cmd = 'INSERT INTO five_minute_data VALUES (' + \
                   '"'+time+'",' + total_power_kWh + ', ' + str(power_kW) + ', ' + \
                   str(power_kW/12.0) + ', null);'
            c.execute(cmd)
            # If there is an entry for date already, then update the "complete" field for that day to
            # incomplete
            if date != old_date:
              c.execute('SELECT complete FROM day_data WHERE date="'+date+'";')
              res = c.fetchone()
              if res is not None:
                c.execute('UPDATE day_data SET complete=0 WHERE date="'+date+'";')
          old_date = date
        line = f.readline()

  def calculate_all_data(self):
    self.calculate_day_data()
    self.calculate_month_data()
    self.calculate_year_data()

  def do_import(self, filename):
    self.import_data(filename)
    self.calculate_all_data()
    self.upload_day_data()

def main():
  with sma_database('..\\dB\\test.db') as db:
    db.do_import('fullOutput')
    db.commit()

if __name__ == "__main__":
  main()
  

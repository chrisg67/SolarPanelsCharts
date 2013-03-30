import sqlite3
import sys
import re

def update_db(filename):
  p = re.compile("^(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)\s+total=([0-9.]+)\s+Kwh\s+current=(\d+)\s+Watts\s+togo=\d+\s+i=\d+\s+crc=\d+")
  conn = sqlite3.connect('..\\dB\\test.db')
  c = conn.cursor()
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
        date = year+'-'+month+'-'+day+
        time = date+' '+hour+':'+minute+':'+second
        c.execute('SELECT * from five_minute_data WHERE time="'+time+'";')
        res = c.fetchone()
        if res is None:
          # New piece of data
          cmd = 'INSERT INTO five_minute_data VALUES (' + \
                 '"'+time+'",' + total_power_kWh + ', ' + str(power_kW) + ', ' + \
                 str(power_kW/12.0) + ');'
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
  conn.commit()
  conn.close()

def main():
  update_db('output')

if __name__ == "__main__":
  main()


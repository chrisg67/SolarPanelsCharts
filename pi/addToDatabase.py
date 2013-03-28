import sqlite3
import sys
import re

def main():
  p = re.compile("^(\d+)/(\d+)/(\d+) (\d+):(\d+):(\d+)\s+total=([0-9.]+)\s+Kwh\s+current=(\d+)\s+Watts\s+togo=\d+\s+i=\d+\s+crc=\d+")
  conn = sqlite3.connect('..\\dB\\test.db')
  c = conn.cursor()
  with open('fullOutput', 'r') as f:
    line = f.readline()
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
        time = year+'-'+month+'-'+day+' '+hour+':'+minute+':'+second
        c.execute('SELECT * from five_minute_data WHERE time="'+time+'";')
        res = c.fetchone()
        if res is None:
          cmd = 'INSERT INTO five_minute_data VALUES (' + \
                 '"'+time+'",' + total_power_kWh + ', ' + str(power_kW) + ', ' + \
                 str(power_kW/12.0) + ');'
          print cmd
          c.execute(cmd)
      line = f.readline()
  conn.commit()
  conn.close()

if __name__ == "__main__":
  main()


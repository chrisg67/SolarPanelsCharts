import sqlite3
import sys

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
        where = "WHERE time BETWEEN '" + date + " 00:00:00' " + \
                "AND '" + date + " 23:55:00';"
        sumd = c.execute("SELECT SUM(power_kWh) FROM five_minute_data " + where).fetchone()[0]
        maxd = c.execute("SELECT MAX(total_power_kWh) FROM five_minute_data " + where).fetchone()[0]
        count = c.execute("SELECT COUNT(power_kWh) FROM five_minute_data " + where).fetchone()[0]
        res = c.execute('SELECT complete,total_power_kWh FROM day_data WHERE date="'+date+'";').fetchone()
        if res is None:
          cmd = "INSERT INTO day_data VALUES ('"+date+"', "+str(maxd)+", "+str(sumd)+", "
          if count >= 200 :
            cmd = cmd + "1, NULL, NULL, 0)"
          else:
            cmd = cmd + "0, NULL, NULL, 0)"
          print cmd
          c.execute(cmd)
        else:
          t = res[1]
          if t != maxd:
            cmd = 'UPDATE day_data SET total_power_kWh='+str(maxd)+', power_kWh='+str(sumd)+' WHERE date="'+date+'";'
            print cmd
            c.execute(cmd)
        c.execute('UPDATE five_minute_data SET processed=1 '+where)

def main():
  with sma_database('..\\dB\\test.db') as db:
    db.calculate_day_data()
    db.commit()

if __name__ == "__main__":
  main()
  

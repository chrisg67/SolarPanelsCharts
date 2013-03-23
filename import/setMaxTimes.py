import sqlite3
import sys

def main():
  conn = sqlite3.connect('..\\dB\\test.db')
  c = conn.cursor()
  dates = c.execute('SELECT date FROM day_data WHERE max_power_kW IS NULL;').fetchall()
  for date in dates:
    timeConstraint = 'time BETWEEN "'+date[0]+' 00:00:00" AND "'+date[0]+' 23:55:00"'
    c.execute('SELECT MAX(power_kW) FROM five_minute_data WHERE '+timeConstraint)
    max_power_kW = c.fetchone()[0]
    c.execute('SELECT time FROM five_minute_data WHERE power_kW = '+str(max_power_kW)+' AND '+timeConstraint)
    time = c.fetchone()[0]
    q='UPDATE day_data SET max_power_kW='+str(max_power_kW)+', max_time='+time+' WHERE date="'+date[0]+'";'
    print q
    #c.execute(count)
    #countv = c.fetchone()[0]
    #if ( countv > 0 ):
      ## Complete Year
      #c.execute(sumd)
      #sumv = c.fetchone()[0]
      #c.execute(maxd)
      #maxv = c.fetchone()[0]
      #insert = "INSERT INTO year_data VALUES ("+date+", "+str(maxv)+", "+str(sumv)+", 1);"
      #print insert
      #conn.execute(insert)
  #conn.commit()
  conn.close()

if __name__ == "__main__":
  main()
  

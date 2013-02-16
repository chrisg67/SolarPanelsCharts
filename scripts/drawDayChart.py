from pageLayout import WebPage
import sqlite3

def main():
  conn = sqlite3.connect('../dB/test.db')
  c    = conn.cursor()
  today = c.execute("SELECT date('now');").fetchone()[0]
  thisMonth = c.execute("SELECT date('now', 'start of month');").fetchone()[0]
  
  page = WebPage("today.html", "Today's Power")
  page.addNav("Today", "today.html", True)
  page.addNav("Month", "month.html")
  page.addNav("Year", "year.html")
  for m in range(-5, 1):
    month = c.execute("SELECT date('" + thisMonth + "', '" + str(m) + " months');").fetchone()[0]
    month = month[:7]
    page.addSideNav(month+".html", month, "Results for "+month, "Monthly Report for "+month)
  page.writeHeader()
  page.writeNavs()
  page.writeDayGraph(c, today)
  page.writeSideNavs()
  page.writeFooter()  

if __name__ == "__main__":
  main()

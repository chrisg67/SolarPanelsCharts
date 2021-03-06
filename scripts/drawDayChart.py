from pageLayout import WebPage
from optparse import OptionParser
import sqlite3

def drawChart(date, page):
  conn = sqlite3.connect('../dB/test.db')
  c    = conn.cursor()
  page.addNav("Today", "today.html", True)
  page.addNav("Month", "month.html")
  page.addNav("Year", "year.html")
  page.addStandardSideNav(c, date, "day.month")
  page.writeHeader()
  page.writeNavs()
  page.writeDayGraph(c, date)
  page.writeSideNavs()
  page.writeFooter()  

def main():
  parser = OptionParser()
  parser.add_option("-a", "--all", dest="all", action="store_true",
                    help="create all day charts")

  (options, args) = parser.parse_args()

  cmd = "SELECT date('now');" # By default draw for today
  if options.all:
    cmd = "SELECT date FROM day_data;" # Optionally draw for all months

  conn = sqlite3.connect('../dB/test.db')
  c = conn.cursor()
  for d in c.execute(cmd):
    date = d[0]
    page = WebPage(date+".html", date)
    drawChart(date, page)

if __name__ == "__main__":
  main()

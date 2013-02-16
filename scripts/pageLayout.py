#!/usr/bin/python
import time
import sys
import sqlite3

class WebPage:

  def __init__(self, filename, title):
    self.f = open(filename, "w")
    self.navs = []
    self.side_navs = []
    self.title = title

  def addNav(self, name, link, current=False):
    self.navs.append({'name':name, 'link':link, 'current':current})

  def addSideNav(self, name, link, title, span):
    self.side_navs.append({'name':name, 'link':link, 'title':title, 'span':span})

  def writeHeader(self):
    self.f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n')
    self.f.write('\n')
    self.f.write('<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">\n')
    self.f.write('\n')
    self.f.write('<head>\n')
    self.f.write('\n')
    self.f.write('<title>Chris & Claire\'s Solar Panels</title>\n')
    self.f.write('\n')
    self.f.write('<meta http-equiv="content-type" content="application/xhtml+xml; charset=UTF-8" />\n')
    self.f.write('<meta name="author" content="Chris Goldsmith" />\n')
    self.f.write('<meta name="description" content="A Collection of pages representing output from our panels" />\n')
    self.f.write('<!--<meta name="keywords" content="keywords, here" />\n')
    self.f.write('<meta name="robots" content="index, follow, noarchive" />\n')
    self.f.write('<meta name="googlebot" content="noarchive" />-->\n')
    self.f.write('\n')
    self.f.write('<link rel="stylesheet" type="text/css" media="screen" href="css/screen.css" />\n')
    self.f.write('\n')
    self.f.write('</head>\n')
    self.f.write('\n')
    self.f.write('<body>\n')
    self.f.write('\n')
    self.f.write('<!-- wrap starts here -->\n')
    self.f.write('<div id="wrap">\n')
    self.f.write('\n')
    self.f.write('  <!--header -->\n')
    self.f.write('  <div id="header">\n')
    self.f.write('\n')
    self.f.write(' 	 <h1 id="logo-text"><a href="index.html" title="">Solar Panels</a></h1>\n')
    self.f.write('    <p id="slogan">Feel the power...</p>\n')
    self.f.write('\n')

  def writeNavs(self):
    self.f.write(' 	 <div  id="nav">\n')
    self.f.write(' 		 <ul>\n')
    for nav in self.navs:
      if nav['current']:
        self.f.write(' 			 <li class="first" id="current"><a href="' + nav['link'] + '">' + nav['name'] + '</a></li>\n')
      else:
        self.f.write(' 			 <li><a href="' + nav['link'] + '">' + nav['name'] + '</a></li>\n')
    self.f.write(' 		 </ul>\n')
    self.f.write(' 	 </div>\n')
    self.f.write('\n')
    self.f.write(' 	 <div id="header-image"></div>\n')
    self.f.write('\n')
    self.f.write('  <!--header ends-->\n')
    self.f.write('  </div>\n')
    self.f.write('\n')
    self.f.write('  <!-- content -->\n')
    self.f.write('  <div id="content-outer" class="clear"><div id="content-wrap">\n')
    self.f.write(' 	 <div id="content">\n')
    self.f.write('      <div class="left" style="width: 60%; float:left;">\n')
    self.f.write('        <div class="entry">\n')
    self.f.write('          <h3>' + self.title + '</h3>\n')

  def writeDayGraph(self, c, day):
    cmd = "SELECT power_kWh " + \
          "FROM day_data " + \
          "WHERE date == '"+day+"';"
    print cmd
    total = c.execute(cmd).fetchone()[0]
    print total

    self.f.write('          <p>'+str(round(total,3))+'KWh</p>\n')
    self.f.write('<script type="text/javascript" src="https://www.google.com/jsapi"></script>\n')
    self.f.write('<script type="text/javascript">\n')
    self.f.write('  google.load("visualization", "1", {packages:["corechart"]});\n')
    self.f.write('  google.setOnLoadCallback(drawChart);\n')
    self.f.write('  function drawChart() {\n')
    self.f.write('    var data = new google.visualization.DataTable();\n')
    self.f.write('    data.addColumn(\'datetime\', \'Time\');\n')
    self.f.write('    data.addColumn(\'number\', \'KW\');\n')
    self.f.write('    data.addColumn(\'number\', \'KWh\');\n')
    self.f.write('    data.addRows([\n')
    cmd = "SELECT time,power_kWh " + \
          "FROM five_minute_data " + \
          "WHERE time BETWEEN '"+day+" 00:00:00' AND '"+day+" 23:55:00';"
    total = 0.0
    for v in c.execute(cmd):
      total = total + v[1]
      self.writeDayValue(v, tot)
      if v[0][11:16] == '23:55':
        self.f.write('\n')
      else:
        self.f.write(',\n')
    self.f.write('    ]);\n')
    self.f.write('\n')
    self.f.write('    // Create and draw the visualization.\n')
    self.f.write('    new google.visualization.LineChart(document.getElementById(\'chart_div\')).\n')
    self.f.write('        draw(data, {vAxes: {0: {maxValue: 4},\n')
    self.f.write('                            1: {maxValue: 30}},\n')
    self.f.write('                    hAxis: {viewWindowMode: \'pretty\',\n')
    self.f.write('                            maxValue: new Date('+time.strftime('%Y,%m-1,%d', vals[0][0])+',23,59,00)},\n')
    self.f.write('                    series: {0:{targetAxisIndex:0},\n')
    self.f.write('                             1:{targetAxisIndex:1}}\n')
    self.f.write('                   }\n')
    self.f.write('            );\n')
    self.f.write('  }\n')
    self.f.write('\n')
    self.f.write('</script>\n')
    self.f.write('<div id="chart_div" style="width: 100%; height: 500px; position: relative; "></div>\n')
    self.f.write('\n')
    self.f.write('        </div>\n')
    self.f.write('      </div>\n')

  def writeDayValue(self, val, tot):
    d = val[0]
    self.f.write('      [new Date('+d[0:4]+','+d[5:7]+','+d[8:10]+','+d[11:13]+','+d[14:16]+','+d[17:19]+'), ' + str(round(val[1],3))+', '+str(round(tot,3))+']')

  def writeMonthGraph(self, vals):
    self.f.write('<script type="text/javascript" src="https://www.google.com/jsapi"></script>\n')
    self.f.write('<script type="text/javascript">\n')
    self.f.write('  google.load("visualization", "1", {packages:["corechart"]});\n')
    self.f.write('  google.setOnLoadCallback(drawChart);\n')
    self.f.write('  function drawChart() {\n')
    self.f.write('    var data = new google.visualization.DataTable();\n')
    self.f.write('    data.addColumn(\'string\', \'Day\');\n')
    #self.f.write('    data.addColumn(\'number\', \'Estimate\');\n')
    self.f.write('    data.addColumn(\'number\', \'Average\');\n')
    self.f.write('    data.addColumn(\'number\', \'KWh\');\n')
    self.f.write('    data.addRows([\n')

    i = 0
    tot = 0.0
    for v in vals:
      if i != 0:
        self.f.write(',\n')
      i = i + 1
      tot = tot + float(v[2])
      self.writeMonthValue(v, tot / i)
    self.f.write('    ]);\n')
    self.f.write('\n')
    self.f.write('    var options = {\n')
    self.f.write('      title: \'Solar Panel Output\',\n')
    self.f.write('      vAxis: {title:"KWh", viewWindowMode: \'explicit\', viewWindow:{max:30, min:0}},\n')
    self.f.write('      seriesType:"bars",\n')
    #self.f.write('      series: { 0: {type: "line"} }\n')
    self.f.write('    };\n')
    self.f.write('\n')
    self.f.write('    var chart = new google.visualization.ComboChart(document.getElementById(\'chart_div\'));\n')
    self.f.write('    chart.draw(data, options);\n')
    self.f.write('  }\n')
    self.f.write('\n')
    self.f.write('</script>\n')
    self.f.write('<div id="chart_div" style="width: 100%; height: 500px; position: relative; "></div>\n')
    self.f.write('\n')
    self.f.write('        </div>\n')
    self.f.write('      </div>\n')

  def writeMonthValue(self, val, av):
    self.f.write('      [\''+time.strftime('%d', val[0])+'\', '+str(round(av,3))+', '+str(round(val[2],3))+']')


  def writeSideNavs(self):
    self.f.write(' 		 <div id="right">\n')
    self.f.write('        <div class="sidemenu">\n')
    self.f.write(' 				 <h3>Other Pages</h3>\n')
    self.f.write(' 				 <ul>\n')
    for nav in self.side_navs:
      self.f.write(' 					 <li><a href="' + nav['link'] + '" title="' + nav['title'] + '">' + nav['name'] + '<br />\n')
      self.f.write('               <span>' + nav['span'] + '</span></a>\n')
      self.f.write('           </li>\n')
    self.f.write(' 				 </ul>\n')
    self.f.write(' 			 </div>\n')
    self.f.write(' 		 </div>\n')

  def writeFooter(self):
    self.f.write(' 	 </div>\n')
    self.f.write('\n')
    self.f.write('  <!-- content end -->\n')
    self.f.write('  </div></div>\n')
    self.f.write('\n')
    self.f.write('  <!-- footer-bottom starts -->\n')
    self.f.write('  <div id="footer-bottom">\n')
    self.f.write(' 	 <div class="bottom-left">\n')
    self.f.write(' 		 <p>\n')
    self.f.write(' 		 &copy; 2012 <strong>Chris Goldsmith</strong>&nbsp; &nbsp; &nbsp;\n')
    self.f.write(' 		 Design by <a href="http://www.styleshout.com/">styleshout</a>\n')
    self.f.write(' 		 </p>\n')
    self.f.write(' 	 </div>\n')
    self.f.write('\n')
    self.f.write(' 	 <div class="bottom-right">\n')
    self.f.write(' 		 <p>\n')
    self.f.write(' 			 <a href="http://jigsaw.w3.org/css-validator/check/referer">CSS</a> |\n')
    self.f.write(' 	   	 <a href="http://validator.w3.org/check/referer">XHTML</a>	|\n')
    self.f.write(' 			 <a href="index.html">Home</a> |\n')
    self.f.write(' 		 </p>\n')
    self.f.write(' 	 </div>\n')
    self.f.write('  <!-- footer-bottom ends -->\n')
    self.f.write('  </div>\n')
    self.f.write('\n')
    self.f.write('<!-- wrap ends here -->\n')
    self.f.write('</div>\n')
    self.f.write('\n')
    self.f.write('</body>\n')
    self.f.write('</html>\n')

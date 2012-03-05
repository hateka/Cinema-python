# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib
import re
import sys

import unittest

class Screen(object):
   NAME = {
          'movix':'http://www.movix.co.jp/app/SMTT000000032_CALENDAR.html',
          'cine':'none',
          'kyoto':'none',
          'toho':'none',
          'gion':'none',
          'minami':'none',
          'ion':'none'
           }

   def __init__(self):
       argvs = sys.argv
       argc = len(argvs)
       self.theater = None
       self.url = None

       if argc == 2:
          if argvs[1] in self.NAME.keys():
             self.theater = argvs[1]
             self.url = self.NAME[self.theater]

class Movie(object):
   def __init__(self,theater,url):
       self.url = url
       self.obj = []
       self.movie_list = []
       self.time_list = []
       self.line = ''
       self.second_line = ''
       self.page = ''
       self.week = ''

   def parse_url(self,tag,att):
       obj = []

       try:
           read = urllib.urlopen(self.url).read()
           read = re.sub(r'.*;','',read)
           read = read.decode('shift-jis')
           comp_read = BeautifulSoup(read)
 
           if att == None:
              for i in comp_read(tag):
                  ko = i.encode("utf-8")
                  obj.append(ko)
              return obj
           else:
               for i in comp_read(tag,att):
                   ko = i.encode("utf-8")
                   obj.append(ko)
               return obj
       except:
           return []

   def spli(self,moli):
       vo = []
       for h in range(len(moli)):
           vo.append(h)
       return vo

   def show_time(self):
       times = self.parse_url('td',{'class':'on'})
       times2 = self.parse_url('td',{'class':'on2'})
       weekd = self.parse_url('th',None)
 
       k = re.compile('(\d+:\d+).*')
       self.week = self.get_week(weekd)
       self.line = self.search_time(times,times,k)
       self.second_line = self.search_time(times2,times2,k)

   def lines(self,p):
       b = []
       for i in range(0,len(p),5):
          m = []
          for j in range(i,i+5):
             m.append(p[j])
          b.append(m)
       return b

   def get_week(self,weekd):
       datet = re.compile(r'<th.*?>(<a\s.*>)?(.*)(</a>)?.*(.*)</th>')
       kon = re.compile(r'.*(\d)')
       listn = []
       vc = 0
       for i in weekd:
           if vc >=1 and vc<=7:
              date = datet.search(i).group(1)
              day = datet.search(i).group(2)
              try:
                 date = kon.search(date).group(1)
              except:
                 pass
              listn.append('3/'+str(date)+'('+str(day)+')')
           vc +=1
       return listn

   def search_time(self,times,times_num,word):
       time_list = []
       for i in range(len(times_num)):
           dn = str(times[i])
           try:
            pint = word.search(dn).group()
            time_list.append(pint)
           except:
            pass
       return time_list

   def main(self):
       no = self.parse_url('li',None)
       gr = self.spli(no)
       p = re.compile('<li><a\shref=\".*>.+</a></li>$')
       gn = re.compile('\">.+</a')

       for j in range(len(gr)):
           ro = str(no[j])
           try:
             pin = p.search(ro).group()
             self.movie_list.append(gn.search(pin).group().replace('</a','').replace('\">',''))
           except AttributeError:
             pass
       return self.movie_list

class TimeTable(Movie):
   def __init__(self,theater,url):
       mo = Movie(theater,url)
       self.title = mo.main()
       mo.show_time()
       a = mo.lines(mo.line)
       b =  mo.lines(mo.second_line)
       tmptitlelist = []
       titlelist = []
       for i in range(len(self.title)):
           if i % 3 == 0 or i % 3 >=0:
              tmptitlelist.append(self.title[i])
       for i in tmptitlelist:
          if i not in titlelist:
             titlelist.append(i)
       pin = zip(a,b)
       za = {}
       lp = []

       for g in pin:
          for c in g:
             lp.append(c)
       num = 0
       for j in titlelist:
          za[j] = lp[num]
          num+=1

       for x in za.keys():
          print '\n'+str(x)
          print '|'.join(mo.week)
          print str(za[x]).replace('<br />',' ').replace('</td>','|')

if __name__ == '__main__':
    the = Screen()
    if the.theater and the.url:
       TimeTable(the.theater,the.url)




import requests, re, sys, time
from bs4 import BeautifulSoup
from functools import partial
from multiprocess import Pool, TimeoutError, cpu_count

class SearchEngine():
    def __init__(self, name):
          self.name = name


class Google(SearchEngine):
    def search_for(self, string, start):
        urls = []
        payload = { 'q' : string, 'start' : start }
        headers = { 'User-agent' : 'Mozilla/11.0' }
        req = requests.get( 'http://www.google.com/search',payload, headers = headers )
        soup = BeautifulSoup( req.text, 'html.parser' )
        h3tags = soup.find_all( 'h3', class_='r' )
        for h3 in h3tags:
            try:
                urls.append( re.search('url\?q=(.+?)\&sa', h3.a['href']).group(1) )
            except:
                continue
        return urls

class Bing(SearchEngine):
    def search_for(self, string, start):
        urls = []
        payload = { 'q' : string, 'first' : start }
        headers = { 'User-agent' : 'Mozilla/11.0' }
        req = requests.get( 'https://www.bing.com/search',payload, headers = headers )
        soup = BeautifulSoup( req.text, 'html.parser' )
        h3tags = soup.find_all( 'li', class_='b_algo' )
        for h3 in h3tags:
            try:
                urls.append(h3.find('a').attrs['href'])
            except:
                continue
        return urls

class Baidu(SearchEngine):
    def search_for(self, string, start):
        urls = []
        payload = { 'wd' : string, 'pn' : start }
        headers = { 'User-agent' : 'Mozilla/11.0' }
        req = requests.get( 'http://www.baidu.com/s',payload, headers = headers)
        soup = BeautifulSoup( req.text, 'html.parser' )
        h3tags = soup.find_all( 'h3', class_='t' )
        for url in soup.find_all('h3', class_='t'):
            try:
                urlu = url.find('a').attrs['href']
                link = requests.get(urlu)
                urls.append(link.url)
            except:
                continue
        return urls



def printf(lista): 
      for i in lista:
            link = str(i)
            ch = link.replace("%3F", "?")
            ch2 = ch.replace("%3D","=")
            print( " " + ch2 )

def main():
      usage = """      Usage:
        Mass_Exploiter.py <search> <pages> <processes>

            <search>          String to be searched for 
            <engine>          Search engine to be used
            <pages>           Number of pages to search in
            <processes>       Number of parallel processes"""

      try:
            string = sys.argv[1]
            engine = sys.argv[2]
            page   = sys.argv[3]
            proc    = int( sys.argv[4]  )

            if string.lower() == "-h" or string.lower() == "--help":
                  print(usage)
                  exit(0)

      except:
            print(" * * Error * * Arguments missing")
            print("\n"+usage)
            exit(0)
      start_time = time.time()
      result = []
      pages = []

      for p in range( 0, int(page)):
            pages.append(p*10)

      p = Pool(proc) 
      print "#################################################"
      print "Searching for: "+str(string)+" in "+str(page)+" page(s) of "+str(engine)+" with "+str(proc)+" process(es)"
      print "#################################################"
      print "\n"
      if engine == "google":
          search = Google(engine)
          request = partial( search.search_for, string )
          all = p.map(request, pages)

      elif engine == "bing":
          search = Bing(engine)
          request = partial( search.search_for, string )
          all = p.map(request, pages)

      elif engine == "baidu":
          search = Baidu(engine)
          request = partial( search.search_for, string )
          all = p.map(request, pages)
      else:
          pass

      for p in all:
            result += [ u for u in p]
            printf( set( result ) )
      print "\n"
      print "#################################################"
      print( " Number of urls : " + str( len( result ) ) )
      print( " Finished in : " + str( int( time.time() - start_time ) ) + "s")
      print "#################################################"

if __name__ == '__main__':
      main()

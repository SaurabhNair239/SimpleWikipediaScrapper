from bs4 import BeautifulSoup
import requests
import json
import pandas as pd
def Crawler(main_link,main_page):
  if main_link and main_page:
    i = 0
    scrawlled = set()
    Page_count = []
    internal_link_count = []
    external_link_count = []
    URLFragment_link_count = []
    timestamps = []
    internal_link = set()
    internal_link.add(main_page)
    while i <= 200:
      if len(internal_link) > 0:

          internal_counter = set()
          external_counter = set()
          URLFragment_counter = set()
          all_pages = set()
          inter = internal_link.pop()
          scrawlled.add(inter)
          html = requests.get(main_link+inter).text
          soap_obj = BeautifulSoup(html,'html.parser')
          for links in soap_obj.find_all("a"):
              all_pages.add(links.get('href'))
          #internal Link
          for link in all_pages:
              if link:
                  if link.startswith('/wiki/'):
                      if i == 0:
                          internal_link.add(link)
                      else:
                          internal_counter.add(link)
                          if link not in scrawlled:
                              internal_link.add(link)
          if i == 0:
              internal_link_count.append(len(internal_link))
          else:
              internal_link_count.append(len(internal_counter))

          #External Link
          for link in all_pages:
              if link:
                  if link.startswith('https'):
                      external_counter.add(link)
          external_link_count.append(len(external_counter))

          # URLFragment Link
          for link in all_pages:
              if link:
                  if link.startswith('#'):
                      URLFragment_counter.add(link)
          URLFragment_link_count.append(len(URLFragment_counter))

          #timestamp
          timestamp = soap_obj.find_all('script', type='application/ld+json')
          for time in timestamp:
            if len(time.text) > 0:
              date_time = json.loads(time.text)['dateModified']
            else:
              date_time = 'None'
          timestamps.append(date_time)
          Page_count.append(i+1)
          i+=1
    dict = {'Pagecount':Page_count,'INTcount':internal_link_count,'EXTcount':external_link_count,'URLfragments':URLFragment_link_count,'timestammp':timestamps}
    return pd.DataFrame(dict)

Data = Crawler('https://simple.wikipedia.org', '/wiki/Climate_change')
print(Data)

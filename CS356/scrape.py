import requests
import re
from bs4 import BeautifulSoup 
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from urllib.request import urlopen
import shutil
import threading
from threading import Thread, Lock
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
import glob, os


TRUE_DIRECTORY =  "urls/*urls" # "urls/test_urls" #


state = "return document.readyState"
lock = Lock()
cur_lock = Lock()
def grab_html(url):
   
   # acquire the lock
   options = webdriver.ChromeOptions();
   options.add_argument('headless');
   options.add_argument('window-size=1200x600');
   try:
      browser = webdriver.Chrome(options=options)
   except:
      print("Couldn't open Chrome")
      return "hello"

   try:
      browser.get(url)
   except:
      print(f"URLS: {url}")
   try:
      WebDriverWait(browser, 3).until(lambda d: d.execute_script(state) == "complete")
   except:
       print(f"TIMEOUT: {url}")
   finally: 
      html = browser.page_source
      browser.quit()

   a = html.split('"')
   html = " ".join(a)
   with lock:
      print(f'DONE: {url}\n')

   return html 

def find_links(url):
   html = grab_html(url)
   urls = re.findall("(?P<url>https?://[^\s]+)", html)
   urls.append(url)
   return urls

def get_all_urls(name): #file_name: urls/bank_urls
   f = open(name)
   return f.readlines() #list of urls

def slice_per(source, step):
    return [source[i::step] for i in range(step)]

def load_current_links(file_name): #file_name: urls/bank_urls
   list_of_urls = get_all_urls(file_name) #list of urls
   threads = list()
   for urls in slice_per(list_of_urls, 5):
      with ThreadPoolExecutor(max_workers = 20) as executor:
         print(f"LOAD SIZE {len(urls)}")
         print(urls)
         results = executor.map(find_links, urls, timeout=5)
      f = open(f"found_no_repeating_domain/{file_name.split('/')[1]}_links.txt", "a")
      for result in results:
         if result == []: continue
         last_url = result[-1] 
         for url in result:
            try:
               search_domain = urlparse(url).hostname
            except ValueError as err:
               print(f'{err}: {url}')
               continue
            if  search_domain is None or  search_domain in last_url: continue
            f.write(f"{url}\n")
      print('First Write Finished')
      f.close()

def grab_all_filenames():
   return  glob.glob(TRUE_DIRECTORY)

def main():
   filenames = grab_all_filenames()
   for name in filenames: #loop through individual files
      print("*"*40)
      print(f"FILE {name}")
      print("*"*40)
      load_current_links(name) #name of file!
      shutil.move(name, "./done")
   
if __name__ == "__main__":
    main()





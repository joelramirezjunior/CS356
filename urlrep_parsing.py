#!/usr/bin/python3

# To run the script just use this:
# python3 /path/to/script.py /path/to/file/with/urls.txt /path/to/output/file.csv

import requests
import urllib.parse
import json
import sys
import os
import time

apivoid_key = None

try:
   my_file = sys.argv[1]
   csv_file = sys.argv[2]
except:
   print("Usage: " + os.path.basename(__file__) + " </path/to/file/with/urls.txt> </path/to/output/file.csv>")
   sys.exit(1)

def apivoid_urlrep(key, url):
   try:
      r = requests.get(url='https://endpoint.apivoid.com/urlrep/v1/pay-as-you-go/?key='+key+'&url='+urllib.parse.quote(url))
      return json.loads(r.content.decode())
   except:
      return ""

def submit_url(url):
    data = apivoid_urlrep(apivoid_key, url)
    if(data):
        if(data.get('error')):
            print("Error: "+data['error'])
        else:
            with open(csv_file, 'a') as f:
                #url,risk_score,ip,is_url_accessible,is_robots_noindex,is_domain_blacklisted,is_http_status_error,is_suspended_page,is_risky_category,is_domain_very_recent,is_domain_recent,is_valid_https
                f.write(str(url)+","+str(data['data']['report']['risk_score']['result'])+","+str(data['data']['report']['server_details']['ip'])+","+str(data['data']['report']['security_checks']['is_url_accessible'])+","+str(data['data']['report']['security_checks']['is_robots_noindex'])+","+str(data['data']['report']['security_checks']['is_domain_blacklisted'])+","+str(data['data']['report']['security_checks']['is_http_status_error'])+","+str(data['data']['report']['security_checks']['is_suspended_page'])+","+str(data['data']['report']['security_checks']['is_risky_category'])+","+str(data['data']['report']['security_checks']['is_domain_very_recent'])+","+str(data['data']['report']['security_checks']['is_domain_recent'])+","+str(data['data']['report']['security_checks']['is_valid_https'])+"\n")
    else:
        print("Error: Request failed")
   
def scan_file(f):
    if( not os.path.isfile(f)):
        print("File not found")
        sys.exit(1)
        
    try:
        with open(f) as fh:
            for line in fh:
                time.sleep(1)
                line = line.strip()
                if line:
                    submit_url(line)
                
    except IOError:
        print("File not accessible")
    
scan_file(my_file)
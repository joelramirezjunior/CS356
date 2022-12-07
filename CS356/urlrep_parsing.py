#!/usr/bin/python3

# To run the script just use this:
# python3 /path/to/script.py /path/to/file/with/urls.txt /path/to/output/file.csv

import requests
import urllib.parse
import json
import sys
import os
import time

apivoid_key = "cef52bbbe26e7d38f0684770a2adc70b9fcd5c86"

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
            all_security_checks = '|'.join([str(x) for x in data['data']['report']['security_checks'].values()])
            with open(csv_file, 'a') as f:
                #url,risk_score,ip,country,is_host_an_ipv4|is_uncommon_host_length|is_uncommon_dash_char_count|is_uncommon_dot_char_count|is_suspicious_url_pattern|is_suspicious_file_extension|is_robots_noindex|is_suspended_page|is_most_abused_tld|is_uncommon_clickable_url|is_phishing_heuristic|is_possible_emotet|is_redirect_to_search_engine|is_http_status_error|is_http_server_error|is_http_client_error|is_suspicious_content|is_url_accessible|is_empty_page_title|is_empty_page_content|is_domain_ipv4_assigned|is_domain_ipv4_private|is_domain_ipv4_loopback|is_domain_ipv4_reserved|is_domain_ipv4_valid|is_domain_blacklisted|is_suspicious_domain|is_sinkholed_domain|is_defaced_heuristic|is_masked_file|is_risky_geo_location|is_china_country|is_nigeria_country|is_non_standard_port|is_email_address_on_url_query|is_directory_listing|is_exe_on_directory_listing|is_zip_on_directory_listing|is_php_on_directory_listing|is_doc_on_directory_listing|is_pdf_on_directory_listing|is_apk_on_directory_listing|is_linux_elf_file|is_linux_elf_file_on_free_dynamic_dns|is_linux_elf_file_on_free_hosting|is_linux_elf_file_on_ipv4|is_masked_linux_elf_file|is_masked_windows_exe_file|is_ms_office_file|is_windows_exe_file_on_free_dynamic_dns|is_windows_exe_file_on_free_hosting|is_windows_exe_file_on_ipv4|is_windows_exe_file|is_android_apk_file_on_free_dynamic_dns|is_android_apk_file_on_free_hosting|is_android_apk_file_on_ipv4|is_android_apk_file|is_external_redirect|is_risky_category|is_domain_recent|is_domain_very_recent|is_credit_card_field|is_password_field|is_valid_https  
                f.write(str(url)+"|"+str(data['data']['report']['risk_score']['result'])+"|"+str(data['data']['report']['server_details']['ip'])+ "|" + str(data['data']['report']['server_details']['country_code']) + "|" + all_security_checks + "\n")
    else:
        print("Error: Request failed")
   
def scan_file(f):
    if( not os.path.isfile(f)):
        print("File not found")
        sys.exit(1)
        
    try:
        with open(f) as fh:
            for line in fh:
                time.sleep(.5)
                line = line.strip()
                if line:
                    submit_url(line)
                
    except IOError:
        print("File not accessible")
    
scan_file(my_file)
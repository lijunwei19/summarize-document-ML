from selectorlib import Extractor
import requests 
import json 
from time import sleep

def scrape(url, i):    
    e = Extractor.from_yaml_file('APP/data_process/selectors.yml')
    headers = {
        'authority': 'www.amazon.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate'

,        'sec-fetch-dest': 'document',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n"%url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d"%(url,r.status_code))
        return None
    # Pass the HTML of the page and create
    data =  e.extract(r.text)
    result={}
    for key, value in data.items():
        if value:
            if key == 'price':
                result['Price']= value
            if key == 'Name' :
                result[key] = value
            if key == 'total_ratings':
                result[key] = value.split(' ')[0] 
            if key == 'reviews_total_scores':
                result['Score']= value[0].split()[0] 
            if key == 'review_detail_score':
                result['Star'] = [float(i) for i in value[0].replace('%', '').split(' ')  if i.isdigit()]
            if key == 'reviews_text':
                result['Reviews'] =[ i+'$$$' for i in value]
        else:
            result[key]=None
        json_object = json.dumps(result, indent = 4) 
        with open('dataset/scrape_json/output'+str(i)+'.json','w') as outfile:     
            outfile.write(json_object)
            sleep(0.3)
    return result
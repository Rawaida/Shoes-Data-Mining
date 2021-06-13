# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 20:09:26 2021

@author: rawaida
"""
import requests, time, json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

url_women = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fwomen%2Fshoes&sort=popularity&dir=desc&category_id=4&gender=women&segment=women&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'
url_men = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fmen%2Fshoes&sort=popularity&dir=desc&category_id=27&gender=men&segment=men&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'
url_kids = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fkids%2Fshoes&sort=popularity&dir=desc&category_id=534&segment=kids&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'

url_aldo = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fwomen%2Fshoes&sort=popularity&dir=desc&category_id=4&occasion=Casual&brand=87&gender=women&segment=women&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'

n = 0
limit = 400
delay_t = 100

def scraper (url_cat, n = n, limit = limit):
    
    offset_param = '&offset=' + str(n)
    limit_param = '&limit=' + str(limit) 
    url = url_cat + offset_param + limit_param  
    sesi = requests.Session()
    response = sesi.get(url, headers = headers)
    
    return response.json(), response.status_code

def repeat_scrape (url_cat, n = n, limit = limit):
    
    out_1st,_ = scraper(url_cat, n, limit) 
    result = out_1st['response']['docs']
    max_num = out_1st['response']['numFound']
    bal_num = max_num - limit
    
    for i in range(int(bal_num/limit)+1):
  
        new_n = n + limit
        out_next, status = scraper(url_cat, new_n)
        n = new_n
        if status == 200:    
            result.extend (out_next['response']['docs'])
        else:
            break  
            
    return result

def extract (data):
    new = []
    for i, item in enumerate (data):    
        new_data = { 'attribute_set_id'   : data[i]['meta']['attribute_set_id'],
                     'attribute_set_name' : data[i]['meta']['attribute_set_name'],
                     'brand'              : data[i]['meta']['brand'],
                     'sku'                : data[i]['meta']['sku'],
                     'name'               : data[i]['meta']['name'],
                     'actual_price'       : data[i]['meta']['max_price'],
                     'discounted_price'   : data[i]['meta']['max_special_price'],
                     'image'              : data[i]['image'] }
        new.append(new_data)
    
    return new

def save_json (data, filename):        
    with open (filename, 'w') as file:
        json.dump(data, file)
            
    return None
    
#################################################################
      
# run the scraper function
women = repeat_scrape(url_women)
time.sleep(delay_t)
men = repeat_scrape(url_men)
time.sleep(delay_t)
kids = repeat_scrape(url_kids)
time.sleep(delay_t)

n = 0
limit = 400
aldo_casual = repeat_scrape(url_aldo)

kids_data = extract (kids)
women_data = extract (women)
men_data = extract (men)
aldo_data = extract (aldo_casual)

save_json (kids_data, 'kids.json')
save_json (women_data, 'women.json')
save_json (men_data, 'men.json')
save_json (aldo_data, 'aldo.json')

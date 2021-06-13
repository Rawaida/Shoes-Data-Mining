# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 20:09:26 2021

@author: waida
"""

# SCRAPE ALL SHOES in Zalora https://www.zalora.com.my/
# SCRAPE ALDO + OCCASION + CASUAL
# https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fwomen%2Fshoes&sort=popularity&dir=desc&offset=0&limit=102&category_id=4&occasion=Casual&brand=87&gender=women&segment=women&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false&session_id=651ddfe4a87fb0f35becb2674a5a1dd5

# import relevant libraries
import requests, time, json

# define pre-set variables
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}

url_women = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fwomen%2Fshoes&sort=popularity&dir=desc&category_id=4&gender=women&segment=women&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'
url_men = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fmen%2Fshoes&sort=popularity&dir=desc&category_id=27&gender=men&segment=men&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'
url_kids = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fkids%2Fshoes&sort=popularity&dir=desc&category_id=534&segment=kids&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'

url_aldo = 'https://www.zalora.com.my/_c/v1/desktop/list_catalog_full?url=%2Fwomen%2Fshoes&sort=popularity&dir=desc&category_id=4&occasion=Casual&brand=87&gender=women&segment=women&special_price=false&all_products=false&new_products=false&top_sellers=false&catalogtype=Main&lang=en&is_brunei=false&search_suggest=false&enable_visual_sort=true&enable_filter_ads=true&compact_catalog_desktop=false&name_search=false&solr7_support=false&pick_for_you=false&learn_to_sort_catalog=false&is_multiple_source=true&enable_similar_term=true&enable_relevance_classifier=false&auto_correct=false'

n = 0
limit = 400
delay_t = 100

# general scraper function 

def scraper (url_cat, n = n, limit = limit):
    
    # define additional parameters     
    
    offset_param = '&offset=' + str(n)
    limit_param = '&limit=' + str(limit)
     
    # define link to be scraped
    url = url_cat + offset_param + limit_param  
    
    # set sessions
    sesi = requests.Session()
    
    # send get requests to the respective url
    response = sesi.get(url, headers = headers)
    
    # check the response status
    # print ("status code response:", response.status_code)
        
    return response.json(), response.status_code


# repetitive scraping for subsequent rounds function
def repeat_scrape (url_cat, n = n, limit = limit):
    
    # run the scraper for 1st round with offset start = 0
    out_1st,_ = scraper(url_cat, n, limit) 
    
    # capture relevant data only
    result = out_1st['response']['docs']
        
    # # delay the scraper for subsequent rounds
    # time.sleep(delay_t)
        
    # know all the total items from the 1st scraped items
    max_num = out_1st['response']['numFound']
    bal_num = max_num - limit
    
    # scraper will run in i rounds based on numbers of items found
    for i in range(int(bal_num/limit)+1):
        
        # set new offset start for subsequent rounds
        new_n = n + limit
        
        # run the scraper
        out_next, status = scraper(url_cat, new_n)
        
        # increase the new offset for next round
        n = new_n
        
        # only append scraped results in a list if status is 200
        if status == 200:
            
            result.extend (out_next['response']['docs'])
        
        else:
            break
                   
    return result


# extract relevant data from json output
def extract (data):
    
    # extract attribute set id, attribute set name, brand, image link, 
    # max price, max special price, sku
    
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


# save json data file into an output
def save_json (data, filename):
        
    with open (filename, 'w') as file:
        json.dump(data, file)
            
    return None
    
#################################################################
      
# run the scraper function

# scrape all women shoes
women = repeat_scrape(url_women)

# delay the scraper
time.sleep(delay_t)

# scrape all men shoes
men = repeat_scrape(url_men)

# delay the scraper
time.sleep(delay_t)

# scrape all kids shoes
kids = repeat_scrape(url_kids)

# delay the scraper
time.sleep(delay_t)
      
# run the the scraper for aldo brand & occasion search
n = 0
limit = 400

aldo_casual = repeat_scrape(url_aldo)

# process the response files to get only relevant data 
# plus additional data for master data & data quality check
kids_data = extract (kids)
women_data = extract (women)
men_data = extract (men)
aldo_data = extract (aldo_casual)

# save the data into output file in host machine
save_json (kids_data, 'kids.json')
save_json (women_data, 'women.json')
save_json (men_data, 'men.json')
save_json (aldo_data, 'aldo.json')


    
    
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 09:22:32 2019

@author: Soeren
"""

import requests
from lxml import html
import math
import csv
import time


# set header global
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def get_review_site(url):

    url_slugs = url.split('/')
    url_slugs[4] = 'product-reviews'
    url_slugs[6] = ''
    link         = '/'.join(url_slugs)

    return link


def to_csv(header, data, fn="amazon_scrape_csv", **kwargs):
    
    # timestamp filename
    fn = fn + "_" + str(int(time.time())) + ".csv"
    
    # write to csv file
    with open(fn, mode='w', newline='', encoding='utf-8') as scrape_file:
        
        # create writer
        file_writer = csv.writer(scrape_file, **kwargs)
        
        # write data
        file_writer.writerow(header)
        for row in data:
            file_writer.writerow(row)
        

def scrape(url, header=HEADER, **kwargs):

    # get review url
    review_url = get_review_site(url)

    # get amount of reviews for pagination
    base_query = "ref=cm_cr_arp_d_paging_btm_next_{pg}?ie=UTF8&reviewerType=all_reviews&pageNumber={pg}&pageSize=20"
    page_url   = review_url + base_query.format(pg=1)
    req        = requests.get(page_url, headers=header)
    tree       = html.fromstring(req.content)
    nbr        = int(tree.xpath(".//span[@data-hook='total-review-count']")[0].text)
    
    # create empty list for reviews
    data = []
    
    # get amount of pages for product
    pages = math.ceil(nbr/20)
    for page in range(pages):
        # build link for correct pagination
        query = base_query.format(pg=page+1)
        page_url = review_url + query
        
        # make request and parse to tree
        req  = requests.get(page_url, headers=header)
        tree = html.fromstring(req.content)
        
        # get all reviews
        reviews = tree.xpath(".//div[@data-hook='review']")
        for review in reviews:
            
            # get title and content of review
            title = review.xpath(".//a[@data-hook='review-title']/span")[0].text
            body  = review.xpath(".//span[@data-hook='review-body']/span")[0].text
            note  = ""
            
            # check if user has a verified purchase or was payed
            vine  = review.xpath(".//a[@data-hook='linkless-format-strip-whats-this']")
            verified = review.xpath(".//span[@data-hook='avp-badge']")
            
            if verified:
                note = verified[0].text
            elif vine:
                note = vine[0].text
            
            data.append((title, body, note))
            
    # write data to csv file
    columns = ['title', 'content', 'note']
    to_csv(columns, data)

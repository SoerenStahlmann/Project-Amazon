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
from datetime import datetime as dt


# set header global
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}


def get_review_site(url, header):

    # get review url
    link       = url.split('/')
    link[4]    = "product-reviews"
    link       = link[:6]
    link       = '/'.join(link)
    review_url = link + "/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

    # make request and parse response to a tree     
    req  = requests.get(review_url, headers=header)
    tree = html.fromstring(req.content)
    
    # extract review link and number of reviews
    review_cnt  = tree.xpath(".//span[@data-hook='total-review-count']")[0].text
    nbr_reviews = [int(s) for s in review_cnt.split() if s.isdigit()][0]
    
    return link, nbr_reviews


def to_csv(header, data, fn = "amazon_scrape_csv", **kwargs):
    
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
    review_url, nbr = get_review_site(url, header)

    # create empty list for reviews
    data = []
    
    # get amount of pages for product
    pages = math.ceil(nbr/20)
    for page in range(pages):
        # build link for correct pageination
        query = "/ref=cm_cr_arp_d_paging_btm_next_{pg}?ie=UTF8&reviewerType=all_reviews&pageNumber={pg}&pageSize=20"\
                .format(pg=page)
        page_url = review_url + query
        
        # make request and parse to tree
        req  = requests.get(page_url, headers=header)
        tree = html.fromstring(req.content)
        
        # get all reviews
        reviews = tree.xpath(".//div[@data-hook='review']")
        for review in reviews:
            
            # get title and content of review
            title     = review.xpath(".//a[@data-hook='review-title']/span")[0].text
            body      = review.xpath(".//span[@data-hook='review-body']/span")[0].text
            note      = ""
            rating    = review.xpath(".//i[@data-hook='review-star-rating']/span")[0].text

            # TODO: TIMEZONE??
            # timestamp
            timestamp = review.xpath(".//span[@data-hook='review-date']")[0].text
            timestamp = time.mktime(dt.strptime(timestamp, "%B %d, %Y").timetuple())

            # check if user has a verified purchase or was payed
            vine  = review.xpath(".//a[@data-hook='linkless-format-strip-whats-this']")
            verified = review.xpath(".//span[@data-hook='avp-badge']")
            
            if verified:
                note = verified[0].text
            elif vine:
                note = vine[0].text
            
            data.append((title, body, note, rating, timestamp))

    # write data to csv file
    columns = ['title', 'content', 'note', 'rating', 'timestamp']
    to_csv(columns, data)


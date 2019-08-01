import scraper.amazon

"""
Header does not need to be changed

URL needs to be the product URL  from the Amazon.COM page 

"""



# input data
url    = "https://www.amazon.com/Deep-Learning-Python-Francois-Chollet/dp/1617294438/ref=cm_cr_arp_d_product_top?ie=UTF8"
url_galaxy = "https://www.amazon.com/TracFone-Samsung-Galaxy-Prepaid-Smartphone/dp/B071RR8NCG/ref=sr_1_2_sspa?keywords=samsung+galaxy+s7&qid=1564654524&s=gateway&sr=8-2-spons&psc=1"
if __name__ == '__main__':

    # scrape data
    scraper.amazon.scrape(url_galaxy)

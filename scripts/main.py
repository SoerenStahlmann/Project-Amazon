import scraper.amazon

"""
Header does not need to be changed

URL needs to be the product URL  from the Amazon.COM page 

"""

if __name__ == "__main__":

    # input data
    url    = "https://www.amazon.com/Deep-Learning-Python-Francois-Chollet/dp/1617294438/ref=cm_cr_arp_d_product_top?ie=UTF8"


    # scrape data
    scraper.amazon.scrape(url)

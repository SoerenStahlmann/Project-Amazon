import scraper.amazon

"""
Header does not need to be changed

URL needs to be the product URL  from the Amazon.COM page 

"""

if __name__ == '__main__':

    # input data
    url = "https://www.amazon.com/Deep-Learning-Python-Francois-Chollet/dp/1617294438/ref=cm_cr_arp_d_product_top?ie=UTF8"
    #url = "https://www.amazon.com/CarGuys-Super-Cleaner-Effective-Upholstery/dp/B071XB18BF/ref=cm_cr_arp_d_product_top?ie=UTF8"
    url = "https://www.amazon.com/DECKER-WP900-6-Inch-Random-Polisher/dp/B000077CPT/ref=pd_sim_263_4/134-4992140-7470069?_encoding=UTF8&pd_rd_i=B000077CPT&pd_rd_r=1887db31-4953-4ce1-8f41-fbc517db1fe7&pd_rd_w=LM3nf&pd_rd_wg=RA9iy&pf_rd_p=5b00861f-dd80-491e-8e32-d1b61e4ab87c&pf_rd_r=65BXCN13SA7TRR0NPXJ3&psc=1&refRID=65BXCN13SA7TRR0NPXJ3"

    # scrape data
    scraper.amazon.scrape(url)

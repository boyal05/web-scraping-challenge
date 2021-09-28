from bs4 import BeautifulSoup as bs
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import requests
import pymongo
import os
import time 
import pandas as pd


def mars_scrape():

    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    connection = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(connection)

    db = client.commerce_db
    collection = db.items

    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(2)

    soup = bs(browser.html, 'lxml')
    print("Check1")

    results = soup.find_all('div', class_='list_text')
    news_dict = []

    for result in results:
        
        thread_title = result.find('div', class_='content_title')        

        title_text = thread_title.text
        teaser_body = ""
        thread = result.find('div', class_='article_teaser_body') 

        # The number of comments made in the thread
        teaser_body = thread.text.lstrip()
        dict_temp = {'title': title_text, 'teaser': teaser_body}
        news_dict.append(dict_temp)
        # Run teaser_body & title 
        if (teaser_body):
            print('\n*****************\n')
            print(title_text)
            print('\n*****************\n')
            print('Body:')
            print(teaser_body)

    url = "https://spaceimages-mars.com/"
    browser.visit(url)
    time.sleep(2)
    print("Check2")
    soup = bs(browser.html, 'lxml')

    html = browser.html
    img_soup = soup(html, 'html.parser')

    header = soup.find_all('div', class_='header')
    header_image = soup.find('img', class_='headerimage fade-in').get('src')

    featured_image_url = url + header_image


    # Mars Facts

    url = 'https://galaxyfacts-mars.com/'

    tables = pd.read_html(url)
    mars_table_df = tables[0]
    mars_table_df.columns = ["Description","Planet 1","Planet 2"]
    mars_table_df.set_index("Description", inplace=True)

    html_table = mars_table_df.to_html()

    clean_html = html_table.replace('\n', '')

    mars_table_df.to_html('mars_table.html')

    ## Mars Hemispheres
    print("Check3")
    planet_dict = []

    ## Cerberus 
    print("Check4")
    # url https://marshemispheres.com/
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)

    browser.links.find_by_partial_text('Cerberus').click()

    html = browser.html
    soup = bs(html,"html.parser")
 
    img_link = soup.find('img', class_='wide-image').get('src')

    cerberus_title = soup.find('h2', class_='title').text

    cerberus_img = url + img_link

    browser.back()

    cerberus_dict = {'title': cerberus_title, 'img_url': cerberus_img}
    planet_dict.append(cerberus_dict)

    print(cerberus_dict)

    ## Schiaparelli
    print("Check5")
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)

    browser.links.find_by_partial_text('Schiaparelli').click()


    html = browser.html
    soup = bs(html,"html.parser") 
    img_link = soup.find('img', class_='wide-image').get('src')

    schiaparelli_title = soup.find('h2', class_='title').text

    schiaparelli_img = url + img_link

    browser.back()

    schiaparelli_dict = {'title': schiaparelli_title, 'img_url': schiaparelli_img}
    planet_dict.append(schiaparelli_dict)

    print(schiaparelli_dict)

    ## Syrtis
    print("Check6")
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)

    browser.links.find_by_partial_text('Syrtis').click()


    html = browser.html
    soup = bs(html,"html.parser")

    img_link = soup.find('img', class_='wide-image').get('src')

    syrtis_title = soup.find('h2', class_='title').text

    syrtis_img = url + img_link

    browser.back()
    syrtis_dict = {'title': syrtis_title, 'img_url': syrtis_img}
    planet_dict.append(syrtis_dict)

    print("Check7")
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(2)

    browser.links.find_by_partial_text('Valles Marineris').click()


    html = browser.html
    soup = bs(html,"html.parser")
    img_link = soup.find('img', class_='wide-image').get('src')

    valles_title = soup.find('h2', class_='title').text

    valles_img = url + img_link

    browser.back()
    
    #Create dictionaries to the img url and title 

    valles_dict = {'title': valles_title, 'img_url': valles_img}
    planet_dict.append(valles_dict)

    # print(valles_dict)

    # print(planet_dict)

    mars_scrape = {
        "news": news_dict,
        "featured_img_url": featured_image_url,
        "mars_table": clean_html,
        "hempisphere_img_urls": planet_dict
        }
    print("Check8")
    browser.quit()

    return mars_scrape

if __name__ == "__main__":
    results = mars_scrape()
    print("results")
    print(results) 

from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Setup splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)


# In[3]:
def scrape():
    #Visit Nasa's Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    #Begin scrape 1
    #Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Get headline and brief paragraph text
    result = soup.find('div', class_='image_and_description_container')
    title = result.find('h3').text
    para = result.find('div', class_='rollover_description_inner').text
    #print(para)
    #print(title)
    #Begin scrape 2
    # Setup splinter
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)
    url= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    #Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #Grab featured JPL image
    result = soup.find('img', class_="fade-in")
    src = result['src']

    featured_image_url = url+"/"+src
    #print(featured_image_url)
    #Begin 3rd scrape (w/ Pandas)
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)
    tables = pd.DataFrame(tables)
    tables.reset_index(drop=True)
    tables_html = tables.to_html()
    tables_html
    #Begin 4th Scrape
    url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    #Loop through 4 Links and Do Queries in Individual Web Pages
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find('div', class_="collapsible results")
    items = result.find_all('div', class_='item')

    #print(items)
    #Create list for individual pictures urls and loop through 'items'
    pic_list = []
    for item in items:
        link = item.find('a', class_='itemLink')
        pic_url = link['href']
        pic_list.append(pic_url)

    #print(pic_list)
    #browser.quit
    url = 'https://astrogeology.usgs.gov'
    hemispheres = []
    for pic in pic_list:
        #executable_path = {'executable_path': ChromeDriverManager().install()}
        #browser = Browser('chrome', **executable_path, headless=False)
        browser.visit(url + pic)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        result = soup.find('div', class_="container")
        items = result.find_all('a')
        item = items[2]
        title = result.find_all('h2', class_="title")[0].text
        item_url = item['href']
        hemispheres.append({'img_url':item_url, 'title':title})
    browser.quit

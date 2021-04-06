from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# Setup splinter
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)


def scrape():
    browser = init_browser()
    scrape_dict = {}
    # Visit Nasa's Mars News Site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Begin scrape 1
    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Get headline and brief paragraph text
    result = soup.find('div', class_='image_and_description_container')
    title = result.find('h3').text
    para = result.find('div', class_='rollover_description_inner').text
    # print(para)
    # print(title)
    scrape_dict['news_title'] = title
    scrape_dict['news_para'] = para
    # Begin scrape 2
    # Setup splinter
    #executable_path = {'executable_path': ChromeDriverManager().install()}
    #browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(url)
    # Scrape page into soup
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    # Grab featured JPL image
    result = soup.find('img', class_="fade-in")
    src = result['src']

    featured_image_url = "https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/"+src
    scrape_dict['featured_image_url'] = featured_image_url
    # print(featured_image_url)
    # Begin 3rd scrape (w/ Pandas)
    url = "https://space-facts.com/mars/"
    tables = pd.read_html(url)[0]
    tables = pd.DataFrame(tables)
    tables = tables.rename({0: "Feature", 1: "Data"}, axis=1)
    tables = tables.set_index("Feature")
    # tables.set_index(0)
    tables_html = tables.to_html()
    tables_html
    scrape_dict['tables_html'] = tables_html

    # Begin 4th Scrape
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    # Loop through 4 Links and Do Queries in Individual Web Pages
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find('div', class_="collapsible results")
    items = result.find_all('div', class_='item')

    # Create list for individual pictures urls and loop through 'items'
    pic_list = []
    for item in items:
        link = item.find('a', class_='itemLink')
        pic_url = link['href']
        pic_list.append(pic_url)

    # Go to individual pages for hemisphere photos and grab urls to append to dictionary
    browser.quit()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    hemispheres = []
    results = soup.find_all('div', class_="description")
    click_list = []
    for item in results:
        pic_url = 'https://astrogeology.usgs.gov' + \
            item.find_all('a')[0]['href']
        click_list.append(pic_url)
        title = item.find('h3').text
        hemispheres.append({'title': title})

    pic_list = []

    for i, link in enumerate(click_list):
        browser.visit(link)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        full_pic = soup.find('div', class_="container")
        full_href = full_pic.find('img', class_='wide-image')
        full_href = full_href['src']
        full_href = 'https://astrogeology.usgs.gov/' + full_href
        pic_list.append(full_href)
        hemispheres[i]['img_url'] = full_href
    scrape_dict['hemispheres'] = hemispheres
    browser.quit()
    return scrape_dict

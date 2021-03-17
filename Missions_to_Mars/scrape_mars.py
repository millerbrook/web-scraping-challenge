#!/usr/bin/env python
# coding: utf-8

# In[26]:


from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


# In[2]:


# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


url = 'https://mars.nasa.gov/news/'
browser.visit(url)


# In[10]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

result = soup.find('div', class_='image_and_description_container')
title = result.find('h3').text
para = result.find('div', class_='rollover_description_inner').text
print(para)
print(title)


# In[12]:


#End first scrape
browser.quit()


# In[13]:


#Begin scrape 2
# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url= 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[25]:


html = browser.html
soup = BeautifulSoup(html, 'html.parser')

result = soup.find('img', class_="fade-in")
src = result['src']

featured_image_url = url+"/"+src
print(featured_image_url)


# In[27]:


#End second scrape
browser.quit()


# In[28]:


url = "https://space-facts.com/mars/"


# In[34]:


tables = pd.read_html(url)
tables = pd.DataFrame(tables)
tables.reset_index(drop=True)
tables_html = tables.to_html()
tables_html


# In[35]:


#Begin Scraping Mars Hemispheres Photos URLs
# Setup splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)
url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[36]:


#Loop through 4 Links and Do Queries in Individual Web Pages
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

result = soup.find('div', class_="collapsible results")
items = result.find_all('div', class_='item')

print(items)


# In[42]:


pic_list = []
for item in items:
    link = item.find('a', class_='itemLink')
    pic_url = link['href']
    pic_list.append(pic_url)

print(pic_list)
browser.quit


# In[69]:


url = 'https://astrogeology.usgs.gov'
hemispheres = []
for pic in pic_list:
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
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


# In[70]:


print(hemispheres)


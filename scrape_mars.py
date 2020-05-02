import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from splinter import Browser
from selenium import webdriver

def init_browser():
    # executable_path = {'executable_path': 'chromedriver'}
    return Browser('chrome', headless=True)

def scrape():
    browser = init_browser()
    mars_data = {}
    
    # NASA mars news
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    list_text = soup.find('div', class_='list_text')
    news_title = list_text.find('div', class_='content_title').text
    news_paragraph = list_text.find('div', class_='article_teaser_body').text
    mars_data["news_title"] = news_title
    mars_data["news_paragraph"] = news_paragraph

    # JPL mars space images - featured image
    mars_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(mars_url)
    mars_html = browser.html
    mars_soup = BeautifulSoup(mars_html, 'html.parser')

    mars_image = mars_soup.find('img', class_='thumb')['src']
    featured_image_url = f'https://www.jpl.nasa.gov{mars_image}'
    mars_data["featured_image_url"] = featured_image_url

    # Mars weather
    # weather_url = 'https://twitter.com/marswxreport?lang=en'
    # browser.visit(weather_url)
    # weather_html = browser.html
    # weather_soup = BeautifulSoup(weather_html, 'html.parser')

    # weather_info = weather_soup.find('div')
    # mars_weather = weather_info.find('p', class_='tweet-text').text
    # mars_data["mars_weather"] = mars_weather

    # Mars facts
    facts_url = 'https://space-facts.com/mars/'
    browser.visit(facts_url)
    facts_html = browser.html
    facts_soup = BeautifulSoup(facts_html, 'html.parser')

    mars_facts = facts_soup.find('table', class_='tablepress tablepress-id-p-mars')
    first_data = mars_facts.find_all('td', class_='column-1')
    second_data = mars_facts.find_all('td', class_='column-2')
    parameters = []
    values = []
    for row in first_data:
        parameter = row.text.strip()
        parameters.append(parameter)
    for row in second_data:
        value = row.text.strip()
        values.append(value)
    mars_facts_df = pd.DataFrame({'Parameters': parameters, 'Values': values})
    mars_facts_html = mars_facts_df.to_html(header=False, index=False)
    # mars_table_html = mars_facts_html.replace("\n", "")
    mars_data["mars_table"] = mars_facts_html

    # Mars hemispheres
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')

    mars_hemispheres = []
    for i in range(4):
        mars_images = browser.find_by_tag('h3')
        mars_images[i].click()
        hemispheres_html = browser.html
        hemispheres_soup = BeautifulSoup(hemispheres_html, 'html.parser')
        four_images = hemispheres_soup.find('img', class_='wide-image')['src']
        four_images_title = hemispheres_soup.find('h2', class_='title').text
        four_images_url = 'https://astrogeology.usgs.gov' + four_images
        images_dic = {'title': four_images_title, 'four_images_url': four_images_url}
        mars_hemispheres.append(images_dic)
        browser.back()
    mars_data['mars_hemispheres'] = mars_hemispheres
    print(mars_data)
    
    return mars_data
    
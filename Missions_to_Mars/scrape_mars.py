from splinter import Browser
from bs4 import BeautifulSoup as bs
from bs4 import BeautifulSoup as soup
import pandas as pd 
import time
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Mission to Mars website URL
    url = "https://redplanetscience.com/"
    browser.visit(url)

    time.sleep(1)
    # Scrape page into Soup
    html = browser.html
    news_soup = soup(html, "html.parser")

    # Get latest news title
    news_title = news_soup.find_all("div", class_="content_title")[0].get_text()

    # Get latest news paragraph
    news_p = news_soup.find_all("div", class_="article_teaser_body")[0].get_text()

    # Setting URL for Mars images
    url = "https://spaceimages-mars.com/image/featured/mars2.jpg"
    browser.visit(url)
    
    time.sleep(1)
    
    # Scrape page into Soup
    html = browser.html
    image_soup = soup(html,"html.parser")
    featured_image_url = image_soup.find_all("img")[0].get("src")

    # Getting Mars facts
    mars_facts = pd.read_html("https://galaxyfacts-mars.com")[0]

    # Converting data to HTML
    mars_html = mars_facts.to_html()

    # Setting URl for Mars Hemisphere
    url = "https://marshemispheres.com/index.html"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    links = browser.links.find_by_partial_text("Hemisphere")

    hemi_url = []
    for i in range(len(links)):
        browser.links.find_by_partial_text("Hemisphere")[i].click()
        
        html = browser.html
        image_soup = soup(html,"html.parser")
        image_link = image_soup.find_all("div", class_="downloads")[0]
        link = image_link.find("a", href=True)
        link = "https://marshemispheres.com/" + link["href"]
        img_title = image_soup.find_all("h2", class_="title")[0].get_text()
        hemi_dict = {
            "img_url":link,
            "title":img_title
        }
        hemi_url.append(hemi_dict)
        browser.back()

    hemi_url
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data

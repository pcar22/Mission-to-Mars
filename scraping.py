# Import Splinter, BeautifulSoup, and Pandas
# from types import NoneType
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():

    # Set-up Splinter. ## Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)
    hemisphere_image_urls = hemisphere(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemispheres": hemisphere_image_urls,
      "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):
    '''creating a function to be used many times'''
    # Scrape Mars News
    # Visit the mars nasa news site
    # This is the lates from module 10.5.3 and it changed from earlier.
    # url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)


    # Convert the browser html to a soup object
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:

        slide_elem = news_soup.select_one('div.list_text')
        # slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as news_title
        news_title = slide_elem.find('div', class_='content_title').get_text()
        
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:
        return None, None

    return news_title, news_p


### JPL Space Images Featured Image

def featured_image(browser):

    # Visit URL
    # Changed in 10.5.3 from earlier. url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()


    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

# Add try/except for error handling
    try:
    
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
                                                               
    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    # Changed in 10.5.3 from earlier. img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url


def mars_facts():
    
    try:
        ### Module 10.3.5 Mars Facts
        # Use `read_html` to scrape the facts table into a dataframe
        # Changed in module 10.5.3 from earlier. df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)
    
    
    
        # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

    # Challenge line 3 - create a function to scrape hemisphere data, use code from Mission_to_Mars_Challenge.py. Return scraped data.
def hemisphere(browser):
    url = 'https://marshemispheres.com/'
    browser.visit(url)

        # From #2 in .py file
    hemisphere_image_urls = []

# Code to retrieve the image urls and titles for each hemisphere.
    for i in range(4):
        hemispheres = {}
        browser.find_by_css('a.product-item h3')[i].click()
        element = browser.links.find_by_text('Sample').first  
        img_url = element['href']
        title = browser.find_by_css("h2.title").text
        hemispheres["img_url"] = img_url
        hemispheres["title"] = title
        hemisphere_image_urls.append(hemispheres)
        browser.back()
    
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())
    

    # This was the last line before adding the def and try/except
    # browser.quit()


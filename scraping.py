# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        #I am not sure if this should match up with the dictionary title in deliverable 1.
        "hemispheres_image": hemispheres_image(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
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

    # Use the base url to create an absolute url
    img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    # Add try/except for error handling
    try:
        # Use 'read_html' to scrape the facts table into a dataframe
        df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def hemispheres_image(browser):
    # 1. Use browser to visit the URL
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    #need browser and HTML parser for next step
    html = browser.html
    image_soup = soup(html, 'html.parser')
    #identify the number of images that I need in my For loop
    # inspecting website seems all relevant code is div class "item" - has both description as h3 and image as href (but only last part of image URL not full)
    count_items= image_soup.find_all('div', class_='item',)
    
    # 2. Create a list to hold the images and titles relates to #5
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.

    #For loop to iterate through the tags or CSS element-relates to the loop portion of #7

    for count in count_items:
        # find title
        title = count.find('h3').text
    
        #find url
        second_url=count.find('a')['href']
        complete_url = url+second_url
    
        #click on each hemisphere link and navigate to the full resolution image page-- relates to the find image anchor and get href portion of number 7
        browser.visit(complete_url)
        html = browser.html
        image_soup = soup(html, 'html.parser')
   
        #retrieve the full resolution image URL string and title for the hemisphere image--relates to #6  retrivce image
        hemisphere_first_image= image_soup.find('div', class_='downloads')
        hemisphere_full_image= url+hemisphere_first_image.find('a')['href']

        #add selection to the list
        item_to_add=dict({'img_url':hemisphere_full_image, 'title':title})
        hemisphere_image_urls.append(item_to_add)
        
    return hemisphere_image_urls
        
if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())



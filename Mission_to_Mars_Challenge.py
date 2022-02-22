# %%
# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

# %%
# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# %%
"""
### Visit the NASA Mars News Site
"""

# %%
# Visit the mars nasa news site
url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# %%
# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

# %%
slide_elem.find('div', class_='content_title')

# %%
# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# %%
# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# %%
"""
### JPL Space Images Featured Image
"""

# %%
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# %%
# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup

# %%
# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# %%
# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# %%
"""
### Mars Facts
"""

# %%
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()

# %%
df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df

# %%
df.to_html()

# %%
"""
# D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
"""

# %%
"""
### Hemispheres
"""

# %%
# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'

browser.visit(url)

# %%
#need browser and HTML parser for next step
html = browser.html
image_soup = soup(html, 'html.parser')

# %%
#identify the number of images that I need in my For loop
# inspecting website seems all relevant code is div class "item" - has both description as h3 and image as href (but only last part of image URL not full)
count_items= image_soup.find_all('div', class_='item',)


# %%
# 2. Create a list to hold the images and titles relates to #5
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.

#For loop to iterate through the tags or CSS element-relates to the loop portion of #7

for count in count_items:

    # find title
    title=count.find('h3').text

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

    #use brower back to get to the nexst hemispher image--  NOT NEEDED????




# %%
# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls

# %%
# 5. Quit the browser
browser.quit()

# %%

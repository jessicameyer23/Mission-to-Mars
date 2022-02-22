# %%
# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

# %%


# %%
#setting up excutable path
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# %%
# Visit the mars nasa news site, setting up wait time to one second
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

# %%
#setting up HLML parser

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

# %%
#searching for article title

slide_elem.find('div', class_='content_title')

# %%
# Use the parent element to find the first `a` tag and save it as `news_title`--putting in get text at the end removes some other stuff
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# %%
# Use the parent element to find the paragraph text--adding summary text-- article teaser is the summary text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p

# %%
"""
### Featured Images
"""

# %%
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# %%
# Find and click the full image button--- indexing chain at the end of the code is to click the second button, 1, 1st would be zero
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# %%
# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# %%
# Find the relative image url-- this is where the image we want lives-- use the link thats inside these tags.
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# %%
# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# %%
#only pulls in the first table--which is why we have a zero.  df=colums --we are assigning columns to the new dataframe
#def-set index===  we are turning the description fcolumn into the dataframs index.

df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

# %%
#converting our dataframe back to an htlm mess!  to enable us to add to our web application
df.to_html()

# %%
#Without it, the automated browser won't know to shut down—it will continue to listen for instructions and use the computer's resources (it may put a strain on memory or a laptop's battery if left on).
browser.quit()

# %%

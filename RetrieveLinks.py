from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup as bs


options = Options()
options.headless = True # set the option "headless" for the web driver
driver = wd.Firefox(options=options)  # configure webdriver to use Firefox browser

def esa_scraper(p):
    """ Function used to scrape and find the right articles that will be indexed in the esa page
    @:param p the page to scrape"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []    # list of articles links for this site 

    for a in soup.find_all(class_="story", href=True):  # obtain <a> class for the articles
            if a.text:
                tmpArticles.append(a['href'])  # to get the "href" value

    tmpArticles = [p[:19] + i for i in tmpArticles] # list of links retrieved from esa web page

    return tmpArticles


def bo_scraper(p):
    """ Function used to scrape and find the right articles that will be indexed in the blue origin page
    @:param p the page to scrape"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []    # list of articles links for this site 

    for a in soup.find_all(class_="NewsArchive__postTitleLink", href=True):  # obtain <a> class for the articles
        if a.text:
            tmpArticles.append(a['href'])  # to get the "href" value

    tmpArticles = [p + i[8:] for i in tmpArticles] # list of links retrieved from blue origin web page

    return tmpArticles


def nasa_scraper(p):

    driver.get(p)

    for i in range(3):
        WebDriverWait(driver, timeout=30).until(lambda d: d.find_element_by_id("trending")).click()
        print(i)

    content = WebDriverWait(driver, timeout=30).until(lambda d: d.page_source)
    print(len(content))


def write_to_file(links_articles):
    """Function used to write down to one file all the links got from the scrapers
    @:param links_articles list of the articles to index"""
    file = open("links.txt", "w")

    for link in links_articles:
        file.write(link)
        file.write("\n")

    file.close()


def main():
    """Main function to start the whole scraping action"""

    root_esa = "https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/(archive)/"   # root of esa site
    root_bo = "https://www.blueorigin.com/news/"    # root page of blue origin site
    root_nasa = "https://www.nasa.gov/topics/humans-in-space"   # root page of nasa site

    links_articles = [] # list of all articles links

    i = 5   # index used to set the max page of esa articles

    #for k in range(i):
    #    links_articles.extend(esa_scraper(root_esa+str(k*50)))  # adding the links retrived from the first "i" esa pages
    
    #links_articles.extend(bo_scraper(root_bo))  # adding the links retrieved from the blue origin page

    #write_to_file(links_articles)

    nasa_scraper(root_nasa)

if __name__ == "__main__":
    main()

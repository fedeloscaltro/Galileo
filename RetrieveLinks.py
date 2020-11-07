from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.wait import WebDriverWait

options = Options()
options.headless = True  # set the option "headless" for the web driver
driver = wd.Firefox(options=options)  # configure webdriver to use Firefox browser


def esa_scraper(p):
    """Function used to scrape and find the articles indexed in the ESA web pages
        @:param p the page to scrape
        @:return tmpArticles temporary list of ESA articles"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []  # list of articles links for this site

    for a in soup.find_all(class_="story", href=True):  # obtain <a> class for the articles
        if a.text:
            tmpArticles.append(a['href'])  # to get the "href" value

    tmpArticles = [p[:19] + i for i in tmpArticles]  # list of links retrieved from esa web page

    return tmpArticles


def bo_scraper(p):
    """Function used to scrape and find the articles indexed in the Blue Origin web page
        @:param p the page to scrape
        @:return tmpArticles temporary list of Blue Origin articles"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []  # list of articles links for this site

    for a in soup.find_all(class_="NewsArchive__postTitleLink", href=True):  # obtain <a> class for the articles
        if a.text:
            tmpArticles.append(a['href'])  # to get the "href" value

    tmpArticles = [p + i[8:] for i in tmpArticles]  # list of links retrieved from Blue Origin web page

    return tmpArticles


def nasa_scraper(p):
    """Function used to scrape and find the articles indexed in the NASA web page
        @:param p NASA's root page
        @:return tmpArticles temporary list of NASA articles"""
    driver.get(p)

    for i in range(12):
        # wait 'til the whole page is loaded and click the desired button
        WebDriverWait(driver, timeout=30).until(lambda d: d.find_element_by_id("trending")).click()

    content = WebDriverWait(driver, timeout=30).until(lambda d: d.page_source)  # to get the content of the NASA's page
    soup = bs(content, "html.parser")
    tmpArticles = []  # list of articles links for this site

    for a in soup.find_all(class_="ubernode", href=True):  # obtain <a> class for the articles
        if a.text:
            tmpArticles.append(a['href'])  # to get the "href" value

    tmpArticles = [p[:20] + i for i in tmpArticles]  # list of links retrieved from NASA web page

    return tmpArticles


def write_to_file(links_articles):
    """Function used to write down to one file all the links got from the scrapers
        @:param links_articles list of the articles to index"""
    with open("links.txt", "w") as file:

        for link in links_articles:
            file.write(link)
            file.write("\n")


def main():
    """Main function to start the whole scraping action"""

    root_esa = "https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/(archive)/"  # root of ESA website
    root_bo = "https://www.blueorigin.com/news/"  # root page of Blue Origin website
    root_nasa = "https://www.nasa.gov/topics/humans-in-space"  # root page of NASA website

    links_articles = []  # list of all articles links

    i = 5  # index used to set the max page of ESA articles

    for k in range(i):
        links_articles.extend(
            esa_scraper(root_esa + str(k * 50)))  # adding the links retrived from the first "i" ESA pages

    links_articles.extend(bo_scraper(root_bo))  # adding the links retrieved from the Blue Origin page

    links_articles.extend(nasa_scraper(root_nasa))  # adding the links retrieved from the NASA page

    write_to_file(links_articles)


if __name__ == "__main__":
    main()

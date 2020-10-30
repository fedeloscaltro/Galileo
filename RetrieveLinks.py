from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs


driver = wd.Firefox()  # configure webdriver to use Firefox browser

page_links = ("https://www.blueorigin.com/news/",
              "https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/(archive)/0",
              "https://www.nasa.gov/topics/humans-in-space")


def scraper(p):
    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    links_articles = []
    for a in soup.find_all(class_="NewsArchive__postTitleLink", href=True):  # obtain <a> class for te articles
        if a.text:
            links_articles.append(a['href'])  # to get the "href" value

    links_articles = [p+i[8:] for i in links_articles]

    print(links_articles)


def main():
    # for p in page_links:

    scraper(page_links[0])


if __name__ == "__main__":
    main()

from selenium import webdriver as wd
from bs4 import BeautifulSoup as bs


driver = wd.Firefox()  # configure webdriver to use Firefox browser

page_links = []

for k in range(5):
    page_links.append("https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/(archive)/"+str(k*50))

page_links.append("https://www.blueorigin.com/news/")
page_links.append("https://www.nasa.gov/topics/humans-in-space")


def scraper(p, j, links_articles):
    """ Function used to scrape and find the right articles that will be indexed
    @:param p the page to scrape
    @:param j the index of the list of initial pages
    @:param links_articles the list of articles to index; initially empty"""

    driver.get(p)  # to obtain a specified web page
    content = driver.page_source  # get the page content
    soup = bs(content, "html.parser")
    tmpArticles = []

    if j < 5:  # if the page refers to one of the ESA website's pages
        for a in soup.find_all(class_="story", href=True):  # obtain <a> class for the articles
            if a.text:
                tmpArticles.append(a['href'])  # to get the "href" value

        tmpArticles = [p[:19] + i for i in tmpArticles]

    elif j == 5:  # if the page refers to the Blue Origin's page
        for a in soup.find_all(class_="NewsArchive__postTitleLink", href=True):  # obtain <a> class for the articles
            if a.text:
                tmpArticles.append(a['href'])  # to get the "href" value

        tmpArticles = [p + i[8:] for i in tmpArticles]

    '''else:  # if the page refers to the NASA's page
        # print(soup.find_all(class_="card", href=True))
        for a in soup.find_all(class_="card", href=True):  # obtain <a> class for the articles
            if a.text:
                tmpArticles.append(a['href'])  # to get the "href" value

        tmpArticles = [p[:20] + i for i in tmpArticles] '''

    links_articles.extend(tmpArticles)
    # print(links_articles)


def write_to_file(links_articles):
    """Function used to write down to one file all the links got from the scraper
    @:param links_articles list of the articles to index"""
    file = open("links.txt", "w")

    for link in links_articles:
        file.write(link)
        file.write("\n")

    file.close()


def main():
    """Main function to start the whole scraping action"""
    links_articles = []

    for i in range(len(page_links)-1):
        scraper(page_links[i], i, links_articles)

    write_to_file(links_articles)


if __name__ == "__main__":
    main()

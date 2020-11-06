from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs

options = Options()
options.headless = True  # set the option "headless" for the web driver
driver = wd.Firefox(options=options)  # configure webdriver to use Firefox browser


def soup_init(url):
    """Function used to initialize the BeautifulSoup object
    @:param url the URL to parse
    @:return soup the BeautifulSoup object """

    driver.get(url)  # to obtain a specified web page
    html = driver.page_source  # get the page content

    soup = bs(html, features="html.parser")

    return soup


def text_formatting(text):
    """Function used to format the extracted text
    @:param text the text to format
    @:return text the text after the format operation"""

    lines = (line.strip() for line in text.splitlines())  # break into lines and remove leading/trailing space on each

    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))  # break multi-headlines into a line each
    text = '\n'.join(chunk for chunk in chunks if chunk)  # drop blank lines

    return text


def esa_extract(soup):
    """Function used to extract the text from ESA's articles
        @:param soup the HTML parser"""

    for script in soup(["script", "style", "section"]):  # kill all script and style elements
        script.extract()    # rip it out

    for div in soup.findAll('div', attrs={'class': ['article__video', 'meta article__item', 'share']}):
        div.extract()

    for div in soup.findAll('div', attrs={'id': ['cookie_loc']}):
        div.extract()

    text = soup.get_text()  # get text

    return text


def bo_extract(soup):
    """Function used to extract the text from Blue Origin's articles
        @:param soup the HTML parser"""

    for script in soup(["script", "style", "noscript", "footer"]):  # kill all script and style elements
        script.extract()  # rip it out

    for a in soup.findAll('a', attrs={'class': 'Btn_skipToContent Cta__Dark'}):
        a.extract()

    for div in soup.findAll('div', attrs={'class': ['NewsEntry__social']}):
        div.extract()

    for sec in soup.findAll('section', attrs={'class': 'LatestNews'}):
        sec.extract()

    text = soup.get_text()  # get text

    return text


def nasa_extract(soup):
    """Function used to extract the text from NASA's articles
    @:param soup the HTML parser"""

    for script in soup(["script", "style", "button", "img"]):  # kill all script and style elements
        script.extract()  # rip it out

    for id in soup.findAll('div', attrs={'id': ['ember192', 'footer']}):
        id.extract()

    for div in soup.findAll('div', attrs={'class': ['editor-info', 'collapse navbar-collapse ']}):
        div.extract()

    text = soup.get_text()  # get text

    return text


def main():
    """Function called to start the text-extraction procedure"""

    file = open("links.txt", "r")

    lines = file.readlines()

    for url in lines:   # dispatcher for the links
        soup = soup_init(url)   # initialize soup with the url

        if url.find("https://www.esa.int/") != -1:
            text = esa_extract(soup)    # extract the text from an esa article

        elif url.find("https://www.blueorigin.com/") != -1:
            text = bo_extract(soup) # extract the text from a blue origin article

        else:
            text = nasa_extract(soup)   # extract the text from a nasa article

        text = text_formatting(text)    # formatting the text
        #print(text)
        #break

if __name__ == "__main__":
    main()

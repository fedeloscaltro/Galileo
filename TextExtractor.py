from selenium import webdriver as wd
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.wait import WebDriverWait
from datetime import datetime

options = Options()
options.headless = True  # set the option "headless" for the web driver
driver = wd.Firefox(options=options)  # configure webdriver to use Firefox browser


def soup_init(url):
    """Function used to initialize the BeautifulSoup object
    @:param url the URL to parse
    @:return soup the BeautifulSoup object """

    driver.get(url)  # to obtain a specified web page
    html = WebDriverWait(driver, timeout=30).until(lambda d: d.page_source)  # get the page content

    soup = bs(html, features="html.parser")
    soup.url = url

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
        @:param soup the HTML parser
        @:return text the extracted text of the article"""

    for script in soup(["script", "style", "section", "figcaption", "ol"]):  # kill all noising elements
        script.extract()  # rip it out

    text = soup.findAll("div", attrs={"class": "meta article__item"})[0].get_text()  # get the publication's date
    text = text.split('\n')[1]

    dd = text[:2]
    mm = text[3:5]
    yyyy = text[6:]

    text = yyyy+'-'+mm+'-'+dd+'\n'

    text += soup.url+'\n'   # add url to the file's text

    for div in soup.findAll('div', attrs={'class': ['article__video',
                                                    'share']}):  # kill video-related and share contents
        div.extract()

    for par in soup(["p", "h1", "h2"]):
        text += par.get_text() + '\n'  # obtain the desired text

    return text


def bo_extract(soup):
    """Function used to extract the text from Blue Origin's articles
        @:param soup the HTML parser
        @:return text the extracted text of the article"""

    text = soup.findAll("span", attrs={'class': 'NewsEntry__meta-date'})[0].get_text()  # get the publication's date

    text = str(datetime.strptime(text, '%b %d, %Y'))    # formatting the date
    text = text[:10]
    day = text[8:10]
    month = text[5:7]
    year = text[:4]
    text = year + '-' + month + '-' + day + '\n'    # add the date at the beginning of the text
    text += soup.url + '\n'  # add url to the file's text

    for script in soup(["script", "style", "noscript", "footer", "header", "title"]):  # deleting all noising elements
        script.extract()  # rip it out

    for a in soup.findAll('a', attrs={'class': 'Btn_skipToContent Cta__Dark'}):
        a.extract()

    for p in soup.findAll('p', attrs={'class': 'image-caption'}):
        p.extract()

    for div in soup.findAll('div', attrs={'class': ['NewsEntry__social']}):
        div.extract()

    for sec in soup.findAll('section', attrs={'class': 'LatestNews'}):
        sec.extract()

    for span in soup.findAll('span', attrs={'class': 'NewsEntry__meta Kicker'}):
        span.extract()

    text += soup.get_text()  # get text

    return text


def space_com_extract(soup):
    """Function used to extract the text from NASA's articles
    @:param soup the HTML parser
    @:return text the extracted text of the article"""

    date = soup.find("time")['datetime'][:10]   # get the publication's date
    yyyy = date[:4]     # formatting the date
    mm = date[5:7]
    dd = date[8:10]
    date = yyyy + "-" + mm + "-" + dd + "\n"

    text = date    # add the date at the beginning of the text

    text += soup.url + '\n'  # add url to the file's text

    for dell in soup.findAll('div', attrs={'class': ['failuremessage --hide-me', 'successmessage --hide-me',
                                                     'sc-bdVaJa cAfMzi', 'byline-social']}):
        dell.extract()

    for script in soup(["script", "style", "button", "form", "aside", "footer", "em"]):  # kill all noising elements
        script.extract()  # rip it out

    for par in soup(["p", "h1"]):   # find the relevant article parts
        text += par.get_text() + '\n'

    return text


def main():
    """Function called to start the text-extraction procedure"""

    file_name = "links.txt"

    with open(file_name, "r") as file:    # opening the file with all the links
        n_links = int(file.readline())   # from which line start to read the file
        lines = file.readlines()[n_links:]

    for url in lines:   # dispatcher for the links
        soup = soup_init(url)   # initialize soup with the url

        with open("Articles/"+str(n_links)+".txt",
                  "w", encoding='utf-8') as f_articles:  # creating 1 article per link

            if url.find("https://www.esa.int/") != -1:
                text = esa_extract(soup)    # extract the text from an ESA article

            elif url.find("https://www.blueorigin.com/") != -1:
                text = bo_extract(soup)  # extract the text from a Blue Origin article

            else:
                text = space_com_extract(soup)   # extract the text from a Space.com article

            text = text_formatting(text)    # formatting the text

            f_articles.write(text)  # writing the text down to the file

            n_links += 1

    driver.quit()

if __name__ == "__main__":
    main()

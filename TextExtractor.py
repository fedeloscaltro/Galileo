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

    text = text_formatting(text)

    print(text)


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

    text = text_formatting(text)

    print(text)


def nasa_extract(soup):
    """Function used to extract the text from NASA's articles
    @:param soup the HTML parser"""

    for script in soup(["script", "style"]):  # kill all script and style elements
        script.extract()  # rip it out

    for id in soup.findAll('div', attrs={'id': ['ember192', 'footer']}):
        id.extract()

    for cls in soup.findAll('div', attrs={'class': 'editor-info'}):
        cls.extract()

    text = soup.get_text()  # get text

    text = text_formatting(text)

    print(text)


def main():
    """Function called to start the text-extraction procedure"""

    url1 = "https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/Orion/First_European_Service_Module_for_Orion_finished_assembly"
    url2 = "https://www.blueorigin.com/news/blue-origin-s-original-charon-flying-vehicle-goes-on-display-at-the-museum-of-flight"
    url3 = "https://www.nasa.gov/press-release/nasa-names-robyn-gatens-acting-director-for-international-space-station"

    soup = soup_init(url3)

    file = open("links.txt", "r")

    lines = file.readlines()

    """for url in lines:
        if url.find("esa.int") != -1:
            print("ESA")
        elif url.find("blueorigin.com") != -1:
            print("BO")
        else:
            print("NASA")"""

    esa_extract(soup)
    bo_extract(soup)
    nasa_extract(soup)

if __name__ == "__main__":
    main()

import requests
from bs4 import BeautifulSoup


def extract_article(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    div = soup.find("div", attrs={"class" : "single-post__content wpb_text_column"})

    text_soup = BeautifulSoup(str(div))

    texts = text_soup.find_all("p")
    texts = [txt.text for txt in texts]

    text = " ".join(texts)
    return text
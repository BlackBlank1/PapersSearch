# encoding: utf-8
# @File  : AAAI.py
# @Author: myarme
# @Date  : 2025/01/23/10:27
from time import sleep

import requests
from bs4 import BeautifulSoup

from utils.tools import translator

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}


def get_papers_abstract(url):
    req = requests.get(url, headers=headers)
    try:
        soup = BeautifulSoup(req.text, 'html.parser')
        try:
            abstract = soup.select_one('section[class="item abstract"]').text.strip().split("Abstract")[1].strip()
        except:
            abstract = ''
        try:
            download_link = soup.select_one('a[class="obj_galley_link pdf"]')['href']
        except:
            download_link = ''
        return translator(abstract), download_link
    except:
        return


def get_papers(keyword, year):

    url = (f"https://ojs.aaai.org/index.php/AAAI/search/search?query={keyword}&dateFromYear={year}&dateFromMonth"
           "=&dateFromDay=&dateToYear=&dateToMonth=&dateToDay=&authors=")

    req = requests.get(url, headers=headers)
    try:
        soup = BeautifulSoup(req.text, 'html.parser')
        papers_list = []
        for i in soup.select("div.search_results > div"):
            papers_dict = {'title': i.select_one('h2.title a').text.strip(), 'url': i.select_one('h2.title a')['href'],
                           'authors': i.select_one('div.authors').text.strip(),
                           'published': i.select_one('div.published').text.strip()}
            papers_list.append(papers_dict)
            print(papers_dict['title'])
        for paper in papers_list:
            paper['abstract'], paper['download_link'] = get_papers_abstract(paper['url'])
            sleep(3)

        print(papers_list)

        return papers_list
    except:
        return []


if __name__ == '__main__':
    get_papers("rumor", "2024")

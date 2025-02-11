# encoding: utf-8
# @File  : ACL.py
# @Author: myarme
# @Date  : 2025/02/11/09:15
from time import sleep

import requests
from bs4 import BeautifulSoup

from utils.tools import translator, translate_month

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}


def get_papers_abstract(url):
    req = requests.get(url, headers=headers)
    try:
        soup = BeautifulSoup(req.text, 'html.parser')
        try:
            abstract = soup.select_one('div[class="card-body acl-abstract"] > span').text.strip()
        except:
            abstract = ""
        try:
            authors = soup.select_one('p.lead').text.strip().replace('\n', ' ')
        except:
            authors = ""
        try:
            published = soup.select_one('dl > dd:nth-child(8)').text + "-" + translate_month(soup.select_one('dl > dd:nth-child(6)').text)
        except:
            published = ""
        try:
            download_link = soup.select_one('div[class="acl-paper-link-block"] > a:nth-child(1)')['href']
        except:
            download_link = ''
        return translator(abstract), authors, published, download_link, abstract
    except:
        return


def get_papers(keyword, year):
    url = f'https://aclanthology.org/events/acl-{year}/'

    req = requests.get(url, headers=headers)
    #
    try:
        soup = BeautifulSoup(req.text, 'html.parser')
        papers_list = []
        for i in soup.select('p[class ="d-sm-flex align-items-stretch"]'):

            paper_link = i.select_one('span[class="d-block"] > strong > a')

            papers_dict = {}
            if keyword.capitalize() in paper_link.text.strip() or keyword.lower() in paper_link.text.strip():
                papers_dict['title'] = paper_link.text.strip()
                print(papers_dict['title'])
                if "https://aclanthology.org/" in i.select_one('span[class="d-block"] > strong > a')['href']:
                    papers_dict['url'] = i.select_one('span[class="d-block"] > strong > a')['href']
                else:
                    papers_dict['url'] = "https://aclanthology.org/" + paper_link['href']

                papers_list.append(papers_dict)

        for paper in papers_list:

            paper['abstract'], paper['authors'], paper['published'], paper['download_link'], paper['raw_abstract'] \
                = get_papers_abstract(paper['url'])
            sleep(3)

        print(papers_list)

        return papers_list
    except:
        return []


if __name__ == '__main__':
    get_papers('rumor', 2023)

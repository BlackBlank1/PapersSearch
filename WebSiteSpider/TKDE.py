# encoding: utf-8
# @File  : TKDE.py
# @Author: myarme
# @Date  : 2025/01/23/13:07
from time import sleep

import requests
from bs4 import BeautifulSoup

from utils.tools import translator

headers = {
    'origin': 'https://ieeexplore.ieee.org',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0'
}


def get_time(paper_id):
    try:
        tim = requests.get(f'https://ieeexplore.ieee.org/rest/document/{paper_id}/similar', headers=headers)
        if tim.status_code == 200:
            if tim.json()['lastupdate']:
                return tim.json()['lastupdate']
            else:
                return ''
        else:
            return ''
    except:
        return ''


def get_paper_info(paper_id):
    paper_url = 'https://ieeexplore.ieee.org/document/' + paper_id
    req = requests.get(paper_url, headers=headers)
    if req.status_code == 200:
        try:
            soup = BeautifulSoup(req.text, 'html.parser')
            # 提取作者信息
            try:
                authors = soup.select('meta[name="parsely-author"]')
                authors_list = [author.get('content') for author in authors]
                authors_list = ", ".join(authors_list)
            except:
                authors_list = ''
            try:
                abstract = soup.find('meta', property='twitter:description')['content']
            except:
                abstract = ''
            try:
                pub_time = get_time(paper_id)
            except:
                pub_time = ''
            sleep(2)
            return authors_list, translator(abstract), pub_time
        except:
            return '', '', ''
    else:
        return '', '', ''


def get_papers(keyword, year):
    json_data = {
        'queryText': "TKDE",
        'highlight': True,
        'returnType': 'SEARCH',
        'matchPubs': True,
        'searchWithin': [
            keyword,
        ],
        'ranges': [
            f'{year}_{year}_Year',
        ],
        'returnFacets': [
            'ALL',
        ],
        'sortType': 'newest',
    }

    response = requests.post('https://ieeexplore.ieee.org/rest/search', headers=headers, json=json_data).json()
    papers_list = []
    if response:
        for paper in response['records']:
            paper_dict = {}
            paper_dict['title'] = paper['articleTitle']
            paper_dict['url'] = 'https://ieeexplore.ieee.org' + paper['pdfLink']
            authors, abstract, pub_time = get_paper_info(paper['articleNumber'])
            paper_dict['published'] = pub_time
            paper_dict['authors'] = authors
            paper_dict['abstract'] = abstract
            paper_dict['download_link'] = ''
            papers_list.append(paper_dict)
            print(paper_dict['title'])
            sleep(1)
        return papers_list
    else:
        return []


if __name__ == '__main__':
    data = get_papers('fake news', '2024')
    print(data)

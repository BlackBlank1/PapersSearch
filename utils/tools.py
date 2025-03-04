# encoding: utf-8
# @File  : tools.py
# @Author: myarme
# @Date  : 2025/01/23/10:43
from datetime import datetime

import translators as ts


def translator(text, chunk_size=1000):
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    translated_text = ""
    for chunk in chunks:
        try:
            translated_chunk = ts.translate_text(chunk, from_language="en", to_language="zh", translator="bing")
            translated_text += translated_chunk
        except ts.server.TranslatorError as e:
            print(f"翻译错误：{e}")
            translated_text += chunk
    return translated_text


def sort_papers(papers_list):

    for paper in papers_list:
        paper['published'] = datetime.strptime(paper['published'], '%Y-%m-%d')

    papers_list.sort(key=lambda x: x['published'], reverse=True)

    for paper in papers_list:
        paper['published'] = paper['published'].strftime('%Y-%m-%d')

    return papers_list


def translate_month(month_name):
    month_dict = {
        "January": "01-01",
        "February": "02-01",
        "March": "03-01",
        "April": "04-01",
        "May": "05-01",
        "June": "06-01",
        "July": "07-01",
        "August": "08-01",
        "September": "09-01",
        "October": "10-01",
        "November": "11-01",
        "December": "12-01"
    }
    return month_dict.get(month_name, "未知月份")


if __name__ == '__main__':
    long_text = "Detecting fake news requires both a delicate sense of diverse clues and a profound understanding of the real-world background, which remains challenging for detectors based on small language models (SLMs) due to their knowledge and capability limitations. Recent advances in large language models (LLMs) have shown remarkable performance in various tasks, but whether and how LLMs could help with fake news detection remains underexplored. In this paper, we investigate the potential of LLMs in fake news detection. First, we conduct an empirical study and find that a sophisticated LLM such as GPT 3.5 could generally expose fake news and provide desirable multi-perspective rationales but still underperforms the basic SLM, fine-tuned BERT. Our subsequent analysis attributes such a gap to the LLM's inability to select and integrate rationales properly to conclude. Based on these findings, we propose that current LLMs may not substitute fine-tuned SLMs in fake news detection but can be a good advisor for SLMs by providing multi-perspective instructive rationales. To instantiate this proposal, we design an adaptive rationale guidance network for fake news detection (ARG), in which SLMs selectively acquire insights on news analysis from the LLMs' rationales. We further derive a rationale-free version of ARG by distillation, namely ARG-D, which services cost-sensitive scenarios without inquiring LLMs. Experiments on two real-world datasets demonstrate that ARG and ARG-D outperform three types of baseline methods, including SLM-based, LLM-based, and combinations of small and large language models."

    result = translator(long_text)
    print(result)

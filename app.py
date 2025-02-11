from flask import Flask, request
from flask_cors import CORS  # 引入 CORS

from WebSiteSpider import AAAI, TKDE, ACL
from utils.results import success
from utils.tools import sort_papers

app = Flask(__name__)
CORS(app)


@app.route('/papers', methods=['POST'])
def papers():
    text_data = request.get_json()

    print(text_data)

    paper_list = []

    if text_data['platform'] == 'aaai':
        paper_list = AAAI.get_papers(text_data['keyword'], text_data['year'])
    elif text_data['platform'] == 'tkde':
        paper_list = TKDE.get_papers(text_data['keyword'], text_data['year'])
    elif text_data['platform'] == 'acl':
        paper_list = ACL.get_papers(text_data['keyword'], text_data['year'])

    try:
        sorted_papers = sort_papers(paper_list)
    except:
        sorted_papers = paper_list

    return success("请求成功！", 200, data=sorted_papers)


if __name__ == '__main__':
    app.run()

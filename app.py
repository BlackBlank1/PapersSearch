from flask import Flask, request
from flask_cors import CORS  # 引入 CORS

from WebSiteSpider import AAAI, TKDE
from utils.results import success

app = Flask(__name__)
CORS(app)


@app.route('/aaai_papers', methods=['POST'])
def aaai_papers():

    text_data = request.get_json()
    print(text_data)
    paper_list = []
    if text_data['platform'] == 'aaai':
        paper_list = AAAI.get_papers(text_data['keyword'], text_data['year'])
    elif text_data['platform'] == 'tkde':
        paper_list = TKDE.get_papers(text_data['keyword'], text_data['year'])
    return success("请求成功！", 200, data=paper_list)


if __name__ == '__main__':
    app.run()

import json

import feedparser
import requests
from openai import OpenAI

client = OpenAI()

system_prompt = """
请根据文本提供一份摘要，并提取五个关键点，生成三个可能感兴趣的读者问题。并确保以上所有内容都输出为JSON格式（确保JSON有效，并可以通过JSON.parse()解析），格式如下：
{
  "summary": "摘要",
  "key_points": ["关键点1", "关键点2", "关键点3", "关键点4", "关键点5"],
  "questions": ["问题1", "问题2", "问题3"]
}
重要的是，摘要部分应使用Markdown编写，以确保布局整洁有吸引力。请仅以json格式和纯文本（非Markdown）输出内容，不要添加其他任何文字，原始文本可能是任何语言，输出结果也需确保为简体中文。
"""


def summarize(content):
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": content}]

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False,
        response_format={
            'type': 'json_object'
        }
    )

    print(json.loads(response.choices[0].message.content))


def fetch(rss_url):
    """
    从rss_url解析
    :param rss_url:
    :return:
    """
    # 解析RSS Feed

    articles = []

    feed = feedparser.parse(rss_url)
    for entry in feed.entries:
        # 获取文章的原始链接
        original_link = entry.link  # 获取链接
        title = entry.title if 'title' in entry else 'No Title Available'
        published = entry.published if 'published' in entry else 'No Date Provided'
        articles.append((title, original_link, published))

    return articles


if __name__ == '__main__':
    lst = fetch("https://rss_url")
    print('准备处理: ', len(lst), '篇文章')
    for each in lst:
        resp = requests.get(f'https://r.jina.ai/{each[1]}')
        if resp.status_code == 200:
            summarize(resp.content.decode('utf-8'))

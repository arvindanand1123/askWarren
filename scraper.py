from multiprocessing import Process, Manager
from datetime import datetime
from bs4 import BeautifulSoup
import argparse
import requests
import json
import re

keyword = "microsoft"
SITE_URL = 'https://old.reddit.com/r/' + keyword + '/new'
REQUEST_AGENT = 'Mozilla/5.0 Chrome/47.0.2526.106 Safari/537.36'

def createSoup(url):
    return BeautifulSoup(requests.get(url, headers={'User-Agent':REQUEST_AGENT}).text, 'lxml')

def getSearchResults(searchUrl):
    posts = []
    while True:
        resultPage = createSoup(searchUrl)
        id = re.compile("thing_t3_\w\w\w\w\w\w")
        posts += resultPage.findAll('div', {'id': id})
        footer = resultPage.findAll('a', {'rel':'nofollow next'})
        print("Ran getSearchResults")
        if footer:
            searchUrl = footer[-1]['href']
            print(footer[-1]['href'])
        else:
            print(posts)
            return posts

def parseComments(commentsUrl):
    commentTree = {}
    commentsPage = createSoup(commentsUrl)
    commentsDiv = commentsPage.find('div', {'class':'sitetable nestedlisting'})
    comments = commentsDiv.findAll('div', {'data-type':'comment'})
    for comment in comments:
        numReplies = int(comment['data-replies'])
        tagline = comment.find('p', {'class':'tagline'})
        author = tagline.find('a', {'class':'author'})
        author = "[deleted]" if author == None else author.text
        date = tagline.find('time')['datetime']
        date = datetime.strptime(date[:19], '%Y-%m-%dT%H:%M:%S')
        commentId = comment.find('p', {'class':'parent'}).find('a')['name']
        content = comment.find('div', {'class':'md'}).text.replace('\n','')
        score = comment.find('span', {'class':'score unvoted'})
        score = 0 if score == None else int(re.match(r'[+-]?\d+', score.text).group(0))
        parent = comment.find('a', {'data-event-action':'parent'})
        parentId = parent['href'][1:] if parent != None else '       '
        parentId = '       ' if parentId == commentId else parentId
        print(commentId, 'date:', date, 'reply-to:', parentId, 'num-replies:', numReplies, content[:63])
        commentTree[commentId] = {'text':content,'date':str(date)}
    return commentTree

def parsePost(post, results):
    time = post.find('time')['datetime']
    date = datetime.strptime(time[:19], '%Y-%m-%dT%H:%M:%S')
    title = post.find("a",class_="title").text
    # score = post.find('span', {'class':'search-score'}).text
    # score = int(re.match(r'[+-]?\d+', score).group(0))
    # author = post.find('a', {'class':'author'}).text
    # subreddit = post.find('a', {'class':'search-subreddit-link'}).text
    commentsTag = post.find('a', {'class':'bylink comments may-blank'})
    if commentsTag['href'] == None:
        url = ""
    else:
        url = commentsTag['href']
    numComments = int(re.match(r'\d+', commentsTag.text).group(0))
    print("\n" + str(date)[:19] + ":", numComments, title)
    commentTree = {} if numComments == 0 else parseComments(url)
    results.append({'title':title, 'url':url, 'date':str(date), 'comments':commentTree})

if __name__ == '__main__':
    try:
        product = json.load(open('product.json'))
    except FileNotFoundError:
        print('WARNING: Database file not found. Creating a new one...')
        product = {}
    searchUrl = SITE_URL
    print('Search URL:', searchUrl)
    posts = getSearchResults(searchUrl)
    print('Started scraping', len(posts), 'posts.')
    results = Manager().list()
    jobs = []
    for post in posts:
        job = Process(target=parsePost, args=(post, results))
        jobs.append(job)
        job.start()
    for job in jobs:
        job.join()
    product['posts'] = list(results)
    with open('product.json', 'w', encoding='utf-8') as f:
        json.dump(product, f, indent=4, ensure_ascii=False)

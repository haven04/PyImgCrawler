#-*- coding: utf-8 -*-
import os.path
import argparse
import mechanize
from urlparse import urlparse
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# usage: $ python 'target_url' 'local_download_path'
# e.g., $ python 'http://www.google.com' './download'


def rm_duplicates(lst):
    seen = set()
    seen_add = seen.add
    return [el for el in lst if not (el in seen or seen_add(el))]


def download(browser, url, fp):
    # req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    # urllib.request.urlretrieve(req, fp)
    browser.retrieve(url, fp)
    print url, "\t==>\t", fp


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('target_url')
    arg_parser.add_argument('downpath')
    args = arg_parser.parse_args()
    default_scheme = urlparse(args.target_url).scheme

    '''load lists of img files'''
    br = mechanize.Browser()
    br.addheaders = [('User-Agent', 'Mozilla/5.0')]
    webpage = br.open(args.target_url)
    soup = BeautifulSoup(webpage, 'html.parser')
    imglist = soup.find_all('img')
    # imglist = [(img['src'], img['src'].split('/')[-1]) for img in imglist]
    imglist = [(default_scheme + ':' + img['src']
        if img['src'].startswith('//')
        else img['src'], img['src'].split('/')[-1])
        for img in imglist]

    '''removes duplicates'''
    imglist = rm_duplicates(imglist)
    dec_cnt = len(str(len(imglist)))

    '''download imgs'''
    if not os.path.exists(args.downpath):
        os.makedirs(args.downpath)

    for idx, imgurl in enumerate(imglist):
        idxstr = '%0*d' % (dec_cnt, idx)
        resultpath = os.path.join(args.downpath, idxstr + '.' + imgurl[1])
        download(br, imgurl[0], resultpath)

    # print("Completed to download %d files." % len(imglist))

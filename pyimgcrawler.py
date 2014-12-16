import re
import urllib.request
import os.path

TARGET_URL = "www.google.com"
DOWNPATH = "./path"

# when the target html file is in local
# TARGET_URL = "file:///"+(os.path.abspath(TARGET_URL))

def rm_duplicates(lst):
    seen = set()
    seen_add = seen.add
    return [el for el in lst if not (el in seen or seen_add(el))]

def download(url, fp):
    urllib.request.urlretrieve(url, fp)
    print(url, "\t==>\t", fp)

if __name__ == "__main__":
    '''load lists of img files'''
    webpage = urllib.request.urlopen(TARGET_URL).read().decode('UTF-8')
    imglist = [res for res in re.findall(r"((?:http|https|ftp):\/\/[\w.\/?]*?\.(jpg|JPG|png|PNG))", webpage)]

    '''removes duplicates'''
    imglist = rm_duplicates(imglist)
    dec_cnt = len(str(len(imglist)))

    '''download imgs'''
    if not os.path.exists(DOWNPATH):
        os.makedirs(DOWNPATH)

    for idx, imgurl in enumerate(imglist):
        idxstr = '%0*d' % (dec_cnt, idx)
        resultpath = os.path.join(DOWNPATH, idxstr + '.' + imgurl[1])
        download(imgurl[0], resultpath)

    print("Completed downloads of %d files." % len(imglist))

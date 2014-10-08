"""
Author: Bharadwaj Srigiriraju

A simple web crawler script that crawls a given website (limited to 2 levels).

"""

import re
import requests
import urlparse
import urllib

ignore_list = ["$\w*.js", "$\w*.png", "$\w*.jpg", "$\w*.jpeg", "^javascript:void\w*"]

name_list = []
link_name = {}
res = []

def crawl(url, max_level=2):
    """
    Crawls the given URL, upto specified number of levels excluding
    the links which fall into the patterns mentioned in config file
    and types of files/links in ignore_list above.
    """
    if max_level == 0:
        return []

    req = requests.get(url)
    if req.status_code != 200:
        return []

    links_in_page = link_regexp.findall(req.text)

    with open('config') as f:
        do_not_visit = f.readlines()
    do_not_visit = [x.strip('\n') for x in do_not_visit]

    do_not_download = do_not_visit
    do_not_download += ignore_list

    for link in links_in_page:
        visit = True

        for pattern in do_not_download:
            if len(re.findall(pattern, link)) > 0:
                visit = False
        if visit:
            if link[:4] == "http":
                if link[:5] == "https":
                    link = link[8:]
                else:
                    link = link[7:]

            full_link = urlparse.urljoin(url, link)
            if full_link not in link_name:
                link_name[full_link] = link
                crawl(full_link, max_level-1)

    return []


def download_links(link_name):
    """
    Downloads all the links previously crawled by the crawler function
    to the download directory.
    """
    for link in link_name:
        name = str(link_name[link])
        location = "downloads/" + name + ".html"
        try:
            urllib.urlretrieve(link, location)
        except IOError:
            pass
    return


if __name__ == "__main__":
    print "Enter the website you want to crawl"
    inp = raw_input()
    pattern = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
    link_regexp = re.compile('href="(.*?)"')
    urls = re.findall(pattern, inp)
    if len(urls) != 1:
        print "Wrong URL entered. Please check the URL"
        exit()
    url = urls[0]
    final = crawl(url)
    download_links(link_name)

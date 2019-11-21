#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import csv


def pagevisit(url_):
    with urllib.request.urlopen(url_) as url:
        html = url.read()
    soup = BeautifulSoup(html, features="lxml")
    return soup


def get_author(soup):
    author = soup.find(attrs={"class": "commit-author"})
    return author.contents


def get_title(soup):
    title = soup.find(attrs={"class": "commit-title"})
    return title.contents


def get_main_div(soup):
    main_div = soup.find('main')
    print(main_div.contents)
    return main_div.contents


def export_to_csv(commits):
    with open('github_commit_data.csv', mode='w') as gh_commit_file:
        fieldnames = commits[0].keys()
        gh_commits = csv.DictWriter(gh_commit_file, fieldnames=fieldnames)
        gh_commits.writeheader()
        for c in commits:
            gh_commits.writerow(c)


def get_commit_content(url):
    soup = pagevisit(url)
    content = {}
    content['author'] = get_author(soup)
    content['commit_title'] = get_title(soup)
    # problematic since we cannot parse some of the html tag to csv - need to find solution
    # content['main_div'] = get_main_div(soup)
    return content


if __name__ == "__main__":
    urls = ["https://github.com/flipboxstudio/lumen-generator/commit/3a7cb3db5ccb1c1967a568b72bc728636e41ef45"]
    contents = []
    for url in urls:
        contents.append(get_commit_content(url))
    export_to_csv(contents)

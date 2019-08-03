#!/usr/bin/env python
"""Parse Leetcode/Lintcode html page to markdown."""

import sys
from pyquery import PyQuery
import requests
import html2text

from leetcode import Leetcode

class OJHtml2Markdown(object):
    """Parse Leetcode/Lintcode html page to markdown."""

    def __init__(self, url, prefer_leetcode=False):
        """Init."""
        self._prefer_leetcode = prefer_leetcode
        url = url.strip().rstrip('/').replace('/zh-cn/', '/en/')
        key_end = url.find('.com/')
        self._site = url[key_end - 8:key_end]
        self._url = url
        self._markdown = None
        try:
            self._raw_p_html = PyQuery(url=url)
        except Exception as e:
            self._markdown = e

        self._p_url_path = url.split('/')[-1]
        self._p_urls = {}
        self.leetcode = Leetcode()

    def _lint2leet(self):
        """Replace lintcode with leetcode if prefer leetcode."""
        if self._url.startswith('https://leetcode.com/problems/'):
            return
        url = 'https://leetcode.com/problems/{}/'.format(self._p_url_path)
        response = requests.head(url)
        if response.status_code == 200:
            self._site = 'leetcode'
            self._url = url
            # self._raw_p_html = PyQuery(url=self._url)

    def _gen_p_url_lists(self, p_title):
        """Generate leetcode/lintcode problem url lists."""
        leetcode_url = 'https://leetcode.com/problems/{}/'.format(self._p_url_path)
        lintcode_url = 'https://www.lintcode.com/problem/{}/'.format(self._p_url_path)
        for url in [leetcode_url, lintcode_url]:
            response = requests.head(url)
            if response.status_code == 200:
                key_end = url.find('.com/')
                site = url[key_end - 8:key_end]
                self._p_urls[site] = url
        p_url_lists = []
        for site in sorted(self._p_urls):
            p_list = '- {site}: [{title}]({url})'.format(
                site=site, title=p_title, url=self._p_urls[site])
            p_url_lists.append(p_list)
        return p_url_lists

    def _get_p_title(self):
        """Get problem title."""
        p_title = self._raw_p_html('title').text().split('|')[0].strip()
        if p_title.endswith('LeetCode'):
            p_title = p_title[:len(p_title) - len('- LeetCode')].strip()
        return p_title

    def _run_method(self, method):
        return getattr(self, '{}{}'.format(
            method,
            self._site))()

    def gen_markdown(self):
        """Generate markdown with problem html."""
        leet_url = self._url.startswith('https://leetcode.com/problems')
        lint_url = self._url.startswith('https://www.lintcode.com/problem')
        if not (leet_url or lint_url):
            return self._markdown or 'Invalid URL!!!'
        h = html2text.HTML2Text()
        if self._prefer_leetcode:
            self._lint2leet()
        leetcode_data = self.leetcode.get_problem_raw(self._url)['data']['question']
        p_title = leetcode_data['title']
        p_body = leetcode_data['content']
        p_difficulty = leetcode_data['difficulty']
        raw_p_tags = [i['name'] for i in leetcode_data['topicTags']]
        raw_p_tags.append(p_difficulty)
        # p_tags = [tag.replace(' ', '_') for tag in raw_p_tags]
        p_tags = raw_p_tags
        # markdown output
        lines = []
        lines.append('# {}\n'.format(p_title))
        tags = ', '.join(p_tags)
        lines.append('Tags: {}\n'.format(tags))
        lines.append('## Question\n')
        p_url_lists = self._gen_p_url_lists(p_title)
        lines.extend(p_url_lists)
        lines.append('\n### Problem Statement\n')
        lines.append(h.handle(p_body))
        return '\n'.join(lines)


def main(argv):
    """Parse from html to markdown."""
    if (len(argv) == 2):
        scripts, url = argv
        prefer_leetcode = False
    elif (len(argv) == 3):
        scripts, url, prefer_leetcode = argv
    else:
        print("Usage: python ojhtml2markdown.py problem_url [prefer_leetcode]")
        sys.exit(1)
    ojhtml2markdown = OJHtml2Markdown(url, prefer_leetcode)
    print(ojhtml2markdown.gen_markdown())

if __name__ == "__main__":
    main(sys.argv)

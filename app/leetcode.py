#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import Template
import requests


class Leetcode(object):

    def __init__(self):
        self._graphql_url = 'https://leetcode.com/graphql'
        self.user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

    def _init_url(self, url):
        self.driver = requests.Session()
        self.driver.headers.update(self.user_agent)
        self.url = self._clean_url(url)
        print('init URL: {}'.format(self.url))
        self.problem_slug = self.url.split('/')[-1]
        response = self.driver.get(self.url)
        assert response.status_code == 200
    
    def _graphql_query(self):
        query_template = """
        {
            question(titleSlug: "$title_slug") {
                title
                titleSlug
                content
                difficulty
                topicTags {
                    name
                    slug
                }
            }
        }
        """
        query = Template(query_template).substitute(title_slug=self.problem_slug)
        return self.driver.post(self._graphql_url, json={'query': query})

    def get_title(self):
        print('get title...')
        raw_title = self.driver.title
        title = raw_title[:-len(' - LeetCode')].strip()
        return title

    def get_description(self):
        print('get description...')
        elem = self.driver.find_element_by_class_name('question-description')
        return elem.get_attribute('innerHTML')
    
    def get_difficulty(self):
        print('get difficulty...')
        # elem = self.driver.find_element_by_class_name('difficulty-label')
        print(self.driver)
        elem = self.driver.find_element_by_name('question-detail-main-tabs')
        print(elem)
        return elem.get_attribute('innerHTML')

    def get_tags(self):
        print('get tags...')
        tags_id = self.driver.find_element_by_id('tags-topics')
        tags_id_a = tags_id.find_elements_by_tag_name('a')
        tags = []
        for i in tags_id_a:
            tag = i.get_attribute('innerHTML')
            tags.append(tag)
        return tags
    
    def _clean_url(self, url):
        new_url = ['https:/', 'leetcode.com', 'problems']
        problem_slug = url[len('https://'):].strip('/').split('/')[2]
        new_url.append(problem_slug)
        return '/'.join(new_url)

    def get_problem_raw(self, url):
        self._init_url(url)
        response = self._graphql_query()
        return response.json()

    def get_problem_all(self, url):
        """获取所有细节"""
        print('get all the problem detail...')
        self.open_url(url)
        title = self.get_title()
        difficulty = self.get_difficulty()
        tags = self.get_tags()
        description = self.get_description()
        problem = {
            'title': title,
            'difficulty': difficulty,
            'tags': tags,
            'description': description,
            'url': self._clean_url(url)
        }
        self.teardown()
        return problem


if __name__ == '__main__':
    url = 'https://leetcode.com/problems/palindrome-number'
    leetcode = Leetcode()
    # print(leetcode.get_problem_all(url))
    response = leetcode.get_problem_raw(url)
    print(response)

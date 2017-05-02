#!/usr/bin/python

import random
import string
import logging

from bs4 import BeautifulSoup

html_report = open('table_content.html', 'r+')
soup = BeautifulSoup(html_report, 'html.parser')


def _gen_random_str(length):
    return ''.join(random.choice(string.lowercase) for i in range(length))


def add_id_to_tag(tag_name):
    """

    Add tag id to a specified tag_name
    :param tag_name:
    :return: Dictionary {'tag_name_randomstring': {'id': 'randomstring', 'text': 'text'}}

    """
    all_tags = soup.find_all(tag_name)
    if all_tags:
        dict_tag = {}
        for tag in all_tags:
            dict_temp = {}
            try:
                dict_temp['id'] = tag.attrs['id']
                dict_temp['text'] = tag.text
                dict_key = str(tag_name) + '_' + tag.attrs['id']
                dict_tag[dict_key] = dict_temp
            except:
                logging.info('No id attribute in tag %s' % tag)
                tag['id'] = '%s' % _gen_random_str(10)
                dict_temp['id'] = tag['id']
                dict_temp['text'] = tag.text
                dict_key = str(tag_name) + '_' + tag.attrs['id']
                dict_tag[dict_key] = dict_temp
        return dict_tag


def h2_table_of_contents():
    """
    Add tag 'a'. Attribute href has value of id of h2 element
    """
    all_tags_h2 = soup.find_all('h2')

    if all_tags_h2:
        dict_tag = {}
        for tag in all_tags_h2:
            if 'Table of contents' in tag:
                continue
            dict_tag[tag.text] = tag.attrs['id']
        for item in dict_tag.items():
            new_tag = soup.new_tag('a', href='#'+item[1])
            soup.body.insert(3, new_tag)
            new_tag.string = item[0]
            new_tag.append(soup.new_tag('br'))


def main():
    add_id_to_tag('h1')
    add_id_to_tag('h2')
    add_id_to_tag('h3')
    add_id_to_tag('p')
    h2_table_of_contents()


if __name__ == "__main__":
    main()

    html_report.close()
    html = soup.prettify("utf-8")
    with open("final_test_report.html", "wb") as tmp_file:
        tmp_file.write(html)

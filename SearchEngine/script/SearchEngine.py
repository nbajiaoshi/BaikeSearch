#coding:utf-8
import json
import re

import gc

import pickle
from os import mkdir
from urllib.request import urlopen

from os.path import exists

from util import *


def download_picture(work_path, url):
    name = url.split('/')[-1]
    if not exists(work_path):
        mkdir(work_path)
    filename = join(work_path, name)
    if exists(filename):
        return
    with open(filename, 'wb') as f:
        web = urlopen(url)
        f.write(web.read())
    return filename


def trunc_list(l, start, end):
    if len(l) < start:
        return []
    if end >= len(l):
        return l[start:]
    return l[start:end]


class SearchEngine:
    def __init__(self):
        with open(CATALOG, 'r', encoding='utf-8') as f:
            f_lines = f.readlines()
        self.page_rank = [0] * (int(f_lines[-1].split('|')[0]) + 1)
        self.website = [0] * (int(f_lines[-1].split('|')[0]) + 1)
        for line in f_lines:
            ll = line.split('|')
            ll[0] = int(ll[0])
            ll[1] = int(ll[1])
            self.page_rank[ll[0]] = ll[1]
            self.website[ll[0]] = ll[3]
            if self.page_rank[ll[0]] > 1117383:
                self.page_rank[ll[0]] = 0
        gc.collect()
        print("begin to load big data")
        with open(join(DATA_DIR, 'InvertedTableTotal.pickle'), 'rb') as f:
            self.inverted_index = pickle.load(f)
        print("load finished")

    def intersect(self, list1, list2):
        result = []
        j = 0
        n = len(list2)
        for i in list1:
            while j < n and self.page_rank[i] > self.page_rank[list2[j]]:
                j += 1
            if j >= n:
                return result
            if i == list2[j]:
                result.append(i)
        print(list1)
        print(list2)
        print(result)
        return result

    def query(self, s, start=0, end=4, pic_limit=6):
        try:
            # s = str(s, encoding="utf-8")
            search_words = re.findall(r"\w+|[\u4e00-\u9fa5]+", s)
        except BaseException as e:
            print("========1=============\n", e)
            try:
                search_words = re.split("\\s+", search_words)
            except BaseException as e:
                print("========2=============\n",e)
                search_words = ["清华大学"]
        search_words = list(set([x for x in search_words if x in self.inverted_index]))
        if len(search_words) < 1:
            search_words = ["清华大学"]
        if len(search_words) < 2:
            result = trunc_list(self.inverted_index[search_words[0]], start, end)
        else:
            result = self.inverted_index[search_words[0]]
            for i in range(1, len(search_words)):
                result = self.intersect(result, self.inverted_index[search_words[i]])
            result = trunc_list(result, start, end * 3)
        result_json = []
        pic_web = []
        for i in result:
            try:
                with open(basic_info(i), 'r', encoding='utf-8') as f:
                    result_json.append(json.load(f))
            except BaseException as e:
                print("========3=============\n",e)
        j = 0
        for i in range(len(result_json)):
            if s.find(result_json[i]["title"]) >= 0:
                result[i], result[j] = result[j], result[i]
                result_json[i], result_json[j] = result_json[j], result_json[i]
                j += 1
        for i in range(j, len(result_json)):
            for tag in result_json[i]["tag"]:
                if s.find(tag) >= 0:
                    result[i], result[j] = result[j], result[i]
                    result_json[i], result_json[j] = result_json[j], result_json[i]
                    j += 1
                    break
        result = trunc_list(result, start, end)
        result_json = trunc_list(result_json, start, end)
        website_list = [BAIKE + self.website[i] for i in result]
        for i in website_list:
            try:
                text = str(urlopen(i).read(), encoding="utf-8")
                pic_web += re.findall(r'<img\s*src="(.*?jpg)"', text)
                if len(pic_web) >= pic_limit:
                    pic_web = pic_web[:pic_limit]
                    break
            except BaseException as e:
                print("========4=============\n", e)

        return [result_json, website_list, [download_picture(join(IMG_PATH, s), url) for url in pic_web]]


if __name__ == '__main__':
    # print(input("input keyword:"))
    search_engine = SearchEngine()
    print(search_engine.query("清华 紫荆"))
    while True:
        try:
            s = search_engine.query(input("input keyword:"))
            with open(join(DATA_DIR, "example.json"), 'w', encoding='utf-8') as f:
                json.dump(s, f, ensure_ascii=False, indent=2)
            # print(json.dumps(s, indent=2, ensure_ascii=False))
        except BaseException as e:
            print("========5=============\n", e)




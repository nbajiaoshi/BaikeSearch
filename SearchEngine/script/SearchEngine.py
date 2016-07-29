#coding:utf-8
import json
import re

import gc

import pickle
from urllib.request import urlopen

from util import *


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
        print("begain to load big data")
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
        return result

    def query(self, s, start=0, end=4, pic_limit=6):
        try:
            # print(s, type(s))
            s = str(s, encoding="utf-8")
            print(s, type(s))
            s = re.split("\\s+", s)
        except BaseException as e:
            print("========1=============\n",e,s)
            try:
                s = re.split("\\s+", s)
            except BaseException as e:
                print("========2=============\n",e)
                s = ["清华大学"]
        print(s, "before cut")
        s = list(set([x for x in s if x in self.inverted_index]))
        print(s, "after cut")
        if len(s) < 1:
            s = ["清华大学"]
        if len(s) < 2:
            result = trunc_list(self.inverted_index[s[0]], start, end)
        else:
            result = self.inverted_index[s[0]]
            for i in range(1, len(s)):
                result = self.intersect(result, self.inverted_index[s[i]])
            result = trunc_list(result, start, end)
        result_json = []
        pic_web = []
        website_list = [BAIKE + self.website[i] for i in result]
        for i in website_list:
            try:
                text = str(urlopen(i).read(), encoding="utf-8")
                pic_web += re.findall(r'<img\s*src="(.*?jpg)"', text)
                if len(pic_web) >= pic_limit:
                    pic_web = pic_web[:pic_limit]
                    break
            except BaseException as e:
                print(e)
        for i in result:
            try:
                with open(basic_info(i), 'r', encoding='utf-8') as f:
                    result_json.append(json.load(f))
            except BaseException as e:
                print(e)

        return [result_json, website_list, pic_web]


if __name__ == '__main__':
    # text = str(urlopen(BAIKE + '/view/1563.htm').read(), encoding="utf-8")
    # print(re.findall(r'<img\s*src="(.*?jpg)"', text))
    print(["清华", "紫荆", "学生"])
    # # print(raw_input("input keyword:"))
    print(input("input keyword:"))
    search_engine = SearchEngine()
    print(search_engine.query("清华 紫荆 学生".encode("utf-8")))
    while True:
        try:
            print(json.dumps(
                search_engine.query(input("input keyword:").encode("utf-8")), indent=2))
        except BaseException as e:
            print(e)




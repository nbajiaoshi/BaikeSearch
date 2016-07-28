import json
from util import *


def trunc_list(l, start, end):
    if len(l) < start:
        return []
    if end >= len(start):
        return l[start:]
    return l[start:end]


class SearchEngine:
    def __init__(self):
        with open(join(DATA_DIR, 'InvertedTableTotal.json'), 'r', encoding="utf-8") as f:
            self.inverted_index = json.load(f)
        with open(CATALOG, 'r', encoding="utf-8") as f:
            f_lines = f.readlines()
        self.page_rank = [0] * (int(f_lines[-1].split('|')[0]) + 1)
        for line in f_lines:
            self.page_rank[int(line.split('|')[0])] = int(line.split('|')[1])
            if self.page_rank[int(line.split('|')[0])] > 1117383:
                self.page_rank[int(line.split('|')[0])] = 0

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

    def query(self, s, start=0, end=20):
        # s = re.split("\\s+", s)
        s = list(set([x for x in s if x in self.inverted_index]))
        if len(s) < 2:
            result = trunc_list(self.inverted_index[s[0]], start, end)
        else:
            result = self.inverted_index[s[0]]
            for i in range(1, len(s)):
                result = self.intersect(result, self.inverted_index[s[i]])
            result = trunc_list(result, start, end)
        result_json = []
        for i in result:
            with open(basic_info(i), 'r', encoding="utf-8") as f:
                result_json.append(json.load(f))
        return result_json

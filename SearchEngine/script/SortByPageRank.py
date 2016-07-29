import json
import pickle
import re
from os import listdir

from util import *


def sort_catalog_by_page_rank():
    j = 0
    page_rank = {}
    with open(PAGE_RANK_RESULT) as f:
        for line in f:
            page_rank[line.split('\t')[0]] = j
            j += 1
    with open(CATALOG, 'r', encoding="utf-8") as f:
        f_lines = f.readlines()

        with open(CATALOG, 'w', encoding="utf-8") as f:
            try:
                for line in f_lines:
                    ll = line.split(":", maxsplit=1)
                    if len(ll) < 2:
                        continue
                    kk = ll[1].split(',')
                    if len(kk) > 2:
                        kk = [','.join(kk[:-1]), kk[-1]]
                    f.write('|'.join([ll[0], str(page_rank[kk[1][:-1]])] + kk))
            except BaseException as e:
                print(e, ll, kk)
                f.writelines(f_lines)


def sort_inverted_index_result():
    with open(CATALOG, 'r', encoding="utf-8") as f:
        f_lines = f.readlines()
    page_rank = [0] * (int(f_lines[-1].split('|')[0]) + 1)
    for line in f_lines:
        page_rank[int(line.split('|')[0])] = int(line.split('|')[1])
        if page_rank[int(line.split('|')[0])] > 1117383:
            page_rank[int(line.split('|')[0])] = 0
    with open(INVERTED_INDEX_RESULT, 'r', encoding="utf-8") as f:
        f_lines = f.readlines()
    with open(INVERTED_INDEX_RESULT + '2', 'w', encoding="utf-8") as f:
        for line in f_lines:
            ll = line[:-1].split('\t', maxsplit=1)
            if len(ll) < 2:
                continue
            index_list = sorted(ll[1].split(',')[:-1], key=lambda x: page_rank[int(x)], reverse=True)
            f.write(ll[0] + '\t' + ','.join(index_list) + '\n')


def inverted_index():
    with open(CATALOG, 'r') as f:
        f_lines = f.readlines()
    page_rank = [0] * (int(f_lines[-1].split('|')[0]) + 1)
    for line in f_lines:
        page_rank[int(line.split('|')[0])] = int(line.split('|')[1])
        if page_rank[int(line.split('|')[0])] > 1117383:
            page_rank[int(line.split('|')[0])] = 0
    dict_totall = {}
    word_matcher = re.compile('\\w+|[\\u4e00-\\u9fa5]+')
    num_parser = re.compile('\\d+')
    i = 0
    for filename in listdir(join(ROOT_DIR, 'segText')):
        i += 1
        if i % 1000 == 0:
            print(str(i / 300000) + "%")
        with open(join(ROOT_DIR, 'segText', filename), 'r', encoding="utf-8") as f:
            text = f.read()
        words = set(word_matcher.findall(text))
        for word in words:
            if word not in dict_totall:
                dict_totall[word] = [int(num_parser.search(filename).group(0))]
            else:
                dict_totall[word].append(int(num_parser.search(filename).group(0)))
        if i < 2:
            print(dict_totall)
    # dict_partial_2 ={}
    # dict_partial_4 ={}
    # dict_partial_8 ={}
    # dict_partial_16 ={}
    for word in dict_totall:
        dict_totall[word] = sorted(dict_totall[word], key=lambda x: page_rank[x], reverse=True)
        # dict_partial_2[word] = [x for x in dict_totall[word] if page_rank[x] > 1117383 // 2]
        # dict_partial_4[word] = [x for x in dict_partial_2[word] if page_rank[x] > 1117383 - 1117383 // 4]
        # dict_partial_8[word] = [x for x in dict_partial_4[word] if page_rank[x] > 1117383 - 1117383 // 8]
        # dict_partial_16[word] = [x for x in dict_partial_8[word] if page_rank[x] > 1117383 - 1117383 // 16]
    with open(join(DATA_DIR, 'InvertedTableTotal.pickle'), 'wb', encoding="utf-8") as f:
        pickle.dump(dict_totall, f, protocol=1)
    # with open(join(DATA_DIR, 'InvertedTable_partial_2.json'), 'w', encoding="utf-8") as f:
    #     json.dump(dict_partial_2, f)
    # with open(join(DATA_DIR, 'InvertedTable_partial_4.json'), 'w', encoding="utf-8") as f:
    #     json.dump(dict_partial_4, f)
    # with open(join(DATA_DIR, 'InvertedTable_partial_8.json'), 'w', encoding="utf-8") as f:
    #     json.dump(dict_partial_8, f)
    # with open(join(DATA_DIR, 'InvertedTable_partial_16.json'), 'w', encoding="utf-8") as f:
    #     json.dump(dict_partial_16, f)


if __name__ == '__main__':
    inverted_index()
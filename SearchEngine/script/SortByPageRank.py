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


if __name__ == '__main__':
    sort_inverted_index_result()
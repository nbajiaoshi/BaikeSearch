from util import *


def fix_link():
    with open(CATALOG, 'r', encoding="utf-8") as f:
        catalog = f.readlines()
    j = 0
    for i in range(100):
        with open(link_list(i)) as f:
            for line in f:
                if len(line) > 2:
                    catalog[j] = catalog[j].split(',')[0]  + ',' + line.split('\t')[0] + '\n';
                    j += 1
    with open(CATALOG, 'w', encoding="utf-8") as f:
        f.writelines(catalog)


def sort_by_page_rank():
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


if __name__ == '__main__':
    sort_by_page_rank()

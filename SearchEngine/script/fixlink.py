from util import *


def fix_link():
    with open(CATALOG, 'r', encoding="utf-8") as f:
        catalog = f.readlines()
    j = 0
    for i in range(100):
        with open(link_list(i)) as f:
            for line in f:
                if len(line) > 2:
                    catalog[j] = catalog[j].split(',')[0] + ',' + line.split('\t')[0] + '\n';
                    j += 1
    with open(CATALOG, 'w', encoding="utf-8") as f:
        f.writelines(catalog)


if __name__ == '__main__':
    fix_link()

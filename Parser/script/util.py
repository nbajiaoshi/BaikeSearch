from os.path import dirname, join

SCRIPT_DIR = dirname(__file__)
ROOT_DIR = dirname(SCRIPT_DIR)
DATA_DIR = join(ROOT_DIR, 'data')


BAIKE = 'http://baike.baidu.com'

REPLACE_LIST = [
    ['&quot;', '"'],
    ['&nbsp;', ''],
    ['&#91;', '['],
    ['&#93;', ']']
]


def basic_info(n):
    return join(DATA_DIR, "BasicInfo",  "BasicInfo_" + str(n).rjust(10, '0') + '.json')


def link_list(n):
    return join(DATA_DIR, "LinkList",  "LinkList_" + str(n).rjust(10, '0') + '.txt')


def baike_text(n):
    return join(DATA_DIR, "Text", "Text_" + str(n).rjust(10, '0') + '.txt')

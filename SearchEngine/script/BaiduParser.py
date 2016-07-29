import re
from util import *
from urllib.request import urlopen, URLError
from os.path import join
from json import *
from threading import Thread
import time


total = 100000000
deep_list = []
done_list = set([])
load_count = 1
thread_list = []


def parse_info(text, num):
    info_dict = {}

    s = re.search(r'<meta\s?name="description"\s?content="(.*?)">', text)
    if s is None:
        info_dict["description"] = ""
    else:
        info_dict["description"] = s.group(1)

    s = re.search(r'<h1\s?>([^<]*)</h1>', text)
    if s is None:
        info_dict["title"] = ""
    else:
        info_dict["title"] = s.group(1)

    s = re.search(r'<div class="open-tag-title">词条标签：</div>' + '(.*?)' +
                  r'<div class="open-tag-collapse" id="open-tag-collapse"></div>', text, flags=re.M | re.S)
    if s is None:
        info_dict["tag"] = []
    else:
        info_dict["tag"] = re.sub('<a target="_blank" href="/wikitag/taglist\\?tagId=\\d+">(.*)</a>|<.*>|\n',
                                  lambda m: m.group(1), s.group(1)).split("，")

    s = re.findall('<dt class="basicInfo-item name">(.*?)</dt>.*?<dd class="basicInfo-item value">\\s+(.*?)\\s+</dd>',
                   text, flags=re.M | re.S)
    info_dict["basic_info"] = []
    for item in s:
        value = re.sub('<[^>]*class=[^>]*>.*|<(?!/dt|br/).*?>|\\s+', "", item[1], flags=re.M | re.S)
        value = re.split('<.*?>', value, flags=re.M | re.S)
        if len(value) == 1:
            value = value[0]
        info_dict["basic_info"].append([re.sub('<.*>', "", item[0]), value])
    with open(basic_info(num), 'w', encoding="UTF-8") as f:
        dump(info_dict, f, indent=2, ensure_ascii=False)
    return info_dict["title"]


def parse_link_list(postfix, text, num):
    html_list = re.findall('"(/view/[^"]*\.htm)"', text)
    html_list = list(set(html_list))
    global deep_list
    with open(link_list(num // 100), 'a', encoding="utf-8") as f:
        f.write(postfix + '\t1|')
        for i in html_list:
            f.write(i + ',')
            if not (i in deep_list or i in done_list):
                deep_list.append(i)
        f.write('\n')


def parse_text(text, num):
    text = re.sub('<script.*?>.*?</script>|<div class="open-tag-title">.*|'
                  '^.*<div class="lemma-summary" label-module="lemmaSummary">|'
                  '^.*<h1\s?>([^<]*)</h1>|<div id="open-tag">.*',
                  '', text, flags=re.M | re.S)
    text = re.sub('<(?!/dt|br/).*?>', '', text, flags=re.M | re.S)
    text = re.sub('<.*?>', '\n', text)
    text = re.sub('\\n\\n*', '\n', text, flags=re.M | re.S)
    with open(baike_text(num), 'w', encoding="UTF-8") as f:
        f.write(text)


def pick_up(postfix, num):
    text = str(urlopen(BAIKE + postfix).read(), encoding="utf-8")
    for i in REPLACE_LIST:
        text = text.replace(i[0], i[1])
    if re.search('div class="errorBox"', text) is not None:
        print("skip")
        return
    global done_list
    title = parse_info(text, num)
    parse_link_list(postfix, text, num)
    parse_text(text, num)
    with open(CATALOG, 'a', encoding="utf-8") as f:
        f.write(str(num).rjust(10, '0') + ":" + title + "," + postfix + '\n')
    done_list.add(postfix)
    with open(join(DATA_DIR, 'done.txt'), 'a', encoding="utf-8") as f:
        f.write(postfix + '\n')
    print(num, postfix, title.encode('utf-8'), "finished.")


def load_list():
    global done_list
    global deep_list

    with open(join(DATA_DIR, "deep_list.json"), 'r', encoding="utf-8") as f:
        deep_list = load(f)

    with open(join(DATA_DIR, 'done.txt'), 'r', encoding="utf-8") as f:
        for line in f:
            done_list.add(line[:-1])
    return done_list


def update_total():
    global total
    with open(CATALOG, 'r', encoding="utf-8") as f:
        for lines in f:
            total_find = re.match('(\d+?):', lines)
            if total_find:
                total = int(total_find.group(1))


def rest():
    global deep_list
    global load_count
    global thread_list
    thread_list = [t for t in thread_list if t[0].isAlive()]
    print("running thread:", [t[1] for t in thread_list])
    if len(thread_list) > 10:
        time.sleep(4)
    with open(join(DATA_DIR, "deep_list.json"), 'w', encoding="utf-8") as f:
        dump(deep_list[load_count:], f, indent=2)


def parse():
    sleepy = 0
    global done_list
    global deep_list
    global load_count
    global thread_list
    global total
    for i in deep_list:
        print(i)
        if int(re.search('\d+', i).group(0)) % 2 == 0 and not(i in done_list):
            try:
                sleepy += 1
                t = Thread(target=pick_up, args=(i, total + 1, ))
                t.setDaemon(True)
                t.start()
                runtime = 0
                while t.isAlive():
                    if runtime > 50:
                        thread_list.append([t, total])
                        break
                    runtime += 1
                    time.sleep(0.1)
                print("time pass:", runtime / 10)
                total += 1
                if sleepy % 10 == 0:
                    sleepy = 0
                    t = Thread(target=rest())
                    t.setDaemon(True)
                    t.start()
                    print("wating....")
                    time.sleep(4)
                    t.join()
            except URLError as err:
                deep_list.append(i)
                t = Thread(target=rest)
                t.setDaemon(True)
                t.start()
                print(err)
                time.sleep(4)
                t.join()
            except KeyboardInterrupt as err:
                print("\nRelax...Program will finish soon be finished")
                t = Thread(target=time.sleep, args=(1,))
                t.setDaemon(True)
                t.start()
                deep_list.append(i)
                rest()
                t.join()
                break
            except BaseException as err:
                print(err)
        load_count += 1
    print("done")


if __name__ == '__main__':
    load_list()
    update_total()
    parse()

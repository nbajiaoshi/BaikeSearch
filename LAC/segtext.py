#coding=utf-8

import os, time
import thulac

def segText(thu, filename, src_dir, out_dir):
    in_text_name = os.path.join(src_dir, filename)
    out_text_name = os.path.join(out_dir, "seg_" + filename)
    if not os.path.isfile(out_text_name):
        with open(in_text_name, 'r') as f:
            with open(out_text_name, 'w') as g:
                for in_line in f.readlines():
                    if not in_line.split():
                        continue
                    res = []
                    try:
                        res = thu.cut(in_line)
                    except:
                        print "except in cut: ", in_line
                    try:    
                        g.write(" ".join(res))
                    except:
                        print res

    else:
        pass

def main():
    src_dir = "/home/zihao/Text"
    out_dir = "/home/zihao/segText2"

    intput_filename_list = os.listdir(src_dir)
    intput_filename_list = [f for f in intput_filename_list if f.endswith(".txt")]

    thu = thulac.thulac("-seg_only")

    counter = 0
    for name in intput_filename_list:
        segText(thu, name, src_dir, out_dir)
        counter += 1
        if counter % 1000 == 0:
            print("Done {} passages.".format(counter))
            localtime = time.asctime( time.localtime(time.time()))
            print "Time :", localtime, "\n"

    print("All done!!")

if __name__ == "__main__":
    main()
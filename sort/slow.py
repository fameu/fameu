# -*- coding: utf-8 -*-

import sys
import re

RE_COUNT_COST = "\*\*\*Process (?P<class_name>.*?)\.(?P<func_name>.*?) costs (?P<tm>[\d\.]*?)ms\, threshold is (?P<thresholds>.*?)ms"
RE_COUNT_REQUEST = "count_request_costs, method: (?P<file_name>.*?)#(?P<func_name>.*?)\, costs\: (?P<tm>[\d\.].*?)\(ms\)"
RE_COUNT_END = "Counter end at \(\'(?P<file_name>.*?)\'\, (?P<lines>\d+), \'(?P<func_name>.*?)\'\)\, slice costs (?P<tm>[\d\.]*?)ms"


SLOW_LOG_FILE = "slow.log"


def main(file_name):
    slow_count_dict = dict()
    slow_request_dict = dict()
    slow_count_end = dict()
    with open(file_name, "r") as f:
        for line in f.readlines():
            try:
                if line[:3] == "cou":
                    ret = re.match(RE_COUNT_REQUEST, line).groups()
                    try:
                        file_name, func_name, tm = ret
                        key = "{file_name}#{func_name}".format(file_name=file_name, func_name=func_name)
                        lst = slow_request_dict.setdefault(key, [])
                        lst.append(int(float(tm)))
                    except Exception as error:
                        print line, error
                        break
                        continue
                elif line[:3] == "***":
                    ret = re.match(RE_COUNT_COST, line).groups()
                    try:
                        class_name, func_name, tm, _ = ret
                        key = "{file_name}#{func_name}".format(file_name=class_name, func_name=func_name)
                        lst = slow_count_dict.setdefault(key, [])
                        lst.append(int(float(tm)))
                    except Exception as error:
                        print line, error
                        break
                        continue
                elif line[:11] == "Counter end":
                    ret = re.match(RE_COUNT_END, line).groups()
                    try:
                        file_name, _line, func_name, tm = ret
                        key = "{file_name}#{func_name}-{line}".format(file_name=file_name, func_name=func_name, line=_line)
                        lst = slow_count_end.setdefault(key, [])
                        lst.append(int(float(tm)))
                    except Exception as error:
                        print line, error
                        break
                        continue
                else:
                    continue
            except Exception as error:
                print line, error
                break
    
    file_csv_line = "{average:>5}\t{cnt:>5}\t{key:40}\t{value}\n"
    with open(SLOW_LOG_FILE, "w") as f:
        for _dict in [slow_request_dict, slow_count_dict, slow_count_end]:
            _lst = []
            f.write(file_csv_line.format(key="request", cnt="cnt", average="average", value="tms"))
            for key, value in _dict.iteritems():
                _lst.append((key, len(value), sum(value)/len(value), sorted(value, reverse=True)))
            
            for key, cnt, average, value in sorted(_lst, key=lambda x:(x[1],x[2]), reverse=True):
                f.write(file_csv_line.format(key=key, cnt=cnt, average=average, value=value))
        
    

if __name__ == "__main__":
    try:
        file_name = sys.argv[1]
    except:
        print "Usage:\n\t python " + sys.argv[0] + " file_name"
        sys.exit(0)
    main(file_name)

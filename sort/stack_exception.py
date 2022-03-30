# -*- coding: utf-8 -*-

import sys
import re


APP_NAME_LIST = ['pyq_web']

RE_ERROR_STR1 = "\[(?P<app_name>[a-zA-Z_]*?)@\w+?\]Attention\!"
RE_ERROR_STR2 = "\[(?P<error_lvl>\w+?)\]\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\,\d{3}\]\[(?P<PID>\d+):(?P<tm>\d+)\]\[(?P<file_name>\w+?\.py):(?P<line>\d+) (?P<functin_name>\w+)\]"
RE_ERROR_STR3 = r"(?P<func_name>\w+?) raise exception\. e:(?P<except>.*?)\, (?P<error_data>.*?)"

STACK_EXCEPTION_FILE = "stack_exception.log"


def main(file_name):
    with open(file_name, 'r') as f:
        file_content = f.readlines()
        print type(file_content), len(file_content)
        for line in file_content:
            s = re.match(RE_ERROR_STR3, line, re.S)
            if s:                    
                print s.groupdict()
                break
    

if __name__ == "__main__":
    file_name = STACK_EXCEPTION_FILE
    if len(sys.argv)>1:
        file_name = sys.argv[1]
        
    main(file_name)


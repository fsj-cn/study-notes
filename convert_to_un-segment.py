# Usage：python3 ori.py baidu_segment.data
# 将文本还原至，未分词状态；[数字/字母]之间保留空格
# 取输入文件名_或.前缀，相应输出文件名为：baidu_ori.data
# encoding=utf-8
import os
import argparse
import re
parser = argparse.ArgumentParser()
parser.add_argument("file", help='input file return un-segmented')
args = parser.parse_args()
input_file = args.file
file_first_name = re.split('[_.]', input_file)[0]
output_file = file_first_name+'_ori.data'
if output_file in os.listdir('.'):
    raise ValueError('---结果文件已存在！---')


def ori(sent):
    sent_split = sent.split(' ')
    res = ''
    for i, w in enumerate(sent_split):
        if i+1 < len(sent_split) and w.encode('UTF-8').isalnum() and sent_split[i+1].encode('UTF-8').isalnum():
            res += w
            res += ' '
        else:
            res += w
    return res


with open(input_file, 'r') as f1, open(output_file, 'w') as f2:
    f1_line = f1.readline().strip()
    while f1_line:
        f2_line = ori(f1_line).strip()
        f2.write(f2_line+'\n')
        f1_line = f1.readline().strip()

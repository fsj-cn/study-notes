# 统计分词文本的词频，去除全[英文/数字/符号]的词，保留一个长度的符号
# 缺点：无法筛选特殊符号、非英文外语
# encoding=utf-8
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument('file', help="file to make word frequency")
args = parser.parse_args()
file = args.file
out = 'word_freq.tmp'
word_dict = {}
punct = ['#', '@', '&', '$', '·', '+', '-', '×', '—', '_', '=', ':', '：', '.', '。', '%',
         '(', ")", ',', '，', '、', '~', '`', '/', '^', '*']
with open(file, 'r') as f1:
    for line in f1:
        word_lst = line.strip().split(' ')
        for word in word_lst:
            count = 0
            if len(word) > 1:
                for i in word:
                    if i in punct or i.encode('UTF-8').isalnum():
                        count += 1
                if count == len(word):
                    continue
            if word == '' or word.encode('UTF-8').isalnum():
                continue
            if word not in word_dict:
                word_dict[word] = 1
            else:
                word_dict[word] += 1
print('字典完成，写入 word_freq')
with open(out, 'w') as f:
    for key, value in word_dict.items():
        f.write(key+'\t'+str(value)+'\n')
os.system('sort -k2 -n -r word_freq.tmp > word_freq')
os.system('rm word_freq.tmp')

# python3 xx.py in_file count out_file
# 按每行长度排序 & 去除全数字行 & 限制相同句子次数
# bug：按理来说排序后相同行连续，但符号不知为何不是
import argparse
import os
parser = argparse.ArgumentParser()
parser.add_argument("in_file", help="file need sorted by sent length")
parser.add_argument("count", type=int, help="same sent appear counts")
parser.add_argument("out_file", help="output file")
args = parser.parse_args()
input_file = args.in_file
max_counts = args.count
out_file = "sort_sent.tmp"
output_file = args.out_file
with open(input_file, 'r') as file1, open(out_file, 'w') as file2:
    for line1 in file1:
        file2.write(str(len(line1.strip()))+'\t'+line1.strip()+'\n')
os.system('sort -k1 -n sort_sent.tmp | cut -f2- > sort_sent')
os.system('rm sort_sent.tmp')

with open("sort_sent", 'r') as f, open(output_file, 'w') as f2:
    line = f.readline().strip()
    tmp = line
    count = 0
    while line:
        if line.encode('utf-8').isdigit():
            line = f.readline().strip()
            continue
        if line == tmp:
            count += 1
            if count <= max_counts:
                f2.write(line+'\n')
        else:
            f2.write(line+'\n')
            tmp = line
            count = 1
        line = f.readline().strip()
os.system('rm sort_sent')
print('结果文件'+output_file+',相同句子限制出现'+str(max_counts)+'次')

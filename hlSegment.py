# 海量中文分词
# 对英文、符号处理不太好
# encoding=utf-8
import jpype
import os
import argparse
import re

parser = argparse.ArgumentParser()
parser.add_argument("file", help='input file to segment')
args = parser.parse_args()
input_file = args.file
file_first_name = re.split('[_.]', input_file)[0]
output_file = file_first_name+'_hlSeg.out'
if output_file in os.listdir('.'):
    raise ValueError('---结果文件已存在！---')
user_dict = 'ctb_single_freq.dict'


if __name__ == "__main__":
    # 打开jvm虚拟机
    jar_path = os.path.abspath('lib')
    jvmPath = jpype.getDefaultJVMPath()
    jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % (jar_path + '/hlSegment-5.1.11.jar'), "-Djava.ext.dirs=%s" % jar_path)

    # 取得类定义
    BasicSegmentor = jpype.JClass('com.hylanda.segmentor.BasicSegmentor')
    SegOption = jpype.JClass('com.hylanda.segmentor.common.SegOption')
    SegResult = jpype.JClass('com.hylanda.segmentor.common.SegResult')
    # SegGrain = jpype.JClass('com.hylanda.segmentor.common.SegOption$SegGrain')
    # 创建分词对象
    segmentor = BasicSegmentor()

    # 加载词典
    if not segmentor.loadDictionary("./dictionary/CoreDict.dat", user_dict):
        print("字典加载失败！")
        exit()

    # 创建SegOption对象，如果使用默认的分词选项，也可以直接传空
    option = SegOption()
    # 小颗粒，切分人名、词组
    # option.grainSize = SegGrain.SMALL
    option.mergeNumeralAndQuantity = False

    # 读取ni，分词，结果写入xx_hlSeg.out
    with open(input_file, 'r') as fi, open(output_file, 'w+') as fo:
        print('生成结果文件：', output_file)
        print('开始写入......')
        x = 5
        sents = [line.strip() for line in fi]
        length = len(sents)
        for i, s in enumerate(sents):
            segResult = segmentor.segment(s, option)
            # 遍历分词结果,写入xx_hlSeg.out
            word = segResult.getFirst()
            res = ""
            while word:
                w = word.wordStr
                if w != ' ':
                    if len(w) > 1 and w[-1] == '.' and w[:-1].isalnum():
                        cur = w[:-1]
                        res += cur
                        res += ' . '
                    else:
                        res += w + ' '
                word = word.next
            fo.write(res.strip()+'\n')
            if i > length * x / 100:
                print('已完成', x, '%')
                x += 5
    print(output_file, '写入完毕')
    jpype.shutdownJVM()
    exit()

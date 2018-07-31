# python3 compare.py file1 file2
# 输出两个文件: 相当于两个文本去除cross的数据
# encoding=utf-8
import argparse
import re
import os
parser = argparse.ArgumentParser()
parser.add_argument("file1")
parser.add_argument("file2")
args = parser.parse_args()
file1 = args.file1
file2 = args.file2
file1_name = os.path.basename(file1)
file2_name = os.path.basename(file2)
file1_first_name = re.split('[_.]', file1_name)[0]
file2_first_name = re.split('[_.]', file2_name)[0]
output_file1 = file1_first_name+'_train_noCross.data'
output_file2 = file2_first_name+'_train_noCross.data'


class SpanMetric:

    def __init__(self):
        self.sentence_num = 0
        self.complete_num, self.no_cross_num = 0, 0
        self.seg_tp, self.seg_fp, self.seg_fn = 0., 0., 0.

    def register(self, file1_sent, file2_sent):
        file1_bracket = self.construct_pos_brackets_from_sent(file1_sent)
        file2_bracket = self.construct_pos_brackets_from_sent(file2_sent)
        file1_seg_bracket = set(file1_bracket)
        file2_seg_bracket = set(file2_bracket)
        self.seg_tp += len(file1_seg_bracket & file2_seg_bracket)
        self.seg_fp += len(file2_seg_bracket - file1_seg_bracket)
        self.seg_fn += len(file1_seg_bracket - file2_seg_bracket)
        self.sentence_num += 1

        if file1_seg_bracket == file2_seg_bracket:
            self.complete_num += 1
            self.no_cross_num += 1
            f1.write(file1_sent + '\n')
            f2.write(file2_sent + '\n')
        elif self.no_cross(file1_bracket, file2_bracket):
            self.no_cross_num += 1
            f1.write(file1_sent + '\n')
            f2.write(file2_sent + '\n')
        else:
            pass

    @staticmethod
    def construct_pos_brackets_from_sent(sent):
        s = sent.split()
        ret = []
        left = 0
        for w in s:
            ret.append((left, left+len(w)))
            left += len(w)
        return ret

    @staticmethod
    def no_cross(a, b):
        i = 0
        j = 0
        while (i < len(a)) and (j < len(b)):
            if a[i][1] == b[j][1]:
                i += 1
                j += 1
                continue
            while a[i][1] > b[j][1]:
                if j < len(b) - 1:
                    j += 1
                if b[j][1] > a[i][1]:
                    return False
            while a[i][1] < b[j][1]:
                if i < len(a) - 1:
                    i += 1
                if a[i][1] > b[j][1]:
                    return False
        return True

    def __str__(self):
        if self.seg_tp:
            seg_p = self.seg_tp / (self.seg_tp + self.seg_fp) * 100
            seg_r = self.seg_tp / (self.seg_tp + self.seg_fn) * 100
            seg_f = 2 * seg_p * seg_r / (seg_p + seg_r)
        else:
            seg_p, seg_r, seg_f = 0., 0., 0.
        no_cross_sent = self.no_cross_num / self.sentence_num * 100
        seg_prf = 'agree / no_cross / total_sent =  %s / %s / %s' \
            % (self.complete_num, self.no_cross_num, self.sentence_num)
        seg_prf += '\nno_cross_sent : P : R : F = {:.2f} : {:.2f} : {:.2f} : {:.2f}' \
            .format(no_cross_sent, seg_p, seg_r, seg_f)
        return seg_prf


with open(file1, 'r') as f:
    file1_content = [line.strip() for line in f]
with open(file2, 'r') as f:
    file2_content = [line.strip() for line in f]
metrics = SpanMetric()
assert(len(file1_content) == len(file2_content)), '句子数量不一致'
with open(output_file1, 'w') as f1, open(output_file2, 'w') as f2:
    for n in range(len(file1_content)):
        metrics.register(file1_content[n], file2_content[n])
print('\n', metrics)

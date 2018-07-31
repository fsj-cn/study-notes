# encoding=utf-8
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("test_file", help='test file')
parser.add_argument("gold_file", help='gold file')
args = parser.parse_args()
tf = args.test_file
gf = args.gold_file


class SpanMetric:

    def __init__(self):
        self.sentence_num = 0
        self.complete_num, self.no_cross_num = 0, 0
        self.seg_tp, self.seg_fp, self.seg_fn = 0., 0., 0.

    def register(self, gold, sys):
        gold_bracket = self.construct_pos_brackets_from_sent(gold)
        sys_bracket = self.construct_pos_brackets_from_sent(sys)
        gold_seg_bracket = set(gold_bracket)
        sys_seg_bracket = set(sys_bracket)
        self.seg_tp += len(gold_seg_bracket & sys_seg_bracket)
        self.seg_fp += len(sys_seg_bracket - gold_seg_bracket)
        self.seg_fn += len(gold_seg_bracket - sys_seg_bracket)
        self.sentence_num += 1

        if gold_seg_bracket == sys_seg_bracket:
            self.complete_num += 1
            self.no_cross_num += 1
            f_agree.write(gold + '\n')
        elif self.no_cross(gold_bracket, sys_bracket):
            self.no_cross_num += 1
            f_noCross.write("%s \n%s\n" % (sys, gold))
        else:
            f_cross.write("%s \n%s\n" % (sys, gold))

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
        seg_prf += '\nno_cross_Sent : P : R : F = {:.2f} : {:.2f} : {:.2f} : {:.2f}' \
            .format(no_cross_sent, seg_p, seg_r, seg_f)
        return seg_prf


with open(tf, 'r') as f:
    model_content = [line.strip() for line in f]
with open(gf, 'r') as f:
    gold_content = [line.strip() for line in f]
metrics = SpanMetric()
assert(len(gold_content) == len(model_content)), '句子数量不一致'
with open('agree.data', 'w') as f_agree, open('diff_noCross.data', 'w') as f_noCross, open('cross.data', 'w') as f_cross:
    for n in range(len(model_content)):
        metrics.register(gold_content[n], model_content[n])
print('\n', metrics)

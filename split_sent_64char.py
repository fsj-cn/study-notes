# 切分长段落文本为短句子
# encoding=utf-8
import re
pattern = re.compile(r'\s+')
split = ['。', '！', '？']


def split_sent_limit(sent, limit):
    if len(sent) > limit:
        start = 1
        end = start + 63
        res = []
        find = False
        while True:
            for i, c in enumerate(sent[end:start-1:-1]):
                if c in split:
                    find = True
                    pos = end - i
                    res += [sent[start:pos + 1]]
                    start = pos + 1
                    end = start + limit
                    break
                else:
                    find = False
            if not find:
                if end + limit > len(sent)-1:
                    res += [sent[start:]]
                    break
                else:
                    end += limit
                continue
            if end > len(sent)-1:
                    res += [sent[start:]]
                    break
        res[0] = sent[0]+res[0]
        return res
    return [sent]


with open('../baidu_segmented_data/segments', 'r') as a, open('baidu_segment.data', 'w') as b:
    for line in a:
        result = split_sent_limit(line.strip(), 64)
        for i in range(len(result)):
            if len(result[i]) > 1:
                temp = re.sub(pattern, ' ', result[i])
                b.write(temp.strip().replace(u'\u3000', u'') + '\n')

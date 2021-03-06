from lib.sentence_similarity import SentenceSimilarity
import lib.mecab_util as mecab_util
from lib.clustering import Analyzer
import functools
import math


class DocSubmodular(object):

    def __init__(self, texts, params):
        self.gumma = params['gumma']
        self.texts = texts
        self.len = len(self.texts)
        self.v_vec = [1] * self.len
        self.memo = [[-1 for i in range(self.len)] for j in range(self.len)]
        self.labels = self._make_labels()

    # fdoc
    def calculate(self, s):
        _lambda = 4
        return self.relevance(s) + _lambda * self.redundancy(s)

    def cost(self, i):
        return 10

    def cost_sum(self, s):
        if len(s) == 0:
            return 0
        sum = functools.reduce(lambda x, y: x + self.cost(y), s, 0)
        print(s)
        print(sum)
        return sum

    # private

    def _make_labels(self):
        analyzer = Analyzer(self.texts)
        clusters = analyzer.make_cluster()
        labels = [-1] * len(self.texts)
        for (idx, text) in enumerate(self.texts):
            for (label, cluster) in enumerate(clusters):
                if text in cluster:
                    labels[idx] = label
        return labels

    def label_num(self, idx):
        return self.labels[idx]

    def s_vec_gen(self, s):
        z = [0] * self.len
        for i in s:
            z[i] = 1
        return z

    # L(S) relevance
    def relevance(self, s):
        s_vec = self.s_vec_gen(s)
        acc = 0
        for i in range(self.len):
            s_r = self.cover(i, s_vec)
            v_r = self.gumma * self.cover(i, self.v_vec)
            result = min(s_r, v_r)
            acc += result
        return acc

    # R(S) redundancy
    def redundancy(self, s):
        labels = list(map(lambda x: self.labels[x], s))
        print(labels)
        m = max(labels)
        acc = 0
        for i in range(m):
            acc += math.sqrt(labels.count(i))
        return acc

    # C(S)
    def cover(self, sentence_num, set_vec):
        sentence = self.texts[sentence_num]
        acc = 0
        for (idx, elem) in enumerate(set_vec):
            if elem == 0:
                continue
            if self.memo[sentence_num][idx] < 0:
                ss = SentenceSimilarity(
                    mecab_util.extractNoun(sentence),
                    mecab_util.extractNoun(self.texts[idx]))
                r = ss.distance()
                self.memo[sentence_num][idx] = r
                self.memo[idx][sentence_num] = r
            acc += self.memo[sentence_num][idx]
        return acc


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    file = open(filename).read()
    texts = open(filename).readlines()

    d = DocSubmodular(texts, {'gumma': 0.3})
    r = d.calculate([1, 2, 3])
    print(r)

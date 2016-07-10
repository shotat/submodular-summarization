from lib.sentence_similarity import SentenceSimilarity
import lib.mecab_util as mecab_util
from lib.clustering import Analyzer
import functools

class DocSubmodular(object):

    def __init__(self, texts, params):
        self._gumma = params['gumma']
        self._texts = texts
        self.len = len(self._texts)
        self._v_vec = [1] * self.len
        self._memo = [[-1 for i in range(self.len)] for j in range(self.len)]
        self._labels = self.cluster_labels()

    # fdoc
    def calculate(self, s):
        _lambda = 0.2
        return self.relevance(s) + _lambda * self.redundancy(s)

    def cost(self, i):
        return 10

    def cost_sum(self, s):
        if len(s) == 0:
            return 0
        return functools.reduce(lambda x, y: x + self.cost(y), s)

    def cluster_labels(self):
        analyzer = Analyzer(self._texts)
        clusters = analyzer.make_cluster()
        labels = [-1] * len(self._texts)
        for (idx, text) in enumerate(self._texts):
            for (label, cluster) in enumerate(clusters):
                if text in cluster:
                    labels[idx] = label
        print(labels)
        return labels

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
            v_r = self._gumma * self.cover(i, self._v_vec)
            result = min(s_r, v_r)
            acc += result
        return acc

    # R(S) redundancy
    def redundancy(self, s):
        return 0

    # C(S)
    def cover(self, sentence_num, set_vec):
        sentence = self._texts[sentence_num]
        acc = 0
        for (idx, elem) in enumerate(set_vec):
            if elem == 0:
                continue
            if self._memo[sentence_num][idx] < 0:
                ss = SentenceSimilarity(
                        mecab_util.extractNoun(sentence),
                        mecab_util.extractNoun(self._texts[idx]))
                r = ss.distance()
                self._memo[sentence_num][idx] = r
                self._memo[idx][sentence_num] = r
            acc += self._memo[sentence_num][idx]
        return acc


if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    file = open(filename).read()
    texts = open(filename).readlines()

    d = DocSubmodular(texts, { 'gumma': 0.3 })
    r = d.calculate([1,2,3,4,5,6])
    print(r)

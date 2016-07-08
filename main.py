from lib.doc_submodular import DocSubmodular
import sys

class Main(object):
    def greedy_search(k, texts):
        params = { 'gumma' : 0.5 }
        doc_submodular = DocSubmodular(texts, params);
        # step 0
        s = []
        s_ = []
        # step 1
        while k > doc_submodular.cost_sum(s):
            # step  2
            s_ = s
            # step 3
            tmp_max = 0
            idx_max = -1
            for i in range(doc_submodular.len):
                if i in s:
                    continue
                tmp = doc_submodular.calculate(s + [i]) / doc_submodular.cost(i)
                if tmp > tmp_max:
                    tmp_max = tmp
                    idx_max = i
            print(tmp_max, texts[idx_max])
            s.append(idx_max)
        return s_

if __name__ == '__main__':
    filename = 'recruit.txt' # sys.argv[1]
    texts = open(filename).readlines()

    result = Main.greedy_search(140, texts)
    for idx in result:
        print(texts[idx])



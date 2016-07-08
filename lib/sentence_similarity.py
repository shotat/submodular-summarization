# -*- coding: utf-8 -*-
from scipy.spatial.distance import cosine
import unittest


class SentenceSimilarity(object):

    def __init__(self):
        self._A = None
        self._B = None

    def __init__(self, a, b):
        self._A = a
        self._B = b

    @property
    def A(self):
        return self._A

    @property
    def B(self):
        return self._B

    @A.setter
    def A(self, v):
        self._A = [i for i in v.replace(' ', ',').split(',') if len(i) > 0]

    @B.setter
    def B(self, v):
        self._B = [i for i in v.replace(' ', ',').split(',') if len(i) > 0]

    def distance(self):

        if self._A is None or self._B is None:
            return 0

        if len(self._A) < 2 or len(self._B) < 2:
            return 0

        return self._distance()

    def _distance(self):

        _words = []
        _words.extend(self._A)
        _words.extend(self._B)

        _words = list(set(_words))
        _words.sort()

        _listA = [self._A.count(_w) for _w in _words]
        _listB = [self._B.count(_w) for _w in _words]

        try:
            return 1 - cosine(_listA, _listB)
        except:
            return False


class TestSentenceSimilarity(unittest.TestCase):

    def setUp(self):
        pass

    def test_0(self):

        _sentence = SentenceSimilarity()
        _sentence.A = '今期 業績 予想 未定 期限切れ 肉 問題 販売減'
        _sentence.B = '都市 対抗 野球 西濃運輸 初優勝 佐伯 富士 重工'
        self.assertEqual(_sentence.distance(), 0.0)


    def test_1(self):

        _sentence = SentenceSimilarity()
        _sentence.A = '今期 業績 予想 未定 期限切れ 肉 問題 販売減'

        self.assertEqual(_sentence.distance(), False)

    def test_2(self):

        _sentence = SentenceSimilarity()
        _sentence.A = '今期'
        _sentence.B = '都市'

        self.assertEqual(_sentence.distance(), False)

    def test_3(self):

        _sentence = SentenceSimilarity()
        _sentence.A = '今期,業績,予想,未定'
        _sentence.B = '都市,業績,予想,未定'

        _sentence.B = '業績 対抗 野球 西濃運輸 初優勝'

        self.assertGreater(_sentence.distance(), 0.0)

if __name__ == '__main__':
    unittest.main()

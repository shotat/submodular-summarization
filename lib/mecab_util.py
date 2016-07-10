# -*- coding: utf-8 -*-
import MeCab


def extractNoun(text):
    """
       @input: sentence
       @return: a list of noun words
    """
    MecabMode = '-Ochasen'
    tagger = MeCab.Tagger(MecabMode)
    tagger.parse('')  # これ重要！！！！

    node = tagger.parseToNode(text)
    keywords = []
    while node:
        surface = node.surface
        meta = node.feature.split(",")
        if meta[0] == '名詞':
            keywords.append(node.surface)
        node = node.next
    return keywords
if __name__ == '__main__':
    import sys
    filename = sys.argv[1]
    file = open(filename).read()
    print(open(filename).readlines())
    feature_words = extractNoun(file)
    for x in feature_words:
        pass
        # print(x)

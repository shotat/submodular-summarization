#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import codecs
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer

import lib.mecab_util as mecab_util

class Analyzer:
    def __init__(self, texts):
        self.texts = texts
        self.num_clusters = 5
        self.max_df = 0.8
        self.max_features = 100
        self.minibatch = False

    def make_cluster(self):
        texts = self.texts
        print("texts are %(texts)s" %locals() )

        vectorizer = TfidfVectorizer(
            analyzer=mecab_util.extractNoun,
            max_df=self.max_df,
            max_features=self.max_features
            )
        X = vectorizer.fit_transform(texts)
        print("X values are %(X)s" %locals() )

        if self.minibatch:
            km = MiniBatchKMeans(
                n_clusters=self.num_clusters,
                init='k-means++', batch_size=1000,
                n_init=10, max_no_improvement=10,
                verbose=True
                )
        else:
            km = KMeans(
                n_clusters=self.num_clusters,
                init='k-means++',
                n_init=10,
                verbose=True
                )
        km.fit(X)
        labels = km.labels_

        transformed = km.transform(X)
        dists = np.zeros(labels.shape)
        for i in range(len(labels)):
            dists[i] = transformed[i, labels[i]]

        clusters = []
        for i in range(self.num_clusters):
            cluster = []
            ii = np.where(labels==i)[0]
            dd = dists[ii]
            di = np.vstack([dd,ii]).transpose().tolist()
            di.sort()
            for d, j in di:
                cluster.append(texts[int(j)])
            clusters.append(cluster)
        return clusters

if __name__ == '__main__':
    if sys.version_info > (3,0):
        analyzer = Analyzer(texts)
        clusters = analyzer.make_cluster()

    else:
        print("This program require python > 3.0")

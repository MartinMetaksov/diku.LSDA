import unittest
from itertools import combinations
from unittest import TestCase

import numpy
import time

# KOS blog entries (orig source: dailykos.com) D = 3430; W = 6906; N = 467714
TEST_FILENAME = "docword.kos.txt"


def jaccard_similarity(a, b):
    if isinstance(a, set):
        c = a.intersection(b)
    else:
        c = set(a).intersection(b)
    return float(len(c)) / (len(a) + len(b) - len(c))


def jaccard_distance(a, b):
    return 1 - jaccard_similarity(a, b)


class Tests(TestCase):
    def tic(self, task_name):
        self.task_name = task_name
        self.timer = time.time()

    def tac(self):
        print("Running time for " + self.task_name + ": " + str(time.time() - self.timer) + "s")

    def setUp(self):
        self.tic("loading data")
        print("Loading data...")
        # Data structure: docID | wordID | count
        self.data = numpy.loadtxt("hw2/data/" + TEST_FILENAME, skiprows=3)
        print("Data was successfully loaded")
        self.tac()

    def get_shingles(self):
        all_shingles = []
        shingles_doc = set()
        for line in range(0, len(self.data)):
            shingles_doc.add(self.data[line, 1])
            if self.data[line, 0] != self.data[line - 1, 0] and line > 1:
                all_shingles.append(shingles_doc)
                shingles_doc = set()
            if line == (len(self.data) - 1):
                all_shingles.append(shingles_doc)
        return all_shingles

    @unittest.SkipTest
    def test_ex1p1(self):
        print("Obtaining shingles...")
        self.tic("obtaining shingles")
        shingles = self.get_shingles()
        self.tac()
        print("Successfully obtained shingles")
        print("Comparing jaccard similarities...")
        self.tic("computing jaccard similarities")
        js = []
        for u, v in combinations(shingles, 2):
            js.append(jaccard_similarity(u, v))
        self.tac()
        print("Successfully computed jaccard similarities")
        print("Jaccard similarity average: " + str(sum(js) / float(len(js))))
        print("Writing jaccard similarities to file...")
        out = open("ex1p1out.txt", "w")

        out.write(str("\n".join(map(lambda n: '%.15f' % n, js))))
        out.close()
        print("Finished writing jaccard similarities to file")

    # @unittest.SkipTest
    def test_ex1p2(self):
        K = 100
        print("Computing MinHash signatures...")
        self.tic("computing MinHash signatures")
        # todo: implement
        self.tac()
        print("Finished computing MinHash signatures")

    @unittest.SkipTest
    def test_ex1p3(self):
        pass

    @unittest.SkipTest
    def test_ex1p4(self):
        pass

    @unittest.SkipTest
    def test_ex1p5(self):
        pass

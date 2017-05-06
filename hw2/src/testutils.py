from unittest import TestCase

import numpy as np

from hw2.utils import pairwise_jaccard


class TestUtils(TestCase):
    # "the quick brown fox jumps over the lazy dog"
    #   s1   s2    s3   s4   s5   s6   s7  s8   s9
    def test_jaccard_distance(self):
        # documents = ["the quick brown fox", "brown fox jumps over", "over the lazy dog", "lazy dog the quick"]
        documents = np.array([
            [1, 1, 1, 1, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 0, 1, 1, 1, 1],
            [1, 1, 0, 1, 0, 0, 0, 1, 1]
        ]).T


        js = 1 - pairwise_jaccard_(documents)
        print("")

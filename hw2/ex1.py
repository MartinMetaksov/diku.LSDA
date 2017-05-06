import random
from itertools import combinations

import numpy as np
import time

# KOS blog entries (orig source: dailykos.com) D = 3430; W = 6906; N = 467714
from hw2.config import basedir

DOCWORDS = "docword.kos.txt"
WORDS = "vocab.kos.txt"


class Ex1:
    def pairwise_jaccard(self, X):
        """
        Computes the Jaccard distance between the rows in X.
        Returns a matrix containing the jaccard distance
        """
        self.tic("computing pairwise jaccard similarities")
        X = X.astype(bool).astype(int)
        # interested in documents relation to each other and not the shingles
        intersect = X.T.dot(X)
        row_sums = intersect.diagonal()
        unions = row_sums[:, None] + row_sums - intersect
        dist = 1.0 - intersect / unions
        self.tac()
        return dist

    @staticmethod
    def pairwise_jaccard_diff(X):
        return 1.0 - Ex1.pairwise_jaccard(X)

    @staticmethod
    def find_next_prime(n):
        return Ex1.find_prime_in_range(n, 2 * n)

    @staticmethod
    def find_prime_in_range(a, b):
        for p in range(a, b):
            for i in range(2, p):
                if p % i == 0:
                    break
            else:
                return p
        return None

    def tic(self, task_name):
        print("Starting task: " + task_name + " ...")
        self.task_name = task_name
        self.timer = time.time()

    def tac(self):
        print("Running time for " + self.task_name + ": " + str(time.time() - self.timer) + "s")
        print("Finished task: " + self.task_name + "\n")

    def __init__(self):
        self.task_name = ""
        self.timer = time.time()
        self.tic("loading data")
        # Data structure: docID | wordID | count
        self.D = 3430
        self.W = 6906
        self.N = 467714
        self.data = np.loadtxt(basedir + "/data/" + DOCWORDS, skiprows=3, dtype=int)
        self.tac()
        self.tic("obtaining binary matrix")
        self.binary_matrix = self.get_binary_matrix()
        self.tac()

    def get_binary_matrix(self):
        bin_mat = np.zeros([self.W, self.D])
        for line in self.data:
            bin_mat[line[1] - 1, line[0] - 1] = 1
        return bin_mat

    def jaccard_similarities(self, out_file):
        self.pairwise_jaccard(self.binary_matrix)
        self.tic("writing jaccard similarities to file")
        out = open(out_file, "w")
        out.write(str("\n".join(map(lambda n: '%.15f' % n, js))))
        out.close()
        self.tac()

    '''
    To generate the K random hash functions, we have been inspired by another project, which we have found on GitHub:
    https://github.com/chrisjmccormick/MinHash
    '''
    def k_signatures(self, k):
        print("Finding the highest shingle value: " + str())
        highest_shingles = []
        for shingle in self.shingles:
            highest_shingles.append(max(shingle))
        highest_shingle = max(highest_shingles)
        print("Highest val: " + str(highest_shingle))
        next_prime = self.find_next_prime(int(np.ceil(highest_shingle)))
        print("Next prime: " + str(next_prime))

        # We will generate K random hash function with the form h(x) = (a*x + b) % c
        # where a and b are random coefficients and c is a prime number > highest_shingle.

        def get_rand_coefficients(K):
            rand_list = []
            # ensure a unique index is given
            while K > 0:
                rand_index = random.randint(0, highest_shingle)
                while rand_index in rand_list:
                    rand_index = random.randint(0, highest_shingle)
                rand_list.append(rand_index)
                K = K - 1
            return rand_list

        # 100 different coefficients for a and 100 more for b
        a = get_rand_coefficients(k)
        b = get_rand_coefficients(k)

        self.tic("computing MinHash signatures with k=" + str(k))
        # documents by signatures matrix
        signatures = []

        for shingle in self.shingles:
            signature = []
            for i in range(0, k):
                min_hash_code = next_prime + 1
                for token in shingle:
                    hash_code = (a[i] * token + b[i]) % next_prime
                    # update the min hash code.
                    if hash_code < min_hash_code:
                        min_hash_code = hash_code
                signature.append(min_hash_code)
            signatures.append(signature)

        self.tac()
        return signatures

    def ex1p3(self):
        pass

    def ex1p4(self):
        pass

    def ex1p5(self):
        pass


ex = Ex1()
# Task 1
ex.jaccard_similarities(out_file="out11.txt")
# Task 2
# ex.k_signatures(k=100)
ex.ex1p3()
ex.ex1p4()
ex.ex1p5()

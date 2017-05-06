import random
from itertools import combinations

import numpy
import time

# KOS blog entries (orig source: dailykos.com) D = 3430; W = 6906; N = 467714
from hw2.config import basedir

TEST_FILENAME = "docword.kos.txt"


class Ex1:
    @staticmethod
    def jaccard_similarity(a, b):
        if isinstance(a, set):
            c = a.intersection(b)
        else:
            c = set(a).intersection(b)
        return float(len(c)) / (len(a) + len(b) - len(c))

    @staticmethod
    def jaccard_distance(a, b):
        return 1 - Ex1.jaccard_similarity(a, b)

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
        print("Running time for " + self.task_name + ": " + str(time.time() - self.timer) + "s\n")
        print("Finished task: " + self.task_name)

    def __init__(self):
        self.task_name = ""
        self.timer = time.time()
        self.tic("loading data")
        # Data structure: docID | wordID | count
        self.data = numpy.loadtxt(basedir + "/data/" + TEST_FILENAME, skiprows=3)
        self.tac()
        self.tic("obtaining shingles")
        self.shingles = self.get_shingles()
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

    def jaccard_similarities(self, collection, c_name, filename="out.txt"):
        self.tic("computing jaccard similarities for " + c_name)
        js = []
        for u, v in combinations(collection, 2):
            js.append(Ex1.jaccard_similarity(u, v))
        self.tac()
        print("Jaccard similarity average: " + str(sum(js) / float(len(js))))
        self.tic("writing jaccard similarities to file")
        out = open(filename, "w")
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
        next_prime = self.find_next_prime(int(numpy.ceil(highest_shingle)))
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
                smallest_hash_code = next_prime + 1
                for token in shingle:
                    hash_code = (a[i] * token + b[i]) % next_prime
                    # update the min hash code.
                    if hash_code < smallest_hash_code:
                        smallest_hash_code = hash_code
                signature.append(smallest_hash_code)
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
# ex.jaccard_similarities(collection=ex.shingles, c_name="shingles", filename="output11.txt")
# Task 2
# ex.k_signatures(k=100)
ex.ex1p3()
ex.ex1p4()
ex.ex1p5()

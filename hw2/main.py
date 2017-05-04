import scipy
from scipy import sparse

from hw2.utils import load_data

DOCWORD_KOS = "data/docword.kos.txt"
VOCAB_KOS = "data/vocab.kos.txt"

data = load_data(DOCWORD_KOS)
x = sparse.spmatrix(data)
print ""

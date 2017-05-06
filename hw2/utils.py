# Not actually necessary for sparse matrices, but it is for
# dense matrices and ndarrays, if X.dtype is integer.
from __future__ import division
from scipy.sparse import csr_matrix, np


def pairwise_jaccard(X):
    """Computes the Jaccard distance between the rows of `X`.
    """
    X = X.astype(bool).astype(int)

    intersect = (X.T).dot(X)
    row_sums = intersect.diagonal()
    unions = row_sums[:, None] + row_sums - intersect
    dist = 1.0 - intersect / unions
    return dist


def pairwise_jaccard_sparse(csr, epsilon):
    """Computes the Jaccard distance between the rows of `csr`,
    smaller than the cut-off distance `epsilon`.
    """
    assert (0 < epsilon < 1)
    csr = csr_matrix(csr).astype(bool).astype(int)

    csr_rownnz = csr.getnnz(axis=1)
    intersect = csr.dot(csr.T)

    nnz_i = np.repeat(csr_rownnz, intersect.getnnz(axis=1))
    unions = nnz_i + csr_rownnz[intersect.indices] - intersect.data
    dists = 1.0 - intersect.data / unions

    mask = (dists > 0) & (dists <= epsilon)
    data = dists[mask]
    indices = intersect.indices[mask]

    rownnz = np.add.reduceat(mask, intersect.indptr[:-1])
    indptr = np.r_[0, np.cumsum(rownnz)]

    out = csr_matrix((data, indices, indptr), intersect.shape)
    return out

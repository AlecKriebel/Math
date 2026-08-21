"""S3-irrep audit of the repeated-replica compression of the M_Q kernel."""

from itertools import product

import numpy as np


def irreps():
    # Generators a=(12), b=(13).  A real standard representation uses
    # reflections whose axes differ by 60 degrees.
    triv = (np.ones((1, 1)), np.ones((1, 1)))
    sign = (-np.ones((1, 1)), -np.ones((1, 1)))
    a = np.array([[1.0, 0.0], [0.0, -1.0]])
    b = np.array([[-0.5, np.sqrt(3) / 2],
                  [np.sqrt(3) / 2, 0.5]])
    std = (a, b)
    return {"t": triv, "s": sign, "v": std}


def kron_all(xs):
    out = np.ones((1, 1))
    for x in xs:
        out = np.kron(out, x)
    return out


def main():
    reps = irreps()
    worst = (1e9, None, None)
    # K has no sign irrep because dim K=2.
    for labels in product(("t", "v"), ("t", "s", "v"),
                          ("t", "s", "v"), ("t", "s", "v")):
        mats = [reps[x] for x in labels]
        f12 = [x[0] for x in mats]
        f13 = [x[1] for x in mats]
        eye = [np.eye(x.shape[0]) for x in f12]
        g = kron_all([f12[0]] + [2 * eye[i] - f12[i]
                                 for i in range(1, 4)])
        global13 = kron_all(f13)
        proj = (np.eye(global13.shape[0]) + global13) / 2
        compressed = proj @ g @ proj
        # Ignore the orthogonal kernel of proj.
        pvals, pvecs = np.linalg.eigh(proj)
        ran = pvecs[:, pvals > 0.5]
        if ran.shape[1] == 0:
            continue
        small = ran.conj().T @ compressed @ ran
        vals = np.linalg.eigvalsh(small)
        if vals[0] < worst[0]:
            worst = (vals[0], labels, vals)
    print("worst", worst)


if __name__ == "__main__":
    main()

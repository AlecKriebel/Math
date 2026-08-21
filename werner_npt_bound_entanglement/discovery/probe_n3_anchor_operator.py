"""Eigenvalue probe for the universal-inversion anchored operator M_A."""

import numpy as np


def trace_replace(x: np.ndarray, dims: tuple[int, ...], site: int):
    n = len(dims)
    a = x.reshape(dims + dims)
    red = np.trace(a, axis1=site, axis2=site + n)
    # Insert I on site, with tensor order restored.
    eye = np.eye(dims[site])
    y = np.tensordot(eye, red, axes=0)
    # y axes: row_site,col_site, rows_except,cols_except
    rest = [i for i in range(n) if i != site]
    row_pos = {site: 0}
    col_pos = {site: 1}
    for k, j in enumerate(rest):
        row_pos[j] = 2 + k
        col_pos[j] = 2 + len(rest) + k
    perm = [row_pos[j] for j in range(n)] + [col_pos[j] for j in range(n)]
    return y.transpose(perm).reshape(x.shape)


def reduction(x, dims, site):
    return trace_replace(x, dims, site) - x


def m_anchor(a: np.ndarray, dims=(2, 3, 3, 3)):
    p = np.outer(a, a.conj())
    d = p.shape[0]
    out = 0.5 * (np.trace(p) * np.eye(d) - p)
    for i in range(1, 4):
        for j in range(i + 1, 4):
            out += reduction(reduction(p, dims, i), dims, j)
    x = p
    for i in range(1, 4):
        x = reduction(x, dims, i)
    out += 3 * x
    return out


def main():
    rng = np.random.default_rng(12990)
    for k in range(10):
        a = rng.normal(size=54) + 1j * rng.normal(size=54)
        a /= np.linalg.norm(a)
        vals = np.linalg.eigvalsh(m_anchor(a))
        print(k, vals[0], vals[:5])


def alternating(dims=(2, 3, 3, 3), starts=100, steps=100):
    rng = np.random.default_rng(821122)
    d = int(np.prod(dims))
    best = (1e9, None, None)
    for start in range(starts):
        a = rng.normal(size=d) + 1j * rng.normal(size=d)
        a /= np.linalg.norm(a)
        old = 1e9
        for _ in range(steps):
            vals, vecs = np.linalg.eigh(m_anchor(a, dims))
            b = vecs[:, 0]
            vals2, vecs2 = np.linalg.eigh(m_anchor(b, dims))
            a = vecs2[:, 0]
            value = float(np.vdot(b, m_anchor(a, dims) @ b).real)
            if abs(value - old) < 1e-13:
                break
            old = value
        if value < best[0]:
            best = (value, a, b)
            print("alternate best", start, value)
    return best


if __name__ == "__main__":
    main()
    alternating()

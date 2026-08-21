"""Inspect adaptive-frame defect of phase superpositions A+exp(i theta)B."""

from itertools import combinations

import numpy as np


def ptr_vec_projector(x: np.ndarray, dims, kept):
    """Reduced density matrix of |x><x| on kept parties."""
    kept = tuple(kept)
    rest = tuple(i for i in range(len(dims)) if i not in kept)
    xp = x.reshape(dims).transpose(kept + rest)
    dk = int(np.prod([dims[i] for i in kept], dtype=int))
    dr = int(np.prod([dims[i] for i in rest], dtype=int))
    m = xp.reshape(dk, dr)
    return m @ m.conj().T


def delta(x: np.ndarray, dims=(2, 3, 3, 3)):
    p_k = np.vdot(ptr_vec_projector(x, dims, (0,)),
                  ptr_vec_projector(x, dims, (0,))).real
    ans = 3 * p_k
    for i in range(1, 4):
        p_ki = ptr_vec_projector(x, dims, (0, i))
        p_i = ptr_vec_projector(x, dims, (i,))
        ans += np.vdot(p_i, p_i).real - 2 * np.vdot(p_ki, p_ki).real
    return ans


def transition_overlap(a, b, dims, kept):
    """Tr(rho_A^kept rho_B^kept)."""
    ra = ptr_vec_projector(a, dims, kept)
    rb = ptr_vec_projector(b, dims, kept)
    return np.vdot(ra, rb).real


def anchored_d(a, b, dims=(2, 3, 3, 3)):
    qk = transition_overlap(a, b, dims, (0,))
    ans = 3 * qk
    for i in range(1, 4):
        ans -= 2 * transition_overlap(a, b, dims, (0, i))
    for i, j in combinations(range(1, 4), 2):
        ans += transition_overlap(a, b, dims, (0, i, j))
    ans += (np.vdot(a, a).real * np.vdot(b, b).real
            - abs(np.vdot(a, b)) ** 2) / 2
    return ans


def random_matched(rng, d=3):
    n = d ** 3
    xu = rng.normal(size=(n, 2)) + 1j * rng.normal(size=(n, 2))
    xv = rng.normal(size=(n, 2)) + 1j * rng.normal(size=(n, 2))
    u, _ = np.linalg.qr(xu)
    v, _ = np.linalg.qr(xv)
    ss = np.exp(rng.uniform(-1, 1, size=2))
    a = np.stack([np.sqrt(ss[r]) * u[:, r] for r in range(2)])
    b = np.stack([np.sqrt(ss[r]) * v[:, r] for r in range(2)])
    return a.reshape(-1), b.reshape(-1)


def fourier_f(a, b, count=16):
    vals = np.array([
        delta(a + np.exp(2j * np.pi * k / count) * b)
        for k in range(count)
    ])
    return np.fft.fft(vals) / count


def main():
    rng = np.random.default_rng(77291)
    for _ in range(5):
        a, b = random_matched(rng)
        ff = fourier_f(a, b)
        dd = anchored_d(a, b)
        print("D", dd, "deltaA/B", delta(a), delta(b))
        print("fourier c0,c1,c2", ff[0], ff[1], ff[2])
        print("ratios D/c0", dd / ff[0].real)


if __name__ == "__main__":
    main()

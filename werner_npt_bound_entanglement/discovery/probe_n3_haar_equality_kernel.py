#!/usr/bin/env python3
"""Discovery probe for the conditional-normal Haar-equality equations.

For a prescribed right singular two-plane V, build the linear map on
C = U V^* imposed by

    P L_i(P (L_j L_k C)) V = 0

for every rank-two local projection P.  A finite generic sample of P's
spans the degree-(2,2) polynomial identity.  This is discovery code:
small singular values are not exact certificates.
"""

from __future__ import annotations

import argparse
import numpy as np


def local_L(c: np.ndarray, site: int) -> np.ndarray:
    """Apply A -> A - Tr_site(A) I_site / 2 to a 27 by 27 matrix."""
    t = c.reshape((3, 3, 3, 3, 3, 3))
    tr = np.trace(t, axis1=site, axis2=3 + site)
    lifted = np.zeros_like(t)
    for a in range(3):
        sl = [slice(None)] * 6
        sl[site] = a
        sl[3 + site] = a
        lifted[tuple(sl)] = tr
    return (t - 0.5 * lifted).reshape((27, 27))


def left_local(p: np.ndarray, c: np.ndarray, site: int) -> np.ndarray:
    t = c.reshape((3, 3, 3, 3, 3, 3))
    out = np.tensordot(p, t, axes=(1, site))
    out = np.moveaxis(out, 0, site)
    return out.reshape((27, 27))


def local_vectors() -> list[np.ndarray]:
    """A deterministic overcomplete set of CP^2 points."""
    out: list[np.ndarray] = []
    eye = np.eye(3, dtype=complex)
    out.extend(eye)
    phases = [1, -1, 1j, -1j]
    for a in range(3):
        for b in range(a + 1, 3):
            for phase in phases:
                z = eye[a] + phase * eye[b]
                out.append(z / np.linalg.norm(z))
    # Three-support points expose the remaining mixed quartics.
    for p in phases:
        for q in phases:
            z = eye[0] + p * eye[1] + q * eye[2]
            out.append(z / np.linalg.norm(z))
    return out


def ghz_plane(shift: int = 1) -> np.ndarray:
    v = np.zeros((27, 2), dtype=complex)
    for a in range(3):
        v[9 * a + 3 * a + a, 0] = 1 / np.sqrt(3)
        b = (a + shift) % 3
        v[9 * a + 3 * a + b, 1] = 1 / np.sqrt(3)
    return v


def random_plane(rng: np.random.Generator) -> np.ndarray:
    x = rng.normal(size=(27, 2)) + 1j * rng.normal(size=(27, 2))
    q, _ = np.linalg.qr(x)
    return q[:, :2]


def build_map(v: np.ndarray, sites: tuple[int, ...]) -> np.ndarray:
    zs = local_vectors()
    basis_outputs: list[np.ndarray] = []
    for r in range(2):
        for a in range(27):
            c = np.zeros((27, 27), dtype=complex)
            c[a, :] = v[:, r].conj()
            pieces: list[np.ndarray] = []
            for site in sites:
                rest = c.copy()
                for other in range(3):
                    if other != site:
                        rest = local_L(rest, other)
                for z in zs:
                    p = np.eye(3) - np.outer(z, z.conj())
                    pc = left_local(p, rest, site)
                    f = left_local(p, local_L(pc, site), site)
                    pieces.append((f @ v).reshape(-1))
            basis_outputs.append(np.concatenate(pieces))
    return np.stack(basis_outputs, axis=1)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--ghz", action="store_true")
    parser.add_argument("--sites", default="012")
    args = parser.parse_args()
    rng = np.random.default_rng(args.seed)
    v = ghz_plane() if args.ghz else random_plane(rng)
    m = build_map(v, tuple(int(x) for x in args.sites))
    sv = np.linalg.svd(m, compute_uv=False)
    print("shape", m.shape)
    print("largest", sv[0])
    print("smallest", sv[-10:])
    print("numerical rank", np.count_nonzero(sv > 1e-10 * sv[0]))


if __name__ == "__main__":
    main()

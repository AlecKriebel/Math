# Exact \(103\times103\) local crossing bridge for the corrected DTH cone

## Status

This note constructs the local covariant-to-mixed partial-transpose crossing
map with exact rational arithmetic. It supplies two equivalent forms.

1. In a matched permutation/walled-diagram basis the crossing map and its
   inverse are exactly \(I_{103}\).
2. In exact rational highest-weight block coordinates the crossing is the
   bridge
   \[
   h=Ax,\qquad m=Bx,
   \tag{1}
   \]
   where \(A,B\in M_{103}(\mathbb Z)\) are both nonsingular. Thus
   \(m=BA^{-1}h\), but neither the dense inverse nor the dense product needs
   to be stored. Exact forward and inverse solves are performed one right
   hand side at a time.

The construction is memory bounded and dependency free. It is intended for
exact reconstruction of a numerical invariant primal or dual candidate. It
does not determine the sign of the corrected cone.

The verifier and reusable implementation is
verification/agent_dth_local_crossing_exact.py.

## 1. Matched diagram bases

At one physical qutrit site let

\[
{\cal V}_{\rm hol}=(\mathbb C^3)^{\otimes5},
\qquad
{\cal V}_{\rm mix}
=\bar{\mathbb C}^{3\,\otimes2}\otimes\mathbb C^{3\,\otimes3}.
\]

For \(\pi\in S_5\), let \(P_\pi\) permute the five covariant replicas. Let
\(\Theta_{12}\) transpose the first two replicas and put

\[
D_\pi=\Theta_{12}(P_\pi).
\tag{2}
\]

The operators \(D_\pi\) are the corresponding mixed contraction diagrams.
The covariance identity

\[
\Theta_{12}\!\left(
U^{\otimes5}R\,U^{\dagger\otimes5}
\right)
=
(\bar U^{\otimes2}\otimes U^{\otimes3})
\Theta_{12}(R)
(\bar U^{\otimes2}\otimes U^{\otimes3})^\dagger
\tag{3}
\]

shows directly that every \(D_\pi\) belongs to the mixed commutant.

Enumerate \(S_5\) lexicographically, with indices \(0,\ldots,119\). Omit

\[
\boxed{
23,47,71,86,87,89,95,101,107,110,111,113,115,116,117,118,119.
}
\tag{4}
\]

The remaining permutations are denoted \(\pi_1,\ldots,\pi_{103}\). Exact
sparse elimination proves that

\[
\{P_{\pi_b}:1\le b\le103\}
\tag{5}
\]

is a basis of the covariant commutant. Since partial transpose is an
invertible permutation of operator matrix entries,

\[
\{D_{\pi_b}:1\le b\le103\}
\tag{6}
\]

is a basis of the mixed commutant. Therefore

\[
\boxed{
\Theta_{12}\!\left(\sum_bx_bP_{\pi_b}\right)
=\sum_bx_bD_{\pi_b}.
}
\tag{7}
\]

The crossing matrix and inverse in these matched coordinates are both
\(I_{103}\).

The seventeen omitted diagrams are not merely discarded numerically. The
verifier computes their exact reductions in (5). Every reduction coefficient
is an integer; the relations are consequences of four-fold antisymmetrization
in local dimension three.

## 2. Exact Hilbert--Schmidt Gram matrix

For a permutation \(\tau\), let \(c(\tau)\) be its number of cycles, including
fixed points. Directly counting basis words fixed by a permutation gives

\[
\boxed{
G_{ab}
=\operatorname{Tr}(P_{\pi_a}^\dagger P_{\pi_b})
=3^{c(\pi_a^{-1}\pi_b)}.
}
\tag{8}
\]

Partial transpose preserves the Hilbert--Schmidt pairing, so

\[
\operatorname{Tr}(D_{\pi_a}^\dagger D_{\pi_b})=G_{ab}.
\tag{9}
\]

Thus \(G\) has entries only in

\[
\{3,9,27,81,243\}.
\]

Exact modular elimination gives

\[
\det G\equiv
\begin{cases}
471279&\pmod {1000003},\\
901466&\pmod {1000033},\\
379884&\pmod {1000037}.
\end{cases}
\tag{10}
\]

In particular \(G\) is nonsingular over \(\mathbb Q\). This independently
certifies both diagram bases.

## 3. Rational highest-weight bases

For the covariant representation use the integer polytabloid bases already
constructed for the five partitions

\[
[5],\ [4,1],\ [3,2],\ [3,1,1],\ [2,2,1],
\]

with multiplicities \(1,4,5,6,5\) and carrier dimensions
\(21,24,15,6,3\).

For the mixed representation, solve the two exact integer raising-operator
systems in every highest-weight space. Rational row reduction gives bases
for

\[
(3,2)^1,\ (2,1)^6,\ (1,0)^6,\ (1,3)^2,\ (0,2)^5,\ (4,0)^1,
\]

with carrier dimensions \(42,15,3,24,6,15\).

No square roots or numerical nullspaces occur. The Gram determinants of the
five holomorphic bases are

\[
1,\ 5,\ 162,\ 8000,\ 49152,
\tag{11}
\]

and those of the six mixed bases are

\[
1,\ 216,\ 163840,\ 3,\ 2400,\ 2.
\tag{12}
\]

All are nonzero.

## 4. The exact block bridge

Let \(H_\lambda\) be the matrix whose columns are the exact holomorphic
highest-weight basis vectors, and \(M_\mu\) the analogous mixed matrix.
For every selected diagram define

\[
\begin{aligned}
A_{\lambda,b}&=H_\lambda^\dagger P_{\pi_b}H_\lambda,\\
B_{\mu,b}&=M_\mu^\dagger D_{\pi_b}M_\mu.
\end{aligned}
\tag{13}
\]

Flatten and concatenate all square blocks in (13). Since

\[
\sum_\lambda(f^\lambda)^2=103,
\qquad
\sum_\mu m_\mu^2=103,
\]

this gives two square matrices \(A,B\in M_{103}(\mathbb Z)\).
They are relatively sparse:

\[
\#\operatorname{supp}A=9031,\qquad
\#\operatorname{supp}B=7228,
\tag{14}
\]

with largest absolute entries \(12\) and \(54\), respectively.

Their exact modular determinants are

\[
\begin{array}{c|ccc}
&1000003&1000033&1000037\\ \hline
\det A&35462&66447&581742\\
\det B&260461&350489&842759.
\end{array}
\tag{15}
\]

Thus both are nonsingular over \(\mathbb Q\). Equation (1) is an exact
equivalent representation of the local crossing:

\[
\boxed{m=BA^{-1}h,\qquad h=AB^{-1}m.}
\tag{16}
\]

The implementation exposes exact_restriction_bridge(),
cross_holomorphic_to_mixed(), and cross_mixed_to_holomorphic().
The latter two use exact one-right-hand-side rational elimination, so an
exact candidate can be reconstructed without materializing \(A^{-1}\),
\(B^{-1}\), or \(BA^{-1}\).

## 5. Independent block-Gram audit

The block bridge is checked against the raw diagram Gram, not merely by
modular ranks. If \(G_\lambda=H_\lambda^\dagger H_\lambda\) and
\(A_{\lambda,a}\) is a block in (13), then the contribution of the
\(\lambda\)-isotypic component to the Hilbert--Schmidt pairing is

\[
d_\lambda\operatorname{Tr}\!\left(
G_\lambda^{-1}A_{\lambda,a}^\dagger
G_\lambda^{-1}A_{\lambda,b}
\right).
\tag{17}
\]

Consequently

\[
\sum_\lambda d_\lambda\operatorname{Tr}\!\left(
G_\lambda^{-1}A_{\lambda,a}^\dagger
G_\lambda^{-1}A_{\lambda,b}
\right)
=G_{ab}.
\tag{18}
\]

The verifier checks (18) coefficient by coefficient over \(\mathbb Q\).
It separately checks the mixed identity

\[
\sum_\mu \widehat d_\mu\operatorname{Tr}\!\left(
\widehat G_\mu^{-1}B_{\mu,a}^\dagger
\widehat G_\mu^{-1}B_{\mu,b}
\right)
=G_{ab}.
\tag{19}
\]

Both reconstructed \(103\times103\) matrices equal the integer matrix (8)
exactly. This audits the permutation convention, two-slot transpose,
rational highest-weight bases, carrier-dimension weights, and bridge
normalizations.

## 6. Three-site use and equality-nullspace reconstruction

For three physical sites, use the coefficient tensor
\(x_{b_1b_2b_3}\) in the tensor diagram basis. Before source compression,
the global holomorphic and mixed block coordinates are obtained by

\[
h=(A\otimes A\otimes A)x,
\qquad
m=(B\otimes B\otimes B)x.
\tag{20}
\]

These tensor products should never be allocated densely. Apply the local
matrices successively along the three tensor axes.

All Pluecker, Omega, support, witness-equality, and active-kernel conditions
are rational linear equations in \(x\) once expressed in these exact bases.
A numerical candidate can therefore be processed as follows.

1. Convert its orthonormal highest-weight blocks to the rational basis using
   the small local Gram/change-of-basis matrices.
2. Solve \(Ax=h\) locally, one tensor axis at a time.
3. Impose the reported active nullspaces by exact modular elimination.
4. Reconstruct rational coordinates in the surviving nullspace.
5. Map to mixed blocks with \(B\), and verify positivity or a negative
   principal minor exactly.

The current numerical full-cone trajectory is broad rather than concentrated:
most ordered holomorphic blocks remain active and the apparent negative value
moves toward zero as consistency improves. Thus no exact pseudomoment is
claimed here. The bridge makes the next reconstruction deterministic if a
stable active equality face emerges.

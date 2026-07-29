# Track B9: a Weyl cubic near-miss and the \(U(m)\)-equivariant no-go

**Date:** 2026-07-28--29
**Scope:** exact \(d=6\) cubic construction; fixed-Schmidt-frame numerical
deformations; exact \(U(m)\)-equivariant obstruction for every odd \(m\)
**Status:** the near-miss and equivariant no-go are proved exactly; the
pairing deformation search is numerical evidence only

## 1. Executive conclusion

The Weyl-diagonal canonical-channel countermodel has a surprisingly rigid
shared realization.  Pairing its nineteen Hermitian Schmidt directions
identically produces a traceless Hermitian \(36\times36\) matrix \(H_0\)
that satisfies the full exceptional cubic relation exactly:

\[
(H_0)_{12}(H_0)_{23}(H_0)_{12}
-(H_0)_{23}(H_0)_{12}(H_0)_{23}
=\frac13\bigl((H_0)_{12}-(H_0)_{23}\bigr).
\tag{1}
\]

It is not an exceptional solution because it is not an involution.  Its
minimal polynomial and spectrum are

\[
3H_0^2+2\sqrt3H_0-3I=0,
\qquad
\sigma(H_0)=
\{(-\sqrt3)^{\,9},(1/\sqrt3)^{\,27}\}.
\tag{2}
\]

Thus this construction lands exactly on the cubic variety but on the wrong
quadratic stratum.  The affine transform

\[
K=\frac{I+\sqrt3H_0}{2}
\tag{3}
\]

is an involutive braid operator, but
\(\operatorname{Tr}K=18\), so it is not the balanced exceptional
involution either.

This near-miss suggested preserving the full color symmetry and replacing
the two qubit blocks independently.  That entire mechanism can be excluded,
not merely in \(d=6\), but in every unresolved congruence class.

> **Theorem (odd-color equivariant no-go).**
> Let \(m\) be odd and let
> \(V=\mathbb C^2\otimes\mathbb C^m\).  Suppose a traceless Hermitian
> involution \(H\in\operatorname{End}(V\otimes V)\) is equivariant for the
> diagonal color action
> \[
> I_{\mathbb C^2\otimes\mathbb C^2}\otimes(U\otimes U),
> \qquad U\in U(m),
> \]
> after grouping the two qubit factors before the two color factors.  Then
> \(H\) cannot satisfy (1).

Consequently, no exceptional solution in any dimension
\(d=2m\equiv2\pmod4\) can retain full diagonal \(U(m)\) color symmetry.
This is an exact obstruction for a broad invariant branch, not a proof of
the complete dimension spectrum.

## 2. Closed form of the Weyl point

Let \(F_3\) be the swap on
\(\mathbb C^3\otimes\mathbb C^3\).  Grouping tensor factors as

\[
(Q_1,Q_2,T_1,T_2),
\qquad Q_i\cong\mathbb C^2,\quad T_i\cong\mathbb C^3,
\]

the nineteen-term Weyl construction collapses to

\[
\boxed{
H_0=\frac1{\sqrt3}
\left[
Y\otimes Y\otimes I_9
+(X\otimes X+Z\otimes Z)\otimes F_3
\right].
}
\tag{4}
\]

Indeed, an orthonormal Hermitian basis \(\{Q_a\}_{a=1}^9\) of \(M_3\)
satisfies

\[
\sum_{a=1}^9 Q_a\otimes Q_a=F_3.
\tag{5}
\]

The eighteen equal Schmidt directions are

\[
\frac{Z}{\sqrt2}\otimes Q_a,\qquad
\frac{X}{\sqrt2}\otimes Q_a,
\]

with singular value \(2/\sqrt3\).  The remaining direction is
\(Y\otimes I_3/\sqrt6\), with singular value \(2\sqrt3\).  Substitution
gives (4).

Put

\[
A=Y\otimes Y,\qquad C=X\otimes X+Z\otimes Z.
\]

The Pauli relations give

\[
A^2=I,\qquad C^2=2(I-A),\qquad AC=CA=-C.
\tag{6}
\]

Since \(F_3^2=I\), equation (2) follows immediately from (4) and (6).
The two roots are distinct.  Together with
\(\operatorname{Tr}H_0=0\), this gives multiplicities \(9\) and \(27\).

## 3. Exact six-coefficient certificate for the cubic

The same formula gives a short exact certificate of (1).  Write

\[
H=C_0\otimes I+D_0\otimes F_m
=A_+\otimes P_{\rm sym}+A_-\otimes P_{\rm asym},
\tag{7}
\]

where

\[
C_0=\frac{A_++A_-}{2},\qquad
D_0=\frac{A_+-A_-}{2}.
\]

On three color factors, let \(s=F_{12}\) and \(t=F_{23}\).
The six elements

\[
e,\ s,\ t,\ ts,\ st,\ sts=tst
\]

form the group algebra basis of \(S_3\).  With
\(C_i,D_i\) denoting the adjacent qubit copies, the cubic residual has
the following six coefficients:

\[
\begin{aligned}
\mathcal R_e={}&
C_1C_2C_1+D_1C_2D_1-C_2C_1C_2-D_2C_1D_2
-\frac13(C_1-C_2),\\
\mathcal R_s={}&
C_1C_2D_1+D_1C_2C_1-C_2D_1C_2-\frac13D_1,\\
\mathcal R_t={}&
C_1D_2C_1-C_2C_1D_2-D_2C_1C_2+\frac13D_2,\\
\mathcal R_{ts}={}&C_1D_2D_1-D_2D_1C_2,\\
\mathcal R_{st}={}&D_1D_2C_1-C_2D_1D_2,\\
\mathcal R_{sts}={}&D_1D_2D_1-D_2D_1D_2.
\end{aligned}
\tag{8}
\]

For (4),

\[
C_0=\frac{Y\otimes Y}{\sqrt3},
\qquad
D_0=\frac{X\otimes X+Z\otimes Z}{\sqrt3}.
\tag{9}
\]

Direct Pauli multiplication makes every matrix in (8) zero.  This is
independently checked by the exact verifier, without constructing the
nineteen Weyl directions or the dense \(216\times216\) matrices.

Equivalently, \(K\) from (3) is an involutive braid operator.  Affinely
substituting

\[
H_0=\frac{2K-I}{\sqrt3}
\]

into the braid relation for \(K\) gives (1).

## 4. The \(U(m)\)-equivariant normal form

Assume \(m\ge2\).  The tensor square of the defining \(U(m)\)-module
decomposes multiplicity-free as

\[
\mathbb C^m\otimes\mathbb C^m
=\operatorname{Sym}^2(\mathbb C^m)
\oplus\Lambda^2(\mathbb C^m).
\]

Schur's lemma therefore forces every diagonally \(U(m)\)-equivariant
operator to have the form

\[
\boxed{
H=A\otimes P_{\rm sym}+B\otimes P_{\rm asym},
}
\tag{10}
\]

where \(A,B\in M_4(\mathbb C)\) act on the two qubits.  If \(H\) is a
Hermitian involution, then

\[
A=A^*,\quad B=B^*,\quad A^2=B^2=I_4.
\tag{11}
\]

Write \(a=\operatorname{Tr}A\) and \(b=\operatorname{Tr}B\).  Since
\[
\dim\operatorname{Sym}^2(\mathbb C^m)=\frac{m(m+1)}2,\qquad
\dim\Lambda^2(\mathbb C^m)=\frac{m(m-1)}2,
\]
tracelessness of \(H\) is equivalent to

\[
(m+1)a+(m-1)b=0.
\tag{12}
\]

Both \(a\) and \(b\) belong to
\(\{-4,-2,0,2,4\}\).

For \(m=3\), equation (12) permits precisely

\[
(a,b)=(-2,4),(0,0),(2,-4).
\tag{13}
\]

For odd \(m\ge5\), write \(a=2r,b=2s\), where
\(|r|,|s|\le2\).  Dividing (12) by two and using that
\((m-1)/2\) and \((m+1)/2\) are coprime gives

\[
(r,s)=k\left(\frac{m-1}{2},-\frac{m+1}{2}\right).
\]

The bounds force \(k=0\), hence

\[
a=b=0.
\tag{14}
\]

For \(m=1\), the color factor is trivial and the problem is already the
known \(d=2\) case.

## 5. Restriction to the totally symmetric color sector

The space \(\operatorname{Sym}^3(\mathbb C^m)\) is nonzero.  Both adjacent
color swaps act there as \(+I\).  Consequently, on

\[
(\mathbb C^2)^{\otimes3}
\otimes\operatorname{Sym}^3(\mathbb C^m),
\]

the adjacent copies of (10) reduce to

\[
H_{12}=A_{12},\qquad H_{23}=A_{23}.
\]

If \(H\) satisfies (1), then \(A\) itself satisfies

\[
A_{12}A_{23}A_{12}-A_{23}A_{12}A_{23}
=\frac13(A_{12}-A_{23})
\tag{15}
\]

on three qubits.

If \(a=0\), then \(A\) is a traceless Hermitian involution satisfying
(15), exactly a member of the established empty exceptional class in
base dimension two.  This excludes (14) and the middle case in (13).

It remains only to exclude \(a=\pm2\), which occurs for \(m=3\).

## 6. A basis-free rank-one qubit lemma

> **Lemma.** There is no Hermitian involution
> \(A\in\operatorname{End}(\mathbb C^2\otimes\mathbb C^2)\) with
> \(\operatorname{Tr}A=\pm2\) satisfying (15).

Choose the sign so that

\[
A=I-2Q,
\]

where \(Q=\lvert\psi\rangle\langle\psi\rvert\) has rank one.  Negating
\(A\) preserves (15), so this covers both signs.  The corresponding
projection equation is

\[
Q_1Q_2Q_1-Q_2Q_1Q_2=\frac13(Q_1-Q_2).
\tag{16}
\]

Compress (16) by \(Q_1\).  On the two-dimensional range of \(Q_1\), put

\[
T=Q_1Q_2Q_1.
\]

Then

\[
T-T^2=\frac13(I-T),
\qquad
(T-I)(3T-I)=0.
\tag{17}
\]

Thus both eigenvalues of \(T\) lie in \(\{1,1/3\}\), and

\[
\det T\ge\frac19.
\tag{18}
\]

Write

\[
\lvert\psi\rangle=\sum_{i,j=1}^2S_{ij}\lvert i,j\rangle,
\qquad
\|S\|_F=1.
\]

Under the natural identification
\(\operatorname{ran}Q_1\cong\mathbb C^2\), the compression \(T\) is

\[
T=L^*L,\qquad L=S\overline S.
\tag{19}
\]

This formula is basis-free and does not require an illegitimate
independent Schmidt-basis change on alternating tensor legs.  It gives

\[
\det T
=|\det(S\overline S)|^2
=|\det S|^4.
\tag{20}
\]

If \(s_1,s_2\) are the singular values of \(S\), then
\(s_1^2+s_2^2=1\), so

\[
|\det S|=s_1s_2\le\frac12.
\]

Therefore

\[
\det T\le\frac1{16}<\frac19,
\tag{21}
\]

contradicting (18).  This proves the lemma and the theorem.

## 7. Fixed-Schmidt pairing deformation

The exact channel model fixes nineteen left Schmidt directions
\(A_\alpha\) and singular values

\[
\sigma_1=\cdots=\sigma_{18}=\frac2{\sqrt3},
\qquad
\sigma_{19}=2\sqrt3.
\]

The numerical deformation family was

\[
H(O)=\sum_{i=1}^{19}\sigma_i A_i\otimes
\left(\sum_{j=1}^{19}O_{ji}A_j\right),
\qquad O\in O(19).
\tag{22}
\]

Every member is Hermitian, traceless, has squared Hilbert--Schmidt norm
\(36\), and retains the prescribed left and right Schmidt singular values.
It need not be involutive or satisfy the cubic.

### Exact block-preserving pairing no-go

The symmetry-preserving signed and permutation pairings can be eliminated
before numerical optimization.  More generally, suppose \(O\) fixes the
special \(Y\otimes I_3\) direction up to sign and preserves the two
nine-dimensional spaces

\[
Z\otimes\operatorname{Herm}(3),\qquad
X\otimes\operatorname{Herm}(3).
\]

Then, in grouped coordinates,

\[
H(O)=\frac1{\sqrt3}\left(
\varepsilon\,Y\otimes Y\otimes I
+Z\otimes Z\otimes K_Z
+X\otimes X\otimes K_X
\right),
\tag{22a}
\]

where \(\varepsilon=\pm1\), and \(K_Z,K_X\) are nonzero because each is
the tensor corresponding to an orthogonal map between nine-dimensional
Hilbert--Schmidt spaces.  In \(H(O)^2-I\), the \(X\otimes X\) Pauli
coefficient is

\[
-\frac{2\varepsilon}{3}K_Z,
\]

and the \(Z\otimes Z\) coefficient is

\[
-\frac{2\varepsilon}{3}K_X.
\]

Pauli orthogonality forces both coefficients to vanish if \(H(O)^2=I\),
a contradiction.  The same calculation, with \(X\otimes Z\) and
\(Z\otimes X\), excludes a whole-block interchange.  Thus all
within-block signed, permutation, and orthogonal pairings are ruled out
exactly.  Any viable fixed-Schmidt deformation must genuinely mix the two
blocks (or the exceptional nineteenth direction).

### Tangent calculation at \(O=I\)

The real tangent space has dimension \(171\).  Numerical SVD of the full
cubic Jacobian gives

\[
\operatorname{rank}J=90,\qquad \dim\ker J=81,
\tag{23}
\]

with the smallest nonzero singular value \(10.666666666666655\).
The kernel agrees to \(2.4\times10^{-15}\) with the realification

\[
\mathfrak u(9)\ni A+iB
\longmapsto
\begin{pmatrix}
A&-B\\
B&A
\end{pmatrix},
\qquad A^T=-A,\quad B^T=B,
\tag{24}
\]

on the two nine-dimensional \(Z\)- and \(X\)-blocks; the nineteenth
direction is fixed.

The first derivative of the involution objective also vanishes on the
entire tangent space.  Hence \(H_0\) is a singular intersection point and
first-order analysis alone cannot tell whether an involutive cubic branch
leaves it.

This \(81\)-dimensional infinitesimal kernel does **not** integrate to a
full \(U(9)\) family.  Three seeded Haar-unitary realifications had cubic
residuals between \(9.84\) and \(10.34\).  The scalar \(U(1)\) subgroup
does integrate, but it is only a qubit basis rotation: it leaves the
spectrum (2), and the involution residual remains

\[
\|H^2-I\|_F=4\sqrt3.
\]

All tangent statements in this subsection are numerical diagnostics, not
an exact local-classification theorem.

### Numerical optimization

The optimizer used polar retraction on \(O(19)\), an analytic adjoint
gradient, and the normalized objective

\[
\frac1{36}\|H^2-I\|_F^2
+w\,\frac1{216}\|\mathcal C(H)\|_F^2.
\tag{25}
\]

The analytic gradient was checked against centered finite differences.
Eighteen pilot runs used three retained seeds and
\(w\in\{0,0.01,0.1,1,10,100\}\).  Three further seeds were declared in
advance.  No candidate approached both zero conditions:

| seed | \(w\) | involution residual | cubic residual |
|---:|---:|---:|---:|
| 26073411 | \(0.1\) | \(4.4547\) | \(19.7754\) |
| 26073412 | \(1\) | \(6.9282032303\) | \(5.06\times10^{-6}\) |
| 26073413 | \(10\) | \(6.9282032303\) | \(2.55\times10^{-6}\) |

At higher cubic weight the search returns the \(H_0\) orbit.  At low
cubic weight it lowers the involution residual but badly violates the
cubic.  This is only a failed search in the precisely defined family
(22); it is not evidence of global nonexistence.

## 8. Swap-block numerical provenance

Before the exact theorem above was recognized, real and complex
Grassmann searches were run over (10), with the three trace signatures
(13).  The three-site objective used the six reduced matrices (8), and
later runs also imposed the automatic-standardness filters

\[
2\operatorname{Tr}_{Q_2}A+\operatorname{Tr}_{Q_2}B=0,
\qquad
2\operatorname{Tr}_{Q_1}A+\operatorname{Tr}_{Q_1}B=0.
\tag{26}
\]

No zero appeared.  Those negative runs are retained only as discovery
provenance because Sections 4--6 now exclude the entire ansatz exactly.
The saved JSON files contain the actual \(A,B\) matrices and optimizer
parameters, rather than only hashes.

## 9. Reproduction

Exact verifier:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_weyl_h0_and_swap_block_no_go.py
```

Tangent calculation:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/d6_weyl_pairing_deformation.py \
  --mode tangent \
  --output results/d6_weyl_pairing_tangent.json
```

The complete numerical seed declaration is

```text
results/d6_weyl_swap_seed_manifest.json
```

## 10. Scope and next consequence

The exact theorem excludes all exceptional solutions with full diagonal
\(U(m)\) color symmetry in the unresolved dimensions \(d=2m\equiv2\bmod4\).
It does not exclude:

- solutions with a smaller finite color symmetry;
- solutions whose operator-Schmidt frame is unrelated to (22);
- non-equivariant \(d=6\) solutions;
- deformations that change the Schmidt singular values and break the
  qutrit-swap decomposition.

The useful structural lesson is sharper than another failed numerical
search: the exact Weyl cubic point lies in the natural full-color commutant,
but every balanced involutive point in that commutant would collapse on
the totally symmetric color sector to the already-impossible qubit
problem.  Any genuine \(d\equiv2\pmod4\) construction must therefore break
this full color symmetry.

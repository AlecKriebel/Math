# Four-strand pairing on the nonreal three-strand sector

**Date:** 2026-07-29

**Status:** exact limitation theorem; no unrestricted divisibility result

## 1. Question and conclusion

Let \(d=2s\), and for an arbitrary exceptional Hermitian involution put
\[
S=H_{12},\qquad T=H_{23},\qquad C=H_{34},\qquad U=ST.
\tag{1}
\]
On the generic three-strand sector, \(U\) has the two eigenvalues
\[
\lambda_\pm=\frac{-1\pm2\sqrt2\,i}{3},
\tag{2}
\]
each with multiplicity
\[
m=3s^3.
\tag{3}
\]
Thus \(m\) is odd exactly when \(s\) is odd.  The intended parity route
was to use the fourth-strand generator \(C\) to construct an alternating
form, an antiunitary of square \(-1\), or a second \(M_2\)-action on one
of these two \(m\)-dimensional multiplicity spaces.

The exact four-strand audit gives a sharp negative delimitation:

1. after adding the fourth local site, each nonreal eigenspace splits
   into three Hecke branches, each of multiplicity \(2s^4\);
2. its same-sign Hecke corner is
   \(\mathbb C^3\), while the two-sign corner is
   \(M_2(\mathbb C)^{\oplus3}\);
3. the \(M_2\)'s pair the \(\lambda_+\) and \(\lambda_-\) lines.  They
   do not act on the multiplicity \(3s^3\);
4. the polar fourth-strand intertwiner, combined with the real form of
   the Hecke simples, gives an antiunitary of square \(+1\), not
   \(-1\);
5. normalized last-site trace sends every four-strand Hecke word back
   to the three-strand algebra.  Its compression to one nonreal line is
   scalar, so tracing down cannot create a multiplicity-space \(M_2\);
6. bare partial transpose does not remove the last tensor leg and
   requires a noncanonical identification \(V^*\cong V\);
7. at \(s=3\), all of the resulting corner polynomial, spectrum, and
   zero-last-trace data admit an exact factorization with the odd
   multiplicity \(m=81\).

Consequently, no parity follows from the four-strand Hecke algebra, its
nonreal spectral corners, the polar \(H_{34}\) intertwiner, normalized
last-site trace, or bare partial transpose.  A positive theorem must
use the unresolved **flat tensor-local coherence** which identifies the
same two-site \(H\) at every adjacent placement.

The odd-\(s\) model below is an abstract four-strand representation with
the correct restriction multiplicities and a factorization of the
nonreal corner.  It is not a tensor-local \(d=6\) Yang--Baxter matrix.

## 2. The real three-strand block

The generic irreducible block of the two reflections \(S,T\) has the
real form
\[
S_0=
\begin{pmatrix}1&0\\0&-1\end{pmatrix},
\qquad
T_0=
\begin{pmatrix}
-\frac13&\frac{2\sqrt2}{3}\\
\frac{2\sqrt2}{3}&\frac13
\end{pmatrix}.
\tag{4}
\]
It satisfies
\[
S_0T_0S_0-T_0S_0T_0=\frac13(S_0-T_0),
\tag{5}
\]
and \(S_0T_0\) has spectrum (2).  Let
\(\Pi_\pm\) denote the corresponding spectral projections.  Conjugation
in the displayed real basis exchanges them:
\[
\overline{\Pi_+}=\Pi_-,
\tag{6}
\]
and
\[
S_0\Pi_+S_0=\Pi_-.
\tag{7}
\]

The full three-strand quotient is
\[
\mathcal A_3\cong
\mathbb C\oplus M_2(\mathbb C)\oplus\mathbb C.
\tag{8}
\]
In particular,
\[
\Pi_+\mathcal A_3\Pi_+=\mathbb C\Pi_+,\qquad
\dim_\mathbb C(\Pi_+\mathcal A_3\Pi_-)=1.
\tag{9}
\]
This is the first warning: every three-strand word is scalar on the
\(m\)-dimensional multiplicity of \(\Pi_+\).

## 3. Exact four-strand simple blocks

The exceptional four-strand quotient is
\[
\mathcal A_4
\cong
M_3(\mathbb C)\oplus M_2(\mathbb C)\oplus M_3(\mathbb C),
\tag{10}
\]
with simple labels
\[
(31),\qquad(22),\qquad(211).
\]
Automatic standardness and faithfulness of the matrix trace identify
the image of every exceptional solution with this trace quotient; no
extra localization hypothesis is being inserted here.
Their restrictions are
\[
\begin{aligned}
(31)\downarrow\mathcal A_3&=(3)\oplus(21),\\
(22)\downarrow\mathcal A_3&=(21),\\
(211)\downarrow\mathcal A_3&=(21)\oplus(111).
\end{aligned}
\tag{11}
\]
Thus the generic \(M_2\)-block occurs once in each four-strand simple.

For completeness, all three simples have small exact real reflection
models.  Use \(S_0,T_0\) from (4).  For \((31)\), take
\[
S_{31}=\operatorname{diag}(1,1,-1),\qquad
T_{31}=1\oplus T_0,
\]
\[
C_{31}=
\begin{pmatrix}
0&1&0\\1&0&0\\0&0&1
\end{pmatrix}.
\tag{12}
\]
For \((22)\), take
\[
(S_{22},T_{22},C_{22})=(S_0,T_0,S_0).
\tag{13}
\]
For \((211)\), take
\[
S_{211}=\operatorname{diag}(-1,1,-1),\qquad
T_{211}=(-1)\oplus T_0,
\]
\[
C_{211}=
\begin{pmatrix}
0&0&1\\0&-1&0\\1&0&0
\end{pmatrix}.
\tag{14}
\]
In each case the three operators are Hermitian involutions,
\[
[S,C]=0,
\tag{15}
\]
and the two adjacent pairs satisfy (5).

Since \(\Pi_+\) has rank one in each of (12)--(14), (10)--(11) give
\[
\boxed{
\Pi_+\mathcal A_4\Pi_+\cong\mathbb C^3,
}
\tag{16}
\]
and
\[
\boxed{
(\Pi_++\Pi_-)\mathcal A_4(\Pi_++\Pi_-)
\cong M_2(\mathbb C)^{\oplus3}.
}
\tag{17}
\]
The matrix factors in (17) act on the pair of spectral signs.  They do
not act on any tensor-space multiplicity.

## 4. The canonical \(H_{34}\) compression

Define, on \(\Pi_+V^{\otimes4}\),
\[
B=\Pi_+SC\Pi_+.
\tag{18}
\]
Because \(S\) and \(C\) commute, \(SC\) is a Hermitian involution, so
\(B=B^*\).  Evaluation in (12)--(14) gives the three scalars
\[
\begin{array}{c|ccc}
\text{branch}&(31)&(22)&(211)\\ \hline
B&-\frac12&1&-\frac12.
\end{array}
\tag{19}
\]
Therefore every exceptional solution satisfies
\[
\boxed{(B-I)(B+\tfrac12I)=0}
\quad\text{on }\operatorname{ran}\Pi_+.
\tag{20}
\]

Every four-strand simple in (10) has tensor-space multiplicity
\[
2s^4.
\tag{21}
\]
It follows that the eigenvalue \(1\) in (20) has multiplicity \(2s^4\)
and the eigenvalue \(-1/2\) has multiplicity \(4s^4\).  Their sum is
\[
6s^4=(3s^3)(2s)=md,
\tag{22}
\]
as required after adding the fourth site.  These numbers are integral
for every integer \(s\) and contain no parity condition on \(s\).

Automatic standardness gives
\[
\operatorname{Tr}_4 C=0.
\tag{23}
\]
The two copies of \(\Pi_+\) and the factor \(S\) in (18) are supported
on the first three sites.  Hence
\[
\boxed{\operatorname{Tr}_4B=0.}
\tag{24}
\]
Equation (24) is exactly the cancellation
\[
(2s^4)\cdot1+(4s^4)\cdot(-\tfrac12)=0
\tag{25}
\]
at the level of ordinary traces.  It does not turn either eigenspace
into an even-dimensional copy of the original \(m\)-space.

For the published \(d=4\) witness, \(s=2\).  Thus (19) appears with
exact multiplicities
\[
32,\quad32,\quad32,
\tag{26}
\]
and \(B\) has eigenvalue \(1\) with multiplicity \(32\) and
\(-1/2\) with multiplicity \(64\).  The evenness visible here comes
from the universal factor \(2s^4\), not from a symplectic structure on
the original \(m=24\) multiplicity.

## 5. The polar linking antiunitary is orthogonal

The direct fourth-strand link between the two nonreal sectors is
\[
A=\Pi_+C\Pi_-.
\tag{27}
\]
Using (7),
\[
B=A S\Pi_+,
\tag{28}
\]
and hence
\[
AA^*=B^2.
\tag{29}
\]
Thus the singular values of \(A\) in the branches
\((31),(22),(211)\) are
\[
\frac12,\qquad1,\qquad\frac12.
\tag{30}
\]
In particular, its polar part \(W:\operatorname{ran}\Pi_-\to
\operatorname{ran}\Pi_+\) is unitary.

Let \(K\) be entrywise conjugation in the real models (12)--(14).  It
exchanges \(\Pi_+\) and \(\Pi_-\).  Since
\[
\overline A=A^*,
\]
polar decomposition gives
\[
\overline W=W^*.
\tag{31}
\]
Consequently
\[
\Theta=WK:\operatorname{ran}\Pi_+\longrightarrow
\operatorname{ran}\Pi_+
\tag{32}
\]
is antiunitary but
\[
\boxed{\Theta^2=W\overline W=WW^*=I.}
\tag{33}
\]
It is an orthogonal real structure, not a Kramers structure.

This conclusion is unchanged if \(W\) is replaced by any Hecke-algebra
unitary in the linking corner.  By (17), such a unitary is one phase
times \(W\) in each of the three simple branches.  The phase cancels in
\(X\overline X\), leaving square \(+1\) branch by branch.

One can introduce a square-\(-1\) antiunitary by inserting an operator
from the tensor multiplicity commutant.  On each four-strand branch that
multiplicity has dimension \(2s^4\), which is already even for every
\(s\).  This optional choice therefore gives no information about the
parity of \(m=3s^3\), and it is not supplied by a Hecke word.

## 6. Tracing a four-strand word cannot act on \(m\)

Let
\[
\mathbb E_3(X)=\frac1d\operatorname{Tr}_4(X)
\tag{34}
\]
be normalized last-site trace.  It maps
\(\mathcal A_4\) into \(\mathcal A_3\).

This can be seen without importing a tower theorem.  The ordinary
Hecke double-coset decomposition gives
\[
\mathcal A_4
=\mathcal A_3+\mathcal A_3C\mathcal A_3.
\tag{35}
\]
The map \(\mathbb E_3\) is \(\mathcal A_3\)-bimodular and (23) says
\(\mathbb E_3(C)=0\).  Thus (35) immediately implies the asserted
range.

For every \(X\in\mathcal A_4\),
\[
\Pi_+\mathbb E_3(X)\Pi_+
\in\Pi_+\mathcal A_3\Pi_+
=\mathbb C\Pi_+.
\tag{36}
\]
Likewise, the off-diagonal compression lies in the one-dimensional
space in (9).  Therefore no sequence consisting of

- four-strand Hecke words,
- compression by \(\Pi_\pm\),
- normalized last-site traces, and
- polar decomposition inside a nonzero one-dimensional linking corner

can produce a noncommutative action on the \(m\)-dimensional
multiplicity.  The only antiunitary sign obtained from the real linking
corner is (33).

## 7. Why bare partial transpose does not close the argument

Partial transpose on the fourth factor changes the variance of that
factor.  Coordinate-free, it naturally replaces an occurrence of
\(V\) by \(V^*\); it does not erase the last tensor leg or produce an
endomorphism of \(\operatorname{ran}\Pi_+\subset V^{\otimes3}\).

To regard the result again as acting on \(V\), one must choose an
**complex-linear** identification
\[
V^*\cong V,
\tag{37}
\]
equivalently a nondegenerate bilinear form on \(V\).  There is no
nonzero \(U(d)\)-equivariant choice: a scalar unitary \(e^{i\theta}I\)
acts on \(V\) and \(V^*\) with opposite weights, so equivariance for
all \(\theta\) forces the map to vanish.

The Hermitian inner product does give the canonical anti-linear Riesz
map \(V\to V^*\).  Using it on both sides converts transpose back to
the ordinary adjoint; it does not supply a complex bilinear form or an
antiunitary of square \(-1\) on the three-strand multiplicity.

An \(H\)-dependent identification might conceivably exist, but proving
that would be a new structural theorem.  Bare partial transpose itself
does not supply it.  Choosing an alternating form on the already-even
local space \(V\) also cannot be used as evidence that the unrelated
multiplicity \(m\) is even.

Tensor flips have the same closure problem.  Reversal of four sites
sends
\[
(S,T,C)\longmapsto(C,T,S),
\]
so it sends the \(\lambda_+\)-space of \(ST\) to a generally different
spectral space for \(CT\).  A local two-site flip sends \(H\) to the
opposite solution \(FHF\), which need not equal \(H\).  For the
published \(d=4\) witness this failure is exact:
\[
\left\|P-FPF\right\|_{\mathrm{HS}}^2=8
\]
(`notes/overlap_kramers_parity_audit.md`).  Hence neither bare reversal
nor local flip canonically closes the fourth-strand polar map on one
chosen nonreal multiplicity.

## 8. Exact odd-\(s\) limitation model

Take \(s=3\), so
\[
d=6,\qquad m=3s^3=81,\qquad2s^4=162.
\tag{38}
\]
Form the exact abstract four-strand module
\[
S_{31}\otimes\mathbb C^{162}
\;\oplus\;
S_{22}\otimes\mathbb C^{162}
\;\oplus\;
S_{211}\otimes\mathbb C^{162},
\tag{39}
\]
using the matrices (12)--(14).  Its dimension is \(6^4=1296\).
Its restriction to three strands has multiplicities
\[
162,\qquad486,\qquad162,
\tag{40}
\]
which are exactly the three-strand multiplicities
\[
27,\qquad81,\qquad27
\tag{41}
\]
tensored by a six-dimensional spectator.

On the \(\Pi_+\) sector, identify
\[
\mathbb C^{486}\cong\mathbb C^{81}\otimes\mathbb C^6
\]
by splitting the last factor into three two-dimensional colors
corresponding to \((31),(22),(211)\).  Then (18) becomes
\[
B=I_{81}\otimes
\operatorname{diag}
\left(
-\tfrac12,-\tfrac12,\,
1,1,\,
-\tfrac12,-\tfrac12
\right).
\tag{42}
\]
This operator is invertible, Hermitian, obeys (20), and has zero trace
over the displayed six-dimensional factor.  Partial transpose leaves
this real diagonal model symmetric, not alternating.

Thus every invariant isolated in Sections 3--7 is compatible with the
odd value \(m=81\).  The model does not extend (39) to a common
two-site tensor-local generator \(H\) on \((\mathbb C^6)^{\otimes2}\).
The compatibility of the three branch-multiplicity identifications
with the common/zero sectors is precisely the missing flat-coherence
problem.

## 9. Remaining viable target

The fourth strand does contain information beyond the abstract
three-strand two-projection block, but its ordinary Hecke content is now
exhausted for this parity route.  A successful proof that \(4\mid d\)
must construct structure on the multiplicity \(3s^3\) from the actual
spatial equality
\[
H_{12}=H\otimes I,\qquad
H_{23}=I\otimes H,\qquad
H_{34}=I^{\otimes2}\otimes H,
\tag{43}
\]
not merely from an abstract representation of \(\mathcal A_4\).

Equivalently, it must prove that the three branch identifications in
(39)--(42) cannot be made coherently when \(s\) is odd.  Neither the
Hecke corner algebra nor its canonical polar pairing detects that
failure.

The independent exact replay is
`verifiers/verify_four_strand_nonreal_pairing_limitation.py`.

# Lossless physical-site reduction of the degree-three source cone

## Theorem and census

The complete post-Omega degree-three source contains 487 ordered local-shape
blocks and 519434 real-symmetric coordinates.  The physical-site group
(S_3) permutes the three local shapes and acts orthogonally inside blocks
with repeated shapes.

For a site-invariant five-replica target and an equivariant marginal map,
source averaging is lossless.  The invariant positive source cone is exactly
a product of 171 smaller positive-semidefinite cones, with

\[
\boxed{
\begin{aligned}
\text{active unordered shape orbits}&=112,\\
\text{PSD cone components}&=171,\\
\text{sum of component ranks}&=3665,\\
\text{invariant symmetric variables}&=87540,\\
\text{largest component rank}&=106.
\end{aligned}}
\tag{1}
\]

For comparison, the largest ordered block has rank 298.  The sum of cubes
of the component ranks, which controls a complete eigendecomposition sweep,
falls to

\[
\boxed{11060723.}
\tag{2}
\]

This reduction is exact and preserves both feasibility and strict block
floors after the elementary orbit normalizations below.

## 1. Why averaging is lossless

Let

\[
\mathcal X=\bigoplus_\Lambda\operatorname{Sym}(K_\Lambda)
\]

be the ordered source, let (\mathcal C\subset\mathcal X) be its product PSD
cone, and let (A:\mathcal X\to\mathcal Y) be the degree-three marginal.
Physical-site permutations act orthogonally, preserve (\mathcal C), and
intertwine (A).  If the required target (r) is invariant and (AX=r) with
(X\in\mathcal C), then

\[
\bar X=\frac16\sum_{\pi\in S_3}\pi X
\]

is positive, invariant, and still satisfies (A\bar X=r).  The converse is
immediate.  Hence restricting to (\mathcal C^{S_3}) loses nothing.

## 2. Stabilizer cone decomposition

Choose one sorted shape triple from each orbit and write (m) for its
post-Omega multiplicity rank.

### Three distinct shapes

The stabilizer is trivial.  One matrix in (\operatorname{PSD}_m) determines
all six ordered blocks by orthogonal congruence.

### Exactly two equal shapes

Let (T) be the orthogonal involution that exchanges the equal physical
sites.  If its eigenspace dimensions are (p,q), then an invariant source
block is

\[
X=Q_+X_+Q_+^{\mathsf T}+Q_-X_-Q_-^{\mathsf T},
\qquad
X_+\succeq0,\quad X_-\succeq0.
\tag{3}
\]

Thus this orbit contributes (\operatorname{PSD}_p\times
\operatorname{PSD}_q), omitting zero factors.

### Three equal shapes

Decompose the stabilizer representation as

\[
K_\Lambda
\cong
\mathbb R^a\otimes[3]
\oplus
\mathbb R^b\otimes[1,1,1]
\oplus
\mathbb R^c\otimes[2,1].
\tag{4}
\]

The invariant symmetric positive cone is exactly

\[
\operatorname{PSD}_a\times
\operatorname{PSD}_b\times
\operatorname{PSD}_c,
\tag{5}
\]

where a matrix in the last factor is repeated on the two-dimensional
standard irrep.  For the seven active equal-shape blocks, indexed by the
local S7 list used throughout the project, the exact decompositions are

\[
\begin{array}{c|c|c}
i& m&(a,b,c)\\ \hline
1&1&(1,0,0)\\
2&23&(6,3,7)\\
3&26&(7,3,8)\\
4&23&(7,2,7)\\
5&298&(55,47,98)\\
6&65&(15,8,21)\\
7&62&(11,11,20).
\end{array}
\tag{6}
\]

The dimension identity is (a+b+2c=m).

## 3. Exact stabilizer characters

The entries in (1) and (6) do not come from numerical eigenspaces.  Let
(V_i) be the restriction to (S_6) of the local (S_7) Specht module
([\Lambda_i]), and let (\chi_i) denote its character.  Before Omega
deflation, the source multiplicity space is

\[
\operatorname{Hom}_{S_6}
\bigl([3,3],V_1\otimes V_2\otimes V_3\bigr).
\]

For a repeated shape (a) and singleton (b), the trace of the site
transposition is

\[
\boxed{
t_{aab}
=\frac1{6!}\sum_{g\in S_6}
\chi_{33}(g)\chi_a(g^2)\chi_b(g).
}
\tag{7}
\]

For three equal shapes, the trace of a site three-cycle is

\[
\boxed{
u_{aaa}
=\frac1{6!}\sum_{g\in S_6}
\chi_{33}(g)\chi_a(g^3).
}
\tag{8}
\]

These follow from the elementary identities

\[
\operatorname{Tr}\bigl(F(A\otimes A)\bigr)=\operatorname{Tr}(A^2),
\qquad
\operatorname{Tr}\bigl(C_3A^{\otimes3}\bigr)=\operatorname{Tr}(A^3).
\]

The Omega map is site-equivariant and surjective onto its established S4
output.  Therefore its corresponding S4 character traces, obtained from
(7)--(8) with ([3,3],S_6) replaced by ([2,2],S_4), subtract from (t) and
(u).  On the post-Omega kernel,

\[
p=\frac{m+t}{2},\qquad q=\frac{m-t}{2},
\tag{9}
\]

and

\[
a=\frac{m+3t+2u}{6},\qquad
b=\frac{m-3t+2u}{6},\qquad
c=\frac{m-u}{3}.
\tag{10}
\]

This proves the cone decomposition and makes the census wholly exact.

## 4. Isometric coordinates for a reduced projection engine

For an orbit of size (h), store one representative matrix with the embedding

\[
X_{\pi\Lambda}=h^{-1/2}T_\pi X_\Lambda T_\pi^{\mathsf T}.
\tag{11}
\]

For (aab), apply (11) independently to the two matrices in (3).  For the
standard component in (4), first use the canonical repetition
(C\mapsto C\otimes I_2) and then divide by (\sqrt2).  With these factors,
the embedding from the 171 reduced matrix spaces into the 487 ordered blocks
is an isometry for the Frobenius inner product.  Its adjoint is therefore the
exact source reduction needed in (AA^*) and in Douglas--Rachford affine
projection.  PSD projection consists of only 171 eigendecompositions in the
ranks counted in (1).

The square roots in (11) are merely numerical isometric coordinates.  An
exact rational certificate may instead retain orbit-size weights in its
inner product.

## 5. Numerical Slater point for the PSD-only marginal problem

The reduced projection engine was applied to the complete 761-coordinate
site-invariant target.  Direct effective Kraus maps remove the intermediate
expansion to all 487 ordered source blocks.  Their marginal agrees with the
expanded marginal to Frobenius error (3.75\times10^{-13}) in the numerical
audit.

The physical common-floor normalization is as follows.  For an orbit of
size (h), the reduced shift is

\[
S_c(t)=t\sqrt h\,r_c I,
\qquad
r_c=\begin{cases}
\sqrt2,&c\text{ is a standard }S_3\text{ component},\\
1,&\text{otherwise}.
\end{cases}
\tag{12}
\]

With the isometric embedding (E) of (11), direct substitution gives

\[
\boxed{E(S(t))_\Lambda=tI_\Lambda}
\tag{13}
\]

for every one of the 487 ordered source blocks.  Hence a reduced positive
solution (Z_c\succeq0) of

\[
A Z=r-A S(t)
\]

produces the physical source (E(Z+S(t))), satisfying every ordered-block
bound (X_\Lambda\succeq tI_\Lambda).

Using the saved floor-zero candidate as a warm start, the complete reduced
solve at (t=10^{-12}) produced

\[
\begin{aligned}
\|A Z-(r-AS(t))\|_2&=2.8872376192091776\times10^{-20},\\
\left(\sum_c\|Z_{c,-}\|_F^2\right)^{1/2}&=0,\\
\min_c\lambda_{\min}(Z_c)&=5.885296438818831\times10^{-20}.
\end{aligned}
\tag{14}
\]

After expansion, the smallest eigenvalue among all 487 physical ordered
blocks is (1.000000033978775\times10^{-12}).  The retained floating-point
cache is `discovery/dth_level2_source_reduced_floor1e12_warm.pkl`, with
SHA-256

```
998d978a306869cf32b5bf46a493d34236cd7e45f1b69004982268bc297b5cb9
```

This is a numerical Slater point for the **holomorphic PSD-only
fixed-marginal relaxation**.  It is not yet an exact rational certificate,
and it does not impose the prolonged support partial-transpose face or the
remaining grouped PPT constraints.

## Verification

`verification/verify_dth_level2_source_site_symmetry.py` evaluates
(7)--(10) by exact conjugacy-class arithmetic, checks every one of the 112
active orbit rows, and pins all totals in (1)--(2).  It uses only Python's
standard library and the independent exact S7 character census.

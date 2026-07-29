# The full one-sided \(4+2\) extension branch

**Date:** 2026-07-29

**Status:** complete exact color-block reduction and corrected numerical
falsifier; no extension theorem and no candidate

## 1. Outcome and scope

Let
\[
V=W\oplus U,\qquad \dim W=4,\qquad\dim U=2,
\tag{1}
\]
and suppose that \(W\otimes W\) reduces an exceptional projection \(P\),
with restriction equal to the published \(d=4\) projection \(Q\).
Nothing is assumed about the individual cells
\[
W\otimes U,\qquad U\otimes W,\qquad U\otimes U.
\tag{2}
\]
They may mix arbitrarily.

This audit gives:

1. a complete six-block parametrization of the arbitrary
   \(20\)-dimensional complement projection;
2. every projection and scalar-partial-trace equation in those blocks;
3. one master formula which is exactly equivalent to all \(64\)
   input/output color blocks of the ambient cubic;
4. a dedicated Grassmann search that really freezes the published
   \(16\times16\) block throughout;
5. an adversarial search constrained toward nonzero
   \(U\otimes U\)-leakage;
6. a correction to the interpretation of the earlier numerical archive.

No exact extension was found.  More importantly, no proof was found that
the cubic forces \(U\otimes U\) to reduce.  The result is therefore a
rigorous reduction and provenance correction, not a nonexistence theorem.

The exact question remains
\[
\boxed{
\text{Do the block equations below force }X=Y=0?
}
\tag{3}
\]

## 2. The complete two-site block

Order the three non-\(WW\) cells as
\[
a=W\otimes U,\qquad
b=U\otimes W,\qquad
c=U\otimes U.
\tag{4}
\]
Since \(P=P^*\) and \(W\otimes W\) is invariant, that cell is reducing.
Thus
\[
P=Q\oplus K,
\tag{5}
\]
where \(Q\) is the fixed published rank-eight projection and \(K\) is
an arbitrary rank-ten projection on the direct sum in (4).  Write
\[
\boxed{
K=
\begin{pmatrix}
A&Z&X\\
Z^*&B&Y\\
X^*&Y^*&C
\end{pmatrix}.
}
\tag{6}
\]
The block types are
\[
\begin{aligned}
A&\in\operatorname{End}(W\otimes U),&
B&\in\operatorname{End}(U\otimes W),\\
C&\in\operatorname{End}(U\otimes U),&
Z&:U\otimes W\to W\otimes U,\\
X&:U\otimes U\to W\otimes U,&
Y&:U\otimes U\to U\otimes W.
\end{aligned}
\tag{7}
\]
No block in (6) is silently set to zero.

The projection identity \(K^2=K\) is exactly the following six equations
and their adjoints:
\[
\begin{aligned}
A^2+ZZ^*+XX^*&=A,\\
B^2+Z^*Z+YY^*&=B,\\
C^2+X^*X+Y^*Y&=C,\\
AZ+ZB+XY^*&=Z,\\
AX+ZY+XC&=X,\\
Z^*X+BY+YC&=Y.
\end{aligned}
\tag{8}
\]

The complementary square \(U\otimes U\) reduces \(P\) if and only if
\[
X=Y=0.
\tag{9}
\]
Since \(\operatorname{Tr}C=2\), the exact leakage defect is
\[
\boxed{
\delta
=2-\operatorname{Tr}(C^2)
=\|X\|_{\mathrm{HS}}^2+\|Y\|_{\mathrm{HS}}^2.
}
\tag{10}
\]
Thus (9) is equivalent to \(\delta=0\).

## 3. All scalar-partial-trace equations

Automatic standardness of any exact exceptional extension gives
\[
\operatorname{Tr}_1P=\operatorname{Tr}_2P=3I_6.
\tag{11}
\]
The fixed restriction has
\[
\operatorname{Tr}_1Q=\operatorname{Tr}_2Q=2I_4.
\tag{12}
\]
Subtracting (12) from (11) and retaining the off-diagonal first- and
second-leg blocks gives all of the following operator equations.

Tracing the displayed \(U\)-leg in \(A\), and the displayed \(U\)-leg
in \(B\), gives
\[
\boxed{
\operatorname{Tr}_{U}^{(2)}A=I_W,\qquad
\operatorname{Tr}_{U}^{(1)}B=I_W.
}
\tag{13}
\]
On the \(U\)-diagonal marginal blocks,
\[
\boxed{
\operatorname{Tr}_{W}^{(1)}A+\operatorname{Tr}_{U}^{(1)}C=3I_U,
}
\tag{14}
\]
\[
\boxed{
\operatorname{Tr}_{W}^{(2)}B+\operatorname{Tr}_{U}^{(2)}C=3I_U.
}
\tag{15}
\]
The only off-diagonal marginal blocks which survive the color
contraction are
\[
\boxed{
\operatorname{Tr}_{U}^{(2)}X=0_{W,U},\qquad
\operatorname{Tr}_{U}^{(1)}Y=0_{W,U}.
}
\tag{16}
\]
The transfer block \(Z\) has different colors on both contracted legs
and contributes to neither one-site partial trace.

Equations (13)--(16) imply
\[
\operatorname{Tr}A=4,\qquad
\operatorname{Tr}B=4,\qquad
\operatorname{Tr}C=2,
\tag{17}
\]
and hence \(\operatorname{Tr}K=10\), as required.

The exact two-site limitation model in
`notes/one_sided_square_invariance_audit.md` satisfies every equation
(5)--(17) with
\[
\delta=\frac12.
\tag{18}
\]
Therefore none of these two-site equations can prove (9).

## 4. The complete \(64\)-block cubic equation

Put \(V_0=W\), \(V_1=U\).  For two color pairs
\(\alpha=(\alpha_1,\alpha_2)\) and
\(\beta=(\beta_1,\beta_2)\), let
\[
\mathsf P_{\alpha,\beta}:
V_{\beta_1}\otimes V_{\beta_2}
\longrightarrow
V_{\alpha_1}\otimes V_{\alpha_2}
\tag{19}
\]
be the corresponding block of \(P\).  The only nonzero blocks involving
\((0,0)\) are
\[
\mathsf P_{00,00}=Q.
\tag{20}
\]
The remaining nine blocks are exactly the entries of (6).

Let
\[
\mathcal D=P_{12}P_{23}P_{12}
-P_{23}P_{12}P_{23}
-\frac13(P_{12}-P_{23}).
\tag{21}
\]
For output color \(abc\in\{0,1\}^3\) and input color
\(ijk\in\{0,1\}^3\), the complete block is
\[
\boxed{
\begin{aligned}
\mathcal D_{abc,ijk}
={}&
\sum_{x,y,z\in\{0,1\}}
(\mathsf P_{ab,xz}\otimes I_c)
(I_x\otimes\mathsf P_{zc,yk})
(\mathsf P_{xy,ij}\otimes I_k)\\
&-
\sum_{x,y,t\in\{0,1\}}
(I_a\otimes\mathsf P_{bc,ty})
(\mathsf P_{at,ix}\otimes I_y)
(I_i\otimes\mathsf P_{xy,jk})\\
&-\frac13\,\delta_{c,k}
(\mathsf P_{ab,ij}\otimes I_k)
+\frac13\,\delta_{a,i}
(I_i\otimes\mathsf P_{bc,jk}).
\end{aligned}
}
\tag{22}
\]
Here juxtaposition on each line means composition from right to left,
and \(I_x\) is the identity on \(V_x\).

Equation (22), for the \(8\times8\) choices of output and input color,
is exactly equivalent to the full ambient cubic:
\[
\boxed{
\mathcal D=0
\quad\Longleftrightarrow\quad
\mathcal D_{abc,ijk}=0
\text{ for all }abc,ijk.
}
\tag{23}
\]
This is not a schematic path count.  The independent exact verifier
assembles a deterministic rational two-site operator, evaluates the
dense three-site residual independently, and checks all \(64\) blocks
entry by entry against (22).

The \(000\leftarrow000\) equation is the already-known cubic for \(Q\).
All blocks between \(000\) and a different color vanish automatically,
because \(W^{\otimes3}\) is reducing.  The unresolved information lies
in the remaining \(49\) complement-to-complement blocks.  In particular,
the equations containing \(X\) and \(Y\) are coupled to \(A,B,C,Z\);
none isolates \(X^*X+Y^*Y\) as a positive term.  Treating one of them
as a linear leakage equation would discard genuine cubic paths.

## 5. Correction to the earlier numerical interpretation

The archived runs described in Section 4 of
`notes/one_sided_square_invariance_audit.md` used the
`one_sided_4plus2` label in `scripts/d6_riemannian_search.py`.
That label creates two invariant matrix blocks of sizes \(16\) and \(20\),
and `h4_block` inserts the published matrix at initialization.

However, the old tangent projection permits Grassmann motion in **both**
blocks.  Thus those runs did not freeze the published restriction.
They searched the broader family
\[
\text{\(WW\) remains reducing with signature \((8,8)\),}
\tag{24}
\]
while its internal reflection was allowed to move away from the
published exceptional matrix.

The old raw files remain valid records of that broader failed search and
have not been altered.  Their residuals must not be cited as results for
the fixed-extension problem.  The new archive verifier demonstrates the
scope issue directly by constructing a nonzero old tangent supported
entirely inside the \(WW\) block.

## 6. Dedicated frozen-\(Q\) search

The new program
`scripts/d6_one_sided_fixed_h4_search.py` parametrizes only a
signature-\((10,10)\) Hermitian involution on the full \(20\)-dimensional
complement.  Every iterate has the exact block form
\[
H=H_4\oplus H_{20},
\tag{25}
\]
so the published \(H_4\) is immutable.  The cells in (2) are not
preserved separately.

The analytic Grassmann gradient was checked by independent central
differences.  At step \(10^{-4}\), the two audited errors were below
\[
6.4\times10^{-9}.
\tag{26}
\]
Every final state records
\[
\|H|_{WW}-H_4\|_{\mathrm F}=0
\tag{27}
\]
exactly at floating-point storage level.

The predeclared production archive contains:

- six unrestricted complex runs;
- one complex run starting from the exact two-site leakage model;
- three complex runs with partial-trace penalty \(10\);
- two real runs;
- three complex runs with a penalty targeting
  \(\delta=1/4\).

Thus there are \(15\) frozen-\(Q\) runs.  No candidate met the
predeclared residual threshold \(10^{-6}\).  The best ordinary cubic
residual was
\[
\boxed{6.011210894660647.}
\tag{28}
\]
All six unpenalized complex random runs converged to
\[
\delta<10^{-12},
\tag{29}
\]
although their cubic residuals remained nonzero.  This is an optimizer
observation, not a proof that the exact cubic forces \(\delta=0\).

The leakage-target search minimizes
\[
\|\mathcal D\|_{\mathrm F}^2
+1000(\delta-\tfrac14)^2.
\tag{30}
\]
It was separately gradient-checked.  Its three final states retained
\[
\delta>0.17,
\tag{31}
\]
but the smallest cubic residual was still
\[
\boxed{6.284217255318515.}
\tag{32}
\]
Starting from the exact two-site leakage model led instead to a
nonzero-leakage stationary point with
\[
\delta=0.4094493658\ldots,\qquad
\|\mathcal D\|_{\mathrm F}=15.5154527934\ldots.
\tag{33}
\]

None of (28)--(33) is a lower bound.  A small numerical residual would
also not count without exact reconstruction.

## 7. What has and has not been resolved

The exact reduction has closed the bookkeeping gap:

\[
\boxed{
\text{A fixed-\(Q\) extension exists}
\iff
\text{(8), (13)--(16), and all equations (22) admit a solution.}
}
\tag{34}
\]
The forward implication uses automatic standardness.  Conversely, the
block projection, Hermiticity, rank, marginals, and cubic reconstruct an
exceptional \(d=6\) projection with the required fixed restriction.

What remains missing is an exact elimination of the \(49\)
complement-to-complement cubic blocks.  Two outcomes are still possible:

1. those equations force \(X=Y=0\), after which the known \(d=2\)
   obstruction excludes the extension;
2. a genuinely leaking solution exists but lies outside every numerical
   basin reached here.

The numerical tendency toward (29) makes the first possibility a useful
proof target, but it is not mathematical evidence strong enough to choose
between them.

## 8. Reproducibility

Exact block replay:

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_one_sided_fixed_h4_color_blocks.py
```

Numerical archive and gradient audit:

```text
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 \
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_d6_fixed_h4_search_archive.py
```

The seed and command manifest is
`results/d6_fixed_h4_seed_manifest.json`.  Raw JSONL output is retained
in the five `results/d6_fixed_h4_*runs.jsonl` files.  Both search programs
record their source hashes, seeds, dependency versions, platform,
timestamps, fixed-block error, involution error, residual, partial traces,
and leakage defect.

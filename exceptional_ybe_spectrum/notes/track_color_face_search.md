# Track B2: canonical-channel colors and operator-valued face search

**Date:** 2026-07-28
**Status:** exact reduced equations and exact \(d=4\) calibration family;
reproducible negative numerical evidence at \(d=6\), not a nonexistence proof

## Executive conclusion

The independent unconstrained \(d=4\) point contains a genuine color/face
signature, but it is more specific than the initial description suggested.
For
\[
P=\frac{I-H}{2},
\]
the two canonical bistochastic maps
\[
\Phi_1(x)=\frac2d\operatorname{Tr}_2\!\bigl(P(x\otimes I)P\bigr),
\qquad
\Phi_2(x)=\frac2d\operatorname{Tr}_1\!\bigl(P(I\otimes x)P\bigr)
\tag{1}
\]
each have a two-dimensional fixed algebra.  Their nontrivial fixed
reflections have \(2+2\) spectra and commute with \(P\) on the corresponding
leg.

For the saved point, however, the two local reflections also commute with
**each other**.  Their four joint intersections are one-dimensional.  Thus
the numerical point is naturally an operator-valued crossed face model
\[
V=A\otimes B,\qquad \dim A=\dim B=2,
\]
not a model in which the two rank-two decompositions are related by a scalar
\(2\times2\) mixing matrix tensored with an untouched internal qubit.

I pursued both generalizations to \(d=6\):

1. the requested three-color model with three rank-two sectors on both
   sides, related by \(U\otimes I_2\), \(U\in U(3)\);
2. the more literal crossed-factor generalization
   \(V=\mathbb C^3\otimes\mathbb C^2\), with arbitrary operator-valued face
   blocks.

Both searches were calibrated successfully at \(d=4\).  In fact, the first
calibration exposed an exact symbolic one-parameter \(d=4\) family.  Across
39 reproducible complex \(d=6\) runs, no residual approached zero.  The best
Frobenius residual was
\[
4.958747221723511.
\]
This is useful falsifier evidence against these two mechanisms, but it is
not a theorem about either ansatz and says nothing by itself about arbitrary
\(d=6\) solutions.

## 1. Why fixed reflections commute with \(P\)

Suppose the partial traces make (1) unital, and let \(z=z^*=z^{-1}\) be
fixed by \(\Phi_1\).  Put \(Z=z\otimes I\).  Then
\[
\operatorname{Tr}(z\Phi_1(z))
=\frac2d\operatorname{Tr}(ZPZP)
=\operatorname{Tr}(I_d)=d.
\]
Since \(\operatorname{Tr}P=d^2/2\), this gives
\[
\operatorname{Tr}(ZPZP)=\operatorname{Tr}P.
\]
Direct expansion now yields
\[
\lVert[P,Z]\rVert_2^2
=2\operatorname{Tr}P-2\operatorname{Tr}(ZPZP)=0.
\]
Hence
\[
[P,z\otimes I]=0.
\tag{2}
\]
The same argument applies to a fixed reflection of \(\Phi_2\).

This is also the multiplicative-domain argument for a fixed unitary of a
bistochastic channel, written in a form that makes the implication (2)
explicit.

## 2. Numerical extraction from the saved \(d=4\) point

The input was

```text
results/d6_candidates/d4_complex_none_random_seed26072804.npz
```

and the analysis is replayed by

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/color_face_d4_analyze.py \
  results/d6_candidates/d4_complex_none_random_seed26072804.npz \
  --output results/color_face_d4_analysis_seed26072804.json
```

The diagnostics are:

\[
\begin{array}{c|c}
\text{quantity}&\text{value}\\ \hline
\text{cubic residual}&8.7324\times10^{-11}\\
\lVert[P,z_1\otimes I]\rVert_F&1.7135\times10^{-11}\\
\lVert[P,I\otimes z_2]\rVert_F&5.0479\times10^{-11}\\
\lVert[z_1,z_2]\rVert_F&6.6299\times10^{-13}\\
\text{face off-block norm}&2.5245\times10^{-11}
\end{array}
\]

Each \(z_i\) has eigenvalues
\[
-1,-1,+1,+1
\]
to error below \(2\times10^{-13}\).  For every pair of negative/positive
eigenspaces \(L_a,R_b\), the compression
\[
L_aR_bL_a
\]
has numerical spectrum \(\{0,1\}\).  Thus every intersection
\[
L_a\cap R_b
\]
is one-dimensional.  In their common eigenbasis, \(P\) splits into four
\(4\times4\) blocks, and every block is a rank-two projection to errors of
order \(10^{-15}\).

These statements are numerical because the unconstrained point itself is
numerical.  They motivate the exact ansatz below; they do not recognize that
specific point algebraically.

## 3. Exact reduced equation: equal-size mixed colors

Let
\[
V=\mathbb C^c\otimes K,\qquad \dim K=r,
\]
and let \(U\in U(c)\), with columns \(u_b\).  On the first leg use the color
projections
\[
L_a=|a\rangle\langle a|\otimes I_K,
\]
and on the second leg use
\[
R_b=|u_b\rangle\langle u_b|\otimes I_K.
\]
Choose trace-zero Hermitian involutions
\[
K_{ab}\in\operatorname{End}(K\otimes K).
\]
There is a unique pair operator \(H\) which, in the mixed
\(L_a\)-on-the-first-leg and \(R_b\)-on-the-second-leg basis, is the direct
sum of the blocks \(K_{ab}\).  It is automatically Hermitian, traceless, and
an involution.

Fix the first site's left color \(a\) and the third site's right color \(d\).
On
\[
\mathbb C^c_{\mathrm{middle\ color}}\otimes K^{\otimes3}
\]
define
\[
X_a=\sum_b |u_b\rangle\langle u_b|\otimes K_{ab}^{12},
\qquad
Y_d=\sum_e |e\rangle\langle e|\otimes K_{ed}^{23}.
\tag{3}
\]
The full three-site cubic relation is equivalent to the \(c^2\) equations
\[
\boxed{
X_aY_dX_a-Y_dX_aY_d=\frac13(X_a-Y_d)
}
\qquad(a,d=0,\ldots,c-1).
\tag{4}
\]
This is the precise reduced system used in the `mixed` searches.  For
\(c=3,r=2\), it has nine arbitrary signature-\((2,2)\) reflection blocks
and a \(3\times3\) mixing unitary.

In the color basis of the \(u_b\), the \((b,b')\) matrix element of (4) can
also be printed without any large matrices:
\[
\begin{aligned}
&\sum_e\overline{U_{eb}}U_{eb'}\,
 K_{ab}^{12}K_{ed}^{23}K_{ab'}^{12}\\
&\quad-\sum_{e,e',f}
 \overline{U_{eb}}U_{ef}\overline{U_{e'f}}U_{e'b'}\,
 K_{ed}^{23}K_{af}^{12}K_{e'd}^{23}\\
&=\frac13\left(
\delta_{bb'}K_{ab}^{12}
-\sum_e\overline{U_{eb}}U_{eb'}K_{ed}^{23}
\right).
\end{aligned}
\tag{5}
\]

## 4. Exact reduced equation: crossed factors

Let
\[
V=A\otimes B,\qquad \dim A=a,\quad\dim B=b.
\]
Use the \(A\)-coordinate of the first site as a left color and the
\(B\)-coordinate of the second site as a right color.  For every
\((\alpha,\beta)\), choose a trace-zero Hermitian involution
\[
K_{\alpha\beta}\in
\operatorname{End}(B_{\mathrm{first}}\otimes A_{\mathrm{second}})
\cong M_{ab}(\mathbb C).
\]
The direct sum over the outer colors defines \(H\).

On three sites, fix \(A_1=\alpha\) and \(B_3=\beta\).  The two reflections
then act on
\[
B_1\otimes A_2\otimes B_2\otimes A_3
\]
by
\[
X_\alpha
=\sum_{\gamma=0}^{b-1}
K_{\alpha\gamma}^{B_1A_2}
\otimes|\gamma\rangle\langle\gamma|_{B_2}\otimes I_{A_3},
\tag{6}
\]
\[
Y_\beta
=\sum_{\delta=0}^{a-1}
I_{B_1}\otimes|\delta\rangle\langle\delta|_{A_2}
\otimes K_{\delta\beta}^{B_2A_3}.
\tag{7}
\]
Again the full equation is equivalent to
\[
\boxed{
X_\alpha Y_\beta X_\alpha-Y_\beta X_\alpha Y_\beta
=\frac13(X_\alpha-Y_\beta)
}
\tag{8}
\]
for all outer colors.

The extracted \(d=4\) point has \(a=b=2\).  The \(d=6\) searches used both
\((a,b)=(3,2)\) and \((2,3)\), with six completely unrestricted
signature-\((3,3)\) blocks in \(M_6(\mathbb C)\).

## 5. Exact \(d=4\) calibration family

The mixed ansatz contains the following exact family.  Let \(F\) be the
\(2\times2\) Hadamard matrix and take real \(s,t\) satisfying
\[
s^2+2t^2=1.
\tag{9}
\]
Define
\[
B_0=X,\qquad B_1=-Y,
\]
\[
C_0=-tX-tY-sZ,\qquad C_1=-tX-tY+sZ,
\]
and
\[
\boxed{
K_{ab}
=\frac{(-1)^{a+b}}{\sqrt3}Z\otimes I
+\sqrt{\frac23}\,B_{a+b\ {\rm mod}\ 2}\otimes C_b.
}
\tag{10}
\]
Use \(U=F\) in the mixed construction.

Equation (9) makes \(C_0,C_1\) reflections.  Since \(Z\) anticommutes with
\(B_0,B_1\), every \(K_{ab}\) is a trace-zero Hermitian involution.  More
strongly, exact symbolic expansion shows that every entry of both
\[
H^2-I
\]
and
\[
H_1H_2H_1-H_2H_1H_2-\frac13(H_1-H_2)
\]
is divisible by \(s^2+2t^2-1\).  The independent exact replay is

```text
/Users/alec/Documents/Math/.venv/bin/python \
  scripts/verify_color_face_d4_family.py
```

with retained output in
`results/color_face_d4_family_exact.txt`.

This exact family validates the reduced equations and the implementation.
Its equivalence classes, relation to the published sparse point, and
novelty have not been audited.  It should not yet be advertised as a new
classification result.

## 6. Numerical \(d=6\) experiments

All runs used complex Hermitian reflection blocks, exact signature at every
iterate up to roundoff, analytic pullback gradients, deterministic seeds,
and Armijo-style backtracking.  A separate finite-difference check validates
both the block and mixing-unitary gradients; see
`results/color_face_gradient_check.txt`.
Candidate filenames are deterministic in the model and seed.  The search
script refuses to overwrite an existing candidate and emits a
`candidate_not_saved_existing` event instead.

\[
\begin{array}{l|r|r}
\text{model}&\text{runs}&\text{best residual}\\ \hline
\text{crossed }3\times2&9&8.496600768684832\\
\text{crossed }2\times3&5&11.048696098612051\\
\text{mixed }3\times2,\ U\text{ optimized}&10&6.000000000000003\\
\text{mixed }3\times2,\ U=F_3&10&4.958747221723511\\
\text{mixed, embedded exact }d=4\text{ seed}&5&6.014459182988110
\end{array}
\]

The optimized-\(U\) runs often drove \(U\) to a permutation matrix and
landed at residual \(6\).  Fixing \(U=F_3\) prevented that collapse and gave
the best value, but still nowhere near a candidate.  The exact \(d=4\)
calibrations reached residuals below \(1.1\times10^{-10}\), so the same code
does find true solutions when they lie in the tested landscape.

The retained logs are:

```text
results/color_face_d6_crossed_runs.jsonl
results/color_face_d6_crossed_2x3_runs.jsonl
results/color_face_d6_mixed_runs.jsonl
results/color_face_d6_mixed_fourier_runs.jsonl
results/color_face_d6_mixed_embed_d4_runs.jsonl
```

## 7. Scope and next deductions

What is proved:

1. equations (4), (5), and (8) are exact reductions of their stated
   ansätze;
2. the family (9)--(10) is an exact \(d=4\) exceptional family;
3. the canonical-channel fixed reflections of the saved numerical point
   produce the reported crossed face blocks to the recorded precision.

What is not proved:

1. the saved unconstrained \(d=4\) point has not been recognized as an exact
   algebraic matrix;
2. neither \(d=6\) ansatz has been exhaustively classified;
3. nonzero numerical minima do not prove nonexistence even inside an ansatz;
4. the mixed ansatz restricts the relative rank-two decompositions to
   \(U\otimes I_2\), not an arbitrary unitary in \(U(6)\);
5. neither ansatz covers arbitrary exceptional matrices.

The most promising exact follow-up is to substitute the four-term
two-qubit normal form suggested by (10) into the \(c=3\) equations (5).
The \(c=2\) solution uses the three mutually orthogonal Pauli axes
\[
Z,\quad X,\quad -Y.
\]
Determining whether the \(c=3\) equations demand a fourth anticommuting
qubit reflection would turn the numerical failure into a clean exact no-go
for this broad low-operator-Schmidt-rank branch.  That would still be an
ansatz theorem, not the desired unrestricted four-divisibility result.

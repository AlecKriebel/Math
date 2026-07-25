# Exact edge-conditioned obstruction to the degree-four witness

## Theorem and scope

Let
\[
S=\left\{-\frac{77}{100},-\frac7{10},-\frac{11}{25},
          -\frac9{100},\frac{499}{1000}\right\}.
\]
There is no 41-point kissing code whose ordered pair counts and unordered
triangle counts are those in
`local_hybrid_degree4_rank_color_clique_pseudodistribution.json`.
In fact, those data have no nonnegative Gram-PSD colored-\(K_4\) orbit
extension satisfying even the diagonal coordinate inequalities of the
edge-conditioned degree covariance matrices.

This refutes one particular pseudodistribution.  It does not exclude all
pair/triple data on \(S\), and it does not prove a global kissing-number
upper bound.

The exact enumeration metadata are in
`certificates/edge_conditioned_k4_exact_obstruction.json`.  The
standard-library verifier
`verifiers/verify_edge_conditioned_k4_exact_obstruction.py` reconstructs
all objects rather than trusting the exploratory LP.

## A short universal common-neighbor lemma

**Lemma.**  Let \(y,z\in S^4\) satisfy
\[
\langle y,z\rangle\leq-\frac{11}{25}.
\]
There is at most one code point \(x\) satisfying
\[
\langle x,y\rangle,\langle x,z\rangle
\geq\frac{499}{1000}.                                \tag{1}
\]

**Proof.**  Put \(q=\langle y,z\rangle\).  If \(q=-1\), then \(z=-y\),
and the two inequalities (1) are already impossible after adding them.
Assume \(q>-1\), and set
\[
u=\frac{y+z}{\sqrt{2+2q}}.
\]
Every point satisfying (1) has height
\[
\langle x,u\rangle
\geq\frac{2(499/1000)}{\sqrt{2+2q}},
\]
whose square is at least
\[
p=\frac{2(499/1000)^2}{1-11/25}
=\frac{249001}{280000}>\frac12.                    \tag{2}
\]

If \(x,w\) were two such points, decompose them into their \(u\)-components
and orthogonal components.  For heights \(a,b\geq\sqrt p\),
\[
\begin{aligned}
\langle x,w\rangle
&\geq ab-\sqrt{1-a^2}\sqrt{1-b^2}\\
&\geq 2p-1
=\frac{109001}{140000}
=\frac12+\frac{39001}{140000}>\frac12.             \tag{3}
\end{aligned}
\]
The second inequality follows because the preceding expression is
increasing separately in \(a,b\in[\sqrt p,1]\).  Equation (3) contradicts
the non-strict kissing constraint. \(\square\)

Consequently, if \(B\) is the set of unordered code pairs with inner
product at most \(-11/25\), then
\[
\#\{(\{y,z\},x):\{y,z\}\in B,\
 \langle x,y\rangle,\langle x,z\rangle\geq499/1000\}
\leq |B|.                                             \tag{4}
\]
All inequalities include their boundary values.

For the stored witness, colors \(0,1,2\) are precisely the base colors in
(4), and color \(4\) is precisely the high color.  Thus (4) requires
\[
n_{044}+n_{144}+n_{244}\leq E_0+E_1+E_2.             \tag{5}
\]
But its two sides are
\[
0+0+243=243,\qquad 85+3+131=219.
\]
The exact violation is \(24\).  Even the color-2 part alone demands
\(n_{244}\leq E_2\), while \(243>131\).

## The edge-conditioned covariance interpretation

For an edge \(e=\{y,z\}\) of color \(c\), let \(n_e(a,b)\) count third
vertices \(x\) for which the two incident colors, sorted, are \((a,b)\).
For fixed \(c\), the vectors \(n_e\in\mathbb R^{15}\) obey
\[
\sum_{e:\,\operatorname{col}(e)=c}
n_en_e^{\mathsf T}
-\frac1{E_c}
\left(\sum_e n_e\right)
\left(\sum_e n_e\right)^{\mathsf T}\succeq0.          \tag{6}
\]
This is simply a centered covariance matrix.

At \(c=2\) and coordinate \((4,4)\), the first moment is
\[
\sum_en_e(4,4)=n_{244}=243.                           \tag{7}
\]
The lemma says \(n_e(4,4)\leq1\), so no Gram-PSD colored \(K_4\) can
contain a color-2 anchor edge and two distinct \((4,4)\)-profile vertices.
Hence the distinct-vertex part of the diagonal second moment is zero.
The corresponding diagonal entry of (6) is exactly
\[
243-\frac{243^2}{131}
=-\frac{27216}{131}<0.                                \tag{8}
\]
This is the one-row exact Farkas contradiction found numerically.

## Exact \(K_4\)-orbit audit

A labeled colored \(K_4\) is encoded by its six edge colors in the order
\[
01,02,03,12,13,23.
\]
The verifier checks all \(5^6\) patterns.  A pattern is retained exactly
when every \(3\times3\) face Gram matrix is PSD and its full \(4\times4\)
Gram determinant is nonnegative.  These conditions check every principal
minor, hence are equivalent to Gram PSD.  The comparisons use `>= 0`, so
determinant-zero boundary patterns would be retained.

The result is 3,213 labeled feasible patterns in 198 vertex-permutation
orbits.  Their orbit-size distribution is
\[
\begin{array}{c|rrrrrr}
\text{orbit size}&1&3&4&6&12&24\\
\text{number}&2&7&7&17&75&90.
\end{array}
\]
There happen to be no determinant-zero retained triangle or \(K_4\) types
on this particular support, but the enumeration does not assume strict
positivity.

An orbit variable \(y_R\) counts unordered four-vertex sets of type \(R\).
Therefore its face coefficient is simply the number, from zero to four, of
its faces of each triangle type.  Every unordered triangle lies in exactly
\(41-3=38\) four-vertex sets, giving
\[
\sum_R f_T(R)y_R=38n_T.                               \tag{9}
\]
No orbit-size or stabilizer factor belongs in (9).  The verifier confirms
this convention by reconstructing all labeled orbit sizes and by checking
that every column of the face-incidence matrix sums to four.

For (6), each anchor edge of a \(K_4\) has two remaining vertices.  If their
profiles are distinct, that \(K_4\) contributes one to each symmetric
off-diagonal entry; if they agree, it contributes two to the corresponding
diagonal entry, accounting for the two ordered distinct vertices.  This
coefficient is invariant across every labeled representative of an orbit,
so again no stabilizer averaging is needed.

The verifier rebuilds:

- all 21 feasible triangle types;
- all 198 Gram-PSD \(K_4\) orbits;
- the complete \(21\times198\) face-incidence matrix and its targets;
- all five \(15\times15\) edge-conditioned covariance affine matrices; and
- all 75 coordinate diagonal rows.

For the special color-2, profile-\((4,4)\) row, every one of the 198
distinct-vertex coefficients is exactly zero, while the constant is the
negative rational (8).  Giving this inequality multiplier \(1\), with all
other inequality and face-equation multipliers zero, is an exact Farkas
ray.  Thus the four-point relaxation is infeasible independently of any
floating-point solver status.

The proof dependency is
\[
\text{projection lemma}\Longrightarrow\text{counting cut (5)}
\Longrightarrow\text{nonrealizability},
\]
with the separate machine audit
\[
\text{exact orbit enumeration}\Longrightarrow
\text{covariance row (8)}\Longrightarrow
\text{one-row Farkas contradiction}.
\]

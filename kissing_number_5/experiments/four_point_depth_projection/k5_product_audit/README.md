# K5 semantics of the edge-conditioned depth/common product

## Result

The exact 51-atom local Gram-PSD `K5` extension does encode the
four-distinct-point statistic needed by the depth/common-capacity product
inequality.  When it is decoded with the correct without-replacement
normalization, it violates two necessary exact-base-stratum rows:

\[
(q,b,M)=(-1/2,1/2,1),\qquad
(q,b,M)=(-1/4,1/2,3).
\]

In the convention “left side minus right side must be nonpositive,” the
two exact scaled residuals are

\[
\frac{7819447598603429}{228000000000000}>0
\]

and

\[
\frac{
1222373249978570665696597731104959481
}{
81785237862093261678000000000000000
}>0,
\]

respectively.

Thus this particular symmetric local `K5` extension is not the uniform
five-subset marginal of any 41-point code satisfying robust
\(\pm1/300\) depth and the proved common-pair capacities.  This does not
show that no other `K5` extension of the same pair/triple
pseudodistribution exists.

That distinction is decisive: a second marginal LP produced an exact
64-atom symmetric local Gram-PSD `K5` extension with the same pair/triple
marginals that satisfies **all 560 distinct averaged product rows** on the
quarter support.  These comprise every direction
\(\lambda y+\mu z\), both strict tails and algebraic boundaries, and all
seven applicable common-pair capacity families.  The exact certificate is
`centered_quarter_k5_product_extension.json`; its independent verifier is
`verify_product_extension_independent.py`.  It finds 89 equality rows; the
smallest strictly positive twice-symmetrized slack is
\[
\frac{8096793946939774078089812119067413501}
     {27983771922390159676600800000000000000}>0.
\]

Hence the product inequalities reject the stored sparse extension but do
not obstruct local `K5` extension of the centered pair/triple witness.

The audit pins these inputs:

- `centered_quarter_bv_pseudodistribution.json`, SHA-256
  `112be681b4fb98dcfb8af29d08be78bfecfde7088154429fba76774d4c57d550`;
- `centered_quarter_k5_extension.json`, SHA-256
  `133e8b502653b3bb1e1c4c3eb6c0452705020f65128959dc9d0cb34a8c0645ef`.

## What a stored atom means

Choose a stored labeled representative \(A\) with probability \(w_A\),
then apply a uniform permutation in \(S_5\).  This gives a symmetric
distribution.  There is no orbit-size multiplier: sampling a uniform
permutation is valid even when a representative has automorphisms.

For a base edge \(e=\{y,z\}\) of an atom, let the other three vertices be
the sampled residual set.  Write

\[
\begin{aligned}
h_e&=\#\{x:\langle x,y\rangle+\langle x,z\rangle
 <-\delta\sqrt{2+2q_e}\},\\
g_e&=\#\{w:\langle w,y\rangle\ge b,\
                 \langle w,z\rangle\ge b\},
\end{aligned}
\qquad \delta=1/300.
\]

Because \(b>0\), the two sets are disjoint.  Hence \(h_eg_e\) counts
ordered pairs of distinct residual vertices \((x,w)\).  All three
quantities are summed over the ten base edges of the representative.
Those sums are invariant under relabeling, which the verifier also checks
over all \(120\) permutations.

The certificate's familiar marginal normalizations follow from the same
uniform-five-subset interpretation.  For \(N=41\),

\[
\mathbb E[\#\hbox{ edges of color }q\hbox{ in }K_5]
=\frac{\alpha_q}{4},
\]

and the expected number of faces of triangle type \(T\) is
\(\nu_T/156\).  Dividing by ten gives the uniform edge and face
probabilities \(\alpha_q/40\) and \(\nu_T/1560\).

## Exact without-replacement normalization

Fix a global base edge.  A uniform five-subset containing it selects
three of its \(39=N-2\) residual vertices.  If the global edge counts are
\(H_e,\Gamma_e\), then

\[
\mathbb E[h_e\mid e]=\frac3{39}H_e=\frac{H_e}{13},
\qquad
\mathbb E[g_e\mid e]=\frac{\Gamma_e}{13}.
\]

Each ordered pair of distinct residual vertices is retained with
probability

\[
\frac{(3)_2}{(39)_2}=\frac1{247}.
\]

Disjointness therefore gives

\[
\mathbb E[h_eg_e\mid e]=\frac{H_e\Gamma_e}{247}.       \tag{1}
\]

The pointwise inequality

\[
H_e\Gamma_e\le M_eH_e+7\Gamma_e-7M_e
\]

thus becomes the following linear condition on any symmetric `K5`
marginal:

\[
\boxed{\;
\sum_Aw_A\sum_e
\bigl(247h_e g_e-13M_eh_e-91g_e+7M_e\bigr)\le0.
\;}                                                   \tag{2}
\]

The sum may be restricted to one exact base color or any collection of
base edges on which the stated capacity \(M_e\) is valid.

Equivalently, if \(B,H,G,P\) denote the weighted atom totals of,
respectively, base edges, sampled depth incidences, sampled common
incidences, and sampled ordered depth/common pairs in a fixed stratum,
then

\[
\bar H=13H/B,\qquad
\bar\Gamma=13G/B,\qquad
\overline{H\Gamma}=247P/B,
\]

and (2) is

\[
\overline{H\Gamma}
\le M\bar H+7\bar\Gamma-7M.
\]

For comparison, direct subset counting gives

\[
\mathbb E\sum_e h_e=\frac1{1066}\sum_eH_e,\quad
\mathbb E\sum_e h_eg_e=\frac1{20254}\sum_eH_e\Gamma_e,\quad
\mathbb E\sum_e M_e=\frac1{82}\sum_eM_e.
\]

Multiplication by \(20254=82\cdot247\) gives exactly (2).

## General half-planes and the diagonal correction

For an arbitrary nonzero direction \(\lambda y+\mu z\), put
\[
L^2=\lambda^2+\mu^2+2q\lambda\mu
\]
and let \(H_e\) count third points satisfying
\[
\lambda\langle x,y\rangle+\mu\langle x,z\rangle
>\frac{L}{300}.
\]
After deleting the two base endpoints, robust depth gives
\[
r=7-\mathbf1_{\{\lambda+\mu q>L/300\}}
    -\mathbf1_{\{\lambda q+\mu>L/300\}}.
\]
Now \(H_e\) may overlap the common neighborhood.  For the full code write
\[
I_e=|H_e\cap\Gamma_e|,\qquad
C_e=H_e\Gamma_e-I_e,
\]
so \(C_e\) counts ordered pairs of distinct third points.  In a uniform
five-subset let \(i_e\) and \(c_e\) be the sampled intersection and
sampled distinct-pair counts.  Then
\[
\mathbb E[i_e\mid e]=\frac{I_e}{13},\qquad
\mathbb E[c_e\mid e]=\frac{C_e}{247}.
\]
Therefore the fully general symmetrized `K5` row is
\[
\boxed{\;
247c+13i\le13Mh+13r g-rME.
\;}                                                   \tag{3}
\]
Equivalently, because \(hg=c+i\),
\[
247hg-234i\le13Mh+13rg-rME.                          \tag{4}
\]
The negative \(y+z\) row in (2) is the disjoint special case \(I=0,r=7\).

On the finite quarter support, membership changes only at exact quadratic
critical slopes.  After duplicate half-plane states are merged, the seven
capacity families contain
\[
62,\ 62,\ 80,\ 88,\ 92,\ 92,\ 84
\]
states, respectively, for 560 rows in total.  The alternative extension
passes all of them exactly; some rows are attained with equality.

## Boundary conventions

The tail inequality is strict.  The verifier evaluates it without square
roots:

\[
s<-\delta\sqrt{2+2q}
\iff s<0\ \hbox{ and }\ s^2>\delta^2(2+2q).
\]

Equality is excluded.  On the quarter grid and \(q>-1\), this is simply
\(s<0\), since \(s\) is a multiple of \(1/4\) while
\(\delta\sqrt{2+2q}\le\sqrt3/300<1/4\).

The common-neighbor inequalities use `>=`, so threshold equality is
included.  In particular \(q=-1/4,b=1/2\) gives \(p=2/3\) and capacity
three, not two.  The antipodal base \(q=-1\) is excluded from the product
row because \(y+z=0\), although its common-neighbor capacity alone is
zero.

For the two positive support thresholds, the strongest distinct
quarter-grid rows are:

\[
\begin{array}{c|c|c}
b&q&M\\\hline
1/4&-3/4&6\\
1/2&-3/4&0\\
1/2&-1/2&1\\
1/2&-1/4&3\\
1/2&0&6\\
1/2&1/4&7\\
1/2&1/2&7.
\end{array}
\]

The last two use the separately proved positive-base common-contact cap.

## Scope

This audit proves that the stored extension fails (2), not that the
pair/triple pseudodistribution has no admissible `K5` extension.  The
stored LP matched only edge and triangular-face marginals; it never
imposed (2).

The alternative certificate answers the local marginal-LP question:
the polytope remains feasible even after every row (3) is imposed.  It is
still only a probability measure on locally Gram-PSD colored `K5` atoms.
It does not provide:

- one global 41-point Gram matrix;
- consistency of overlapping labeled five-subsets from a common source;
- a five-point Lasserre/moment-matrix PSD certificate; or
- any global rank-at-most-five realization.

Local `K5` consistency and global/Lasserre consistency must therefore not
be conflated.

## Reproduction

The discovery script `search_alternative_extension.py` used NumPy 2.5.1,
SciPy 1.18.0, and the existing 105,930-column local-`K5` enumeration.  It
is not trusted by either exact verifier.

From the repository root:

```sh
PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k5_product_audit/verify.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k5_product_audit.test_verify -v

PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k5_product_audit/verify_alternative_extension.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k5_product_audit.test_alternative_extension \
  -v

PYTHONPATH=. /usr/bin/python3 \
  experiments/four_point_depth_projection/k5_product_audit/verify_product_extension_independent.py

PYTHONPATH=. /usr/bin/python3 -m unittest \
  experiments.four_point_depth_projection.k5_product_audit.test_verify_product_extension_independent \
  -v
```

The independently implemented full-orbit audit and its pinned result are
`verify_centered_quarter_k5_product.py` and
`centered_quarter_k5_product_audit.json`.  The much smaller
`verify_two_violations_independent.py` recomputes only the two decisive
positive residuals.

# Degree-three fixed-marginal discovery: the leading negative sectors extend

## Status

This note records a **numerical discovery-layer** result.  It does not give
an exact rational degree-three moment and it does not prove physical DTH.

The committed exact five-replica pseudomoment was tested for a positive
degree-three Grassmann extension, first on its most negative (444) block
and then on one common collection containing

\[
444,qquad333,qquad433,qquad343,qquad334.
\]

Both tests are strictly feasible numerically.  In particular, the five
blocks above are reproduced by **one shared source moment**; they were not
extended independently.

The discovery scripts are

* `discovery/agent_dth_level2_444_extension.py`;
* `discovery/agent_dth_level2_joint_extension.py`; and
* `discovery/agent_dth_level2_negative_extension.py`.

They use NumPy/SciPy from the project virtual environment.  Exact source
census and exact contraction normalization remain in the independent
verifiers recorded in the companion notes.

## 1. Compression used by the numerical test

At one site, use Young orthogonal bases of the (S_7) Specht modules.  With
the final vector placed in slot 5, the three bivector pairs occupy

\[
(1,2),\quad(3,4),\quad(6,7).
\]

Let (P_{\rm wr}) antisymmetrize each pair and symmetrize the three pairs.
On this wreath-isotypic space,

\[
\operatorname{Sym}^3(\wedge^2)
=S_{(3,3)}\oplus S_{(2,2,1,1)}\oplus S_{(1^6)}.
\]

If

\[
Z=\sum_{1\le i<j\le6}(ij),
\]

then its eigenvalues on the three displayed summands are (3,-5,-15).
Thus the exact orthogonal degree-three Grassmann projector is represented
numerically as

\[
\boxed{
P_{(3,3)}
=P_{\rm wr}\frac{(Z+5I)(Z+15I)}{144}.
}
\tag{1}
\]

The prolonged Omega kernel is removed using the product of the three local
antisymmetrizers on the deleted bivector pair and the final vector.  Its
rank in every block is checked against the exact character census.

For a five-replica local shape triple (kappa) and a seven-replica source
triple (Lambda), the restriction

\[
[\Lambda]\downarrow S_5\times S_2
\]

is resolved into horizontal and vertical two-strip channels.  Only channel
triples with an odd number of vertical strips contribute, because the traced
global pair is antisymmetric.  If (J_{b,p}) is the corresponding branch
embedding and (K_b) is the post-Omega source basis, the adjoint marginal
has Kraus compression

\[
L_b(Y)=
K_b^*\left(
\sum_{p\text{ odd vertical}}J_{b,p}YJ_{b,p}^*
\right)K_b.
\tag{2}
\]

Only the span of the projected branch ranges is retained.  This loses
nothing for a target marginal: a positive source block can be compressed to
that span without changing (2).

The carrier normalization for an ordered source (b) and target (kappa)
is

\[
\frac{
\prod_i\dim S_{\Lambda_i}\mathbb C^3
}{
\prod_i\dim S_{\kappa_i}\mathbb C^3
}.
\tag{3}
\]

Formula (3) agrees with the exact diagram-deletion adjoint and preserves the
physical monomial normalization.

## 2. The isolated (444) marginal

The exact reachability census gives 23 post-Omega source blocks.  After the
lossless marginal-range compression, their total PSD rank is only 315 and
their real-symmetric coordinate count is 2770.

The target has dimension ten.  The affine normal operator on its 55
symmetric coordinates is full rank, with numerical spectrum

\[
[406.1318706858,\ 477.5269472524].
\]

The minimum-norm affine solution is already positive definite:

\[
\begin{aligned}
\|\mathcal M(T)-R_{444}\|_F&=4.04\times10^{-21},\\
\min_b\lambda_{\min}(T_b)&=1.03\times10^{-12}.
\end{aligned}
\tag{4}
\]

Thus the worst-ratio block of the five-replica obstruction does not by itself
give a degree-three extension obstruction.

## 3. One shared extension for (444+333+433)

The ordered target list is

\[
(444),(333),(433),(343),(334).
\]

The common source contains 63 blocks.  Its marginal-relevant total PSD rank
is 3194 and its real-symmetric coordinate count is 111019.  The target has
551 symmetric equations.  The affine normal operator is full rank, with
spectrum

\[
[153.5145259526,\ 483.1835779294].
\tag{5}
\]

To distinguish a true Slater point from a boundary artifact, a common floor
was imposed.  Write

\[
T_b=Z_b+tI_b,
\qquad Z_b\succeq0,
\]

and solve

\[
\mathcal M(Z)=R-t\mathcal M(I).
\]

At

\[
t=10^{-12},
\]

Douglas--Rachford projection gives

\[
\begin{aligned}
\|\mathcal M(Z)-[R-t\mathcal M(I)]\|_F
  &=1.70\times10^{-20},\\
\text{PSD defect}(Z)&=0,\\
\min_b\lambda_{\min}(Z_b)&=2.24\times10^{-18}.
\end{aligned}
\tag{6}
\]

Consequently the reconstructed common moment has numerical block floor

\[
\min_b\lambda_{\min}(T_b)
\ge1.000002\times10^{-12}.
\tag{7}
\]

An independent site-averaged calculation reproduced strict feasibility with
the same (10^{-12}) floor.  Equations (6)--(7) are strong numerical
evidence of a shared interior extension, but remain floating-point evidence.

## 4. Enlarged selected-negative problem

The next single extension target adds every ordered permutation of

\[
(141),\qquad(331),\qquad(321)
\]

to the five core blocks.  Its exact combinatorial/numerical dimensions are

\[
\boxed{
\begin{aligned}
\text{ordered targets}&=17,\\
\text{target symmetric equations}&=1199,\\
\text{candidate source blocks}&=301,\\
\text{marginal-relevant PSD rank}&=12793,\\
\text{marginal-relevant symmetric variables}&=481805.
\end{aligned}}
\tag{8}
\]

The corresponding 12 MB numerical CP-map cache is
`discovery/dth_level2_negative_blocks.pkl`.  It is a disposable discovery
artifact tied to NumPy 2.5 and is not an exact certificate.

The enlarged common problem is also strictly feasible numerically.  Its
affine normal operator has full rank 1199 and spectrum

\[
[81.7702866440,\ 483.3129456523].
\tag{9}
\]

At common floor (t=10^{-13}), the shifted problem converged in 50
over-relaxed iterations to

\[
\begin{aligned}
\text{affine residual}&=1.23\times10^{-20},\\
\text{PSD defect}&=0,\\
\min_b\lambda_{\min}(Z_b)&=1.25\times10^{-15}.
\end{aligned}
\tag{10}
\]

Thus all 17 selected negative-sector outputs share a numerical Slater
extension with minimum block eigenvalue at least

\[
1.0125\times10^{-13}.
\tag{11}
\]

This closes the selected-negative-sector test at discovery precision.

## 5. Complete marginal map

The same generic builder was then run on every active five-replica output
block.  It gives

\[
\boxed{
\begin{aligned}
\text{active ordered outputs}&=118,\\
\text{raw target symmetric equations}&=4139,\\
\text{source blocks}&=487,\\
\text{marginal-relevant PSD rank}&=14511,\\
\text{marginal-relevant symmetric variables}&=519434.
\end{aligned}}
\tag{12}
\]

The last three numbers agree exactly with the independent complete
post-Omega S7 census.  In particular, after all 118 targets are included,
the marginal-relevant compression recovers every post-Omega source direction;
this is a strong independent completeness audit of the branch construction.

The 48 MB disposable map cache is
`discovery/dth_level2_full_blocks.pkl`.  It is intentionally not committed.
Physical-site averaging reduces the 4139 raw target coordinates to the
smaller invariant fixed-marginal decision now being solved independently.

## 6. Consequence and remaining decision

The most negative ratio sectors (444,333,433) do not expose a missing
degree-three Veronese relation: they admit a common numerical Slater
extension.  The larger selected-negative extension (8) is also strictly
feasible numerically.  Consequently no subset chosen merely by negative
objective contribution has exposed the missing rank-one equation.

The next finite decision is the complete site-averaged marginal built in
(12), including positive-objective sectors.  Even a positive answer there
would not yet enforce prolonged mixed support or grouped PPT at degree three.
No claim beyond the numerical marginal statements (4), (6), and (10) is made
here.

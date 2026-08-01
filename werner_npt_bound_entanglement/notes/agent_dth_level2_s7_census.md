# Exact degree-three Grassmann census for the DTH extension

## Scope

This note constructs the representation target for the next DTH moment
level.  It does **not** assert that the committed negative five-replica
pseudomoment extends, or that it does not extend.  It gives an exact finite
block census and isolates the smallest first marginal test.

The seven replicas are arranged as three copies of the bivector and one copy
of the final vector:

\[
 w_{12}\otimes w_{34}\otimes w_{56}\otimes z_7.
\]

After quotienting the degree-three Pluecker ideal, the vector source is

\[
 \mathscr K_3^{\rm pre\text{-}\Omega}
 =S_{(3,3)}H\otimes H,
 \qquad H=(\mathbb C^3)^{\otimes3}.
\]

The exact verifier is
`verification/verify_dth_level2_s7_census.py`.  It uses only integer and
`Fraction` arithmetic.

## 1. Local Schur--Weyl data

Only the following partitions of seven occur at one qutrit site:

\[
\begin{array}{c|rrrrrrrr}
\lambda &(7)&(6,1)&(5,2)&(5,1,1)&(4,3)&(4,2,1)&(3,3,1)&(3,2,2)\\
\hline
f^\lambda&1&6&14&15&14&35&21&21\\
\dim S_\lambda\mathbb C^3&36&48&42&15&24&15&6&3.
\end{array}
\]

The checks

\[
 \sum_\lambda f^\lambda\dim S_\lambda\mathbb C^3=3^7,
 \qquad
 \sum_\lambda(f^\lambda)^2=2761
\]

hold exactly.

For a local type triple \((\lambda,\mu,\nu)\), the reduced multiplicity
rank of the degree-three Grassmann source is

\[
 r_{\lambda\mu\nu}
 =\dim\operatorname{Hom}_{S_6}
 \left(
 [3,3],
 \operatorname{Res}^{S_7}_{S_6}[\lambda]
 \otimes
 \operatorname{Res}^{S_7}_{S_6}[\mu]
 \otimes
 \operatorname{Res}^{S_7}_{S_6}[\nu]
 \right).
\tag{1}
\]

Equivalently,

\[
 r_{\lambda\mu\nu}
 =\sum_{\rho\vdash6}
 \frac{
 \chi^{(3,3)}(\rho)
 \chi^\lambda(\rho,1)
 \chi^\mu(\rho,1)
 \chi^\nu(\rho,1)
 }{z_\rho}.
\tag{2}
\]

The verifier evaluates every character from the Frobenius coefficient
formula, rather than importing a character table.

The exact pre-Omega census is:

\[
\boxed{
\begin{aligned}
\text{ordered local blocks}&=512,\\
\text{active blocks}&=487,\\
\sum r_{\lambda\mu\nu}&=14572,\\
\max r_{\lambda\mu\nu}&=300
  \quad\text{at }(4,2,1)^{\otimes3},\\
\sum\frac{r(r+1)}2&=526070,\\
\dim(S_{(3,3)}H\otimes H)&=80800902.
\end{aligned}}
\tag{3}
\]

The last identity is independently checked from

\[
 \dim S_{(3,3)}(\mathbb C^{27})=2992626.
\]

## 2. The prolonged Omega equation

Up to a fixed nonzero normalization, the degree-three polarized map is

\[
 \mathcal C_{\Omega,3}
 =\frac13\left(
 \Omega_{127}\otimes I_{3456}
 +\Omega_{347}\otimes I_{1256}
 +\Omega_{567}\otimes I_{1234}
 \right).
\tag{4}
\]

On a physical monomial it has the intrinsic form

\[
 \mathcal C_{\Omega,3}(w^3\otimes z)
 =\Omega(w,z)w^2,
\tag{5}
\]

and hence maps onto (S_{(2,2)}H).

Here is a short proof of surjectivity.  Squares of decomposable bivectors
span (S_{(2,2)}H).  The set of decomposable (w=a\wedge b) for which
\(z\mapsto\Omega(a,b,z)\) is nonzero is a nonempty Zariski-open subset of
the irreducible Grassmann cone.  It is nonempty, for example, on the
computational triple

\[
 a=|000\rangle,\qquad b=|111\rangle,\qquad z=|222\rangle.
\]

An open subset has the same linear span as the whole irreducible cone.  For
each such (w), choose (z) with \(\Omega(w,z)=1\); then (5) produces
(w^2).  This proves surjectivity.

Locally the epsilon contraction removes a determinant column.  Thus only

\[
\begin{array}{c|cccc}
\lambda&(5,1,1)&(4,2,1)&(3,3,1)&(3,2,2)\\
\hline
\kappa&(4)&(3,1)&(2,2)&(2,1,1)
\end{array}
\tag{6}
\]

can map, with (S_\lambda\mathbb C^3\cong
\det\otimes S_\kappa\mathbb C^3).  The output multiplicity in a local
triple is

\[
 o_{\kappa_1\kappa_2\kappa_3}
 =\left\langle
 \chi^{(2,2)},
 \chi^{\kappa_1}\chi^{\kappa_2}\chi^{\kappa_3}
 \right\rangle_{S_4}.
\tag{7}
\]

Surjectivity and equivariance imply that (7) is the rank removed from the
corresponding source block.  There are 39 active output blocks, their total
reduced rank is 61, and their maximum rank is 3.  Therefore the exact
post-Omega census is

\[
\boxed{
\begin{aligned}
\sum k_{\lambda\mu\nu}&=14511,\\
\sum\frac{k(k+1)}2&=519434,\\
\sum k^2&=1024357,\\
\dim\ker\mathcal C_{\Omega,3}&=80756676.
\end{aligned}}
\tag{8}
\]

The dimension loss is exactly

\[
80800902-80756676=44226
=\dim S_{(2,2)}(\mathbb C^{27}),
\]

an independent check of (5)--(7).

The support equation (W^\dagger z=0) is not another holomorphic vector
kernel: it contains conjugation.  As at the five-replica level, its correct
prolongation is a linear density equation on a suitable partial transpose of
the moment.  Consequently (8), not an additional unsupported ket quotient,
is the correct positive-block source for the fixed-extension problem.

## 3. Exact seven-to-five reachability

The marginal removes one two-replica bivector pair.  Ordinary restriction
from an (S_7) shape (lambda) to an (S_5) shape (kappa) has
multiplicity equal to the number of two-step paths in Young's lattice.  The
exact table, using the indices displayed in the verifier, is

\[
\begin{array}{c|l}
(5)&(7):1,(6,1):2,(5,2):1,(5,1,1):1\\
(4,1)&(6,1):1,(5,2):2,(5,1,1):2,(4,3):1,(4,2,1):2\\
(3,2)&(5,2):1,(4,3):2,(4,2,1):2,(3,3,1):2,(3,2,2):1\\
(3,1,1)&(5,1,1):1,(4,2,1):2,(3,3,1):1,(3,2,2):1\\
(2,2,1)&(4,2,1):1,(3,3,1):1,(3,2,2):2.
\end{array}
\tag{9}
\]

The refinement to (S_5\times S_2) distinguishes a horizontal two-strip
(H=[2]) from a vertical two-strip (V=[1,1]).  A multiplicity two in (9)
means that both (H) and (V) occur.  Since the removed global pair is a
bivector, a three-site contraction can use only channel triples with an odd
number of vertical strips.  The verifier checks this refinement exactly.

This is a reachability test only.  It is necessary, but a reachable diagram
block can still have a smaller projected contraction rank.  The exact
diagram contraction and normalization are independently established in
`notes/agent_dth_seven_to_five_contraction.md`.

## 4. Blocks forced by the known negative marginal

Use the five-replica shape indices

\[
0=(5),\quad1=(4,1),\quad2=(3,2),\quad
3=(3,1,1),\quad4=(2,2,1).
\]

The exact five-replica obstruction has its worst negative objective ratios
in (444), (333), and permutations of (433); its largest negative raw
contributions include permutations of (141), (331), and (321).
Intersecting their seven-to-five strip reachability with the post-Omega
source gives:

\[
\begin{array}{c|r|r|r}
\text{target family}&\#\text{ source blocks}&\sum k&
\sum k(k+1)/2\\
\hline
444&23&2530&162213\\
333&50&4704&287350\\
433&60&5174&299377\\
141&199&9331&382879\\
331&170&10188&451993\\
321&274&12907&496192.
\end{array}
\tag{10}
\]

Their union contains 301 source blocks, total reduced rank 13660, and
514945 real-symmetric block coordinates.  Hence taking all negative sectors
at once barely reduces the level-two problem.  The smallest decisive first
test is instead the (444) marginal alone:

\[
\boxed{
23\text{ post-Omega PSD blocks}\longrightarrow
R_{444}\in\operatorname{Sym}_{10}.
}
\tag{11}
\]

If (11) is infeasible, the committed first-level moment has no positive
degree-three Grassmann extension, without needing any prolonged support
constraint.  If it is feasible, the exact contraction can be enlarged first
to the (333/433) sectors and then to all 487 blocks; the mixed support and
PPT equations must then be imposed at density level.

## Status

Exact results in this note are the local S7 census, the prolonged-Omega
quotient, the horizontal/vertical contraction reachability, and the finite
target sizes.  The fixed-marginal feasibility decision (11) remains open.


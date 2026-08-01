# Exact five-replica Omega map and obstruction audit

## Status

This note derives the lifted minimal-DTH Omega constraint, including its
normalization, and audits the cloud obstruction directly in the raw qutrit
tensor basis.  The exact conclusion is

\[
 \boxed{
  \mathcal A_4\xi=0,
  \qquad \mathcal C_\Omega\xi=0,
  \qquad
  \frac{\langle\xi,\widetilde{\mathcal O}_0\xi\rangle}
       {\|\xi\|^2}=-\frac14 .
 }
 \tag{1}
\]

In fact, the two summands defining \(\mathcal C_\Omega\) vanish on \(\xi\)
separately.  Thus the Omega equation does **not** remove the known negative
first-Plucker direction.  Of the minimal-DTH equations, only the lifted
support equation can still remove this particular vector.

This is not a physical DTH counterexample: no claim is made that \(\xi\) has
Veronese--Segre form \((w\otimes w)\otimes z\), and the support constraint has
not been imposed here.

The dependency-free exact checker is
`verification/agent_dth_omega_lift.py`.

## 1. Conventions

Put
\[
 H=(\mathbb C^3)^{\otimes3}
\]
and use multi-indices \(\mathbf a=(a_1,a_2,a_3)\).  If
\[
 w=\sum_{\mathbf a,\mathbf b}
 w_{\mathbf a\mathbf b}
 |\mathbf a\rangle\otimes|\mathbf b\rangle
 \in\wedge^2H,
\]
write \(W_w\) for the skew matrix with entries
\[
 (W_w)_{\mathbf a\mathbf b}=w_{\mathbf a\mathbf b}.
\]
There is no conjugation in this identification.

Recall
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai},
 \qquad
 D_z=\sum_{p,q,r}z_{pqr}A_p\otimes A_q\otimes A_r .
\]
Thus
\[
 (D_z)_{\mathbf a\mathbf b}
 =2^{-3/2}
 \sum_{\mathbf p}z_{\mathbf p}
 \prod_{j=1}^3\varepsilon_{p_j a_j b_j}.
 \tag{2}
\]

For three global replicas \(a,b,c\), define the unnormalized local-volume
contraction
\[
 \mathcal E_{abc}
 =\bigotimes_{j=1}^3
 \left(
  \sum_{p,q,r=0}^2
  \varepsilon_{rpq}
  \langle p|_{a,j}\langle q|_{b,j}\langle r|_{c,j}
 \right).
 \tag{3}
\]
The ordering in (3) is: row index of \(W\), column index of \(W\), then
the coefficient index of \(z\).

Directly from (2),
\[
 \mathcal E_{125}(w_{12}\otimes z_5)
 =2^{3/2}\sum_{\mathbf a,\mathbf b}
 (D_z)_{\mathbf a\mathbf b}(W_w)_{\mathbf a\mathbf b}.
 \tag{4}
\]
Since \(W_w^{\mathsf T}=-W_w\),
\[
 \operatorname{Tr}(D_zW_w)
 =-\sum_{\mathbf a,\mathbf b}
 (D_z)_{\mathbf a\mathbf b}(W_w)_{\mathbf a\mathbf b}.
\]
Consequently the exactly normalized scalar constraint map is
\[
 \boxed{
  \omega_{125}=-2^{-3/2}\mathcal E_{125},
  \qquad
  \omega_{125}(w_{12}\otimes z_5)
  =\operatorname{Tr}(D_zW_w).
 }
 \tag{5}
\]

Equivalently, if
\[
 |\mathrm{Alt}\rangle
 =\frac1{\sqrt6}\sum_{p,q,r}\varepsilon_{pqr}|pqr\rangle,
\]
then
\[
 \omega=-3\sqrt3\,
 \langle\mathrm{Alt}|^{\otimes3}.
 \tag{6}
\]
The sign in (5)--(6) is fixed by the matrix trace, rather than chosen only
up to a nonzero scalar.

## 2. The five-replica lift

Use replicas \(1,2\) for the first bivector, replicas \(3,4\) for the
second, and replica \(5\) for \(z\).  Identify either surviving pair with
one fixed copy of \(\wedge^2H\).  Define
\[
 \boxed{
 \mathcal C_\Omega
 =\frac12\left(
 I_{12}\otimes\omega_{345}
 +\omega_{125}\otimes I_{34}
 \right).
 }
 \tag{7}
\]
For every physical monomial
\[
 \eta(w,z)=w_{12}\otimes w_{34}\otimes z_5,
\]
both terms in (7) have the same value.  Therefore
\[
 \boxed{
 \mathcal C_\Omega\eta(w,z)
 =w\,\operatorname{Tr}(D_zW_w).
 }
 \tag{8}
\]
No extra factor occurs in (8).

The map is complex-linear and holomorphic: no adjoints or coefficient
conjugations enter (7).  Its elementary symmetry checks are:

* \(\omega_{ab5}F_{ab}=-\omega_{ab5}\), so pair-antisymmetric inputs
  produce an antisymmetric output;
* exchange of the pairs \((12)\leftrightarrow(34)\) exchanges the two
  summands of (7), so \(\mathcal C_\Omega\) is defined on
  \(\operatorname{Sym}^2(\wedge^2H)\otimes H\);
* physical-site permutations merely permute the three factors in (3),
  hence commute with the construction;
* for \(g=g_1\otimes g_2\otimes g_3\in U(3)^3\),
  \[
  \omega((g\otimes g)w\otimes gz)
  =\chi(g)\omega(w\otimes z),
  \qquad
  \chi(g)=\prod_{j=1}^3\det g_j.
  \tag{9}
  \]
  Thus the target of (7) is properly
  \(\wedge^2H\otimes\chi\).  The zero equation is fully
  \(U(3)^3\)-invariant; on \(SU(3)^3\) the determinant twist is trivial.

As a normalization audit, take
\[
 w=|000\rangle|111\rangle-|111\rangle|000\rangle,
 \qquad z=|222\rangle.
\]
Then the raw contraction (3) is \(2\), while
\[
 \operatorname{Tr}(D_zW_w)=-\frac1{\sqrt2}.
\]
Equation (7) gives
\[
 \sqrt2\,\mathcal C_\Omega\eta(w,z)=-w,
\]
which is checked coefficient by coefficient in the verifier.

## 3. Raw realization of the cloud obstruction

At one physical qutrit site, realize the point permutation module on five
symbols by the binary words
\[
 e_i^{(1)}=|0\cdots 010\cdots0\rangle,
\]
with the \(1\) in replica \(i\), and realize the two-subset incidence
module by
\[
 e_{\{i,j\}}^{(2)}
 =|0\cdots010\cdots010\cdots0\rangle.
\]
Set
\[
 f_i=e_i^{(1)}-e_4^{(1)}
\]
and
\[
 r_{ab\mid cd}
 =e_{\{a,c\}}^{(2)}-e_{\{a,d\}}^{(2)}
  -e_{\{b,c\}}^{(2)}+e_{\{b,d\}}^{(2)}.
\]
The exact integer vector is
\[
\begin{aligned}
\xi={}&-
 (f_1\otimes f_1+f_3\otimes f_3)\otimes r_{01\mid23}\\
&+(f_3\otimes f_3-f_2\otimes f_2)\otimes r_{01\mid24}\\
&+(f_1\otimes f_1-f_0\otimes f_0)\otimes r_{04\mid23}.
\end{aligned}
\tag{10}
\]
The three tensor factors in (10) are the three physical qutrit sites;
each factor itself contains the five replica positions.

After exact collection, \(\xi\) has 52 nonzero computational-basis
coefficients and
\[
 \boxed{\|\xi\|^2=64.}                                 \tag{11}
\]
Direct simultaneous replica permutations give
\[
 F_{12}\xi=-\xi,
 \qquad F_{34}\xi=-\xi,
 \qquad F_{(13)(24)}\xi=\xi,
 \qquad \mathcal A_4\xi=0.                             \tag{12}
\]

## 4. Omega audit

Every computational-basis monomial in (10) uses only the local qutrit
symbols \(0\) and \(1\).  Each local factor in (3), however, is nonzero
only when its three inputs contain all three symbols \(0,1,2\).
It follows term by term, without cancellation, that
\[
 \boxed{
  \mathcal E_{125}\xi=0,
  \qquad
  \mathcal E_{345}\xi=0.
 }
 \tag{13}
\]
Therefore
\[
 \boxed{\mathcal C_\Omega\xi=0.}                       \tag{14}
\]

This also explains why the strong cofactor repair vanishes on \(\xi\):
the local three-replica antisymmetrizer has zero range on a two-symbol
alphabet.

## 5. Minimal witness audit

For a pair of global replica positions \(a,b\), write
\[
 \mathsf G_{ab}=\prod_{j=1}^3\frac{I-F_{ab}^{(j)}}2.
\]
Exact subset expansion in the computational basis gives
\[
 \langle\xi,\mathsf G_{15}\xi\rangle=16,
 \qquad
 \langle\xi,\mathsf G_{35}\xi\rangle=16.              \tag{15}
\]
Since
\[
 (\mathcal O_0)_{125}=\frac14I-2\mathsf G_{15},
 \qquad
 (\mathcal O_0)_{345}=\frac14I-2\mathsf G_{35},
\]
(11) and (15) give
\[
 \boxed{
  \langle\xi,(\mathcal O_0)_{125}\xi\rangle
  =\langle\xi,(\mathcal O_0)_{345}\xi\rangle
  =-16.
 }
 \tag{16}
\]
Hence
\[
 \boxed{
  \langle\xi,\widetilde{\mathcal O}_0\xi\rangle=-16,
  \qquad
  \frac{\langle\xi,\widetilde{\mathcal O}_0\xi\rangle}
       {\|\xi\|^2}=-\frac14.
 }
 \tag{17}
\]

## 6. Exact consequence and remaining finite question

The first-Plucker obstruction survives the complete Omega equation.  Thus
\[
 \ker\mathcal A_4\cap\ker\mathcal C_\Omega
\]
is still an indefinite relaxation for \(\widetilde{\mathcal O}_0\).
The known vector lies in the local Schur--Weyl block
\[
 [4,1]\otimes[4,1]\otimes[3,2].
\]

This sharply localizes the immediate full-DTH audit:

1. compute \(\mathcal C_{\mathrm{supp}}\xi\) exactly;
2. if it is nonzero, restrict the same block to
   \(\ker\mathcal C_{\mathrm{supp}}\) and compute its exact inertia;
3. only then examine other local blocks.

The current result is a certificate-level obstruction, not a physical
Werner witness and not a proof or disproof of DTH.

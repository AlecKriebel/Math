# The corrected mixed-conjugate first DTH lift

## Status

This note repairs the conjugation defect in the proposed five-replica DTH
kernel.  The repair is not to invent a linear map from the holomorphic ket

\[
h(w,z)=w\otimes w\otimes z,
\]

to a mixed ket.  Such a map is phase-obstructed.  The correct consistency
relation occurs one level higher, between density operators:

\[
\boxed{
 |\bar w\otimes w\otimes z\rangle
 \langle\bar w\otimes w\otimes z|
 =
 \bigl(|w\otimes w\otimes z\rangle
 \langle w\otimes w\otimes z|\bigr)^{\Gamma _1}.
}
\tag{1}
\]

Here \(\Gamma _1\) transposes the first bivector slot and consequently
changes that ket slot from \(\wedge ^2V\) to
\(\overline{\wedge ^2V}\).

Equation (1) gives a finite, mathematically well-defined first lifted
relaxation.  It uses one Hermitian variable \(\rho\), requires

\[
 \rho\succeq0,
 \qquad
 \rho^{\Gamma _1}\succeq0,
\]

puts the holomorphic Pluecker and Omega equations on the range of \(\rho\),
and puts the mixed support equation on the range of
\(\rho^{\Gamma _1}\).  All conditions are linear equalities and positive
semidefinite constraints.

The main exact theorem proved below is:

> **Rank-one exactness.**  The nonzero rank-one feasible points of this
> corrected relaxation are exactly the physical DTH monomials
> \((w\otimes w)\otimes z\), with \(w\) decomposable,
> \(W^\dagger z=0\), and \(\operatorname{Tr}(D_zW)=0\).

Thus a negative rank-one feasible point is an exact physical DTH
counterexample.  A negative higher-rank feasible point is an exact
first-degree pseudomoment obstruction.  Positivity of the entire relaxation
proves DTH.  No one of these three outcomes is asserted here: the purpose of
this note is to identify the correct finite decision problem without
collapsing a pseudomoment statement into a physical statement.

The companion dependency-free exact checker is
`verification/agent_dth_mixed_module.py`.

## 1. Spaces and conventions

Let

\[
 V=(\mathbb C^3)^{\otimes3},
 \qquad A=\wedge ^2V,
 \qquad
 \mathscr B=A_1\otimes A_2\otimes V_3,
\]

and introduce the mixed space

\[
 \widehat{\mathscr B}
 =\bar A_1\otimes A_2\otimes V_3.
\tag{2}
\]

If

\[
 w=\sum_{i,j}W_{ij}e_i\otimes e_j\in A,
 \qquad W^{\mathsf T}=-W,
\tag{3}
\]

then \(W\) is the coefficient matrix of \(w\).  We use the Hilbert-space
embedding convention in (3); in particular, if the logical wedge basis is
\((e_i\otimes e_j-e_j\otimes e_i)/\sqrt2\), its coefficient matrix has
entries divided by \(\sqrt2\).  This fixes all normalizations below.

Let

\[
 \omega(w,z)=\operatorname{Tr}(D_zW).
\tag{4}
\]

On \(\operatorname{Sym}^2(A)\otimes V\), let \(\mathcal A_4\) denote
the wedge map on the first two factors, with irrelevant nonzero
normalization, and let

\[
 \mathcal C_\Omega(w\otimes w\otimes z)
 =w\,\omega(w,z)
\tag{5}
\]

be the exactly normalized polarized Omega map derived in
`agent_dth_omega_lift.md`.  Define the holomorphic constraint space

\[
 \boxed{
 \mathscr K_{\rm hol}
 =\operatorname{Sym}^2(A)\otimes V
   \cap\ker\mathcal A_4
   \cap\ker\mathcal C_\Omega .
 }
\tag{6}
\]

Pair antisymmetry is already built into \(A\).  Pair exchange symmetry is
built into \(\operatorname{Sym}^2(A)\).

## 2. Canonical partial transpose into the mixed module

Choose an orthonormal basis \((a_\alpha)\) of \(A\) only to display
indices.  For \(R\in\operatorname{End}(\mathscr B)\), define

\[
 \Theta _1(R)=R^{\Gamma _1}
 \in\operatorname{End}(\widehat{\mathscr B})
\]

by

\[
 \boxed{
 (R^{\Gamma _1})_{\bar\alpha\,\beta k;
                         \bar\alpha'\,\beta'k'}
 =R_{\alpha'\,\beta k;
      \alpha\,\beta'k'} .
 }
\tag{7}
\]

This is basis-independent when the transposed slot is understood as the
conjugate Hilbert space.  Intrinsically, on an elementary operator it is

\[
 |a\otimes q\rangle\langle b\otimes r|
 \longmapsto
 |\bar b\otimes q\rangle\langle\bar a\otimes r|.
\tag{8}
\]

It is complex-linear, trace preserving, Hermiticity preserving, an
involution after the canonical double-conjugate identification, and
self-adjoint for the Hilbert--Schmidt pairing.

For

\[
 h=w\otimes w\otimes z,
 \qquad
 m=\bar w\otimes w\otimes z,
\]

the matrix entries are

\[
 \begin{aligned}
 |h\rangle\langle h|_{\alpha\beta k;
                         \alpha'\beta'k'}
 &=w_\alpha w_\beta z_k
   \bar w_{\alpha'}\bar w_{\beta'}\bar z_{k'},\\
 |m\rangle\langle m|_{\bar\alpha\beta k;
                         \bar\alpha'\beta'k'}
 &=\bar w_\alpha w_\beta z_k
   w_{\alpha'}\bar w_{\beta'}\bar z_{k'}.
 \end{aligned}
\]

Substitution in (7) proves (1) coefficient by coefficient.  Notice that
this avoids the phase contradiction at ket level: both sides of (1) are
phase invariant density operators.

## 3. Exact mixed support evaluation

Define

\[
 E:\bar A\otimes V\longrightarrow\bar V
\]

by

\[
 \boxed{
 E(\bar w\otimes z)
 =\sum_j\left(\sum_i\bar W_{ij}z_i\right)\bar e_j
 =W^\dagger z,
 }
\tag{9}
\]

where the last expression is regarded as a vector in \(\bar V\).  The full
support contraction is

\[
 \boxed{
 \mathcal C_{\rm supp}
 =I_A\otimes E:
 \bar A\otimes A\otimes V\longrightarrow A\otimes\bar V,
 }
\tag{10}
\]

with the tensor factors reordered in the displayed target.  Thus

\[
 \boxed{
 \mathcal C_{\rm supp}
 (\bar w\otimes u\otimes z)
 =u\otimes(W^\dagger z).
 }
\tag{11}
\]

There is no hidden factor in (9)--(11) under convention (3).

If \(g\in U(V)\), then \(W\mapsto gWg^{\mathsf T}\) and

\[
 (gWg^{\mathsf T})^\dagger(gz)
 =\bar g(W^\dagger z).
\]

Consequently (10) intertwines

\[
 \overline{\wedge ^2g}\otimes\wedge ^2g\otimes g
 \quad\hbox{with}\quad
 \wedge ^2g\otimes\bar g.
\]

Taking \(g=g_1\otimes g_2\otimes g_3\) proves exact local
\(U(3)^3\) covariance; physical-site permutations are also respected.

Put

\[
 K_{\rm supp}=\mathcal C_{\rm supp}^\dagger
                    \mathcal C_{\rm supp}\succeq0.
\tag{12}
\]

For a physical mixed monomial,

\[
 \boxed{
 \langle m,K_{\rm supp}m\rangle
 =\|w\|^2\|W^\dagger z\|^2.
 }
\tag{13}
\]

If \(\sigma\succeq0\), the following conditions are equivalent:

\[
 \mathcal C_{\rm supp}\sigma=0,
 \qquad
 \operatorname{ran}\sigma\subseteq\ker\mathcal C_{\rm supp},
 \qquad
 \operatorname{Tr}(K_{\rm supp}\sigma)=0.
\tag{14}
\]

Indeed,

\[
 \operatorname{Tr}(K_{\rm supp}\sigma)
 =\|\mathcal C_{\rm supp}\sigma^{1/2}\|_2^2.
\]

This is the positive mixed localizer that was missing from the holomorphic
common-kernel proposal.

## 4. Relation to the indefinite holomorphic scalar localizer

Let

\[
 J_5=F_{15}+F_{25}+F_{35}+F_{45}
\]

be the cross Jucys operator of `agent_dth_support_lift.md`, and let
\(P_{\rm sym}\) project onto
\(\operatorname{Sym}^2(A)\otimes V\).  Polarization of the exact identity

\[
 \langle w^{\otimes2}\otimes z,
 J_5(w^{\otimes2}\otimes z)\rangle
 =4\|w\|^2\|W^\dagger z\|^2
\]

gives

\[
 \boxed{
 P_{\rm sym}\,\Theta _1(K_{\rm supp})\,P_{\rm sym}
 =\frac14P_{\rm sym}J_5P_{\rm sym}.
 }
\tag{15}
\]

To see that polarization is legitimate, regard the difference as a
Hermitian polynomial of bidegree \((2,2)\) in \((w,\bar w)\) and bidegree
\((1,1)\) in \((z,\bar z)\).  Its vanishing for every \(w,z\) makes every
coefficient vanish.  Equivalently, first polarize in \(z\), then apply the
four-variable polynomial polarization of the symmetric square in \(w\).
This proves (15); mere linear spanning of the Veronese vectors is not being
used as a substitute for polynomial polarization.

Equation (15) explains both the usefulness and the failure of the scalar
condition.  If \(\sigma=\rho^{\Gamma _1}\succeq0\), then

\[
 \operatorname{Tr}(J_5\rho)=0
 \iff
 \operatorname{Tr}(K_{\rm supp}\sigma)=0
 \iff
 \mathcal C_{\rm supp}\sigma=0.
\tag{16}
\]

Without \(\sigma\succeq0\), the middle expression is merely the
expectation of a positive operator against an indefinite matrix.  Positive
and negative directions can cancel.  The exact vector \(\zeta\) in
`agent_dth_five_block.md` exploits precisely this missing consistency.

## 5. The corrected first-degree cone

Let \(P_{\rm hol}\) be the orthogonal projector onto
\(\mathscr K_{\rm hol}\).  Define

\[
 \boxed{
 \begin{aligned}
 \mathfrak C_1=\{\rho\in\operatorname{Herm}(\mathscr B):{}&
 \rho\succeq0,
 \quad \rho^{\Gamma _1}\succeq0,\\
 &P_{\rm hol}\rho P_{\rm hol}=\rho,\\
 &\mathcal C_{\rm supp}\rho^{\Gamma _1}=0\}.
 \end{aligned}
 }
\tag{17}
\]

Every condition in (17) is a linear matrix equality or a positive
semidefinite constraint.  Thus (17), unlike the proposed ket-level common
kernel, is a genuine finite semidefinite cone.

Let

\[
 \widetilde{\mathcal O}_0
 =\frac12\bigl((\mathcal O_0)_{A_1,V}
                 +(\mathcal O_0)_{A_2,V}\bigr)
\tag{18}
\]

on \(\mathscr B\), with the unused bivector factor carrying the identity.
The corrected first-degree decision is

\[
 \boxed{
 \mu_1=min\{\operatorname{Tr}(\widetilde{\mathcal O}_0\rho):
        \rho\in\mathfrak C_1,\ \operatorname{Tr}\rho=1\}.
 }
\tag{19}
\]

The feasible set is closed and compact, so the minimum is attained.  It is
nonempty, for example by taking the physical computational-basis DTH triple

\[
 u_0=|111\rangle,
 \qquad u_1=|112\rangle,
 \qquad z=|000\rangle,
 \qquad w=u_0\wedge u_1.
\]

Here \(W^\dagger z=0\) and direct support inspection gives
\(\omega(w,z)=0\).

The decision (19) has the exact logical alternatives

\[
 \begin{array}{c|l}
 \mu_1\ge0 & \text{DTH is proved;}\\
 \mu_1<0\text{ with a rank-one minimizer}
   & \text{an exact physical DTH counterexample is obtained;}\\
 \mu_1<0\text{ only at higher rank}
   & \text{the corrected first-degree relaxation is insufficient.}
 \end{array}
\tag{20}
\]

No implication in the opposite direction is silently used: a higher-rank
negative point need not be a physical counterexample.

For scale, \(\dim A=351\),

\[
 \dim\mathscr B=351^2\cdot27=3,326,427,
\]

whereas before imposing Omega

\[
 \dim\bigl(\ker\mathcal A_4\cap\operatorname{Sym}^2(A)\bigr)
 =\frac{351\cdot352}{2}-\binom{27}{4}=44,226.
\]

The dimension subtraction is exact because the wedge map is onto:
each basis four-form is the wedge of two basis two-forms.

The raw SDP is therefore finite but not suitable for a dense calculation on
the available machine.  Any actual inertia calculation must use local
unitary or mixed contraction-algebra blocks.  This hardware observation
does not alter the exact formulation.

## 6. Rank-one exactness theorem

### Lemma 1: positivity of a pure partial transpose

For nonzero \(h\in A\otimes B\),

\[
 (|h\rangle\langle h|)^{\Gamma_A}\succeq0
\]

if and only if \(h=a\otimes b\) is a product vector across \(A:B\).

**Proof.**  Use the singular-value decomposition of the coefficient matrix
of \(h\) to write

\[
 h=\sum_{j=1}^r s_j a_j\otimes b_j,
 \qquad s_j>0,
\]

with both displayed families orthonormal.  The partial transpose has
eigenvectors \(\bar a_j\otimes b_j\), with eigenvalues \(s_j^2\).  For
each \(i<j\), the symmetric and antisymmetric combinations

\[
 \frac{\bar a_i\otimes b_j\pm
             \bar a_j\otimes b_i}{\sqrt2}
\]

have eigenvalues \(\pm s_is_j\).  Positivity is therefore equivalent to
\(r=1\), which is exactly the product condition. \(\square\)

### Lemma 2: symmetry forces the same bivector twice

If \(0\ne h=a\otimes q\in A\otimes(A\otimes V)\) and
\(h\in\operatorname{Sym}^2(A)\otimes V\), then

\[
 h=a\otimes a\otimes z
\]

for some nonzero \(z\), after absorbing a scalar into \(a\) or \(z\).

**Proof.**  In a basis, symmetry says

\[
 a_\alpha q_{\beta k}=a_\beta q_{\alpha k}.
\]

Choose \(\alpha_0\) with \(a_{\alpha_0}\ne0\).  Then

\[
 q_{\beta k}=a_\beta
 \frac{q_{\alpha_0k}}{a_{\alpha_0}},
\]

so \(q=a\otimes z\). \(\square\)

### Lemma 3: the first Pluecker equation

For a two-form \(w\),

\[
 w\wedge w=0
\]

if and only if \(w\) is decomposable (or zero).

**Proof.**  One direction is immediate.  Conversely choose indices
\(1,2\) with \(W_{12}\ne0\).  The coefficient of
\(e_1\wedge e_2\wedge e_i\wedge e_j\) in \(w\wedge w\) is, up to one
fixed nonzero factor,

\[
 W_{12}W_{ij}-W_{1i}W_{2j}+W_{1j}W_{2i}.
\]

Its vanishing expresses every \(W_{ij}\) in terms of the first two rows.
Set

\[
 x=e_1-\sum_{j>2}\frac{W_{2j}}{W_{12}}e_j,
 \qquad
 y=W_{12}e_2+\sum_{j>2}W_{1j}e_j.
\]

A coefficient check gives \(w=x\wedge y\), with the sign adjusted if the
opposite coefficient convention is chosen. \(\square\)

### Theorem: rank-one feasible points are physical

Let \(0\ne\rho=|h\rangle\langle h|\).  Then
\(\rho\in\mathfrak C_1\) if and only if, up to an overall scalar,

\[
 h=w\otimes w\otimes z
\]

where

\[
 w\wedge w=0,
 \qquad
 \omega(w,z)=0,
 \qquad
 W^\dagger z=0.
\tag{21}
\]

**Proof.**  If \(\rho\in\mathfrak C_1\), Lemma 1 applied across
\(A_1:(A_2\otimes V)\) gives \(h=a\otimes q\).  The source symmetry and
Lemma 2 give \(h=w\otimes w\otimes z\).  The range constraint
\(\mathcal A_4h=0\), followed by Lemma 3, makes \(w\) decomposable.  Since
\(w\ne0\), \(\mathcal C_\Omega h=0\) gives \(\omega(w,z)=0\).

By (1),

\[
 \rho^{\Gamma _1}
 =|\bar w\otimes w\otimes z\rangle
  \langle\bar w\otimes w\otimes z|.
\]

Equation (11) and the mixed range constraint then give
\(W^\dagger z=0\).

Conversely, (21) puts \(h\) in \(\mathscr K_{\rm hol}\), equation (1)
proves both positive semidefinite constraints, and (11) proves the mixed
support constraint. \(\square\)

This theorem identifies exactly what the partial-transpose consistency adds:
at rank one it supplies the missing Segre relation between the first
bivector and the remaining two factors.  At higher rank it is a convex
relaxation of that relation, not an assertion of physical realizability.

## 7. Exact two-cone and dual forms

Let \(L=\ker\mathcal C_{\rm supp}\subset\widehat{\mathscr B}\), and let
\(\iota_K:\mathscr K_{\rm hol}\hookrightarrow\mathscr B\) and
\(\iota_L:L\hookrightarrow\widehat{\mathscr B}\) be the inclusions.
Equivalently, (19) is

\[
 \begin{aligned}
 \text{minimize}\quad&
 \operatorname{Tr}(O_KX)\\
 \text{subject to}\quad&
 X\succeq0\text{ on }\mathscr K_{\rm hol},
 \quad Z\succeq0\text{ on }L,\\
 &\Theta _1(\iota_KX\iota_K^\dagger)
     =\iota_LZ\iota_L^\dagger,\\
 &\operatorname{Tr}X=1,
 \end{aligned}
\tag{22}
\]

where

\[
 O_K=\iota_K^\dagger\widetilde{\mathcal O}_0\iota_K.
\]

This makes the holomorphic--mixed consistency completely explicit: the two
positive moment matrices are not independent; every entry is tied by the
partial transpose (7).

For completeness, a dual lower-bound certificate is a Hermitian operator
\(Y\) on \(\widehat{\mathscr B}\) and a real number \(\gamma\) satisfying

\[
 \boxed{
 \begin{aligned}
 O_K-\gamma I_K
  -\iota_K^\dagger\Theta _1(Y)\iota_K&\succeq0,\\
 \iota_L^\dagger Y\iota_L&\succeq0.
 \end{aligned}
 }
\tag{23}
\]

Indeed, for every feasible \((X,Z)\), taking traces in (23) and using the
coupling equation in (22) gives

\[
 \operatorname{Tr}(O_KX)-\gamma
 \ge
 \operatorname{Tr}(Y\iota_LZ\iota_L^\dagger)\ge0.
\]

Thus (23) proves \(\mu_1\ge\gamma\) by direct algebra, without invoking an
unproved optimizer or numerical classification.  Conversely, the value of
(19) is exactly the value of the finite two-positive-cone program (22);
standard block reduction is unnecessary for defining the decision.

## 8. Exact local representation routing

At one physical qutrit site, the mixed five-slot representation is

\[
 \bar{\mathbf3}^{\otimes2}\otimes\mathbf3^{\otimes3}.
\]

Writing an \(SU(3)\) irreducible by its two highest-weight integers, direct
symmetrization and trace splitting first give

\[
 \bar{\mathbf3}^{\otimes2}=(0,2)\oplus(1,0),
 \qquad
 \mathbf3^{\otimes3}=(3,0)\oplus2(1,1)\oplus(0,0).
\]

Distributing these six summands and splitting their symmetrized and traced
parts uses the four elementary products

\[
\begin{aligned}
 (0,2)\otimes(3,0)&=(3,2)\oplus(2,1)\oplus(1,0),\\
 (0,2)\otimes(1,1)&=(1,3)\oplus(2,1)\oplus(0,2)\oplus(1,0),\\
 (1,0)\otimes(3,0)&=(4,0)\oplus(2,1),\\
 (1,0)\otimes(1,1)&=(2,1)\oplus(0,2)\oplus(1,0).
\end{aligned}
\]

They follow by adding one symmetrized box and then separating the available
contractions; their dimensions agree term by term.  Together with the two
products by \((0,0)\), they give

\[
 \boxed{
 (3,2)^1\oplus(2,1)^6\oplus(1,0)^6
 \oplus(1,3)^2\oplus(0,2)^5\oplus(4,0)^1.
 }
\tag{24}
\]

The dimension formula

\[
 \dim(p,q)=\frac{(p+1)(q+1)(p+q+2)}2
\]

checks (24) exactly:

\[
 42+6\cdot15+6\cdot3+2\cdot24+5\cdot6+15=243=3^5.
\]

The local mixed commutant consequently has dimension

\[
 1^2+6^2+6^2+2^2+5^2+1^2=103.
\tag{25}
\]

Equations (24)--(25) do not decide the SDP.  They give the correct finite
local block sizes \(1,6,6,2,5,1\) for constructing the partial-transpose
coupling and support localizer without allocating the raw matrices.

## 9. What has and has not been resolved

Established exactly here:

1. the minimal density-level consistency relation (1);
2. the correctly normalized equivariant support map (9)--(11);
3. the positive mixed support localizer and its scalar holomorphic shadow;
4. the finite corrected first-degree program (19)/(22);
5. exact physical realizability of every rank-one feasible point;
6. an explicit dual certificate form.

Still open:

1. the sign of \(\mu_1\);
2. whether a negative higher-rank PPT pseudomoment exists;
3. DTH itself;
4. the compatible common-plane--square-zero cross inequality;
5. unrestricted three-copy and all-copy Werner positivity.

The previous vector \(\zeta\) proves only that dropping
\(\rho^{\Gamma _1}\succeq0\) loses essential information.  It does not
answer (19).  The correct next calculation is a mixed-contraction-algebra
block decomposition of (22), not another unconstrained holomorphic
Pluecker lift.

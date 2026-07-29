# Full-cubic color compression for a one-sided square restriction

**Date:** 2026-07-29

**Status:** exact mixed-color reduction; no proof that the complementary
square is invariant

**Scope:** arbitrary balanced exceptional projections until Section 4,
which is explicitly an abstract three-strand limitation model and not a
local \(R\)-matrix

## 1. Setup and the first exact boundary identity

Let \(V=W\oplus U\), with \(\dim W=r\), \(\dim U=u\), and write \(e,f\)
for the corresponding one-site projections.  Let \(P\) be a balanced
exceptional projection and suppose that \(W\otimes W\) is invariant.
The four-strand restriction theorem then gives

\[
P_W=P|_{W\otimes W},\qquad
\operatorname{rank}P_W=\frac{r^2}{2},\qquad
\operatorname{Tr}_1P_W=\operatorname{Tr}_2P_W=\frac r2 I_W.
\tag{1}
\]

On three sites put

\[
A=P_{12},\qquad B=P_{23}.
\tag{2}
\]

They obey

\[
ABA-BAB=\frac13(A-B).
\tag{3}
\]

The two boundary-color projections

\[
G_L=e_1e_2f_3,\qquad G_R=f_1e_2e_3
\tag{4}
\]

have rank \(r^2u\).  The first commutes with \(A\), and the second
commutes with \(B\).  Balance of \(P\) and \(P_W\) gives

\[
\begin{aligned}
\operatorname{Tr}(G_LA)
&=\operatorname{Tr}(G_LB)=\frac{r^2u}{2},\\
\operatorname{Tr}(G_LAB)&=\frac{r^2u}{4},
\end{aligned}
\qquad
\begin{aligned}
\operatorname{Tr}(G_RA)
&=\operatorname{Tr}(G_RB)=\frac{r^2u}{2},\\
\operatorname{Tr}(G_RBA)&=\frac{r^2u}{4}.
\end{aligned}
\tag{5}
\]

For example, after contracting the first and third sites,

\[
\begin{aligned}
\operatorname{Tr}(G_LAB)
&=\operatorname{Tr}\!\left[
  (P_W)_{12}f_3P_{23}\right]\\
&=\operatorname{Tr}_W\!\left[
  \left(\frac r2I_W\right)
  \left(\frac u2I_W\right)\right]
=\frac{r^2u}{4}.
\end{aligned}
\tag{6}
\]

Here the second factor follows by subtracting the \(W\)-restriction
marginal from the ambient marginal:

\[
e\,\operatorname{Tr}_3\!\left[P_{23}(I\otimes f_3)\right]e
=\left(\frac d2-\frac r2\right)e=\frac u2e.
\tag{7}
\]

Taking the trace of (3) against \(G_L\), using
\([G_L,A]=0\), yields

\[
\operatorname{Tr}(G_LABA)=\operatorname{Tr}(G_LAB),
\qquad
\operatorname{Tr}(G_LBAB)=\|G_LBA\|_{\rm HS}^2.
\tag{8}
\]

The right side of the traced cubic vanishes by (5).  Therefore

\[
\boxed{\|G_LBA\|_{\rm HS}^2=\frac{r^2u}{4}.}
\tag{9}
\]

The shifted argument gives

\[
\boxed{\|G_RAB\|_{\rm HS}^2=\frac{r^2u}{4}.}
\tag{10}
\]

For \(r=4,u=2\), both values are exactly \(8\).

These identities use the ambient cubic in a genuinely mixed sector.
They are stronger than the two-site marginal data, but they are not
zero-variance identities.

## 2. The complete compressed operator equation

The reason (9) does not isolate the desired defect is visible before
taking a trace.  For \(G=G_L\), put

\[
s=GAG,\qquad T=GBG,\qquad
L=(I-G)BG,\qquad
A_\perp=(I-G)A(I-G).
\tag{11}
\]

Because \(G\) commutes with \(A\), both \(s\) and \(A_\perp\) are
projections.  Compressing (3) by \(G\) gives the exact equation

\[
\boxed{
sTs-TsT-L^*A_\perp L=\frac13(s-T).
}
\tag{12}
\]

Projection of \(B^2=B\) to the same corner gives

\[
T^2+L^*L=T.
\tag{13}
\]

Thus the cubic sees the leakage only through the weighted positive
operator \(L^*A_\perp L\), whereas complementary invariance would
require control of the unweighted quantity \(L^*L\).  Replacing \(P\)
by \(I-P\) gives no independent equation: it converts
\(A_\perp\) to \(I-A_\perp\), and the apparent second equation reduces
to (12) using (13).

There is a symmetric formula at \(G_R\).  With

\[
t=G_RBG_R,\quad S=G_RAG_R,\quad
M=(I-G_R)AG_R,\quad
B_\perp=(I-G_R)B(I-G_R),
\tag{14}
\]

one obtains

\[
\boxed{
StS+M^*B_\perp M-tSt=\frac13(S-t).
}
\tag{15}
\]

Equations (12)--(15) are the color-compressed consequences of the
full cubic at the two boundary sectors.

## 3. Relation to the two-site defect

On two sites use the color cells

\[
F=f\otimes f,\qquad
X=e\otimes f,\qquad
Y=f\otimes e.
\tag{16}
\]

Set

\[
\begin{aligned}
c_X&=\|FPX\|_{\rm HS}^2,&
c_Y&=\|FPY\|_{\rm HS}^2,\\
m&=\|YPX\|_{\rm HS}^2
   =\|XPY\|_{\rm HS}^2.
\end{aligned}
\tag{17}
\]

Then the defect from the two-site audit is

\[
\delta(P,W)=c_X+c_Y.
\tag{18}
\]

The boundary leakages in (11) and (14) instead satisfy

\[
\|L\|_{\rm HS}^2=r(c_X+m),\qquad
\|M\|_{\rm HS}^2=r(c_Y+m).
\tag{19}
\]

Consequently,

\[
\|L\|_{\rm HS}^2+\|M\|_{\rm HS}^2
=r\bigl(\delta(P,W)+2m\bigr).
\tag{20}
\]

Even an identity determining both total boundary leakages would not
by itself determine \(\delta\): it also contains the unconstrained
mixed-cell transfer \(m\).  More importantly, (12) and (15) determine
only the \(A_\perp\)- and \(B_\perp\)-weighted parts of these leakages.
Any successful sum-of-squares proof must therefore use additional
off-diagonal color blocks of (3) to eliminate both the weights and
the mixed-transfer term.  Treating (9) or (10) as a saturation of
\(L^*L\) is not valid.

## 4. Exact abstract limitation model at the \(d=6,r=4\) ranks

There is an exact abstract countermodel to any argument using only:

1. the two-projection cubic (3);
2. the balanced \(d=6\) three-strand multiplicities;
3. an inherited balanced \(d=4\) three-strand subrepresentation;
4. the ranks and scalar traces in (5); and
5. the boundary identities (9)--(10).

This does **not** disprove complementary invariance for a genuine local
\(P\).  It proves that tensor-overlap locality across the remaining
color sectors must enter any such proof.

The canonical decomposition of a balanced \(d=6\) \(H_3\)
representation is

\[
\mathcal H
=\mathbb C^{27}_{11}\oplus
 \mathbb C^{27}_{00}\oplus
 \left(\mathbb C^2\otimes\mathbb C^{81}\right),
\tag{21}
\]

where \(A=B=1\) on the first summand, \(A=B=0\) on the second, and on
each standard two-dimensional block

\[
A_0=
\begin{pmatrix}1&0\\0&0\end{pmatrix},
\qquad
B_0=
\begin{pmatrix}
1/3&\sqrt2/3\\
\sqrt2/3&2/3
\end{pmatrix}.
\tag{22}
\]

These matrices satisfy

\[
A_0B_0A_0-B_0A_0B_0=\frac13(A_0-B_0).
\tag{23}
\]

The inherited \(d=4\) summand has multiplicities

\[
8\ \text{common-one},\qquad
8\ \text{common-zero},\qquad
24\ \text{standard blocks},
\tag{24}
\]

and hence dimension \(8+8+2\cdot24=64=4^3\).

In its orthogonal complement choose an abstract \(WWU\) projection
\(G_L\) consisting of:

- four common-one dimensions;
- four common-zero dimensions;
- twelve \(A_0=1\) rows on one multiplicity subspace; and
- twelve \(A_0=0\) rows on a disjoint multiplicity subspace.

Then

\[
\begin{gathered}
\operatorname{rank}G_L=32,\qquad [G_L,A]=0,\\
\operatorname{Tr}(G_LA)=\operatorname{Tr}(G_LB)=16,\qquad
\operatorname{Tr}(G_LAB)=8,\\
\|G_LBA\|_{\rm HS}^2=8,
\end{gathered}
\tag{25}
\]

exactly as required by (5) and (9), but

\[
\boxed{
\frac12\|[B,G_L]\|_{\rm HS}^2=\frac{16}{3}>0.
}
\tag{26}
\]

On disjoint multiplicity coordinates one can choose an abstract
\(UWW\) projection \(G_R\), diagonal in the \(B_0\)-eigenbasis, with
the symmetric properties

\[
\begin{gathered}
\operatorname{rank}G_R=32,\qquad [G_R,B]=0,\\
\operatorname{Tr}(G_RA)=\operatorname{Tr}(G_RB)=16,\qquad
\operatorname{Tr}(G_RBA)=8,\\
\|G_RAB\|_{\rm HS}^2=8,\qquad
\frac12\|[A,G_R]\|_{\rm HS}^2=\frac{16}{3}>0.
\end{gathered}
\tag{27}
\]

The inherited \(W^3\), \(G_L\), and \(G_R\) projections are mutually
orthogonal.  The unused orthogonal complement has dimension \(88\),
exactly the combined dimension of the five remaining color sectors
\[
WUW,\ WUU,\ UWU,\ UUW,\ UUU.
\tag{28}
\]

The exact verifier constructs the full \(216\times216\) sparse
matrices and checks every assertion.

## 5. A stronger eight-color abstract model

The preceding model treats the two boundary projections separately.
One can go further and realize all eight color sectors simultaneously
by three commuting projections \(p_1,p_2,p_3\), while preserving every
commutation relation visible at the color level:

\[
[A,p_3]=0,\qquad [B,p_1]=0,\qquad
[A,p_1p_2]=0,\qquad [B,p_2p_3]=0.
\tag{29}
\]

Their ranks are

\[
\operatorname{rank}p_1
=\operatorname{rank}p_2
=\operatorname{rank}p_3
=4\cdot6^2=144,
\tag{30}
\]

and their joint sectors have the genuine \(4+2\) tensor dimensions

\[
\begin{array}{c|cccccccc}
\text{sector}&WWW&WWU&WUW&UWW&WUU&UWU&UUW&UUU\\ \hline
\text{rank}&64&32&32&32&16&16&16&8.
\end{array}
\tag{31}
\]

Moreover,

\[
\operatorname{Tr}(p_iA)=\operatorname{Tr}(p_iB)=72
\qquad(i=1,2,3),
\tag{32}
\]

so the one-color scalar traces agree with ambient standardness.  The
\(WWW\) sector is exactly the inherited \(d=4\) subrepresentation.
The \(WWU\) and \(UWW\) sectors obey every identity in (5),
(9), and (10).

The construction uses the same canonical decomposition (21).  Most
standard multiplicity blocks are assigned a constant color word.  On
eight additional standard blocks put

\[
p_2=0,\qquad p_3=I,\qquad
p_1\in\{B_0,I-B_0\},
\tag{33}
\]

using each choice four times.  These blocks split between the
\(WUW\) and \(UUW\) sectors.  On eight further blocks put

\[
p_1=p_2=0,\qquad
p_3\in\{A_0,I-A_0\},
\tag{34}
\]

again using each choice four times.  These split between \(UUW\) and
\(UUU\).  The remaining common and standard blocks fill the exact
dimensions in (31); the verifier records the complete assignment.

Let

\[
F_{12}=(I-p_1)(I-p_2),\qquad
F_{23}=(I-p_2)(I-p_3).
\tag{35}
\]

Although the two \(WW\) pair colors reduce the appropriate
generators, their complementary \(UU\) pair colors do not:

\[
\boxed{
\frac12\|[A,F_{12}]\|_{\rm HS}^2
=\frac12\|[B,F_{23}]\|_{\rm HS}^2
=\frac{16}{9}>0.
}
\tag{36}
\]

Thus even the complete color incidence table, all one-color scalar
traces, both spectator-color commutations, both \(WW\)-invariance
conditions, the inherited \(W^3\) representation, and the exact
two-projection cubic do not force complementary color invariance.

The remaining distinction from a genuine local \(P\) is crucial:
the abstract \(A\) and \(B\) have not been shown to factor as
\[
A=P\otimes I_6,\qquad B=I_6\otimes P
\tag{37}
\]
for one common two-site projection \(P\).  Equivalently, the model
matches the commutative color algebra but not the full spectator
matrix algebras.  This identifies the only remaining place where a
positive proof can live.

## 6. Conclusion

The full cubic gives nontrivial and exact mixed-color information:
the boundary norms (9)--(10) and the positive operator equations
(12), (15).  It does not, after the currently justified
compressions, yield \(\delta=0\).

The abstract model proves that no trace or sum-of-squares identity
depending only on the \(H_3\) cubic, its multiplicities, the inherited
\(W^3\) summand, and the scalar boundary data can force zero leakage.
The remaining possible proof must exploit simultaneous realization
of **all eight** color sectors by a single two-site projection
\(P\), especially the off-diagonal blocks of (3) linking
\(WUU,UWU,UUW\), and \(UUU\).

Accordingly, for \(r=4,u=2\), the statement

\[
\delta(P,W)=0
\tag{38}
\]

remains unproved and undisproved for genuine local exceptional
solutions.  The exact reduction above narrows the missing ingredient
to tensor-overlap compatibility, rather than the abstract Hecke
relation or its scalar trace consequences.

## 7. Exact replay

Run

```text
/Users/alec/Documents/Math/.venv/bin/python \
  verifiers/verify_one_sided_cubic_abstract_countermodel.py
```

The verifier checks the exact cubic, all ranks and traces, the
inherited \(d=4\) summand, mutual orthogonality of the three selected
sectors, and the two nonzero leakage values.

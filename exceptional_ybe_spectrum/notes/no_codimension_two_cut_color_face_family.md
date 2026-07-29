# No codimension-two cut of the color/face \(d=4\) circle

**Date:** 2026-07-29

**Status:** PROVED

**Scope:** the exact color/face circle of C15 and all of its identity
amplifications.  This is a construction no-go, not a nonexistence theorem
for arbitrary solutions in dimensions \(4m-2\).

## 1. Statement

Let \(H_{s,t}\) be the exact four-dimensional color/face family of C15,
where
\[
s^2+2t^2=1.
\]
On
\[
V_m=\mathbb C^4\otimes\mathbb C^m
\]
let \(H_{s,t}^{(4m)}=H_{s,t}\boxtimes I_m\) denote the identity
amplification, reordered as a two-site operator on \(V_m\otimes V_m\).

> **Theorem 1.**
> For every \(m\ge2\), every orthogonal projection
> \(Q\in\operatorname{End}(V_m)\) satisfying
> \[
> [H_{s,t}^{(4m)},Q\otimes Q]=0
> \]
> has
> \[
> \operatorname{rank}Q\ne4m-2.
> \]

In particular, none of these exact \(d=8\) amplifications can be cut
down to an exceptional solution on a six-dimensional square.

There is also a structural simplification of C15:

> **Proposition 2.**
> The circle \(\{H_{s,t}:s^2+2t^2=1\}\) is one continuous orbit under
> sitewise unitary conjugacy \(H\mapsto(U\otimes U)H(U^*\otimes U^*)\).

This explains why the three numerical landscapes in E38 were identical
to the reported precision.  Theorem 1 is exact and does not use that
numerical observation.

The orbit is not the published five-Pauli solution:

> **Proposition 3.**
> No member of the C15 circle is sitewise-unitarily equivalent to the
> published \(d=4\) witness.

## 2. A uniform three-term form

Put
\[
U_\pm=\frac{X\pm Y}{\sqrt2},\qquad
a=\sqrt2\,t,\qquad b=s,
\]
so \(a^2+b^2=1\).  Direct coefficient extraction from the defining
color/face blocks gives
\[
H_{a,b}=A_1\otimes B_1+A_2\otimes B_2+A_3\otimes B_3, \tag{1}
\]
where
\[
\begin{aligned}
A_1&=I\otimes U_-,
&
B_1&=-\frac{a\,I\otimes U_++b\,X\otimes Z}{\sqrt3},\\
A_2&=Z\otimes U_+,
&
B_2&=-\frac{b\,I\otimes Z+a\,X\otimes U_+}{\sqrt3},\\
A_3&=Z\otimes Z,
&
B_3&=\frac{X\otimes I}{\sqrt3}.
\end{aligned} \tag{2}
\]
The three \(A_i\) are pairwise anticommuting Hermitian involutions.
Thus \(A(x)=x_1A_1+x_2A_2+x_3A_3\) is invertible for every nonzero
real \(x\).

Set \(\widehat B_i=\sqrt3B_i\).  The right coefficients satisfy
\[
\widehat B_i^2=I,\qquad
[\widehat B_i,\widehat B_j]=0,\qquad
\widehat B_1\widehat B_2\widehat B_3=I. \tag{3}
\]
Their four joint eigenspaces are one-dimensional, with joint sign
vectors
\[
(1,1,1),\quad
(1,-1,-1),\quad
(-1,1,-1),\quad
(-1,-1,1). \tag{4}
\]
Consequently the eigenvalues of the real pencil
\[
B(x,y,z)=xB_1+yB_2+zB_3
\]
are \(1/\sqrt3\) times the four linear forms whose coefficient rows are
(4).  Its nonzero rank is at least two.  Its rank-at-most-two cone is
the union of the six real lines
\[
\begin{gathered}
\mathbb R(0,1,1),\quad \mathbb R(0,1,-1),\quad
\mathbb R(1,0,1),\quad \mathbb R(1,0,-1),\\
\mathbb R(1,1,0),\quad \mathbb R(1,-1,0).
\end{gathered} \tag{5}
\]
In particular this cone contains no real plane.  Both the spectrum and
the low-rank geometry are independent of \((a,b)\).

## 3. The circle is one local-unitary orbit

Define the Hermitian involution
\[
C=X\otimes U_-.
\]
It commutes with all three \(A_i\).  For
\[
W_\theta=e^{i\theta C/2}
\]
put
\[
a'=a\cos\theta+b\sin\theta,\qquad
b'=-a\sin\theta+b\cos\theta. \tag{6}
\]
The two planes entering \(B_1\) and \(B_2\) rotate in opposite tensor
coordinates but with the same parameter transformation:
\[
W_\theta B_i(a,b)W_\theta^*=B_i(a',b')
\quad(i=1,2,3). \tag{7}
\]
Since \(W_\theta A_iW_\theta^*=A_i\), equations (1) and (7) give
\[
(W_\theta\otimes W_\theta)H_{a,b}
(W_\theta^*\otimes W_\theta^*)=H_{a',b'}. \tag{8}
\]
Ordinary rotations act transitively on \(a^2+b^2=1\), proving
Proposition 2.

## 4. Separation from the published orbit

Let \(F(\xi\otimes\eta)=\eta\otimes\xi\) be the tensor flip.  Because
\(F\) commutes with every \(U\otimes U\), the quantities
\[
\operatorname{Tr}\bigl((HF)^k\bigr) \tag{9}
\]
are invariants of sitewise unitary conjugacy.  At the convenient family
point \((a,b)=(0,1)\), direct Pauli multiplication gives
\[
\operatorname{Tr}\bigl((H_{0,1}F)^4\bigr)=-\frac{16}{3}. \tag{10}
\]
For the published five-Pauli witness \(H_{\rm pub}\),
\[
(H_{\rm pub}F)^4=I_{16},\qquad
\operatorname{Tr}\bigl((H_{\rm pub}F)^4\bigr)=16. \tag{11}
\]
Proposition 2 makes (10) constant on the C15 orbit, so (10)--(11) prove
Proposition 3.  The same fourth-power invariant is unchanged by
\(H\mapsto-H\) and by tensor flip \(H\mapsto FHF\), so those elementary
operations do not identify the two orbits either.

## 5. Leakage and the active algebra

Amplify (1) by \(I_m\), absorbing the spectator identity into every
coefficient.  Suppose for contradiction that
\(\operatorname{rank}Q=4m-2\), and put \(E=I-Q\), so
\(\operatorname{rank}E=2\).  The square-invariance equation implies
\[
0=(E\otimes Q)H_{a,b}^{(4m)}(Q\otimes Q)
 =\sum_{i=1}^3(EA_iQ)\otimes(QB_iQ). \tag{12}
\]

Let
\[
\mathcal D=\operatorname{span}_{\mathbb R}
\{QB_1Q,QB_2Q,QB_3Q\}.
\]
If \(\dim_{\mathbb R}\mathcal D\le1\), the kernel of
\[
x\longmapsto QB(x)Q
\]
contains a real plane.  Relative to \(QV_m\oplus EV_m\), every pencil
element in this kernel has block form
\[
\begin{pmatrix}0&D\\D^*&F\end{pmatrix}
\]
and therefore rank at most \(4\).  But the amplified pencil has rank
\(m\operatorname{rank}B(x)\).  For \(m=2\), the kernel plane would lie
inside the six-line cone (5).  For \(m\ge3\), every member would have
rank at most one, whereas every nonzero pencil element has rank at least
two.  Both conclusions are impossible.  Hence
\[
\dim_{\mathbb R}\mathcal D\ge2. \tag{13}
\]

Expanding the three compressions in a real basis of \(\mathcal D\),
linear independence of tensor coefficients in (9) supplies two
independent real directions \(u,v\) with
\[
EA(u)Q=EA(v)Q=0.
\]
Taking adjoints shows that \(Q\) commutes with \(A(u)\) and \(A(v)\).
Two independent Clifford directions generate the full active
\(M_2(\mathbb C)\), so
\[
[Q,A_i]=0\qquad(i=1,2,3). \tag{14}
\]
Returning to the full commutator and using the linear independence of
\(A_iQ\) gives
\[
[Q,B_i]=0\qquad(i=1,2,3). \tag{15}
\]

It remains to identify the common active commutant.  The commutant of
the three \(A_i\) is a copy of \(M_2(\mathbb C)\).  Inside it,
\[
C=X\otimes U_-
\]
is a Hermitian involution and
\[
\sqrt3B_3=A_1C.
\]
Thus (11)--(12) force \(Q\) to commute with \(C\), reducing its active
commutant component to \(\operatorname{span}\{I,C\}\).  With the
spectator retained, this means
\[
Q=I\otimes T_0+C\otimes T_1
\]
for operators \(T_0,T_1\in M_m(\mathbb C)\).  On the other hand,
\[
\{C,B_1\}=0,\qquad B_1^2=\frac13I.
\]
Therefore commutation with \(B_1\) gives
\([C,B_1]\otimes T_1=0\).  The first factor is invertible, so \(T_1=0\).
Thus commutation with \(B_1\) kills the \(C\)-coefficient.  The
joint active algebra generated by the six coefficient operators is
all of \(M_4(\mathbb C)\), uniformly on the parameter circle.

After restoring the spectator,
\[
Q\in I_4\otimes M_m(\mathbb C).
\]
Every projection in this commutant has rank divisible by four, contrary
to \(\operatorname{rank}Q=4m-2\).  This proves Theorem 1.

## 6. Consequence and limitation

C40 and Theorem 1 now exclude codimension-two square restriction from
two distinct exact \(d=4\) mechanisms: the published five-Pauli witness
and the complete color/face orbit.  Proposition 3 proves that these are
genuinely different sitewise-unitary orbits.  They do not classify all
four-dimensional exceptional solutions, and they do not constrain a
genuinely new irreducible solution in dimension six.

The exact orbit calculation supersedes the speculative interpretation
in E38: equivalence of the three sampled color/face points is now
proved.  The positive numerical endpoint remains only an optimizer
observation; no global lower bound for the cut objective is claimed.

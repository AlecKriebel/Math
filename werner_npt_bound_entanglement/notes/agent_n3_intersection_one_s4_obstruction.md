# Three-copy intersection-one frontier: an exact \(S_4\) linear no-go

## Status

This note does **not** disprove the intersection-one inequality or
unrestricted three-copy positivity.  It proves that the most direct
four-replica positive-semidefinite certificate is impossible, even after
imposing the linear symmetry forced by the repeated vector \(w\).

The missing information is nonlinear: a physical test vector has the
Veronese form
\[
 Z=w_1\otimes w_2\otimes u_3\otimes v_4,\qquad w_1=w_2.
\]
The exact negative direction below obeys \(F_{12}Z=Z\), but is not
asserted to have this repeated-factor form.

The independent exact checker is
`verification/verify_n3_intersection_one_s4_obstruction.py`.

## 1. The three-vector determinant

Let
\[
 Y=\bigotimes_{i=1}^3\left(I-\frac12F_i\right),
\]
and let \(w,u,v\) be arbitrary unit vectors.  Put
\[
\begin{aligned}
 a&=\langle w\otimes w,Y(w\otimes w)\rangle,\\
 b&=\langle u\otimes v,Y(u\otimes v)\rangle,\\
 z&=\langle w\otimes v,Y(u\otimes w)\rangle.
\end{aligned}
\]
The unresolved intersection-one assertion is
\[
 |z|^2\leq ab.                                             \tag{1}
\]

On four replicas define
\[
 {\cal O}=Y_{12}Y_{34}-Y_{14}Y_{23}F_{13}F_{24}.          \tag{2}
\]
For
\[
 Z=w_1\otimes w_2\otimes u_3\otimes v_4
\]
one has
\[
 \boxed{\qquad
 \langle Z,{\cal O}Z\rangle=ab-|z|^2.
 \qquad}                                                   \tag{3}
\]
Indeed, the first summand factors as \(ab\).  After
\(F_{13}F_{24}\), the four factors are \(u_1,v_2,w_3,w_4\).
The \(14\) contraction is \(z\), while the \(23\) contraction is
\(\overline z\), using invariance of \(Y\) under its two-replica swap.

Since the first two factors of \(Z\) are equal,
\[
 F_{12}Z=Z.                                                \tag{4}
\]
It is therefore tempting to prove
\[
 P_{12}^+{\cal O}P_{12}^+\succeq0.                        \tag{5}
\]
The next section gives an exact qutrit-allowed counterexample to (5).

## 2. Rational \([22]\) model

For one physical site, let \(S_4\) act on the three perfect matchings
\[
 m_0=12|34,\qquad m_1=13|24,\qquad m_2=14|23.
\]
The sum-zero subspace is the irreducible \([22]\) module.  Use the
rational basis
\[
 e_1=m_0-m_2,\qquad e_2=m_1-m_2.
\]
Its Gram matrix is
\[
 G=\begin{pmatrix}2&1\\1&2\end{pmatrix}.                  \tag{6}
\]
This module occurs in four replicas of every local space of dimension
at least two, in particular in the qutrit case.

In this basis the transposition \(F_{12}\) is
\[
 f=\begin{pmatrix}1&0\\-1&-1\end{pmatrix}.                \tag{7}
\]
The two local factors in (2) are
\[
\begin{aligned}
 A&=\left(I-\frac12F_{12}\right)
    \left(I-\frac12F_{34}\right)
   =\begin{pmatrix}1/4&0\\1&9/4\end{pmatrix},\\
 B&=\left(I-\frac12F_{14}\right)
    \left(I-\frac12F_{23}\right)F_{13}F_{24}
   =\begin{pmatrix}5/4&-1\\-1&5/4\end{pmatrix}.
\end{aligned}                                             \tag{8}
\]
All displayed matrices are self-adjoint for the metric \(G\).
On the three-site block \([22]^{\otimes3}\),
\[
 {\cal O}=A^{\otimes3}-B^{\otimes3},\qquad
 F_{12}=f^{\otimes3}.                                     \tag{9}
\]

## 3. Exact negative vector

In lexicographic tensor coordinates
\((111,112,121,122,211,212,221,222)\), take
\[
 x=(-2,1,1,-1,1,-1,-1,1)^{\mathsf T}.                   \tag{10}
\]
Direct rational multiplication gives
\[
 f^{\otimes3}x=x,                                         \tag{11}
\]
\[
 x^{\mathsf T}G^{\otimes3}x=18,                           \tag{12}
\]
and
\[
\boxed{\qquad
 x^{\mathsf T}G^{\otimes3}
 (A^{\otimes3}-B^{\otimes3})x=-\frac{891}{8}.
\qquad}                                                   \tag{13}
\]
The exact Rayleigh quotient is therefore
\[
 -\frac{99}{16}.                                          \tag{14}
\]
This disproves (5) inside a representation block which is already
present for three qutrits.

## 4. The physical Veronese image is also blockwise negative

The nonlinear repeated-\(w\) condition does not make the
\([22]^{\otimes3}\) contribution nonnegative by itself.  Take the
physical computational-basis triple
\[
 w=|000\rangle,\qquad u=v=|111\rangle.                    \tag{15}
\]
The displayed example happens to obey \(w\perp u,v\), and its
four-replica vector is already a tensor product over physical sites.
At each site its local four-replica word is \(|0011\rangle\).

Let \(P_{[22]}\) be the central projector onto the local \([22]\)
isotypic component.  Direct character projection gives
\[
\begin{aligned}
 t=P_{[22]}|0011\rangle
 ={}&\frac13\bigl(|0011\rangle+|1100\rangle\bigr)\\
 &-\frac16\bigl(
 |0101\rangle+|0110\rangle+|1001\rangle+|1010\rangle
 \bigr).
\end{aligned}                                              \tag{16}
\]
For the local operators \(A,B\) in (8),
\[
 \langle t,t\rangle=\frac13,\qquad
 \langle t,At\rangle=\frac1{12},\qquad
 \langle t,Bt\rangle=\frac7{12}.                          \tag{17}
\]
The projected three-site vector is \(t^{\otimes3}\), and hence its exact
block contribution is
\[
\boxed{\qquad
 \langle t^{\otimes3},
 (A^{\otimes3}-B^{\otimes3})t^{\otimes3}\rangle
 =
 \left(\frac1{12}\right)^3-\left(\frac7{12}\right)^3
 =-\frac{19}{96}.
\qquad}                                                    \tag{18}
\]

This is a physical repeated-\(w\) vector, but it is still not a
counterexample to (1).  In fact
\[
 a=b=\frac18,\qquad z=-\frac18,
\]
so the full four-replica expectation is exactly zero.  The other local
\(S_4\) isotypic blocks compensate (18) by \(19/96\).

### 4.1 Exact compensating blocks

The local orbit of \(|0011\rangle\) is the six-dimensional permutation
module
\[
 [4]\oplus[31]\oplus[22].
\]
Writing \(t_\lambda=P_\lambda|0011\rangle\), exact character projection
gives
\[
\begin{array}{c|ccc}
\lambda&
\langle t_\lambda,t_\lambda\rangle&
\langle t_\lambda,At_\lambda\rangle&
\langle t_\lambda,Bt_\lambda\rangle\\ \hline
[4]&1/6&1/24&1/24\\
[31]&1/2&1/8&-3/8\\
[22]&1/3&1/12&7/12 .
\end{array}                                                \tag{19}
\]
Thus the local difference \(A-B\) has expectation \(0,+1/2,-1/2\)
on these three components.  The smallest compensation is exactly the
pairing \([31]\leftrightarrow[22]\); the trivial block contributes
nothing to the local difference.

For completeness, group the three-site terms by the counts
\((n_{[4]},n_{[31]},n_{[22]})\).  Including multinomial multiplicity,
their exact contributions are
\[
\begin{array}{c|r@{\qquad}c|r}
(0,0,3)&-19/96 &(0,1,2)&37/96\\
(0,2,1)&-31/128&(0,3,0)&7/128\\
(1,0,2)&-1/24 &(1,1,1)&11/192\\
(1,2,0)&-1/64 &(2,0,1)&-1/384\\
(2,1,0)&1/384&(3,0,0)&0 .
\end{array}                                                \tag{20}
\]
They sum to zero.  Equivalently, in units of \(1/24\), the local
\(A\)-weights are \((1,3,2)\) and the local \(B\)-weights are
\((1,-9,14)\); both totals equal \(6\).

There is also an exact telescoping description:
\[
 A^{\otimes3}-B^{\otimes3}
 =(A-B)\otimes A\otimes A
 +B\otimes(A-B)\otimes A
 +B\otimes B\otimes(A-B).                                \tag{21}
\]
For this site-product equality, every summand has zero expectation
because
\(\langle0011|(A-B)|0011\rangle=0\).  For entangled \(w,u,v\),
(21) remains true, but the three factors no longer separate.  A global
recoupling must therefore compare the common \([31]\) and \([22]\)
multiplicity tensors across different sites.

## 5. Consequence and remaining lemma

Any proof based only on the linear relation \(F_{12}Z=Z\), including a
positive \(S_4\)-group-algebra certificate modulo \(I-F_{12}\), is
impossible.  The common repeated-factor equations for
\[
 Z=w^{\otimes2}\otimes u\otimes v                         \tag{22}
\]
must enter essentially.

Equation (18) strengthens this no-go: even restricting each individual
isotypic block to the physical repeated-\(w\) Veronese image is not a
positive strategy.  A successful \(S_4\) proof must couple distinct
local isotypic blocks before using the common origin of their
components.  The live inequality remains the full quartic restriction
\[
 \langle w^{\otimes2}\otimes u\otimes v,\,
 {\cal O}\,
 w^{\otimes2}\otimes u\otimes v\rangle\geq0,
\quad \|w\|=\|u\|=\|v\|=1.                                \tag{23}
\]
Neither the abstract negative vector (10) nor the physical negative
block contribution (18) is a rank-two distillation witness.

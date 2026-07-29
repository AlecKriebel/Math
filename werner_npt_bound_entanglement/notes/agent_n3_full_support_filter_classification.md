# Exact classification of the three-copy full-support filter forms

## Status

This note completely classifies the one-site Hermitian quadratic
forms left by the full-support critical-point reduction for the
three-copy pair-sector inequality.

The classification has two consequences.

1. At the boundary value \(f=2/3\), each local form is automatically
   positive semidefinite on all of \(M_3\), not merely on its
   determinantal hypersurface.
2. Above the boundary, the proposed one-site ``full-support filter
   lemma'' is false as an abstract quadratic-form statement.  There
   is an exact family satisfying every one-site condition presently
   available, with \(q(I)<0\).

Thus a proof excluding \(f>2/3\) must use the common origin of the six
left/right filter maps in one tensor \(C\) and the one global
projection \(\Pi _2\).  The last section records an exact trace
identity coupling the three maps on either side and states the
smaller remaining lemma.

The dependency-free exact checker is
`verification/verify_n3_full_support_filter_classification.py`.

## 1. Abstract classification

Fix \(\rho>0\) in \(M_3\), and define
\[
 {\cal N}(A,B)=\operatorname{Tr}(A^\dagger B\rho),
 \qquad \tau=\operatorname{Tr}\rho.
 \tag{1}
\]
Let \(q\) be a Hermitian sesquilinear form on \(M_3\).  Suppose that
for some \(\delta>0\),
\[
 q(A,I)=-\delta\,{\cal N}(A,I)
 \quad\hbox{for every }A,
 \tag{2}
\]
and
\[
 q(A,A)\geq0\qquad\hbox{whenever }\det A=0.
 \tag{3}
\]
The condition in (2) says that \(I\) is a generalized eigenvector of
\(q\) relative to \({\cal N}\), with negative eigenvalue
\(-\delta\).

Put
\[
 {\cal H}_0=\{B:\operatorname{Tr}(B\rho)=0\}.
 \tag{4}
\]
Every \(A\) has the unique decomposition
\[
 A=tI+B,\qquad
 t=\frac{\operatorname{Tr}(A\rho)}{\tau},\quad B\in{\cal H}_0.
 \tag{5}
\]
Equation (2) makes this decomposition \(q\)-orthogonal:
\[
 \boxed{\quad
 q(tI+B,tI+B)=-\delta\tau |t|^2+H(B,B),
 \quad H=q|_{{\cal H}_0}.
 \quad}
 \tag{6}
\]

For \(B\in M_3\), write
\[
 r(B)=\max\{|\lambda|:\lambda\text{ is an eigenvalue of }B\}.
 \tag{7}
\]

### Theorem 1 (canonical form)

Under (2), condition (3) is equivalent to
\[
 \boxed{\qquad
 H(B,B)\geq\delta\tau\,r(B)^2
 \quad\hbox{for every }B\in{\cal H}_0.
 \qquad}
 \tag{8}
\]
In particular, \(H\geq0\), and \(q\) has exactly one negative
direction, counted with multiplicity.

#### Proof

Let \(B\in{\cal H}_0\), and let \(\lambda\) be any eigenvalue of \(B\).
Then \(B-\lambda I\) is singular.  Applying (3) and (6) gives
\[
 0\leq q(B-\lambda I,B-\lambda I)
 =H(B,B)-\delta\tau|\lambda|^2.
 \tag{9}
\]
Taking the largest modulus over the three eigenvalues proves (8).

Conversely, suppose (8), and let \(A=tI+B\) be singular.  Then
\(-t\) is an eigenvalue of \(B\), so \(r(B)\geq|t|\).  Equations
(6) and (8) give
\[
 q(A,A)\geq-\delta\tau|t|^2+\delta\tau r(B)^2\geq0.
 \tag{10}
\]
Thus (3) holds.

The bound (8) gives \(H\geq0\).  Formula (6) then displays one
negative line, \(\mathbb CI\), and no other negative direction.
\(\square\)

The assumption about the negative index is therefore redundant once
(2)--(3) are known.  Even without (2), nonnegativity on singular
matrices implies that the negative index is at most one: every
two-dimensional complex linear subspace contains a nonzero singular
matrix, because the restriction of the homogeneous cubic
\(\det\) to that subspace has a projective root.

### Boundary corollary

If instead
\[
 q(A,I)=0\quad\hbox{for every }A
 \tag{11}
\]
and (3) holds, then
\[
 \boxed{\qquad q\geq0\text{ on all of }M_3,\qquad I\in\ker q.\qquad}
 \tag{12}
\]
Indeed, for arbitrary \(B\), choose an eigenvalue \(\lambda\) of
\(B\).  Then \(B-\lambda I\) is singular and
\[
 0\leq q(B-\lambda I)=q(B).
 \tag{13}
\]
This is the exact statement needed at a critical pair-sector point
with \(f=2/3\).

## 2. A sharp weighted rank-two overlap

The filters \(I-|z\rangle\langle z|\) are instances of the following
sharp lemma.

### Lemma 2 (weighted best rank-two overlap)

Let \(m=\lambda_{\min}(\rho)\).  Then
\[
 \boxed{\quad
 \sup_{\substack{\operatorname{rank}A\leq2\\A\ne0}}
 \frac{|\operatorname{Tr}(A\rho)|^2}
      {\operatorname{Tr}(A^\dagger A\rho)}
 =\tau-m.
 \quad}
 \tag{14}
\]
Equality is attained by \(A=I-|z\rangle\langle z|\), where \(z\) is
a unit eigenvector for \(m\).

#### Proof

Set
\[
 X=A\rho^{1/2},\qquad Y=\rho^{1/2}.
 \tag{15}
\]
Then \(\operatorname{rank}X=\operatorname{rank}A\),
\[
 \|X\|_2^2=\operatorname{Tr}(A^\dagger A\rho),
 \qquad
 \langle Y,X\rangle=\operatorname{Tr}(A\rho).
 \tag{16}
\]
Let \(P\) be the orthogonal projection onto the range of \(X\).
It has rank at most two, and
\[
 |\langle Y,X\rangle|
 =|\langle PY,X\rangle|
 \leq\|PY\|_2\|X\|_2.
 \tag{17}
\]
For every rank-two projection \(P\),
\[
 \|P\rho^{1/2}\|_2^2=\operatorname{Tr}(P\rho)
 \leq\tau-m.
 \tag{18}
\]
To see (18) directly, diagonalize \(\rho\), write its eigenvalues as
\(\lambda_1\geq\lambda_2\geq\lambda_3=m\), and put
\(p_j=\langle e_j,Pe_j\rangle\).  Then
\(0\leq p_j\leq1\), \(\sum_jp_j\leq2\), and hence
\(\sum_j\lambda_jp_j\leq\lambda_1+\lambda_2=\tau-m\).
Equations (17)--(18) prove the upper bound.

Taking \(P=I-|z\rangle\langle z|\), \(A=P\), gives equality.
\(\square\)

## 3. Specialization to a critical pair-sector filter

Put
\[
 c=\frac23.
 \tag{19}
\]
At a normalized rank-two critical point, let
\[
 T(A)=\Pi _2(A_iC),\qquad
 {\cal G}(A,B)=\langle T(A),T(B)\rangle,\qquad
 D=T(I),
 \tag{20}
\]
for one left site; the right-site formula is identical.  Write
\[
 \tau=\|C\|_2^2,\qquad
 f=\frac{\|D\|_2^2}{\tau}.
\tag{21}
\]
Thus \(f=\|D\|_2^2\) under the usual normalization \(\tau=1\).
We retain \(\tau\) in the formulas below to make their scaling
transparent.  The critical identities give
\[
 {\cal G}(A,I)=f{\cal N}(A,I).
 \tag{22}
\]
The local-support boundary theorem gives
\[
 q(A,A):=c{\cal N}(A,A)-{\cal G}(A,A)\geq0
 \quad\hbox{for }\operatorname{rank}A\leq2.
 \tag{23}
\]
If \(f>c\), put \(\delta=f-c\).  Then Theorem 1 applies.

There is a useful exact orthogonal decomposition of the Gram map.
Define
\[
 T_0(A)=T(A)-\frac{{\cal N}(I,A)}{\tau}D.
 \tag{24}
\]
Then \(T_0(A)\perp D\), \(T_0(I)=0\), and
\[
 \boxed{\quad
 {\cal G}(A,A)
 =\frac f\tau|{\cal N}(I,A)|^2+\|T_0(A)\|_2^2.
 \quad}
 \tag{25}
\]
Consequently Theorem 1 is exactly the residual-map inequality
\[
 \boxed{\quad
 \|T_0(B)\|_2^2+\delta\tau r(B)^2
 \leq c\,{\cal N}(B,B)
 \quad(B\in{\cal H}_0).
 \quad}
 \tag{26}
\]

### Sharp filter consequences

For a unit vector \(z\), set
\[
 P_z=|z\rangle\langle z|,
 \qquad r_z=\langle z,\rho z\rangle.
 \tag{27}
\]
Both \(P_z\) and \(I-P_z\) are singular.  Gram
Cauchy--Schwarz, (22), and (23) give
\[
 \boxed{\qquad
 f(\tau-r_z)\leq c\tau.
 \qquad}
 \tag{28}
\]
Indeed,
\[
 {\cal G}(I-P_z,I-P_z)
 \geq\frac{|{\cal G}(I-P_z,I)|^2}{{\cal G}(I,I)}
 =\frac f\tau(\tau-r_z)^2,
 \tag{29}
\]
whereas (23) bounds the left side by \(c(\tau-r_z)\).
Choosing a minimum-eigenvalue vector gives
\[
 \boxed{\quad
 \frac{\lambda_{\min}(\rho)}{\tau}
 \geq1-\frac cf=\frac{\delta}{f}.
 \quad}
 \tag{30}
\]
Thus every one-site density on both the left and right of a
hypothetical \(f>2/3\) critical point is quantitatively full rank.

Since \(T_0(I-P_z)=-T_0(P_z)\), (25) and the two singular filters give
the stronger pointwise estimate
\[
 \boxed{
 \begin{aligned}
 \|T_0(P_z)\|_2^2\leq
 \min\Bigl\{&
 r_z\left(c-\frac{fr_z}{\tau}\right),\\
 &(\tau-r_z)
 \left(c-\frac{f(\tau-r_z)}{\tau}\right)
 \Bigr\}.
 \end{aligned}}
 \tag{31}
\]
In an eigenbasis of \(\rho\), put
\[
 Y_j=T(P_j)-\frac{\lambda_j}{\tau}D.
 \tag{32}
\]
Then
\[
 \sum_{j=1}^3Y_j=0,\qquad Y_j\perp D,
 \tag{33}
\]
and every \(Y_j\) obeys (31) with \(r_z=\lambda_j\).
These are coupled vector constraints, not merely scalar marginal
bounds.

## 4. Exact counterexample to an abstract one-site lemma

The preceding consequences do not force \(\delta=0\).  In fact they
are sharp.

For any \(\rho>0\), define
\[
 {\cal G}_\rho(A,B)
 =\frac f\tau {\cal N}(A,I){\cal N}(I,B).
 \tag{34}
\]
This is a positive semidefinite rank-one Gram form.  It satisfies
\[
 {\cal G}_\rho(A,I)=f{\cal N}(A,I),
 \qquad
 {\cal G}_\rho\preceq f{\cal N}.
 \tag{35}
\]
By Lemma 2,
\[
 q_\rho(A,A)
 :=c{\cal N}(A,A)-{\cal G}_\rho(A,A)\geq0
 \quad(\operatorname{rank}A\leq2)
 \tag{36}
\]
if and only if
\[
 \boxed{\qquad f(\tau-m)\leq c\tau.\qquad}
 \tag{37}
\]
Nevertheless,
\[
 q_\rho(I,I)=(c-f)\tau<0
 \tag{38}
\]
whenever \(f>c\).  On \({\cal H}_0\), \(q_\rho=c{\cal N}>0\), so this
form has exactly one negative direction.

The cleanest concrete instance is
\[
 \rho=\frac13I_3,\qquad f=1.
 \tag{39}
\]
Then
\[
 \boxed{\quad
 q_\rho(A,A)=\frac29\|A\|_2^2-\frac19|\operatorname{Tr}A|^2.
 \quad}
 \tag{40}
\]
For rank at most two,
\[
 |\operatorname{Tr}A|
 \leq\|A\|_1\leq\sqrt2\,\|A\|_2,
 \tag{41}
\]
so (40) is nonnegative.  It vanishes at
\(\operatorname{diag}(1,1,0)\), while
\[
 q_\rho(I,I)=-\frac13.
 \tag{42}
\]
This example also satisfies the critical Hessian domination
\({\cal G}_\rho\preceq f{\cal N}\).  Therefore no argument using only
one site's forms \({\cal N},{\cal G}\), the generalized eigenvector
identity, Hessian domination, and positivity on singular filters can
exclude \(f>2/3\).

## 5. A common-origin trace identity

Actual Werner filter maps contain additional information not present
in (34).  Here is one exact coupling among the three left maps.

Normalize \(\|C\|_2^2=1\), and decompose \(C\) according to the number
of traceless local operator factors:
\[
 C=C_0+C_1+C_2+C_3,\qquad w_k=\|C_k\|_2^2.
 \tag{43}
\]
At a pair-sector critical point,
\[
 w_2=f,\qquad \sum_{k=0}^3w_k=1.
 \tag{44}
\]
Let \(\operatorname{Tr}_{HS}{\cal G}_i^L\) denote the trace of the
one-site Gram operator on the nine-dimensional Hilbert space
\(M_3\), using the ordinary Hilbert--Schmidt metric.

### Proposition 3 (three-site Gram trace)

\[
 \boxed{\qquad
 \sum_{i=1}^3\operatorname{Tr}_{HS}{\cal G}_i^L
 =\frac{16}{3}w_1+\frac{17}{3}f+w_3.
 \qquad}
 \tag{45}
\]
The identical formula holds for the sum of the three right maps.

#### Proof

Let \(P_0(X)=\operatorname{Tr}(X)I_3/3\) and
\(P_1=I-P_0\).  For the Hilbert--Schmidt orthonormal matrix units,
\[
 \sum_{a,b}\|P_0(E_{ab}X)\|_2^2=\frac13\|X\|_2^2,
 \qquad
 \sum_{a,b}\|P_1(E_{ab}X)\|_2^2=\frac83\|X\|_2^2.
 \tag{46}
\]
At site \(i\), a component having two traceless factors on the other
sites must be projected to \(P_0\) locally; a component having one
traceless factor on the other sites must be projected to \(P_1\)
locally.  All other components make no contribution to \(\Pi_2\).

Summing (46) over \(i\), a global degree-one component receives the
coefficient \(2(8/3)=16/3\).  A degree-two component receives
\(1/3+2(8/3)=17/3\).  A degree-three component receives
\(3(1/3)=1\).  A scalar component receives zero.  Orthogonality of
the scalar/traceless sectors proves (45).  Right multiplication gives
the same calculation. \(\square\)

For
\[
 \rho_i^L=\operatorname{Tr}_{\bar i}(CC^\dagger),
 \tag{47}
\]
the decomposition (25) also gives
\[
 \operatorname{Tr}_{HS}{\cal G}_i^L
 =f\operatorname{Tr}\bigl((\rho_i^L)^2\bigr)
  +\operatorname{Tr}_{HS}\bigl((T_{0,i}^L)^\dagger T_{0,i}^L\bigr).
 \tag{48}
\]
Hence
\[
 \boxed{
 \begin{aligned}
 \sum_i\operatorname{Tr}_{HS}
 \bigl((T_{0,i}^L)^\dagger T_{0,i}^L\bigr)
 ={}&\frac{16}{3}w_1+\frac{17}{3}f+w_3\\
 &-f\sum_i\operatorname{Tr}\bigl((\rho_i^L)^2\bigr).
 \end{aligned}}
 \tag{49}
\]
Again, there is an identical right-hand formula.

The elementary trace bound obtained by summing (23) over the nine
matrix units is
\[
 \frac{16}{3}w_1+\frac{17}{3}f+w_3\leq6.
 \tag{50}
\]
This does not by itself contradict \(f>2/3\); it records precisely
where a nonlinear common-origin estimate must improve on independent
filter bounds.

## 6. Smallest remaining lemma

The abstract one-site lemma is false by (34)--(42).  After the
critical-point and local-support boundary reductions, the remaining
interior exclusion can be stated as follows.

> **Common-origin six-filter lemma.**  There is no normalized
> rank-two \(C\in M_3^{\otimes3}\) with all six one-site left/right
> densities positive definite and \(f=\|\Pi_2C\|_2^2>2/3\), satisfying
> the critical normal-space equations, such that all six residual
> maps obtained from the same \(D=\Pi_2C\) obey (26).

Unlike the earlier full-support filter lemma, this statement retains
the indispensable common tensor \(C\), common projection \(D\), and
simultaneous left/right multiplication geometry.  Equations
(30)--(33) and (45)--(49) are exact necessary conditions for it.

Thus the one-site quadratic-form geometry is now closed.  What
remains is not another \(9\times9\) inertia question: it is a
compatibility theorem for six Gram maps coming from one rank-two
three-qutrit operator.

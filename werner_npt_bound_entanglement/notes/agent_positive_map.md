# Positive-map, flag-amplification, and shadow-enumerator notebook

## 2026-07-28 10:03 PDT — scope

The endpoint coefficient form is
\[
\mathcal B_n(A,B)
 :=\operatorname{Tr}\!\left[A^\dagger\mathcal L^{\otimes n}(B)\right],
\qquad
\mathcal L(Z)=Z-\frac12\operatorname{Tr}(Z)I_3,
\qquad
Q_n(A)=\mathcal B_n(A,A).
\tag{1}
\]
More generally, at Werner parameter \(-1<\alpha<0\), put
\[
\mathcal L_\alpha(Z)=Z+\alpha\operatorname{Tr}(Z)I_d,\qquad
\mathcal B_{n,\alpha}(A,B)
 =\operatorname{Tr}\!\left[A^\dagger
 \mathcal L_\alpha^{\otimes n}(B)\right].
\tag{2}
\]
The forms tensor-factorize:
\[
\mathcal B_{n+m,\alpha}(A\otimes C,B\otimes D)
=\mathcal B_{n,\alpha}(A,B)\mathcal B_{m,\alpha}(C,D).
\tag{3}
\]

The main exact result of this note is a flag-amplification theorem: for the
all-copy existence question, arbitrary rank-two matrices can be replaced
without loss by orthogonal rank-two projections.  This turns the
single-code/projection enumerator problem into a globally sufficient target.
The note then records the positive-map shadow inequalities available for
projections and an exact obstruction showing that these linear shadows alone
do not decide the sign.

Best-guess completion toward the full all-copy problem: **35%**.  The
projection reduction is complete, but the projection inequality itself is
not proved.

## 1. Exterior-square amplification, stated in the needed form

The following lemma is included so the later projection reduction is
self-contained.

**Lemma 1 (equal-singular amplification).**  Suppose
\(X_{\alpha,d}^{\otimes n}\) is block-positive and has negative expectation
on a Schmidt-rank-at-most-two vector.  Then
\(X_{\alpha,d}^{\otimes 2n}\) has negative expectation on a coefficient
matrix
\[
D=|u_1\otimes u_2\rangle\langle v_1\otimes v_2|
 -|u_2\otimes u_1\rangle\langle v_2\otimes v_1|,
\tag{4}
\]
whose two nonzero singular values both equal one.

*Proof.*  Write a negative coefficient matrix in singular form
\[
C=s_1C_1+s_2C_2,\qquad C_i=|u_i\rangle\langle v_i|,
\]
where both displayed pairs are orthonormal.  Let
\[
H_{ij}=\mathcal B_{n,\alpha}(C_i,C_j).
\]
Block positivity gives \(H_{11},H_{22}\geq0\).  Since some quadratic
combination of the \(C_i\)'s is negative, the Hermitian matrix \(H\) is not
positive semidefinite.  Therefore
\[
\det H=H_{11}H_{22}-|H_{12}|^2<0.
\tag{5}
\]
The two left vectors and the two right vectors in (4) are orthonormal, so
(4) is a singular-value decomposition with singular values \(1,1\).
Tensor factorization gives
\[
\begin{aligned}
Q_{2n,\alpha}(D)
&=2H_{11}H_{22}-H_{12}H_{21}-H_{21}H_{12}\\
&=2\det H<0.
\end{aligned}
\tag{6}
\]
\(\square\)

For the Werner family in the physical range, the block-positivity hypothesis
holds: \(X_{\alpha,d}\) is the partial transpose of
\(I+\alpha F\succeq0\) for \(-1\leq\alpha\leq1\); the same statement
holds for every tensor power.

## 2. Flag amplification to an orthogonal rank-two projection

**Theorem 2 (projection reduction).**  Fix \(d\geq2\) and
\(-1<\alpha<0\).  There exists a negative finite-copy
Schmidt-rank-at-most-two Werner witness if and only if there exists, possibly
at a larger finite copy number, a negative coefficient matrix which is an
orthogonal rank-two projection.

In particular, at the endpoint \(\alpha=-1/2,d=3\), all-copy
two-block-positivity is equivalent to
\[
Q_n(P)\geq0
\quad\text{for every }n\text{ and every orthogonal rank-two projection }P.
\tag{7}
\]

*Proof.*  Only the forward implication needs proof.  By Lemma 1, it is
enough to start with a rank-two partial isometry
\[
D=\sum_{i=1}^2|l_i\rangle\langle r_i|,
\qquad
P_R=D^\dagger D=\sum_i|r_i\rangle\langle r_i|,
\qquad
P_L=DD^\dagger=\sum_i|l_i\rangle\langle l_i|,
\tag{8}
\]
such that \(q:=Q_{n,\alpha}(D)<0\).

Add \(m\) physical flag copies and use the two product strings
\[
a=|0\rangle^{\otimes m},\qquad b=|1\rangle^{\otimes m}.
\]
For \(F_{xy}=|x\rangle\langle y|\), direct application of
\(\mathcal L_\alpha\) on each flag site gives the complete nonzero
contraction table
\[
\begin{array}{c|c}
\text{pairing}&\mathcal B_{m,\alpha}\text{ value}\\ \hline
(F_{aa},F_{aa}),\ (F_{bb},F_{bb})&(1+\alpha)^m\\
(F_{aa},F_{bb}),\ (F_{bb},F_{aa})&\alpha^m\\
(F_{ab},F_{ab}),\ (F_{ba},F_{ba})&1.
\end{array}
\tag{9}
\]
Every other pairing among these four matrix units is zero.  Indeed, on one
site a diagonal matrix unit has self-pairing \(1+\alpha\), two distinct
diagonal units have pairing \(\alpha\), and an off-diagonal matrix unit is
fixed by \(\mathcal L_\alpha\).

Set
\[
w_i=a\otimes r_i+b\otimes l_i,\qquad
E_m=\sum_{i=1}^2|w_i\rangle\langle w_i|.
\tag{10}
\]
Then
\[
E_m
=F_{aa}\otimes P_R+F_{bb}\otimes P_L
 +F_{ab}\otimes D^\dagger+F_{ba}\otimes D.
\tag{11}
\]
Using (3) and the table (9), with
\(c=\mathcal B_{n,\alpha}(P_R,P_L)\), gives the exact identity
\[
\boxed{\quad
Q_{n+m,\alpha}(E_m)
=2q+(1+\alpha)^m\bigl(Q_{n,\alpha}(P_R)+Q_{n,\alpha}(P_L)\bigr)
 +2\alpha^m\operatorname{Re}c.
\quad}
\tag{12}
\]
Here \(Q(D^\dagger)=Q(D)\), because \(\mathcal L_\alpha\) preserves
adjoints, and
\(\mathcal B(P_L,P_R)=\overline{\mathcal B(P_R,P_L)}\).
Because \(-1<\alpha<0\), both nuisance coefficients tend to zero.  The
first term in (12) is the fixed negative number \(2q\), so (12) is negative
for every sufficiently large finite \(m\).

Finally,
\[
\langle w_i,w_j\rangle=2\delta_{ij}.
\]
Consequently \(P_m:=E_m/2\) is an orthogonal rank-two projection, and
\(Q(P_m)=Q(E_m)/4<0\).  The converse is immediate because an orthogonal
rank-two projection has matrix rank two. \(\square\)

At the endpoint one may make “sufficiently large” completely explicit.
The Hilbert--Schmidt operator norm of \(\mathcal L^{\otimes n}\) is one,
while \(\|P_R\|_2=\|P_L\|_2=\sqrt2\).  Hence
\[
|Q_n(P_R)|,\ |Q_n(P_L)|,
|\mathcal B_n(P_R,P_L)|\leq2.
\tag{13}
\]
The absolute value of the nuisance part of (12) is therefore at most
\(8\,2^{-m}\).  Any
\[
2^{-m}<-\frac q4
\tag{14}
\]
guarantees negativity.

**Why multiple flags matter.**  With one flag, (12) contains support
projection and mixed-support invariants whose signs are uncontrolled.
The off-diagonal matrix units \(F_{ab},F_{ba}\) are traceless and therefore
have flag eigenvalue one, whereas all diagonal nuisance coefficients have
modulus strictly below one.  Repeating the flag isolates \(Q(D)\) in the
limit without ever taking an infinite number of copies.

## 3. The \(d=3\) reduction map and a continuum of exact shadows

Define
\[
\mathcal R(A)=\operatorname{Tr}(A)I_3-A.
\tag{15}
\]
With the real skew matrices \((A_k)_{ij}=\varepsilon_{kij}\),
\[
\mathcal R(A)=\sum_{k=0}^2 A_kA^TA_k^\dagger.
\tag{16}
\]
This follows from
\[
\sum_k\varepsilon_{kia}\varepsilon_{kjb}
=\delta_{ij}\delta_{ab}-\delta_{ib}\delta_{aj}.
\]
Thus \(\mathcal R\) is completely copositive.  The endpoint coefficient
superoperator is
\[
\mathcal L=\frac12(I-\mathcal R).
\tag{17}
\]

There is a useful one-parameter extension.  For real \(t\), set
\[
\Theta_t=\mathcal R+tI.
\tag{18}
\]
Then
\[
(\Theta_t\circ T)(A)=\operatorname{Tr}(A)I_3+(t-1)A^T.
\]
Its Choi matrix is
\[
I+(t-1)F,
\tag{19}
\]
whose eigenvalues on the symmetric and antisymmetric subspaces are
\(t\) and \(2-t\).  Therefore
\[
\boxed{\quad \Theta_t\text{ is completely copositive for }0\leq t\leq2.
\quad}
\tag{20}
\]
Its tensor powers are again completely copositive, because the tensor
product of all local transposes is the global transpose.  Consequently,
for every positive semidefinite \(H\),
\[
\langle H,\Theta_t^{\otimes n}(H)\rangle_{\rm HS}\geq0,
\qquad 0\leq t\leq2.
\tag{21}
\]

Now let \(P\) be an orthogonal rank-two projection.  Decompose local
operator space orthogonally as
\[
M_3=\operatorname{span}\{I/\sqrt3\}\oplus M_3^0.
\]
For \(T\subseteq[n]\), let \(P_T\) be the component which is traceless
exactly at the sites in \(T\), and put
\[
a_T=\|P_T\|_2^2\geq0.
\tag{22}
\]
Since \(\mathcal R\) has eigenvalue \(2\) on the scalar direction and
\(-1\) on the traceless directions,
\[
\boxed{\quad
f_P(t):=\langle P,\Theta_t^{\otimes n}(P)\rangle
=\sum_{T\subseteq[n]}(2+t)^{n-|T|}(t-1)^{|T|}a_T.
\quad}
\tag{23}
\]
Equations (20)--(21) prove \(f_P(t)\geq0\) throughout \([0,2]\).
The desired endpoint value lies outside that interval:
\[
\boxed{\quad
Q_n(P)=(-1)^n2^{-n}f_P(-1).
\quad}
\tag{24}
\]
Also
\[
a_\varnothing=\frac{|\operatorname{Tr}P|^2}{3^n}
=\frac4{3^n},
\qquad
\sum_Ta_T=\|P\|_2^2=2.
\tag{25}
\]

The same shadow construction applies after reducing \(P\) to any subset of
physical sites.  In terms of (22), it gives, up to an irrelevant positive
power of \(3\), all inequalities
\[
\sum_{T\subseteq S}(2+t)^{|S|-|T|}(t-1)^{|T|}a_T\geq0
\quad(0\leq t\leq2,\ S\subseteq[n]).
\tag{26}
\]

## 4. Exact obstruction: all linear co-CP shadows are insufficient

The family (26), even together with nonnegativity, trace, and norm, does not
imply the endpoint sign.  At \(n=3\), consider the following formal
operator-sector weights:
\[
a_\varnothing=\frac4{27},\qquad
a_T=\frac{50}{81}\quad(|T|=2),\qquad
a_T=0\quad\text{otherwise}.
\tag{27}
\]
They obey
\[
a_T\geq0,\qquad
\sum_Ta_T=\frac4{27}+3\frac{50}{81}=2.
\tag{28}
\]
For every subset \(S\), every nonzero term in (26) has even \(|T|\).
Since \(2+t\geq0\) and \((t-1)^{|T|}\geq0\) on \(0\leq t\leq2\),
every inequality (26) holds.  Nevertheless,
\[
\sum_T\left(-\frac12\right)^{3-|T|}a_T
=-\frac18\frac4{27}-\frac12\frac{50}{27}
=-\frac{17}{18}<0.
\tag{29}
\]
The weights (27) are not asserted to arise from a projection.  Their role is
to prove exactly that positivity of all reduction-map shadows does not encode
the idempotence/Pluecker constraints of a genuine two-plane.  A successful
shadow proof must add nonlinear projection information.

## 5. The two-copy skew-factor route and its exact factor-two barrier

This section records how far the direct skew-matrix factorization goes on
the unresolved two-copy inequality.

Let \(X_1,X_2\in M_3\) be Hilbert--Schmidt orthonormal and define the CP map
\[
\mathcal E(A)=\sum_{k=1}^2X_kAX_k^\dagger,
\qquad
\rho_L=\sum_kX_kX_k^\dagger,\qquad
\rho_R=\sum_kX_k^\dagger X_k.
\tag{30}
\]
For traceless \(A,B\), the mixed term in the exact two-copy dual reduction is
\[
\chi=\sum_k\langle BX_k,X_kA\rangle
=\langle B,\mathcal E(A)\rangle.
\tag{31}
\]
Its two defects are
\[
\begin{aligned}
\delta_A&=\operatorname{Tr}\bigl[A^\dagger(2I-\rho_R)A\bigr],\\
\delta_B&=\operatorname{Tr}\bigl[B^\dagger B(2I-\rho_L)\bigr].
\end{aligned}
\tag{32}
\]
The desired result is \(|\chi|^2\leq\delta_A\delta_B\).

Let \(P=J(\mathcal E)=\sum_k|\operatorname{vec}X_k\rangle
\langle\operatorname{vec}X_k|\), with output tensor factor first.  Since
\(\operatorname{Tr}P=2\),
\[
\boxed{\quad
S:=(\mathcal R\otimes\mathcal R)(P)
=2I\otimes I-\rho_L\otimes I-I\otimes\rho_R^T+P\succeq0.
\quad}
\tag{33}
\]
The positivity follows either from (16), noting that the two local
transposes form the global transpose, or directly because
\(\mathcal R\otimes\mathcal R\) is completely copositive.  Its marginals are
\[
\operatorname{Tr}_2S=2(2I-\rho_L),\qquad
\operatorname{Tr}_1S=2(2I-\rho_R^T).
\tag{34}
\]
Moreover, \(S-P\) has an identity in at least one tensor factor.  Hence the
Choi bilinear forms of \(S\) and \(P\) agree when both arguments are
traceless.  Taking Kraus operators for the CP map with Choi matrix \(S\) and
applying ordinary Cauchy--Schwarz therefore gives exactly
\[
|\chi|\leq2\sqrt{\delta_A\delta_B},
\tag{35}
\]
but not the required constant one.  This is the intrinsic factor-two loss
of the unrefined double-reduction shadow.

One might try to replace \(S\) by a positive Choi matrix which has the same
traceless--traceless bilinear form as \(P\) and the desired, uninflated
marginals \(2I-\rho_L\) and \(2I-\rho_R^T\).  Such a matrix, if it exists,
is forced uniquely.  Indeed, the orthogonal complement of
\(M_3^0\otimes M_3^0\) consists of matrices
\(M\otimes I+I\otimes N\).  Solving the two marginal equations gives
\[
\boxed{\quad
S_*=P+\frac{10}{9}I\otimes I
-\frac23\bigl(\rho_L\otimes I+I\otimes\rho_R^T\bigr).
\quad}
\tag{36}
\]
This forced completion need not be positive.  Take the exact orthonormal
frame
\[
X_1=E_{10},\qquad
X_2=\frac{E_{00}+E_{11}}{\sqrt2}.
\tag{37}
\]
Then
\[
\rho_L=\operatorname{diag}\left(\frac12,\frac32,0\right),\qquad
\rho_R=\operatorname{diag}\left(\frac32,\frac12,0\right).
\tag{38}
\]
The vector
\[
v=\frac{|11\rangle-|00\rangle}{\sqrt2}
\]
is orthogonal to both \(\operatorname{vec}X_1\) and
\(\operatorname{vec}X_2\), so \(Pv=0\).  On each of \(|00\rangle\) and
\(|11\rangle\), the sum of the two marginal eigenvalues in (36) is \(2\).
Therefore
\[
S_*v=\left(\frac{10}{9}-\frac43\right)v=-\frac29v.
\tag{39}
\]
Thus no ordinary Kraus-Cauchy proof with exactly the two defect marginals
can exist in this natural Choi-completion form.  Any successful skew/SOS
argument must use additional relations among the Kraus factors rather than
only their two squared norms.

## 2026-07-28 10:20 PDT — checkpoint and status

Exact progress:

1. Any finite-copy negative witness, throughout \(-1<\alpha<0\), produces
   a finite-copy negative orthogonal rank-two projection.
2. At \(d=3,\alpha=-1/2\), the problem is therefore exactly the rank-two
   projection inequality (7).
3. The full continuum of co-completely-positive reduction shadows is (23)
   and its subset hierarchy is (26).
4. The formal enumerator (27) proves that these linear shadows alone cannot
   decide the sign.
5. The direct \(d=3\) double-reduction Kraus factorization loses an exact
   factor two; the unique obvious constant-one Choi completion is
   nonpositive by the rational certificate (37)--(39).

What is not resolved: no proof of (7), and no finite-copy negative
projection, is obtained here.  The remaining obstruction is precisely a
nonlinear inequality for the Pluecker coordinates of a genuine
two-dimensional subspace.

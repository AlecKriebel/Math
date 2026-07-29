# Six-map covariance at a three-copy pair-sector critical point

## Status

This note proves an exact common-origin identity coupling the three
left and three right local-filter maps at a critical point of the
qutrit pair-sector functional.  If
\[
 D=\Pi_2C,\qquad f=\|D\|_2^2,\qquad \|C\|_2=1,
\]
and
\[
 T_i^L(A)=\Pi_2(A_iC),\qquad
 T_i^R(A)=\Pi_2(CA_i),
\]
then
\[
 \boxed{\qquad T_i^L(A)-T_i^R(A)=[A_i,D].\qquad}
 \tag{1}
\]
The complete Hilbert--Schmidt norm of the three commutator maps is
independent of how the pair-sector mass is distributed:
\[
 \boxed{\qquad
 \sum_{i=1}^3\sum_{\mu=0}^8
 \|[F_\mu^{(i)},D]\|_2^2=12f,
 \qquad}
 \tag{2}
\]
for every Hilbert--Schmidt orthonormal basis
\((F_\mu)_{\mu=0}^8\) of \(M_3\).

After removing the common \(D\) component, (2) becomes the covariance
identity
\[
 \boxed{\quad
 \sum_i\|T_{0,i}^L-T_{0,i}^R\|_{HS}^2
 +f\sum_i\|\rho_i^L-\rho_i^R\|_2^2
 =12f.
 \quad}
 \tag{3}
\]
This is genuine six-map information.  Nevertheless, an exact formal
model below satisfies (3), every boundary contraction, all Gram-trace
and cross-trace arithmetic, and a pair-sector equality with nonzero
low mass.  It would have \(Q_3=-1/8\).  Thus these norm/covariance
constraints still do not exclude a full-support negative equality.
What they omit is now precise: the three differences in (1) must be
the commuting local derivations of one physical degree-two operator
\(D\), rather than arbitrary maps with the same norms.

The dependency-free checker is
`verification/verify_n3_six_map_covariance_obstruction.py`.

## 1. The exact commutator identity

Let \(P_0(X)=\operatorname{Tr}(X)I_3/3\) and \(P_1=I-P_0\).
For every \(A,X\in M_3\),
\[
 P_0([A,X])=0,\qquad
 P_1([A,X])=[A,P_1X].
 \tag{4}
\]
The scalar/traceless projections on the other two sites commute with
left and right multiplication at site \(i\).  Applying (4) in the
Boolean-sector expansion of \(\Pi_2\) gives
\[
 \Pi_2([A_i,C])=[A_i,\Pi_2C]=[A_i,D].
 \tag{5}
\]
Since the left side of (5) is
\(T_i^L(A)-T_i^R(A)\), this proves (1).  Notice that (1) is not merely
an equality of norms; it retains the common operator \(D\).

## 2. Exact summed commutator norm

For an arbitrary operator \(X\) on
\(\mathbb C^3\otimes{\cal K}\), the matrix units give
\[
\begin{aligned}
 \sum_{a,b=0}^2\|[E_{ab}\otimes I,X]\|_2^2
 &=
 6\|X\|_2^2-2\|\operatorname{Tr}_{\mathbb C^3}X\|_2^2.
\end{aligned}
\tag{6}
\]
Indeed, the two squared terms each sum to
\(3\|X\|_2^2\), while
\[
 \sum_{a,b}(E_{ba}\otimes I)X(E_{ab}\otimes I)
 =I_3\otimes\operatorname{Tr}_{\mathbb C^3}X
\]
makes the cross term equal to
\(2\|\operatorname{Tr}_{\mathbb C^3}X\|_2^2\).
Unitary invariance gives the same formula for every
Hilbert--Schmidt orthonormal basis.

Write the degree-two operator as the orthogonal sum
\[
 D=D_{\widehat1}+D_{\widehat2}+D_{\widehat3},
 \tag{7}
\]
where \(D_{\widehat i}\) is scalar at site \(i\) and traceless at the
other two sites.  Put
\[
 p_i=\|D_{\widehat i}\|_2^2,\qquad
 p_1+p_2+p_3=f.
 \tag{8}
\]
Only \(D_{\widehat i}\) survives \(\operatorname{Tr}_i\), and the
normalized scalar factor gives
\[
 \|\operatorname{Tr}_iD\|_2^2=3p_i.
 \tag{9}
\]
Equations (6)--(9) prove the sharper sitewise and summed formulas
\[
\boxed{
\begin{aligned}
 \sum_\mu\|[F_\mu^{(i)},D]\|_2^2&=6(f-p_i),\\
 \sum_{i,\mu}\|[F_\mu^{(i)},D]\|_2^2&=12f.
\end{aligned}}
\tag{10}
\]

## 3. Removing the common critical direction

At a rank-two critical point, the normal-space equations imply
\[
 CD^\dagger=fCC^\dagger,\qquad
 D^\dagger C=fC^\dagger C.
\tag{11}
\]
Define the one-site left and right densities
\[
 \rho_i^L=\operatorname{Tr}_{\widehat i}(CC^\dagger),
 \qquad
 \rho_i^R=\operatorname{Tr}_{\widehat i}(C^\dagger C),
\tag{12}
\]
both of trace one, and the linear functionals
\[
 n_i^L(A)=\operatorname{Tr}(A\rho_i^L),\qquad
 n_i^R(A)=\operatorname{Tr}(A\rho_i^R).
\tag{13}
\]
Equations (11) give
\[
 \langle D,T_i^L(A)\rangle=f\,n_i^L(A),\qquad
 \langle D,T_i^R(A)\rangle=f\,n_i^R(A).
\tag{14}
\]
Hence the residual maps
\[
 T_{0,i}^L(A)=T_i^L(A)-n_i^L(A)D,\qquad
 T_{0,i}^R(A)=T_i^R(A)-n_i^R(A)D
\tag{15}
\]
take values orthogonal to \(D\).  Combining (1), (14), and (15)
orthogonally gives, site by site,
\[
\boxed{\quad
 \|T_{0,i}^L-T_{0,i}^R\|_{HS}^2
 +f\|\rho_i^L-\rho_i^R\|_2^2
 =6(f-p_i).
\quad}
\tag{16}
\]
Summing (16) proves (3).

There is also an operator-valued local covariance relation:
\[
 \boxed{\qquad
 \operatorname{Tr}_{\widehat i}(DD^\dagger-D^\dagger D)
 =f(\rho_i^L-\rho_i^R).
 \qquad}
\tag{17}
\]
To see this, pair both sides with arbitrary \(A\) and use
\[
 \langle D,[A_i,D]\rangle
 =f\bigl(n_i^L(A)-n_i^R(A)\bigr),
\]
which follows from (1) and (14).

## 4. Sector and residual cross traces

Let \(w_k=\|\Pi_kC\|_2^2\), so \(w_2=f\).  The established Gram-trace
calculation gives, on each side,
\[
 K:=
 \sum_i\operatorname{Tr}_{HS}\bigl((T_i^L)^\dagger T_i^L\bigr)
 =
 \sum_i\operatorname{Tr}_{HS}\bigl((T_i^R)^\dagger T_i^R\bigr)
 =
 \frac{16}{3}w_1+\frac{17}{3}f+w_3.
\tag{18}
\]
Equations (2) and (18) determine the total left--right cross trace:
\[
 \boxed{\quad
 \operatorname{Re}\sum_{i,\mu}
 \langle T_i^L(F_\mu),T_i^R(F_\mu)\rangle
 =K-6f.
\quad}
\tag{19}
\]
Put
\[
\begin{aligned}
 P_L&=\sum_i\operatorname{Tr}((\rho_i^L)^2),&
 P_R&=\sum_i\operatorname{Tr}((\rho_i^R)^2),\\
 S&=\sum_i\operatorname{Tr}(\rho_i^L\rho_i^R).
\end{aligned}
\tag{20}
\]
The residual norm and cross-trace identities are
\[
\boxed{
\begin{aligned}
 \sum_i\|T_{0,i}^L\|_{HS}^2&=K-fP_L,\\
 \sum_i\|T_{0,i}^R\|_{HS}^2&=K-fP_R,\\
 \operatorname{Re}\sum_i
 \langle T_{0,i}^L,T_{0,i}^R\rangle_{HS}
 &=K-6f-fS.
\end{aligned}}
\tag{21}
\]
Consequently covariance Cauchy--Schwarz gives the exact necessary
condition
\[
 \boxed{\qquad
 |K-6f-fS|
 \leq
 \sqrt{(K-fP_L)(K-fP_R)}.
 \qquad}
\tag{22}
\]
The weaker parallelogram consequence of (3) is
\[
 \boxed{\qquad
 4K\geq12f+f(P_L+P_R+2S).
 \qquad}
\tag{23}
\]

At a pair equality \(f=2/3\), the endpoint value is
\[
 Q_3(C)=-\frac98w_0-\frac34w_1.
\tag{24}
\]
Thus ruling out low sector mass at equality would require (1), not
just a bound on the separate six norms.

## 5. Exact obstruction to norm-only covariance arguments

The following finite model passes all scalar identities
(2)--(3) and (18)--(23), as well as every boundary contraction of the
six maps, while carrying nonzero scalar mass.

Take the formal sector distribution
\[
 (w_0,w_1,w_2,w_3)
 =\left(\frac19,0,\frac23,\frac29\right).
\tag{25}
\]
Then
\[
 f=\frac23,\qquad K=4,\qquad Q_3^{\rm formal}=-\frac18.
\tag{26}
\]
At every site set
\[
 \rho_i^L=\rho_i^R=\frac13I_3.
\tag{27}
\]
The sitewise difference norm in the model below corresponds to the
uniform degree-two split
\[
 p_1=p_2=p_3=\frac29.
\tag{27a}
\]
Let \(F_0=I_3/\sqrt3,F_1,\ldots,F_8\) be an orthonormal matrix basis
with the last eight elements traceless.  Choose an output vector
\(D\) of squared norm \(2/3\), and output vectors \(e_{ij}\) which are
orthonormal and orthogonal to \(D\).  Put
\[
 a=\frac{\sqrt5}{6},\qquad
 \eta=\frac{-1+2i\sqrt6}{5}.
\tag{28}
\]
Thus
\[
 a^2=\frac5{36},\qquad |\eta|=1,\qquad
 \operatorname{Re}\eta=-\frac15,\qquad
 |1-\eta|^2=\frac{12}{5}.
\tag{28a}
\]
For each of the three sites define
\[
\begin{aligned}
 T_i^L(F_0)&=D/\sqrt3,&
 T_i^R(F_0)&=D/\sqrt3,\\
 T_i^L(F_j)&=a e_{ij},&
 T_i^R(F_j)&=a\eta e_{ij}
 \quad(1\leq j\leq8).
\end{aligned}
\tag{29}
\]

For \(\rho=I/3\), the boundary filter metric at \(f=2/3\) is
\[
 \frac23\operatorname{Tr}(A^\dagger A\rho)
 =\frac29\|A\|_2^2.
\]
Thus every map in (29) obeys the full positive-semidefinite
contraction.  The scalar direction saturates it, while every
traceless singular value is strictly smaller.  Per site,
\[
\begin{aligned}
 \operatorname{Tr}_{HS}(T_i^{L\dagger}T_i^L)
 &=\operatorname{Tr}_{HS}(T_i^{R\dagger}T_i^R)=\frac43,\\
 \operatorname{Re}\operatorname{Tr}_{HS}
 (T_i^{L\dagger}T_i^R)&=0,\\
 \|T_i^L-T_i^R\|_{HS}^2&=\frac83.
\end{aligned}
\tag{30}
\]
After summing three sites, these become \(K=4\), cross trace zero
\(=K-6f\), and difference norm \(8=12f\), exactly as required.
The residual norms are \(10/3\) on each side, their cross trace is
\(-2/3\), and (3), (21), and (22) all hold exactly.

This is not asserted to be a physical rank-two code.  In particular,
the formal differences in (29) have not been realized as
\([A_i,D]\) for one degree-two operator \(D\).  That failure identifies
the surviving obstruction rather than hiding it.  Notice that each
formal difference map has full rank eight on the traceless input
space, so the obstruction is not a cheap rank defect.

## 6. Comparison with the sharp Haar-filter inequalities

Write the fine sector masses as \(w_i,w_{ij},w_{123}\), according to
the exact set of traceless sites.  The one-site Haar-filter inequality
is
\[
 \frac14w_i-\frac12(w_{ij}+w_{ik})+w_{123}\geq0.
\tag{31}
\]
In the notation of (7)--(8),
\[
 w_{ij}+w_{ik}=f-p_i.
\]
Consequently (31), together with the covariance identity (16), is
equivalent to the pointwise covariance bound
\[
\boxed{\quad
 \|T_{0,i}^L-T_{0,i}^R\|_{HS}^2
 {}+f\|\rho_i^L-\rho_i^R\|_2^2
\leq 3w_i+12w_3.
\quad}
\tag{32}
\]
Thus the Haar filter does give a sitewise upper bound on the exact
commutator energy.  Summing (31) gives
\[
 f\leq 3w_3+\frac14w_1
 =\frac34-\frac34w_0-\frac{11}{16}w_1.
\tag{33}
\]
Filtering two sites also gives
\[
 p_i=w_{jk}\leq2w_3.
\tag{34}
\]

The formal model (25)--(29) survives all of these stronger
constraints.  Take the degree-one masses to vanish sitewise,
\(w_i=0\), and retain the uniform split \(p_i=2/9\).  Then each
instance of (31), or equivalently (32), is saturated:
\[
 -\frac12\left(\frac49\right)+\frac29=0,\qquad
 6(f-p_i)=\frac83=12w_3.
\tag{35}
\]
Equation (33) is likewise saturated by
\[
 \frac23
 =\frac34-\frac34\left(\frac19\right),
\]
while (34) holds with slack.  Hence neither the new pointwise
commutator-energy bound nor its summed sector consequence rules out
the exact negative formal model.

There is, however, a stronger equality datum not represented by
these scalar constraints.  The Haar inequality is obtained by
averaging nonnegative conditional endpoint forms.  If a physical
code saturates (31), then the unaveraged conditional form must vanish
for almost every filter direction, hence everywhere by continuity.
Classifying that continuum of equality conditions is a possible way
to recover the common-\(D\) information lost by averaging.

## 7. The smaller missing compatibility

The commutator maps in a physical solution obey identities absent
from the formal model.  For distinct sites,
\[
 [A_i,[B_j,D]]=[B_j,[A_i,D]]
 \qquad(i\ne j),
\tag{36}
\]
and on one site,
\[
 [A_i,[B_i,D]]-[B_i,[A_i,D]]
 =[[A,B]_i,D].
\tag{37}
\]
They also arise from the same degree-two decomposition (7), and
their parallel components are fixed by (17).

Therefore the remaining equality question has been reduced to the
following explicit lemma:

> **Lie-compatible six-map lemma.**  A normalized rank-two critical
> pair \(C,D=\Pi_2C\) with \(f=2/3\), all six one-site densities
> positive definite, and six boundary contractions cannot satisfy
> (1), (17), and the mixed derivation identities (36)--(37) when
> \(w_0+w_1>0\).

The norm identities proved here do not settle this lemma.  Any next
certificate must retain at least one mixed commutator moment, or an
equivalent common-\(D\) Gram tensor; separate or summed covariance
norms are now exactly known to be insufficient.

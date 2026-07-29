# A pointwise common-derivation filter inequality

## Status

This note records a matrix-valued necessary condition for a
hypothetical full-support qutrit three-copy pair-sector critical point.
It retains the actual common operator
\[
D=\Pi_2C
\]
and the derivations \(A\mapsto[A_i,D]\), rather than summing the six
left/right filter maps to scalar traces.

For every local matrix \(A\), the two one-site filter inequalities
combine to
\[
\boxed{
\begin{aligned}
&\|[A_i,D]\|_2^2-f|\ell(A)-r(A)|^2\\
&\quad+2\delta\bigl(r(B_L)^2+r(B_R)^2\bigr)\\
&\le\frac43\left(
{\cal N}_L(B_L,B_L)+{\cal N}_R(B_R,B_R)\right),
\end{aligned}}                                        \tag{1}
\]
where
\[
\begin{gathered}
f=\|D\|_2^2,\qquad \delta=f-\frac23,\\
\ell(A)=\operatorname{Tr}(A\rho^L_i),\qquad
r(A)=\operatorname{Tr}(A\rho^R_i),\\
B_L=A-\ell(A)I,\qquad B_R=A-r(A)I.
\end{gathered}                                         \tag{2}
\]
Here \(r(B)\) on the right side of (1) denotes spectral radius; it is
unrelated to the functional \(r(A)\) in (2).

There is also a sharper square-root form,
\[
\boxed{
\begin{aligned}
&\sqrt{\|[A_i,D]\|_2^2-f|\ell(A)-r(A)|^2}\\
&\le
\sqrt{\frac23{\cal N}_L(B_L,B_L)-\delta r(B_L)^2}\\
&\quad+
\sqrt{\frac23{\cal N}_R(B_R,B_R)-\delta r(B_R)^2}.
\end{aligned}}                                        \tag{3}
\]
Both statements hold pointwise for every complex \(A\in M_3\).

The commutator maps also obey exact same-site and cross-site
integrability identities.  These are polynomial constraints absent
from the earlier formal six-map covariance model.  Thus (1)--(3)
give a concrete matrix-valued replacement for the scalar trace route,
which has now been proved structurally incapable of reaching
\(f\le2/3\).

This note does not yet prove that (1)--(3) are inconsistent when
\(f>2/3\).

The independent checker is
`verification/verify_n3_common_derivation_filter_inequality.py`.

## 1. Critical maps and their common difference

Normalize \(\|C\|_2=1\), and define at site \(i\)
\[
\begin{aligned}
T_L(A)&=\Pi_2(A_iC),&
T_R(A)&=\Pi_2(CA_i),\\
{\cal N}_L(A,B)&=\operatorname{Tr}(A^\dagger B\rho_i^L),&
{\cal N}_R(A,B)&=\operatorname{Tr}(A^\dagger B\rho_i^R),
\end{aligned}                                         \tag{4}
\]
where
\[
\rho_i^L=\operatorname{Tr}_{\widehat i}(CC^\dagger),
\qquad
\rho_i^R=\operatorname{Tr}_{\widehat i}(C^\dagger C). \tag{5}
\]
The critical normal-space equations give
\[
\langle D,T_L(A)\rangle=f\ell(A),\qquad
\langle D,T_R(A)\rangle=fr(A).                         \tag{6}
\]
Define the residual maps
\[
X(A)=T_L(A)-\ell(A)D,\qquad
Y(A)=T_R(A)-r(A)D.                                    \tag{7}
\]
Their values are orthogonal to \(D\).

The scalar/traceless sector projection commutes with local
commutators, so the established common-origin identity is
\[
T_L(A)-T_R(A)=[A_i,D].                                 \tag{8}
\]
Subtracting the \(D\)-components in (7) gives the exact pointwise
identity
\[
\boxed{
X(A)-Y(A)=[A_i,D]-(\ell(A)-r(A))D.}                   \tag{9}
\]
Taking the inner product of (8) with \(D\) and using (6) shows that
the second term in (9) is exactly the orthogonal projection of the
commutator onto \(\mathbb CD\).  Therefore
\[
\boxed{
\|X(A)-Y(A)\|_2^2
=\|[A_i,D]\|_2^2-f|\ell(A)-r(A)|^2.}                  \tag{10}
\]

## 2. Combining the two filter inequalities

The centered matrices in (2) obey
\[
\operatorname{Tr}(B_L\rho_i^L)
=\operatorname{Tr}(B_R\rho_i^R)=0,                   \tag{11}
\]
and
\[
X(A)=X(B_L),\qquad Y(A)=Y(B_R).                       \tag{12}
\]
At a hypothetical critical point with \(f>2/3\), the exact
one-site canonical filter inequality on each side is
\[
\begin{aligned}
\|X(A)\|_2^2+\delta r(B_L)^2
&\le\frac23{\cal N}_L(B_L,B_L),\\
\|Y(A)\|_2^2+\delta r(B_R)^2
&\le\frac23{\cal N}_R(B_R,B_R).                       \tag{13}
\end{aligned}
\]

Define the nonnegative filter slacks
\[
\begin{aligned}
s_L(A)&=\frac23{\cal N}_L(B_L,B_L)
       -\|X(A)\|_2^2-\delta r(B_L)^2,\\
s_R(A)&=\frac23{\cal N}_R(B_R,B_R)
       -\|Y(A)\|_2^2-\delta r(B_R)^2.                 \tag{14}
\end{aligned}
\]
The parallelogram identity and (10) give the exact certificate
\[
\boxed{
\begin{aligned}
&\frac43\bigl({\cal N}_L(B_L,B_L)
              +{\cal N}_R(B_R,B_R)\bigr)\\
&\quad-\|[A_i,D]\|_2^2
      +f|\ell(A)-r(A)|^2\\
&\quad-2\delta\bigl(r(B_L)^2+r(B_R)^2\bigr)\\
&=2s_L(A)+2s_R(A)+\|X(A)+Y(A)\|_2^2.
\end{aligned}}                                        \tag{15}
\]
The right side is nonnegative, proving (1).  Equality in (1) occurs
exactly when both local filter inequalities saturate and
\[
X(A)=-Y(A).                                           \tag{16}
\]

The triangle inequality applied to (10), followed by (13), proves
(3).  It is generally stronger than (1), because (1) applies
\((u+v)^2\le2u^2+2v^2\).

If \(A\) belongs to the common centered hyperplane
\[
\ell(A)=r(A)=0,
\]
then \(B_L=B_R=A\), and (1) simplifies to
\[
\boxed{
\|[A_i,D]\|_2^2+4\delta r(A)^2
\le\frac43\operatorname{Tr}
\left(A^\dagger A(\rho_i^L+\rho_i^R)\right).}          \tag{17}
\]

For the rank-one projector \(P_z=|z\rangle\langle z|\), put
\[
t_L=\langle z,\rho_i^Lz\rangle,\qquad
t_R=\langle z,\rho_i^Rz\rangle,\qquad
m(t)=\max\{t,1-t\}.
\]
Since
\[
\begin{aligned}
r(P_z-tI)&=m(t),\\
{\cal N}(P_z-tI,P_z-tI)&=t(1-t),
\end{aligned}
\]
equation (1) gives the explicit continuum of physical constraints
\[
\boxed{
\begin{aligned}
&\|[P_z^{(i)},D]\|_2^2-f(t_L-t_R)^2\\
&\quad+2\delta\bigl(m(t_L)^2+m(t_R)^2\bigr)\\
&\le\frac43\bigl(t_L(1-t_L)+t_R(1-t_R)\bigr)
\qquad(\|z\|=1).
\end{aligned}}                                        \tag{18}
\]

## 3. The commutator Gram operator

The left side of (10), as \(A\) varies, is not an arbitrary positive
quadratic form.  Let
\[
R_L=\operatorname{Tr}_{\widehat i}(DD^\dagger),\qquad
R_R=\operatorname{Tr}_{\widehat i}(D^\dagger D),       \tag{19}
\]
and define
\[
\begin{aligned}
\Phi_D(A)&=\operatorname{Tr}_{\widehat i}(D A_iD^\dagger),\\
\Psi_D(A)&=\operatorname{Tr}_{\widehat i}(D^\dagger A_iD).
\end{aligned}                                         \tag{20}
\]
For the derivation
\[
{\mathscr C}_i(A)=[A_i,D],
\]
direct contraction gives the exact positive Gram superoperator
\[
\boxed{
{\mathscr C}_i^\dagger{\mathscr C}_i(A)
=A R_L+R_R A-\Phi_D(A)-\Psi_D(A).}                    \tag{21}
\]
If \(|\Delta\rho_i\rangle\!\rangle\) denotes vectorization of
\(\Delta\rho_i=\rho_i^L-\rho_i^R\), then (9)--(10) become the
operator identity
\[
\boxed{
(X-Y)^\dagger(X-Y)
={\mathscr C}_i^\dagger{\mathscr C}_i
-f|\Delta\rho_i\rangle\!\rangle
  \langle\!\langle\Delta\rho_i|.}                     \tag{22}
\]
This is a full \(9\times9\) positive-semidefinite constraint at every
site, not merely its trace.

## 4. Derivation and cross-site integrability

For all \(A,B\in M_3\), the maps
\({\mathscr C}_i(A)=[A_i,D]\) obey the Leibniz identity
\[
\boxed{
{\mathscr C}_i(AB)
=A_i{\mathscr C}_i(B)+{\mathscr C}_i(A)B_i.}           \tag{23}
\]
At the same site, their curvature identity is
\[
\boxed{
[A_i,{\mathscr C}_i(B)]
-[B_i,{\mathscr C}_i(A)]
={\mathscr C}_i([A,B]).}                              \tag{24}
\]
At distinct sites \(i\ne j\), local matrices commute, and the Jacobi
identity gives
\[
\boxed{
[A_i,{\mathscr C}_j(B)]
=[B_j,{\mathscr C}_i(A)].}                            \tag{25}
\]

Equations (21)--(25) express the missing common-frame geometry
precisely.  A collection of six abstract maps can satisfy all
individual filter inequalities, summed norms, and covariance traces
while failing these identities.  Any exact critical countermodel must
now realize one common \(D\) and these derivations, in addition to the
scalar constraints.

## 5. Remaining explicit problem

The full-support interior exclusion is reduced further to the
following matrix-valued feasibility question:

> Can a normalized rank-two \(C\), with \(D=\Pi_2C\) and \(f>2/3\),
> satisfy the critical normal equations, all six one-site filter
> inequalities, the pointwise common-derivation inequalities
> (1)--(3), and the integrability identities (21)--(25)?

Unlike the earlier scalar trace system, this question retains every
commutator of the common degree-two tensor \(D\).  A useful next step
would be an exact lower bound for the operator in (22) on the
left/right common-centered hyperplanes, or an \(S_3\)-coupled
certificate obtained from the cross-site identities (25).

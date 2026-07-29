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

## 6. Exact obstruction: even the common derivations are insufficient

The restrictions above are genuinely stronger than the scalar
covariance identities, but they still do not by themselves close the
problem.  This section constructs an exact formal critical model which
has one physical degree-two operator \(D\), hence satisfies every
derivation and integrability identity, while passing all pointwise
filter inequalities and all earlier trace arithmetic for
\[
\boxed{\frac23\le f\le\frac{24}{31}.}                  \tag{26}
\]
The remaining nonphysical freedom lies only in the symmetric
left/right residual sum.

Let \(F_1,\ldots,F_8\) be a Hilbert--Schmidt orthonormal traceless
Hermitian qutrit basis and put \(J=I/\sqrt3\).  Define the three
orthogonal pair Casimirs
\[
\begin{aligned}
\Omega_{12}&=\sum_aF_a\otimes F_a\otimes J,\\
\Omega_{13}&=\sum_aF_a\otimes J\otimes F_a,\\
\Omega_{23}&=\sum_aJ\otimes F_a\otimes F_a,
\end{aligned}                                         \tag{27}
\]
and
\[
D_*=\frac16(\Omega_{12}+\Omega_{13}+\Omega_{23}).
\tag{28}
\]
Each \(\Omega_{ij}\) has squared norm \(8\), so
\[
\|D_*\|_2^2=3\frac8{36}=\frac23.                      \tag{29}
\]
For the desired value of \(f\), scale
\[
D_f=\sqrt{\frac{3f}{2}}\,D_*.
\]

The qutrit adjoint Casimir identity is
\[
\sum_{a=1}^8
\langle[A,F_a],[B,F_a]\rangle
=6\langle A_0,B_0\rangle,\qquad
A_0=A-\frac{\operatorname{Tr}A}{3}I.                 \tag{30}
\]
To check it directly, Hilbert--Schmidt completeness gives
\[
\sum_aF_aXF_a=\operatorname{Tr}(X)I-\frac13X,
\qquad
\sum_aF_a^2=\frac83I.
\]
Expanding the four terms in the two commutators then gives
\[
6\operatorname{Tr}(A^\dagger B)
-2\overline{\operatorname{Tr}A}\operatorname{Tr}B
=6\langle A_0,B_0\rangle.
\]
At a fixed site, two of the three orthogonal pair sectors in (27)
are nontrivial.  Equations (28)--(30) therefore give the complete
commutator Gram
\[
\boxed{
\langle[A_i,D_f],[B_i,D_f]\rangle
=\frac f2\langle A_0,B_0\rangle.}                     \tag{31}
\]
In particular, these are actual commuting local derivations of the
one common physical tensor \(D_f\).

Set the six formal one-site densities to
\[
\rho_i^L=\rho_i^R=\frac13I.                            \tag{32}
\]
The operator \(D_f\) is Hermitian, so the operator covariance
condition involving \(\rho_i^L-\rho_i^R\) is satisfied.

The operator Hilbert space \(M_{27}\) has dimension \(729\).  The
span of \(D_f\) and the twenty-four commutator vectors
\([F_a^{(i)},D_f]\) has dimension at most \(25\).  Choose twenty-four
orthonormal vectors \(e_{ia}\) in its orthogonal complement, and
define, on the traceless basis,
\[
Z_i(F_a)=\sqrt{\frac{5f}{72}}\,e_{ia},\qquad Z_i(I)=0. \tag{33}
\]
Now put
\[
\begin{aligned}
X_i(A)&=Z_i(A_0)+\frac12[A_i,D_f],\\
Y_i(A)&=Z_i(A_0)-\frac12[A_i,D_f],                    \tag{34}\\
T_i^L(A)&=\frac{\operatorname{Tr}A}{3}D_f+X_i(A),\\
T_i^R(A)&=\frac{\operatorname{Tr}A}{3}D_f+Y_i(A).
\end{aligned}
\]
Then \(X_i,Y_i\perp D_f\), and
\[
T_i^L(A)-T_i^R(A)=[A_i,D_f].                          \tag{35}
\]
Thus all identities (6)--(10) and (21)--(25) hold exactly.

For every traceless \(B\), equations (31), (33)--(34) give
\[
\|X_i(B)\|_2^2=\|Y_i(B)\|_2^2
=\frac{7f}{36}\|B\|_2^2.                              \tag{36}
\]
Every complex traceless \(3\times3\) matrix obeys
\[
r(B)^2\le\frac23\|B\|_2^2.                            \tag{37}
\]
Indeed, choose a unit eigenvector of \(B\), extend it to an
orthonormal basis, and repeat on the lower-right compression.  This
inductively produces a unitary upper-triangular representation whose
diagonal entries are the eigenvalues.  Hence
\(\|B\|_2^2\ge\sum_j|\lambda_j|^2\).  If
\(|\lambda_1|=r(B)\), then
\(\lambda_2+\lambda_3=-\lambda_1\), so
\[
|\lambda_2|^2+|\lambda_3|^2\ge\frac12|\lambda_1|^2.
\]
This proves (37).

Using (36)--(37), each canonical filter inequality follows from
\[
\frac{7f}{36}
+\frac23\left(f-\frac23\right)
\le\frac29,
\]
which is exactly \(f\le24/31\).  Hence the full pointwise inequalities
(1)--(3), not only their traces, hold throughout (26).

Finally assign the formal sector masses
\[
(w_0,w_1,w_2,w_3)=(1-f,0,f,0).                        \tag{38}
\]
For every site,
\[
\operatorname{Tr}_{HS}(T_i^{L\dagger}T_i^L)
=\operatorname{Tr}_{HS}(T_i^{R\dagger}T_i^R)
=\frac{17f}{9},
\]
so the three-site trace is \(17f/3\), exactly the common-origin
sector formula for (38).  Moreover
\[
\begin{aligned}
\sum_i\|X_i\|_{HS}^2
&=\sum_i\|Y_i\|_{HS}^2=\frac{14f}{3},\\
\operatorname{Re}\sum_i\langle X_i,Y_i\rangle_{HS}
&=-\frac{4f}{3},\\
\sum_i\|X_i-Y_i\|_{HS}^2&=12f,
\end{aligned}                                         \tag{39}
\]
which are exactly the earlier residual norm, cross-trace, and
covariance identities at the maximally mixed densities.

This model is not asserted to come from a rank-two \(C\).  Its
importance is diagnostic: even an actual common \(D\), its complete
commutator Gram, every derivation/integrability identity, every
pointwise filter inequality, and all scalar sector arithmetic leave
formal negative critical data through \(f=24/31\).  What remains
unencoded is the symmetric part
\[
T_i^L(A)+T_i^R(A)
=\Pi_2(A_iC+CA_i),
\]
which must arise, simultaneously at all sites, from one common
rank-two \(C\).  That anticommutator/common-\(C\) geometry is the next
strictly smaller target.

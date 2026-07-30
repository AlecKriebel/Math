# The symmetric-cube third-minor family is insufficient

## Status

The rank-two identity
\[
 \det\left(
 \langle x_r^{\otimes3},C\,y_s^{\otimes3}\rangle
 \right)_{r,s=0}^2=0
\tag{1}
\]
does detect the first invariant high-rank stationary model.  However,
the entire family (1), including all of its polarizations and frame
averages, is still insufficient.

This note gives one exact operator \(C_\star\) with all of the
following properties:

1. \(x=a=0\) and its negative depth is
   \[
     \delta=\frac1{14}<\frac18;
   \]
2. all six local endpoint, pair-sector, and depth Euler forms are
   isotropic, site-independent, and have positive Hessians;
3. all local maps arise from the same \(C_\star\), so every cyclic
   multiplication and commutator identity holds;
4. nevertheless
   \[
     P_{\mathrm{Sym}^3}C_\star
     P_{\mathrm{Sym}^3}=0.
   \]

Consequently every matrix in (1) is identically zero.  Averaging
\(|\det|^2\), polarizing the determinant within the symmetric-cube
orbit, or extracting scalar purity inequalities from that average
cannot distinguish \(C_\star\) from rank two.

The operator has high rank and is not a Werner witness.  The exact
obstruction says that the next third-compound certificate must use
independently polarized product tensors
\[
 x_{r1}\otimes x_{r2}\otimes x_{r3},
\]
not only diagonal cubes \(x_r^{\otimes3}\).

The exact checker is
`verification/verify_n3_cyclic_stationary_high_rank_obstruction.py`.

## 1. Construction

Retain the flips \(F_{ij}\) and cycles \(V,V^{-1}\) from
`agent_n3_cyclic_stationary_high_rank_obstruction.md`.  Let
\(\omega\) be a primitive cube root of unity:
\[
 \omega^3=1,\qquad 1+\omega+\omega^2=0.
\tag{2}
\]
Define
\[
\begin{aligned}
 A_2&=
 \left(F_{12}-\frac13I\right)
 +\omega\left(F_{23}-\frac13I\right)
 +\omega^2\left(F_{13}-\frac13I\right),\\
 A_3&=V-V^{-1}.
\end{aligned}
\tag{3}
\]
The scalar terms in \(A_2\) cancel by (2).  Each displayed flip
minus \(I/3\) is pure degree two, while \(V,V^{-1}\) have identical
degree-zero and degree-two projections.  Therefore
\[
 \Pi_2A_2=A_2,\qquad \Pi_3A_3=A_3.
\tag{4}
\]
The three fine degree-two terms are orthogonal and have squared norm
24.  Direct permutation contraction gives
\[
\boxed{
 \|A_2\|_2^2=72,\qquad
 \|A_3\|_2^2=48,\qquad
 \langle A_2,A_3\rangle=0.
 }
\tag{5}
\]

Set
\[
\boxed{
 C_\star=A_2+\sqrt{\frac35}\,A_3.
 }
\tag{6}
\]
Its sector masses are
\[
\boxed{
 x=a=0,\qquad
 c=72,\qquad
 d=\frac{144}{5},\qquad
 N=\|C_\star\|^2=\frac{504}{5}.
 }
\tag{7}
\]
Hence
\[
\begin{aligned}
 Q_3(C_\star)
 &=-\frac12c+d=-\frac{36}{5},\\
 \sigma(C_\star)
 &=2Q_3(C_\star)+3c=\frac{1008}{5},\\
 \delta
 &:=-\frac{2Q_3(C_\star)}{\sigma(C_\star)}
 =\boxed{\frac1{14}}.
\end{aligned}
\tag{8}
\]

## 2. Exact uniform local stationarity

Both \(A_2,A_3\), and hence \(C_\star\), commute with
\(U^{\otimes3}\) for every unitary \(U\).  As in the preceding note,
every one-site form is therefore scalar on the scalar line and on the
traceless matrices.  Although \(C_\star\) is not invariant under all
site permutations, the three degree-two coefficients in (3) have
equal modulus.  Exact contraction makes the local spectra
site-independent.

Let
\[
\begin{aligned}
 h_i^{L}(A,B)
 &=\langle A_iC_\star,L^{\otimes3}(B_iC_\star)\rangle,\\
 k_i^{L}(A,B)
 &=\langle\Pi_2(A_iC_\star),\Pi_2(B_iC_\star)\rangle,
\end{aligned}
\tag{9}
\]
and define the right forms similarly.  For every site and both
orientations, their eigenvalues are
\[
\boxed{
\begin{array}{c|cc}
 &\text{scalar}&\text{traceless}\\ \hline
 n_i&168/5&168/5\\
 h_i&-12/5&93/10\\
 k_i&24&76/5.
\end{array}}
\tag{10}
\]
Here \(n_i(A,B)=\langle A_iC_\star,B_iC_\star\rangle\).

For transparency, the degree-two part of the traceless contractions
is diagonal in the three fine pair sectors.  At one site its endpoint
diagonal is a permutation of
\[
 \left(-\frac{13}{4},-\frac{13}{4},8\right),
\]
and its pair-sector diagonal is a permutation of
\[
 (7,7,0).
\]
The degree-three contribution, multiplied by \(3/5\), is respectively
\[
 \frac35(13),\qquad \frac35(2).
\]
This gives \(93/10\) and \(76/5\) in (10) at every site.  All mixed
degree-two/degree-three contractions vanish.

The normalized endpoint and pair-sector quotient values are
\[
 q=\frac{Q_3(C_\star)}N=-\frac1{14},\qquad
 f=\frac cN=\frac57.
\tag{11}
\]
Equations (10)--(11) give the exact Hessian spectra
\[
\boxed{
\begin{array}{c|cc}
 &\text{scalar}&\text{traceless}\\ \hline
 h_i-qn_i&0&117/10\\
 fn_i-k_i&0&44/5\\
 2(1+\delta)h_i+3\delta k_i&0&1623/70.
\end{array}}
\tag{12}
\]
Thus every left and right one-site Euler equation holds, and all
three complete local Hessians are positive with precisely the scalar
kernel.

## 3. Every symmetric-cube minor vanishes

Let \(P_{\rm sym}\) project onto
\(\mathrm{Sym}^3(\mathbb C^3)\).  Every flip and both cycles act as
the identity on this subspace.  Equations (2)--(3) therefore give
\[
 A_2P_{\rm sym}
 =(1+\omega+\omega^2)P_{\rm sym}=0,
\qquad
 A_3P_{\rm sym}=(1-1)P_{\rm sym}=0.
\tag{13}
\]
The same equations hold on the left, so
\[
\boxed{
 P_{\rm sym}C_\star P_{\rm sym}=0.
 }
\tag{14}
\]

For arbitrary \(x,y\in\mathbb C^3\),
\[
 x^{\otimes3},y^{\otimes3}\in\mathrm{Sym}^3(\mathbb C^3).
\]
Hence (14) gives the stronger entrywise identity
\[
\boxed{
 \langle x^{\otimes3},C_\star y^{\otimes3}\rangle=0
 \qquad(x,y\in\mathbb C^3).
 }
\tag{15}
\]
Every determinant (1) is therefore zero before taking the
determinant.

In particular, for every choice of left and right Haar frames,
\[
 \left|\det\left(
 \langle x_r^{\otimes3},C_\star y_s^{\otimes3}\rangle
 \right)\right|^2=0.
\tag{16}
\]
Its average, every weighted frame average, and every polarization
which remains inside the symmetric-cube subspace also vanish.

## 4. Exact limitation and the next finite family

The construction is not rank two.  The point of (15) is that the
symmetric-cube third-minor family cannot see why.

Pure cubes span only the ten-dimensional symmetric subspace of the
27-dimensional three-qutrit space.  Thus (1) tests only
\[
 \operatorname{rank}(P_{\rm sym}CP_{\rm sym})\leq2,
\]
not \(\operatorname{rank}C\leq2\).

A separating third-compound family must allow independent local
polarization.  One finite version is
\[
\boxed{
 \det\left(
 \left\langle
 x_{r1}\otimes x_{r2}\otimes x_{r3},\,
 C\,
 y_{s1}\otimes y_{s2}\otimes y_{s3}
 \right\rangle
 \right)_{r,s=0}^2=0,
 }
\tag{17}
\]
for independently chosen local triples.  Product tensors span the
whole physical space, so the complete family (17) is equivalent to
\(\wedge^3C=0\).  The remaining problem is to select and average a
small enough polarized subfamily that still couples to the local
Hessian invariants without collapsing to (16).

## 5. Consequences for the six-purity and Haar-\({\cal R}\) routes

Let \(D=\Pi_2C_\star\), \(c=\|D\|^2=72\), and define the six
pair-centered Hermitian matrices
\[
\begin{aligned}
 H_i^L&=\frac1c\operatorname{Herm}
 \operatorname{Tr}_{\widehat i}(C_\star D^\dagger),\\
 H_i^R&=\frac1c\operatorname{Herm}
 \operatorname{Tr}_{\widehat i}(D^\dagger C_\star).
\end{aligned}
\tag{18}
\]
The products inside every partial trace commute with
\(U^{\otimes3}\).  Their one-site reductions therefore commute with
every qutrit unitary and are scalar.  Since every \(H_i^{L,R}\) has
trace one,
\[
\boxed{
 H_i^L=H_i^R=\frac13I_3
 \qquad(i=1,2,3).
 }
\tag{19}
\]
Consequently
\[
 \sum_{i=1}^3
 \left(\|H_i^L\|_2^2+\|H_i^R\|_2^2\right)=2.
\tag{20}
\]

For this model
\[
 \lambda=\frac{Q_3(C_\star)}c=-\frac1{10}.
\tag{21}
\]
Thus the normalized six-purity candidate
\[
 \sum_i(\|H_i^L\|^2+\|H_i^R\|^2)
 \stackrel{?}{\geq}3-\frac{\lambda}{2}
\tag{22}
\]
would read
\[
 2\geq\frac{61}{20},
\]
which is false.  This does not refute (22) on rank-two matrices;
\(C_\star\) has high rank.  It proves that no derivation of (22) can
use only the symmetric-cube minors, the six local stationary forms,
and cyclic compatibility, because \(C_\star\) satisfies all of those
inputs.

There is also no universal linear scalar inequality which controls
the positive purity excess of a trace-one Hermitian \(H\) by the Haar
functional \({\cal R}(H)\).  Take
\[
 H_t=\operatorname{diag}\left(\frac12+t,\frac12,-t\right),
 \qquad t>0.
\tag{23}
\]
Then
\[
\begin{aligned}
 \operatorname{Tr}H_t^2-\frac12
 &=t+2t^2,\\
 {\cal R}(H_t)
 &=\frac{t^2}{\frac12+2t}
 =\frac{2t^2}{1+4t}.
\end{aligned}
\tag{24}
\]
Therefore
\[
\boxed{
 \frac{\operatorname{Tr}H_t^2-\frac12}{{\cal R}(H_t)}
 =
 \frac1{2t}+3+4t.
 }
\tag{25}
\]
The ratio diverges as \(t\downarrow0\) and as \(t\to\infty\).
Hence there is no finite constant \(K\) such that
\[
 \left(\operatorname{Tr}H^2-\frac12\right)_+
 \leq K{\cal R}(H)
\tag{26}
\]
for all trace-one Hermitian \(3\times3\) matrices.

The obstruction is sharp at the qualitative level:
\[
 {\cal R}(H)=0
 \quad\Longleftrightarrow\quad
 0\preceq H\preceq\frac12I
\tag{27}
\]
for trace-one Hermitian \(H\).  Indeed, the divided-difference
integral is zero exactly when \(\lambda_{\max}(H)\leq1/2\).  If all
three eigenvalues are at most \(1/2\) and sum to one, none can be
negative.  Conversely (27) makes the truncated Haar integrand zero.
It follows that \({\cal R}=0\) implies
\(\operatorname{Tr}H^2\leq1/2\), but (25) rules out a linear
quantitative strengthening without an additional spectral bound or
a genuinely six-matrix coupling.

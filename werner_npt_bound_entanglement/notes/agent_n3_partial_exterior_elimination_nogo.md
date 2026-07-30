# Partial-contraction exterior bounds and their exact scalar limitation

## Status

This note retains the nuclear/exterior mass of each one-site partial
trace and proves its natural factorization bound through the common
left and right singular planes.  Eliminating the three exterior masses
independently gives the exact aggregate inequality
\[
\boxed{\qquad
 1072R+20S
 \geq1260c+2835a+90\Delta .
\qquad}                                                   \tag{1}
\]
Here \(R,S,a,c\) are the quantities in the common trace/slack theorem
and \(\Delta=(s_1-s_2)^2\).

This does not strengthen the explicit negative-depth bound
\(\delta<3/22\).  In negative-depth simplex variables, (1) becomes
\[
 940\delta+177(1-5\delta)L+315a+10\Delta\leq132,         \tag{2}
\]
and the common global trace inequality implies (2) coefficient by
coefficient.  An exact negative scalar model satisfies all the
resulting inequalities.  Therefore the three contraction exterior
masses cannot be discarded separately.  A successful use of them must
retain their shared qutrit Hodge alignment, precisely the cyclic
information absent from the abstract face model.

This is a no-go result for one elimination route, not a negative
Werner witness.  The dependency-free exact checker is
`verification/verify_n3_partial_exterior_elimination_nogo.py`.

## 1. Exterior mass of a partial trace

Let
\[
 T_i=\operatorname{Tr}_iC,\qquad
 n_i=\|T_i\|_2^2,
\]
and let \(\tau_{i,1},\ldots,\tau_{i,6}\) be its singular values,
padded by zeros.  Define
\[
 \pi_i=\sum_{r<s}\tau_{i,r}\tau_{i,s}
      =\|\wedge^2T_i\|_1.                                \tag{3}
\]
The trace is unchanged by the partial trace, and
\[
 \|T_i\|_1^2=n_i+2\pi_i.
\]
Hence
\[
\boxed{\qquad
 n_i+2\pi_i-|\operatorname{Tr}C|^2\geq0.
\qquad}                                                   \tag{4}
\]

The exact rank-six trace slack satisfies
\[
 r_i=\frac{6n_i-|\operatorname{Tr}C|^2}{12}.             \tag{5}
\]
Eliminating the common trace between (4) and (5) gives
\[
\boxed{\qquad
 12r_i+2\pi_i\geq5n_i.
\qquad}                                                   \tag{6}
\]
Unlike \(r_i\geq0\), this formula has not yet replaced \(\pi_i\) by
the worst rank-six estimate.

## 2. Common singular-plane factorization

Write a singular-value decomposition
\[
 C=\sum_{\rho=1}^2s_\rho|u_\rho\rangle\langle v_\rho|.
\]
For site \(i\), define slice maps from
\(\mathbb C^3\otimes\mathbb C^2\) to the complementary two-qutrit
space by
\[
\begin{aligned}
 A_i(|a\rangle|\rho\rangle)
 &=\sqrt{s_\rho}\,(\langle a|_i u_\rho),\\
 B_i(|a\rangle|\rho\rangle)
 &=\sqrt{s_\rho}\,(\langle a|_i v_\rho).
\end{aligned}                                             \tag{7}
\]
Direct contraction gives
\[
 T_i=A_iB_i^\dagger.                                     \tag{8}
\]
The exterior functor and Schatten Hölder inequality therefore give
\[
\begin{aligned}
 \pi_i
 &=\|(\wedge^2A_i)(\wedge^2B_i)^\dagger\|_1\\
 &\leq
 \|\wedge^2A_i\|_2\,\|\wedge^2B_i\|_2.                  \tag{9}
\end{aligned}
\]
Both slice maps have squared Hilbert--Schmidt norm
\[
 \|A_i\|_2^2=\|B_i\|_2^2=s_1+s_2=:t.                   \tag{10}
\]
For any rank-at-most-six map \(A\), if the squared singular values are
\(\mu_1,\ldots,\mu_6\), then
\[
\begin{aligned}
 \|\wedge^2A\|_2^2
 &=\sum_{r<s}\mu_r\mu_s\\
 &=\frac12\left[\left(\sum_r\mu_r\right)^2
                 -\sum_r\mu_r^2\right]\\
 &\leq\frac5{12}\left(\sum_r\mu_r\right)^2.             \tag{11}
\end{aligned}
\]
The last step is Cauchy--Schwarz
\(\sum_r\mu_r^2\geq(\sum_r\mu_r)^2/6\).
Equations (9)--(11) prove
\[
\boxed{\qquad
 \pi_i\leq\frac5{12}(s_1+s_2)^2
 =\frac5{12}(2N-\Delta),
\qquad}                                                   \tag{12}
\]
where
\[
 N=\|C\|_2^2,\qquad
 \Delta=(s_1-s_2)^2.
\]

The important information lost in (12) is the relative alignment of
the three pairs
\[
 (\wedge^2A_i,\wedge^2B_i),\qquad i=1,2,3.
\]
These maps are three Hodge views of the same two singular planes, not
six independent rank-six maps.

## 3. Aggregate elimination

Summing (6) over the three sites and applying (12) gives
\[
 12R+\frac52(2N-\Delta)
 \geq5\sum_i n_i.                                       \tag{13}
\]
In sector masses,
\[
 \sum_i n_i=9x+6a+3c.                                   \tag{14}
\]
Substitute
\[
\begin{aligned}
 x&=\frac23c+\frac43a-\frac49R,\\
 d&=\frac19S-\frac1{12}a+\frac13c,\\
 N&=x+a+c+d.
\end{aligned}
\]
After clearing the denominator \(36\), equation (13) is exactly (1):
\[
 1072R+20S-1260c-2835a-90\Delta\geq0.                  \tag{15}
\]

## 4. Comparison on the negative-depth simplex

For a normalized negative direction put
\[
 u=(1-5\delta)L.
\]
The exact simplex identities are
\[
 c=\frac{1+\delta}{3},\qquad
 R=\frac32(1-5\delta-u),\qquad
 S=\frac34u.                                             \tag{16}
\]
Substitution in (1) gives
\[
\boxed{\qquad
 940\delta+177u+315a+10\Delta\leq132.
\qquad}                                                   \tag{17}
\]
The common global trace theorem gives
\[
\boxed{\qquad
 1584\delta+297u+567a+18\Delta\leq216.
\qquad}                                                   \tag{18}
\]
Multiply (18) by \(11/18\).  Its left side exceeds the left
side of (17) by
\[
\boxed{\qquad
 28\delta+\frac92u+\frac{63}{2}a+\Delta\geq0,
\qquad}                                                   \tag{19}
\]
while its right side becomes \(132\).  Thus (18) implies (17)
coefficient by coefficient.  Independent elimination of the three
partial exterior masses supplies no new scalar restriction at all.

## 5. Exact negative scalar model

The limitation is not merely a comparison of constants.  Take
\[
\delta=\frac1{10},\qquad
 L=\frac1{10},\qquad
 a=\frac1{24},\qquad
 \Delta=0.
\tag{20}
\]
Thus \(u=(1-5\delta)L=1/20\).  The induced exact sector and slack data
are
\[
\begin{aligned}
 x&=0,&
 c&=\frac{11}{30},&
 d&=\frac{59}{480},&
 N&=\frac{17}{32},\\
 R&=\frac{27}{40},&
 S&=\frac3{80},&
 Q_3&=-\frac1{20},&
 p&=\frac{17}{64}.
\end{aligned}                                             \tag{21}
\]
Split \(a,c,R,S\) equally among the three sites and choose
\[
 \theta_i=\frac13,\qquad \lambda_i=\frac1{10}.
\]
Then
\[
 a_i=\frac1{72},\quad c_i=\frac{11}{90},\quad
 r_i=\frac9{40},\quad s_i=\frac1{80}.                  \tag{22}
\]
Every sector mass and every face slack is nonnegative, while the
assigned endpoint is negative.  The global and partial-exterior
left sides in (18) and (17) are respectively
\[
 \frac{1575}{8}<216,\qquad
 \frac{4639}{40}<132.                                   \tag{23}
\]
One may take the formal partial exterior masses \(\pi_i=0\), since
\[
 n_i=\frac9{20},\qquad
 |\operatorname{Tr}C|^2=0,
\]
and (4), (6), and (12) all hold.

These numbers are not asserted to come from a single rank-two matrix.
They prove exactly that sector nonnegativity, the face slacks, the
global exterior mass, and the three separately eliminated contraction
exterior masses do not force \(Q_3\geq0\).  The next inequality must
couple their three exterior factorizations through the shared
qutrit Hodge channel.


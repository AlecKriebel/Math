# A common rank-two trace tradeoff for the three face slacks

## Status

This note proves an exact nonlinear realizability constraint on the six
face slacks in the unrestricted three-copy problem.  It does not prove
unrestricted positivity.

Let
\[
 R=\sum_{i=1}^3r_i,\qquad S=\sum_{i=1}^3s_i
\]
be the rank-six trace and block-Haar slacks from the exact two-face
theorem.  If \(a,c\) denote respectively the total one-traceless and
two-traceless sector masses of a rank-at-most-two coefficient matrix
\(C\), then
\[
\boxed{\qquad
 200R+4S\ \geq\ 252c+567a+18\Delta ,
\qquad}                                                   \tag{1}
\]
where
\[
 \Delta=(s_1(C)-s_2(C))^2
\]
(with \(s_2=0\) in the rank-one case).  More precisely, before
discarding either the polar-alignment or singular-value-imbalance
defect, the exact identity is
More precisely, the difference in (1) is exactly eighteen times the
global rank-two trace deficit:
\[
\boxed{\qquad
 200R+4S-252c-567a
 =18\left(2\|C\|_2^2-|\operatorname{Tr}C|^2\right).
\qquad}                                                   \tag{2}
\]

Thus the abstract isotropic frame obstruction
\[
 R=S=0,\qquad c>0
\]
cannot come from one physical rank-two matrix.  This is the first
explicit common-\(C\) constraint excluding that model; the separate
face certificates do not imply it.

Any negative endpoint candidate is confined to the strict band
\[
\boxed{\qquad
 \frac{27}{22}c+\frac{63}{22}a+\frac1{11}\Delta
 <R<\frac92c,
 \qquad 63a+2\Delta<72c .
\qquad}                                                   \tag{3}
\]
Equality in the strengthened inequality (1), for nonzero \(C\),
forces \(C\), up to scalar phase, to be positive semidefinite of rank
at most two.  Such matrices are already known to obey the stronger
estimate \(Q_3(C)\geq\Delta/8\).  Hence every negative candidate
satisfies (1) strictly.  Equality in the weaker inequality obtained
by omitting \(18\Delta\) further forces \(\Delta=0\), hence a scalar
multiple of a rank-two orthogonal projection.

The dependency-free exact checker is
`verification/verify_n3_common_trace_slack_tradeoff.py`.

## 1. Sector notation

Decompose \(C\) orthogonally according to which local qutrit operator
factors are scalar or traceless.  Write
\[
\begin{aligned}
 x&=\|\Pi_0C\|_2^2,\\
 a_i&=\|\Pi_{\{i\}}C\|_2^2,\qquad
 a=\sum_i a_i,\\
 c_i&=\|\Pi_{\{1,2,3\}\setminus\{i\}}C\|_2^2,\qquad
 c=\sum_i c_i,\\
 d&=\|\Pi_3C\|_2^2 .
\end{aligned}                                             \tag{4}
\]
Then
\[
 \|C\|_2^2=x+a+c+d,\qquad
 |\operatorname{Tr}C|^2=27x,                            \tag{5}
\]
and
\[
 Q_3(C)=-\frac18x+\frac14a-\frac12c+d.                  \tag{6}
\]

For a fixed site \(i\), let \(\{j,k\}\) be its complement.  The
partial trace \(T_i=\operatorname{Tr}_iC\) retains only sectors which
are scalar on site \(i\), and multiplies their squared norms by three.
Consequently
\[
\begin{aligned}
 \|T_i\|_2^2
 &=3(x+a_j+a_k+c_i),\\
 t_i:=Q_2(T_i)
 &=\frac34x-\frac32(a_j+a_k)+3c_i,\\
 w_i&=3c_i.
\end{aligned}                                             \tag{7}
\]
The two exact face slacks are
\[
 r_i=\frac32w_i-t_i,\qquad
 s_i=3q_i-t_i,                                           \tag{8}
\]
where
\[
 q_i=\frac14(x+a_i)
 -\frac12(a_j+a_k+c_j+c_k)+c_i+d.                       \tag{9}
\]
Substitution gives
\[
\boxed{
\begin{aligned}
 r_i&=\frac32c_i+\frac32(a_j+a_k)-\frac34x,\\
 s_i&=3d+\frac34a_i-\frac32(c_j+c_k).
\end{aligned}}                                           \tag{10}
\]
Summing over the three sites yields
\[
\boxed{
\begin{aligned}
 R&=\frac32c+3a-\frac94x,\\
 S&=9d+\frac34a-3c.
\end{aligned}}                                           \tag{11}
\]

## 2. Exact conversion of the global trace deficit

Solving (11) for the scalar and fully traceless masses gives
\[
\begin{aligned}
 x&=\frac23c+\frac43a-\frac49R,\\
 d&=\frac19S-\frac1{12}a+\frac13c.
\end{aligned}                                             \tag{12}
\]
Therefore
\[
\begin{aligned}
 2\|C\|_2^2-|\operatorname{Tr}C|^2
 &=2(x+a+c+d)-27x\\
 &=\frac{100}{9}R+\frac29S
   -14c-\frac{63}{2}a.                                  \tag{13}
\end{aligned}
\]
Multiplication by \(18\) proves the identity (2).

If \(\operatorname{rank}C\leq2\), then
\[
 |\operatorname{Tr}C|
 \leq\|C\|_1
 =s_1+s_2.                                               \tag{14}
\]
Writing \(N=\|C\|_2^2=s_1^2+s_2^2\), this gives
\[
\begin{aligned}
 2N-|\operatorname{Tr}C|^2
 &=(N-2s_1s_2)
   +(N+2s_1s_2-|\operatorname{Tr}C|^2)\\
 &\geq(s_1-s_2)^2=\Delta.                               \tag{15}
\end{aligned}
\]
Equations (2) and (15) prove (1).

This implication is genuinely common-origin.  The individual
nonnegative quantities \(r_i,s_i\) do not encode the global trace and
norm in (14).  In particular, if \(R=S=0\), (1) forces
\[
 c=a=\Delta=0.                                          \tag{15a}
\]
Hence the nonzero scalar frame model with all six face slacks zero is
not physically realizable by a rank-two coefficient matrix.

## 3. Consequences for a negative candidate

The sitewise sharp-trace identity is
\[
 12Q_3(C)=2r_i+4s_i-9c_i.
\]
After summing over \(i\),
\[
 36Q_3(C)=2R+4S-9c.                                     \tag{16}
\]
If \(Q_3(C)<0\), then
\[
 2R+4S<9c.                                               \tag{17}
\]
Subtracting (17) from (1) gives
\[
 198R>243c+567a+18\Delta,
\]
or
\[
 R>\frac{27}{22}c+\frac{63}{22}a+\frac1{11}\Delta.       \tag{18}
\]
Since \(S\geq0\), (17) also gives \(R<9c/2\).  Compatibility of
these two strict bounds forces \(63a+2\Delta<72c\).  This
proves (3).

## 4. Equality classification

For nonzero rank-at-most-two \(C\), equality in the strengthened
inequality (1) is equality in
\(|\operatorname{Tr}C|\leq\|C\|_1\).  This forces the polar partial
isometry to be a common scalar phase on the support of \(|C|\).
Hence
\[
 C=e^{i\theta}H,\qquad
 H\succeq0,\quad\operatorname{rank}H\leq2.               \tag{19}
\]

Conversely every matrix (19) saturates (14), so it saturates (1).
The established positive-semidefinite three-copy theorem gives
\[
 Q_3(C)=Q_3(H)
 \geq\frac18\left(2\operatorname{Tr}H^2
                  -(\operatorname{Tr}H)^2\right)
 =\frac18\Delta\geq0.                                   \tag{20}
\]
Therefore equality in the new common-trace tradeoff is disjoint from
the negative endpoint locus.

Equality in the weaker version without \(18\Delta\) additionally
requires \(\Delta=0\).  If \(C\ne0\), this is exactly
\[
 C=e^{i\theta}sP
\]
with \(P\) a rank-two orthogonal projection.

## 5. Sharper singular-value identity

Let \(s_1,s_2\) be the two possibly nonzero singular values of \(C\)
and put \(p=s_1s_2=\|\wedge^2C\|_2\).  The sharper trace inequality
\[
 |\operatorname{Tr}C|^2\leq(s_1+s_2)^2
 =\|C\|_2^2+2p                                          \tag{21}
\]
has the exact slack conversion
\[
\boxed{
\begin{aligned}
 &416R+4S+72p-576c-1215a\\
 &\hspace{22mm}
 =36\left(\|C\|_2^2+2p-|\operatorname{Tr}C|^2\right)
 \geq0.
\end{aligned}}                                           \tag{22}
\]
This refinement retains the global exterior mass \(p\).  Substituting
\[
 2p=\|C\|_2^2-\Delta
\]
recovers the strengthened inequality (1).  A further improvement
requires a common-code relation between \(p\) and the three
partial-contraction exterior masses; treating those masses
independently cannot improve the coefficient in (1).

## 6. An explicit improvement of the negative-depth bound

The exact negative-depth simplex gives a particularly clean
consequence of (1).  Normalize a negative direction by
\[
 \langle S_V\rangle=1,\qquad
 \langle H_V\rangle=-\delta,\qquad \delta>0.
\]
Use its simplex coordinates
\[
 \theta_i>0,\qquad \sum_i\theta_i=1,\qquad
 0<\lambda_i\leq1,
\]
and put
\[
 L=\sum_i\theta_i\lambda_i.
\]
The established simplex identities are
\[
\begin{aligned}
 c&=\frac{1+\delta}{3},\\
 R&=\frac32(1-5\delta)(1-L),\\
 S&=\frac34(1-5\delta)L.                                \tag{23}
\end{aligned}
\]
Substitution in the strengthened common-trace inequality (1) gives
\[
\boxed{\qquad
 (1-5\delta)(300-297L)
 \geq84(1+\delta)+567a+18\Delta .
\qquad}                                                  \tag{24}
\]
Equivalently,
\[
\boxed{\qquad
 1584\delta+297(1-5\delta)L+567a+18\Delta
 \leq216 .
\qquad}                                                  \tag{25}
\]
Every term after \(1584\delta\) is nonnegative.  Moreover \(L>0\)
for every negative transition, while the previously established
bound gives \(1-5\delta>0\).  Therefore
\[
\boxed{\qquad
 0<\delta<\frac3{22}.
\qquad}                                                  \tag{26}
\]
This replaces the earlier explicit depth bound \(1/5\) by \(3/22\)
without compactness or an unevaluated stability constant.  Equation
(25) is stronger than the scalar bound: approaching \(3/22\) forces
simultaneously
\[
 (1-5\delta)L\longrightarrow0,\qquad
 a\longrightarrow0,\qquad
 \Delta\longrightarrow0.
\]
The inequality still does not force \(\delta=0\); a further
site-coupled exterior estimate is required inside the remaining
depth interval.

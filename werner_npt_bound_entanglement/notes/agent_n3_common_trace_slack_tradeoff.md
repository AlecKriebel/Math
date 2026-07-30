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
 200R+4S\ \geq\ 252c+567a .
\qquad}                                                   \tag{1}
\]
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
 \frac{27}{22}c+\frac{63}{22}a<R<\frac92c,
 \qquad a<\frac87c .
\qquad}                                                   \tag{3}
\]
Equality in (1), for nonzero \(C\), forces
\[
 C=e^{i\theta}sP
\]
with \(P\) a rank-two orthogonal projection.  Such matrices are
already known to obey \(Q_3(C)\geq0\).  Hence every negative candidate
would satisfy (1) strictly.

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
 \leq\sqrt2\,\|C\|_2.                                   \tag{14}
\]
Thus the right side of (2) is nonnegative, proving (1).

This implication is genuinely common-origin.  The individual
nonnegative quantities \(r_i,s_i\) do not encode the global trace and
norm in (14).  In particular, if \(R=S=0\), (1) forces
\[
 c=a=0.                                                  \tag{15}
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
 198R>243c+567a,
\]
or
\[
 R>\frac{27}{22}c+\frac{63}{22}a.                       \tag{18}
\]
Since \(S\geq0\), (17) also gives \(R<9c/2\).  Compatibility of
these two strict bounds forces \(a<8c/7\).  This proves (3).

## 4. Equality classification

For nonzero rank-at-most-two \(C\), equality in (1) is equality in
both inequalities in (14).  Equality in
\(\|C\|_1\leq\sqrt2\|C\|_2\) forces rank exactly two with equal
nonzero singular values.  Equality in
\(|\operatorname{Tr}C|\leq\|C\|_1\) forces the polar partial isometry
to be a common scalar phase on the support of \(|C|\).  Hence
\[
 C=e^{i\theta}sP                                      \tag{19}
\]
for a rank-two orthogonal projection \(P\).

Conversely every matrix (19) saturates (14), so it saturates (1).
The established positive-semidefinite three-copy theorem gives
\[
 Q_3(C)=s^2Q_3(P)\geq0.                                  \tag{20}
\]
Therefore equality in the new common-trace tradeoff is disjoint from
the negative endpoint locus.

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
This refinement retains the global exterior mass \(p\).  Eliminating
it only by \(2p\leq\|C\|_2^2\) recovers (1).  A further improvement
therefore requires a common-code relation between \(p\) and the three
partial-contraction exterior masses; treating those masses
independently cannot improve the coefficient in (1).


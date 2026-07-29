# A sharp quantitative no-switching inequality for factor-plane pencils

## Status

This note proves two exact quantitative versions of algebraic steps in
the three-copy Haar-equality exclusion.  Let \(f_\mu\) and \(g_\nu\)
be the two families of quadratic Plücker polynomials which test the two
possible factor types of a contracted two-plane.  If
\[
 a(z)=\sum_\mu |f_\mu(z)|^2,\qquad
 b(z)=\sum_\nu |g_\nu(z)|^2,
\]
then
\[
 \boxed{\qquad
 \mathbb E_z[a(z)b(z)]
 \geq \frac25\,\mathbb E_z a(z)\,\mathbb E_z b(z).
 \qquad}                                                   \tag{1}
\]
The constant \(2/5\) is sharp.

Thus a factor-plane pencil cannot switch rapidly between its two
factor types while keeping the product of their Plücker defects small:
small averaged product forces one complete family of minors to have
small averaged mass.

This is a genuine quantitative common-origin constraint.  It uses
that both minor families are homogeneous quadratics in the same
contraction variable \(z\).  Pointwise estimates which regard the
two families independently do not imply (1).

There is also an explicit marginal-floor estimate.  If the tensor
encodes an isometry from the logical qubit and its \(H_2\)- and
\(H_3\)-marginals obey
\[
 \sigma_2,\sigma_3\succeq mI_3,
 \qquad \operatorname{Tr}\sigma_2
 =\operatorname{Tr}\sigma_3=2,
\]
then both minor families satisfy
\[
 \boxed{\qquad
 \mathbb E a,\ \mathbb E b
 \geq
 \frac{m^8(1-m)^4}{79\,350}.
 \qquad}                                                   \tag{2}
\]
The constants are not optimized.  The significance is the polynomial
dependence and the exact proof: a uniformly full pair of one-site
marginals is quantitatively incompatible with either factor-plane
minor family becoming arbitrarily small.

The result does not yet settle unrestricted three-copy positivity.
The remaining stability step is to derive an upper bound for
\(\mathbb E(ab)\) from the simultaneous near-kernel block Grams and
compare it with (1)--(2).  Moreover, even that comparison by itself
controls the near-Haar-equality regime; a complete sign proof still
requires a mechanism which excludes negative stationary points with
large Haar slack.

The dependency-free checker
`verification/verify_n3_factor_pencil_product_gap.py` audits the
symmetrizer identity, the dimensions producing \(2/5\), and an exact
sharp example.

## 1. The scalar quadratic inequality

Let \(V=\mathbb C^3\), and identify a homogeneous quadratic
polynomial with a tensor \(f\in\operatorname{Sym}^2V\):
\[
 f(z)=\langle \overline z^{\otimes2},f\rangle.
 \tag{2}
\]
Write \(P_4\) for the orthogonal projection of \(V^{\otimes4}\) onto
\(\operatorname{Sym}^4V\).  Since \(z^{\otimes4}\) is symmetric, the
tensor representing the product polynomial \(f(z)g(z)\) is
\[
 P_4(f\otimes g).
 \tag{3}
\]

### Lemma 1

For every \(f,g\in\operatorname{Sym}^2V\),
\[
\boxed{
\begin{aligned}
 6\|P_4(f\otimes g)\|^2
 ={}&\|f\|^2\|g\|^2+|\langle f,g\rangle|^2\\
 &+4\operatorname{Tr}(\rho_f\rho_g),
\end{aligned}}
\tag{4}
\]
where
\[
 \rho_f=\operatorname{Tr}_2|f\rangle\langle f|,
 \qquad
 \rho_g=\operatorname{Tr}_2|g\rangle\langle g|.
\tag{5}
\]
In particular,
\[
 \|P_4(f\otimes g)\|^2
 \geq\frac16\|f\|^2\|g\|^2.
\tag{6}
\]

### Proof

The tensor \(f\otimes g\) is invariant under the subgroup
\[
 S_{\{1,2\}}\times S_{\{3,4\}}\subset S_4.
\]
Consequently the \(24\) terms in the full symmetrizer collapse into
the six choices of the two output positions occupied by the first
quadratic tensor:
\[
 \|P_4(f\otimes g)\|^2
 =
 \frac16\sum_{\substack{A\subset\{1,2,3,4\}\\|A|=2}}
 \langle f\otimes g,U_A(f\otimes g)\rangle.
\tag{7}
\]
The unchanged partition contributes
\(\|f\|^2\|g\|^2\), and the exchanged partition contributes
\(|\langle f,g\rangle|^2\).  Each of the four crossing partitions
contributes
\[
 \sum_{i,j,k,\ell}
 \overline{f_{ij}}f_{ik}\,
 \overline{g_{k\ell}}g_{j\ell}
 =
 \operatorname{Tr}(\rho_f\rho_g).
\tag{8}
\]
Both reduced operators in (5) are positive semidefinite, so
\(\operatorname{Tr}(\rho_f\rho_g)\geq0\).  Equations (7)--(8) prove
(4), and discarding the last two nonnegative terms proves (6).
\(\square\)

Let \(z\) be Haar-uniform on the unit sphere of \(\mathbb C^3\).
For \(h\in\operatorname{Sym}^kV\),
\[
 \mathbb E_z|\langle\overline z^{\otimes k},h\rangle|^2
 =
 \frac{\|h\|^2}{\dim\operatorname{Sym}^kV}.
\tag{9}
\]
Here
\[
 \dim\operatorname{Sym}^2V=6,\qquad
 \dim\operatorname{Sym}^4V=15.
\tag{10}
\]
Applying (9) to (3) and then using (6) gives
\[
\begin{aligned}
 \mathbb E|f(z)g(z)|^2
 &=\frac1{15}\|P_4(f\otimes g)\|^2\\
 &\geq\frac1{90}\|f\|^2\|g\|^2\\
 &=\frac25\,
 \mathbb E|f(z)|^2\,\mathbb E|g(z)|^2.
\end{aligned}
\tag{11}
\]

The constant is sharp.  Take orthonormal vectors \(e_1,e_2\) and
\[
 f=e_1^{\otimes2},\qquad g=e_2^{\otimes2}.
\tag{12}
\]
Then \(\langle f,g\rangle=0\) and
\(\rho_f\rho_g=0\), so equality holds in (6) and (11).

## 2. Vector-valued Plücker families

Let \((f_\mu)_\mu\) and \((g_\nu)_\nu\) be arbitrary finite families
in \(\operatorname{Sym}^2\mathbb C^3\), and put
\[
 a(z)=\sum_\mu|f_\mu(z)|^2,\qquad
 b(z)=\sum_\nu|g_\nu(z)|^2.
\tag{13}
\]
Applying (11) to every pair \((\mu,\nu)\) and summing proves
\[
\begin{aligned}
 \mathbb E[a(z)b(z)]
 &=\sum_{\mu,\nu}\mathbb E|f_\mu(z)g_\nu(z)|^2\\
 &\geq\frac25
 \left(\sum_\mu\mathbb E|f_\mu(z)|^2\right)
 \left(\sum_\nu\mathbb E|g_\nu(z)|^2\right),
\end{aligned}
\]
which is (1).

## 3. Application to contracted singular planes

Let
\[
 {\boldsymbol X}\in
 H_1\otimes H_2\otimes H_3\otimes K,
 \qquad
 H_i\simeq\mathbb C^3,\quad K\simeq\mathbb C^2,
\tag{14}
\]
encode a two-dimensional singular plane, and contract the first
physical factor:
\[
 X(z)=(\langle z|\otimes I){\boldsymbol X}
 \in H_2\otimes H_3\otimes K.
\tag{15}
\]
Regard \(X(z)\) first as a \(3\times6\) matrix across
\[
 H_2:(H_3\otimes K)
\]
and then as a \(3\times6\) matrix across
\[
 H_3:(H_2\otimes K).
\]
Let \(f_\mu(z)\) be all \(2\times2\) minors of the first flattening
and \(g_\nu(z)\) all \(2\times2\) minors of the second.  Every minor
is a homogeneous quadratic in \(z\).

The first minor family vanishes identically at \(z\) exactly when
\(X(z)\) has a fixed \(H_2\) factor; the second vanishes exactly when
it has a fixed \(H_3\) factor.  Therefore (1) is the sharp averaged
inequality
\[
 \boxed{\quad
 \mathbb E_z
 \left[
 \|\wedge^2_{H_2}X(z)\|^2
 \,\|\wedge^2_{H_3}X(z)\|^2
 \right]
 \geq
 \frac25
 \mathbb E_z\|\wedge^2_{H_2}X(z)\|^2\,
 \mathbb E_z\|\wedge^2_{H_3}X(z)\|^2.
 \quad}
\tag{16}
\]
Here each squared wedge norm means the sum of squared flattening
minors, with the same convention on both sides.

At exact zero, (16) recovers the irreducibility argument used in the
Haar-equality proof: if the product vanishes for every \(z\), then
one complete minor family vanishes identically.  Quantitatively, it
prevents a near-zero product from being explained by alternating
between the two factor types on different regions of
\(\mathbb{CP}^2\).

## 4. An explicit marginal-determinant floor

We now prove the second quantitative ingredient.  The constants are
chosen for transparent auditing rather than sharpness.

### Theorem 2

Let
\[
 T\in A\otimes B\otimes C\otimes K,
 \qquad
 A,B,C\simeq\mathbb C^3,\quad K\simeq\mathbb C^2,
\tag{17}
\]
encode an isometry \(K\to A\otimes B\otimes C\).  Thus
\[
 \|T\|^2=2,\qquad \operatorname{Tr}_{ABC}|T\rangle\langle T|=I_K.
\tag{18}
\]
For a Haar-unit vector \(z\in A\), put
\[
 M_z=(\langle z|\otimes I)T\in B\otimes(C\otimes K)
\tag{19}
\]
and
\[
 {\cal A}(T)
 =
 \mathbb E_z\,e_2\!\left(
 \operatorname{Tr}_{CK}|M_z\rangle\langle M_z|
 \right).
\tag{20}
\]
Let
\[
 \sigma_B=\operatorname{Tr}_{ACK}|T\rangle\langle T|,
 \qquad
 \sigma_C=\operatorname{Tr}_{ABK}|T\rangle\langle T|,
\qquad
 \Delta=\det\sigma_B\,\det\sigma_C.
\tag{21}
\]
Then
\[
 \boxed{\qquad
 {\cal A}(T)\geq\frac{\Delta^2}{1\,269\,600}.
 \qquad}
\tag{22}
\]
Consequently, if
\(\sigma_B,\sigma_C\succeq mI_3\), then
\[
 \boxed{\qquad
 {\cal A}(T)
 \geq
 \frac{m^8(1-m)^4}{79\,350}.
 \qquad}
\tag{23}
\]

The same theorem with \(B\) and \(C\) exchanged gives the identical
bound for the other factor-side minor family.

### Proof

Put \(D=C\otimes K\) and define
\[
 W=(P_+^A\otimes P_-^B)(T\otimes T),
\qquad
 w=\|W\|.
\tag{24}
\]
Here the two projectors act on two replicas:
\[
 P_+^A=\frac{I+F_A}{2},\qquad
 P_-^B=\frac{I-F_B}{2}.
\]
The two-copy Haar identity gives
\[
 \boxed{\qquad w^2=6{\cal A}(T).\qquad}
\tag{25}
\]
Moreover, contraction of \(W\) by
\(\overline z^{\otimes2}\) gives
\[
 P_-^B(M_z\otimes M_z).
\]
Hence, for every unit \(z\),
\[
 \left\|P_-^B(M_z\otimes M_z)\right\|\leq w.
\tag{26}
\]

Choose an orthonormal basis of \(A\), write its slices as
\[
 T=\sum_{i=0}^2|i\rangle M_i,
\qquad \sum_i\|M_i\|^2=2,
\tag{27}
\]
and relabel so that
\[
 \|M_0\|^2\geq\frac23.
\tag{28}
\]
Let \(s_1\geq s_2\geq s_3\) be the singular values of \(M_0\).
Then
\[
 s_1\geq\frac{\|M_0\|}{\sqrt3}\geq\frac{\sqrt2}{3}.
\tag{29}
\]
Since
\[
\begin{aligned}
 e_2(M_0M_0^\dagger)
 &=s_1^2s_2^2+s_1^2s_3^2+s_2^2s_3^2\\
 &=\|P_-^B(M_0\otimes M_0)\|^2\leq w^2,
\end{aligned}
\tag{30}
\]
the best rank-one approximation
\[
 M_0=s\,x\otimes r+R,
\qquad \|x\|=\|r\|=1,\quad s=s_1,
\tag{31}
\]
obeys
\[
 \|R\|^2=s_2^2+s_3^2
 \leq\frac{w^2}{s_1^2}\leq\frac92w^2.
\tag{32}
\]

For every \(i\), decompose \(M_i\) orthogonally relative to the two
lines \(\mathbb Cx\subset B\) and \(\mathbb Cr\subset D\):
\[
 M_i=\alpha_i x\otimes r+x\otimes s_i+b_i\otimes r+N_i,
\tag{33}
\]
where
\[
 s_i\perp r,\qquad b_i\perp x,\qquad
 N_i\in x^\perp\otimes r^\perp.
\tag{34}
\]
For \(i=1,2\), contracting \(W\) by
\((|0i\rangle+|i0\rangle)/\sqrt2\) gives
\[
 \left\|
 P_-^B(M_0\otimes M_i+M_i\otimes M_0)
 \right\|
 \leq\sqrt2\,w.
\tag{35}
\]
Replace \(M_0\) by its leading term \(s\,x\otimes r\).  The change in
the left side is at most
\[
 2\|R\|\|M_i\|\leq6w,
\tag{36}
\]
because \(\|M_i\|\leq\sqrt2\).  After projecting the result onto
\[
 (x\wedge x^\perp)\otimes(r\wedge r^\perp),
\]
all terms in (33) except \(N_i\) vanish.  On \(N_i\) the projected
map is \(s\) times an isometry.  Therefore (29), (35), and (36) give
\[
 \boxed{\qquad \|N_i\|\leq18w.\qquad}
\tag{37}
\]
For \(i=0\), the same bound follows directly from
\(N_0=R\) and (32).  Thus (37) holds for all three slices.
Put
\[
 N=\sum_i|i\rangle N_i,\qquad n=\|N\|.
\]
Then
\[
 n^2\leq972w^2,\qquad n<32w.
\tag{38}
\]

First suppose
\[
 w\leq\frac1{100}.
\tag{39}
\]
Let \(T'=T-N\), and let \(M_z'\) be its \(z\)-slice.  Since
\[
 \|M_z\|\leq\sqrt2,\qquad
 \|M_z'\|\leq\sqrt2+n,
\]
equations (26), (38), and (39) imply
\[
\begin{aligned}
 \|P_-^B(M_z'\otimes M_z')\|
 &\leq
 \|P_-^B(M_z\otimes M_z)\|\\
 &\quad+
 (\|M_z\|+\|M_z'\|)\|M_z-M_z'\|\\
 &\leq w+4n\leq129w.
\end{aligned}
\tag{40}
\]
Write the linear contractions of the two middle terms in (33) as
\[
 b(z)=\sum_i\overline z_i b_i,\qquad
 s(z)=\sum_i\overline z_i s_i.
\tag{41}
\]
The matrix \(M_z'\) has the form
\[
 x\otimes(\alpha(z)r+s(z))+b(z)\otimes r.
\]
Because \(x\perp b(z)\) and \(r\perp s(z)\), its only nonzero
second exterior singular product is exactly
\[
 \|P_-^B(M_z'\otimes M_z')\|
 =\|b(z)\|\,\|s(z)\|.
\tag{42}
\]
Thus
\[
 \|b(z)\|\,\|s(z)\|\leq129w
\quad\text{for every unit }z.
\tag{43}
\]

Put
\[
 B_0=\sum_i\|b_i\|^2,\qquad
 S_0=\sum_i\|s_i\|^2.
\tag{44}
\]
For scalar linear forms \(p,q\) on \(\mathbb C^3\),
\[
 \mathbb E|p(z)q(z)|^2
 =
 \frac{\|p\|^2\|q\|^2+|\langle p,q\rangle|^2}{12}
 \geq\frac1{12}\|p\|^2\|q\|^2.
\tag{45}
\]
Apply (45) to every pair of scalar components of \(b(z)\) and
\(s(z)\), and sum.  Equations (43)--(45) give
\[
 \frac1{12}B_0S_0
 \leq\mathbb E\bigl[\|b(z)\|^2\|s(z)\|^2\bigr]
 \leq129^2w^2.
\tag{46}
\]
Therefore
\[
 \boxed{\qquad \min\{B_0,S_0\}\leq450w.\qquad}
\tag{47}
\]

If \(B_0\leq450w\), the squared distance of \(T\) from the common
\(B\)-factor line \(\mathbb Cx\) is
\[
 d_B=\|(I-|x\rangle\langle x|)_BT\|^2
 =B_0+n^2\leq460w.
\tag{48}
\]
For a positive \(3\times3\) matrix of trace two whose mass on the
orthogonal complement of a line is \(d_B\), the Schur complement and
the arithmetic--geometric mean give
\[
 \det\sigma_B\leq\frac12d_B^2.
\tag{49}
\]
Also \(\det\sigma_C\leq(2/3)^3<1\).  Hence
\[
 \Delta\leq105\,800w^2.
\tag{50}
\]

If instead \(S_0\leq450w\), then \(T\) has squared distance at most
\[
 d_D=S_0+n^2\leq460w
\tag{51}
\]
from a tensor having the fixed \(D\)-factor \(r\).  The \(C\)-support
of \(r\in C\otimes K\) has dimension at most two.  A unit vector
orthogonal to that support therefore has \(\sigma_C\)-mass at most
\(d_D\), so
\[
 \lambda_{\min}(\sigma_C)\leq d_D,\qquad
 \det\sigma_C\leq d_D.
\tag{52}
\]
Using again \(\det\sigma_B<1\), we obtain
\[
 \Delta\leq460w.
\tag{53}
\]

Since \(\Delta<1\), equations (50) and (53) imply in either branch
\[
 w^2\geq\frac{\Delta^2}{211\,600}.
\tag{54}
\]
If (39) fails, then
\[
 w^2>\frac1{10\,000}
 \geq\frac{\Delta^2}{211\,600},
\tag{55}
\]
again because \(\Delta<1\).  Thus (54) is universal.  Equation (25)
now gives (22).

Finally, if both marginals are bounded below by \(mI_3\), their
eigenvalues are at least \(m\) and sum to two.  Their product is
therefore at least
\[
 2m^2(1-m).
\tag{56}
\]
Consequently
\[
 \Delta^2\geq16m^8(1-m)^4.
\tag{57}
\]
Substitution in (22), using
\[
 \frac{1\,269\,600}{16}=79\,350,
\]
proves (23). \(\square\)

Combining Theorem 2 with (1) gives the explicit common-origin product
floor
\[
 \boxed{\qquad
 \mathbb E[a(z)b(z)]
 \geq
 \frac{
 m^{16}(1-m)^8
 }{15\,741\,056\,250}.
 \qquad}
\tag{58}
\]
This is the first fully effective inequality which simultaneously
uses:

1. the common contraction variable \(z\);
2. both possible factor-plane Plücker families; and
3. the quantitative full-support condition on the two uncontracted
   physical marginals.

# The physical isotropic block Gram as one weighted Plücker inequality

## Status

This note does not prove unrestricted three-copy positivity.  It gives
an intrinsic exterior-algebra formulation of the surviving isotropic
block-Gram question
\[
 \beta=A|\operatorname{vec}I_3\rangle
          \langle\operatorname{vec}I_3|+BI_9,
 \qquad A\stackrel{?}{\leq}5B.                         \tag{1}
\]
The coefficients \(A,B\) are recovered from two invariant
contractions of the common rank-two matrix.  After a partial transpose,
the complete physical realizability condition is a difference of two
positive Gram matrices: the logical symmetric square and the unique
logical exterior square.  Consequently (1) is exactly one weighted
norm domination between those two pieces.

The negative side is not an arbitrary vector.  It is the mixed
component of one decomposable bivector and obeys the full common-factor
Plücker identities.  Thus the remaining isotropic problem is:

\[
\boxed{\begin{minipage}{0.88\linewidth}
Prove the weighted symmetric-square domination (25) for four physical
factor vectors satisfying the isotropic Gram-difference identity
(20), using the mixed Plücker relations (16).
\end{minipage}}                                           \tag{2}
\]

This is a genuine nonlinear realizability condition absent from the
formal negative block-Gram models.  It is, however, an exact
reformulation rather than a proof of the desired sign.

The dependency-free exact checker is
`verification/verify_n3_isotropic_plucker_reduction.py`.

## 1. Two invariant contractions

Fix one qutrit site \(A\simeq\mathbb C^3\), put
\[
 E=H_2\otimes H_3,
 \qquad
 {\cal R}_E=
 \left(I-\frac12F_2\right)
 \left(I-\frac12F_3\right),                             \tag{3}
\]
where the product in (3) is the tensor product of the two commuting
replica swaps.  Thus \({\cal R}_E\succ0\).

Let \(C\in M_{27}\) have rank at most two and write its blocks at the
selected site as \(C_{ap}\in M_9\).  Define
\[
 \beta_{ap,bq}
 =
 {\cal B}_2(C_{ap},C_{bq}),\qquad
 {\cal B}_2(D,E)
 =
 \langle D,L^{\otimes2}(E)\rangle_{\rm HS}.             \tag{4}
\]
There are two canonical scalar contractions:
\[
\begin{aligned}
 T&:=\operatorname{Tr}\beta
   =\sum_{a,p}Q_2(C_{ap}),\\
 S&:=\langle\operatorname{vec}I_3,\,
          \beta\operatorname{vec}I_3\rangle
   =Q_2\left(\sum_a C_{aa}\right)
   =Q_2(\operatorname{Tr}_A C).
\end{aligned}                                            \tag{5}
\]
The one-site recursion is
\[
 Q_3(C)=T-\frac12S.                                      \tag{6}
\]

If (1) holds, then
\[
 T=3A+9B,\qquad S=9A+3B.                                \tag{7}
\]
Therefore the coefficients themselves are the invariant contractions
\[
\boxed{
 A=\frac{3S-T}{24},\qquad
 B=\frac{3T-S}{24}.}                                    \tag{8}
\]
In particular,
\[
\boxed{
 5B-A=\frac{2T-S}{3},\qquad
 Q_3(C)=\frac32(5B-A).}                                 \tag{9}
\]

## 2. The logical symmetric and exterior Gram matrices

Choose any thin factorization
\[
 C=XY^\dagger
  =|x_0\rangle\langle y_0|
   +|x_1\rangle\langle y_1|.                            \tag{10}
\]
For an intrinsic choice one may take the balanced singular-value
gauge
\[
 x_r=\sqrt{s_r}\,u_r,\qquad
 y_r=\sqrt{s_r}\,v_r,                                   \tag{11}
\]
so that the two logical Gram matrices are both
\(\operatorname{diag}(s_0,s_1)\).
Slice the four vectors at the selected qutrit:
\[
 x_r=\sum_a|a\rangle x_{ar},\qquad
 y_r=\sum_p|p\rangle y_{pr},\qquad x_{ar},y_{pr}\in E.  \tag{12}
\]

On two copies of the logical qubit let
\[
 P_\pm^K=\frac12(I\pm F_K).
\]
For each local pair \((a,p)\), the three symmetric-square vectors and
the single exterior vector are
\[
\begin{aligned}
 s_{ap}^{00}&=x_{a0}\otimes y_{p0},\\
 s_{ap}^{11}&=x_{a1}\otimes y_{p1},\\
 s_{ap}^{01}&=\frac1{\sqrt2}
 (x_{a0}\otimes y_{p1}+x_{a1}\otimes y_{p0}),\\
 w_{ap}&=\frac1{\sqrt2}
 (x_{a0}\otimes y_{p1}-x_{a1}\otimes y_{p0}).
\end{aligned}                                            \tag{13}
\]
Use the positive weighted inner product
\[
 \langle z,z'\rangle_E
 :=\langle z,{\cal R}_E z'\rangle.                       \tag{14}
\]
Define the two positive semidefinite \(9\times9\) Gram matrices
\[
\begin{aligned}
 (G_+)_{ap,bq}
 &=
 \sum_{\lambda\in\{00,11,01\}}
 \langle s_{ap}^{\lambda},s_{bq}^{\lambda}\rangle_E,\\
 (G_-)_{ap,bq}
 &=\langle w_{ap},w_{bq}\rangle_E.
\end{aligned}                                            \tag{15}
\]

The array \(w\) carries the rank-two condition.  In full physical
indices \(\alpha,\gamma\) on the left and \(\beta,\delta\) on the
right, put
\[
\begin{aligned}
 p_{\alpha\gamma}
 &=\frac1{\sqrt2}
 (x_{\alpha0}x_{\gamma1}-x_{\alpha1}x_{\gamma0}),\\
 r_{\beta\delta}
 &=\frac1{\sqrt2}
 (y_{\beta0}y_{\delta1}-y_{\beta1}y_{\delta0}).
\end{aligned}
\]
Then the mixed exterior coefficients obey the exact common-factor
Plücker identity
\[
\boxed{
 w_{\alpha\beta}w_{\gamma\delta}
 -w_{\alpha\delta}w_{\gamma\beta}
 =p_{\alpha\gamma}r_{\beta\delta}.}                      \tag{16}
\]
In particular the unreshuffled matrix \(w=X\epsilon Y^{\mathsf T}\)
has rank at most two, and all of its minors arise from the same two
exterior factors \(p=x_0\wedge x_1\) and
\(r=y_0\wedge y_1\).

### Proposition 2.1

The partial transpose of the physical block Gram is
\[
\boxed{\qquad
 \beta^{\Gamma_2}=G_+-G_-.
\qquad}                                                   \tag{17}
\]

### Proof

For four environment vectors, the replica-swap formula gives
\[
 {\cal B}_2(|x\rangle\langle y|,
            |x'\rangle\langle y'|)
 =
 \langle x\otimes y',{\cal R}_E(x'\otimes y)\rangle.
                                                               \tag{18}
\]
Expanding (10) blockwise therefore gives
\[
 \beta_{ap,bq}
 =
 \sum_{r,t}
 \langle x_{ar}\otimes y_{qt},
 {\cal R}_E(x_{bt}\otimes y_{pr})\rangle.                \tag{19}
\]
On the other hand, \(G_+-G_-\) inserts
\(P_+^K-P_-^K=F_K\) between
\((\sum_r x_{ar}|r\rangle)\otimes
 (\sum_t y_{pt}|t\rangle)\) and the corresponding
\((b,q)\) vector.  Its \((ap,bq)\) entry is the right side of
(19) with \(p\) and \(q\) interchanged.  This is precisely
\((\beta^{\Gamma_2})_{ap,bq}=\beta_{aq,bp}\).
\(\square\)

Thus exact isotropy is the positive-Gram-difference identity
\[
\boxed{\qquad
 G_+-G_-=BI_9+AF_A,
\qquad}                                                   \tag{20}
\]
where \(F_A\) swaps the two displayed qutrit factors.

## 3. The single weighted Plücker inequality

Let
\[
 P_\sigma^A=\frac12(I+\sigma F_A),\qquad \sigma\in\{+,-\},
\]
and define four nonnegative masses
\[
 m_{\sigma,\tau}
 :=
 \operatorname{Tr}(P_\sigma^A G_\tau),
 \qquad \sigma,\tau\in\{+,-\}.                           \tag{21}
\]
Equivalently, these are the squared norms obtained by first selecting
the logical symmetric/exterior component in (13), then the displayed
physical symmetric/exterior component, and finally applying
\({\cal R}_E^{1/2}\).

Since the symmetric and antisymmetric qutrit-pair dimensions are six
and three, respectively, (20) gives
\[
\begin{aligned}
 m_{+,+}-m_{+,-}&=6(B+A),\\
 m_{-,+}-m_{-,-}&=3(B-A).
\end{aligned}                                            \tag{22}
\]
Consequently
\[
\boxed{
 3(5B-A)
 =
 m_{+,+}+3m_{-,+}
 -m_{+,-}-3m_{-,-}.}                                    \tag{23}
\]
Combining this with (9) gives the fully invariant identity
\[
 Q_3(C)
 =
 \frac12\left[
 m_{+,+}+3m_{-,+}
 -m_{+,-}-3m_{-,-}
 \right].                                                \tag{24}
\]

We have therefore proved the promised exact equivalence:
\[
\boxed{
\begin{aligned}
 A\leq5B
 \quad\Longleftrightarrow\quad
 m_{+,-}+3m_{-,-}
 \leq
 m_{+,+}+3m_{-,+}.
\end{aligned}}                                           \tag{25}
\]
Written out, the left side of (25) is the weighted norm of the one
logical Plücker vector \(w\); the right side is the sum of the
corresponding weighted norms of its three logical symmetric
companions.

## 4. Equivalent Schmidt-number threshold

There is a second exact interpretation of the same coefficient \(5\).
Let
\[
 \Omega_3=\frac1{\sqrt3}\operatorname{vec}I_3.
\]
For a positive operator \(\sigma\) on
\(\mathbb C^3\otimes\mathbb C^3\), say that its Schmidt number is at
most two when it is a sum of projectors onto vectors whose coefficient
matrices have rank at most two.

### Proposition 4.1

Suppose \(A,B\geq0\).  Then
\[
\boxed{\qquad
 B I_9+A|\operatorname{vec}I_3\rangle
          \langle\operatorname{vec}I_3|
 \text{ has Schmidt number at most two}
 \quad\Longleftrightarrow\quad
 A\leq5B.
\qquad}                                                   \tag{26}
\]

### Proof

If \(z\) has coefficient matrix \(M_z\) of rank at most two, then
\[
 |\langle\Omega_3,z\rangle|^2
 =\frac13|\operatorname{Tr}M_z|^2
 \leq\frac13\|M_z\|_1^2
 \leq\frac23\|z\|^2.                                    \tag{27}
\]
Thus every positive operator \(\sigma\) of Schmidt number at most two
obeys
\[
 \langle\Omega_3,\sigma\Omega_3\rangle
 \leq\frac23\operatorname{Tr}\sigma.                     \tag{28}
\]
For the operator in (26), (28) is
\[
 B+3A\leq\frac23(9B+3A),
\]
which is exactly \(A\leq5B\).

Conversely, let \(P\) range over rank-two orthogonal projections on
\(\mathbb C^3\), with invariant probability measure, and put
\[
 \Sigma=\mathbb E_P
 |\operatorname{vec}P\rangle\langle\operatorname{vec}P|. \tag{29}
\]
Every vector in this mixture has Schmidt rank two.  Invariance under
\(U\otimes\overline U\) makes
\(\Sigma=a|\operatorname{vec}I\rangle
\langle\operatorname{vec}I|+bI\).  The two contractions
\[
 \operatorname{Tr}\Sigma=\operatorname{Tr}P=2,\qquad
 \langle\operatorname{vec}I,\Sigma\operatorname{vec}I\rangle
 =|\operatorname{Tr}P|^2=4                              \tag{30}
\]
and (8) give
\[
 \Sigma=\frac1{12}\left(
 I_9+5|\operatorname{vec}I\rangle
       \langle\operatorname{vec}I|
 \right).                                                \tag{31}
\]
Here the claimed two-dimensional invariant operator space follows
directly by commuting successively with diagonal phase matrices and
with unitaries mixing each pair of basis vectors.  The integral is in
the finite-dimensional convex hull of the displayed rank-two
projectors; compactness, or the elementary finite-dimensional convex
hull theorem, replaces it by a finite convex combination if desired.

For \(0\leq A\leq5B\),
\[
 BI_9+A|\operatorname{vec}I\rangle
 \langle\operatorname{vec}I|
 =
 \left(B-\frac A5\right)I_9
 +\frac A5\left(
 I_9+5|\operatorname{vec}I\rangle
 \langle\operatorname{vec}I|
 \right).                                                \tag{32}
\]
The first term is a sum of product-basis projectors and the second is
a positive multiple of (31).  This proves the converse.
\(\square\)

In a hypothetical negative physical isotropic model, block positivity
on product local contractions first gives \(B\geq0\).  Explicitly, for
product coefficients \(z_{ap}=u_av_p\),
\[
 z^\dagger\beta z
 =
 Q_2\left[
 \left(\sum_a u_aX_a\right)
 \left(\sum_p\overline{v_p}Y_p\right)^\dagger
 \right]\geq0,                                           \tag{32a}
\]
because the contracted matrix has rank at most two.  Choosing
\(\sum_a u_av_a=0\) leaves only the \(B\)-term.  Meanwhile
\(Q_3(C)<0\) gives \(A>5B\), hence \(A>0\).  Proposition 4.1 therefore
applies.  The surviving question can equivalently be stated as:
\[
\boxed{\begin{minipage}{0.88\linewidth}
Does positivity and same-\(C\) rank-two realizability of an isotropic
block Gram force that block Gram to have Schmidt number at most two?
\end{minipage}}                                          \tag{33}
\]
By (25)--(26), this is the same question as weighted Plücker
domination.

## 5. What the reduction does and does not supply

Equation (25) identifies the exact nonlinear information missing from
the formal sector and block-Gram models.  Such models specify only the
difference \(G_+-G_-\).  A physical rank-two code must realize both
positive Grams using the same four factor vectors, so its negative
Gram is tied to the positive Gram by (13) and the common Plücker
relations (16).

The exact same-code example with \(A/B=6/5\) shows that these relations
do not force \(G_+-G_-\) to be positive after partial transpose:
all three physical antisymmetric directions can be negative.
Nevertheless that example obeys (25) strictly.  A negative isotropic
code would require \(A/B>5\), equivalently a strict reversal of (25).

No termwise comparison of the four masses is justified.  The required
coefficient three is the eigenvalue of \(2I-F_A\) on the physical
antisymmetric sector, and the cancellation between all four masses is
the endpoint functional itself.  Progress beyond (25) must therefore
use the common identities (16), or an equivalent relation coupling
the symmetric companions to both exterior factors \(p,r\).

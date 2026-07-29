# The sharp triple-skew stable-rank theorem

## Status

This note proves the sharp triple-skew stable-rank theorem.  It does
**not** prove unrestricted three-copy positivity, because the full
logical feature contains a coherently coupled two-skew component.

Let
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai},\qquad p,a,i\in\{0,1,2\},
\]
and, for \(t\in(\mathbb C^3)^{\otimes3}\), put
\[
 D_t=\sum_{p,q,r}t_{pqr}A_p\otimes A_q\otimes A_r.
\]
The sharp inequality
\[
 \boxed{\qquad
 \|D_t\|_{\rm op}^2\leq\frac16\|D_t\|_2^2
 =\frac16\|t\|^2
 \qquad}                                                   \tag{1}
\]
is proved below.  It is equivalent to each of three elementary-looking
nonlinear inequalities below.  The constant is forced by an exact
biseparable equality orbit.

The independent exact checker is
`verification/verify_n3_triple_skew_reduction.py`.

## 1. The triple-reduction operator

The epsilon contraction gives
\[
 \boxed{\qquad
 A_p^\dagger A_s
 =\frac12\bigl(\delta_{ps}I-|s\rangle\langle p|\bigr).
 \qquad}                                                   \tag{2}
\]
In particular the \(A_p\)'s are Hilbert--Schmidt orthonormal, so
\[
 \|D_t\|_2^2=\sum_{p,q,r}|t_{pqr}|^2.                      \tag{3}
\]

Normalize \(t\), set \(\rho=|t\rangle\langle t|\), and denote its
reduced density operators by \(\rho_A,\rho_{AB}\), and so on.
Expanding the three factors in (2) gives the exact identity
\[
\boxed{
\begin{aligned}
 8D_t^\dagger D_t={}&I
 -\rho_A\otimes I\otimes I
 -I\otimes\rho_B\otimes I
 -I\otimes I\otimes\rho_C\\
 &+\rho_{AB}\otimes I
 +\rho_{AC}^{(AC)}
 +I\otimes\rho_{BC}
 -\rho .
\end{aligned}}                                            \tag{4}
\]
Here \(\rho_{AC}^{(AC)}\) means the canonical embedding on the first
and third tensor factors.  Thus (1) is exactly
\[
 \boxed{\qquad
 I-\rho_A-\rho_B-\rho_C+\rho_{AB}+\rho_{AC}+\rho_{BC}-\rho
 \preceq\frac43I .
 \qquad}                                                   \tag{5}
\]
All missing identity factors in (5) are understood.

Formula (4) is the threefold qutrit antisymmetric-channel output.
Indeed
\[
 {\cal W}(X)=\sum_pA_pX A_p^\dagger
 =\frac12\bigl(\operatorname{Tr}(X)I-X^{\mathsf T}\bigr)
                                                               \tag{6}
\]
is trace preserving, and (4) is its triple tensor output, up to a
harmless full transpose.

## 2. Cross-marginal and Grassmannian forms

For another unit vector \(x\), taking its expectation in (5) gives
the equivalent cross-marginal inequality
\[
\boxed{
\sum_{i<j}\operatorname{Tr}
   \bigl(\rho_{ij}^t\rho_{ij}^x\bigr)
\leq
\frac13+
\sum_i\operatorname{Tr}\bigl(\rho_i^t\rho_i^x\bigr)
+|\langle t,x\rangle|^2 .
}                                                         \tag{7}
\]

The bilinear triple-skew contraction changes sign when its two
arguments are exchanged.  Hence \(D_tt=0\), and (4) gives
\((8D_t^\dagger D_t)t=0\).  It follows that it is enough to test
(7) on \(x\perp t\).

For such an orthonormal pair put
\[
 P=|t\rangle\langle t|+|x\rangle\langle x|.
\]
Purity across a cut is the same on the two sides for each of the two
pure summands, and direct expansion therefore gives
\[
\operatorname{Tr}P_{\bar i}^2-\operatorname{Tr}P_i^2
=2\left[
\operatorname{Tr}(\rho_{\bar i}^t\rho_{\bar i}^x)
-\operatorname{Tr}(\rho_i^t\rho_i^x)
\right].                                                  \tag{8}
\]
Consequently (7) is equivalent to the intrinsic rank-two-code
inequality
\[
 \boxed{\qquad
 \sum_{i=1}^3
 \left(\operatorname{Tr}P_{\bar i}^2
       -\operatorname{Tr}P_i^2\right)
 \leq\frac23 .
 \qquad}                                                   \tag{9}
\]

Equivalently, for the normalized decomposable bivector
\[
 \omega=\frac{t\otimes x-x\otimes t}{\sqrt2},
\]
and local antisymmetrizers
\({\mathsf A}_i=(I-F_i)/2\),
\[
 \boxed{\qquad
 \|{\mathsf A}_1{\mathsf A}_2{\mathsf A}_3\omega\|^2
 \leq\frac13 .
 \qquad}                                                   \tag{10}
\]
Since a globally antisymmetric bivector has only the three
single-skew sectors and the triple-skew sector, (10) is the
Hodge--Pluecker comparison
\[
 \sum_{\text{one local skew}}\|\omega_R\|^2
 \geq
 2\|\omega_{\{1,2,3\}}\|^2.                               \tag{11}
\]

There is also a four-party purity formulation.  Let
\[
 |\Psi\rangle
 =\frac{|0\rangle_K|t\rangle+|1\rangle_K|x\rangle}{\sqrt2}.
\]
Then \(\rho_K=I_2/2\), and purity of complementary reductions of the
pure state \(\Psi\), together with (8), shows that (9) is equivalent
to
\[
 \boxed{\qquad
 \sum_{i=1}^3
 \left[
 \operatorname{Tr}(\rho_{Ki}^{\Psi})^2
 -\operatorname{Tr}(\rho_i^{\Psi})^2
 \right]\leq\frac16 .
 \qquad}                                                   \tag{12}
\]
The next two sections prove (12), and hence all of (1), (5), (7),
(9), (10), and (12).

## 3. A refined qutrit sign-frame lemma

The missing input is a state-dependent strengthening of the usual
trace-norm sign argument.

### Lemma 3.1

Let \(X=X^\dagger\in M_3(\mathbb C)\) be traceless and let
\(\sigma\) be a qutrit density operator.  There is a Hermitian
contraction \(G\) such that
\[
\boxed{
\operatorname{Tr}(XG)=\sqrt2\|X\|_2,\qquad
\operatorname{Tr}(\sigma G^2)
\leq\frac23\left(1+\operatorname{Tr}\sigma^2\right).
}                                                         \tag{L1}
\]

#### Proof

The case \(X=0\) is immediate with \(G=0\).  After possibly replacing
\(X\) by \(-X\), its eigenvalues can be written
\[
 a,\quad b,\quad-a-b,\qquad a\geq b\geq0.
\]
Put \(S=a^2+ab+b^2\).  If \(b>0\), define
\[
 g=\frac{2\sqrt S-2a-b}{b};
\]
if \(b=0\), put \(g=0\).  In the displayed eigenbasis take
\[
 G=\operatorname{diag}(1,g,-1).                           \tag{L2}
\]
The inequalities
\[
 a+\frac b2\leq\sqrt S\leq a+b
\]
show \(0\leq g\leq1\).  More sharply, writing \(r=a/b\geq1\),
\[
 g=2\sqrt{r^2+r+1}-2r-1
\]
is strictly decreasing in \(r\), because
\[
 \frac{2r+1}{\sqrt{r^2+r+1}}<2.
\]
Hence
\[
 0\leq g\leq2\sqrt3-3,\qquad g^2<\frac13.                 \tag{L3}
\]
The final strict inequality follows exactly from
\[
 (2\sqrt3-3)^2=21-12\sqrt3<\frac13;
\]
after moving the radical and squaring, this is \(3844<3888\).

Since \(\|X\|_2^2=2S\), the choice (L2) gives
\[
\operatorname{Tr}(XG)
=2a+b(1+g)=2\sqrt S=\sqrt2\|X\|_2.                        \tag{L4}
\]

Let \(q\) be the diagonal entry of \(\sigma\) on the
\(b\)-eigenvector.  Then
\[
 \operatorname{Tr}(\sigma G^2)=1-(1-g^2)q.               \tag{L5}
\]
The diagonal entries of a density matrix are a probability vector,
and off-diagonal entries only increase its Hilbert--Schmidt purity.
Cauchy--Schwarz on the other two diagonal entries therefore gives
\[
 \operatorname{Tr}\sigma^2
\geq q^2+\frac{(1-q)^2}{2}.                               \tag{L6}
\]
Combining (L3), (L5), and (L6),
\[
\begin{aligned}
\frac23(1+\operatorname{Tr}\sigma^2)
-\operatorname{Tr}(\sigma G^2)
&\geq
q\left(q+\frac13-g^2\right)\\
&\geq0.
\end{aligned}
\]
This proves the lemma. \(\square\)

## 4. Proof of the stable-rank theorem

It suffices, by Section 2, to prove (12).  For an orthonormal pair
\(t,x\), expand its logical purification as
\[
 |\Psi\rangle\langle\Psi|
 =\frac12\sum_{a=0}^3\sigma_a\otimes X_a,                 \tag{T1}
\]
where \(\sigma_0=I_2\) and \(\sigma_1,\sigma_2,\sigma_3\)
are the Pauli matrices.  On physical site \(i\), put
\[
 X_{a,i}=\operatorname{Tr}_{\bar i}X_a,\qquad
 p_i=\|X_{0,i}\|_2^2,\qquad P_1=p_1+p_2+p_3.              \tag{T2}
\]
Here \(X_{0,i}=\rho_i^\Psi\) is a qutrit density matrix, while
every \(X_{a,i}\), \(a>0\), is Hermitian and traceless.
Pauli orthogonality gives
\[
\operatorname{Tr}(\rho_{Ki}^{\Psi})^2
=\frac12\sum_{a=0}^3\|X_{a,i}\|_2^2.                     \tag{T3}
\]
Thus (12) is exactly
\[
\sum_{i=1}^3\sum_{a=1}^3\|X_{a,i}\|_2^2
\leq P_1+\frac13.                                        \tag{T4}
\]

Fix a permutation \(\pi\in S_3\).  Apply Lemma 3.1 to
\((X_{\pi(i),i},X_{0,i})\), obtaining \(G_i\), and define
\[
 O_i=\sigma_{\pi(i)}^{(K)}\otimes G_i^{(i)}.
\]
The \(G_i\)'s act on distinct physical sites and commute, while the
three distinct Pauli matrices anticommute.  Hence the \(O_i\)'s are
pairwise anticommuting Hermitian contractions.  Set
\[
 z_i=\langle\Psi|O_i|\Psi\rangle
=\sqrt2\|X_{\pi(i),i}\|_2,\qquad
 s=\sum_i z_i^2.                                         \tag{T5}
\]
For \(O=\sum_i z_iO_i\), anticommutation and Cauchy--Schwarz in the
state \(\Psi\) give
\[
\begin{aligned}
s^2
=|\langle O\rangle_\Psi|^2
&\leq\langle O^2\rangle_\Psi\\
&=\sum_i z_i^2
  \operatorname{Tr}(X_{0,i}G_i^2)\\
&\leq
s\max_i\frac23(1+p_i).
\end{aligned}                                             \tag{T6}
\]
Every qutrit density matrix has purity at least \(1/3\).  Therefore,
for each \(i\),
\[
\frac23(1+p_i)
\leq\frac29+\frac23P_1.                                  \tag{T7}
\]
Equations (T5)--(T7) prove, also when \(s=0\),
\[
 2\sum_i\|X_{\pi(i),i}\|_2^2
\leq\frac29+\frac23P_1.                                  \tag{T8}
\]

Sum (T8) over all six permutations.  Each ordered pair \((i,a)\)
occurs twice, so
\[
4\sum_{i,a>0}\|X_{a,i}\|_2^2
\leq\frac43+4P_1.
\]
This is (T4), and hence proves (12).

Finally, for fixed normalized \(t\), the bilinear triple-skew
contraction gives \(D_tt=0\).  Any unit \(y\) decomposes as
\(y=\alpha t+\beta x\), where \(x\perp t\) is unit when
\(\beta\ne0\).  The already proved orthogonal case gives
\[
\|D_ty\|^2=|\beta|^2\|D_tx\|^2\leq\frac16.
\]
Together with (3), this proves (1). \(\square\)

## 5. Exact equality orbit

Let
\[
 |\Phi\rangle_{AB}
 =\frac{|00\rangle+|11\rangle+|22\rangle}{\sqrt3},
\qquad
 t=|\Phi\rangle_{AB}|0\rangle_C,\qquad
 x=|\Phi\rangle_{AB}|2\rangle_C .
                                                               \tag{13}
\]
Then \(t,x\) are orthonormal.  Their one-body cross overlaps are
\[
 (a_A,a_B,a_C)=\left(\frac13,\frac13,0\right),
\]
their two-body cross overlaps are
\[
 (b_{AB},b_{AC},b_{BC})=(1,0,0),
\]
and \(\langle t,x\rangle=0\).  Thus (7) is an equality.

The associated normalized triple-skew matrix is
\[
 D_t=\frac1{\sqrt3}
 \left(\sum_{p=0}^2A_p\otimes A_p\right)\otimes A_0.
                                                               \tag{14}
\]
The exact Hodge identity
\[
 \sum_pA_p\otimes A_p=\frac{3P_\Phi-F}{2}                 \tag{15}
\]
gives
\[
 \|D_t\|_2^2=1,\qquad \|D_t\|_{\rm op}^2=\frac16.          \tag{16}
\]
Permuting the three sites and applying local unitaries gives the
corresponding equality orbit.

### Theorem 5.1 (complete equality classification)

Conversely, every nonzero equality case in (1) belongs to the orbit
just described.  More precisely, after normalizing \(t\), permuting
the three sites, and applying local unitaries,
\[
 t=|\Phi\rangle_{AB}|0\rangle_C.                          \tag{E1}
\]
The two-dimensional top right and left singular spaces of \(D_t\)
are the corresponding common-factor planes
\[
 |\Phi\rangle_{AB}\otimes |0\rangle_C^\perp,              \tag{E2}
\]
with the harmless conjugations dictated by the Hodge covariance.

#### Proof

Choose a unit vector \(x\) with
\(\|D_tx\|^2=1/6\).  Since \(D_tt=0\), equality forces
\(x\perp t\).  Use the purification and notation of Section 4, and
write
\[
 h_{a,i}=\|X_{a,i}\|_2^2,\qquad
 P_1=\sum_i p_i,\qquad
 R=\frac29+\frac23P_1.
\]
Equality in (T4) implies equality in the sum of the six inequalities
(T8).  Since each of them is bounded above by the same number \(R\),
every permutation satisfies
\[
 2\sum_i h_{\pi(i),i}=R.                                  \tag{E3}
\]

Suppose \(h_{a,i}>0\).  Choose a permutation with
\(\pi(i)=a\).  Equality throughout (T6)--(T7) forces
\[
 \frac23(1+p_i)=R.
\]
Hence the other two physical marginals both have their minimum
qutrit purity \(1/3\).  If nonzero encoded-Pauli signals occurred on
two distinct sites, this argument would make all three marginals
maximally mixed.  But for \(\sigma=I_3/3\), the contraction (L2)
satisfies
\[
 \operatorname{Tr}(\sigma G^2)
 =\frac{2+g^2}{3}<\frac89
 =\frac23(1+\operatorname{Tr}\sigma^2),
\]
by (L3), contradicting equality in (T6).  Thus all encoded-Pauli
signals occur on one physical site, say \(C\), and
\[
 p_A=p_B=\frac13.                                        \tag{E4}
\]

Equation (E3), applied to the two permutations assigning each Pauli
axis to \(C\), now gives
\[
 h_{1,C}=h_{2,C}=h_{3,C}=\frac R2.                        \tag{E5}
\]
Equality in the proof of Lemma 3.1 forces the diagonal weight \(q\)
in (L5) to vanish and forces equality in (L6).  Therefore
\[
 X_{0,C}=\frac12P_E                                      \tag{E6}
\]
for a two-dimensional subspace \(E\subset\mathbb C^3\), so
\(p_C=1/2\) and \(R=1\).  The two physical output states
\[
 X_{0,C}\pm X_{a,C}
\]
are positive.  Their positivity on \(\ker P_E\) forces the middle
eigenvalue \(b\) of every \(X_{a,C}\) to vanish.  Equations (E5)--(E6)
then show that each \(X_{a,C}\) has eigenvalues
\((1/2,0,-1/2)\) on the same support.

Using (T3),
\[
 \operatorname{Tr}(\rho_{KC}^{\Psi})^2
 =\frac12\left(\frac12+3\frac12\right)=1.
\]
Thus \(\rho_{KC}^{\Psi}\) is pure, and its two marginals are maximally
mixed on two-dimensional supports.  The global purification factors
as a Bell pair on \(K:C\) times a pure state on \(A:B\).  By (E4), the
two qutrit marginals of that pure state are maximally mixed, so it is
maximally entangled.  Expanding the Bell pair in the original logical
basis proves (E1).  Formula (E2) follows directly from (14)--(15).
\(\square\)

### Corollary 5.2 (joint compensation at maximal triple skew)

Let \(Q_{(2)},Q_{(3)}\) be the two positive logical feature operators
for arbitrary qutrit singular planes, with
\[
 Q_{(3)}
 =\operatorname{comp}\left[\frac89
 {\mathsf A}_1{\mathsf A}_2{\mathsf A}_3\right],
\qquad
 Q_{(2)}
 =\operatorname{comp}\left[\frac49
 \sum_{i<j}{\mathsf A}_i{\mathsf A}_j\right].
\]
Then
\[
 {\cal C}(Q_{(3)})\leq\frac8{27}.                         \tag{E7}
\]
If equality holds in (E7), the two singular planes lie in the
common-factor chart, and the compensation is exact:
\[
\boxed{
 {\cal C}(Q_{(2)})=0,\qquad
 {\cal C}(Q_{(2)}+Q_{(3)})=\frac8{27}.
}                                                         \tag{E8}
\]
The corrected common-plane floor then has the strict margin \(2/27\).

#### Proof

For a coherent unit triple-skew coefficient vector \(c\), put
\[
 D_c=\sum_{p,q,r}c_{pqr}A_p\otimes A_q\otimes A_r.
\]
The Takagi variational formula for the polarized determinant matrix
of \(Q_{(3)}\) gives
\[
 t_1
 =\frac{16}{9}\max_{\|c\|=1}
 \left|\det(U^{\mathsf T}D_cV)\right|
 \leq\frac{16}{9}\max_{\|c\|=1}\|D_c\|_{\rm op}^2
 \leq\frac8{27}.                                         \tag{E9}
\]
Since concurrence is at most the largest Takagi singular value, this
proves (E7).

Equality in (E7) forces equality in both inequalities in (E9).
Theorem 5.1 classifies \(D_c\), while equality in the compression
determinant places \(\overline{\operatorname{ran}U}\) and
\(\operatorname{ran}V\) on its two-dimensional top singular spaces.
Thus, after local and logical unitary changes,
\[
 u_a=x\otimes e_a,\qquad v_a=y\otimes e_a,
\]
where \(x,y\) are maximally entangled on the other two qutrits.

For this chart direct swap contraction gives
\[
\begin{aligned}
 Q_{(3)}&=\frac89\eta_{12}A_{\rm L},\\
 Q_{(2)}&=\frac49\left[
 \eta_{12}I_4+(\eta_1+\eta_2)A_{\rm L}\right].
\end{aligned}                                             \tag{E10}
\]
Maximal entanglement gives \(\eta_1=\eta_2=1/3\), and equality in
(E7) gives \(\eta_{12}=1/3\).  The two matrices in (E10) are invariant
under logical spin flip, so their four Takagi values give (E8)
immediately.  The common-plane floor has least eigenvalue
\[
 \frac29(1-\eta_1-\eta_2)=\frac2{27}.
\]
\(\square\)

The corollary is an exact joint result on the maximal-AAA locus.
The next subsection gives an exact stable-rank deficit and a
quantitative compensation theorem on the entire common-factor chart.
A global conversion of that deficit into control of \(Q_{(2)}\)
outside the chart remains open.

### 5.3 Exact deficit and quantitative common-chart compensation

The proof of (1) retains an exact sum of nonnegative gaps.  This
strengthens the equality classification without using compactness.
Let \(t,x\) be orthonormal, put
\[
 c=\|D_tx\|^2,\qquad
 {\mathsf G}=\sum_{i=1}^3\sum_{a=1}^3\|X_{a,i}\|_2^2,
 \qquad P_1=\sum_i p_i,
\]
and, for \(\pi\in S_3\), use the quantities in (T5):
\[
 s_\pi=\sum_i z_{\pi,i}^2
 =2\sum_i\|X_{\pi(i),i}\|_2^2,\qquad
 R=\frac29+\frac23P_1.
\]
Then
\[
\boxed{
 \frac16-c
 =\frac{P_1+1/3-{\mathsf G}}8
 =\frac1{32}\sum_{\pi\in S_3}(R-s_\pi).
}                                                         \tag{S1}
\]

Indeed, taking the expectation of (4) in \(x\), and using
\(\langle t,x\rangle=0\), gives
\[
 8c=1+\sum_i
 \left[
 \operatorname{Tr}(\rho_{\bar i}^t\rho_{\bar i}^x)
 -\operatorname{Tr}(\rho_i^t\rho_i^x)
 \right].
\]
The four-party purity identity used in (12) says that the sum in
brackets is \({\mathsf G}-P_1\).  This proves the first equality in
(S1).  Moreover,
\[
 \sum_{\pi\in S_3}s_\pi=4{\mathsf G},\qquad
 6R=4(P_1+1/3),
\]
which proves the second.

Each summand in (S1) itself has a lossless nonnegative
decomposition.  Fix \(\pi\), abbreviate \(s=s_\pi\), and suppose
\(s>0\).  Define
\[
 w_i=\frac{z_i^2}{s},\qquad
 e_i=\operatorname{Tr}(X_{0,i}G_i^2),\qquad
 r_i=\frac23(1+p_i),
\]
and let
\[
 v_\pi=
 \left\langle\left(\sum_i z_iO_i\right)^2\right\rangle_\Psi
 -\left\langle\sum_i z_iO_i\right\rangle_\Psi^2
 \geq0
\]
be the variance discarded in (T6).  Pairwise anticommutation gives
\[
 \left\langle\left(\sum_i z_iO_i\right)^2\right\rangle_\Psi
 =\sum_i z_i^2e_i,
\]
and hence
\[
\boxed{
 R-s
 =\sum_iw_i\bigl[(R-r_i)+(r_i-e_i)\bigr]+\frac{v_\pi}{s}.
}                                                         \tag{S2}
\]
All terms on the right are nonnegative.  The global-purity part is
\[
 R-r_i
 =\frac23\sum_{j\ne i}\left(p_j-\frac13\right)\geq0.      \tag{S3}
\]
For the local eigenframe in Lemma 3.1, let \(q_i\) be the middle
diagonal weight of \(X_{0,i}\), and let \(g_i\) be the middle
eigenvalue of \(G_i\).  Direct subtraction of (L5) gives the exact
local gap
\[
\boxed{
\begin{aligned}
 r_i-e_i={}&
 \frac23\left[
 p_i-q_i^2-\frac{(1-q_i)^2}{2}\right]\\
 &+q_i\left(q_i+\frac13-g_i^2\right).
\end{aligned}}                                           \tag{S4}
\]
The first term is nonnegative by (L6), and the second by (L3).
For \(s=0\), \(R-s=R\geq0\) directly.  Equations (S1)--(S4)
therefore give a compactness-free stability certificate: a small
stable-rank deficit forces, in an averaged quantitative sense, all
of the purity, local-frame, and variance equality conditions used
in Theorem 5.1.

There is a complementary exact deficit identity at the logical
Takagi level.  Choose a coherent unit coefficient \(c_0\) attaining
the leading Takagi value of \(Q_{(3)}\), put
\[
 M=U^{\mathsf T}D_{c_0}V,
\]
and let \(t_1\geq t_2\geq t_3\geq t_4\) be the Takagi values of
\(Q_{(3)}\).  In the positive-concurrence regime,
\[
 t_1=\frac{16}{9}|\det M|,
\]
so
\[
\boxed{
\begin{aligned}
 \frac8{27}-{\cal C}(Q_{(3)})
 =\frac{16}{9}\biggl[
 &\left(\frac16-\|D_{c_0}\|_{\rm op}^2\right)\\
 &+\left(\|D_{c_0}\|_{\rm op}^2-|\det M|\right)
 \biggr]+t_2+t_3+t_4 .
\end{aligned}}                                           \tag{S5}
\]
Every term on the right is nonnegative.  Thus the logical deficit
separates exactly into the Hodge stable-rank deficit, a compression
plane-misalignment deficit, and the residual Takagi mass.

Finally, the two-skew compensation can be quantified on the full
common-factor chart
\[
 u_a=x\otimes e_a,\qquad v_a=y\otimes e_a.
\]
For its two non-logical qutrit sites define
\[
 \tau_i=\operatorname{Tr}(\rho_i^{\bar x}\rho_i^y),
 \qquad
 \gamma=|\langle\bar x,y\rangle|^2.
\]
The swap contractions in (E10) give
\[
 \eta_i=\frac{1-\tau_i}{2},\qquad
 4\eta_{12}=1-\tau_1-\tau_2+\gamma.                       \tag{S6}
\]
The least eigenvalue of the corrected common-plane floor is
\[
 m=\frac29(1-\eta_1-\eta_2)
 =\frac{\tau_1+\tau_2}{9}.                               \tag{S7}
\]
For either \(i\), apply
\(|\operatorname{Tr}Z|^2\leq3\|Z\|_2^2\) to the one-qutrit
operator obtained by tracing site \(i\) from
\(|\bar x\rangle\langle y|\).  This gives
\[
 \gamma\leq3\tau_i.
\]
Writing \(s=\tau_1+\tau_2\), we have
\(\gamma\leq3s/2\), and (S6) yields
\[
 4\eta_{12}\leq1+\frac s2.
\]
Since \({\cal C}(Q_{(3)})=8\eta_{12}/9\) on this chart, (S7)
proves the quantitative compensation law
\[
\boxed{
 m\geq
 \max\left\{0,\ {\cal C}(Q_{(3)})-\frac29\right\}.
}                                                         \tag{S8}
\]
It interpolates between the zero-floor boundary at triple
concurrence \(2/9\) and the strict margin \(2/27\) at the maximal
triple concurrence \(8/27\).  What is still missing is an invariant
replacement for (S8) when the two singular planes are not already
in a common-factor chart.

## 6. Why the naive two-site induction fails

The channel form suggests grouping two copies and trying to use the
sharp double-skew estimate first.  The required comparison map would
be
\[
 \Lambda_2(X)
 =\frac13\operatorname{Tr}(X)I_9
  -({\cal W}\otimes{\cal W})(X).                           \tag{17}
\]
Its Choi matrix is
\[
 J(\Lambda_2)=\frac13I-{\mathsf A}\otimes{\mathsf A},
 \qquad {\mathsf A}=\frac{I-F}{2}.                         \tag{18}
\]
This map is not even two-positive.

Indeed the normalized double-skew matrix
\[
 B=\frac1{\sqrt3}\sum_pA_p\otimes A_p
\]
has squared singular values
\[
 \frac13,\quad
 \underbrace{\frac1{12},\ldots,\frac1{12}}_{\text{eight times}}.
                                                               \tag{19}
\]
Its best rank-two truncation therefore has squared norm \(5/12\).
After normalization its vectorization is a Schmidt-rank-two vector
\(\zeta\), and low-rank projection duality gives
\[
 \langle\zeta|
 {\mathsf A}\otimes{\mathsf A}
 |\zeta\rangle\geq\frac5{12}.
\]
Consequently
\[
 \langle\zeta|J(\Lambda_2)|\zeta\rangle
\leq\frac13-\frac5{12}=-\frac1{12}.                       \tag{20}
\]
Thus neither a two-positive nor a three-positive induction through
(17) can prove (1).  The proof above instead retains the three-site
decomposability/monogamy constraint.

## 7. Consequence and remaining compensation

The theorem (1) implies that the triple-skew logical feature obeys
\[
 {\cal C}(Q_{(3)})\leq
 \frac89\cdot2\cdot\frac16=\frac8{27}.                    \tag{21}
\]
This is sharp on the equality code (13), and it is strictly larger
than the false separate budget \(2/9\).

Therefore (1) alone does **not** prove the coherent feature target
\({\cal C}(Q_{(2)}+Q_{(3)})\leq4/9\), nor unrestricted three-copy
positivity.  The two-skew part must compensate whenever the
triple-skew cost exceeds \(2/9\).  One exact sufficient coupled target
already isolated elsewhere is the conjugation-correct floor
\[
 Q_{(2)}^\Gamma+
 \left(\frac29-\frac12\operatorname{Tr}Q_{(3)}\right)I_4
 \succeq0.                                                \tag{22}
\]
The stable-rank theorem (1) does not imply the common-plane floor
(22), which remains unresolved.

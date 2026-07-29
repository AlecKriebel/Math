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

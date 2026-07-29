# The sharp triple-skew stable-rank reduction

## Status

This note isolates an exact positive subproblem.  It does **not** prove
unrestricted three-copy positivity.

Let
\[
 (A_p)_{ai}=2^{-1/2}\varepsilon_{pai},\qquad p,a,i\in\{0,1,2\},
\]
and, for \(t\in(\mathbb C^3)^{\otimes3}\), put
\[
 D_t=\sum_{p,q,r}t_{pqr}A_p\otimes A_q\otimes A_r.
\]
The numerically supported sharp inequality
\[
 \boxed{\qquad
 \|D_t\|_{\rm op}^2\leq\frac16\|D_t\|_2^2
 =\frac16\|t\|^2
 \qquad}                                                   \tag{1}
\]
is equivalent to each of three elementary-looking nonlinear
inequalities below.  It is still unproved.  The constant is forced by
an exact biseparable equality orbit.

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
Thus a qutrit antisymmetrizer identity, a collision-purity monogamy
identity, or a Pluecker sum of squares proving any one of
(5), (7), (9), (10), or (12) proves all of them.

## 3. Exact equality orbit

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

## 4. Why the naive two-site induction fails

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
(17) can prove (1).  A proof must retain the three-site
decomposability/monogamy constraint.

## 5. Consequence and remaining compensation

If (1) is proved, the triple-skew logical feature obeys only
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
The stable-rank inequality (1) and the common-plane floor (22) are
separate unresolved statements.

# The scalar-shifted pair frontier as one local reflection

## Status

This note records one exact obstruction and one strengthened open
frontier for the qutrit three-copy pair problem.

The proposed operator strengthening
\[
 {\cal A}_\Psi\succeq\frac32|\Psi\rangle\langle\Psi|
 \tag{1}
\]
is false by exactly \(1/6\).  The corrected sharp candidate
\[
 \boxed{\qquad
 {\cal A}_\Psi\succeq\frac43|\Psi\rangle\langle\Psi|
 \qquad}                                                  \tag{2}
\]
survives the obstruction and is an equality there.

Candidate (2) is not merely an equal-Schmidt-coefficient statement.
It is exactly equivalent to two-positivity of one explicit map, to a
rank-two partial-trace inequality, and to a scalar-plus-pair
Ky--Fan inequality.  It is strictly stronger than the still-open
pair-only theorem, so these equivalences are a reduced target, not a
proof.

The exact checker is
`verification/verify_n3_pair_scalar_reflection_frontier.py`.
The floating-point adversarial probe is
`discovery/probe_n3_pair_marginal_schur.cpp`.

## 1. The marginal operator and its map

Let
\[
 {\cal H}=(\mathbb C^3)^{\otimes3},\qquad K=\mathbb C^2,
\]
and let
\[
 |\Psi\rangle=\frac1{\sqrt2}
 \left(v_0\otimes|0\rangle_K+v_1\otimes|1\rangle_K\right),
 \qquad \langle v_a,v_b\rangle=\delta_{ab}.
 \tag{3}
\]
Thus \(\rho_K^\Psi=I_K/2\).  As in the normalized marginal
reduction, put
\[
 {\cal A}_\Psi
 =3I+2\sum_{i<j}\rho_{Kij}^\Psi
      -3\sum_i\rho_{Ki}^\Psi.                            \tag{4}
\]
The pair-only theorem is exactly
\[
 {\cal A}_\Psi-|\Psi\rangle\langle\Psi|\succeq0.          \tag{5}
\]

On \(M_3\), define the unnormalized trace-replacement map
\[
 e(X)=\operatorname{Tr}(X)I_3.                           \tag{6}
\]
Let \(e_i\) act at physical site \(i\), and define
\[
 \Xi
 =6e_1e_2e_3
 -3(e_1e_2+e_1e_3+e_2e_3)
 +2(e_1+e_2+e_3).                                       \tag{7}
\]
Since
\[
 (e_1e_2e_3\otimes\operatorname{id}_K)
 (|\Psi\rangle\langle\Psi|)
 =I_{\cal H}\otimes\frac{I_K}{2},
 \tag{8}
\]
directly tracing the indicated physical sites gives
\[
 \boxed{\qquad
 (\Xi\otimes\operatorname{id}_K)
 (|\Psi\rangle\langle\Psi|)
 ={\cal A}_\Psi.
 \qquad}                                                  \tag{9}
\]

For a real number \(c\), the assertion
\[
 {\cal A}_\Psi\succeq c|\Psi\rangle\langle\Psi|
 \quad\hbox{for every normalized code purification (3)}
 \tag{10}
\]
is equivalent to \(2\)-positivity of
\[
 \Lambda_c=\Xi-c\,\operatorname{id}.                     \tag{11}
\]
Indeed, every full-Schmidt-rank vector on \(K\otimes{\cal H}\)
is an invertible operator on \(K\), applied to a vector of the form
(3).  Since \(\Lambda_c\) acts only on \({\cal H}\), that filter
becomes a congruence on the output.  Rank-one inputs follow by a
limit.  Thus no unequal logical Schmidt coefficients are omitted.

## 2. Exact failure at \(c=3/2\)

Write
\[
 |\Phi_3\rangle_{12}
 =\frac1{\sqrt3}\sum_{a=0}^2|aa\rangle,\qquad
 |\Phi_2\rangle_{K3}
 =\frac1{\sqrt2}(|00\rangle+|11\rangle),
 \tag{12}
\]
and take
\[
 |\Psi\rangle
 =|\Phi_3\rangle_{12}\otimes|\Phi_2\rangle_{K3}.
 \tag{13}
\]
Equivalently,
\[
 v_0=|\Phi_3\rangle_{12}|0\rangle_3,\qquad
 v_1=|\Phi_3\rangle_{12}|1\rangle_3.
 \tag{14}
\]
Let
\[
 P=P_{\Phi_3}^{12},\qquad Q=P_{\Phi_2}^{K3},
 \tag{15}
\]
with identities on all unshown factors.  The six marginals are
\[
\begin{aligned}
 \rho_{K12}&=\frac12P,&
 \rho_{K13}&=\frac13Q,&
 \rho_{K23}&=\frac13Q,\\
 \rho_{K1}&=\frac16I,&
 \rho_{K2}&=\frac16I,&
 \rho_{K3}&=Q.
\end{aligned}                                             \tag{16}
\]
Substitution in (4) yields the commuting-projector formula
\[
 \boxed{\qquad
 {\cal A}_\Psi=2I+P-\frac53Q.
 \qquad}                                                  \tag{17}
\]
Since \(PQ=|\Psi\rangle\langle\Psi|\),
\[
 {\cal A}_\Psi|\Psi\rangle=\frac43|\Psi\rangle.
 \tag{18}
\]
Consequently
\[
 \boxed{\qquad
 \langle\Psi|
 \left({\cal A}_\Psi-\frac32|\Psi\rangle\langle\Psi|\right)
 |\Psi\rangle=-\frac16.
 \qquad}                                                  \tag{19}
\]
This is an exact physical counterexample to (1).

The same example has
\[
 {\cal A}_\Psi\succeq\frac13I,\qquad
 \langle\Psi,{\cal A}_\Psi^{-1}\Psi\rangle=\frac34.
 \tag{20}
\]
Moreover, the four joint eigenspaces of the commuting projections
\((P,Q)\) give
\[
\begin{array}{c|rrrr}
(P,Q)&(0,0)&(1,0)&(0,1)&(1,1)\\ \hline
{\cal A}_\Psi-\frac43PQ&2&3&1/3&0 .
\end{array}                                               \tag{21}
\]
Thus \(c=4/3\) is sharp if (2) is true.

## 3. Parity collapse at \(c=4/3\)

Put
\[
 m=e-\frac23\operatorname{id}.
 \tag{22}
\]
Expanding the tensor cube gives the exact map identity
\[
\boxed{
 \Lambda_{4/3}
 =\Xi-\frac43\operatorname{id}
 =\frac32e^{\otimes3}+\frac92m^{\otimes3}.
}                                                         \tag{23}
\]

Use the Choi convention
\[
 J(\Phi)=\sum_{a,b}|a\rangle\langle b|
              \otimes\Phi(|a\rangle\langle b|).
 \tag{24}
\]
For \(P_3=|\Omega_3\rangle\langle\Omega_3|\), with normalized
\(|\Omega_3\rangle\), one has
\[
 J(e)=I_9,\qquad J(\operatorname{id})=3P_3,\qquad
 J(m)=I_9-2P_3.
 \tag{25}
\]
Therefore
\[
\boxed{
 J(\Lambda_{4/3})
 =\frac32I+\frac92\prod_{i=1}^3(I-2P_i).
}                                                         \tag{26}
\]
On the simultaneous sector containing \(r\) maximally-entangled
projectors, its eigenvalue is
\[
\begin{array}{c|rrrr}
r&0&1&2&3\\ \hline
J(\Lambda_{4/3})&6&-3&6&-3 .
\end{array}                                               \tag{27}
\]
The original four coefficients have collapsed to parity.

## 4. Exact coefficient-matrix and reflection forms

For \(C\in M_{27}\), let \(|\psi_C\rangle\) be its coefficient
vector.  The contraction identity
\[
 \left\langle\psi_C\left|
 \prod_{i\in S}P_i
 \right|\psi_C\right\rangle
 =3^{-|S|}\|\operatorname{Tr}_SC\|_2^2                  \tag{28}
\]
and (26) give
\[
\boxed{
\begin{aligned}
 \langle\psi_C|J(\Lambda_{4/3})|\psi_C\rangle
 ={}&\frac32\|C\|_2^2\\
 &+\frac92\sum_{S\subseteq\{1,2,3\}}
 \left(-\frac23\right)^{|S|}
 \|\operatorname{Tr}_SC\|_2^2.
\end{aligned}}                                           \tag{29}
\]
Hence candidate (2) is exactly
\[
\boxed{
 \sum_S\left(-\frac23\right)^{|S|}
 \|\operatorname{Tr}_SC\|_2^2
 \geq-\frac13\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).
}                                                         \tag{30}
\]

There is an especially short sector form.  Define the
Hilbert--Schmidt reflection
\[
 {\mathfrak r}(X)=X-\frac23\operatorname{Tr}(X)I_3.
 \tag{31}
\]
It is \(-1\) on the scalar direction and \(+1\) on traceless
matrices.  If \(w_k\) is the squared norm of the component of \(C\)
having exactly \(k\) traceless local factors, then
\[
\begin{aligned}
 \langle C,{\mathfrak r}^{\otimes3}(C)\rangle
 &=(w_1+w_3)-(w_0+w_2)\\
 &=\|C\|_2^2-2(w_0+w_2).                                \tag{32}
\end{aligned}
\]
Thus (30) is equivalent to the strengthened primal projection
inequality
\[
\boxed{\qquad
 w_0+w_2\leq\frac23\|C\|_2^2
 \qquad(\operatorname{rank}C\leq2).
\qquad}                                                   \tag{33}
\]
The original pair-only theorem drops the nonnegative \(w_0\) from
the left side, so (33) is strictly stronger.

By low-rank duality, (33) is also equivalent to
\[
\boxed{\qquad
 s_1(D)^2+s_2(D)^2\leq\frac23\|D\|_2^2
\qquad
 (D\in{\cal V}_0\oplus{\cal V}_2),
\qquad}                                                   \tag{34}
\]
where \({\cal V}_k\) is the degree-\(k\) scalar/traceless sector.
In ordinary notation,
\[
 D=cI_{27}+\sum_{i<j}B_{ij}^{(ij)},\qquad
 \operatorname{Tr}_iB_{ij}
 =\operatorname{Tr}_jB_{ij}=0.                           \tag{35}
\]

## 5. Exact rank-two equality

Let
\[
 C=P_{\Phi_3}^{12}\otimes
 \left(|0\rangle\langle0|+|1\rangle\langle1|\right)_3.
 \tag{36}
\]
This is a rank-two orthogonal projection and \(\|C\|_2^2=2\).
The scalar/traceless weights of \(P_{\Phi_3}^{12}\) are
\[
 \left(\frac19,\frac89\right)
 \quad\hbox{in degrees }0,2,
 \tag{37}
\]
while those of the last factor are
\[
 \left(\frac43,\frac23\right)
 \quad\hbox{in degrees }0,1.
 \tag{38}
\]
Consequently
\[
 (w_0,w_1,w_2,w_3)
 =\left(\frac4{27},\frac2{27},
         \frac{32}{27},\frac{16}{27}\right),             \tag{39}
\]
and
\[
 w_0+w_2=\frac43=\frac23\|C\|_2^2.                      \tag{40}
\]
Equivalently, the left side of (30) is \(-2/3\), exactly
\(-\|C\|_2^2/3\).

## 6. A complete factorized chart

The equality example extends to an exact positive family.  Let
\(|\phi\rangle_{12}\) be any bipartite qutrit unit vector and put
\[
 |\Psi\rangle=|\phi\rangle_{12}\otimes|\Phi_2\rangle_{K3}.
 \tag{41}
\]
Write
\[
 P_\phi=|\phi\rangle\langle\phi|,\qquad
 M=\rho_1^\phi\otimes I_2+I_1\otimes\rho_2^\phi,\qquad
 Q=P_{\Phi_2}^{K3}.
 \tag{42}
\]
The two commuting \(Q\)-blocks of (4) are
\[
\begin{aligned}
 Q=0:\quad&3I+P_\phi-\frac32M,\\
 Q=1:\quad&P_\phi+\frac12M.
\end{aligned}                                             \tag{43}
\]
The first is positive because \(M\preceq2I\).  On the second block,
candidate (2) reduces to
\[
 \frac12M-\frac13P_\phi\succeq0.                         \tag{44}
\]
In a Schmidt basis
\[
 |\phi\rangle=\sum_{a=1}^r\sqrt{\lambda_a}|aa\rangle,
 \qquad r\leq3,
 \tag{45}
\]
the inverse rank-one criterion gives
\[
 \left\langle\phi\left|
 \left(\frac32M\right)^+
 \right|\phi\right\rangle
 =\frac r3\leq1.                                        \tag{46}
\]
This is exactly (44).  Equality occurs for full Schmidt rank
\(r=3\), including (13).

Thus (2) is proved on the entire Bell-spectator chart (41), not only
at the maximally entangled point.

## 7. What remains

The exact \(c=3/2\) conjecture is false.  The corrected constant
\(4/3\) is sharp and survives unrestricted complex discovery
optimization, but that numerical observation is not evidence.

A proof of any one of (2), (30), (33), or (34) would prove the
original pair-only theorem immediately.  Conversely, failure would
require an exact rank-two matrix with
\[
 w_0+w_2>\frac23\|C\|_2^2;
 \tag{47}
\]
it need not violate the weaker pair-only inequality.


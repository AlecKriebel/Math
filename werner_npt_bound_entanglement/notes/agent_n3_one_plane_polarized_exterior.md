# Lossless polarized exterior form of the one-plane inequality

## Status

This note gives two exact, lossless reductions of the one-plane
pair-sector inequality
\[
 {\cal S}_V\preceq2I
 \tag{1}
\]
for every isometry
\[
 V:\mathbb C^2\longrightarrow(\mathbb C^3)^{\otimes3}.
 \]
The first is a single four-vector polarized exterior inequality.  The
second is a five-versus-five inequality among positive exterior
reductions of one rank-one operator.

Neither inequality is proved here.  Two exact examples show why the
most natural simplifications fail:

1. the weight-three exterior layer cannot be bounded separately;
2. ordinary Cauchy--Schwarz followed by a comparison of crossed and
   matched diagonal energies loses a sharp unit even on the canonical
   fixed-factor equality plane.

The latter example is especially informative after the complete
fixed-left two-copy equality classification: the failed relaxation is
worst precisely where the true inequality is an equality.  A proof
must retain the coherent transition matrix element, not replace it by
the product of two crossed energies.

The dependency-free exact checker is
`verification/verify_n3_one_plane_polarized_exterior.py`.

## 1. Replica form

Let
\[
 |\boldsymbol V\rangle
 =v_0\otimes|0\rangle_K+v_1\otimes|1\rangle_K,
 \qquad
 R=|\boldsymbol V\rangle\langle\boldsymbol V|,
 \qquad
 \operatorname{Tr}_{123}R=I_K.                           \tag{2}
\]
On operators carrying \(K\), put
\[
 {\cal R}_i(X)=I_i\otimes\operatorname{Tr}_iX-\frac13X,
 \qquad
 {\cal S}_V=\sum_{i<j}{\cal R}_i{\cal R}_j(R).            \tag{3}
\]
The sharp pair-sector inequality is exactly (1).

Let \(F_i\) swap the \(i\)-th physical qutrits of two replicas and
let \(F_K\) swap the two auxiliary qubits.  Define
\[
\begin{aligned}
 H
 &=
 6I-3\sum_iF_i
 +2\sum_{i<j}F_iF_j-F_1F_2F_3\\
 &=2I+E_2+E_3,                                           \tag{4}\\
 E_2&=\sum_{i<j}(I-F_i)(I-F_j),\\
 E_3&=(I-F_1)(I-F_2)(I-F_3).
\end{aligned}
\]
On a simultaneous local-swap sector with \(r\) antisymmetric signs,
\[
\begin{array}{c|cccc}
r&0&1&2&3\\ \hline
H&2&2&6&22,\\
E_2+E_3&0&0&4&20.
\end{array}                                               \tag{5}
\]
Thus \(H\succeq0\).  Direct expansion of the marginal formula for
\({\cal S}_V\) gives, for every
\(x=x_0\otimes|0\rangle+x_1\otimes|1\rangle\),
\[
\boxed{\quad
3\langle x,(2I-{\cal S}_V)x\rangle
=
\langle x\otimes\boldsymbol V|
F_KH
|x\otimes\boldsymbol V\rangle.
\quad}                                                    \tag{6}
\]

## 2. The smallest polarized scalar inequality

Put
\[
 E=E_2+E_3=H-2I.                                         \tag{7}
\]
Since \(v_0,v_1\) are orthonormal, the identity part has no polarized
cross term.  Define
\[
\begin{aligned}
 N&=\|x_0\|^2+\|x_1\|^2,\\
 A&=
 \langle x_0\otimes v_0,E(x_0\otimes v_0)\rangle
 +\langle x_1\otimes v_1,E(x_1\otimes v_1)\rangle,\\
 c&=
 \langle x_0\otimes v_1,E(x_1\otimes v_0)\rangle.
\end{aligned}                                             \tag{8}
\]
Equation (6) becomes
\[
 3\langle x,(2I-{\cal S}_V)x\rangle
 =2N+A+2\operatorname{Re}c.                              \tag{9}
\]
The relative phase of \(x_1\) is arbitrary.  Therefore (1) is exactly
equivalent to
\[
\boxed{\qquad
 |c|\le N+\frac12A.
\qquad}                                                   \tag{10}
\]

Equivalently, after separating the lengths of \(x_0,x_1\), (10) is
the following four-unit-vector inequality:
\[
\boxed{
\begin{aligned}
&\left|
\langle u\otimes v_1,E(w\otimes v_0)\rangle
\right|^2\\
&\quad\le
\left(
2+\langle u\otimes v_0,E(u\otimes v_0)\rangle
\right)
\times
\left(
2+\langle w\otimes v_1,E(w\otimes v_1)\rangle
\right),
\end{aligned}}                                            \tag{11}
\]
or, displayed without line crowding,
\[
 |c(u,w)|^2\le(2+a(u))(2+b(w)).                           \tag{12}
\]
Here \(u,w\) are arbitrary unit vectors and \(v_0,v_1\) are an
orthonormal pair.

To see the equivalence, apply (12) to
\(x_0=s u,x_1=t w\).  Then
\[
\begin{aligned}
N+\frac12A
&=\frac{s^2}{2}(2+a(u))+\frac{t^2}{2}(2+b(w))\\
&\ge st\sqrt{(2+a(u))(2+b(w))}
\ge st|c(u,w)|.
\end{aligned}                                             \tag{13}
\]
Conversely, minimizing (10) over the ratio \(s:t\) recovers (12).

There is an exact \(27\times27\) Schur form.  Define
\[
\begin{aligned}
\langle u,T_r u\rangle
&=\langle u\otimes v_r,E(u\otimes v_r)\rangle,\\
\langle u,K_{01}w\rangle
&=\langle u\otimes v_1,E(w\otimes v_0)\rangle.
\end{aligned}                                             \tag{14}
\]
Then the complete one-plane theorem is equivalent to
\[
\boxed{\qquad
\begin{pmatrix}
2I+T_0&K_{01}\\
K_{01}^\dagger&2I+T_1
\end{pmatrix}\succeq0,
\qquad}                                                   \tag{15}
\]
or, since the diagonal blocks are strictly positive,
\[
\boxed{\quad
\left\|
(2I+T_0)^{-1/2}K_{01}(2I+T_1)^{-1/2}
\right\|\le1.
\quad}                                                    \tag{16}
\]
This is lossless.  It retains one transition operator \(K_{01}\)
rather than bounding it by unrelated crossed diagonal energies.

## 3. The five-versus-five exterior cube

On the four parties \(K,1,2,3\), define the local trace replacement
\[
 e_j(X)=I_j\otimes\operatorname{Tr}_jX,\qquad
 r_j=e_j-I.
 \tag{17}
\]
For \(T\subseteq\{K,1,2,3\}\), put
\[
 M_T(R)=r_Te_{T^c}(R),                                   \tag{18}
\]
with the convention
\[
 M_\varnothing(R)=e_Ke_1e_2e_3(R)=2I.
\]
Every \(M_T(R)\) is positive semidefinite.  Indeed, if \(F_j\) swaps
party \(j\) in two replicas, then
\[
\langle x,M_T(R)x\rangle
=
2^{|T|}
\left\|
\prod_{j\in T}\frac{I-F_j}{2}
(\boldsymbol V\otimes x)
\right\|^2.                                               \tag{19}
\]

Exact Möbius expansion of the defect gives
\[
\boxed{
\begin{aligned}
3(2I-{\cal S}_V)
={}&
4M_K+\sum_{i<j}M_{ij}+M_{123}\\
&-M_\varnothing-\sum_{i<j}M_{Kij}-M_{K123}.
\end{aligned}}                                            \tag{20}
\]
Thus (1) is equivalently the positive-operator comparison
\[
\boxed{
4M_K+\sum_{i<j}M_{ij}+M_{123}
\succeq
M_\varnothing+\sum_{i<j}M_{Kij}+M_{K123}.
}                                                         \tag{21}
\]
There are five positive terms on each side if \(4M_K\) is counted as
one weighted term.  Unlike scalar sector inequalities, all ten terms
come from the same rank-one \(R\) with
\(\operatorname{Tr}_{123}R=I_K\).

## 4. Exact failure of a layerwise proof

Split
\[
 A=A_2+A_3,\qquad c=c_2+c_3,                             \tag{22}
\]
using \(E_2,E_3\) in place of \(E\) in (8).  A tempting proof of (10)
would establish separately
\[
 |c_m|\le\frac12N+\frac12A_m,\qquad m=2,3.                \tag{23}
\]
The \(m=3\) instance is false.

Let
\[
 |\Phi_3\rangle_{23}
 =
 \frac1{\sqrt3}(|00\rangle+|11\rangle+|22\rangle),
\qquad
 \psi_r=|r\rangle_1\otimes|\Phi_3\rangle_{23},
 \tag{24}
\]
and take
\[
 v_0=\psi_0,\quad v_1=\psi_1,\qquad
 x_0=\frac{\psi_0}{\sqrt2},\quad
 x_1=-\frac{\psi_1}{\sqrt2}.                             \tag{25}
\]
Exact swap contraction gives
\[
\boxed{
(A_3,c_3)=\left(0,\frac23\right),\qquad
(A_2,c_2)=\left(\frac43,\frac23\right),\qquad N=1.
}                                                         \tag{26}
\]
The weight-three proposal would require \(2/3\le1/2\), failing by
\(1/6\).  The full right side retains the required pair-layer matched
mass:
\[
 |c_2+c_3|-\frac12(A_2+A_3)=\frac23<1.                   \tag{27}
\]
There is no cancellation between \(c_2\) and \(c_3\); both have the
same phase in this convention.

## 5. Exact failure of crossed-diagonal Cauchy

Positivity of \(E\) gives ordinary Cauchy--Schwarz:
\[
\begin{aligned}
 |\langle u\otimes v_1,E(w\otimes v_0)\rangle|^2
 \le{}&
 \langle u\otimes v_1,E(u\otimes v_1)\rangle\\
 &\times
 \langle w\otimes v_0,E(w\otimes v_0)\rangle.
\end{aligned}                                             \tag{28}
\]
To prove the lossless inequality (12) this way, one would need to
compare the crossed product in (28) with the matched product in
(12).  That comparison is false even at the canonical pair-sector
equality.

Use computational strings
\[
 v_0=|110\rangle,\quad v_1=|111\rangle,\qquad
 u=|000\rangle,\quad w=|001\rangle.                      \tag{29}
\]
For basis strings \(p,q\),
\(\langle p\otimes q,F_S(p\otimes q)\rangle=1\) exactly when
the strings agree on every site of \(S\).  Since
\[
 E=4I-3\sum_iF_i+2\sum_{i<j}F_iF_j-F_1F_2F_3,            \tag{30}
\]
we obtain
\[
\begin{aligned}
 \langle u v_0,E(u v_0)\rangle
 &=
 \langle w v_1,E(w v_1)\rangle=1,\\
 \langle u v_1,E(u v_1)\rangle
 &=
 \langle w v_0,E(w v_0)\rangle=4,\\
 \langle u v_1,E(w v_0)\rangle&=-3.
\end{aligned}                                             \tag{31}
\]
Thus the crossed Cauchy upper bound is \(4\), while the matched
right side of (12) is only
\[
 \sqrt{(2+1)(2+1)}=3.
\]
The relaxation fails by one.  Nevertheless the coherent transition
matrix element has magnitude exactly three, so the true inequality
(12) is an equality:
\[
 |-3|^2=(2+1)(2+1).                                      \tag{32}
\]

This is the fixed-factor plane singled out by the exact two-copy
kernel classification.  Consequently, replacing \(K_{01}\) in
(15) by a product of crossed diagonal norms destroys the equality
geometry that a sharp proof must preserve.

## 6. Remaining lemma

The one-plane problem is now the explicit transition contraction
(16), equivalently the four-vector inequality (12), equivalently the
five-versus-five exterior comparison (21).  The corrected layer
example (24)--(27) and the fixed-factor example (29)--(32) rule out:

1. separate estimates for \(E_2\) and \(E_3\);
2. an ordinary Cauchy estimate followed by independent diagonal
   comparison;
3. any proof that discards the common orthonormal pair
   \((v_0,v_1)\).

A useful next step would be a three-replica antisymmetrizer identity
for \(K_{01}\), or a direct Schur completion of (15) whose kernel on
the fixed-factor branch is the equality vector in (29).

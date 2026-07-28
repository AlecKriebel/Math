# Four-copy qubit-reference inequality: exact rank cutoff and discovery record

## Status

The four-copy projector problem would follow from the still-unproved
inequality
\[
 {\cal I}(\Psi):=
 6\operatorname{Tr}\rho_K^2+
 \sum_{1\leq i<j\leq4}\operatorname{Tr}\rho_{ij}^2
 -3\sum_{i=1}^4\operatorname{Tr}\rho_{Ki}^2\geq0                 \tag{1}
\]
for every pure state on
\[
 K\otimes A_1\otimes A_2\otimes A_3\otimes A_4,\qquad \dim K=2.
\]
This note records three exact facts which sharpen the target:

1. (1) is precisely a rank-at-most-two quadratic inequality for the
   physical marginal;
2. the corresponding pure-state inequality fails already when
   \(\dim K=3\), by an elementary exact example;
3. after diagonalizing the rank-two marginal, the missing statement is a
   single \(2\times2\) Gram/copositivity inequality whose diagonal entries
   are nonnegative by elementary linear-entropy subadditivity.

No proof of (1) is claimed here.  Floating-point optimization described at
the end is discovery evidence only.

## 1. Physical rank-two form

For an operator \(H\) on the four physical parties, let
\(\operatorname{Tr}_S H\) mean the trace over the parties in \(S\), and set
\[
 {\cal B}(H,G)
 =6\operatorname{Tr}(HG)
  +\sum_{|S|=2}\operatorname{Tr}\!\left[
       (\operatorname{Tr}_S H)(\operatorname{Tr}_S G)\right]
  -3\sum_{|S|=1}\operatorname{Tr}\!\left[
       (\operatorname{Tr}_S H)(\operatorname{Tr}_S G)\right].     \tag{2}
\]
Write \({\cal B}(H)={\cal B}(H,H)\).

Let \(\Psi\) be pure and \(H=\rho_{1234}\).  Complementary reductions of
a pure state have equal nonzero spectra.  Thus
\[
 \operatorname{Tr}H^2=\operatorname{Tr}\rho_K^2,
\]
\[
 \|\operatorname{Tr}_{ij}H\|_2^2
 =\operatorname{Tr}\rho_{\overline{\{i,j\}}}^2
 =\operatorname{Tr}\rho_{Kij}^2.
\]
Complementation permutes the six physical pairs, and
\[
 \|\operatorname{Tr}_iH\|_2^2
 =\operatorname{Tr}\rho_{\bar i}^2
 =\operatorname{Tr}\rho_{Ki}^2.
\]
Consequently
\[
 \boxed{{\cal I}(\Psi)={\cal B}(H).}                            \tag{3}
\]
Moreover \(\operatorname{rank}H\leq\dim K\).  Conversely, every positive
operator \(H\) of rank at most two has a purification with a qubit
reference.  Therefore (1) is exactly
\[
 \boxed{{\cal B}(H)\geq0\quad
        \text{for every }H\succeq0\text{ with }\operatorname{rank}H\leq2.}
                                                                    \tag{4}
\]

For the rank-two code projector \(P\), (2) is the double-reduction sum
\[
 {\cal B}(P)
 =\sum_{i<j}\langle P,{\cal R}_i{\cal R}_j(P)\rangle,
 \qquad {\cal R}_i(Z)=\operatorname{Tr}_i(Z)\otimes I_i-Z.       \tag{5}
\]
In the two-replica sector notation of the earlier notes,
\[
 {\cal B}(P)=4(e_2-3e_3+6e_4).                                  \tag{6}
\]
Thus (4) implies the sharp four-copy candidate.

## 2. Exact failure at rank three

The reference dimension in (1) cannot be discarded.  Let every displayed
local system be a qutrit and put
\[
 |\Phi\rangle_{K4}
 =\frac{|00\rangle+|11\rangle+|22\rangle}{\sqrt3},\qquad
 |G\rangle_{123}
 =\frac{|000\rangle+|111\rangle+|222\rangle}{\sqrt3},            \tag{7}
\]
\[
 |\Psi\rangle=|\Phi\rangle_{K4}\otimes|G\rangle_{123}.           \tag{8}
\]
Then
\[
 \operatorname{Tr}\rho_K^2=\frac13,\qquad
 \operatorname{Tr}\rho_{K4}^2=1,\qquad
 \operatorname{Tr}\rho_{Ki}^2=\frac19\quad(1\leq i\leq3).        \tag{9}
\]
For physical pairs contained in \(\{1,2,3\}\), the purity is \(1/3\);
for a pair \(\{i,4\}\), it is \(1/9\).  Hence
\[
 \sum_{i<j}\operatorname{Tr}\rho_{ij}^2
 =3\frac13+3\frac19=\frac43,
\qquad
 \sum_i\operatorname{Tr}\rho_{Ki}^2
 =1+3\frac19=\frac43.                                           \tag{10}
\]
Substitution gives the exact negative value
\[
 \boxed{{\cal I}(\Psi)=2+\frac43-4=-\frac23.}                    \tag{11}
\]
The physical marginal has rank three.  Thus any proof of (4) must use the
rank-two cutoff, not merely positivity or purity identities valid for an
arbitrary reference.

The same construction also explains the sharp boundary at rank two.
Replace (7) on \(K4\) by a maximally entangled qubit pair supported on a
two-dimensional subspace, while leaving an arbitrary pure state on
\(123\).  A direct substitution gives \({\cal I}=0\).

## 3. A two-state Gram formulation

Let
\[
 H=\lambda|u\rangle\langle u|+\mu|v\rangle\langle v|,
 \qquad \lambda,\mu\geq0,\quad
 \langle u,v\rangle=0,\quad \|u\|=\|v\|=1.                      \tag{12}
\]
Define the real symmetric matrix
\[
 G=
 \begin{pmatrix}
 {\cal B}(p_u,p_u)&{\cal B}(p_u,p_v)\\
 {\cal B}(p_v,p_u)&{\cal B}(p_v,p_v)
 \end{pmatrix},
 \qquad p_u=|u\rangle\langle u|.                                \tag{13}
\]
Then
\[
 {\cal B}(H)=
 \begin{pmatrix}\lambda&\mu\end{pmatrix}
 G
 \begin{pmatrix}\lambda\\\mu\end{pmatrix}.                      \tag{14}
\]

For a pure state \(u\), complementary purities give
\[
 G_{uu}
 =6+\sum_{i<j}\operatorname{Tr}(\rho_{ij}^u)^2
    -3\sum_i\operatorname{Tr}(\rho_i^u)^2.                      \tag{15}
\]
For every pair \(i<j\),
\[
 1-\operatorname{Tr}(\rho_i^u)^2
  -\operatorname{Tr}(\rho_j^u)^2
  +\operatorname{Tr}(\rho_{ij}^u)^2\geq0.                       \tag{16}
\]
Indeed, the left side is
\[
 \langle u|^{\otimes2}(I-F_i)(I-F_j)|u\rangle^{\otimes2}\geq0.
\]
Summing (16) over the six pairs proves
\[
 G_{uu}\geq0,\qquad G_{vv}\geq0.                                \tag{17}
\]

For \(T\subseteq\{1,2,3,4\}\), put
\[
 g_T(u,v)=\operatorname{Tr}(\rho_T^u\rho_T^v).
\]
Orthogonality eliminates the \(6\operatorname{Tr}(p_up_v)\) term, and
directly polarizing (2) gives
\[
 \boxed{\quad
 G_{uv}
 =\sum_{|T|=2}g_T(u,v)
  -3\sum_{|T|=3}g_T(u,v).
 \quad}                                                        \tag{18}
\]

It follows that (4) is reduced to the following scalar assertion:
\[
 \boxed{\quad
 G_{uv}\geq-\sqrt{G_{uu}G_{vv}}
 \quad\text{for every orthonormal pair }u,v.
 \quad}                                                        \tag{19}
\]
Because the weights \(\lambda,\mu\) in (12) are nonnegative, (19) is the
exact copositivity condition.  The stronger determinant condition
\(|G_{uv}|^2\leq G_{uu}G_{vv}\) is not required when \(G_{uv}>0\).

The rank-three example (8) shows why only a two-state assertion can hold.
In its three-dimensional Schmidt basis, the corresponding matrix has
diagonal entries \(2\) and off-diagonal entries \(-2\).  Every \(2\times2\)
principal submatrix is positive semidefinite, while the full \(3\times3\)
matrix has eigenvalue \(-2\) in the all-ones direction.

## 4. Discovery-only optimization

`discovery/search_n4_homogeneous_purity.cpp` minimizes (1) directly over a
normalized pure tensor.  It independently contracts every reduced purity
and uses a tangent gradient on the unit sphere.

- For \(\dim K=2\), physical dimensions \(2,3,4\), all tested restarts
  approached zero and none produced a resolved negative value.
- For \(\dim K=3\) and qutrit physical sites, the optimizer repeatedly
  reached \(-2/3\), and its purities matched (9)--(10).
- At qutrit zero points with \(\dim K=2\), the four one-site physical
  marginal determinants approached zero.  This suggests that the
  optimizer is reaching the already-understood common-local-qubit
  boundary, but it is not a proof that every equality case has that form.

These calculations are not evidence for (4).  Their purpose is to audit
the formulas, expose the exact rank cutoff, and focus the proof search on
(19).

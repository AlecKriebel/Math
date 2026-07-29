# The missing auxiliary-marginal hypothesis in the two-site cofactor lemma

## Status

The proposed quantitative two-site lemma is false if it is stated only
for positive semidefinite rank-at-most-two operators of trace two.  The
boundary reduction that motivates the lemma has one further hypothesis:
the auxiliary-qubit marginal is the identity.  This note gives an exact
counterexample when that hypothesis is omitted and records the corrected
statement still under investigation.

Throughout, for a physical site \(i\), put
\[
 E_i(X)=I_i\otimes\operatorname{Tr}_iX,\qquad
 M_{Q,2}(X)=(2E_1-I)(2E_2-I)(X).
\tag{1}
\]

## 1. Exact counterexample to the unconditioned statement

Let \(K=\mathbb C^2\), \(H_1=H_2=\mathbb C^3\), and define
\[
\begin{aligned}
 |\Omega_0\rangle
 &=\frac{|00\rangle+|11\rangle+|22\rangle}{\sqrt3},\\
 |\Omega_1\rangle
 &=\frac{|01\rangle+|12\rangle+|20\rangle}{\sqrt3},\\
 P&=|\Omega_0\rangle\langle\Omega_0|
   +|\Omega_1\rangle\langle\Omega_1|,\\
 R&=|0\rangle\langle0|_K\otimes P.
\end{aligned}
\tag{2}
\]
The two vectors in (2) are orthonormal, so \(P\), and hence \(R\), is
an orthogonal projection of rank two.  In particular,
\[
 R\succeq0,\qquad \operatorname{Tr}R=2,\qquad
 \operatorname{pdet}R=1.
\tag{3}
\]
Both physical marginals are maximally mixed:
\[
 \rho_1=\operatorname{Tr}_{K2}R=\frac23I_3,\qquad
 \rho_2=\operatorname{Tr}_{K1}R=\frac23I_3.
\tag{4}
\]
Thus
\[
 \det\rho_1\,\det\rho_2\,\operatorname{pdet}R
 =\left(\frac8{27}\right)^2=\frac{64}{729}>0.
\tag{5}
\]

On the other hand, both maps in (1) act trivially on \(K\), and hence
\[
 M_{Q,2}(R)=|0\rangle\langle0|_K\otimes M_{Q,2}(P).
\tag{6}
\]
It follows that
\[
 M_{Q,2}(R)(|1\rangle_K\otimes z)=0
\qquad(z\in H_1\otimes H_2).
\tag{7}
\]
Equations (5)--(7) disprove
\[
 M_{Q,2}(R)\succeq
 \det\rho_1\det\rho_2\operatorname{pdet}(R)\,I
\tag{8}
\]
under the hypotheses \(R\succeq0\), \(\operatorname{rank}R\le2\), and
\(\operatorname{Tr}R=2\) alone.

## 2. The corrected boundary problem

In the actual three-copy boundary reduction, \(R\) is obtained by
tracing one physical site from the rank-two code purification
\[
 |\mathcal U\rangle
 =|0\rangle_Ku_0+|1\rangle_Ku_1,\qquad
 \langle u_i,u_j\rangle=\delta_{ij}.
\tag{9}
\]
Consequently it satisfies the additional normalization
\[
 \boxed{\operatorname{Tr}_{12}R=I_K.}
\tag{10}
\]
The counterexample (2) violates (10), since
\[
 \operatorname{Tr}_{12}R=2|0\rangle\langle0|_K.
\tag{11}
\]

The corrected quantitative lemma is therefore:
\[
\boxed{
\begin{gathered}
 R\succeq0,\quad \operatorname{rank}R\le2,\quad
 \operatorname{Tr}_{12}R=I_K,\\
 M_{Q,2}(R)\stackrel{?}{\succeq}
 \det\rho_1\det\rho_2\operatorname{pdet}(R)\,I .
\end{gathered}}
\tag{12}
\]
Condition (10) already implies \(\operatorname{Tr}R=2\).  No
counterexample to (12) is asserted here.

The dependency-free verifier
`verification/verify_n3_cofactor_boundary_condition_audit.py` checks
all identities in (2)--(7) and (11) by exact rational arithmetic.

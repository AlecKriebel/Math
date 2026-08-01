# Rational seed compression for an exact degree-three DTH certificate

## Result

The numerical degree-three extension code uses SVD bases in tensor products
of Young orthogonal modules.  Those bases are suitable for discovery but are
poor final certificate coordinates.  This note gives an exact rational
replacement whose largest linear algebra occurs in the reduced multiplicity
rank (at most 300), not in the raw Specht tensor product (as large as 42875).

This is a certificate architecture, not by itself a proof that the recorded
five-replica pseudomoment extends.

## 1. Exact source projectors

Fix a local shape triple

\[
\Lambda=(\Lambda_1,\Lambda_2,\Lambda_3)
\]

of partitions of seven with at most three rows.  Use integral polytabloid
bases in the local Specht modules and let

\[
V_\Lambda=[\Lambda_1]\otimes[\Lambda_2]\otimes[\Lambda_3],
\qquad
G_\Lambda=G_{\Lambda_1}\otimes G_{\Lambda_2}\otimes G_{\Lambda_3}
\]

be the raw rational coordinate space and its positive rational Gram matrix.

On the six bivector replicas define the wreath idempotent

\[
E=\frac1{2^3 3!}
\sum_{\sigma\in S_3}\sum_{\epsilon\in(\mathbb Z/2)^3}
(-1)^{|\epsilon|}\,\rho(\sigma,\epsilon).
\tag{1}
\]

It antisymmetrizes each pair and symmetrizes the three pairs.  If

\[
Z=\sum_{1\le i<j\le6}(ij),
\]

then the degree-three Grassmann projector is

\[
\boxed{
P=E\frac{(Z+5I)(Z+15I)}{144}.
}
\tag{2}
\]

Both (E) and (P) are rational, (G_\Lambda)-self-adjoint idempotents.  After
collecting permutations, (P) has exactly 720 nonzero terms.  Its coefficient
multiset is

\[
\begin{array}{c|rrrrrr}
c&1/576&-1/576&1/288&-1/288&1/144&-1/144\\
\#&192&192&144&144&24&24.
\end{array}
\tag{3}
\]

Thus applying (P), or evaluating one matrix element of (G_\Lambda P), is a
finite rational group-algebra calculation; no algebraic orthogonalization is
needed.

Let (Q_i) be the local three-replica antisymmetrizer on the deleted
bivector pair and the final vector.  The Omega Gram operator is

\[
Q=Q_1\otimes Q_2\otimes Q_3.
\tag{4}
\]

It is also a rational orthogonal projector.

## 2. Seed-Gram theorem

Let

\[
m=\operatorname{rank}P,
\qquad
o=\operatorname{rank}(QP),
\qquad
r=m-o.
\]

The exact census gives (m\le300), (o\le3), and (r) equal to the post-Omega
source rank.  Choose a rational seed matrix (S\in\mathbb Q^{\dim V_\Lambda
\times m}) such that

\[
U=PS
\]

has rank (m).  Define the two small rational Gram matrices

\[
K=S^{\mathsf T}G_\Lambda PS=U^\dagger U,
\qquad
H=S^{\mathsf T}P^{\mathsf T}G_\Lambda QPS=U^\dagger Q U.
\tag{5}
\]

Let (N) be any rational column basis of (\ker H).  Then

\[
\boxed{B=PSN}
\tag{6}
\]

is a rational basis of the complete post-Omega degree-three source.

### Proof

Since (U) is a basis of (\operatorname{ran}P), the matrix (K) is positive
definite.  For every coefficient vector (a),

\[
a^*Ha
=\langle Ua,QUa\rangle
=\|QUa\|^2,
\tag{7}
\]

because (Q) is an orthogonal projector.  Hence

\[
Ha=0
\iff
QUa=0.
\]

It follows that (UN) is exactly

\[
\operatorname{ran}P\cap\ker Q.
\]

All matrices in (5) are rational, so Gaussian elimination gives a rational
(N).  This proves (6).  \(\square\)

The theorem replaces an exact nullspace calculation in dimension up to
42875 by one positive Gram matrix and one rank-at-most-three correction in
dimension at most 300.  Seeds may be chosen deterministically by scanning
standard coordinate vectors and retaining modular Gram pivots; the resulting
pivot list can then be replayed over (\mathbb Q).

## 3. Exact rational marginal blocks

Let (K_\kappa) be the established rational five-replica post-Omega basis in
one target block, and put

\[
H_\kappa=K_\kappa^{\mathsf T}G_\kappa K_\kappa.
\]

For an odd-vertical two-box branch channel

\[
J_p:V_\kappa\longrightarrow V_\Lambda,
\]

the coefficient matrix of the source-to-target contraction in the rational
bases is

\[
\boxed{
C_{\Lambda,\kappa,p}
=H_\kappa^{-1}
K_\kappa^{\mathsf T}J_p^{\mathsf T}G_\Lambda B.
}
\tag{8}
\]

Every factor in (8) is rational.  If (X_\Lambda\succeq0) is the coefficient
density in basis (B), the exact target chart is

\[
\boxed{
R_\kappa
=\sum_{\Lambda,p}
d_{\Lambda,\kappa}
C_{\Lambda,\kappa,p}X_\Lambda
C_{\Lambda,\kappa,p}^{\mathsf T},
}
\tag{9}
\]

where the already audited carrier ratio (d_{\Lambda,\kappa}) is rational.

To verify (8), let (Ba) be a source vector.  Its branch restriction is in
the target post-Omega range, so write it as (K_\kappa c).  Taking inner
products with the columns of (K_\kappa) gives

\[
H_\kappa c
=K_\kappa^{\mathsf T}J_p^{\mathsf T}G_\Lambda Ba,
\]

which is precisely (8).  Applying this to both legs of a positive rank-one
source density and summing proves (9).

## 4. Consequence for exactification

Equations (5)--(9) put the complete degree-three marginal over
(\mathbb Q).  They can therefore be combined with the exact right-inverse
lemma in `agent_dth_level2_exact_right_inverse.md`:

1. solve the rational-coordinate system numerically and find a common block
   floor;
2. round the source blocks to rational matrices;
3. compute the marginal residual exactly;
4. correct it by the rational equivariant right inverse; and
5. certify the corrected block spectra by exact LDL or interval Cholesky.

The large disposable Young-orthogonal SVD cache is then needed only to find a
Slater point.  It is not part of the final verifier.

## Verification

`verification/verify_dth_level2_rational_seed_projector.py` constructs (E)
and (P) in the rational group algebra, verifies self-adjoint idempotence, and
checks the complete coefficient census (3) using dependency-free exact
arithmetic.

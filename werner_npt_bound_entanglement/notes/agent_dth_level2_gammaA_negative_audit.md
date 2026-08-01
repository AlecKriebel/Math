# Audit and exact pullback seeds for the cap-100 Γ_A-negative blocks

## Status

The strict holomorphic degree-three extension recorded in the discovery cache
is **not** positive after partial transpose on the anchored bivector.  Four
mixed multiplicity blocks have negative eigenvalues far above reconstruction
error:

\[
\begin{array}{c|r|r|r}
\text{mixed indices}&\dim&\lambda_{\min}&\lambda_{\max}\\ \hline
(1,2,9)&44&-7.513279839639349\,10^{-10}&5.846340712063830\,10^{-10}\\
(1,4,9)&55&-7.373929691281344\,10^{-10}&2.024234963002391\,10^{-9}\\
(0,2,5)&96&-4.688871504245988\,10^{-11}&2.041900118397953\,10^{-9}\\
(1,4,6)&100&-5.725898875679038\,10^{-11}&3.125061970864254\,10^{-9}.
\end{array}
\tag{1}
\]

This disproves PPT of the present Slater extension.  It does **not** prove
that no other positive fixed-marginal extension is PPT, and therefore is not
a constrained-lift obstruction or a DTH result.

The numerical audit is
`discovery/agent_dth_level2_audit_gamma_negative.py`.  Exact rational
pullback seeds are checked by
`verification/verify_dth_level2_gammaA_pullback_seeds.py`.

## 1. Exact carrier labels

The local mixed indices used above have the following exact labels:

\[
\begin{array}{c|c|c|r|r}
i&GL_3\text{ weight}&SU(3)\text{ Dynkin}&d_i&m_i\\ \hline
0&(5,0,-2)&(5,2)&81&1\\
1&(5,-1,-1)&(6,0)&28&1\\
2&(4,1,-2)&(3,3)&64&4\\
4&(3,2,-2)&(1,4)&35&5\\
5&(3,1,-1)&(2,2)&27&24\\
6&(3,0,0)&(3,0)&10&20\\
9&(1,1,1)&(0,0)&1&11.
\end{array}
\tag{2}
\]

Thus the four global carrier types and dimensions are

\[
\begin{array}{c|c|r|r}
(1,2,9)&(6,0)\otimes(3,3)\otimes(0,0)&1792&44\\
(1,4,9)&(6,0)\otimes(1,4)\otimes(0,0)&980&55\\
(0,2,5)&(5,2)\otimes(3,3)\otimes(2,2)&139968&96\\
(1,4,6)&(6,0)\otimes(1,4)\otimes(3,0)&9800&100.
\end{array}
\tag{3}
\]

The last column is the multiplicity-block dimension.  The full crossed
operator is identity on the carrier and equals the displayed numerical
matrix on that multiplicity block, so carrier multiplicity does not change
the sign in (1).

The holomorphic local (S_7) index convention is

\[
\begin{array}{c|cccccccc}
i&0&1&2&3&4&5&6&7\\ \hline
\lambda_i&[7]&[6,1]&[5,2]&[5,1,1]&[4,3]&[4,2,1]&[3,3,1]&[3,2,2].
\end{array}
\tag{4}
\]

For both leading blocks, the largest negative source contribution comes from
the ordered type

\[
[5,1,1]\otimes[4,2,1]\otimes[4,2,1],
\tag{5}
\]

namely source indices ((3,5,5)).  For ((0,2,5)), the leading negative
source is ((2,5,5)).  These contributions are not individually conclusive:
positive source blocks compensate substantially, so a dual calculation must
retain the common fixed-marginal coupling.

## 2. Independent numerical audits

The saved cap-100 blocks were reconstructed a second time from the 112
source-site representatives.  Each raw union was recovered directly from its
cached marginal frames, each local crossing was independently reshuffled and
factorized, and the signed Gram contributions were accumulated block by
block.

The local Choi matrices have maximum rank twelve.  Their maximum relative
reconstruction error is

\[
6.49\times10^{-15}.
\]

Fourteen source contributions were also evaluated with the original raw
six-index contraction, before any Choi factorization.  The companion JSON
records every absolute and relative discrepancy.  This audits the order of
the six Specht indices and the sign of every local Choi eigenvalue, rather
than merely rerunning the same eigensolver on a cached matrix.

The largest absolute raw-versus-Choi discrepancy is

\[
3.16\times10^{-24}.
\]

Eleven of the fourteen audited contributions have Frobenius norm above
\(10^{-11}\); on those terms the largest relative discrepancy is
\(8.60\times10^{-15}\).  The other three are numerically vanishing terms, so
their relative errors are ill-conditioned and only the absolute audit is
meaningful.

The SHA-256 digest of the cap-100 cache used for (1) is

```
0819c18bbb2222d288b6e8ebc73b622017a68f6f4841a6e60c9540c6f4186bb9
```

All statements in this section remain numerical discovery evidence.

## 3. Exact sparse rational directions

The numerical mixed bases are orthonormal nullspace bases and hence are not
appropriate final certificate coordinates.  The audit explicitly changes
to the rational highest-weight bases constructed from the integral raising
equations.  In those bases, rounding each negative eigenvector gives a very
sparse integer vector that retains a robust numerical negative value:

\[
\begin{array}{c|r|r|r}
\text{block}&\#\operatorname{supp}c&\max|c_i|&c^{\mathsf T}Gc\\ \hline
(1,2,9)&7&1&528\\
(1,4,9)&6&1&912\\
(0,2,5)&6&1&32\\
(1,4,6)&26&2&696.
\end{array}
\tag{6}
\]

The complete integer vectors are embedded in the exact verifier.  Their Gram
norms in (6) are checked with Fraction arithmetic, independently of the
crossed candidate.

For an exact mixed diagram block

\[
\Delta_{\mu_1}(\pi_1)\otimes
\Delta_{\mu_2}(\pi_2)\otimes
\Delta_{\mu_3}(\pi_3),
\]

the rational seed defines the exact scalar

\[
\boxed{
\beta_c(\pi_1,\pi_2,\pi_3)
=c^{\mathsf T}G
\bigl(\Delta_{\mu_1}(\pi_1)\otimes
\Delta_{\mu_2}(\pi_2)\otimes
\Delta_{\mu_3}(\pi_3)\bigr)c.
}
\tag{7}
\]

The verifier evaluates (7) on five deterministic diagram triples.  All
twenty values are integers.  For example, for the leading ((1,2,9)) seed
the signature is

\[
(528,-528,240,240,0).
\tag{8}
\]

This is exact pullback data, not a floating approximation to an eigenvector.

## 4. Exact pullback formula and normalization

Let a holomorphic source block have local (S_7) shapes

\[
\Lambda=(\lambda_1,\lambda_2,\lambda_3)
\]

and raw Specht-coordinate density (X_\Lambda).  Put

\[
R_\Lambda(\boldsymbol\pi)
=R_{\lambda_1}(\pi_1)\otimes
R_{\lambda_2}(\pi_2)\otimes
R_{\lambda_3}(\pi_3).
\]

The exact Fourier coefficient of the raw invariant operator is

\[
a_{\boldsymbol\pi}
=\frac{f^{\lambda_1}f^{\lambda_2}f^{\lambda_3}}{(7!)^3}
\operatorname{Tr}\!\left(
R_\Lambda(\boldsymbol\pi^{-1})X_\Lambda
\right).
\tag{9}
\]

Consequently the exact pullback of the seed (c) is

\[
\boxed{
\Phi_{c,\Lambda}(X_\Lambda)
=\frac{f^{\lambda_1}f^{\lambda_2}f^{\lambda_3}}{(7!)^3}
\sum_{\boldsymbol\pi\in S_7^3}
\beta_c(\boldsymbol\pi)
\operatorname{Tr}\!\left(
R_\Lambda(\boldsymbol\pi^{-1})X_\Lambda
\right).
}
\tag{10}
\]

Every term in (10) is rational.  It can be streamed without storing a dense
global crossing.  Restriction to the exact post-Omega source chart then uses
the rational seed-Gram basis already established for each Λ.

The discovery crossing cache used trace-normalized columns

\[
I_{d_\lambda}\otimes E_{ab}/d_\lambda,
\]

which explains the local factor (f^\lambda/(7!d_\lambda)) in its Fourier
table.  Before applying a raw source density, `local_blocks()` multiplies the
column by (d_\lambda).  Formula (9) therefore has (f^\lambda/7!), exactly
as required.  This normalization is also independently checked by the exact
trace and Hilbert--Schmidt identities in
`verify_dth_level2_local_crossing_oracle.py`.

## 5. What remains

The sparse seeds provide compact rational negative directions and an exact
pullback oracle.  To prove that the two-cone fixed-marginal problem is
infeasible, one must combine one or more pullbacks (10) with an exact dual
multiplier for the fixed-marginal equations so that every holomorphic source
block has positive-semidefinite dual slack.  The negativity of one chosen
primal extension cannot supply that multiplier by itself.

Conversely, a different source extension may repair all four blocks.  The
next numerical task is therefore a genuine two-cone feasibility solve or a
cutting-plane iteration that adds these four mixed PSD constraints to the
fixed-marginal system.

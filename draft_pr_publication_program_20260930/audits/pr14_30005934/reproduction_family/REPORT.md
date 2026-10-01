# PR #14 finite-rank algebra and reproduction audit

**Frozen target:** problem 30005934 / OWR-14298374-003, head `a81fa89f6613791dd55ad5b79bfe8053bd1585f3`.

**Independent verdict:** PASS for finite-rank algebra and computation reproduction. No defect found in this family's assigned scope. This verdict does not certify the moving stochastic tests, conditional-distribution step, or imported noncentral Wishart theorem, and does not alone approve the full proposition or publication.

## Independence, assumptions, and evidence

The frozen `CANDIDATE.md`, the two computation scripts, and their stored receipts were read. Historical `REVIEW.md`, `review_summary.json`, and sibling conclusions were not read before this verdict. No manuscript, canonical problem status, branch, environment, or remote was changed; there was no external communication.

The exact target algebra is: for bounded positive self-adjoint injective `Q`, a strongly continuous semigroup `S`, and finite-rank domain-admissible columns `L`,

\[
C_t=\int_0^t S(s)^*QS(s)\,ds,\quad D_t=I+2L^*C_tL,\quad
\psi_t=S(t)LD_t^{-1}L^*S(t)^*,\quad
\phi_t=\frac\alpha2\log\det D_t.
\]

The test is whether the identities and compressed Laplace expression asserted in the candidate are correct for noncommuting matrices, singular positive tests, nonsymmetric generators, and the zero/sign/dimension parameter boundaries. A pass requires the stated formulas, independently derived checks, and rejection of meaningful corruptions. It does not mean a finite computation establishes an infinite-dimensional probability theorem.

The existing runtime is **Python 3.9.6**, **SymPy 1.14.0**. Both historical scripts ran in isolated `tmp/historical_replay/` and reproduced their receipts byte for byte, with exit code zero and empty stderr:

| Suite | Recorded checks | Receipt SHA-256 |
|---|---:|---|
| `check_identities.py` | 8 | `ce5393b0425d3cf419bc5eb9b95302f06f70464ec7dfeffd63e5cfef016a0172` |
| `independent_review/independent_checks.py` | 19 | `79ff1f388a087c9cbde98f62a320f84bd6478f2c25ff615f9ba4b29294e5515e` |

The author script's Python 3.10+ comment is an overly strong runtime claim for the replayed code: it works in the available 3.9.6 interpreter. This is a minor documentation discrepancy, not an algebra defect.

`independent_probes.py` is new code and passes **29 exact check groups**. It adds generic-entry identities, a distinct stable nonnormal generator, a universal Hilbert–Schmidt coefficient computation, nonsymmetric noise factors, noncommuting rank 0/1/2/3 compression examples, and domain-admissible overlapping directions for a genuinely noninjective semigroup. Its complete exact evidence is in `probe_results.json`.

## Determinant and resolvent compression

Write `v=RR*`, allowing a rectangular factor and singular `v`, and `D=I+2R*CR`. The identity

\[
(I+2vC)R=RD
\]

implies

\[
R D^{-1}R^*=(I+2vC)^{-1}v=v(I+2Cv)^{-1}.
\]

Sylvester's determinant identity gives `det D=det(I+2Cv)`. For `C,v` positive semidefinite, `D` is positive definite, so all these inverses exist. The factor form also proves that the resolvent expression is symmetric positive semidefinite, despite the generally nonsymmetric matrix `I+2Cv`. Therefore the noncentral expression `tr[b v(I+2Cv)^(-1)]` is correct for any positive `b`; no commutation assumption is needed.

The equivalent correct orders are `v(I+2Cv)^(-1)` and `(I+2vC)^(-1)v`. Moving `v` to the other side without changing the inverse's internal order is false. The fresh probes symbolically establish generic 2-by-2 symmetry and equivalent orders, then check positive 3-by-3 examples of all possible test ranks. They reject `(I+2Cv)^(-1)v`, both as an operator and after trace against the chosen positive `b`. Determinants in the four examples are `1`, `61`, `819`, and `12031`.

## Riccati derivative, adjoints, and backward time

With `B=S(t)L`, the domain assumption gives `B'=AB`. Since `D'=2B*QB` and `(D^(-1))'=-D^(-1)D'D^(-1)`, direct differentiation gives

\[
\psi'=A\psi+\psi A^*-2\psi Q\psi,\qquad
\phi'=\alpha\operatorname{tr}(Q\psi).
\]

The adjoint orientation agrees with the weak drift `XA+A*X`: pairing it with a self-adjoint finite-rank test gives `tr[X(A psi+psi A*)]`. In the backward exponential `Z_s=-phi_(T-s)-tr(psi_(T-s)X_s)`, the drift is therefore

\[
\phi'+\operatorname{tr}(\psi'X)-\alpha\operatorname{tr}(Q\psi)
-\operatorname{tr}[X(A\psi+\psi A^*)]
=-2\operatorname{tr}(X\psi Q\psi).
\]

The fresh symbolic probe uses `A=[[-2,3],[0,-1]]`, `Q=[[2,1],[1,3]]`, and `x=exp(-t)`, with

\[
S(t)=\begin{pmatrix}x^2&3(x-x^2)\\0&x\end{pmatrix},\qquad
C_t=\int_x^1 S(y)^*QS(y)\,\frac{dy}{y}.
\]

This generator is stable and nonnormal, materially different from the historical nilpotent examples. The code checks `-x dS/dx=AS`, `-x dC/dx=S*QS`, the full symbolic Riccati identity, log-determinant derivative, and initial values. At `x=1/2`, it rejects swapping generator adjoints, reversing the backward time signs, reversing the Riccati quadratic sign, and halving the quadratic-variation coefficient. For example, the wrong drift-adjoint residual is `19800/48611`, while the wrong time residual is `2696173270/2363029321`; neither is zero.

This confirms the deterministic algebra of cancellation. It does not prove that the weak stochastic equation admits these moving tests; that is an analytic gate for the separate review family.

## Quadratic variation and the factor four

Let `R=sqrt(X)` and `T=sqrt(Q)`. For a real Hilbert–Schmidt direction `E` and self-adjoint test `v`, the scalar noise functional is

\[
\operatorname{tr}[v(RE T+TE^*R)]
=2\operatorname{tr}(TvRE)
=\langle2RvT,E\rangle_{HS}.
\]

The representing integrand is thus `2RvT`, and its squared Hilbert–Schmidt norm is

\[
4\operatorname{tr}(XvQv).
\]

The two terms use the same cylindrical Brownian motion. Their cross variation is already included in the squared combined coefficient; treating them as independent terms would lose a factor two. The original stochastic coefficient needs no square root of the test `v`, and this identity also holds for indefinite self-adjoint tests.

Fresh code proves this coefficient and variance identity for unrestricted symbolic symmetric 2-by-2 `R,T,v`. It independently enumerates every matrix-unit Brownian direction for dimensions 1, 2, and 4, including nonsymmetric covariance factors `X=RR*`, `Q=TT*`. The exact variances are `144`, `3892`, and `1092840`. Factors one and two are rejected. Half of the correct QV, namely `2tr(X psi Q psi)`, is exactly the scalar Itô correction needed to cancel the exponent drift above.

The passage from the Hilbert–Schmidt norm identity to locally defined infinite-dimensional scalar stochastic integrals is not certified merely by these matrix checks.

## Positive integrated covariance despite a noninjective semigroup

This is a deduction, not a matrix-model assumption. For fixed nonzero `h`, positivity and injectivity of `Q` imply `||sqrt(Q)h||>0`. Strong continuity at zero gives an interval `[0,epsilon]` on which `||sqrt(Q)S(s)h||` stays bounded below by a positive number. For any `t>0`, integration over a sufficiently small positive interval yields `⟨C_t h,h⟩>0`. This proves strict positive definiteness of every finite-dimensional injective compression. It does not assert a uniform infinite-dimensional lower bound, or trace-class covariance.

A checkable example is the killed left shift on `L2(0,1)`:

\[
(S(t)f)(r)=f(r+t)\mathbf1_{\{r+t<1\}},\qquad Q=I.
\]

It is noninjective for every positive `t`, and identically zero for `t>=1`. Nevertheless,

\[
\langle C_Tf,f\rangle=\int_0^1\min(T,r)|f(r)|^2\,dr>0
\]

for every nonzero `f`. The new exact probes use overlapping directions `f_i(r)=(1-r)^2r^i`, `i=0,1,2`. They satisfy `f_i(1)=f_i'(1)=0` and belong to `D(A^2)` for this shift generator. Their compressed covariance Gram matrices are strictly positive definite at `T=1/10,3/5,1,2`, as shown by exact positive leading minors. The directions can be orthonormalized without changing definiteness. This verifies a concrete noninjective example of the covariance mechanism; it constructs no Wishart solution.

## Parameter normalization and boundary cases

For a real scalar Gaussian `Z` with mean `mu` and variance `c>0`, square completion gives

\[
\mathbb E e^{-vZ^2}=(1+2cv)^{-1/2}
\exp\{-\mu^2v/(1+2cv)\}.
\]

The new code verifies the square completion symbolically. Multiplication for independent Gaussian squares fixes `alpha=m`, determinant exponent `-alpha/2`, scale `2C`, and noncentrality as the sum of mean outer products. Thus there is no factor-of-two error in converting between the candidate's diffusion parameter `alpha` and the transform's exponent `p=alpha/2`. This normalization check does not prove the imported parameter theorem.

Assuming the candidate's stated necessary parameter set in dimension `n`,

\[
\alpha\in\{0,1,\ldots,n-2\}\cup[n-1,\infty),
\]

the arithmetic is correct. For a nonnegative noninteger `alpha`, `n=floor(alpha)+2` satisfies `n>alpha+1`, so `alpha<n-1` and `alpha` misses the discrete set. The fresh probes cover small and large rational examples; `alpha=801/8` is excluded in dimension `102`. All nonnegative integers survive these necessary parameter sets, which is not an existence assertion.

Negative `alpha` is excluded already in dimension one: as `v=r` tends to infinity, `exp[-br/(1+2cr)]` tends to the strictly positive constant `exp[-b/(2c)]`, while `(1+2cr)^(-alpha/2)` diverges. An exact witness for `alpha=-2,c=b=1,r=1` is `3exp(-1/3)>2>1`, impossible for a probability Laplace transform. The zero boundary is correctly retained: with `alpha=0` and `X_0=0`, the zero process and constant transform one are consistent. No claim about arbitrary initial values at `alpha=0` is made.

## Exact remaining gaps and reproducibility

The strongest verified result of this family is that the candidate's finite-rank deterministic algebra, noise-coefficient algebra, covariance positivity argument, normalization, and obstruction-dimension arithmetic are correct, and that both stored historical receipts reproduce exactly. No central difficulty has been discharged by a finite numerical surrogate.

The following remain outside this verdict: passage from fixed weak equations to moving graph-norm tests with localized stochastic convergence; regular conditional laws and a common countable-test null set for random initial data; applicability and proof of the imported noncentral Wishart theorem; and source/priority/publication assessment. They must receive their own independent review before the overall proposition is promoted.

Reproduce from the repository root using the existing environment:

```text
.venv/bin/python draft_pr_publication_program_20260930/audits/pr14_30005934/reproduction_family/reproduce_historical.py
.venv/bin/python draft_pr_publication_program_20260930/audits/pr14_30005934/reproduction_family/independent_probes.py
```

Tracked receipts are `historical_replay_results.json`, `author_replayed_receipt.json`, `historical_independent_replayed_receipt.json`, and `probe_results.json`. Regenerable scratch is ignored. The family research log records timestamps and completion estimates.

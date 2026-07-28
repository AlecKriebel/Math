# Checkpoint 2B — Adversarial Re-review

**Reviewer:** standing adversarial subagent  
**Verdict:** conditional go as a synthesis/framework checkpoint; no-go as a
novelty-bearing foundation for a new mathematical branch  
**Score:** 9/14

| Criterion | Score | Finding |
|---|---:|---|
| Mathematical coherence | 2 | Main constructions and proofs are substantially correct |
| Novel object/invariant | 1 | Useful packaging; signature and margins have standard reductions |
| Coordinate/gauge invariance | 1 | Orthogonal covariance was sound; affine gauges needed completion |
| Theorem depth | 1 | Affine result and guard-margin result are imported |
| Nonsmooth coverage | 1 | Partial guards are modeled; no new seam-dynamics theorem |
| Predictive utility | 1 | Falsifiable examples, initially without a native failure-conversion test |
| Cross-domain naturalness | 2 | Configuration repair and online allocation are recognizable domains |

## Decisive collision

For a continuation domain \(D\), define \(h_D=1_D\). Its exact pointwise
robustness radius is

\[
\rho_D(y)=\inf\{d(y,z):h_D(z)\ne h_D(y)\}=m_D(y).
\]

Therefore

\[
d(y,y')<m_D(y)\Longrightarrow h_D(y)=h_D(y')
\]

is the defining metric robustness certificate. Substituting route outcomes
\(y=p(x)\), \(y'=q(x)\) gives a useful NCS interpretation but no new
mathematical content. Fainekos and Pappas already define distance, depth, and
signed-distance robustness in arbitrary metric spaces and prove
truth-preservation for predicates and temporal/hybrid traces (TCS 410 (2009),
DOI `10.1016/j.tcs.2009.06.021`). The distributional statement is a
boundary-band risk bound of the same type used in robust classification.

Required disposition: call the result an imported signed-distance
guard-robustness lemma and the distributional estimate a baseline indicator
bound.

## Mathematical corrections required

1. Define the Lipschitz modulus as an infimum over finite-distance pairs in an
   extended metric space.
2. Preserve directional failure:
   \(A_\mu^+=\mu(D_p\setminus D_q)\) and
   \(A_\mu^-=\mu(D_q\setminus D_p)\).
3. For \(E=D_p\cap D_q\) and
   \(\delta(x)=d(p(x),q(x))\), use the sharper exposure
   \[
   \mu\{x\in E:
   \max(m_D(p(x)),m_D(q(x)))\le\delta(x)\}.
   \]
   Membership disagreement forces *both* endpoint margins below the mutual
   distance. The earlier `min` used the looser union of seam bands.
4. Partition the corollary proof into original asymmetric failure, common
   failure, and common success. Outside a domain symmetric difference, both
   prefixes need not succeed; both can fail.
5. State that presentation-response morphisms ignore weights, or add
   derivation witnesses and quantitative weight distortion.
6. Extend affine gauge covariance from origin-fixing orthogonal maps to
   \(\phi_b(x)=Q_bx+g_b\).
7. Make response-order logarithms dimensionless; use cofinal bi-Lipschitz
   reparameterizations; separate sparse and eventual failure scales.
8. Specify the allocation fibers and full partial maps, including the feasible
   input \(A\to2\) for the “add \(B\)” edge.
9. Exercise guard failure conversion in a native example.

## Novelty assessment

The deterministic domain/value split is operationally useful, but after
totalizing undefined values to \(\bot\), its asymmetric-failure-plus-value
part is a decomposed bounded \(L^1\) distance. Common failure is
common-\(\bot\) mass. This is a reporting convention, not a new invariant.

The affine relation operator is correct and genuinely accommodates
noninvertible edge maps, but its Moore–Penrose estimate is known Hyers–Ulam
theory. The response-order calculus is standard order-of-vanishing machinery
used across several response sectors.

No stronger theorem survived the prior-art audit. The checkpoint can support
an honest field proposal only as an interdisciplinary modeling synthesis.
Research-program status should depend on solving such problems as partial
Ulam stability, dependence-sensitive transported seam exposure, regular-guard
failure asymptotics, and presentation comparison under weighted refinements.

## Disposition

All listed correctness repairs were incorporated into the frozen Checkpoint 2
statement. The seam result and signature were demoted in the novelty ledger.
The checkpoint is accepted for continuation to applications and paper
construction, with the explicit label **candidate synthesis/research
program**, not established new branch.

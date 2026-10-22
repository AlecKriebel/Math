# Status: scoped results, original question not fully resolved

Target: rank 663, 4000018 / AMR-039-0018, *L2 Bonnet–Myers and dimension*.
Original source: Yann Ollivier, *Discrete Ricci curvature: Open problems*, Problem R.

**Verdict: UNSOLVED, five substantive approaches completed.** This packet proves an obstruction to a universal finite-dimensional converse for arbitrary Markov semigroups, and a positive implication in canonical finite-dimensional heat-flow settings. Neither is represented as a complete answer to the source's open-ended request for a dimensional interpretation.

Main proved result: On any metric probability space of diameter at most one, the reset semigroup

\[
P_t f=e^{-2t}f+(1-e^{-2t})\int f\,d\nu
\]

satisfies

\[
W_1(P_s^*\delta_x,P_t^*\delta_y)
\le e^{-\min(s,t)}d(x,y)+\frac{16(\sqrt t-\sqrt s)^2}{2d(x,y)}
\]

for all distinct points and all \(0\le s,t\le1/4\). This includes compact geodesic examples with full-support reversible invariant measure in arbitrarily large, and even infinite, Hausdorff dimension. On an atomless space its generator satisfies \(BE(1,\infty)\), but no \(BE(1,N)\) for finite positive \(N\). The generator is nonlocal and is not the canonical heat generator for the given metric.

Other proved results:

- Under the cited finite-dimensional space-time \(W_2\) heat-flow estimate, \(C=2Ne^{KT}\), \(\kappa=K>0\) is admissible on the horizon \([0,T]\). This applies to the RCD* setting in Erbar–Kuwada–Sturm and to the complete smooth diffusion setting in Kuwada, subject to the explicitly recorded assumptions.
- Time and metric scaling prevent identifying an unnormalized admissible \(C\) with an intrinsic dimension. A chosen \(C\), a best \(C\), and an admissible upper dimension \(N\) are different objects.
- Standard Euclidean Brownian motion has the rigorous calibration \(n-1\le C_*\le n\); in dimension one the coefficient cannot be zero. This is a zero-curvature calibration, not a positive-curvature counterexample to Bonnet–Myers.
- Ornstein–Uhlenbeck provides exact same-time positive-curvature contraction and \(BE(\lambda,\infty)\) but violates the proposed uniform unequal-time estimate for every finite \(C\).

The source's finite-scale theorem is Proposition 52, with epsilon-geodesicity, a scale restriction, and an additive \(4\pi\varepsilon\) diameter correction. Dropping those hypotheses is not justified. The transport in Problem R is \(W_1\), despite “L2” in the title.

See FULL_PROOFS.md, SOURCE_AND_ASSUMPTIONS.md, APPROACH_LOG.md and LIMITATIONS.md. The exact controls are corroboration of the written arguments, not a proof of the original problem. Independent adversarial audit is required before publication. No historical novelty, priority, or human-peer-review claim is made.

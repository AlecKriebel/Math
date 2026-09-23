# Verification summary and proof checklist

## Verdict

The stated theorem has a complete analytic proof for the two explicitly defined unitary-group length metrics. Independent reviewers found no remaining gap. The proof answers the literal printed assertion of Gromov [?24](i) with the stronger requirement of never increasing the Lipschitz constant. Reviews are internal, AI-assisted, and not external peer review.

## Checkable chain

| Step | Input | Check | Output |
|---|---|---|---|
| Image confinement | Lip Φ = L ≤ 1/2; sphere diameter π | Eigenvector path length bounds every principal eigenangle by d(I,W) ≤ πL | Re W ≥ 0 |
| Invertibility | W unitary; Re W ≥ 0 | (I+tW)*(I+tW) ≥ (1+t²)I | inverse norm ≤ (1+t²)^(-1/2), even at t=1 |
| Unitarity | X=W+tI; Y=I+tW | X*X=Y*Y | XY^(-1) unitary |
| Contraction | Ordered numerator identity | Mixed products UV cancel without commuting U,V | difference and derivative norm ≤ q_t |
| Intrinsic metric | Φ restricted to a minimizing domain geodesic | Absolute continuity, chain rule, integrate matrix-norm speed | Lip H_t(Φ) ≤ q_t L |
| Family continuity | Nearby anchors and normalized maps | sup-norm bound 3δ; uniform time continuity on compact semicircle | Jointly continuous deformation |
| Retraction | Substitute W=I, t=0, t=1 | Exact identities | Constants fixed; endpoint Φ(p) |

The intrinsic step uses the actual image of a domain geodesic. It does not assume that a minimizing target geodesic remains in the semicircle or equate chordal distance with intrinsic distance. The algebra report provides a local logarithm comparison if an explicit justification for equality of curve lengths is desired.

## Independent mechanisms

- **Möbius/resolvent route:** passes for Hilbert–Schmidt and operator norms; proves the advertised coefficient and the closed boundary.
- **Principal-power/geometric route:** independently verifies a nonincreasing deformation in Hilbert–Schmidt norm. A stronger HS threshold derived in the geometric report is auxiliary and is not a claimed result of the released paper.
- **Adversarial tests:** noncommutativity, nonsmooth maps, anchor variation, t=0/1, eigenangles ±π/2, scalar target, domain antipodes, and the optional two-point sphere all pass.
- **Finite diagnostics:** 10 exact checks and 7,679 fixed-seed numerical checks pass. These test identities and instances, not the quantified theorem.

## Qualifications

The source's shortest-geodesic normalization does not specify every invariant metric uniquely. The theorem explicitly defines its metrics. In the operator-norm metric, the normalization statement is restricted to closed one-parameter subgroups; arbitrary metric geodesics of a nonsmooth norm require care. The final manuscript review records this correction.

There is no mathematical gap identified in the released theorem. First-publication priority remains unestablished: the bounded audit found no earlier explicit resolution, while identifying classical machinery and the elementary logarithm-chart solution to the weaker topological assertion. Specialist human review could further assess the note and its historical context; no outreach has been made or prepared.

# Verification report and proof map

## Verdict

The candidate proof is mathematically complete for the real linear change-of-basis problem printed as Brandes's Problem 11 on p. 3182 of Oberwolfach Report 50/2019. It covers the absolute-value version. The final paper strengthens the conclusion to unit diagonal and strictly positive mixed entries below one. No gap remains identified under its explicit hypotheses and coefficient convention.

This is an internal AI-assisted verification, not external peer review or a proof-assistant formalization. The bounded priority search found no prior full resolution; it does not certify first priority.

## Exact scope and success criteria

- p is a real homogeneous polynomial, positive away from zero, in dimension m >= 1, with positive degree (therefore even d >= 2).
- Coefficients are entries of the unique symmetric polarization A, summed over **all ordered tuples**. An ordinary monomial coefficient is the tensor entry multiplied by its multinomial factor.
- One invertible real matrix must work simultaneously for every tuple, including repeated indices. No orthogonality, determinant normalization, integrality, or basis-conditioning bound is requested in the primary source.
- An admissible proof must justify strict mixed inequalities before choosing a common small perturbation and must handle pure equality exactly.

## Checkable proof map

| Step | Evidence | Status / gap |
| --- | --- | --- |
| Authenticate the problem | Publisher PDF rendered at p. 3182; source URL and SHA-256 in sources/inventory.json | Passed; catalogue itself unavailable (429) |
| Find a positive tangent slice | Sphere minimum c>0; p/c >= norm^d; first and second derivative at the touching point | Complete |
| Candidate logarithmic calculation | Full independent coefficient derivation in adversarial-proof.md | Complete |
| Shorter polynomial-gap calculation | Paper equation (3): leading term d/2 times sum Q(a_r-a_s,a_r-a_s) | Complete |
| One actual basis | Columns v+epsilon*w_i with w_m=0; tangential decomposition proves independence for epsilon != 0 | Complete |
| Simultaneous absolute bound | Positive quadratic term for every mixed tuple; finiteness; continuity gives positive numerators; pure gap identically zero | Complete |
| Restore scale and normalize diagonal | Both sides scale by c; positive column rescaling | Complete |
| Independent mechanism | Positive bilinear slices on a cone; Cauchy–Schwarz; maximizing coefficient with maximal sum alpha_i^2 is pure | Complete; stronger cone theorem in independent-geometry.md |
| Rational verification companion | 12 certificates,120 classes,110 independent polarization checks;23 finite symbolic degree checks;2 rejection controls | Passed; finite checks only |
| Final manuscript | Independent source/equation/scope review, with two minor wording/reference corrections applied | Passed; see final-manuscript-review.md |
| Priority | 2015 precursor credited; direct and related primary-literature searches | No earlier full solution found; priority not established |

## Boundary and failure controls

Dimension one gives only pure tuples. Degree two reduces to a positive quadratic form. Odd positive degree is impossible because p(-x)=-p(x). Degree zero is excluded because the question's 1/d exponent is undefined. Merely semidefinite forms do not give the strictly positive sphere minimum used here. The proof makes no such extension.

Global convexity and a universal Hölder inequality on all vectors are not assumed. The nonconvex quartic x^4-x^2*y^2+y^4 is positive definite and is included in exact checks. The positive quartic x^4+12*x^2*y^2+y^4 violates the ordered bound in its initial basis, confirming that a coordinate change matters. The basis may be arbitrarily poorly conditioned; this is compatible with the source.

## Approach-family ledger

The direct algebra and independent geometry agents began separately. They share the valid idea of a positive slice at a sphere minimum but use distinct mechanisms for the central mixed inequality: Taylor/polynomial coefficients versus conditioned Cauchy–Schwarz and a discrete maximum. A further adversarial check independently reviewed the latter. The local-convexity-only shortcut would leave the mixed inequality unsupported; it was not used. No unresolved route is silently substituted for the desired theorem.

Outside bibliographic expertise might reveal missed prior work. No outreach was prepared or initiated, in accordance with the project's independent-research policy.

## Fresh preprint-readiness cycle, 23 September 2026

Three newly spawned adversarial reviewers independently challenged the existing paper. The second reconstructed the bilinear-slice/Cauchy–Schwarz mechanism independently. During integration, root corrected a coefficient in a new auxiliary negative-control calculation and added direct-evaluation/polarization checks. The third reviewer independently re-derived the corrected formula and reassessed the paper. No theorem, proof, original-verifier or PDF change was required. See [the decision and dispositions](preprint-readiness.md), [Round 1](preprint-round-1.md), [Round 2](preprint-round-2.md), and [Round 3](preprint-round-3.md). Older reports remain historical snapshots; the fresh reviews identify the unchanged manuscript by SHA-256.

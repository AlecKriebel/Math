# Bounded acceptance for the elasticity Lavrentiev question

## Review status of this edition

This AI-assisted mathematical exposition and independent internal AI source/proof audit are unrefereed. Bounded acceptance here does not mean external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification. The AKM result is prior published work; no novelty is claimed. Deep cited existence, finite-distortion, change-of-variables and topological dependencies remain external. No author was contacted.

Problem identity: Ball 2002 Problem 4; catalog identifier 2000004; code AMR-019-0004.

## Accepted

A prior, published Lavrentiev-gap result by Almi–Krömer–Molchanova in the exact two-component reference geometry, with homogeneous polyconvex energy, positive Jacobian almost everywhere, continuity-forcing p>d growth, partial Dirichlet data and the Ciarlet–Nečas condition on both comparison classes.

The accepted parameter ranges are:

- d=2: p>2 and 1<q<p/(p−2).
- d=3: 3<p<4 and 2<q<p/(p−2).

The comparison is between the admissible W^{1,p} minimum (existence from the cited Theorem 2.3) and the admissible Lipschitz infimum. The low-energy bound is o(s), while the Lipschitz infimum is between m s and M s for all sufficiently small s. The explicit p=7/2, q=11/5 corollary avoids all endpoints.

Acceptance is by substantive source/hypothesis reconciliation and examination of the proof architecture, with elementary local corrections recorded in ENDPOINT_AND_PROOF_NOTES.md. The external existence, finite-distortion, change-of-variables and topological results remain cited dependencies. There is no claim that they, or the underlying full theorem, were independently reproved.

## Not accepted by this audit

- An unqualified solution attributed to the one-dimensional Ball–Mizel examples or an unspecified elastic-bar reduction.
- The two-dimensional endpoint q=p/(p−2) as verified by the printed logarithmic competitor. The exact determinant calculation proves that competitor has infinite determinant-penalty energy. This is a failed proof step, not a disproof of the endpoint theorem.
- A connected reference domain with only boundary mixed-Dirichlet constraints, inferred solely from Remark 3.1.
- Substitution of everywhere-injective homeomorphisms or their closure for the Ciarlet–Nečas class.
- Removal of CN, or extension to every p>3, the three-dimensional upper endpoint, incompressibility, or higher dimensions without further work.
- A claim of novelty or a new solution to Ball's problem.

## Recommended status language

“Prior result, accepted with scope qualifications: AKM (ZAMP 75:2, 2024), Theorem 4.1 and the strict-range part of Theorem 3.2 give a continuous-deformation Lavrentiev gap on two disconnected components with partial Dirichlet data and Ciarlet–Nečas admissibility. The written connected-domain extension is not supplied. The printed 2D endpoint competitor fails determinant integrability.”

For the broad existential question allowing multiple reference components and CN, the accepted three-dimensional result is a genuine affirmative literature answer. For the stronger connected-domain, boundary-only interpretation, this audit establishes relevance and a precise missing interface; it does not certify a complete answer. This is not an assertion that the stronger interpretation is globally open in all subsequent literature.

## Scope of work and evidence

The controlling Ball hypotheses, both AKM published theorem statements, the full two- and three-dimensional proof chains, the exact reference configurations, the connecting-piece remark, and the endpoint formula were inspected. The publisher PDF confirms that the endpoint issue is present in that version as well as arXiv v2. A bounded erratum search found no repair; that negative result is not exhaustive.

Public source titles, URLs, versions, byte counts, SHA-256 hashes and inspection ranges are recorded in SOURCE_METADATA.json. The theorem summary, hypothesis audit, proof note and this acceptance are authored mathematical commentary. They contain no copied third-party source documents or private coordination material.

## Citations

Ball, Some open problems in elasticity (2002): https://people.maths.ox.ac.uk/ball/Articles%20in%20Conference%20Proceedings%20and%20Books/JMB%202002%20re%20Marsden%2060th.pdf

Almi, Krömer and Molchanova, A new example for the Lavrentiev phenomenon in nonlinear elasticity, ZAMP 75:2 (2024): https://doi.org/10.1007/s00033-023-02132-4 ; arXiv v2 https://arxiv.org/abs/2309.08288v2

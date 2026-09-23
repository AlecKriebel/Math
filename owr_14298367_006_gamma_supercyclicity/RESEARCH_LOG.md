# Research log: OWR-14298367-006

Goal: verify the supplied arbitrary-Gamma supercyclicity equivalence against the original problem, audit priority, and only if warranted publish a concise proof and reproducibility package.

## 2026-09-23T04:04:28Z — Initial verification checkpoint (35%)

- Working on `main` in a dedicated top-level folder. Pre-existing unrelated changes are excluded from this effort.
- The index page is unavailable (HTTP 429); recovered the official Oberwolfach Report 19/2024, DOI 10.4171/OWR/2024/19. Exact question is on printed p.1083.
- Target: for every fixed subset Gamma of the complex field, existence of a dense Gamma-scaled forward orbit is equivalent for the composition operator and its associated scalar weighted bilateral shift. This is not a claim that all such operators are supercyclic.
- Standing assumptions: 1 <= p < infinity, separable complex Lp space, bijective bimeasurable nonsingular map with bounded invertible composition operator, a finite positive-measure wandering generator, and uniform bounded distortion.
- Independent approach families: (1) adversarial audit of the supplied tail estimates and constructive proof; (2) primary-source matching and measure-theoretic conjugacy audit; (3) alternative Baire-category amplification argument. All three are in progress with distinct owned audit files.
- Preliminary direct check finds no gap in the scalar tail estimates or constructive amplification. Separability must be explicitly retained; sigma-finiteness alone does not imply it.
- Early literature triage finds that the scalar arbitrary-Gamma tail criterion predates this candidate. Its status as a claimed new by-product requires correction. A dedicated priority audit is now in progress; no novelty decision yet.
- Success criteria: checkable proof under the actual hypotheses; independent adversarial agreement; correct attribution and no located prior resolution; verified final artifacts. Computational checks, if included, will check finite identities and examples rather than purport to prove an infinite-dimensional theorem.
- No external individuals have been contacted and no outreach will be prepared.

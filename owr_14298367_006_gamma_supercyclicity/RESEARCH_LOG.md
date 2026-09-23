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

## 2026-09-23T04:08:18Z — Verification and priority checkpoint (85%)

- All three initial independent approaches pass in the source's separable setting. Both the original construction and a shorter Baire-category proof are checked. The source/conjugacy audit gives an explicit counterexample if separability is dropped.
- Decisive priority finding: Abbar (2019) explicitly provides the scalar criterion and a general Gamma-supercyclicity criterion. Abbar–Kuznetsova (2020 preprint, 2021 journal article), Theorem B, also implies the entire amplification statement through Z, Z², and a bounded dense-range coefficient map.
- A separate source reviewer independently verified this prior-theorem deduction. It does not depend on the candidate's tail proof or amplification lemma, so there is no circular priority argument.
- Distinguish two claims: the full mathematical equivalence is verified; an explicit previously published answer to this particular Oberwolfach question has not been located. A new scalar criterion or new amplification theorem cannot responsibly be claimed here.
- User was informed of the overlap and offered an optional choice between audit-only delivery and an attributed explanatory package. In the absence of changed scope, the user's original clean-priority condition governs: no original-resolution paper/site/Zenodo package.
- Initial checkpoint committed and pushed as `aad71a7df`.

## 2026-09-23T04:11:29Z — Final audit checkpoint (100% of verification and priority decision)

- Exact original question on printed p.1083 visually inspected from the official PDF; source hashes and primary locators recorded.
- Final adversarial review rechecked both the prior theorem's hypotheses and the Z²/dense-range deduction. No material mathematical or reporting correction remains.
- All four exact-arithmetic check groups pass. They check finite identities and examples, not the infinite-dimensional theorem. Output is preserved in `verification/results.json`.
- Final status: proof PASS in the original setting; originality gate NOT CLEAR; conditional original-resolution publication does not proceed. The complete audit, analytic proof, source records, and verifier are the deliverable. An attributed application note would be a separate publication scope.
- Remaining gap is bibliographic/editorial, not a gap in the verified equivalence: who first explicitly observed the application to this 2024 question is not established. A claim of new criterion/amplification is blocked by the concrete older results; further keyword searching alone cannot remove that overlap.
- No GitHub release or Zenodo deposition is created, and no person is contacted.

# Public source and claim ledger

Checked 2026-10-09. Hashes identify the inspected bytes, not mathematical correctness. Only authored mathematical analysis and public-source metadata are included in this edition. Source copies, extracted text and renderings are excluded.

## Primary sources

### OWR 14/2016

- Public URL: https://ems.press/content/serial-article-files/46618
- Source: Justyna Szpond's contribution, joint with Marcin Dumnicki and Daniel Harrer, printed pp.695–697.
- Inspected definition and Conjecture 1 at p.696; rendered conjecture page checked against the DHS display.
- 479,779 bytes; SHA-256 `1ebdfcab0ae22c16adfc3e8b12c13477cec1a6ae57cbe34469f1c16ccbda3fcf`.
- Public PDF originally retrieved 2026-10-09T23:08:40.710724+00:00.
- Purpose: exact all-fields target, prime-power rule, epsilon thresholds, finite band and special endpoint.

### Dumnicki–Harrer–Szpond

- Public URL: https://arxiv.org/pdf/1507.04080 ; version record: https://arxiv.org/abs/1507.04080v2
- Title: *On absolute linear Harbourne constants*.
- Published: Finite Fields and Their Applications 51 (2018), 371–387; DOI https://doi.org/10.1016/j.ffa.2018.03.001 . The official publisher record confirms this status.
- 162,237 bytes; SHA-256 `171fbcdbf266753e217476c5731109216318aa2c55be8d1a901d13e5fcff112e`.
- Public PDF originally retrieved 2026-10-09T23:08:36.799707+00:00.
- Inspected Sections 1–5, especially Definition 1.1, Conjecture 1.2, Theorems 1.4/1.6, Corollary 4.1 and Proposition 5.1; rendered pp.2–3 visually checked.
- The PDF sidebar identifies arXiv v2, 13 January 2016. Its title-page generated date reads 23 July 2021. This is recorded without inferring a different arXiv version or new publication.
- Credited inputs: d≤31 values, full-plane exact values, pair-count methodology and all finite-plane upper-bound constructions. The mathematical text does not state the general one-line-deficit lower-bound theorem proved in the report; this inspection does not establish worldwide novelty.
- Source discrepancy: at q=2,d=4 the literal special expression gives −6/5, conflicting with its own H(4)=−4/3. The special construction's multiplicity-(q−1) point is nonsingular then. This known small case is not presented as a new counterexample.

### Erdős–Mullin–Sós–Stinson (EMSS)

- Title: *Finite linear spaces and projective planes*.
- Published: Discrete Mathematics 47 (1983), 49–62; DOI https://doi.org/10.1016/0012-365X(83)90071-7 .
- Acquired public primary scan: https://users.renyi.hu/~p_erdos/1983-05.pdf
- 1,725,402 bytes; SHA-256 `53f080d78d1bc027c060bd9ae95d726ad30323e58b32a351dd392be364178507`.
- Retrieved 2026-10-09T23:30:38Z. The alternate indexed institutional hostname was used after the www.renyi.hu URL returned HTTP 403 locally. Web extraction had succeeded at the www hostname; no authentication or private access was attempted.
- Inspected full extracted text and visually inspected printed pp.53–57, 60–61. Definitions on p.49 and the theorem domains were checked; NLS excludes near-pencils and its blocks are proper subsets.
- Imported results: Theorem 3.6; Lemmas 3.7–3.8, 3.11, 3.14, 3.16–3.17, 3.20–3.21; Corollary 3.12; Theorem 3.23. The report states their exact roles rather than claiming an independent proof of the full paper.
- Source discrepancy: Lemma 3.20's displayed even/odd labels are reversed relative to its proof. The proof and Lemma 3.22/Theorem 3.23 agree with each other. The report derives the degree-excess parity bounds from the proof's class-count inequalities and discloses the discrepancy.
- The completion plane can be abstract. It is used for counting only. Field-plane constructions separately establish realizable attainment.

## Source-to-result boundary

The report's mathematical contribution is the ratio comparison using consecutive-integer quadratic bounds, its combination with the credited minimal-linear-space/completion results, the integer sharpening of the degree-excess test, and the exact residual realizability obstruction. No literature-wide novelty, complete conjecture resolution, new small-case counterexample, proof-assistant certification, or independent validation of all EMSS arguments is claimed.

The all-fields lower bounds do not assume configurations are deletions from a finite plane. The cited theorems establish embedding only in the minimal cases where it is invoked. Nonminimal configurations are excluded by a separate inequality, and pencils/near-pencils are handled separately.

## Disposition and inspection limits

The original target's general residual status is unresolved after one shared substantive approach, 1/5. Broader targets 30003086 and 30004521 share that history if the same mathematical work is reused. Preparation of this edition adds no proof-search approach.

The [independent mathematical audit](INDEPENDENT_AUDIT.md) accepts only the bounded partial theorem, with the literal q=2 endpoint exception preserved. The packaging check rehashed the same three held public PDFs and matched their recorded byte counts and SHA-256 values. No new source download, new literature search or independent proof of the whole EMSS paper was performed during editorial preparation.

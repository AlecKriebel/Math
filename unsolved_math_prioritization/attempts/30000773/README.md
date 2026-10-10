# Attracting edges under reciprocal summability

Problem **30000773 / OWR-1543-004**, historical queue rank 1226, is credited to the prior Cotar–Thacker result for its original bounded-degree, ordinary-initialization scope. This is a proof-only audit edition with **zero new proof-search turns**, not a new solution or priority claim.

Codina Cotar and Debleena Thacker, *Edge- and vertex-reinforced random walks with super-linear reinforcement on infinite graphs*, Annals of Probability 45(4) (2017), 2655–2706, [DOI 10.1214/16-AOP1122](https://doi.org/10.1214/16-AOP1122), is the credited published article. The full proof inspected for this audit is [arXiv:1509.00807v3](https://arxiv.org/abs/1509.00807v3), dated 2 June 2016. The journal proof was unavailable for inspection.

The authored certificate, proof audit, and acceptance report in this edition are **AI-assisted and unrefereed**, with no proof-assistant certification. That status is distinct from the prior article's journal publication.

## Accepted scope

The original target is almost-sure eventual alternation along one undirected edge of a connected bounded-degree simple graph with at least one edge, including the triangle, with a common finite nonnegative integer initial count and arbitrary positive finite reciprocally summable reinforcement. The weights may be nonmonotone.

The written proof additionally verifies every finite connected simple graph with at least one edge and finitely many initial offsets whose individual shifted reciprocal series converge, and infinite bounded-degree graphs whose offsets range over a finite set with convergence at each offset. Nonnegative integer offsets under the stated reciprocal-summability and bounded-initial-reinforcement assumptions reduce to that finite-set scope.

Arbitrary real edge-dependent offsets under the manuscript's conditions (6) and (8) are theorem-cited but are **not independently proof-certified** here. No unbounded-degree, directed-edge, or vertex-reinforcement extension is asserted.

## Manuscript estimate correction

The inspected manuscript's formula (36) is false as printed. On the integer line, with zero initial offsets and reinforcement w(j)=10^j, the relevant forward-fixation probability is at most 1/11, while its asserted product lower bound is at least 7/36. The full exact derivation is retained in Section 5 of [PROOF_AUDIT.md](PROOF_AUDIT.md).

This is an error in the displayed estimate, not a counterexample to attracting-edge fixation. Sections 3 and 4 give the corrected finite-offset frontier product and confinement argument. The journal proof was not obtained; no defect in that uninspected version is claimed.

## Reading guide

- [PRIOR_APPLICABILITY_CERTIFICATE.md](PRIOR_APPLICABILITY_CERTIFICATE.md): original question, exact model, hypothesis matching, and boundaries.
- [PROOF_AUDIT.md](PROOF_AUDIT.md): complete finite count-vector proof, corrected finite-offset infinite proof, exact manuscript discrepancy, and limitations.
- [ACCEPTANCE_REPORT.md](ACCEPTANCE_REPORT.md): mathematical disposition and required qualifications.
- [SOURCE_LEDGER.md](SOURCE_LEDGER.md): public citations, PDF byte identities, inspection history, and journal-access limits.
- [VERIFICATION.json](VERIFICATION.json): mathematical audit status and certification boundaries.
- [STATUS.json](STATUS.json): machine-readable scope, attribution, and turn count.
- [PROVENANCE.md](PROVENANCE.md): edition provenance and dated research checkpoint.
- [MANIFEST.json](MANIFEST.json): exact edition membership and SHA-256 identities.

This edition contains authored mathematical exposition and public verification metadata. It includes no copied source-document bodies, extracts or images; dataset contents; computational scripts, logs or result artifacts; or private coordination material.

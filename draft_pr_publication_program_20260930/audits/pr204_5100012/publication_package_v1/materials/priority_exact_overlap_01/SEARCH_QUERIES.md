# Bounded indexed queries and access log

Nine queries total, in three batches on 2026-10-16 UTC. Search results were treated as leads. Positive statements below rely on the primary PDFs/metadata described in PRIMARY_SOURCE_ACCESS.md and PRIMARY_RECEIPTS.json. No further broad queries are planned after exact positive overlap was established.

| Batch/access interval UTC | Actual query | Material result |
|---|---|---|
| after10:02:53/before10:03:52 (bounds from surrounding tool calls; no per-query server timestamp) | `"k203" "pedal" "area"` | RGK published Table 3; also irrelevant commercial pedal results |
| same batch | `"Center-Pedal Area Products" elliptic billiards` | EulerSolve exact centered title/landing page |
| same batch | `"AMR-050-0012" proof` | Exact centered landing page and paper listing |
| after10:03:56/before10:04:07 | `"elliptic billiard" "pedal" "area product" center proof` | Related focal pedal-antipedal page and older inversive work; different observables |
| same batch | `"Poncelet" "center-pedal" area invariant` | RGK and centered-preprint leads; no additional exact proof object identified |
| same batch | `"k203,b" proof` | RGK row; irrelevant identifier collisions; identifiers alone perform poorly |
| after10:04:18/before10:04:48 | `"elliptic billiards" "signed" "center" "pedal" invariant proof` | Author's geometry/media list and adjacent invariants; no further exact object established |
| same batch | `"center-pedal" "Jacobi" proof` | Centered source lead; generic pedal-curve references |
| same batch | `"origin-pedal" elliptic area proof` | Generic/irrelevant origin-pedal and inversive-triangle results; no further exact object established |

The above intervals are reconstructed from surrounding tool-call times, not timestamped search-index logs. They must not be represented as an exact server history. Precise HTTP access times for fetched primary bytes are in PRIMARY_RECEIPTS.json. The first batch's recorded rough clock in the initial log was rounded; the original PDF/API reads began at10:03:52 UTC.

Material primary URLs opened through the web tool, all on2026-10-16 between10:03 and10:05 UTC:

- https://eulersolve.org/papers/amr-050-0012/ — landing page read; manuscript and online date both1 October2026, version1.0, DOI23085904, scope and unrefereed/AI-assisted caveats. Landing dates are not clock-time publication proof.
- https://eulersolve.org/papers/amr-050-0012/paper.pdf?v=8ba41a5466bc — this audit's web open returned Internal Error. The original Zenodo API PDF fetch succeeded and was read in full instead; do not describe the failed website open as byte verification.
- https://arxiv.org/abs/2004.12497 — all11 version-history entries read; v1 andv11 date evidence recorded; current latest version isv11.
- https://arxiv.org/pdf/2004.12497v1 — original primary PDF read, pages1–4; direct in-memory extraction separately authenticated bytes.
- https://arxiv.org/abs/2004.05404 — original arXiv history read.
- https://arxiv.org/abs/2105.03624 — v1/v2 history read.
- https://arxiv.org/abs/2001.02934 and https://arxiv.org/pdf/2001.02934 — original record and relevant primary theorem/method pages read; PDF isv2 as stamped onp1.

The centered primary PDF's bibliography led directly to RGK, Stachel and Chavez-Caliz; the original PR204 credits AST. The later arbitrary-point PDF was a known positive adjacent lead, not a result inferred from snippets. No outreach, comments, e-mail, PR writes, publication actions, UI or private-account service mutation occurred. No exhaustive review of inaccessible, deleted, private, historical non-English or unstated-corollary literature is claimed.

# Nilpotent twist restrictions: audited partial results (30000879)

**Status: PARTIAL. The exact original conjecture remains unresolved by this work.**

This is an unrefereed AI-assisted authored mathematical exposition with an independent internal AI mathematical, source, and computational audit. “Accepted” means the partial scope accepted by that internal audit. It does not mean external human peer review, journal acceptance of these authored documents, or formal proof-assistant certification. No novelty or comprehensive current open-status certification is claimed.

## Exact question and remaining range

Aljadeff's Problem 3 in Oberwolfach Report 55/2007 asks: for a torsion-free nilpotent group G with finite integral cohomological dimension n and a class α in H²(G,C×), is there a subgroup H with α restricted to H equal to zero and gldim(CH) = gldim(C^αG) = r? Finite generation is not a hypothesis. Restriction means vanishing of the cohomology class; global dimension is consistently left global dimension in this exposition.

The source reports the r = n case as affirmative. Its unnamed proof was not audited or imported as a proof dependency. The elementary r = 0 and r = 1 boundaries are addressed. The outstanding range after crediting that reported prior result remains **2 ≤ r < n**.

## Accepted partial results

- The twisted subgroup algebra is free on both sides. Its bimodule splitting gives subgroup global-dimension monotonicity. The twisted diagonal tensor action proves r ≤ n for arbitrary modules, without finite generation.
- Finite integral cohomological dimension makes a torsion-free nilpotent group countable. If d is the supremum of the twisted global dimensions over finitely generated subgroups, the countable telescope gives d ≤ r ≤ d + 1. When r = d + 1, no finitely generated subgroup can witness the desired conclusion.
- For G = Q and the trivial twist, d = 1 while gldim(CQ) = cd_Z(Q) = 2. This is an obstruction to a finitely generated reduction, **not a counterexample**: H = Q is a witness.
- Every twist of a group of nilpotency class at most c ≥ 1 vanishes on the lower central subgroup γ_m(G) for m = ceiling((c + 2)/2), without torsion-freeness or finite generation. Explicit finitely generated torsion-free examples prove this universal cutoff sharp for every positive class. They do not compute their twisted global dimensions or refute the original conjecture.
- A class-two example shows that the splitting subgroup cannot silently be replaced by its isolator. Equality of the lower central subgroup's ordinary global dimension with r remains a sufficient condition, not a universal conclusion.

The complete proofs are in `RESEARCH_NOTE.md`; the complete substantive audit is in `MATHEMATICAL_AUDIT.md`. The countable bound is attributed to Osofsky (1968), and an independent telescope proof establishes the exact left-module form used here. No uninspected Berstein proof, quantum-torus dimension theorem, or nilpotent Hirsch-length formula is imported.

## Exact terminology clarification and reviewed versions

The supplied `CLARIFICATION.patch` was applied exactly to an isolated copy of the accepted note. It changes only “left” to “right” for the cosets H\G and “right” to “left” for G/H. The two module decompositions, all hypotheses, every theorem, and every proof inference are unchanged.

- Original reviewed note: 19,481 bytes; SHA-256 `734a12ebaa684e20feaba65d7e31db4dbb8892d58ffd02c2fc5b0a7315ab0807`
- Distributed clarified note: 19,481 bytes; SHA-256 `7fca262d2764d203a7a27793b218b4f98d3f5ab04e0350f78b928e84705735fa`
- Exact authored clarification patch: 1,271 bytes; SHA-256 `948c433fad20c296c975208d9319aff5ef9feba004c032e8b98fae0154b8576b`

`ACCEPTANCE.md`, `REVIEWED_FILES.json`, `MATHEMATICAL_AUDIT.md`, and `VALIDATION_REPORT.md` are retained verbatim as historical review records. Their references to the reviewed note identify the original bytes; the distributed note includes their accepted terminology-only patch. Both source-metadata files are also retained verbatim. Neither sealed original package was changed.

## Source and verification boundaries

The recorded research and audit are dated 10 October 2026. During that audit, both complete publisher PDFs were independently retrieved and matched the candidate's recorded hashes and byte counts. The original problem page and Osofsky's decisive pages were freshly rendered and visually inspected. Exact inspection scopes, public source titles and URLs, PDF sizes and hashes, retrieval history, and limitations are retained in `SOURCE_METADATA.json` and `SOURCE_VERIFICATION.json`.

`VALIDATION_REPORT.md` preserves the exact scope of the independent arithmetic diagnostics, normal Python / -O / -OO runs, and deliberate adverse controls. Finite tests corroborate formulas and detect particular errors; they do not prove the universal statements mechanically. The proofs and substantive audit support the accepted mathematical claims.

Edition preparation rechecked the unchanged 23-member candidate inventory and 42-member audit inventory in normal Python, -O, and -OO. It also reran the audit's 48 integrity-control runs, including one baseline and fifteen adverse cases in each mode, and verified the externally pinned audit-validation receipts. It did not rerun the mathematical diagnostics, retrieve or inspect scholarly sources, conduct a new literature search, or attempt a new proof.

Candidate inventory SHA-256: `efd1d85b6442fe702233a3ca5ba01bcb5c0cc84a2f2744de392b2474dd3a7a9f`. Audit inventory SHA-256: `1f0afb621b52799b2abefad0335574289ccfa7ee56dc2925ff17b4e65fc85f93`. Audit-validation receipt pin: `e19508689b5bfcb92187a7b359f31ffe5215c62ad155c976f7af3d748262af87`. These hashes establish recorded byte identity, not mathematical truth or novelty.

## Public contents

This edition contains ten files: the clarified complete research note, its exact authored correction patch, the complete mathematical audit, acceptance and reviewed-version records, the complete validation report, two public source-metadata records, this explanatory README, and `MANIFEST.json`.

Only authored mathematical prose, audit, acceptance, an authored correction patch, and public source/verification metadata are included. Copied scholarly sources, datasets, executable code, computational certificates, private sources, private personal data, and private coordination material are excluded. The edition documents computational checks but is not an executable reproduction package. The manifest lists all ten files and hashes the other nine; its own digest is supplied separately to avoid self-reference.

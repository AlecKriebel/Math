# Geodesic cycles: full written audit of a prior counterexample

Record 3169 / OPG-500. Prepared 2026-10-11 UTC.

This is an AI-assisted, unrefereed internal AI audit of a prior public candidate. It is not human peer review or formal proof-assistant certification. The source construction and the C09/C10 arguments are credited to vibemathing at commit a41fe59b4535851ea55f6e868e938b9aaf81e924. No new discovery, novelty or priority is claimed. This prose edition is not a computational reproduction package.

The eight-vertex graph consists of a K4 core and four independent apices, each adjacent to all but a different core vertex. For every strictly positive real edge-length assignment, including all shortest-path ties, it has a nonperipheral geodesic cycle. The universal affirmative question is therefore answered negatively at the locally accepted written-mathematics level. No mathematical proof patch was required.

## Reading guide

- PROOF.md: complete graph and connectivity/peripheral classification; four metric lemmas; tight-rank contradiction; constructive extraction; C09 perturbation proof and its uniqueness counterexample; finite vertex-pair/all-points equivalence; formalization limits.
- AUDIT.md: the other parts of the same audit: verdict, exact source inspection, historical finite-check coverage, negative controls and acceptance boundary.
- ACCEPTANCE.md and ACCEPTANCE.json: precise accepted result and distribution scope.
- SOURCES.json: public citations, identities and source-inspection history, including the historical intake/current-audit distinction.
- VERIFICATION.json: aggregate historical checks and receipt hashes; this does not distribute their contents.
- MANIFEST.json: exact eight-file membership and hashes of the other seven files.

The source construction and universal arguments are credited to [vibemathing's pinned repository](https://github.com/vibemathing/problem-opg-500-geodesic-cycles/tree/a41fe59b4535851ea55f6e868e938b9aaf81e924), especially C10's tight-rank argument and C09's perturbation route. That source still stated candidate_only and best_verified_result: none at the inspected commit. Our completed local written audit does not change those source-author declarations.

The original question is [Geodesic cycles and Tutte's theorem](https://www.openproblemgarden.org/op/geodesic_cycles_and_tuttes_theorem). The finite geodetic-cycle-space context is Georgakopoulos and Sprüssel, [Geodetic topological cycles in locally finite graphs](https://arxiv.org/abs/0911.3999), arXiv:0911.3999v1, §3.1 and Problem 3. No infinite-graph extension is asserted.

PROOF.md and AUDIT.md partition one authored audit; they do not create two independent reviewers. The entire mathematical argument is preserved. Necessary small graph data and the finite tie example are proof content. Raw cycle/mask/certificate arrays, executable code, copied source prose, PDFs, images, full receipts, dataset contents and private coordination material are omitted. Historical checks were authenticated during preparation; no source-author code or Lean was executed and no mathematical computation was rerun for this edition.

Only these eight files are proposed for addition. QUEUE.md and unrelated repository files remain unchanged. This draft edition requests no merge, release, DOI creation or outreach.

# Source and identity gate

Checked 2026-10-05 UTC. `sources.json` binds downloaded scholarly versions by
SHA-256 and byte count. Source files are excluded from the author packet.

## Governing target

The initial request URL was https://www.unsolvedmath.com/problems/2870 .
The web retrieval tool could not access it; a direct HTTP request returned 403.
No contents of that page are claimed read. The live repository queue identifies
2870 as KP-3.72 / Kirby Problem 3.72. The modern K3 source supplies the full
mathematics: section 3.8 p.181 defines smooth homology cobordism, and p.183
contains the two-part rational-kernel question. The p.183 page was also visually
inspected. These pages govern this investigation.

A search also found the **1997** Kirby No.3.72 on convergence groups, explicitly
answered in Bowditch's *A topological characterisation of hyperbolic groups*.
Its hypotheses concern a group action on a compactum, so it is not this target.
No theorem or status was transferred across the numbering collision.

## Dataset and repository checks

The public manifest declares dataset `ulamai/UnsolvedMath`, revision
37e53eabe540fb458758e198be61634bd02ee008, 15,458 records. Its published metadata:
- problems.json: 68,931,837 bytes; SHA-256 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json: 80,334,822 bytes; SHA-256 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b

These are manifest values, **not independent rehashes of downloaded corpora**.
The full corpus, selected imported record and prior AI report were not read.
No byte-comparison claim against their contents is made.

Live repository reads checked the queue, state, related-target groups and
attempt directory. The queue row is rank 692, queued, 0/5; its queue Git blob
is dce961ea85917a765b29405f55dec6347d326660. The numeric ID is absent from the
state and related-group records. The main attempt directory lookup returned
404. Searches for PRs, branches and commits matching 2870 or exact 3.72 found
none; a broader homology/kernel search found the distinct 2869 question in
PR #72. This is a bounded duplicate check, not an exhaustive search of every
historical unmerged blob. Main at a checked checkpoint was
2669042ac964d5710972af552df141f7934588af.

## What was actually inspected

- K3: relevant section definition, exact problem, remarks and references; one
  target page visually. Not the entire 436-page book.
- Akbulut--Larson: introduction, Theorem 1, Lemma 2 and its proof, construction
  description. The full handle-slide diagrams were not independently replayed.
- Savk: introduction, Theorem 1.1, Lemma 2.1, beginning of construction proof.
  Not a verification of all diagrams or all Floer computations.
- Simone: Lemma 1.1 and its proof, Theorem 1.2, Remark 1.4. Not every plumbing
  or symplectic statement in the article.
- DHST: Theorem 1.1, its proof and Remark 1.3; the algebraic homomorphism
  definitions in the introduction. The 50-page Floer construction was not
  reconstructed from first principles.
- Ozsvath--Szabo: Theorem 1.2, Proposition 9.9 and its proof, including the
  extending Spin^c hypothesis; p.67 visually. Foundational Floer maps are credited.
- NST: Corollary 1.4, Corollary 5.6 and its proof, Theorem 5.15 and adjacent
  context, with orientation signs visually checked. Published PDF, pp.4702,
  4741,4745. The foundational moduli-space theory is not formally reverified.
- Lee--Savk: version-2 introduction, Theorems 2.5,2.14,2.15,3.1, Theorem 3.3
  and its proof, including R(B_n)=1; p.11 visually. The result's kernel and
  rational independence conclusion were also checked on the publisher page.
- Alfieri--Cavallo--Matkovic: preprint introduction and Lemma 1.2/proof;
  no general smooth-ball prohibition was inferred from its symplectic results.

## Status and source limits

Current-source searches included the exact rational kernel, infinite rank,
Brieskorn rational balls, and 2025/2026 updates. The inspected sources provide
no full resolution of modern K3 3.72. That is a bounded research finding,
not a certificate that no result exists anywhere. The 2026 local-equivalence
and symplectic results have different conclusions, explicitly separated in
the authored proof. No uploaded source contents, corpus or source screenshot
is needed to replay the public exact controls.

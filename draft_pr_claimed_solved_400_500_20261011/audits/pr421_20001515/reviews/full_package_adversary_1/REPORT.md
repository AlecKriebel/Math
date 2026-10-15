# Full preprint and supporting-package adversarial audit 1

Completed 2026-10-12 UTC. PR421 / problem 20001515 only. Fresh reviewer with no role in the preceding construction, mathematical review, priority review, drafting, or repair work.

**PASS for this first complete-package review. Required findings: 0. Optional findings: 0.** The exact mathematical claim, all six PDF pages, standalone source archive, verification archive, metadata, and global candidate map survived the adversarial checks below. This verdict does not complete the separately required new second review, publish a record, or authorize a claim of historical firstness.

## Candidate and independence

The candidate manifest is `PREPRINT_PACKAGE_CANDIDATE.json`, SHA-256 `0a43f04fde4e6335e7ee852357429310e013dd62d2f9a3da6b81cacb50b0cd41`. All 53 mapped candidate files matched its pins initially and at final readback. The controlling original source head is `d5bf8b5a25cabb177433338fae60af52ebfecf1c`, selected status `claimed_solved`, original author budget `1/5`.

The exact hypothesis was sealed in `CRITERIA_AND_CANDIDATE_SEAL.json` before conclusions or peer reports. I independently reconstructed the proof and computed actual incidence data without importing an author program. `INDEPENDENT_PROOF_SEAL.json` preserves that reconstruction and the initial mathematical conclusion before reading the packet's historical audit or the controlling math/priority gates. The later comparison is explicitly recorded in `GLOBAL_COMPATIBILITY_AND_GATE_COMPARISON.json`; the gates were not used as premises of the independent proof.

The immutable candidate artifacts include:

| Artifact | SHA-256 |
|---|---|
| Paper source | `6c339c55aef95458e633ba2dc3136b26e4abacf55acca08e170b992783785390` |
| Canonical PDF | `3dfdfca7c0b9d41c54ed03dc9500afd8d8013fef2ebd589b2806712f84781841` |
| Source ZIP | `a244ddbbbb0f7ca6d9ca073d21589bef1e9c0a98a404daaca195ee9fc87f6935` |
| Verification ZIP | `8ff6e88f6d4a539680667b22931e080365dfd905dd64f795f408e23cc7bb8f01` |

No original proof-search turn was allocated or used. All mutations were owned disposable copies. No Git, index, branch, remote, release, deposit, tracker, or external-person communication action occurred.

## Independent mathematical reconstruction and falsification

The conclusion is for the full exact group

`G=<a,b,c,t | tat^-1=a, tbt^-1=ab, tct^-1=bcb>`.

The final `b` is positive. Both compositions of the displayed inverse free-group automorphism reduce to the identity. The independent reconstruction retained the characteristic Q-square cycles `(B,A,C,D)` and `(A,B,A,C)`. Its two A-corners in the second square contribute distinct edges `{d+,q+}` and `{p-,e-}`; the first square supplies `{p-,q+}`. They are not omitted, merged, or treated as one corner.

The complete signed Q links are paths with vertex counts `(4,3,3,2)` and edge counts `(3,2,2,1)`. Both endpoint maps are injective on germs and edges and have full induced images in the actual base link. The involution is geometric on cells: the uniquely determined square-corner permutations are `[0,3,2,1]` and `[1,0,3,2]`. They agree with `x<->y,b->b^-1` on faces and both square to the identity. The second permutation is accurately computed in the independently sealed results; the initial reviewer prose transcribed it incorrectly. `RECONSTRUCTION_PROSE_ERRATUM.md` corrects that reviewer-only transcription while preserving the original seal. It is not a candidate defect.

From the actual eight square boundaries, the independent computation obtained 32 distinct link-edge occurrences. From all actual corners of the two product cubes, at both interval ends, it obtained 16 distinct triangles. It checked these independently against the cone reconstruction, rather than assuming a clique count realizes cube incidences. The repeated `z_A` positions in the second cube are compatible product faces, and the two affected triangles have different base edges. There are no link loops, parallel edges, or repeated simplices. The link has `(14,32,16)`, every three-clique is an actual triangle, and no four-clique exists. Every attaching map comes from the genuine product and the two compatible square isometries. The quotient counts are `(1,7,8,2)` and Euler characteristic zero.

I checked the reverse group implication. Eliminating `z_B,z_C,z_D` from the p,q,s product squares gives `z_B=xzY`, `z_C=Yzx`, `z_D=YxzYx`. The r relation is redundant by commutation. The d and e relations reduce respectively to `z^-1(bx)z=By` and `z^-1(yb)z=xB`, which agree by `yb=bx` and `xB=By`. Every elimination is reversible. The inverse basis substitutions compose freely in both directions. The remaining conjugacy relation is successively equivalent to `(zx)(Bx)(zx)^-1=bx`, `c^-1(b^-1t)c=bt`, and `tct^-1=bcb`. Thus the construction gives an isomorphism, not merely a homomorphism into G, a quotient, a subgroup, a monodromy power, or the workshop's `aba,bcb` formula.

The quotient uses the stated general cube-complex convention. Fresh primary inspection of [Leary v3](https://arxiv.org/abs/1009.1540v3) verifies C.9 at printed page 33 for arbitrary links, including the CAT(0) universal-cover conclusion; C.4 at page 31 makes that cover strict cubical; C.11 at page 33 permits second subdivision of the quotient. B.8 is not substituted for the general quotient statement. Finite links, bounded dimension, and unit cube shapes ensure completeness and local compactness of the natural geodesic cover metric, hence properness. The deck orbit of a point is a closed discrete fiber; proper balls meet it finitely. If a compact set meets its translate, the corresponding deck orbit point lies in a bounded ball, proving proper action. The finite quotient gives cocompactness. Deck transformations act freely and cubically, so all action claims apply to actual G.

The optional ribbon and lifted-involution claims retained in the frozen supporting proof also check: with `g=bx`, vertices `A_i=g^i`, `B_i=A_iX`, `C_i=A_iy`, `D_i=A_iXy` give the first square; the other follows `A_i,B_(i+1),A_(i+1),C_i`. This uses `yb=bx`. For the identity-fixing lift of lambda, `f=B lambda` satisfies `f^2=1` and `f(Bx)f^-1=bx`. Neither optional claim is needed to close the main proof.

## Older-tools route and exact citations

All six cited exact primary arXiv versions were freshly downloaded into the assigned private directory. The application was checked before reading prior route conclusions.

The HNN base is genuinely Z² by normal form. For `g=bx`, the edges from `g^nA0` to `g^(n+1)A0` form the actual monotone-height axis. The adjacent stabilizers at A0 are `<y>` and `g^-1<y>g=<x>`, with trivial intersection in Z². Thus the actual length-two axis segment has trivial pointwise stabilizer. [Minasyan–Osin corrected v6](https://arxiv.org/abs/1310.6289v6), Corollary 4.3, applies to this g and gives WPD. No unsupported finite-extension inference is present.

[DGO v5](https://arxiv.org/abs/1111.7048v5), Theorem 6.8 for a single element and Corollary 2.9, yield a virtually cyclic hyperbolically embedded E(g) containing g. Its infinite order follows from b-exponent one. [Sisto v1](https://arxiv.org/abs/1310.7753v1), Theorem 1, gives Morse behavior and the needed quasiconvexity of C. The one-vertex base identifies the combinatorial edge metric exactly with the `{x,y,b}` word metric. The lifted bx circle contains C and lies within one edge of it; endpoint extensions turn geodesics between its vertices into uniform quasi-geodesics with endpoints in C. This supplies edge quasiconvexity without assuming CAT(0)-metric quasiconvexity implies it.

[BKL v1](https://arxiv.org/abs/2011.05374v1), Theorems 1.1 and 5.1, apply in that precise maximal-tree generating-set metric and give a finite local-isometry completion whose image is exactly C. The factorization preserves the generator bx, not a power. Postcomposition by the established geometric lambda supplies the other end map on the same domain, with image By. The direct full-link cone argument supplies finite NPC gluing and van Kampen identifies the same HNN group G. [Hagen–Wise v3](https://arxiv.org/abs/1605.07879v3), Remark 3.7, accurately credits this local-isometry gluing mechanism; its Corollary 7.2 states free action and is not incorrectly promoted to a geometric action. The BKL [publisher record](https://doi.org/10.1017/S0305004121000645) confirms volume 173 (2022), pages 227–238, and the DOI.

Fresh ordinary HTTP recovery and both archived AIM recoveries return the pinned 25,734 identical bytes and confirm the displayed and embedded exact question, Rylee Lyman attribution, record ID, revision, and geometric cube-action request. No TLS warning was bypassed. The workshop primary report specifies the different `aba,bcb` formula and a nearby three-dimensional candidate. The empty AIM status field is not interpreted as an openness certificate.

The bounded priority wording survives: no firstness, absolute novelty, minimal dimension/cell count, virtual specialness, or universal current openness claim is asserted. The presently assembled deduction from older tools is explicitly acknowledged and does not automatically date historical recognition of this exact application. This audit verifies the deduction and the bounded wording; it is not a new exhaustive priority search.

## Complete package, reproduction, and integrity

Both ZIPs have exact positive inventories, safe canonical relative names, no duplicate entries, and only regular-file modes. The source ZIP contains four original UTF-8 files; the verification ZIP contains the documented 24 files. Every archive member was decoded and inspected or structurally checked. No credential marker, foreign primary-source body, raw catalog, private fixture, bytecode, or environment payload is included. Foreign papers and fresh AIM HTML remain private. Independently rebuilding both archives with their declared deterministic entry settings reproduced their bytes exactly.

The packet remains exactly 13 files. Comparison with the pinned source snapshot shows that only the three accepted script paths differ; all ten other files, including proof and saved baselines, are byte-identical. Reversing each `if not ...: raise AssertionError(...)` replacement reproduces the original complete AST exactly: 34 author, 24 geometry, and 4 algebra gates, totaling 62. No current bare assertion remains. This checks preservation independently of the prior repair report.

The flat archives were extracted into clean owned paths containing spaces. Both documented full driver modes passed from an outside working directory. Per full driver run: six clean script launches, three integrity-tampering rejections, seven mathematical/proof corruptions in both modes, and six additional clean launches through the relocated optimized complete driver. The own rerunnable audit script also independently reran both full drivers with isolated launches.

All saved result files are deleted before every launch. Geometry and algebra must newly generate their complete result files, matching full JSON and expected bytes; the geometry stdout projection cannot stand in for the full result. The author program's stdout must match its baseline and it must not unexpectedly write outputs. Negative launches have nonzero status, empty stdout, the expected validation exception, and no success artifacts. The seven mutations fail substantive closure, incidence, involution, triangle, face-sign, inverse-automorphism, or proof-pin checks; syntax/import failures are not counted. All three tamper cases fail SHA checking.

An additional 14 owned tests, in both modes, reject an extra file, extra empty directory, missing baseline, symlinked proof, duplicate JSON key, coordinated rehashing of a changed proof, and coordinated rehashing of saved success data. The latter two still fail the independent hard packet pins. These outcomes are preserved in `INDEPENDENT_PACKAGE_CONTROLS.json`. Integrity records are unsigned and the documented separately trusted digest boundary remains accurate.

The preparation execution evidence is accurately labeled historical. Its baseline and corruption records match the new fresh runs, and its tested driver hash matches the current code. The relocation semantic fields also match; only its JSON checksum changes because that JSON carries the historical versus final manifest/whitelist digests. No self-hash cycle or stale evidence is promoted into a current run.

The global update manifest exactly maps all 53 candidate records, with unique remote destinations confined to this case. The global author packet is the same exact 13 current files plus the dated publication addendum. That addendum explicitly supersedes historical pending/provisional/portability-only prose without changing the pinned proof, acknowledges unavailable earlier checker bytes, gives corrected general cube citations, and keeps the prior-tool deduction and finite-evidence ceiling explicit.

## PDF, source, and metadata

I rendered and inspected every one of the six canonical PDF pages at 125 dpi. Typography, signed link table, equations, page numbering, references, and margins are readable; there is no clipping, overlap, broken glyph, table defect, missing citation marker, or overflow. Compiling the clean standalone source ZIP with cached Tectonic succeeds. It emits an underfull-box warning in a bibliography paragraph, with no visible defect. All six rebuilt page PNGs and extracted text are byte-identical to the canonical rendering/text. PDF byte hashes differ with build metadata, so content/pixel identity was checked explicitly. Private render images and `PDF_VISUAL_AND_REBUILD_QA.json` retain the evidence.

Title, author, independent affiliation, ORCID, date, exact theorem, three deposit files, license, AI disclosure, and unrefereed status agree across the paper, source README, verification README/license, and deposit metadata. The documented Zenodo deposit fields admit the selected preprint type, creator/ORCID, language `eng`, allowed HTML, and related-identifier relations. Zenodo's current license vocabulary confirms `cc-by-4.0`. No actual deposit, DOI reservation, authenticated upload validation, or publishing action was invoked or claimed.

## Findings and remaining process gap

Required mathematical, citation, source, layout, reproducibility, integrity, metadata, and claim-scope repairs: **none**. Optional candidate edits: **none**. Reviewer-only prose correction and the preliminary flat-archive harness adjustment are disclosed in owned notes and do not change this verdict.

The strongest independently verified result is the explicit finite NPC model for exact G and its proper cocompact strict cubical universal-cover action, accompanied by faithful optimization-safe finite checks and consistent publication materials. The remaining gap is procedural: root must accept/apply this reviewed candidate and obtain the separately required NEW second complete-package review. This first-round audit alone does not certify publication readiness. Evidence remains written proof plus exact finite computation and internal AI-assisted review, without external human peer review or proof-assistant certification.

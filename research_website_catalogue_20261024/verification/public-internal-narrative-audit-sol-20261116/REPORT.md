# Bounded public copy audit

Completed 16 November 2026 UTC. Completion: 100% of the assigned read-only copy audit; implementation is separate.

The 107 article URLs in the actual research index and visible list were inspected. Every whole HTML file and the index are bound by path, byte count and SHA-256 in [ARTICLE_INVENTORY.json](/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/public-internal-narrative-audit-sol-20261116/ARTICLE_INVENTORY.json). The final recheck at 11:49:39 UTC found no changes in those 108 files. No website, source, Sheet, Git or deployment action was taken. The parent separately supplied the W revision context; this lane performed no Git commands.

The main opportunity is **11 duplicate native-description blocks**, rather than a site-wide problem with all mentions of verification. Two of the blocks contain clear audit or readiness-round counts and dated internal search narratives. Six blocks can be removed with their full original abstracts and all central claims, hypotheses, limits, prior credit, rights, status and collaboration retained elsewhere. For five others, first preserve a short statement of their distinct scientific support; coefficient normalization is the clearest case because its alternative proof is otherwise mentioned only inside the description.

## Exact candidates

All paths below are actual index-listed files. The numbers are index positions, not spreadsheet rows. Detailed paragraph anchors, classifications and per-category preservation maps are in [CANDIDATES.json](/Users/alec/Documents/Math/research_website_catalogue_20261024/verification/public-internal-narrative-audit-sol-20261116/CANDIDATES.json). The line numbers refer only to the bound snapshot.

| Index | Article | Exact visible block | Bounded recommendation |
|---|---|---|---|
| 96 | [focal-distance-period-criterion](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/focal-distance-period-criterion/index.html) | `details#native-deposit-description` | Retain one short scientific-support sentence elsewhere, then remove the duplicate block. |
| 98 | [binary-relation-liveness](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/binary-relation-liveness/index.html) | `details.deposit-description containing p#native-description` | Remove the duplicate block; the protected content remains elsewhere. |
| 99 | [rational-point-undecidability](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/rational-point-undecidability/index.html) | `section#native-description` | Remove the duplicate block; the protected content remains elsewhere. |
| 100 | [outer-pedal-area-centroid](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/outer-pedal-area-centroid/index.html) | `details.deposit-description containing p#native-description` | Retain one short scientific-support sentence elsewhere, then remove the duplicate block. |
| 101 | [cost-betti-rank-100-amalgam](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/cost-betti-rank-100-amalgam/index.html) | `section#native-description` | Retain one short scientific-support sentence elsewhere, then remove the duplicate block. |
| 102 | [bilinear-ergodic-hilbert-variation](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/bilinear-ergodic-hilbert-variation/index.html) | `section[aria-labelledby=record-description], h2#record-description, p#native-description` | Remove the duplicate block; the protected content remains elsewhere. |
| 103 | [exact-semidefinite-tsp](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/exact-semidefinite-tsp/index.html) | `Unidentified h2 at line 85 and following p#record-description` | Remove the duplicate block; the protected content remains elsewhere. |
| 104 | [takao-self-duality-counterexample](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/takao-self-duality-counterexample/index.html) | `Unidentified h2 at line 90 and following div#record-description` | Remove the duplicate block; the protected content remains elsewhere. |
| 105 | [alternating-antimorphic-fine-wilf](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/alternating-antimorphic-fine-wilf/index.html) | `Unidentified h2 at line 83 and following p#record-description` | Retain one short scientific-support sentence elsewhere, then remove the duplicate block. |
| 106 | [positive-definite-coefficient-normalization](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/positive-definite-coefficient-normalization/index.html) | `Unidentified h2 at line 90 and following div#record-description` | Retain one short scientific-support sentence elsewhere, then remove the duplicate block. |
| 107 | [restricted-boundary-twist-factorizations](/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research/restricted-boundary-twist-factorizations/index.html) | `section[aria-labelledby=description-heading], h2#description-heading` | Remove the duplicate block; the protected content remains elsewhere. |

These structures differ: positions 96, 98 and 100 use expandable `details` elements; 103–106 use an unlabelled h2 followed by a named paragraph or div; 99 and 101 use named sections. A single assumed section selector would miss some and could remove the wrong content. No in-page links to the candidate description IDs were found in the bound article tree.

## Narrow trims with clear operational content

- **Fine–Wilf, line 84, p#record-description:** the sentence beginning “A portable verification supplement preserves” lists “three independent adversarial mathematical audits,” complete saved outputs and a dated priority audit. Replace that sentence with a brief reference to the proof and finite verification controls, or move that brief support reference outside and remove the duplicate block. Preserve the next no-global-novelty/first-discovery limitation.
- **Coefficient normalization, line 91, div#record-description, middle paragraph:** remove the clause “internal adversarial audits including three fresh preprint-readiness rounds and independently rechecked supplementary controls, a dated priority search, and”. Keep its independent proof via positive definite bilinear slices and Cauchy–Schwarz, exact rational verifier evidence, and the limitation that finite checks do not formally verify the universal theorem. Whole-block deletion becomes safe after moving that short support statement elsewhere.
- **Binary relation liveness, line 151, p#native-description:** “due local disk exhaustion” is an internal reason for a failed reproduction. It can be deleted without deleting the material limitation that the upstream Lean build, axiom printing and Comparator validation were not reproduced. Removing the whole duplicate details block also preserves that limitation in #verification.
- **Cost–Betti, line 101, last native-description paragraph:** the inventory of scoped proof audits, source hashes, priority records and reproduction instructions is archive-process detail. Preserve the short scientific-support claim about exact arithmetic and Fox-identity checks outside the block before removing the whole duplicate section.
- **Restricted boundary twists, line 50, #paper:** remove only “Its statements about reviews pending as of that date are part of the deposited edition.” Keep the printed preparation-candidate label, version and edition/creation dates. The description’s source/custody/fault-control inventory is also removable with the duplicate block; the finite-check limitation remains in the status section.

For focal-distance products, outer-pedal centroids and Fine–Wilf, the conservative support-preservation sentences need only identify the existing theta-series diagnostics, symbolic/rational and high-precision orbit controls, or finite controls respectively. They should carry the existing supporting-evidence limits, without repeating output inventories or review histories. These are preservation suggestions, not new verification claims.

## Content that should remain

The audit distinguishes operational narrative from scientific substance. In particular:

- Keep every full original printed abstract, including TSP’s abstract even though it mentions mathematical audits. Removing a separate native description does not authorize rewriting an original abstract.
- Keep theorem assumptions, model conventions and quantified boundaries. Chip-firing “checkpoints” describe mathematical dynamics; Hessian “frozen-coefficient” identities are mathematics. They are not internal workflow logs.
- Keep the JC network article’s exact finite classification and separately implemented replay evidence. This is part of the stated computer-assisted evidence, with its distinction from human review, rather than an audit-count narrative.
- Keep liveness’s optimized-Python/assert caveat and earlier-source build-receipt limitation. They disclose limitations of evidence. They may be expressed more simply, but should not disappear together with procedural prose.
- Keep bounded-priority and source-access/version limitations, including the unavailable journal bodies, intermediate upstream source status, and distinctions between manuscript/declared publication/record creation dates. Those prevent stronger scientific or priority claims.
- Keep scientific dependency and formalization limits, such as TSP’s superpolynomial-only Lean statements and the bilinear variation note’s older-maximal-theorem artifacts. Keep AI use, unrefereed status, author responsibility, licensing splits, third-party rights, and substantive collaboration invitations.
- Links to original ZIPs, checksums, source or supporting records are useful access links. Their existence is not itself a detailed public verification log.

No comparable clear counted or dated internal review narrative was identified in the other 96 indexed articles. Brief AI-review disclosures and generic supporting-material descriptions are not classified as violations merely because they contain “audit,” “review” or “verification.”

## Evidence and limits

Inspection combined whole-file byte capture, a heading/paragraph inventory of all 107 pages, manual reading of the status/materials copy across the set, and full candidate passages with their remaining scientific context. Keyword searches supplied leads, not deletion decisions. The tenet for a whole-block removal was retention in the *remaining HTML*, not just availability of a PDF elsewhere. The helper was read in full before execution and used only standard-library HTML parsing and hashing; its only writes were in this audit folder. No browser, HTTP, literature search, manuscript re-review or scientific program execution was used.

This is a copy audit of the current HTML. It does not reauthenticate the HTML abstracts against archived PDFs or establish that a native description was historically complete. “Preserve the full original abstract” means keep every currently displayed printed-abstract block unchanged; original-file authentication remains with the existing scientific/source packets. Semantic preservation is a contextual editorial judgment documented per page, not a machine proof. No website changes are authorized by this report itself.

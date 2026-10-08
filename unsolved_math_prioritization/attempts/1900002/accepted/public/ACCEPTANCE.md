# Independent acceptance: planar convex integer IKEA

Date: 2026-10-08 UTC. Target: 1900002 / AMR-018-0002, rank 1016.

## Disposition

**ACCEPT the credited prior resolution for planar convex lattice polygons.** Recommended status: **SOLVED-IN-LITERATURE-PLANAR-CONVEX**, **0 proof turns**.

Credit belongs to James Dolan and Oleg Karpenkov, *Lattice angles of lattice polygons*, JTNB 37(3) (2025), 873–896, [DOI 10.5802/jtnb.1345](https://jtnb.centre-mersenne.org/articles/10.5802/jtnb.1345/), Theorem 3.3 and §5.1. The publisher confirms online publication on 27 November 2025. The exact corpus target is the 2017 source's Problem 2, not the adjacent cosine-rule question. Convexity is explicit in the later authors' formulation and theorem; do not broaden this disposition to arbitrary nonconvex or higher-dimensional polygons/polyhedra.

## Corrections and source status

The original frozen v1 is preserved unchanged. Publish only corrected v3 and the explicit public review allowlist.

- RESULT.md now paraphrases the source problem instead of reproducing its sentence.
- SOURCE_METADATA.json preserves the producer's initial unsuccessful correction search as history and records the later independent discovery, retrieval, and inspection of the author's correction file for the 2023 preprint.
- The correction file concerns an endpoint label/coordinate definition, vortex terminology, and the missing continuant K in a supporting winding proposition. Some supporting notation slips persist in the journal. They do not amend the three conditions of the main theorem, whose printed formula already has K correctly. The independent audit supplies the needed crossing-count argument and carefully avoids the unrelated uniqueness claim of Theorem 3.8.
- The correction file is 141 bytes, SHA-256 28a2619377376f85a5c245d86a43985adbe785ba19a2d5b99c5e80e1e6022a7d, reached through the author's university homepage. Its complete contents were inspected privately; no source passages are included in this public review.

SOURCE_STATUS.json contains verified public URLs, byte identities, version mapping, retrieval outcomes, and the qualified current source assessment. The 2025 journal PDF and 2017 source PDF were independently fetched again from their official URLs; both exactly matched the inspected/pinned bytes.

## Mathematical verification

The full necessary-and-sufficient statement, quantifiers, orientation conventions, cyclic indexing, signed continuants, zero handling, winding condition, final curvature, and constructive rational-to-integer polygon step were reviewed. The audit independently derives a scalar matrix-monodromy equivalent of the closing floor quotient and supplies the tangent-half-plane construction omitted as classical in the published sufficiency proof.

The complete published theorem is still an imported primary result. The review is neither formal verification nor a claim to have replaced every geometric sail lemma with an independent proof. In particular, its sail-coordinate and angle-curvature correspondence lemmas remain explicitly credited imports. Finite computations support the review; they are not a universal proof.

Each normal/-O/-OO independent run checks 97,656 signed words, all 2,719 convex hulls on the 4×4 grid, 11,868 cyclic cases, 10,876 affine GL(2,Z) cases, 47,296 curvature candidates, and 157 constructed lattice polygons. It exercises 934 polygons with internal zero prefix continuants, 101 accepted zero-or-positive-curvature witnesses, 146 algebraically closed wrong-winding witnesses, and 39 malformed angle/JSON/polygon inputs. Signed local chord displacements include positive, zero, and negative cases.

The criterion gives an existential integer-witness classification. No curvature bound, terminating rejection procedure from bounded search, unique polygon, cosine-rule solution, or higher-dimensional solution is asserted.

## Reproducibility and read-only checks

- Original v1 producer controls replayed: six positive runs and 51 negative controls over normal/-O/-OO; producer final checks also replayed all three full-private modes and 18 hostile/coherent-repack controls.
- Corrected v3 producer controls replayed: six positive runs and 51 negative controls.
- Corrected v3 independently replayed in all three modes at its frozen location and from a frozen relocated copy, with full corpus files, exact target records, and the two pinned private source PDF identities matching.
- Independent mathematical controls ran from a separately frozen script in all three modes.
- uid 1000 encountered 17 actual append/create permission denials in each release location and two for the independent script directory/file. These are permission-enforced read-only trees, not claimed to be immutable filesystem mounts.
- Fifteen additional independent external-pin/tamper checks were rejected. Frozen original and corrected distributions retained their bytes and modes.
- No remote writes, copied source documents, corpus content, or private coordination material enter the public slice.

## Corrected v3 external anchors

Verify the bootstrap hash against this independently delivered value before execution; a matching PINS.json from the same potentially altered folder is not an independent trust anchor.

- bootstrap.py: 5,070 bytes; SHA-256 3cc10cb75fbaf266f990e3dc99dc46fd36095439fd6a345d9ec672a023df4ea0
- bundle/EXTERNAL_MANIFEST.json: 1,284 bytes; SHA-256 896aa18f3f5d56d440e2150221f08f478de0f7f99613097a211723947a71c0cb
- bundle/AUTHOR.zip: 14,265 bytes; SHA-256 5e68021c3bb1d16eff575beeae468412e17f5a08ab20eca52fac7940a52a5239

The separately delivered public manifest binds the corrected release, authored mathematical audit, independent controls, source-status metadata, and external receipts. A literal local correction patch is intentionally excluded because it repeats the removed source passage.

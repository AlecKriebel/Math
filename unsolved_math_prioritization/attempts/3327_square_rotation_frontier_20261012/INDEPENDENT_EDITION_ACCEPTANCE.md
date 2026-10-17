# Independent acceptance of the second surface-obstruction edition

Date: 13 October 2026. Problem 3327 / OPG-172.

**Verdict: accepted with the stated mathematical and publication scope.** This is an independent review of the complete second prose-and-certificate edition, including its unchanged first-edition companions. It is not human peer review or a resolution of the unrestricted existence problem.

The second edition is the second newly documented substantive investigation. The lifetime investigation count remains unknown. Earlier work is preserved, and no fresh investigation budget or historical reset is asserted.

## 1. Exact accepted edition and unchanged history

The accepted second-edition base manifest is `PUBLIC_MANIFEST.json`, 1,817 bytes, SHA256:

`d080c63f0024c49dcf07a98236352268fc8b63b800bf4b088c12ff18a2744547`.

It identifies eleven authored reports, navigation/verification documents and small certificates. Together with that manifest there are twelve new public files. Each manifest entry was checked against the actual bytes. This independent acceptance is an additional companion; it does not silently alter or extend the already pinned base manifest.

The twelve first-edition companions are preserved byte for byte, including their complete independent acceptance. Their base manifest has SHA256 `cd42ee4cc48296552f957df78f680e326124f257be5e618b4665c0b331d59483`; the first independent acceptance has SHA256 `0023827a56ef7281bb95cd217fed61190905a7cb1b18adc83f72e6b5b3e802ad`. The historical statement that the first investigation proved the co-Heawood Euler genus at least three remains a faithful account of that edition. It is supplemented by the exact genus-four result in the present edition.

All 24 supplied public files, every relative navigation link, the two manifests and the first acceptance were checked. Complete bidirectional text maps cover all 23 files other than the new manifest. Every unchanged interval and every replacement interval was verified, followed by full forward reconstruction and full inverse reconstruction. For the first-edition files all maps are identities.

The complete [structural proof](STRUCTURAL_REPORT.md), [co-Heawood proof](COHEAWOOD_GENUS_REPORT.md), and [mathematical audit](INDEPENDENT_AUDIT.md) were read. Their original accepted reports have respective SHA256 identities:

- Structural report: `9d1007abe23f28e18de0592bd373d086ecd0389eb1e99eeac60c7f524e02595d`.
- Co-Heawood report: `9dca807e9fb444e47f354bb12c8704acfa3116922bc995c387092c55f8ed32d6`.
- Mathematical audit: `1d5ff303d8af041f5ac9c73bec87fab9bd2adde3d39f161a3204ae95529ddc24`.

The public structural report is 16,228 bytes, SHA256 `79217df19fe6d7fe7539880ea428242909c87c00ea4671c71ba73b3020e61793`. Its edits replace operational provenance with working links, identify the companion computational report and remove an operational-only final sentence. The public co-Heawood report is 12,521 bytes, SHA256 `0ade8877d6bbd0aaf863ffd7a0fa1c5a3d9d5da80436042fdd21ab3641403219`. Its edits provide links and finalized cross-reference wording. No mathematical argument, hypothesis, exception or proof step is removed. The independent mathematical audit is byte-identical to its accepted original. The acceptance JSON updates public artifact identities and navigation only; its accepted results, rejected inferences and verification scope remain intact.

## 2. Structural arguments retained and accepted

The exact-cover theorem applies to connected finite simple quartic triangle-free K_(2,3)-free graphs in which each edge belongs to two or three squares. Density forces Euler genus at least two. An Euler-genus-two embedding must be quadrangular, so every two-square edge retains both squares and every three-square edge omits exactly one. Conversely, omitting eligible squares that partition the three-square edges leaves two disk incidences at every edge. K_(2,3)-freeness makes every four-symbol vertex link simple; its degree is two, hence it is C4. The resulting closed connected surface has Euler characteristic zero. The theorem is a global exact-cover equivalence, not an automatic-existence theorem.

The block-reversal proof expands a consecutive proper block into a second vertex disk, twists one auxiliary ribbon and contracts that ribbon. The boundary reconnection changes the number of boundary components by at most one. Thus it gives an Euler-genus increase of at most one. Neither exact increase by one nor automatic nonorientability is asserted. For three ends of each endpoint class, a nonalternating order has two or four runs; in the four-run case a single specified block reversal makes the classes contiguous. The inverse contraction then recovers the original graph without merged edges, using triangle-freeness.

For an h=2 target the contraction has a degree-six vertex and two or three graph triangles. The retained face identity

`f3 - sum_{j>=5} (j-4) fj = 10 - 4k`

forces Euler genus k=2 and either two triangular faces with all others quadrangular, or three triangular faces with one pentagonal face and all others quadrangular. The repeated-walk argument excludes nonsimple face walks of length at most five in this minimum-degree setting. Strict endpoint-class alternation then leaves at least four, or at least two, quadrangular faces through the contracted vertex. Their inverse contractions give distinct 5-cycles through the original edge.

Accordingly every edge of an h=2 target lies in at least two 5-cycles, and an edge in exactly two squares lies in at least four. The extension to ordinary Euler-genus-four hoppers re-establishes the required structural hypotheses from Euler-minor assumptions; it does not substitute Klein-bottle embeddability for Euler genus two. Hence there is no bipartite h=2 target and no bipartite ordinary Euler hopper of Euler genus four.

These deductions retain the accepted first-edition dependencies and their attribution. The finite rotation and square-cover tests corroborate local algebra; they do not prove the unbounded assertions by exhaustion. The ribbon and surface-link arguments carry those assertions.

## 3. New independent replay of every small certificate

A separate implementation for this edition imports neither the author's nor the earlier auditor's checking code. Graphs are reconstructed directly from Fano nonincidence, with the deletion and contraction performed explicitly. Short cycles are generated from vertex subsets and cyclic permutations. Partial links are tested by degree and connected-component structure: a disjoint union of paths is permitted, a proper cycle is forbidden, and the complete cycle on all incident symbols is permitted.

### 3.1 Signed rotations as closed surfaces

The [N4 rotation](COHEAWOOD_N4_CERTIFICATE.json), [deletion torus rotation](COHEAWOOD_DELETE_0_10_TORUS_CERTIFICATE.json), and the unchanged first-edition K4,4 rotation were replayed using three fixed-point-free involutions on flags. Edge-side involutions commute; edge components have four flags; vertex components give exactly the specified cyclic links; the entire flag structure is connected. Face components are reconstructed rather than read from claimed face counts. Their boundary incidence total is 2m. Bipartiteness of the flag adjacency graph determines orientability independently of the supplied sign-potential claim. Complete claimed facial walks, Euler characteristics and orientability data agree.

- Original co-Heawood graph: 14 vertices, 28 edges and 12 faces, with lengths ten times 4, once 6 and once 10. Euler characteristic is −2 and the surface is nonorientable. The supplied negative cycle also has sign product −1.
- Deletion of (0,10): 14 vertices, 27 edges and 13 faces, with lengths twelve times 4 and once 6. Euler characteristic is zero and the surface is orientable. The supplied sign potential satisfies every edge equation.
- Historical K4,4 certificate: 8 vertices, 16 edges and 8 quadrangular faces; Euler characteristic zero and nonorientable surface. This is a Klein-bottle embedding certificate, not a target witness.

### 3.2 Complete square-set orbit certificate

The [orbit certificate](COHEAWOOD_SQUARE_ORBIT_CERTIFICATE.json) has exactly 21 graph squares. All 168 independent ordered basis images of F2^3 were reconstructed; every resulting point-line permutation preserves the complete graph. The 84 forbidden square triples were independently regenerated using partial links.

For an additional completeness check, the new replay enumerates all compatible subsets directly by successively adding a larger-indexed square, without trusting the recorded orbit-extension lists. At every size it expands every listed representative under all 168 automorphisms and checks equality with the independently constructed full set. It also checks minimal representatives, disjoint orbits and every recorded extension statistic.

For sizes zero through eleven, the orbit counts are:

`1, 1, 4, 14, 39, 83, 128, 119, 67, 17, 2, 0`.

The independently recovered full counts are:

`1, 21, 210, 1246, 4725, 11655, 18438, 17874, 9765, 2604, 252, 0`.

Therefore eleven square faces cannot coexist. Bipartiteness gives `56 >= 6F - 2f4`; with `f4 <= 10`, this yields F<=12 and Euler genus at least four. Together with the replayed N4 rotation, it proves E(G)=nu(G)=4.

### 3.3 Deletion completion and contraction exclusion

All 18,564 twelve-square subsets of the deletion's eighteen squares were independently tested. Exactly one survives. Each of its fourteen local unoriented rotations is forced. After normalizing those rotations, the square-face equations force every one of its 27 edge signs consistently, with no free edge-sign variables. The resulting rotations and signs agree exactly with the torus certificate. This proves uniqueness of the normalized Euler-genus-two completion and rules out a Klein-bottle completion. Thus E(G−e)=2 and nu(G−e)=3.

The contraction has thirteen vertices, twenty-seven edges, three triangles and eighteen squares. The partial-link method permits 37 masks at degree four and 1,556 at degree six. All 55,692 selections of two triangles and twelve squares and all 43,758 selections of three triangles and ten squares were tested; none is compatible. These are exactly the two possible Euler-genus-two profiles. No simplicity assumption on the unspecified pentagonal face is required for this exclusion. Consequently `3 <= E(G/e) <= nu(G/e) <= 4`.

The historical co-Heawood square-partition certificate was also independently reconstructed: all 116,280 seven-square subsets fail to partition the 28 edges, and every branch of its eleven-node rejection tree was checked for state, eligible choices, child completeness and reachability. Its weaker historical conclusion remains valid.

## 4. Optimization modes and hostile controls

The new independent replay, the edition validator and its hostile-control suite were executed against the original bytes, a freshly extracted archive copy and a freshly reconstructed content-store copy, each in normal Python, -O and -OO. Each program gives byte-identical results in all three modes. The independent replay uses explicit failures; no essential condition disappears under optimization.

Its sixteen semantic corruptions are rejected directly by semantic checking, before any checksum gate: duplicated edges, invalid signs, wrong geometry, false face counts, false orientability, repeated rotation neighbors, omitted orbit representatives, missing automorphisms, missing forbidden triples and changed squares. All 28 single-vertex switches of the two new rotations preserve the surface. Positive and negative partial-link controls distinguish disconnected paths, full degree-three links and improper short cycles at degree four or six.

The edition's 33 additional controls reject missing/corrupt source objects, unsafe paths, recursive archive references, incomplete or false reversible mappings, unverified new citations, public executable additions, private paths, broken links, changed historical acceptance, false PDF identities, copied source text, false solution/history claims and corrupted certificate data. Semantic controls bypass the byte-manifest checks rather than treating a digest mismatch as evidence of mathematical rejection.

The seven recovered structural, computational, orbit and independent-audit replay programs were additionally executed from both recovered source trees in normal, -O and -OO modes, with matching per-program outputs and no source-byte drift. Their finite scope remains explicit, including the block-reversal regressions rather than an exhaustive proof over all graphs.

## 5. Source identities and publication boundary

The [source identity record](SOURCE_IDENTITIES.json) is byte-identical to the first-edition record. All seven cited PDF objects were checked as actual PDF bytes against their full SHA256 identities and byte counts, and their document titles were checked against the documents themselves. The Ukrainian article's English title is present in its English abstract. The 2014 and two 2020 arXiv version markers match the cited v1 identities. Journal-version claims and bounded inspection coverage remain those of the unchanged [source audit](../3327_surface_obstruction_reductions_20261012/SOURCE_AUDIT.md); this edition claims no fresh online retrieval or complete literature update.

Campbell's triangle argument remains credited to [Finding obstructions within irreducible triangulations](https://dspace.library.uvic.ca/items/cca9ac7d-a34e-4991-99ba-0b0d458e2e62). The unavailable original full text of the 1977 block-genus paper remains described as unavailable, with the applicable formula supported by its inspected later restatement. No expanded source-reading claim is introduced.

The public allowlist contains authored prose, small exact mathematical certificates and public identity/verification metadata. It contains no source PDF, extracted source text, raw search log, executable, private personal data or private coordination material. Automated source-text overlap and private-marker checks supplement the full textual review; they are not presented as a universal privacy theorem. No remote, repository or queue change is part of this review.

## 6. Actual preservation and recovery

The reviewed edition was read-only and matched its external seal before replay. Its archived bytes were independently rehashed and freshly extracted. Its full-file content store was independently rehashed and freshly restored, including its stored external seal. All paths and member types were checked; duplicate archive member names, symlinks and special entries are disallowed. Both recovered full inventories agree exactly with the accepted edition.

The complete unique-source pool contains 228 named source files represented by 135 unique byte objects. Every object digest and length was checked and every named file was materialized from both recovered copies. Both complete source inventories agree. The compact recovery boundary contains file objects rather than nested historical archive files; no recursive archive duplication is used.

This establishes actual recovery and execution of the current edition and its retained sources. It does not retroactively certify any missing earlier recovery event. Post-replay inventory checks found no drift.

## 7. Final scope

Accepted: the exact square-cover equivalence under its hypotheses; the corrected block-reversal Euler bound and strict alternation argument; the stated pentagon requirements; exclusion of bipartite h=2 targets and bipartite ordinary Euler-genus-four hoppers; and the co-Heawood equalities and minor bounds above.

Not established: an unrestricted target, a universal nonexistence theorem, exact contraction genus three or four, nonexistence of higher-genus hoppers, exclusion of all orientably simple Euler-critical graphs, a novelty claim or a complete current-literature status certificate. A failed genus-three search is not used as a lower bound. Both deletion and contraction obligations remain essential.

The unrestricted problem remains unresolved. The complete accepted proof is preserved, historical companions are unchanged, and the precise second-edition publication scope is accepted.

# Independent acceptance audit: KP-3.53 / ID 2851

## Decision and exact target

**ACCEPT UNCHANGED AS A RESTRICTED PARTIAL RESULT.** The original all-genus question remains unresolved. Rank 914; three of five approaches used. No solution, manifold counterexample, novelty, or classification claim is accepted.

The accepted author freeze is exactly 14,473 bytes with SHA-256 `0b194b2b9ee859709b8e668f881aeb2db4939cc3939b2a99a6d79bfebbc02dda`. Its ten distinct members match the supplied external manifest by filename, length, and SHA-256. The internal manifest correctly lists the nine other members. Every original file was read. The original archive is preserved byte-for-byte inside this audit package; its historical pending-audit status is unchanged. This report supplies the later acceptance decision. No mathematical or source correction patch is required.

The accepted mathematical conclusions are:

1. The specified positive unweighted 7-by-7 Fano incidence matrix has determinant and permanent 24, with nonplanar support.
2. Seven alpha and seven beta curves realizing exactly that geometric incidence matrix, with every local intersection positive, have regular-neighborhood genus at least nine. In particular they cannot lie on a genus-seven surface.
3. These conclusions invalidate the proposed purely algebraic planarity shortcut and the particular genus-seven candidate. They do not decide whether every strong L-space is an alternating-link double branched cover.

## Independent finite computation

`independent_check.py` was written separately for this audit. It does not import the author checker or use either of its boundary permutations. It deliberately uses a different crossing order, indexes crossings by incidence pairs, and enumerates tuples of fourteen signs rather than author bit masks.

The permanent is computed by Ryser inclusion-exclusion over the 128 column subsets. The determinant is computed with fraction-free Bareiss elimination. Both return 24. A depth-first perfect-matching search finds 24 matchings; permutation parity is calculated by cycle count. Every matching is positive and every one of the 21 support edges occurs eight times.

For the surface calculation, the program builds an undirected graph of boundary corners. Each crossing disk contributes four corner arcs. An untwisted band joins the corner after its first attaching ray to the corner before the other ray, and joins the two remaining corners. Each corner has degree two. The connected components of this graph are exactly the boundary circles of the ribbon neighborhood. A disjoint-set computation counts these components; no permutation-orbit boundary tracer is used.

All 16,384 choices yield exactly:

- 2,688 cases: one boundary circle, genus 11
- 11,680 cases: three boundary circles, genus 10
- 2,016 cases: five boundary circles, genus 9

The independent program also reverses the local rotation at every crossing and checks the boundary count in each corresponding case, giving 16,384 further agreements. Normal and optimized runs, relocated away from the author directory, reproduce the independently recorded output.

## Completeness of the geometric reduction

**Exactly the stated model.** There are fourteen oriented circles, disjoint within each family, with transverse alpha-beta intersections at the 21 nonzero entries of A. The geometric entries are one, so each incidence is a single crossing. In particular each curve has three distinct labeled crossings. There are no triple points under these assumptions.

**Cyclic orders.** An oriented circle through three specified points has `(3-1)! = 2` cyclic orders after forgetting the arbitrary starting point. The fourteen orders are independent combinatorial choices, giving exactly `2^14`. The enumeration need not quotient by symmetry: repeated isomorphic thickened surfaces cause harmless repeated cases. Every actual embedding supplies one of these cases.

**Local rotations.** For a positive crossing on an oriented surface, the cyclic order of the outgoing rays is alpha+, beta+, alpha-, beta-. This follows from the definition of the local oriented intersection sign. Choosing the opposite convention reverses all local rotations, already independently tested. Arbitrary local negative signs are not included in this claim.

**Edge pairings and bands.** The successor of a crossing on an oriented alpha curve pairs its alpha+ ray with the alpha- ray at that successor, and likewise for beta. Thus the cyclic orders determine all 42 edge pairings. A neighborhood in an oriented surface uses orientation-compatible untwisted bands. There are no additional independent twist bits in the stated orientable model. The local disk rotations and these pairings determine its boundary components.

**Connectedness and Euler characteristic.** Connectedness of the bipartite incidence support implies connectedness of the union of curves. Its 21 crossings are four-valent graph vertices; the 42 curve segments are edges. A regular neighborhood retracts to this graph and has Euler characteristic -21. Consequently `2g + b = 23`. The independently reproduced maximum boundary count is five, giving minimum genus nine.

**Embedding obstruction.** This calculation concerns the neighborhood, without assuming disk complements. If it embedded in a genus-seven surface, a symplectic family of eighteen homology classes supported in its genus-nine handles would retain its intersection matrix in the ambient surface. Their images would be independent, contradicting the ambient first-homology dimension fourteen. Adding complement components or additional complement genus cannot evade this obstruction.

**Heegaard conditions are not needed for the exclusion.** The enumeration permits more configurations than Heegaard cut systems. It does not test whether the seven curves of a family bound a complete set of compressing disks. Excluding the larger class on a genus-seven surface therefore excludes the proposed Heegaard realization, without certifying any higher-genus configuration as a Heegaard diagram.

**Labels and orientations.** Row and column permutations only relabel the fourteen circles and the 21 crossings; conjugating the corner incidence data is a bijection on cases and preserves boundary count. No separate enumeration of every label permutation is required. Simultaneous reversal of curve orientations is represented by cyclic-order reversals. Global surface orientation conventions do not change the genus obstruction. Changing individual local signs or replacing incidence ones with weights changes the model and is not authorized by this result.

## Algebra and logical scope

The geometric intersection counts N give `per(N)` generators, whereas the signed intersection matrix M presents first homology and has determinant of absolute value `|H1|` for a rational homology sphere. The determinant expansion can be refined into individual signed generators. Equality of its absolute value with their number forces a common sign. If one intersection of a given pair participates in a generator, replacing it by another intersection of that same pair forces their local signs to agree. This justifies coherence after the 1-extendible reduction, without incorrectly assuming every strong diagram is initially coherent.

For the chosen matrix, the row inner products are three on the diagonal and one off diagonal, so `AA^T = 2I + J` and the absolute determinant is 24. The independently checked signed matching count fixes its sign. The connected bipartite support has 14 vertices, 21 edges, no bridges, and no 4-cycles. In a planar embedding every face boundary would have length at least six; the resulting bound `e <= 3(v-2)/2 = 18` contradicts 21. This is a support-graph statement. It is not a necessity claim about support planarity for alternating branched covers.

No universal geometric information is recovered from a Pólya matrix alone. Weighted entries introduce additional crossings and cyclic orders; arbitrary signings change local rotations. Stabilizations and other diagrams introduce further geometric data. None are excluded by the finite diagnostic. Weak reducibility likewise does not supply a strong-preserving genus reduction or a branched-cover-compatible reconstruction. The report correctly identifies this missing step rather than declaring an induction complete.

## Sources, inherited material, and search limits

The full three corpus byte streams were independently hashed and parsed. The exact-ID record is unique, the catalog uses the string ID `2851`, rank is 914, and the separate exact-key report is empty. The complete record contains dated literature triage, not an inherited proof or computation. Default sorted-key JSON serialization of the complete record/report pair reproduces SHA-256 `7460a0bc185952a828d87e51464d3bd948cbc0f04c0bc240f02f8e3101009e4d`; the statement hash and catalog links also match. The audit does not substitute an excerpt, normalized statement, or partial download for these checks.

All five local source-PDF lengths, SHA-256 pins, and PDF signatures match. Those checks certify the supplied bytes, not an independent second download. The following targeted intellectual inspection was performed:

- [K3 author preliminary version](https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf), printed page 169: the all-genus question, rational-homology-sphere definition, zero-differential distinction, and cautious Usui assessment agree. The page was visually inspected.
- [Greene–Levine, published 2016 paper](https://msp.org/agt/2016/16-6/agt-v16-n6-p03-p.pdf): definitions, Theorems 1.5 and 1.6, Proposition 3.1, and Propositions 7.7–7.8 were checked. These establish the determinant-at-most-eight and genus-two cases and the stated reductions, not the all-genus classification. Printed page 3204 was visually inspected.
- [Usui, arXiv:1202.3333v1](https://arxiv.org/abs/1202.3333v1): definitions, Proposition 2.1, and Theorem 1.3 were inspected. Its terminology uses zero differential with a separate L-space hypothesis; that hypothesis must not be dropped. Its complete proof was not independently certified.
- [McCuaig–Robertson–Seymour–Thomas extended abstract](https://thomas.math.gatech.edu/PAP/permstoc.pdf): the Fano-incidence identification of the Heawood graph and its place in the Pfaffian structural statement were checked. The present matrix calculation does not depend on accepting the entire structural theorem.
- [Agol, arXiv:2306.10918v1](https://arxiv.org/abs/2306.10918v1): Section 8 explicitly leaves the new examples' strong-L-space status as a question. The current public abstract record lists Pacific Journal of Mathematics 341 (2026), 199–218. The journal text and full manuscript proof were not independently certified in this audit.

The report's claim about the author's prior whole-preprint inspection is historical provenance; this independent audit certifies the targeted inspection stated above. Primary public K3 and Greene–Levine PDF records and the Agol abstract record were also opened during this audit. Bounded current web searches did not establish a later full solution. Fresh repository searches for the ID/problem number/strong-Heegaard terms returned no code, pull-request, or commit hits in their requested result windows. Such negative searches are not exhaustive absence or novelty certificates. The earlier problem-page retrieval failure is retained as history and was not bypassed.

## Replay, failure handling, and artifact safety

`replay.py` first enforces the exact author ZIP hash, external-manifest hash, ten-member allowlist, every member hash/length, internal-manifest consistency, and independent checker/result hashes. Only then does it extract and execute the author checker. Both ordinary and optimized Python reproduce `CHECK_RESULTS.json`, including when launched from an unrelated working directory.

Twenty-five negative fixture cases are exercised in both modes: wrong identifiers, altered/weighted/negative/boolean/float matrix entries, malformed dimensions, wrong determinant, histogram and genus changes, scope overclaim, missing/extra fields, invalid JSON, wrong top-level types, and a missing fixture. All fifty runs must exit 1 with explicit `REJECT:` and no success output. These are rejection tests, not another mathematical proof. Code/content byte drift is handled by cryptographic pins rather than by pretending a few mutation tests certify arbitrary program edits.

Seven artifact-integrity mutations (ZIP byte drift, truncation, extra member, member replacement, external-manifest drift, independent-code drift, and independent-result drift) are also tested in both modes. All fourteen must reject explicitly before mathematical acceptance. The outer replay itself was run under normal and optimized Python with identical results.

The independent mathematical program is then replayed in both modes from a relocated path. Source/corpus pin checking is separately reproducible with `verify_source_pins.py` when the authorized local inputs are supplied. No private input is included in the deliverable.

The final audit package is an explicit allowlist containing the original safe archive, its external metadata, this authored audit, independent code, replay code, and verification results. It excludes source PDFs, extracted source text, corpus records, dataset content, renderings, raw connector responses, and private coordination. The external audit manifest anchors the exact final ZIP and every member. Acceptance applies only to those bytes.

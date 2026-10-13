# Independent acceptance of the fourth prose edition

## Decision and scope

**Accept the fourth prose edition without a required correction.** The complete authored proofs, mathematical reviews, exact certificates and examples, source credit, convention repairs, historical acceptance records, and unresolved boundaries survive the preparation. This is an independent automated review, not human peer review, a literature-novelty determination, or a current-status certificate.

The general triangle-and-segment representation conjecture remains unresolved. This is the fourth confirmed substantive mathematical pass, with lifetime attempt count unknown. Preparing or reviewing this edition does not consume a fifth substantive mathematical pass and does not declare the final pass complete. The historical October 11 proof remains unrecovered.

The mathematical target uses finite covered loopless linear hypergraphs, closed filled triangles and segments, and unrestricted common intersections. The full nerve records every intersecting subfamily; its maximal faces are exactly the stated whole hyperedges. The isolated-singleton/Sperner normalization and the distinction between contacts and unrestricted filled intersections remain necessary. A literal nested-singleton obstruction is not a refutation of the intended loopless conjecture.

## Accepted document set and full preservation

The reviewed [public manifest](../3326_rooted_blocks_20261012/PUBLIC_MANIFEST.json) has SHA-256 `1af542a1adc87190d36501efac9440c05b1da5cac1a01854f1befa5eb79171f8`. It identifies twelve payload files totaling 198,503 bytes and a thirteenth manifest file. The ten second-edition and thirteen third-edition companions remain byte for byte unchanged. This acceptance is an additional review document; it does not silently modify that prepared thirteen-file manifest.

Eight complete source documents were compared with their complete edition counterparts. Eighty character-level replacement spans reconstruct both directions exactly, including all unchanged text between replacements. The full [rooted-block proof](../3326_rooted_blocks_20261012/ROOTED_BLOCK_PROOF.md), complete [finite realizer certificates](../3326_rooted_blocks_20261012/EXACT_CERTIFICATES.json), [source identities](../3326_rooted_blocks_20261012/SOURCE_IDENTITIES.json), and complete [third-edition acceptance](../3326_rooted_blocks_20261012/THIRD_EDITION_REVIEW.md) are unchanged.

Only four source documents contain replacements:

- The final inventory paragraph of [the root-5 dimension proof](../3326_rooted_blocks_20261012/ROOT5_DIMENSION_PROOF.md) describes the prose-only distributed edition and the separately retained computational material.
- [The geometric verification summary](../3326_rooted_blocks_20261012/ROOTED_BLOCK_VERIFICATION_SUMMARY.md) replaces the identity of an omitted diagnostic output with an identity-free statement of byte equality.
- [The realizer verification summary](../3326_rooted_blocks_20261012/REALIZER_VERIFICATION_SUMMARY.md) links the distributed theorem and certificate and replaces executable filenames and run commands with a prose account of the historical checks.
- The opening identification paragraph of [the mathematical review](../3326_rooted_blocks_20261012/INDEPENDENT_PROOF_REVIEW.md) points to the distributed documents and identifies the bounded publication-metadata substitution.

No theorem, proof step, mathematical hypothesis, correction, source attribution, numerical check, substantive review, or unresolved limitation is removed or rewritten by these substitutions. The complete original sources are retained for reconstruction. The complete second-edition acceptance remains in the unchanged third companion. Historical pass counts and then-open boundaries in the frozen companions retain their historical meaning.

## Argument-level mathematical review

### Rooted insertion and full-nerve control

The rooted insertion lemma uses a private open side arc of an old nondegenerate rational triangle. A rational point in that arc has a sufficiently small neighborhood meeting no other old object and no other side of its own triangle. In suitable rational affine coordinates the old triangle agrees there with the lower half-plane. All nonroot objects of the rooted model are bounded, so one sufficiently small positive rational scale places their union in that neighborhood. The transformed root need not be retained: the unchanged old triangle has exactly its effect on every new object.

This proves the full nerve, including mixed subfamilies. Old-only intersections are unchanged. New-only and new-plus-root intersections are those of the rooted model. Any subfamily containing a new object and an old nonroot object is empty. The old and new whole edges share at most the root, preserving linearity and maximality in the stated loopless setting. The construction does not connect a new block to two independently constrained old triangles.

The previous private-boundary lemma applies at an old vertex of degree at least two. Intersections with other objects are grouped by incident hyperedge. These compact groups are nonempty and disjoint: an intersection between distinct groups would create an unintended triple and contradict linearity. If their boundary traces covered the connected triangle boundary, one group would cover the whole boundary. Every object in that group contains a common edge witness. Extending the ray from that witness through any point of the triangle to the boundary shows that the group would cover the entire triangle, contradicting the presence of another nonempty disjoint group. Thus the boundary has a private point, and closedness supplies an open side arc. Each new block vertex has degree at least two, so the lemma supplies an eligible private arc for later insertion. This justifies finite recursive use while preserving all initial triangles.

### Both root types

The five-vertex block has edges 12, 23, 34, 14, 135, and 245. The root-5 model starts from four segments and a lower half-plane. The root-1 model uses three segments, a triangle, and a lower half-plane. Their full degenerate nerves are checked explicitly. Because there are finitely many nonfaces, boundedness and positive separation preserve all empty intersections under sufficiently small thickening. The half-plane is handled by restricting attention to a common bounded neighborhood of the nonroot objects. Rational thin triangles and rational centroid dilation produce nondegenerate objects; the displayed parameter is verified exactly.

The cyclic automorphism on vertices 1, 2, 3, 4 covers every degree-three root. Together with root 5, these are all possible root types. The theorem therefore applies to any allowed one-vertex insertion of the complete source block. It makes no general incidence-dimension-preservation claim.

### Root-1 wedges

The three orders in the rooted-block proof are linear extensions on every block. Their restrictions to each block and the common root are the complete verified local realizer. Opposite block order in the first two extensions reverses every cross-block pair; the third extension supplies the needed root comparisons. These categories exhaust all distinct pairs of incidence elements. The induced standard example S3 supplies dimension at least three. Hence every positive number k of root-1 blocks has incidence dimension exactly three.

Every incidence node has degree at least two, so the whole incidence graph is its 2-core. The root degree is 3k and is wholly cyclic, not contributed by pendant trees. The displayed internally disjoint paths give a K3,3 subdivision in a block, proving nonplanarity. The separated rational triangle construction has disjoint horizontal ranges for different blocks, and its common root triangle agrees with the lower half-plane on every relevant portion of the nonroot triangles. The resulting full nerve is the asserted wedge for every k.

### Exact root-5 threshold

The complete two- and three-block certificates give the upper bound three for one through three blocks by restriction. Each block contains S3, proving equality.

For the lower bound beyond three blocks, the source block cannot have its root before all four other vertices in two of three realizing orders. The missing incidences force the two opposite bipartition classes to be ordered in opposite ways in those two extensions. Reversing the remaining two-element nonincidences in the third extension then forces two distinct vertices each to follow all other nonroot vertices, an impossibility.

In any three-order realizer of a root-5 wedge, every block consequently has a vertex lying after the root in exactly one extension. If two blocks used the same sole-after-root extension, their corresponding root-edge/nonincident-vertex reversals would force an alternating directed cycle in that extension. Different blocks must therefore use different members of a set of only three orders, so there can be at most three blocks.

The four-order construction provides the matching upper bound for every k. The first three extensions realize all within-block nonroot pairs. Opposite block order reverses cross-block pairs. The fourth extension places all nonroot vertices and nonroot edges before the root and all root-incident edges after it, supplying every remaining incomparable root pair without violating any incidence. These cases exhaust all pair types. The dimension is exactly four for every k at least four.

This is an analytic lower bound and a universal constructive upper bound. The historical unsuccessful search at four blocks is not evidence of infeasibility. Dimension four is not geometric nonrepresentability: all root-5 wedges remain triangle-representable by the rooted construction.

### Unchanged dependency chain

The review includes the full convex-reduction, normalized-coordinate, private-boundary, pendant-extension, incidence-core, convention and obstruction proofs in the unchanged companions. The coordinate argument uses exponentially separated rank coordinates, the proved B>d specialization, and the minimum-lift normalization argument to establish the full nerve rather than merely pairwise intersection. A vertex with at most three incident hyperedges receives a convex hull with at most three generating points; compact nonface separation permits rational nondegenerate thickening in the stated finite setting.

The core proof preserves whole original hyperedges. Pruned incidence components have at most one core attachment and can be reconstructed through eligible private arcs. The construction supplies fresh private arcs for the new pendant objects, while the connected-boundary argument supplies the required arcs at selected degree-at-least-two backbone vertices. It does not assume that an arbitrary pre-existing degree-one triangle has a private boundary arc. The previously documented correction to the printed coordinate growth condition and every historical acceptance qualification remain intact. No theorem of either cited source is claimed to fail.

## Exact independent checks

The preparation's exact fixture checks were rerun successfully under normal Python, -O, and -OO at two different hash seeds. They recheck both rooted formulas, all strict witnesses, wedge coordinates, cyclic-core degrees, actual recursive affine grafts, unchanged old triangles, complete finite incidence orders, every supplied witness, exact inventories, source maps, manifests, links, privacy and scope. Their outputs are byte-identical across the six runs.

A separately written rational Fourier–Motzkin elimination procedure supplies an independent geometric cross-check. It checks 1,647 subfamilies of size at most three across the seven complete examples. Planar Helly then determines all 140,857 nonempty subfamilies, including all 131,071 subfamilies of the seventeen-triangle root-5 four-block example. Every computed nerve matches the declared whole-edge family. This count distinguishes direct elimination from the subsequent full-subfamily Helly verification; it is not described as 140,857 separately solved linear systems.

The two rooted models have seventeen nonempty faces each and strict minimum oriented-inequality slacks 1/62500 and 1/125000. The three wedge examples have 33, 33, and 65 faces. The two recursive examples have 33 and 49 faces. Their retained coordinates and whole-edge relationships agree with the displayed formulas.

The independent incidence checker directly compares all 420 ordered pairs for the root-5 two-block certificate and all 930 for the three-block certificate, with exactly 28 and 42 strict incidences. It also checks both displayed uniform-order formulas at k=1,2,3,4,5,10,20,32,64. These finite comparisons supplement the complete pair-type proofs; they do not establish the universal claims by extrapolation.

The independent semantic results are byte-identical under normal Python, -O, and -OO. Exact arithmetic uses rational numbers or integer order positions throughout. No numerical tolerance, optimization solver, or timeout is used as a certificate.

## Fail-closed controls and limitations

Each of the six preparation replays rejects all thirty-eight required negative controls with the intended diagnostic. These distinguish semantic errors from parser, scope, link, privacy, source-preservation and closed-inventory failures. They include incorrect rational geometry, altered strict witnesses, collisions, wrong core degrees, broken realizers, missing pair witnesses, malformed or nonfinite JSON, private material, omitted-artifact identities, executable text, broken or escaping links, missing scope fences, changed companions, altered programs and source maps, extra or missing files, and symbolic links.

The independent checker additionally passes six exact geometric controls, including point and segment feasible sets, an unbounded half-plane, and two infeasible parallel-constraint systems. Twelve independent hostile controls reject incorrect rationals, degenerate triangles, malformed JSON, reversed or missing orders, an outside root witness, a false nerve, a false face count, and an explicitly failed gate. These outcomes and diagnostics agree in all three optimization modes. Gate logic uses explicit exceptions rather than removable assertions.

An initial preparation control-routing correction is retained: the stand-alone privacy test needed the fixed identities of actually distributed files so a modified disposable README would reach its intended link/privacy diagnostic rather than first encountering the original manifest hash. This did not alter public or mathematical content, and the external seal, fixed-content, manifest and inventory checks remained active. During this independent review, the first hostile-control outputs rejected correctly but named different first bad pairs because set traversal was unordered. Sorting the pair traversal made the diagnostics deterministic; final checks were rerun. Neither issue was a mathematical counterexample or a relaxation of an acceptance gate.

Controls operate on disposable copies or in-memory test objects. A mismatch rejected by a cryptographic seal is not counted as an independent mathematical check. Read-only permissions are not immutability, concurrency protection or a remote guarantee. A successful local link and preserved public-host check does not establish fresh remote availability.

## Citation and publication boundary

The base block, its original three-order realizer and its nonplanarity remain credited to de Fraysseix, Ossona de Mendez and Rosenstiehl, [Representation of Planar Hypergraphs by Contacts of Triangles](https://doi.org/10.1007/978-3-540-77537-9_15), printed page 135. The retained complete publisher PDF and extracted page agree with that attribution and with the public source identity: 478,062 bytes and SHA-256 `024cea81886d5c549a475263ba2d11208e35fb6113cd28f29fe05456c19466cb`. The normalized-coordinate dependency remains credited to Ossona de Mendez, [Realization of Posets](https://jgaa.info/index.php/jgaa/article/view/paper48). The earlier source ledger and its actual retrieval/inspection history are unchanged.

The prepared public tree contains exactly the thirteen new files and twenty-three frozen companions. They contain authored mathematical prose, reviews, acceptance and correction prose, small complete mathematical examples, explicit order certificates, permitted public scholarly metadata, and identities of actually distributed files. Programs, raw computational/search outputs, copied source documents or source text, private sources, private personal data and private coordination material are excluded. Public metadata does not advertise omitted operational artifacts. The reviewer has not conducted a fresh literature search or inferred a new current-status result.

## Actual recovery and final boundary

The accepted preparation archive was independently read and safely extracted. Its actual content-addressed chunks were separately read, checked, reassembled into the complete archive bytes and extracted again. Both routes restore every one of the fifty-two preparation files plus the external seal. The nested source snapshots actually restore 478 unique retained source files through three snapshot documents, with complete byte comparisons. The restored preparation was successfully reexecuted in all three optimization modes from both routes.

The complete independent review, its full inputs, exact checks and outputs are retained with actual recoverable bytes and a separately verified archive-and-byte-store round trip. A digest alone is not a backup. The retained input set contains only this review and the relevant accepted preparation and its existing source dependencies; it does not duplicate unrelated historical archives.

Acceptance is limited to the fourth prose edition and its stated results. It authorizes no claim that arbitrary block gluing preserves incidence dimension three, that an arbitrary block has a rooted half-plane model, that two-parent insertion is proved, that dimension four prevents triangle representation, or that unrestricted high-degree indivisible cyclic cores are settled. The general conjecture remains unresolved. No remote publication or queue mutation was performed in this review.

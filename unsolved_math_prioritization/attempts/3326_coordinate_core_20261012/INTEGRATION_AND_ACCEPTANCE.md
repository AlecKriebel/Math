# Integration, acceptance, corrections, and limits

## Accepted results and historical preservation

The [coordinate proof review](COORDINATE_PROOF_REVIEW.md) accepts the explicit normalized dual-edge hull construction for all finite covered hypergraphs, whose full nerve is the downward closure of the edge family. The Sperner condition is needed to identify the listed hyperedges with maximal faces, and is not needed for the downward-closure construction. The [core proof review](CORE_PROOF_REVIEW.md) accepts the private-boundary lemma, rational pendant-edge graft, whole-edge backbone, and resulting sufficient-condition theorem, including its explicitly accepted coordinate-base integration.

The ten files in the [second edition](../3326_convex_reduction_20261012/README.md) are preserved byte for byte. Its complete independent proof review, convention audit, source ledger, exact examples, correction history, and then-open source dependency remain historical evidence. The [third-pass core proof](CYCLIC_CORE_EXTENSION_PROOF.md) is also preserved byte for byte. In particular its concurrent-proof paragraph still says that it did not assume acceptance of the new coordinate deduction. That paragraph is a faithful historical statement; the following separately labeled integration supplies the later deduction without rewriting it.

## Integration deduction: discharge of the credited-base dependency

Let H be a finite covered loopless linear hypergraph of incidence dimension at most three. Assume every vertex-node remaining in the incidence graph 2-core has degree at most three.

The core proof selects a whole-edge backbone K. Its proof establishes that K is covered, has maximum vertex degree at most three, and is obtained by restricting the incidence poset to its selected whole edges and their vertices. The restriction of a three-order incidence realizer is therefore a realizer for K. Whole-edge selection matters: no hyperedge is truncated or replaced by its intersection with a selected vertex set. Loopless linearity makes K Sperner.

Apply the accepted coordinate theorem to that restricted realizer with d=3 and B=4. It gives rational planar hulls whose full nerve is exactly the downward closure of E(K). Each vertex of K belongs to at most three hyperedges, so each hull is a point, segment, or triangle. Apply the [previously accepted compact-nerve stability and inflation proof](../3326_convex_reduction_20261012/CONVEX_REDUCTION_PROOFS.md). It replaces these hulls by nondegenerate rational triangles with the same full nerve, retaining common edge witnesses in their interiors. This is now a complete independently reviewed proof of the degree-three base used in the frozen core argument; it requires no unproved inference from symmetric-difference separation.

Every selected vertex needing an omitted branch has degree at least two in K. The private-boundary lemma therefore supplies a private side-interior arc. The rational graft constructs one pendant edge at a time, with all of its fresh vertices introduced together and with a private exposed tip for each new object. Reading every omitted incidence tree away from its unique selected vertex reconstructs H exactly. The full-nerve checks in the graft proof exclude every unintended old/new or descendant/grandparent intersection. Separate components can be placed in pairwise disjoint rational boxes. The empty hypergraph uses the empty family.

Consequently the core sufficient-condition theorem is established using an explicit accepted coordinate construction and accepted written inflation and graft proofs. The source construction and its published consequence remain credited. This integration is a deduction joining accepted results, not a new fourth substantive mathematical pass.

The same argument directly discharges the prior maximum-vertex-degree-three corollary's omitted convex-consequence deduction. It does not remove any other historical caveat: the singleton/Sperner mismatch, contact-model distinction, fixed-representation limitations, missing October 11 proof, and absence of a novelty or current-open-status determination all remain.

## Source credit and growth-condition correction

Ossona de Mendez, Realization of Posets, JGAA 6(1) (2002), pp. 149–153, supplies rapidly increasing order coordinates followed by radial normalization. The proof here specializes those coordinates to B raised to integer ranks and supplies the direct full-nerve minimum-lift argument. De Fraysseix, Ossona de Mendez and Rosenstiehl, Representation of Planar Hypergraphs by Contacts of Triangles, LNCS 4875 (2008), pp. 125–136, states the convex maximal-intersection consequence on p. 135. [Poset article](https://jgaa.info/index.php/jgaa/article/view/paper48); [triangle chapter](https://doi.org/10.1007/978-3-540-77537-9_15).

Both primary texts were read, and the relevant printed pages were visually inspected in the independent coordinate review. The printed p. 151 condition is weaker than the next estimate uses. B>d supplies the stronger coordinate growth condition actually required. This is a local correction to the inequality used in the argument, not a claim that the source theorem fails. Different hulls require different positive radial lifts of a normalized common point; the proof deliberately compares them by choosing a minimum lift rather than treating the scales as equal.

[COORDINATE_SOURCE_IDENTITIES.json](COORDINATE_SOURCE_IDENTITIES.json) retains public scholarly PDF metadata and full authored source-inspection statements. Identities of undistributed extracted text and rendered screenshots are omitted. The preserved [source ledger](../3326_convex_reduction_20261012/SOURCE_LEDGER.json) retains earlier source retrieval failures and recoveries, inspection limits, and the distinction between downloading and proof inspection. A limited literature search cannot exclude a later or unindexed resolution.

## Complete mathematical and computational review boundary

The coordinate review independently derives the realizer/minimal-nonface bound, reciprocal inequalities, normalized lift, minimum-scale contradiction, exceptional cases, and planar consequence. Its separate rational barycentric method checks 334 nonempty subfamilies across twelve fixtures in ambient dimensions zero through four, with 120 checked primal certificates, 214 checked Farkas certificates, and four additional extremality certificates. These are finite implementation regressions alongside the universal written proof.

The original coordinate author checks cover thirteen fixtures, 1,096 ordered pairs, 95 minimal nonfaces, 201 root certificates, and 501 planar subfamilies checked by two exact methods. The historical author summary originally marked independent final review pending; its status annotation now links to the subsequently completed review while preserving that timing. All other numerical and scope statements remain intact. Result-file hashes of undistributed raw diagnostics are omitted.

The complete core verification summary and independent core review preserve their actual tested scope, proof limitations, and correction history. The reported uniform-family regressions do not replace the all-k pair-type proof. Neither the geometry checks nor the graph-core checks claim that arbitrary pendant attachment preserves incidence dimension three; the displayed family has its own uniform realizer proof.

## Edition checks and recovery

This edition checks its three small complete exact examples separately from historical checker verdicts. It recomputes 312 ordered incidence-poset pairs and 165 nonempty geometric subfamilies, coordinate hulls, all fifteen root-exclusion certificates, nondegeneracy, the seven-object core, and the grandparent nonincidence. The rational triangle test enumerates intersections of independent bounding lines and checks all inequalities. Bounded nonempty polygon intersections have such an extreme point, including a degenerate point, so the finite feasibility test is exact.

The preservation maps reconstruct every complete source document in both directions. Metadata-only substitutions remove undistributed-artifact identifiers or operational wording and repair links; no mathematical argument, source-credit statement, correction, acceptance boundary, or substantive diagnostic is abridged. The core author proof and all second-edition public files undergo no substitutions.

Validation enforces closed exact inventories, strict JSON parsing, scalar types, sorted paths and diagnostics, fixed accepted-input hashes, public scholarly PDF identities, permitted actual distributed-file hashes, local link targets, and a narrow public prose/example allowlist. Semantic fixture, parser, scope, privacy, link, source-preservation, and integrity failures are tested separately. A rejected hash is not mislabeled as a mathematical test. All mutation tests use disposable writable copies; canonical inputs remain unchanged. Explicit exception gates remain active under normal Python, -O, and -OO. No timeout counts as rejection.

Actual full-byte archive extraction and separate content-addressed-store reconstruction reproduce the complete sealed preparation and its exact retained input records, followed by revalidation. A digest is not a backup. Read-only permission bits provide static-snapshot protection, not immutability, race safety, or a remote guarantee. Local link targets and preserved public URL syntax are checked; no new remote-availability claim is inferred.

## Remaining question

The general intended triangle-and-segment problem remains unresolved. In particular the sufficient condition does not address a vertex with four incident edges all surviving in the incidence 2-core. The coordinate construction can produce more than three extreme points; local private-neighborhood grafts cannot join several already constrained core vertices. Neither observation proves impossibility of a coordinated global representation.

This is at least the third confirmed substantive pass, lifetime count unknown, not a final pass. The nested-singleton convention mismatch is not treated as a solution or refutation. No fourth mathematical result, general counterexample, novelty certificate, or present-day status certificate is claimed.

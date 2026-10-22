# One common color on subcubic critical graphs

Row 1751, problem 3200, OPG 388. Authored mathematics and independent audit dated 12 October 2026 UTC. This is the fifth and final substantive research round in the present continuation. Five substantive rounds are confirmed; the total lifetime attempt count is unknown. The general conjecture remains unsolved by this work. No historical novelty is claimed.

## Exact theorem

Let G be a finite simple graph of maximum degree at most three. Suppose G is not properly three-edge-colorable, but G−e is properly three-edge-colorable for every edge e. Assign a list of exactly three colors to every edge. If the total intersection of the lists is nonempty, then G is list-edge-colorable if and only if the assignment is nonconstant.

There is no bound on graph order, total palette, distinct-list count or number of exceptional edges. Isolated vertices are allowed. The complete symbolic proof was independently accepted without correction. It is independent of all finite computational checks and of the preceding bounded-exception results.

## Proof and the matching distinction

For any chosen edge and any ordinary coloring of its deletion, a permissible color class covers all original degree-three vertices. Its complement has maximum degree two and exactly one odd cycle, which contains the deleted edge. Two such critical cycles through incident edges share an edge at their common endpoint. Therefore, if reduced lists differ on those incident edges, at least one critical cycle has nonconstant reduced two-lists. Color its matching with the globally common color and its complement component by component.

The critical-cycle lemma uses a permissible color class of an ordinary edge-deletion coloring. An arbitrary matching covering all degree-three vertices does not acquire the unique-odd-cycle property from coverage alone. Even a permissible matching can fail for a particular list assignment; the proof selects a suitable one using two local cycles. The construction needs supplied ordinary deletion colorings for at most two incident edges and does not claim an efficient algorithm for obtaining them.

## Complete distributed contents

- [THEOREM.md](THEOREM.md): complete byte-identical accepted proof, all four lemmas, constructive reduction, four-palette corollary and source boundaries
- [AUDIT.md](AUDIT.md): full substantive independent mathematical audit, all proof-review steps, finite domains, controls, input-verification and replay conclusions
- [ACCEPTANCE.md](ACCEPTANCE.md): exact accepted scope and excluded conclusions
- [CHECKS.md](CHECKS.md): complete author and independent computational counts, all per-fixture strata, exact choice quantifiers, authored small controls and reproduction limits
- [SOURCES.md](SOURCES.md): bounded source inspection, public citations and search limitations
- MANIFEST.json: byte counts and SHA-256 identities of actual distributed files, excluding the manifest itself

The author validated 2,644,056 assignment runs; the independent auditor validated 18,606 full constructions on 3,384 assignments and separately replayed the full author suite. Their domains overlap and are not disjoint coverage. All counts are supplementary to the symbolic proof. The independent audit's larger-palette assignment sample is deterministic pseudorandom, not exhaustive; all deletion colorings and permissible matching labels on its seven fixtures were exhausted.

## Accepted complementary matching analysis

[METHODS.md](METHODS.md), [AUDIT_METHODS.md](AUDIT_METHODS.md), [METHOD_ACCEPTANCE.md](METHOD_ACCEPTANCE.md) and [METHOD_CHECKS.md](METHOD_CHECKS.md) preserve the accepted complement from this same fifth round. It proves the exact fixed-matching criterion and connectedness of the full critical-cycle family under edge intersection, without claiming pairwise intersection.

An explicit 25-vertex, 37-edge critical graph has a covering matching whose complement is C3+C3+C19; arbitrary covering matchings therefore need not satisfy the critical-cycle lemma. A separate seven-edge example has exactly one common color, a failed matching choice and an explicit successful full coloring using another matching. These are limitations of matching selection, not bad-list counterexamples.

The complementary independent audit re-enumerates 1,692 deletion colorings, 1,908 admissible classes and 30 critical cycles; it tests all 38 covering matchings and all 4,374 matching/list pairs. The last fixture here has 37 edges, whereas the primary suite's last fixture has 13. The domains overlap and must not be added as distinct coverage. All proofs, explicit examples, count strata, choice quantifiers and reproduction limits are retained. Only reversed implication labels are editorially clarified. No unaudited claim is included.

## Final frontier and relation to prior editions

The third edition already proves colorability in every degree when a nonconstant exact-maximum-degree list assignment differs from some maximum-degree palette on at most five edges, with arbitrary exceptional lists and support. The fourth edition proves the subcubic common-two-color case with unrestricted exceptions. The present theorem strengthens that common-intersection condition to one color without imposing an exception bound. Those prior editions remain unchanged; their earlier unresolved-frontier wording is historical.

The general conjecture is still unresolved by this work. Subcubic empty-intersection assignments remain outside this theorem, except for cases already covered by preceding results. For lists drawn from a four-color palette, the theorem covers assignments using two or three distinct triple types; using all four types gives empty intersection and is outside its scope. This does not claim such assignments are uncolorable. Higher-degree common-one-color extensions are not proved here.

Five confirmed substantive rounds complete this continuation. Parallel directions are not counted as separate rounds, and an earlier screen means the lifetime count remains unknown. No sixth research round is initiated or promised.

## Distribution and reproduction boundary

Only authored proof, audit, acceptance, source and verification prose plus the distributed-file manifest are included. Programs, binaries, raw graph/fixture/certificate/coloring collections and run outputs, copied third-party source documents, dataset contents, excluded-input identities and private coordination material are excluded. The computational suites cannot be rerun or their omitted records reconstructed from this prose alone; reproduction requires fresh implementation and fresh input generation. The symbolic proof and explicit authored small examples are complete and inspectable. No computational suite was rerun during edition preparation.

The source inspection is bounded: it does not establish historical novelty or certify the current worldwide status of the broader conjecture. The operational criticality hypotheses are stated explicitly to avoid source convention ambiguities.

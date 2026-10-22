# Five exceptional lists and strict deficit method boundaries

Row 1751, problem 3200, OPG 388. Authored mathematics and independent audits dated 12 October 2026 UTC. This is the accepted second substantive research round in the present continuation. It is a restricted partial result, not a resolution or counterexample to the full conjecture. No novelty claim is made.

## Main results and exact setting

Let G be finite and simple with actual maximum degree Δ. Assume that G is not Δ-edge-colorable and G−e is Δ-edge-colorable for every edge e. Every list has exactly Δ colors. Fix a Δ-element palette A and let X be the edges whose lists differ from A. The assignments under discussion are nonconstant.

For Δ=3, every assignment with five exceptional edges forming a 5-cycle is colorable, with arbitrary exceptional three-element lists. The cycle need not be induced; chords and absent off-cycle boundary edges are covered. The complete proof uses the strict residual-deficit theorem, an equality-Hall classification, a five-boundary-color lemma and an explicit uniform-list extension. Separately, five one-color substitutions on arbitrary subcubic support are colorable whenever the omitted base colors are not all equal; exterior colors may coincide or differ arbitrarily.

The other accepted direction completely classifies failure of the strict residual-deficit certificate on five-edge supports of finite simple graphs of maximum degree at most three, for arbitrary exterior-list sizes one through three. Its finite domain has 20 line-graph support types and 3,635,009 generated first-occurrence-normalized families per support, giving 72,700,180 decisions. The generated normalization is complete but can repeat color-relabeling orbits. There are exactly 65 generated failures and 34 support/color orbits. All failures have matching number two, at most three exterior colors and minimum residual deficit exactly three. Fourteen of the sixteen profile-11222 classes admit a universal incident-pair Hall escape. The other two have line graph K3 disjoint union K2 with the common-list patterns described in the full report. This is a line-graph statement; the original three mutually incident edges may form a star.

The classification concerns failure of a sufficient numerical method. It is never a bad-list counterexample. On an explicit critical subdivided-K4 graph, a chosen deletion coloring cannot be repaired by any global permutation, yet one displayed Kempe change followed by a permutation succeeds with the same exterior set. No general one-switch theorem is claimed.

## Complete authored contents

- FIVE_CYCLE.md: complete five-cycle theorem, arbitrary-support varying-omission theorem, equality and boundary lemmas, explicit criticality proof, sharp method limitations and unrestricted-completion equivalence
- KEMPE_REPAIR.md: complete one-switch repair with explicit edge colors and list checks
- METHOD_CLASSIFICATION.md: complete authored support/normalization arguments and decision-method descriptions, exact finite coverage, Hall lemmas, universal 14-class escape and explicit critical fixture
- AUDIT_FIVE_CYCLE.md and FIVE_CYCLE_ACCEPTANCE.json: complete independent structural audit, finite corroboration and exact acceptance limits
- AUDIT_METHOD_CLASSIFICATION.md and METHOD_CLASSIFICATION_ACCEPTANCE.json: complete independent method-classification audit and aggregate finite acceptance contract
- SOURCES.md: named primary sources, inspected publication identities and bounded literature-search limitations
- MANIFEST.json: closed identities of the actual distributed authored files, excluding the manifest itself

## Dependencies and reproduction boundary

The accepted first round is a separate sibling edition: [first-round README](../3200_critical_list_partials_20261012/README.md), [strict residual-deficit proof](../3200_critical_list_partials_20261012/NEAR_CONSTANT.md), and [four-exception theorem](../3200_critical_list_partials_20261012/FOUR_EXCEPTIONS.md). No file in that edition is changed. The strict-deficit proof is also reproduced here. The four-exception theorem supplies the at-most-five cycle-supported extension when fewer than five exceptional edges are present and the earlier support-size threshold.

Every symbolic proof in this round, the explicit criticality matchings and the two displayed completed colorings are retained. The general five-cycle proof is complete and does not take the omitted finite classification as a black-box premise. The finite audit reports remain computational evidence with exact domains: the structural audit completed all 2,476,099 assignments from a six-color universe on the stated fixture, while the method audit independently made all 72,700,180 support/family decisions using one fresh exact dynamic-programming implementation. These domains are different and must not be merged or promoted to arbitrary-list theorems by counting alone.

Executable programs, raw support/failure/orbit/multiplicity collections, raw coloring witnesses, run outputs, copied third-party source documents, private original-input identities and coordination material are excluded. In particular, the 34 orbit representatives are not individually enumerated in this prose edition. Their complete records and multiplicities and the finite scan outputs cannot be reconstructed or rerun from this prose alone. Independent computational reproduction requires fresh implementation and new record generation. The prose preserves the algorithms, exact finite contracts, aggregate counts, accepted conclusions, controls and run-mode limitations.

## Remaining question and round accounting

The full assertion for five arbitrary exceptional lists on arbitrary supports remains unproved by this work. The unrestricted critical-edge-list conjecture remains unresolved by this work. Source inspection was bounded and does not certify present-day openness or historical priority.

This is one newly accepted second substantive round, with the constructive and method-classification directions counted together. Across the first sibling edition and this one, the present continuation confirms two newly accepted rounds. An earlier screen exists, so the total lifetime attempt count is unknown. No later research round is included.

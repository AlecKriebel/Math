# Corroborative verification and its limits

The complete theorem was independently accepted by symbolic proof review before finite enumeration. The finite checks corroborate the proof, the six-edge support classification and the explicit example. They are not proof premises. No computational suite was rerun during preparation of this prose edition; the completed author and auditor results below are faithfully retained.

## Author common-core constructions

The author suite used independently verified critical fixtures with 7, 12 and 13 edges. Across those fixtures it enumerated all 600 ordinary deletion colorings. For three available third colors outside the common pair, it tested all nonconstant third-color assignments: 2,184 on the seven-edge fixture, 531,438 on the twelve-edge fixture and 1,594,320 on the thirteen-edge fixture, totaling 2,127,942 assignments.

Every available third-color class was selected as the proxy class P. The suite verified 6,346,596 class-choice restoration constructions, with 4,336,584 selections using P as the exceptional minority group and 2,010,012 using Q. Every proxy and restored coloring was independently checked for properness and list membership.

A separate binary suite exercised every nontrivial binary edge partition, every eligible mixed-vertex deletion edge, all ordinary deletion colorings, every missing exceptional-neighborhood label and both remaining palette permutations. It verified 5,522,496 complete constructions. Thirty-two all-distinct-third-color constructions exercised original palettes of up to fifteen colors. These three construction domains total 11,869,124 verified construction instances; they overlap in mathematical instances and do not enumerate distinct final colorings.

The author C++ suite was run with an optimized build and with undefined-behavior sanitization. The auditor reviewed the source, separately rebuilt it with -O3 -Wall -Wextra -pedantic and with -O1 -fsanitize=undefined -fno-sanitize-recover=all, and reproduced the frozen recorded outputs byte for byte in both modes. No sanitizer failure occurred.

## Independent construction suite

The independently authored verifier did not import the author's implementation. It used critical fixtures with 7, 10 and 13 edges. The seven-edge subdivided-K₄ fixture was tested over three available third colors; the ten-edge triangle expansion and thirteen-edge fixture were tested over binary third-color assignments. These domains differ from the author's domains.

- Seven-edge fixture: 2,184 assignments, 6,174 class choices, 23,328 eligible boundary witnesses and 299,376 complete constructions
- Ten-edge fixture: 1,022 assignments, 2,044 class choices, 11,264 eligible boundary witnesses and 138,240 complete constructions
- Thirteen-edge fixture: 8,190 assignments, 16,380 class choices, 114,688 eligible boundary witnesses and 1,400,832 complete constructions

The totals are 11,396 nonconstant assignments, 24,598 selected third-color-class choices, 149,280 mixed-vertex/minority-group witnesses and 1,838,448 complete constructions. Both minority groups occurred: 77,556 P witnesses and 71,724 Q witnesses. Mixed vertices had degree two in 24,264 witnesses and degree three in 125,016.

For each assignment the independent suite exercised every selected third-color class, every mixed vertex, both eligible minority groups, every associated deletion, all six permutations of one independently found ordinary deletion coloring, and every absent label for that coloring. It does not claim to enumerate every ordinary deletion coloring. Witness and construction counts are choice counts, not distinct-final-coloring counts.

## Six-edge support and explicit critical example

Both author and independent support checks examined all 5,216 relevant labeled six-edge candidates and found exactly one labeled K₄ and ten labeled K₂,₃ supports. Under minimum support degree two, six edges leave at most six nonisolated vertices, making the relevant bound complete. The author's degree-indexed qualifying counts are one on four vertices, ten on five vertices and zero on six vertices. This confirms the symbolic classification; it does not classify bad lists.

The explicit nine-vertex, thirteen-edge critical graph was checked by exact ordinary-colorability solving, every one of its seven displayed representative deletion certificates, all thirteen separately generated deletion certificates, both stated automorphisms and complete edge-orbit coverage. The three-label fixed-choice obstruction and the exact successful reversed-palette vector were checked. The displayed graph, matchings, automorphisms and coloring vectors are complete in THEOREM.md; raw generated certificate collections are excluded.

The author frontier checker was run normally and under Python -O and -OO. The independent auditor repeated all three modes, each reproducing the recorded output byte for byte.

## Negative controls

All ten independent controls behaved as required:

1. The construction refuses a constant assignment.
2. Exact solving confirms uncolorability for a common constant three-list.
3. Identical replacement palettes on all edges remain uncolorable.
4. Without criticality, a disconnected graph with nonconstant globally common-two-color lists can be uncolorable.
5. A corrupted deletion-coloring certificate is rejected.
6. A certificate naming the wrong deleted edge is rejected.
7. A coloring using a forbidden list color is rejected.
8. Ordinary label 0 fails for the displayed fixed-choice obstruction.
9. Ordinary label 1 fails for that same fixed choice.
10. Ordinary label 2 fails for that same fixed choice.

The author's additional boundary controls confirm that a degree-four mixed vertex with a two-by-two edge partition has no minority edge, and that two constant-list components can be globally nonconstant without satisfying the required criticality hypothesis. These controls diagnose missing hypotheses or failed proof steps; they do not extend the theorem to degree four or assert a general impossibility beyond the tested setting.

## Reproduction boundary

AGGREGATE_CHECKS.json preserves all mathematical numeric outputs and modes. Implementations, binaries, raw fixture/support/certificate/coloring collections and raw completed-run records are not distributed. Rerunning the computational suites requires independently implementing the described enumerations and regenerating their records. The complete symbolic argument and explicit small mathematical certificates are inspectable directly. The public manifest identifies actual distributed files only; it makes no claim that the omitted records are public or reproducible from prose alone.

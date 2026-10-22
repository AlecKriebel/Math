# Exact constructive checks

The proof in [THEOREM.md](THEOREM.md) is symbolic. These finite checks corroborate its construction and test the quantifiers; they are not assumptions of the theorem and do not exhaust all critical graphs.

## Full coloring construction

The author C++ construction checker independently checks that each supplied graph is simple and subcubic, has no ordinary three-edge-coloring, and is three-edge-colorable after each edge deletion. It then constructs the permissible color-class matchings and their ordered path/cycle components.

For each tested nonconstant assignment, it finds incident edges with different reduced lists, selects the first critical cycle if its reduced lists vary, and otherwise selects the second. It colors the matching with the common color and the complement by the elementary traversal in Lemma 4. Every resulting full coloring is checked directly against every edge list and every pair of incident edges.

The tested families are all assignments with one specified common color and the remaining two colors chosen from:

- three other colors, on all seven fixtures (edge counts 7, 10, 10, 10, 10, 12, 13);
- four other colors, on the seven-edge fixture.

Every nonconstant assignment in each family was tested. The five-palette family includes the embedded four-palette families; these are separately scoped test runs rather than a claim of distinct assignments modulo color renaming across runs.

Author construction totals:

- 2,644,056 nonconstant assignment runs;
- 2,585,826 with total intersection exactly the specified common color;
- 58,230 with a larger total intersection;
- 2,641,608 constructions using the first chosen critical cycle;
- 2,448 constructions requiring the second chosen cycle.

All passed. The optimized and undefined-behavior-sanitized builds produced byte-identical result files. Runtime conditions use explicit checked exceptions and remain active in optimized builds.

## Independent Python structural checks and controls

The separate author Python structural checker uses a separate set-based backtracking solver and connected-component analysis. Across the seven fixtures it exhausts:

- all 1,020 ordinary colorings of all edge deletions;
- all 1,236 permissible color-class matchings arising from those colorings;
- 432 witnesses in which an original degree-two endpoint does not see the chosen color, explicitly exercising that boundary;
- 818 choices of distinct cycle sets at incident edges, checking that they share an incident edge at the common endpoint.

Every chosen matching covers all original degree-three vertices; its complement has maximum degree two and exactly one odd cycle through the deleted edge. All original fixtures are also independently verified non-three-colorable, and every deletion has at least one ordinary coloring.

The author control checks include two exact small examples, with all edges, lists, selected matchings, and full coloring vectors. They are expressed as authored examples below:

1. An assignment whose total intersection is exactly one color, for which one valid deletion-color-class matching leaves a constant-list odd cycle and fails the common-color-matching strategy. A full list coloring exists. This checks that selecting a suitable matching is essential; the theorem does not claim that every permissible matching works for every list assignment.
2. An assignment using all four three-subsets of a four-color palette, with empty total intersection, that has a full list coloring. This checks that the theorem's uncovered scope is not being mistaken for an uncolorable family.

Constant three-lists are rejected on every fixture. Constant two-lists on cycles of lengths three through nine are colorable exactly at even lengths.

## Reproduction boundary

The author construction checker was compiled with C++17, `-O3 -Wall -Wextra -pedantic`, and separately with `-O2 -fsanitize=undefined -fno-sanitize-recover=all`. Both outputs were byte-identical. The separate Python structural checks used exact backtracking and component analysis. The independent mathematical audit additionally rebuilt the author checker with `-O2 -std=c++17` and reproduced the recorded result byte for byte.

No random sampling, heuristic timeout, or inferred coloring is counted as a success in the author's exhaustive construction suite. The independent audit's larger-palette assignment sample is deterministic pseudorandom, as explicitly stated below and in AUDIT.md; it is not exhaustive. No computational suite was rerun during preparation of this edition.

The implementations, binaries, raw graph/fixture/certificate/coloring collections and raw run outputs are not distributed. The suites cannot be rerun or omitted records reconstructed from this prose alone. Reproduction requires fresh implementation and fresh input generation. Counts below preserve numerical coverage but do not replace the omitted records. The complete symbolic theorem does not depend on any finite computation.

## Complete author construction strata

Fixture numbers below are count-stratum labels, not identities or representations of the excluded graph collections. Fixtures 0 through 6 have respectively 7, 10, 10, 10, 10, 12 and 13 edges. In each stratum the fields are assignment runs; first-cycle constructions; second-cycle constructions; intersection exactly the specified common color; and intersection larger.
- Fixture 0, 7 edges, total palette 4: 2,184; 2,160; 24; 1,806; 378.
- Fixture 0, 7 edges, total palette 5: 279,930; 279,720; 210; 271,194; 8,736.
- Fixture 1, 10 edges, total palette 4: 59,046; 58,968; 78; 55,980; 3,066.
- Fixture 2, 10 edges, total palette 4: 59,046; 58,962; 84; 55,980; 3,066.
- Fixture 3, 10 edges, total palette 4: 59,046; 58,962; 84; 55,980; 3,066.
- Fixture 4, 10 edges, total palette 4: 59,046; 58,962; 84; 55,980; 3,066.
- Fixture 5, 12 edges, total palette 4: 531,438; 529,854; 1,584; 519,156; 12,282.
- Fixture 6, 13 edges, total palette 4: 1,594,320; 1,594,020; 300; 1,569,750; 24,570.

The four-palette family on each m-edge fixture has 3^m−3 nonconstant assignments. The five-palette family on the seven-edge fixture has 6^7−6=279,930. Embedded domains overlap; these totals count scoped runs, not distinct assignments modulo color renaming across runs.

## Complete author structural strata

For each fixture, the fields are all labeled deletion colorings; all permissible color-class instances; degree-two-endpoint cases missing the selected label; and distinct odd cycles.
- Fixture 0, 7 edges: 48; 60; 24; 2.
- Fixture 1, 10 edges: 96; 120; 48; 3.
- Fixture 2, 10 edges: 108; 120; 24; 3.
- Fixture 3, 10 edges: 72; 84; 24; 2.
- Fixture 4, 10 edges: 144; 168; 48; 4.
- Fixture 5, 12 edges: 360; 468; 216; 8.
- Fixture 6, 13 edges: 192; 216; 48; 4.

## Complete independent audit strata

The independent Python audit exhausts all labeled deletion colorings and permissible labels on the same seven shared fixtures. Assignment coverage is exhaustive on the seven-edge fixture over three noncommon colors (2,184 nonconstant assignments), and consists of 200 deterministic pseudorandom assignments on each other fixture over eleven noncommon colors. Every selected incident-list transition is tested with every available witness pair. The fields below are vertices/edges; labeled deletion colorings; permissible-label instances; distinct edge/matching witnesses; overlap pairs; nonconstant assignments; full validated constructions; second-cycle uses; and separate exhaustive assignment-oracle checks.
- Fixture 0: 5/7; 48; 60; 10; 24; 2,184; 7,284; 48; 2,184.
- Fixture 1: 7/10; 96; 120; 17; 51; 200; 1,776; 0; 0.
- Fixture 2: 7/10; 108; 120; 17; 53; 200; 790; 0; 0.
- Fixture 3: 7/10; 72; 84; 14; 34; 200; 788; 0; 0.
- Fixture 4: 7/10; 144; 168; 28; 140; 200; 3,168; 0; 0.
- Fixture 5: 9/12; 360; 468; 48; 336; 200; 3,200; 0; 0.
- Fixture 6: 9/13; 192; 216; 36; 180; 200; 1,600; 0; 0.

Totals are 1,020 labeled deletion colorings, 1,236 permissible-label instances, 170 distinct edge/matching witnesses, 818 overlap pairs, 3,384 nonconstant assignments, 18,606 directly validated full constructions, 48 second-cycle uses and 2,184 separate assignment-oracle checks. All seven fixtures pass the three-isolated-vertices invariance check with identical deletion-coloring and matching-witness counts. The independent cycle oracle checks 9,828 assignments on cycle lengths three through eight. Author and auditor domains overlap and must not be summed as disjoint coverage. Witness/construction counts do not assert distinct final colorings.

The independent audit reports nine named successful negative/boundary controls: constant exact-three lists on a critical graph; dropping ordinary noncolorability; dropping deletion-criticality on a disconnected example; dropping it on a connected subcubic example; degree-four overlap failure; constant odd-cycle two-lists; the independent cycle-oracle characterization; exact-two common-color-list failure; and all-four-list-type empty intersection. AUDIT.md retains every substantive conclusion.

## Explicit authored controls

Use the ordered seven-edge graph e0=01, e1=02, e2=13, e3=14, e4=23, e5=24, e6=34. A proper ordinary coloring of its e0-deletion is (−1,0,2,1,1,2,0), where −1 marks the deleted edge. Selecting ordinary label 1 gives the matching {e3,e4}; its unique odd cycle has edge set {e0,e1,e2,e5,e6}. A degree-two endpoint does not see the selected label, exercising the boundary allowed by Lemma 2.

For the fixed-matching control, set every list to {0,1,2}, except L(e3)={0,1,3} and L(e4)={0,2,3}. The global intersection is exactly {0}. If the matching {e3,e4} is forced to the common color 0, the residual odd cycle has constant reduced list {1,2}; this fixed-matching strategy fails. Nevertheless (0,1,1,3,3,0,2) is a proper full list coloring in the displayed edge order. Thus not every permissible matching works for every assignment; selecting a suitable critical cycle is essential.

For the empty-intersection control, assign the ordered lists ({1,2,3}, {0,2,3}, {0,1,3}, {0,1,2}, {1,2,3}, {0,2,3}, {0,1,3}). All four triple types occur and the total intersection is empty. The vector (1,2,0,2,1,0,3) is a proper full list coloring. This assignment is outside the theorem but is colorable; the uncovered scope is not an asserted obstruction.

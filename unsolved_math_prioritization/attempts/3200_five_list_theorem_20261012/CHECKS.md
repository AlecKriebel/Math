# Reported mathematical checks and reproduction boundary

Date: 12 October 2026 UTC. AGGREGATE_CHECKS.json preserves the mathematical numerical results reported with the accepted proof and audit packets. This prose preparation verified their source integrity and preservation; it did not rerun the full mathematical suites. The complete symbolic proofs, rather than the computations, establish the theorems.

## Subcubic author checks

The author's local checks include all 958 labeled K4-free five-vertex graphs, of which 570 have triangles, and 64,251 uniform-recoloring cases. The four-vertex lemma check uses all 63 non-K4 graphs and 10,000 list families per graph over four colors: 630,000 cases, with 1,644 bad cases. Equality checks cover 729 three-unit cases, with 36 failures, and 81 two-plus-one cases, with 9 failures. These failures match the exact stated equality criteria.

Twenty supplied simple subcubic supports serve as fixtures, not an independent proof of support completeness. Checks include 83 incident-pair bounds, 19 triple incidences, 153 h=3 cross-incidence cases, 7,600 h=4 eligibility cases and 2,916 universal-edge interior cases. There are 108 disconnected h=3 deletion cases. A normalized doubleton {0,1} and a six-color singleton universe give 129,600 one-doubleton reduction cases, of which 8 have no strict certificate.

The complete-coloring tests verify the criticality of K4 with one edge subdivided and the Petersen graph with one vertex removed, including all 19 edge-deletion colorings. They test 1,240,029 assignments on every one of the 21 five-edge supports of the seven-edge fixture over five colors; 2,476,099 assignments on its diamond support over six colors; and 192,456 assignments on all 792 five-edge supports of the twelve-edge fixture over four colors. The total is 3,908,584 assignments. Two constant-list negative controls and a noncritical disjoint-union control pass. The recorded search-node count, including controls, is 32,702,375.

Python symbolic checks agree in normal, -O and -OO modes. Full-fixture outputs agree between g++ 14.2.0 at -O3 and at -O1 with undefined-behavior sanitization and nonrecovering failures. These are reported completed runs; no new rerun is implied by their inclusion here.

## Independent subcubic audit

AUDIT_SUBCUBIC.md retains the independent list-family normalization, exact equality tests, support generation, every symbolic case review, explicit small graph controls and full-coloring construction scope. Its separately generated local checks cover 1,944,495 four-vertex list tests, 980,992 bounded-palette five-vertex tests, and 810 equality cases. The 18,745 valid endpoint partitions give 673 labeled incidence graphs. Every support-control count and all strict and non-strict construction branch counts are retained in AGGREGATE_CHECKS.json.

The 1,841,454 full-coloring constructions include an exhaustive five-color domain on the seven-edge fixture, systematic deficit/palette placements on two fixtures and 8,748 targeted disconnected-triangle cases. These checks overlap the author domain and are not additional disjoint coverage. C++ -O2 and -O3 -DNDEBUG outputs agree; independent Python support outputs agree in normal, -O and -OO modes.

## Higher-degree checks

The author's endpoint-partition generator examines 20,457 partitions and obtains 24 five-edge line-graph types, one star and 23 nonstar. Every one of 23×4⁵=23,552 ordered capped-deficit profiles is certified. The certificate counts are 23,538 strict greedy, 2 strict two-list and 12 incident-pair. The greedy-only frontier has 14 profiles. A distinct clique-partition support generator and explicit-order checker reproduce the 24 types and all 23,552 outcomes, and check 958 labeled K4-free graphs and 432 final Hall cases. The two author checkers report identical outputs across normal, -O and -OO execution.

AUDIT_HIGHER_DEGREE.md preserves the independent generation of all 16,824 simple five-edge graphs with no isolated vertices, all support and actual recorded certificate-order checks, expanded weights through eight, bounded list-lemma tests, and 258,048 full degree-four fixture constructions. Its independent 23,552 profile certificates have the same type counts. All 753,664 expanded-weight cases preserve the original residual sum. All 432 final distinct-label Hall cases succeed, with at least four successful permutations each. Small-lemma tests include 958 transversal graphs, 36,288 placements for the noncomplete 2,2,3,3 lemma and 53,136 triangle-free two-list placements. The full-graph construction caches 372 ordinary colorings. All eleven explicit negative and boundary controls are retained in the audit. Its normal, -O and -OO results agree byte for byte.

## What is and is not distributed

These records report acceptance evidence with exact finite scopes. Arbitrary colors, arbitrary graph order and the cap-at-four lifting argument are covered by the symbolic proofs, not by extending a finite count beyond its tested domain. The prior large exterior-classification scan and the complementary subcubic boundary enumeration are not logical premises of the theorem. The subcubic audit explicitly did not rerun that complementary enumeration.

No executable programs, support tables, certificate records, raw case outputs or raw coloring witnesses accompany this edition. Only authored arguments, explicitly displayed small mathematical examples, audit explanations and mathematical aggregates are distributed. A reader can check the symbolic proofs in full, but reproducing the computational claims requires independently writing the described checks and generating fresh records.

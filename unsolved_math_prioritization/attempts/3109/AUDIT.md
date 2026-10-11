# Independent audit of the Petersen fragment counterexample

## Decision

**Accept the frozen candidate as a complete refutation of the literal target.** No correction to its mathematical proof is required. The accepted result is a connected simple bridgeless cubic graph on 30 vertices whose every 2-factor consists entirely of odd cycles and whose oddness is 4. More generally, the proof gives oddness \(n+1\) on \(10n\) vertices for every odd \(n\ge3\).

The audited candidate has 7,082 bytes and SHA-256
`39d4d6b4d0d4c48e5cfd8cfb19450d1ba9acfa7b1b629da7f62fd0af6f7c475f`.
The audit does not alter that candidate.

## Target and source checks

The original [Open Problem Garden statement](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness) and its [29 June 2010](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6751) and [2 July 2010](https://www.openproblemgarden.org/op/odd_cycles_and_low_oddness#comment-6753) comments were inspected on 11 October 2026. Both comments are attributed by the page to Anonymous. The displayed conjecture imposes bridgelessness and cubicity, with no 3-edge-connectivity assumption. The source supports attribution of the construction and two-case idea; the mathematical conclusion is accepted on the independent proof below, not on the comment author's authority.

This is a reconstruction and verification of an existing posted counterexample. It does not assert novelty, journal publication, or absence of a journal treatment. The site still displaying a conjecture heading is not evidence against the verified counterexample.

## Mathematical obligations

- **Graph definition:** The indexed edge construction specifies all vertices and edges, including modular conventions. For odd \(n\ge3\) it produces a simple cubic connected graph.
- **Petersen girth:** The proof excludes cycles of lengths 3 and 4 by classifying the number of spokes. The argument also exhibits 5-cycles.
- **Small edge cuts:** The smaller-side count handles every possible side size from 1 through 5. It excludes cuts of size 1 or 2, which is enough to prove that deleting the chosen spoke leaves a connected bridgeless fragment.
- **All Petersen factors:** Complementation reduces the question to perfect matchings. Spoke parity leaves 1, 3, or 5 spokes; the three-spoke case is impossible, and all remaining cases are explicitly classified.
- **Witness correctness:** The displayed five-vertex cycles use valid edges and partition the ten vertices. The containing-edge witness really contains the deleted spoke; removing it gives a four-edge path on five vertices, not a five-edge path.
- **Bridgelessness:** Internal edges lie on cycles within their fragments. A separate cycle through chosen terminal paths and all links covers every link. Connectivity alone would not have sufficed, but the candidate supplies the needed stronger argument.
- **Exhaustive global factors:** Cut parity forces either all or no links. The Petersen classification then proves that the all-link case forms one cross-block cycle. No unsupported assumption that parity alone forces one cycle is needed.
- **Oddness equality:** Both types of factor are realized. The lower bound and upper bound coincide at \(\min(2n,n+1)=n+1\). For \(n=3\), this is 4, not merely an unspecified value greater than 2.
- **Quantifiers:** The proof classifies every 2-factor and explicitly establishes their existence, so there is no vacuous all-factors claim.
- **Limits:** The graphs have 2-edge-cuts. Even \(n\) violates the all-odd premise, and \(n=1\) gives only the Petersen graph of oddness 2. No minimal-order claim or stronger-connectivity claim is accepted.

The accompanying PROOF.md supplies a standalone proof of all these obligations.

## Independent finite verification

Independent finite verification supplements the mathematical proof.

The checker constructs the graph, verifies cubicity and connectedness, deletes every edge in turn to test bridgelessness, and enumerates perfect matchings by recursively covering vertices with edges. Every returned matching is checked and deduplicated. Its complement is checked as a spanning 2-factor before component lengths are counted.

For the Petersen graph alone, an additional brute-force enumeration of all five-edge subsets independently finds the same six perfect matchings. Direct enumeration of all ten-edge subsets independently finds the same six 2-factors. All vertex cuts are inspected to compute edge-connectivity 3. The girth is computed independently as 5. Deleting the chosen spoke is checked to leave a connected bridgeless graph, and the explicit cycle witnesses are checked edge by edge.

All perfect matchings are enumerated for \(n=1,2,3,4,5,6,7\). Their number is \(2^n+4^n\); the two factor types occur with multiplicities \(2^n\) and \(4^n\), respectively. At \(n=1\), the two types have the same length multiset and their histogram entries combine.

- \(n=3\): 30 vertices, 45 edges, 72 matchings; 8 factors with six 5-cycles and 64 with lengths \((5,5,5,15)\). Oddness is 4.
- \(n=5\): 50 vertices, 75 edges, 1,056 matchings; 32 factors with ten 5-cycles and 1,024 with lengths \((5,5,5,5,5,25)\). Oddness is 6.
- \(n=7\): 70 vertices, 105 edges, 16,512 matchings; 128 factors with fourteen 5-cycles and 16,384 with seven 5-cycles and one 35-cycle. Oddness is 8.

These finite checks corroborate the proof; they do not replace its argument for arbitrary odd \(n\).

## Adversarial controls

Eight controls are required to fail their intentionally false acceptance claims:

1. Omitting the closing link fails cubicity.
2. Restoring deleted spokes in addition to links fails cubicity.
3. The \(n=2\) graph has a 2-factor with an even 10-cycle.
4. The \(n=4\) graph has a 2-factor with an even 20-cycle.
5. The \(n=1\) graph has oddness 2 and cannot refute the bound.
6. Changing the inner step from 2 to 1 produces pentagonal-prism fragments, and the all-odd conclusion fails.
7. Claiming oddness \(2n=6\) at \(n=3\) is rejected by the four-cycle factor.
8. An altered displayed 5-cycle containing a nonedge is rejected.

All eight controls are rejected as intended. Positive checks and negative controls pass identically in normal execution and both optimization modes (levels 1 and 2). The validation gates remain active in all three modes.

## Acceptance boundary

Acceptance covers the mathematical refutation and attribution in the frozen candidate, together with the supplied independently authored proof and audit. It does not certify journal publication, an optimal number of vertices, or a result for 3-edge-connected cubic graphs.

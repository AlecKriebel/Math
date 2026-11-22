# Independent review of the finite edge cover counterexample

## Verdict and scope

**Accepted.** The proposed argument correctly proves that the hypergraph whose vertices are the natural numbers and whose edges are all finite subsets of the natural numbers has no strongly minimal edge cover. The witnesses use only finitely many edge changes, and their edge-family differences have unequal finite sizes. No comparison or subtraction of infinite cardinalities is needed.

This is an independent correctness audit of an existing result, not a new counterexample or a novelty claim. The example and argument already appear in Dominic van der Zypen, *Counterexample to a conjecture of Aharoni and Korman*, arXiv:2205.02296v1 (2022), Lemma 2.1: <https://arxiv.org/abs/2205.02296v1>. The two-page source text was inspected for its definition and proof. This review does not claim a formal theorem-prover verification, a new literature search, or an independent audit of any later bounded-edge-size counterexample.

## Statement and conventions

Let V = N and let E = [N]^{<omega}, interpreted as the set of all finite subsets of N, including the empty set. An edge cover is a subfamily C of E with union C = N. A cover C is strongly minimal if, for every edge cover D contained in E,

    |C \ D| <= |D \ C|.

The differences here are sets of edges, not sets of vertices. In particular, an edge with many vertices still counts as one added edge. The direction of this inequality is essential.

The hypergraph satisfies the finite-edge hypothesis and has no isolated vertices: {v} is an edge for every v in N. It has no common finite upper bound on edge size. Every cover contains infinitely many edges, because a finite union of finite sets cannot be N. In particular, every cover has two distinct members.

## Audit of the proposed case split

### Covers that are not inclusion minimal

By the definition of failure of inclusion-minimality, there is a proper subfamily C0 of C that still covers N. Choose a in C \ C0 and put D = C \ {a}. Since C0 is contained in D, D also covers N. Its differences from C are exactly

    C \ D = {a},    D \ C = empty set.

Consequently, 1 > 0 violates strong minimality. This reasoning does not assume that C has an inclusion-minimal subcover. The existence of the proper covering subfamily C0 is sufficient, and deleting one edge outside C0 gives a finite witness even if C \ C0 is infinite.

### Covers that are inclusion minimal

Choose distinct a, b in C. If a were contained in b, then C \ {a} would cover everything C covers, contrary to inclusion-minimality. The same argument excludes b contained in a. Thus u = a union b differs from both a and b.

The set u is finite and hence belongs to E. It cannot belong to C: since u differs from a and contains a, its presence in C \ {a} would make a removable. Set

    D = (C \ {a,b}) union {u}.

Replacing a and b by their union leaves the union of the whole edge family unchanged, so D covers N. Because u is new and differs from both deleted edges,

    C \ D = {a,b},    D \ C = {u}.

Therefore 2 > 1 violates the required inequality. All asserted set differences are exact. The argument does not merely claim that the overall cardinality of the cover decreases.

The two cases exhaust every cover C, completing the proof.

## Independent exchange cross check

The conclusion can also be checked without the inclusion-minimality split. For any cover C and any distinct a,b in C, form u = a union b and D = (C \ {a,b}) union {u}. This remains a cover by union preservation. Exactly one of the following occurs:

- If u equals a or b, precisely the other edge is removed. The difference sizes are (1,0).
- If u belongs to C but differs from a and b, both a and b disappear and no new edge is added. The sizes are (2,0).
- If u does not belong to C, both selected edges disappear and u is new. The sizes are (2,1).

Each case strictly violates strong minimality. This cross-check confirms that neither hidden disjointness nor the existence of a minimal subcover is carrying the proof. It is an alternative verification of the same elementary mechanism, not a claim to a new result.

## Adversarial edge cases

- **Empty edge.** A cover containing the empty edge is not inclusion-minimal, since that edge can be deleted. The first case handles it. Excluding the empty edge from E would not rescue strong minimality: the same proof applies to all nonempty finite subsets.
- **Duplicate edges.** E and C are sets of subsets, so repeated copies of an edge are not separate members. The proof selects distinct sets. A labelled multihypergraph with multiplicity-sensitive definitions is not the statement being audited.
- **Overlapping edges.** Minimality implies that distinct cover edges are incomparable under containment, not that they are disjoint. The union replacement preserves coverage even when a and b overlap.
- **Infinite edge families.** Both C and D may be countably infinite and have the same total cardinality. That does not satisfy strong minimality: the relevant finite differences are still 2 and 1, or 1 and 0. Ordinary minimum-cardinality coverage is a weaker property here.
- **Local exchange interpretation.** The witnesses have finite symmetric difference, so the example also defeats the restricted requirement that the inequality hold only for finite modifications. It does not rely on allowing an infinitely changed competing cover.
- **Membership of the replacement.** Closure under finite unions is indispensable to this particular construction. It holds for all finite subsets, but cannot be silently assumed for an arbitrary finite-edge hypergraph or a uniformly bounded-rank restriction.
- **Choice and maximality principles.** Only one or two members of a nonempty set are selected at a time. No simultaneous choice of infinitely many private vertices, Zorn argument, or existence theorem for minimal covers is invoked.

## Finite truncations and negative controls

For a finite nonempty vertex set Vn, the full subset Vn itself belongs to E_n = P(Vn). The singleton edge family {Vn} is strongly minimal. If a competing cover D contains Vn, the left difference is zero. If it does not, the left difference has size one and D must be nonempty, so the right difference has size at least one.

In fact, {Vn} is the only strongly minimal cover in this finite truncation: every cover with at least two members fails by the three-case exchange above, and the only singleton cover is {Vn}. For the empty vertex set, the empty edge family is the unique strongly minimal cover; the family containing the empty edge alone is not strongly minimal.

Thus finite truncations are not smaller examples of the infinite counterexample. They admit a covering edge that has no permitted analogue on N, since N is not a finite edge. Checking finitely many vertex sets cannot substitute for the infinite argument.

As a finite sanity check, an exhaustive enumeration inspected all edge subfamilies of P(Vn) for 0 <= n <= 4. For every cover with at least two edges, the exchange using its first two edges in bit-mask order preserved coverage and had one of the three strict difference pairs above. The counts were:

| Number of vertices | Edge subfamilies checked | Covers | Covers with at least two edges |
| --- | --- | --- | --- |
| 0 | 2 | 2 | 0 |
| 1 | 4 | 2 | 1 |
| 2 | 16 | 10 | 9 |
| 3 | 256 | 218 | 217 |
| 4 | 65,536 | 64,594 | 64,593 |

The empty-universe deletion case was checked separately. The enumeration checked union preservation and exact strict difference inequalities; it was not an all-pairs search for strong minimality and is not offered as a proof of the infinite theorem. The mathematical analysis above settles both the finite exception and the infinite claim.

A separate structural negative control is the hypergraph on N with only singleton edges. Its sole cover consists of all singleton edges and is strongly minimal. This illustrates why finite edges and an infinite vertex set alone do not force failure in every hypergraph: the counterexample also uses its particular union-closed edge family.

## Consistency with the accompanying audit

The accompanying `MATHEMATICAL_AUDIT.md` and `ACCEPTANCE_REPORT.md` were inspected and agree with the accepted proof and its limits. The functions in `regression.py` were independently rerun under ordinary Python for n = 1, 2, 3, 4 without rewriting their saved output. Their case results matched `REGRESSION_RESULTS.json` exactly: 65,812 families, 64,824 covers, 64,764 deletion-witness covers, 56 merge-witness covers, and four singleton exceptions. These figures exclude the empty-universe case included in the separate cross-check above, so there is no discrepancy between the totals.

The supplied regression checks every pair in each inclusion-minimal cover with at least two edges. The independent cross-check instead tests one pair in every cover with at least two edges, including nonminimal covers. These are complementary bookkeeping tests, not competing classifications. The harness was then hardened with an explicit refusal of optimized Python, where assertions would otherwise be disabled. Independent reruns confirmed both that the normal execution still matches all saved cases and that optimized import raises the intended RuntimeError. This is a fail-closed safeguard, not verification under an optimized interpreter or a proof assistant.

## Acceptance boundary

No mathematical repair is needed. A public account should retain the exact strong-minimality inequality, explain why the union is a new edge in the minimal-cover case, distinguish finite edges from a uniform finite rank bound, and identify this as the existing 2022 counterexample. It should not report the result as newly solved or imply that this audit validates different, later theorems.

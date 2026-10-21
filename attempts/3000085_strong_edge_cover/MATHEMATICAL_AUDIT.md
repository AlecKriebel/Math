# Strongly minimal edge covers: audit of an existing counterexample

Date: 2026-10-21. Target: row 1905, ID 3000085, AMR-029-0085.

## Disposition and attribution

The finite-edge existence assertion is false. The result is already in Dominic van der Zypen, *Counterexample to a conjecture of Aharoni and Korman*, arXiv:2205.02296v1 (4 May 2022), Lemma 2.1, [versioned source](https://arxiv.org/abs/2205.02296v1). The argument below is an independently checked exposition of that existing counterexample, not a new mathematical result or a new solution claim.

Recommended classification: **already_solved**, with **1** audited disposition turn. The conjecture is resolved negatively; “solved” does not mean its assertion is true. No queue edits or publication are part of this audit.

## Exact target

A hypergraph here is H=(V,E), with E a set of subsets of V. Assume every member of E is finite and the union of E is V. An edge cover C is a subfamily of E whose union is V. Strong minimality means that for every edge cover D,

    |C \ D| ≤ |D \ C|.

These are cardinalities of families of edges. The target asserts the existence of such a C for every H under these hypotheses. There is no finite-ground-set assumption and no common finite bound on edge sizes. Reversing this inequality changes the property and is not a harmless typographical convention. An expected-true assessment of the unchanged target is obsolete in light of the 2022 counterexample.

## Counterexample and complete proof

Set V=N and let E consist of all finite subsets of N. Each edge is finite. Every vertex belongs to its singleton edge, so the hypergraph has no isolated vertices and admits edge covers.

Let C be any edge cover. We construct another edge cover D for which the required inequality fails, using only finite differences.

**Case 1: C is not inclusion-minimal.** There is a proper subfamily C0 of C that still covers N. Choose an edge a in C\C0. Then D=C\{a} contains C0 and therefore covers N. Exactly one edge is removed and no edge is added:

    |C \ D|=1 > 0=|D \ C|.

This case does not assume that every cover contains an inclusion-minimal subcover; it uses only the definition of failure of minimality for this C.

**Case 2: C is inclusion-minimal.** C has at least two distinct members, since the union of at most one finite set cannot be N. Select distinct a,b in C. Neither contains the other: if a were contained in b, removing a would preserve the union, contrary to minimality; the reverse containment is excluded in the same way.

Let u=a∪b. This is finite, hence u is an available edge of H. It differs from a and b by the noncontainment just established. In fact u is not any member of C: if u belonged to C, then it would remain after removing a, and since it contains a, that deletion would preserve the cover, again contradicting minimality.

Define D=(C\{a,b})∪{u}. Replacing a and b by their union preserves the union of the whole family, so D covers N. Because u is new and is neither removed edge, the differences are exactly C\D={a,b} and D\C={u}. Consequently,

    |C \ D|=2 > 1=|D \ C|.

Both cases contradict strong minimality. Since C was arbitrary, H has no strongly minimal edge cover. This refutes the target.

## Checks against possible scope errors

- Allowing the empty edge causes no problem: any cover containing it is in Case 1. If one's convention forbids empty edges, deleting the empty edge from E leaves the same counterexample and argument.
- Edges are a set, not a multiset. The proof establishes that the added union is not already present, rather than assuming multiplicity arithmetic.
- No subtraction or cancellation of infinite cardinalities occurs. The witness differences are 1 versus 0 or 2 versus 1, even though C and D are infinite.
- Minimum cardinality is insufficient: every cover in this example is infinite, but the argument disproves strong minimality by finite exchanges. Inclusion-minimality is likewise insufficient. For example, all singleton edges form an inclusion-minimal cover, defeated by merging any two of them.
- Closure under finite unions is essential to this particular construction. E has unbounded finite edge sizes; the proof does not establish a bounded-rank or 3-uniform counterexample.
- On a finite nonempty ground set, the analogous complete hypergraph has the strongly minimal one-edge cover {V}. Thus finite truncations are not finite counterexamples. The infinite ground set is used to exclude precisely the singleton-cover obstruction to Case 2.
- Only two arbitrary members of a particular cover are selected. No simultaneous family of choices or assertion of a minimal-subcover existence theorem is needed.

## Finite regression and its limits

`regression.py` enumerates every edge subfamily of the complete hypergraph on n=1,2,3,4 labeled vertices, including the empty edge. For each cover it verifies either a one-edge deletion or, for every pair in an inclusion-minimal cover with at least two members, the exact two-for-one replacement. It deliberately recognizes {V} as the unique remaining finite exception. It does not purport to formally verify the infinite theorem.

The run checked 65,812 families and 64,824 covers: 64,764 deletion witnesses, 56 merge-witness covers, and four singleton exceptions. Results are in `REGRESSION_RESULTS.json`. The finite tests guard the exchange bookkeeping and empty-edge case; the mathematical proof above supplies the infinite conclusion.

## Sources and bounded claims

The complete two-page van der Zypen source supplies the decisive existing proof. Ron Aharoni, *Strongly maximal matchings and strongly minimal covers*, [arXiv:2206.02576v1](https://arxiv.org/abs/2206.02576v1), is corroborating historical context for the finite-edge counterexample and the later bounded-edge-size refinement, not a certificate that the refined problem remains open.

Lawrence Hollom and Benedict Randall Shaw, *Counterexamples to Conjectures on Strong Maximality and Minimality*, Electronic Journal of Combinatorics 33(2), P2.11 (2026), [DOI 10.37236/14948](https://doi.org/10.37236/14948), states a 3-uniform counterexample in its published Theorem 3. The corresponding [arXiv:2511.13709v1](https://arxiv.org/abs/2511.13709v1) numbers that result Theorem 1.3. This audit does not accept or reconstruct its full gadget proof; that stronger result is unnecessary for the target resolved here.

Attribution to Aharoni and Korman, *Greene–Kleitman's theorem for infinite posets*, Order 9 (1992), 245–253, Conjecture 5.4, is supported by the accessible later primary papers. The 1992 full text and original Egres wiki page were not inspected here, so exact historical wording and a freshly recovered wiki formulation are not certified. These provenance limitations do not affect the explicit counterexample to the target stated above.

# Five-approach investigation

Checked 2026-10-05 UTC. Rank 770, ID 2599, KOU-21.90.

## 1. Exact target, prior work, and current literature

The numeric landing page failed in the web reader. The complete locally available public corpus supplies the exact target, which was checked against the freshly retrieved October 2026 editor PDF. Printed page 190 was visually inspected: A. A. Makhnev is the proposer; there is no annotation or status marker on 21.90. The integrated problem collection governs over aggregator status text. The editor repository had no visible entry labeled 21.90.

The full public problems and research-results corpus bytes were independently hashed. The target record's dated aggregator triage says open. No matching research-result key or record containing 21.90 was found. A content scan found only this exact Q-polynomial/two-strongly-regular target. Public GitHub exact searches and the immutable-base attempt-path lookup did not locate a prior attempt; bounded-search limitations are retained.

The directly matching paper is Belousov–Makhnev–Nirova, *On Q-polynomial distance-regular graphs Γ with strongly regular graphs Γ₂ and Γ₃*, Siberian Electronic Mathematical Reports 16 (2019), 1385–1392, DOI 10.33048/semi.2019.16.096. Its Proposition 1 concerns primitive graphs, Proposition 2 recognizes the crown exception, and subsequent sections give parameter families. Relevant proof passages were inspected. This established that parameter feasibility and the disconnected boundary are old, not new discoveries.

Relevant later/related primary records:

- Makhnev–Isakova–Nirova (2019), DOI 10.33048/semi.2019.16.087: published nonexistence of arrays {69,56,10;1,14,60}, {74,54,15;1,9,60}, {119,100,15;1,20,105}. Abstract and bibliography verified; complete external proof not audited.
- Makhnev–Golubyatnikov (2019), DOI 10.21538/0134-4889-2019-25-4-136-141: excludes an even-parameter subfamily of type II. PDF downloaded; main statement and relevant setup inspected, not independently reproved in general.
- Makhnev–Isakova–Tokbaeva (2020), DOI 10.33048/semi.2020.17.093: small type-III restrictions and exclusions. Web PDF inspected, with arithmetic caveat recorded in LIMITATIONS.md.
- Golubyatnikov (2020), DOI 10.21538/0134-4889-2020-26-4-98-105: excludes {104,70,25;1,7,80} and {272,210,49;1,15,224}; discusses the hypothetical {399,320,64;1,20,336} case. Downloaded and inspected statements plus relevant proof conclusions; no general conclusion extracted.
- Makhnev–Isakova–Tokbaeva (2023), DOI 10.33048/semi.2023.20.017: primary record states nonexistence of {143,108,27;1,12,117}. Abstract-level verification only.

Searches for exact problem number, matching title/keywords, later years through 2026, and specific small arrays did not yield a verified full resolution. Nearby 2025 bipartite results concern diameters four/five and are not a solution of this target. This is a bounded search result, not proof of novelty or universal absence.

## 2. Explicit construction at the convention boundary

Constructed the crown family directly, proved all distances and its intersection array, and wrote a tensor-idempotent Schur multiplication proof of Q-polynomiality. The six-cycle is the smallest explicit witness under the μ=0 convention. Both distance graphs are disconnected, so the question under the connected/nondegenerate interpretation remains unresolved here.

## 3. Symbolic fusion and Krein constraints

Independently computed multiplication by the adjacency matrix. Equality of the two appropriate pairs of intersection numbers yields the three-parameter array without importing the classification. Rational algebraic integrality forces t to be integral. Computed the two eigenmatrices, all relevant square Krein coefficients, and the necessary Diophantine condition. This also separates the t=1 and a=0 exceptional regimes. The printed identities pass exact symbolic checks.

## 4. Exhaustive bounded necessary-parameter sieve

Enumerated all possibilities in 2≤t≤30 using 1≤a≤t²−2 and the forced value of c. Tested exact intersection/Krein data, multiplicities, valencies, parity, array monotonicity, a proved local bound, and the spherical absolute bound. Of 959 integral parameter triples, 159 survive these explicit checks. The finite range does not exhaust the existence question. Elementary arguments exclude all primitive t≤2 and c=1, and reduce t=3 to one nontrivial certificate case.

## 5. Exact triple-intersection obstruction certificates

Built the marginal, zero-coordinate, and vanishing-Krein equations for required base triangles. Floating-point LP was used only to discover candidate contradictions. Exact rational row reduction and equation combinations then produced five independently replayable certificates. The verifier checks every coefficient and the negative constant, checks base-triangle existence, validates 76 actual crown-graph base triples, and rejects mutations of a certificate constant and a multiplier. These establish five array exclusions and finish the independent primitive t≤3 exclusion.

**Stopping point:** five substantive approaches complete. No full result for the problem under the connected/nondegenerate interpretation. The remaining obstacle is realization or a uniform obstruction beyond the current parameter and triple-intersection tests, not an unchecked numerical claim. Freeze for a fresh independent audit; do not mark solved.

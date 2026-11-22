# Independent adversarial audit: literal domino inversion monotonicity

**Verdict: ACCEPTED AS PARTIAL RESULTS ONLY.** The full conjecture remains unresolved. No substantive mathematical error or required correction was found in the exact report and supplement identified below. This audit is not a novelty certificate, global literature-status certificate, or authorization to publish.

## Hash-bound scope

The audited class is the ungridded class

D = Av(1324) ∩ Grid([Av(132) | Av(231)]),

where the grid is a split by position and either cell may be empty. Permutations, not their possible cuts, are counted. Write d(n,k) for its length-n, inversion-k count.

- `domino_1890_analysis/REPORT.md`: SHA-256 `ef8e9aaac99d4b6b845d76e257e51472c172cf0f14e18b61bbaaf7a0773608c8`.
- `domino_1890_analysis/independent_structure.md`: SHA-256 `79ea22171517fdb9d1b7657af644d9369925ed880052109a849a7dc94542ba28`.

The supplementary structural argument is **included**, not left pending. `RECEIPT.json` identifies the reviewed mathematical, computational, and supporting artifacts by byte count and SHA-256. The acceptance applies only to these exact versions and the claims stated here.

## Accepted conclusions

1. D has the exact minimal basis {1324, 15342, 25341, 365241, 465231}.
2. The singleton insertion after the first sum component injects decomposable members of D into D, preserving inversions. It is a bijection between D(n,k) and D(n+1,k) whenever n ≥ k+2.
3. Using the cited Linusson–Verkama injection and its stated domain theorem, d(n,k) ≤ d(n+1,k) for every k ≤ n. The finite cases n ≤ 6 are separately certified by exhaustive permutation enumeration.
4. Direct original-definition enumeration gives all the supplied coefficients through n=11, with total 1,480,089 at n=11. All adjacent-length coefficient inequalities checked in this finite range hold.
5. The permutation 2413 admits no one-point pattern extension preserving inversions and remaining in D. This obstructs insertion-only maps, not arbitrary injections.
6. The cited almost-decomposable map does not preserve D globally. The witness 4723516 → 42835167 is correct, as is the infinite family in the main report. The family fails even in the source's k ≤ 2n−7 range when n ≥ 11.

No assertion of full monotonicity for the unbounded range k>n is accepted. Nor does any map obstruction disprove the counting inequality.

## Mathematical review

### Literal convention and finite basis

The rendered original printed p.285 of *Mini-Workshop: Permutation Patterns*, Oberwolfach Report 6/2024, was visually inspected. It prints the horizontal row [Av(132) | Av(231)] and explicitly requires global 1324-avoidance. The report correctly distinguishes this literal interpretation from a different gridded vertical domino convention. Empty-cell and ungridded-counting choices are declared, rather than attributed to an explicit additional source statement.

For a 132 endpoint E and a 231 start S, a legal cut c is exactly S ≤ c < E. If no cut exists, the chosen occurrences are position-disjoint or meet at their common endpoint/start. Their standardized unions are exactly four length-five orders and twenty length-six orders. The certificate's entire witness set, each forbidden-pattern occurrence, and all one-entry-deletion minimality tests were independently checked. This is an exhaustive bounded-obstruction proof, not an extrapolation from small permutation counts.

### Singleton injection and stabilization

The inserted singleton cannot participate in an inversion with old entries. Hence it cannot be either middle point of 1324 or any point of the sum-indecomposable pattern 231. A new 132 must use it as its first/smallest entry; replacement by an entry in the first component produces the old obstruction at the same ending position. The analogous replacement or later-component argument excludes a new 1324. These observations validate T directly.

Uniqueness of sum decomposition makes the inverse deletion unambiguous. The inequality inv(π) ≥ |π|−number_of_components forces at least two source components and at least three target components in the claimed stable range. An interior component of a 1324-avoider is necessarily a singleton. The inverse therefore covers the whole target, including singleton endpoint-component edge cases.

### Stronger k ≤ n theorem

The supplement's direct inclusion Av(1324,4231) ⊆ D is valid: two obstructing triples give entries x<z<y and u<w<v, with the second triple no earlier than z. Avoiding 1324 forces v<y, and y,w,v,u form 4231. The shared-point case z=w is included.

Its sharper decomposable characterization is also valid. For π=α⊕id_m⊕β, with α avoiding 132 and β avoiding 213, D-membership is equivalent to an increasing-prefix/231-avoiding-suffix split of β. In a 213-avoider this is equivalent to avoiding 4231, by taking the longest increasing prefix and using its last descent when the suffix fails.

The inversion-graph argument has no missing direction: an inversion edge joins every intervening position to one of its endpoints, so connected components occupy position intervals; absence of inter-component inversions then gives the ordered value intervals of the sum decomposition. Cycle rank is k−N+r. The inversion graph of 4231 has cycle rank two, and subgraph inclusion cannot decrease cycle rank of the containing graph.

For an indecomposable source, an f-image with at least three components would have a singleton second component. Deleting it gives a different, decomposable source with exactly the same f-image, contradicting the source theorem's injectivity on the union of its decomposable and almost-decomposable domains. Thus the image has at most two components. At length n+1 with k≤n its cycle rank is at most one, so it avoids 4231 and belongs to D. The decomposable branch is the already-verified T. There is no unproved cross-branch disjointness assumption: all branches use the same published injection.

For n≥7, k≤n implies the required domain bound k≤2n−7. The twenty-eight finite inequalities with 0≤n≤6 and 0≤k≤n were independently matched against exhaustive counts through length seven. This closes the small-case gap.

The cited external dependencies were checked against the retrieved text of arXiv:2604.01143v1, Section 6, Theorems 6.1 and 6.3, including the boundary-deletion priority and explicit F1/F2′/F3′/F4′ formulas. The original 2025 injection theorem itself was not re-proved here. The optional limiting-series observation matches the same source's Section 2 and Proposition 7.6 and is consistent with the supplement's endpoint decomposition.

### Exact negative witnesses

All 25 position/rank insertions into 2413 were independently examined. Exactly two preserve its three inversions: prepending the new minimum and appending the new maximum. Both create 1324. The general zero-new-inversion condition is exactly an isolated direct-sum singleton, so the indecomposable witness rules out all unchanged-pattern insertion-only extensions.

For 4723516, cut 4 is valid. Only deleting its maximum among the four relevant boundary deletions makes it decomposable. F4′ produces 42835167, with eleven inversions, global 1324-avoidance, and a 25341 occurrence in positions 2,3,4,5,6. The input is in D and the output is not, which is the required whole-intersection counterexample.

For π_n=(4,n,2,3,5,1,6,…,n−1), n≥7, the main report's cut, inversion count n+4, boundary-deletion priority, and output formula are correct. Removing n leaves a 132-avoider, so the claimed global avoidance follows. The F4′ output always has the same five-position 25341 obstruction. The condition n+4≤2n−7 is exactly n≥11. The proof is uniform; the independent checker additionally tests every n from 7 to 20.

## Independent computational evidence

`independent_enumerate.cpp` was written separately for this audit. It inserts the new **minimum**, not the maximum, and tests global 1324-avoidance by direct quadruple inequalities and every candidate position cut by direct triple inequalities. It does not use the E/S optimization, the derived basis, or any production module. Heredity and unique minimum deletion establish its completeness.

It reproduces every inversion coefficient, every total, and every two-end-extension-failure count in the supplied tables through n=11. It also directly checks preservation and inversion count for T on all 56,307 decomposable members encountered through n=11. Supplied example permutations were separately checked, without assuming identical enumeration order.

`independent_check.py` uses generic pattern standardization and explicit exceptions, not assertions. It checks the certificate, minimality, all supplied count/log consistency, the two insertion witnesses, the obstruction family, and the source map through two independently written recursive/explicit descriptions. Over all 19,203 1324-avoiders of lengths one through eight, it independently checks the subclass inclusion, decomposable characterization, graph components, and cycle-rank implication. There are 7,106 map implementation comparisons and 5,104 indecomposable-image component checks; no collision or disagreement occurs.

The final production `verify.py`, the exhaustive `independent_smallcase_check.py`, the exploratory `independent_f_test.py`, and the audit checker were rerun in ordinary Python and Python -O. Corresponding outputs are identical. The production verifier reproduces the archived basis certificate and validation JSON byte-for-byte. The independent small-case output likewise matches its archived JSON byte-for-byte. The exploratory map script contains an assert, but no acceptance depends on that assert: the independent audit repeats the relevant conditions using explicit failing checks, including under -O.

The unmodified extended transfer and pruned obstruction-search scripts are supporting experiments, not ingredients of the infinite proofs. Their exact rerun status is recorded in the receipt. In particular, the pruned search is not used to claim completeness or global minimality of its first discovered obstruction.

## Limitations and disposition

No required correction remains for the hash-bound mathematical claims. The original-definition counts, finite certificate, source-dependent restricted-range proof, and explicit obstructions support **partial acceptance only**. Copied source PDFs and extracted source text are inspection inputs, not authored deliverables. The exact verified versions and source-file fingerprints are recorded in the receipt; source text is not reproduced there.

Primary public references: https://doi.org/10.4171/OWR/2024/6 ; https://arxiv.org/abs/2604.01143v1 ; https://arxiv.org/abs/1711.10325 .

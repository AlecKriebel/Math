# Classical upper-bound adversarial audit — PR 1119

**Verdict: PASS; no required mathematical repair found in Sections 1–3.** The claimed canonical tester has polynomial vertex-sample complexity on every nonempty finite input, without knowing its size. Its adjacency-query and total oracle costs are polynomial too. Its finite computation can be exponential; no polynomial running-time claim is needed or established.

This is an independent audit of one approach family, not external peer review or a priority determination. I read the full manuscript first and did not read `MATHEMATICAL_AUDIT.md`, `SOURCE_REVIEW.md`, or other reviewers’ conclusions. No repository, pull-request, tracker, release, or publication state was changed by this reviewer. No other individual was contacted.

## Evidence identity and exact claim

The audited input is `../../inputs/PROOF.md`, 25,005 bytes, SHA256 `1483bcaa29473616799fa9c04937e55fc249bd27e293c45d580af236d38709f3`, supplied revision `786fff9ba06951209e8c1e3bc6114efbfa2c9d16`. I independently checked the proof bytes; I did not authenticate that revision’s Git history.

Let C3 be 3-colorability, A3 the graphs made 3-colorable by removing at most one vertex, and P their intersection with K4-freeness. One changed unordered edge costs 1/n² in the uniform model. The hypotheses under audit are C3 ⊆ P; heredity, extendability, and edge-deletion closure; and a one-sided canonical tester with O(ε^-6 log(1/ε)) sample calls and O(ε^-12 log²(1/ε)) adjacency calls for positive ε, every positive n, sampling with replacement, and unknown n.

The deductions below prove these statements; the reproducible finite checks supplement them. No empirical assumption or black-box colorability theorem is used.

## Independent derivation of Lemma 2

For a proper partial coloring φ on S, let L(v) contain the colors not used by its neighbors in S. Let U contain the vertices outside S with empty lists, and B the other outside vertices. For v in B, define

    δ(v) = min(i ∈ L(v)) |{u ∈ B : uv ∈ E and i ∈ L(u)}|.

Color every B-vertex with a minimizing color and color U arbitrarily. This choice need not give a proper coloring. Instead delete its monochromatic edges. There are none within S or between S and B. At most n|U| edges touch U. Every other monochromatic edge is among the edges counted for its endpoints’ minimizing colors, so their number is at most Σδ(v). Double counting only makes the last bound conservative. This is a permitted deletion repair even though distance allows both additions and deletions. Thus ε-farness from C3 implies

    εn² ≤ n|U| + Σδ(v).

Put W = {v ∈ B : δ(v) ≥ εn/2}. The trivial bound δ(v) ≤ n, together with δ(v) < εn/2 off W, gives

    εn² ≤ n(|U|+|W|) + εn²/2,
    |U ∪ W| ≥ εn/2.

No large-n assumption, divisibility assumption, or bound on |S| was used.

The potential Φ = Σ(v outside S)|L(v)| starts at 3n and remains nonnegative. Coloring v ∈ W with **any** feasible color removes that color from at least δ(v) other nonempty lists; removing v’s own list only helps. Hence Φ decreases by at least εn/2. Choosing a U-vertex closes the branch immediately. Since h = floor(6/ε)+1 is strictly greater than 6/ε, including at an integral boundary, a feasible branch cannot last h steps.

### Conditional union bound with shared blocks

Index all potential nodes by addresses in a complete ternary tree, whether or not those nodes are realized. An address at depth j exists and has its partial coloring determined by the first j sample blocks. Conditional on those blocks, the next block is an independent uniform sequence. Its probability of missing that address’s U ∪ W is at most

    (1−ε/2)^ℓ ≤ exp(−εℓ/2) ≤ 1/(12·3^h).

An unrealized address has failure probability zero. Taking expectations bounds unconditional failure at each address by the same expression. The number of addresses at depths 0 through h−1 is (3^h−1)/2 < 3^h. Summing probabilities proves that any failure has probability less than 1/12. Different nodes may use the very same block; no independence among their failures is asserted or needed.

On the failure-free event, suppose the distinct sampled labels admitted a proper 3-coloring. At each selected vertex, its color would be feasible and would specify a child agreeing with all earlier choices. A U-selection could not occur. This produces a length-h feasible branch, contradicting the potential bound. Every selected vertex lies outside its path’s S, so successive path vertices are distinct even when samples repeat. The proof therefore handles sampling with replacement exactly.

## Structural facts and the all-size tester

A 3-colorable graph has no K4 and needs zero exceptional vertices, proving C3 ⊆ P. Restricting an A3-member to an induced subgraph retains its original exceptional vertex if present; otherwise the restriction is already 3-colorable. K4-freeness is hereditary too. An isolated extension preserves both conditions. Deleting edges preserves both conditions with the same possible exceptional vertex.

Since C3 ⊆ P, distance to C3 is at least distance to P. Consequently ε-farness from P implies ε-farness from C3. Reversing this implication would be wrong; the manuscript uses the correct direction.

Set r = hℓ, N = 12r² and M = ceil(N log(3N)). The actual tester always draws M independent uniform labels, collapses repeats, queries each distinct pair, and decides P on that finite induced graph. The following cases are for the analysis only, so no knowledge of n is needed.

If n ≥ N, each of the first two r-blocks fails to give a non-3-colorable graph with probability at most 1/12. Each of the r² cross-block occurrence pairs has equal labels with probability 1/n. The probability of an intersection between the two distinct-label sets is therefore at most r²/n ≤ 1/12. The union bound, without independence assumptions, gives probability at least 3/4 that both obstructions exist and are vertex-disjoint. One vertex deletion affects at most one obstruction. Their union, and every induced supergraph containing it, lies outside A3 and P. Additional samples or cross edges do not repair either obstruction.

If 1 ≤ n < N, the probability of missing any vertex is at most

    n(1−1/n)^M ≤ n exp(−M/n) ≤ N exp(−M/N) ≤ 1/3

for n ≥ 2. At n = 1 the sole vertex is seen on every draw. On complete coverage the sampled graph is G itself and is rejected if ε-far. The tester need not recognize when complete coverage occurred. The inequalities cover n = N−1, and the large-size argument covers n = N exactly. Also M ≥ 2r because r ≥ 1, N = 12r² and log(3N) ≥ log 36 > 1. Heredity gives certain acceptance for members of P under every sample outcome.

The disjointness requirement is substantive. A six-vertex odd wheel is non-3-colorable but belongs to P by deleting its center. Two wheels sharing a center also belong to P; two vertex-disjoint wheels do not. These adversarial controls were independently checked.

## Parameters, costs and boundaries

For 0 < ε ≤ 1/8, h = O(ε^-1), ℓ = O(ε^-2), r = O(ε^-3), N = O(ε^-6), and M = O(ε^-6 log(1/ε)). If t is the number of distinct labels, t ≤ M, so the adjacency count is at most t(t−1)/2 ≤ M(M−1)/2. The **total** number of oracle calls is at most M(M+1)/2 and hence O(ε^-12 log²(1/ε)). Calling the exponent-6 quantity the total query bound would be incorrect; the manuscript distinguishes the costs explicitly.

Membership of a t-vertex sampled graph in P is decidable by a finite K4 search and enumeration of all possible exceptional vertices and 3-color assignments. This can take exponential time in M. The proof counts oracle access and explicitly makes no polynomial runtime claim. The branching tree in Lemma 2 is an existence proof and does not add query costs to the tester.

| Boundary | Resolution |
|---|---|
| ε = 1/8 | Directly covered; h = 49, ℓ = 902, r = 44,198. |
| ε > 1/8 | Use the 1/8 tester; greater farness implies 1/8-farness. |
| Arbitrarily small positive ε | All parameters remain finite; large constants affect practicality, not the theorem. |
| Distance exactly ε | All necessary distance inequalities are non-strict. |
| n = N | Collision probability bound is exactly 1/12. |
| 1 ≤ n < N | Complete-coverage argument applies uniformly. |
| Repeated sample labels | Collapse before deciding P; the branch construction also selects distinct path vertices. |
| ε = 0 | Excluded by the positive proximity domain. |
| n = 0 | The empty graph is structurally in P. There is no probability distribution on its empty vertex set, so it is not a sampling-model input under the primary definition. |

An optional implementation clarification could specify immediate acceptance of a separately represented empty graph. This is a harmless model convention, not a required repair to the theorem on sampling-model inputs.

## Independent reproducible finite controls

Run `python3 controls.py` and `python3 parameter_controls.py` here. Both use only Python’s standard library; no input audit code was used. Exact machine-readable outputs are retained in `controls_results.json` and `parameter_results.json`.

`controls.py` enumerates all 33,867 labeled simple graphs of orders 1 through 6. Exact coloring search determines C3 and P membership. Shortest-path transforms on the entire edge-edit cube compute nearest-member distance with **both** additions and deletions permitted. Every graph satisfies the asserted inclusion and distance direction. For all 1,099 graphs through order five, a separate minimization of monochromatic edges over all 3-color assignments agrees with the C3 edit-cube optimum.

The program checks 170,827 induced-vertex deletions, 199,509 edge deletions, and 28,658 isolated extensions of P-members. On positive-C3-distance graphs through order five, and on every six-vertex P-member with positive C3 distance, it enumerates all 60,547 proper partial colorings, checks the repair and danger-set inequalities with exact integers at ε = dist(G,C3), and checks all 129,927 feasible W-color steps and their potential decrease. The six-vertex cases add 45,648 states on the K4-free one-exception boundary. These maximal-ε finite controls are stronger than choosing an arbitrary smaller ε on those examples; the general deductions handle every ε.

| Exact adversarial control | C3 | P | What a failed mutation would overlook |
|---|---:|---:|---|
| One odd wheel W6 | false | true | One coloring obstruction does not suffice. |
| Two wheels sharing their center | false | true | Two obstructions must be vertex-disjoint. |
| Two vertex-disjoint wheels | false | false | The amplification conclusion holds. |
| Independent twin blowup of W6, every vertex doubled | false | false | Expanded occurrences differ from the correct distinct-label graph W6, which belongs to P. |

The doubled-wheel control would falsely reject a P-member if repeated occurrences were treated as new vertices; the manuscript explicitly prevents that mutation.

`parameter_controls.py` checks ten high-precision parameter choices: ε = 1/8 and its two nearby rational perturbations; ε down to 10^-12; and parameters above one. It verifies h > 6/ε, the single-address failure bound, M ≥ 2r, the exact collision threshold and coupon-collector exponent using logarithms. Forty exact inclusion-exclusion coupon-collector cases additionally satisfy the union bound. Both programs report PASS.

Finite checks alone do not certify all n and ε; the derivations above supply that certification. A reviewer-only initial idea using just a duplicated wheel center was falsified by the exact solver: deleting a rim vertex makes that graph 3-colorable, so it remains in P. I corrected the control to double all labels. This was a correction to a proposed control, not a manuscript defect. The C++ compiler was unavailable because the host Xcode license had not been accepted; I made no license changes and used Python for every reported result.

## Primary model check

The original question is Problem 5 in Lior Gishboliner’s contribution, joint with Asaf Shapira, physical PDF p.27 / printed p.1139 of [OWR 19/2019](https://ems.press/content/serial-article-files/46798). It compares standard and VDF complexity for extendable hereditary properties. Its preceding definition counts samples and edge queries together and withholds n. The same question appears in [arXiv:1905.09903v5, Problem 5.6](https://arxiv.org/abs/1905.09903v5). Section 1 uses unordered-edge weighted distance and uniform normalization n²; Proposition 5.7 discusses canonical vertex samples. Thus the appropriate conservative polynomial total bound here has exponent 12. I found no runtime requirement in its oracle-count definition. [Version 1](https://arxiv.org/abs/1905.09903v1) already contains the same question and accounting. `SOURCE_LEDGER.md` records versions, hashes and access limits.

## Disposition and exact remaining scope

No unsupported central claim remains within this classical family. Sections 4–7, broad priority research, novelty and final publication disposition are outside this certification. This report alone does not certify the full VDF lower bound or priority of a complete solution.

**Required repairs: none for the audited classical upper bound.** Optional only: an explicit empty-input convention if a separate empty-graph representation is intended.

# Delta adversarial audit: the fixed-P4-graph matching formula

Completed October 24, 2026 UTC; frozen input hashes and the exact time appear in `DELTA_MATCHING_RECEIPT.json`. Audit completion: **100% of this additional lemma's scope**. This is an independent AI mathematical audit, not human peer review, a formal verification, an originality audit, or progress toward a complete resolution of 21.127.

**Verdict: pass.** For the fixed coordinate graph and retained-boundary surface problem stated in `P4_FIXED_GRAPH_OPTIMIZATION.md`,

    alpha = |F| + |U| + |V| - nu(H)

is correct. No substantive objections remain. The finite matching LP computes this fixed-graph relative quantity; it does not compute absolute scl or optimize over arbitrary piece graphs.

## 1. Forced exceptions and the remaining defects

Every target L vertex with nonzero a-charge must remain uncapped, because its incident edges carry only b. Every target R vertex with nonzero d-charge has the analogous obstruction. Thus all m lifts of every vertex in F are mandatory exceptions. These vertices become reservoirs: they are **not removed from the coordinate graphs**. A b- or c-component containing one now has a reservoir and needs no further exception on account of its total charge. This is why the remaining bad components must be entirely contained in D0. Already non-target vertices are also reservoirs and are handled the same way.

After this change, a persistent coordinate obstruction is exactly an all-target tree component with nonzero total charge. The a and d components are isolated vertices and their nonzero cases have all been accounted for by F. The remaining persistent defects are therefore precisely U and V. Zero-total-charge components impose no exception cost. Non-tree components may have finite-stage cost, but their normalized extra cost can be made arbitrarily small by the already audited regular-cover promotion theorem.

## 2. Actual hitting sets and the matching identity

Two different b-components are disjoint, and two different c-components are disjoint. A physical piece vertex can therefore meet at most one node on each side of H. A piece meeting both must be of middle type, and gives the stated edge of H. Parallel edges correspond to distinct available middle pieces and do not alter maximum matching size. A component which has no overlap has at least one piece available to meet it.

The maximum-matching upper construction is valid with actual pieces. Choose the middle piece for every matched edge. For each unmatched component, choose any piece in that component. A genuinely private singleton need not exist: for example, a single isolated middle vertex with nonzero b and c charges belongs to two bad singleton components and has no private choice. Incidental coverage of another component is allowed and only helps. The revised proof now makes this explicit. The construction uses at most `|U|+|V|-nu` pieces and avoids F because every bad component lies in D0.

For the reverse bound, a minimum vertex cover has size nu by the stated alternating-path argument. Its complement is an independent set of size `|U|+|V|-nu`. A physical exception meets at most one node of that independent set, whether it is a genuinely private choice or an overlap edge. This gives the lower bound. Consequently the upper construction has exactly the required minimum size; possible duplicate or incidental choices cannot invalidate it. Isolated H nodes and either empty side of H are covered by the same argument.

The added alternating-path proof of matching/vertex-cover equality is correct: no augmenting path reaches an unmatched right vertex from an unmatched left vertex for a maximum matching. Every matched edge has exactly one endpoint in `(left minus Z) union (right intersect Z)`, and this set meets every edge. It contains no unmatched vertex, so its cardinality is nu. The rational matching LP has this integer optimum; an integral matching and the integral vertex cover give matching primal and dual values.

## 3. Why every cover retains the same normalized persistent cost

The inverse image of a bad tree component in a degree-m graph cover consists of m tree copies, each projecting isomorphically to the original component. In particular, each such copy contains exactly one lift of each original overlap middle vertex. The incidence multigraph H' has one edge for each such lifted middle vertex. At each node of H', the map to H is a bijection of incident edge types. Thus H' really is a degree-m graph cover of H, including isolated nodes and parallel edges. This is stronger than merely knowing that H' has m times as many nodes.

Lift a base maximum matching: its m lifts form a matching of size `m nu(H)`. Lift a base minimum vertex cover: it covers every edge of H' and has the same cardinality `m nu(H)`. Every matching is bounded by a vertex cover, so

    nu(H') = m nu(H).

The hitting-set lower bound applied to H' therefore forces at least `m(|U|+|V|-nu(H))` exceptions beyond the disjoint m|F| already forced. This does not assume that an arbitrary abstract H-cover can be realized by a B-cover; only the actual induced covers are used.

For the upper bound, choose a base optimal hitting set E and keep all lifts of F union E as permanent reservoirs. Every nonzero-charge tree coordinate component now contains an original or permanent reservoir. Applying the prior promotion theorem to the remaining targets produces additional `o(m)` exceptions only for cyclic components, while realizing all other target pieces as actual disks with integral winding choices. Combining the lower and upper bounds proves equality of the infimum. Disconnected covers are allowed, as in the statement. No bounded-winding condition has silently been imposed on the reservoirs.

As an additional consistency check, finite covers of a non-tree component remain non-tree: their first Betti number is `1+k(beta_1-1)` for a connected degree-k lift. Thus no new charged tree defect appears over a cyclic base component. Zero-charge tree components remain zero-charge. These facts explain the exact scaling of the stable formula itself under further covers.

## 4. Nonattainment and ordinary Euler characteristic

Nonattainment is real. Let B have one L vertex and one M vertex joined by two parallel b-edges. Give the L vertex b-charge 1 and a-charge 0, the M vertex both charges 0, and prescribe both as targets. There are no forced vertices and no bad tree components, so the formula gives alpha=0. Nevertheless, every connected lift of the b-cycle has positive total b-charge equal to its degree, and hence at least one exception is necessary in every finite cover. Connected cyclic covers of degree m require exactly one exception and have ratio 1/m, proving infimum zero without attainment. This is the example tested in the author's script.

For the stated relative surfaces, keep all non-target vertices as annuli. A degree-m cover has m paired-turn edges for each base edge and `m|D|-r` capped target pieces. The previously audited interval-gluing calculation gives

    chi/m = |D| - e(B) - r/m.

Taking the supremum gives the displayed Euler formula. It is an identity for ordinary Euler characteristic in this fixed retained-boundary model. No replacement by chi-minus, filling of reservoir boundaries, or conclusion about the absolute-scl infimum follows.

## 5. Independent computation and reproducibility

Run `python3 independent_matching_check.py`. It snapshots the two author scripts inside `matching_reproduction/`, executes the optimization checker there, and requires the resulting JSON to equal the frozen author JSON exactly. This avoids overwriting the author's output and suppresses bytecode artifacts outside the review directory. All original 250 forest brute-force comparisons, 250 arbitrary-cover scaling cases, and 40 cyclic examples reproduced.

The independent code uses union-find component construction, direct exception-subset minimization against all four original coordinate constraints, and a separately implemented unit-capacity network flow. It does not rely on the author's recursive matching routine or forced-vertex reduction for the direct subset check. Results:

- 2,000 general graphs: the formula equals the directly minimized cost of all original charged tree constraints, including a/d singleton constraints.
- 1,000 of those graphs are forests: the same value equals the minimum actual finite-stage exception count, because all coordinate components are trees.
- 400 independently generated permutation-voltage covers: the recomputed stable formula is exactly m times its base value.
- The no-private-singleton example above passes.
- For all 1≤m≤40, the connected cyclic cover example has stable loss 0 and finite minimum exception count 1.

All checks passed. These are finite sanity checks; the preceding mathematical argument establishes the general result. No priority claim has been made for these elementary graph-theoretic ingredients. The unresolved variable-piece-graph encoding and absolute-surface filling gaps remain unchanged.

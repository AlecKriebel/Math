# Independent adversarial audit

2026-10-21. Verdict: **PASS AS A PARTIAL ATTEMPT; ALL THREE RESIDUALS REMAIN UNRESOLVED.** No error changing the report's mathematical disposition was found. No publication or queue change was made. This audit is original analysis; it does not reproduce the source document.

## Mathematical claims

1. **Occupancy rounding is valid.** For an interior chip at coordinate x on a unit edge uv, the divisor u+v is equivalent to chips at coordinates x and 1−x. An integer-slope piecewise-linear function supported on that edge gives this equivalence, including multiplicity when x=1/2. Summing these equivalences establishes an effective divisor dominating D with degree 2d−s. The cited discrete/metric rank agreement for vertex-supported divisors completes the inequality. Rank one guarantees an effective representative containing any selected original vertex, hence s≥1. The proposed occupancy fraction is a sufficient condition only. If a family has ratios approaching 2, then both d→∞ (from the known 2−1/d bound) and maximal occupancy divided by d→0 (from this sharper inequality) indeed follow.

2. **Skewering additivity is valid within the stated source framework.** The skeleton must be connected and simple as in Definition 5.1. At every uniform subdivision m, each block has gonality between its metric minimum b_i and its original gonality a_i. Thus t≥Σa_i remains sufficient for Lemma 5.2 and yields exact additivity at every such subdivision. Choose a common multiple of the finitely many attaining denominators to attain Σb_i. Theorem 1.3 then gives metric equality, not merely an upper bound. The weighted-average ratio cannot improve the best constituent ratio.

3. **Prime-step reduction is valid.** Factoring a witnessing odd integer into primes produces a chain of regular subdivisions; divisibility monotonicity and a strict total drop force a strict odd-prime step. The initial graph can change. This proves an existence equivalence across graphs, not a prime witness for the same graph or a bound on that prime. The report observes both limitations. Its separation of a potential first drop at four from an odd drop is correct. The affine equation 2x=1 correctly defeats an argument from ambient odd-grid density alone.

## Tricycle coverage and bounds

The model has three doubled outer edges, six spokes and three transitions: 15 edges and seven essential vertices. The construction produces exactly 7+15(m−1) vertices in the uniform test, with distinct new vertices on every subdivided edge. Parallel edges are preserved.

The cited Lemma 4.5 concerns arbitrary subdivisions of the minimal tricycle, not merely subdivisions retaining transition lengths one. It therefore applies to both searches. A positive-rank degree-five class has an effective central-reduced representative with two chips at the center and exactly one on each closed transition path. These three paths have disjoint endpoints and interiors. Enumerating their Cartesian product loses no candidate class; allowing non-reduced candidates adds harmless redundancy. Corollary 4.6 excludes all lower degrees.

The six transition vertices are a strong separator even after arbitrary positive integral subdivisions of the 15 edges: every complementary component is a tree, and no separator vertex has more than one edge into any one component. The degree-six divisor supported once on these six vertices therefore supplies the upper bound. Negative degree-five searches consequently certify gonality six, conditional on the cited source lemmas, rather than merely failure to locate a witness.

## Original Dhar implementation

The burning condition uses a strict inequality, as required, and counts parallel-edge multiplicity. Every burned vertex is processed once. For the surviving unburned set U, D(v) is at least the number of incident edges from v into the burned set, so firing U remains effective. The code changes only crossing-edge contributions, exactly implementing set firing. All-burned with a chipless sink certifies a reduced representative unable to reach that sink. Reaching a positive sink chip is an immediate positive certificate. Each target restarts from a copy of the original divisor. All vertices are tested unless a negative target already proves failure. The iteration cap raises rather than returning a false negative. No floating-point calculations occur.

## Independent exact validation

`audit_independent.py` imports neither original script and independently constructs the graphs, preserving parallel edges as repeated adjacency entries. It uses sink-sandpile stabilization, rather than burned sets and complementary-set firing.

For a chipless target q, on nonsink vertices put a(v)=deg(v)−1−D(v). For these candidates this is a nonnegative stable sandpile. Add the sink-boundary vector beta(v), the number of edges from v to q, and stabilize by toppling individual nonsink vertices, retaining integer multiplicities. Repeat until adding beta and stabilizing fixes the configuration. Since every vertex connects to q, this yields the recurrent representative of the sandpile class. Its complement deg(v)−1−a(v) is the nonsink part of the q-reduced divisor. Recover its q coordinate by conservation of total degree; positivity is equivalent to reaching q. This standard recurrent/reduced correspondence is the mathematical foundation of the independent checker. A cap raises on nontermination.

Executed successfully:

- All 3,024 uniform candidates for m=1,…,9. The complete successful-position lists match: none for odd m, and just the midpoint triple for even m.
- All 54 asymmetric length vectors and all three m values, for 162 graph tests. All reported gonality values and first witness positions match exactly. The independent search visited 10,541 candidates in this family, stopping at its first positive candidate just as the original output specification permits.
- `AUDIT_CHECKS.json` records the aggregate result and the uniform successful-position lists. Exit status was zero.

Reproduce from any working directory by running the independent script with its absolute or relative path. It writes its result beside itself. The independent checker is also conditional on the source lemmas for exhaustive candidate reduction and the five/six gonality bounds. It is an independent computational implementation, not an independent full proof of those source lemmas or a formal proof-assistant certificate.

## Minor reproducibility observations and acceptance limits

The original scripts write to paths relative to the repository root. Run them from that root; running inside the deliverable directory will fail when opening output files. Also, importing `check_lengths.py` performs the complete search and rewrites its result because it lacks a main guard. These are packaging concerns, not mathematical failures; the original files were not changed during this audit.

The independent checker validates the recorded results, not the literature-search history. No exhaustive current-openness check or independent full audit of the primary source was performed. No finite exclusion is promoted to a parity theorem, universal sharp ratio, or obstruction to every first drop beyond two. No corrected substantive claim is required. The report's PARTIAL / OPEN RESIDUAL boundary must remain intact.

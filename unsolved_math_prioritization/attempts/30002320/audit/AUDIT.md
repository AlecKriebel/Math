# Independent audit: random-graph coloring growth rates

## Verdict

**PASS for a partial result.** No proof or disproof of the all-density source conjecture is certified. No mathematical correction to the frozen author packet is required. The five research approaches are substantive, and the partial classification and absence of a novelty claim are appropriate.

Reviewed October 3, 2026. The reviewed author manifest has SHA-256 `ba3462a5ffa99f23c5e295a24ba558e2ad74bf857da3b3fa9cca9b14d611038a`. Every listed file matches its recorded size and hash. This review does not authorize publication, repository changes, or a solved classification.

## Source statement

The original defining formula was inspected visually on printed page 1098 of the [official Oberwolfach report](https://publications.mfo.de/handle/mfo/3349), followed by Conjecture 4 on page 1099. The nth root lies inside the expectation: the target is E[Z_k(G(n,m))^(1/n)] for fixed k≥3 and d>0. The catalog's displayed outside-root expression is a consequential extraction error. Its plain-language original statement agrees with the report. The author's simple-graph and floor conventions are explicit and reasonable; they are not represented as a theorem about arbitrary critical-point rounding.

The report's volume year is 2013. The [publisher's page](https://ems.press/journals/owr/articles/12481) gives March 17, 2014 as its publication date. No source PDF, source screenshot, complete extracted source text, or catalog record is included in this audit's public files.

## Proof-by-proof findings

### 1. Outside-root first moment and the strict zero region: pass

For a color-class vector, the allowed-edge count is (n²−Σn_i²)/2. Balanced classes maximize this count and their multinomial multiplicity. The lower multiplicity bound k^n/(n+1)^k is valid because there are at most (n+1)^k types. For m=O(n), each logarithmic factor in the balanced hypergeometric probability is log(1−1/k)+O(1/n), so the total error is O(1). The upper and lower bounds therefore prove the claimed rate k(1−1/k)^(d/2), including the stated k≥2,d≥0 extension and general m_n/n→d/2.

The inequalities P(Z>0)≤E[Z^(1/n)]≤kP(Z>0) are pointwise consequences of integer-valued coloring counts. Jensen's inequality has the stated direction. If d>−2 log k/log(1−1/k), the first moment itself tends to zero exponentially, so Markov proves the expected-root limit is zero. Jensen alone would not prove that conclusion. Equality at this density is correctly left untreated by this argument.

The contrast at k=3,d=6 is exact: the outside-root limit is 8/9 and the source expected-root limit is zero. The binomial-model annealed rate k exp(−d/(2k)) is also correct and differs from the fixed-edge rate. Exponential moments cannot be transferred by the bounded-root coupling argument.

### 2. Subcritical proof: pass

The cycle-plus-path witness count includes the endpoint vertex and handles a path of length zero correctly. With cycle length ℓ and off-cycle path length r, the exact number of such labeled templates is (n)_(ℓ+r)/2: choosing the attachment vertex cancels the cycle-rotation divisor, while the two cycle orientations are identified. All ℓ+r witness edges are distinct. For large n their joint inclusion probability is at most (d′/n)^(ℓ+r), where d<d′<1. Consequently E R≤d′³/[2(1−d′)²] for the number R of vertices in cyclic components.

For each fixed L, a component on s≤L vertices with t≥s+1 edges has an O_L(n^−1) union bound. It is enough to count the presence of the candidate edges; requiring no outgoing edges can only reduce the probability. A larger complex component implies R>L. The bound C/L+O_L(1/n), taking n→∞ before L→∞, excludes all complex components with high probability.

Every tree or unicyclic component is k-colorable for k≥3. On that event the cyclic union has equally many edges and vertices; removing it leaves a forest. Its log-count differs from n log k+m log(1−1/k) by O_k(R). The rare failure event is harmless for convergence in probability, and the uniform bound 0≤Z^(1/n)≤k then gives expectation convergence. This proof cannot be extended to d=1 by the same witness sum or to k=2 by the same colorability step. Neither extension is claimed.

### 3. Prior theorem scope: pass

[Coja-Oghlan, Krzakala, Perkins and Zdeborová, Theorem 1.2](https://arxiv.org/abs/1611.00814v4) applies to every q≥3. It gives the stated deterministic normalized logarithm below the variational condensation threshold and an exponential deficit above it. It does not provide a general limiting entropy above condensation or a boundary assertion. Its Section 4.3 explicitly addresses zero interaction weights. The packet correctly distinguishes this 2018 result from the sufficiently-large-k scope of [Bapst et al.](https://arxiv.org/abs/1404.5513).

[Bayati, Gamarnik and Tetali, Theorems 1–2 and Remark 3](https://arxiv.org/abs/0912.2444) do not justify taking the hard-coloring limit: the finite-temperature theorem requires finite λ, and the zero-temperature optimization concerns the optimum number of satisfied edges. An exponential rate of zero for colorability probability is insufficient to determine its limit. [Ayre, Coja-Oghlan and Greenhill, Theorem 1.3](https://arxiv.org/abs/1812.09691) gives non-colorability bounds, hence additional open zero regions, rather than an all-density hard-coloring entropy limit. The author's bounded literature claim is appropriately qualified. This audit is not a declaration of exhaustive literature coverage.

### 4. Temperature, logarithm, and one-edge controls: pass

The alternating empty-graph/fixed-clique construction has normalized soft pressure tending to log k at every fixed finite inverse temperature. Its hard-coloring root alternates between k and zero. The graph family is deterministic and is correctly not presented as a counterexample in G(n,m).

The count for K_(k+1) with one edge removed is exactly k!: the missing-edge endpoints must share a color and the remaining k−1 vertices must use distinct other colors. Adding the edge annihilates every coloring. Isolates supply the stated multiplicative factor.

For every fixed d>0 and all sufficiently large n, the simple G(n,m) support contains a graph with a prescribed K_(k+1); hence P(Z=0)>0 and the extended E log Z is −∞. This is consistent with a finite normalized-log limit in probability. The nonadditivity example for log(max{1,Z}) is valid.

### 5. Sharp-threshold implication: pass

[Achlioptas and Friedgut, Theorem 1.1](https://cgi.di.uoa.gr/~optas/papers/k-col-threshold.pdf) supplies the two one-sided assertions separated from a threshold sequence by any fixed positive degree gap. It does not assert convergence of that sequence. Low- and high-density bounds keep it in a compact interval away from zero.

For an oscillating threshold sequence and a fixed intermediate degree d, binomial edge-count concentration and the monotone graph process transfer the lower and upper subsequences to G(n,⌊dn/2⌋). On one subsequence F_n(d)→0; on the other liminf F_n(d)≥1. This contradicts convergence at that d. No exponential tail for colorability probability is needed. The conclusion is a necessary condition, not a converse or a solution.

### 6. Conditioning and ensemble transfer: pass

The decomposition F_n=p_n E[exp(S_n) | Z>0] is exact. Conditional entropy convergence to a constant, together with p_n→p, is sufficient by boundedness. If p=0, conditional entropy control is unnecessary. These are sufficient conditions only.

Both fixed-edge/binomial sandwiches have the correct direction. Their errors are bounded by k times an edge-count tail probability. The ±ε slack is essential. It permits transfer where the limiting formula is continuous on a neighborhood, including strictly below condensation, but does not settle an unresolved boundary or discontinuity.

Conditioning on an event whose probability stays positive preserves a deterministic high-probability limit; it does not preserve arbitrary expectation limits. The indicator counterexample is exact. Self-loops must be excluded explicitly for hard coloring because a single loop makes Z zero.

## Independent controls

The author's standard-library script was rerun and its receipt reproduced byte for byte, including its 1,099 enumerated simple graphs and exact value E Z_3(G(6,6))=7560/143.

The separate [audit controls](controls/audit_controls.py) use edge-subset inclusion-exclusion with a subset zeta transform, independently of the author's vertex-color recursion. The [receipt](controls/results.json) records:

- 33,867 simple graphs on 1 through 6 vertices and 101,601 graph/color cases for k=2,3,4;
- 123 first-moment parameter cases, compared with direct enumeration of all vertex assignments, plus balanced-type bounds;
- cycle/path witness domination for all 33,867 graphs and 41 exact expectation identities;
- 9,813 forest coloring identities and 18 binomial-model first-moment identities;
- clique-minus-edge, soft-weight, and annihilation checks for k=2 through 5;
- monotonicity under every available one-edge addition, and numerical finite-root/Jensen inequality checks.

Counting identities use integers or rational arithmetic. Root/Jensen diagnostics use floating point with explicit tolerances. None of these finite controls establishes an asymptotic theorem.

## Release boundary

The supported classification is **partial**. Retain the inside-root statement correction, the restricted domains of all partial results, the prior-work credits, and the remaining all-density and critical-point gaps. The frozen author files need no repair. The audit certifies mathematical scope and reproducibility, not remote workflow history or publication permission.

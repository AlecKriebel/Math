# Independent primary-source audit: family 113

Audit completed 2026-10-07 UTC. This report addresses the upstream mathematical dependency and its actual Lean scope. It does not certify the follow-on gadget, the candidate package, or a global novelty search.

## Finding and coverage

I found no substantive mathematical gap in the pinned classical FPRAS proof after reconstructing its full dependency chain, including the label-cell construction, repairs, signed cancellation, demand recovery, guide conditioning, replica argument, annealing, and bounded-bit implementation. The upstream result therefore does not present an identified mathematical obstruction to deriving a rational weighted consequence by an independently valid polynomial-size reduction.

The actual Lean solution states the substantive finite-machine FPRAS theorem for explicitly encoded simple unweighted graphs. Its source is substantially stronger than a theorem assuming a sampler or count oracle. I inspected the actual declarations and their critical hypotheses, independently inventoried the entire local import closure, and parsed its import headers with the pinned Lean version. **I did not reproduce a kernel check of the theorem or its axiom closure.** The compiled OAI/Mathlib environment is absent, and the direct theorem probe failed before elaboration. Source inspection and successful header parsing must not be described as kernel verification.

I first read the original `research/USER_REQUEST.txt` and the applicable `AGENTS.md`. I did not read prior reviewers' conclusions or reports. I made no candidate changes, installed no dependencies, rebuilt no large environment, contacted no external person, and published nothing. All authored work is in this report's directory. The upstream clone was read-only.

Primary paper coverage:

- FPRAS: read and reconstructed the complete mathematical proof body in `build/main.tex`, from the introduction through the Section 10 sampling consequence. The bibliography was not audited as an independent literature review. I also extracted and read selected passages of the actual pinned PDF: Theorem 1.1; label-adapted quadrangulation and comparability; the cell identity and cancellation; the bounded-bit section; and Lemma 10.2 and its proof. These passages agree with the corresponding primary TeX statements and arguments on inspection. I did not render every PDF page or mechanically prove that the PDF is a faithful compilation of every TeX line.
- Entropy companion: read the introduction, the full central polytope/face-dimension and entropy arguments, the weighted partition-function interface, and the final deterministic algorithm and its guarantee. I inspected relevant actual Lean declarations. The exact optimization machinery, odd-cut recursion, examples, and all appendices were not independently re-proved in full. That limit matters for a comprehensive certification of its deterministic counting implementation; it does not conceal a dependency used by the FPRAS proof.

## Sources and identity

The read-only repository is `/Users/alec/Desktop/math`, pinned at `adc7f1241b42e322a6451854ab7e4b4c146bf78a`. Independently checked remote HEAD and `refs/heads/main` were still this commit at the recorded audit time. This is a point-in-time check, not a promise about later corrections.

The principal primary paths are:

1. `/Users/alec/Desktop/math/preprints/A-Fully-Polynomial-Randomized-Approximation-Scheme-for-Perfect-Matchings-in-General-Graphs-September-23-2026/`, especially `build/main.tex`, `main.pdf`, and its README.
2. `/Users/alec/Desktop/math/preprints/Entropy-and-Face-Dimension-of-the-Perfect-Matching-Polytope-September-23-2026/`, especially `build/main.tex`, `build/sections/`, `main.pdf`, and its README.
3. `/Users/alec/Desktop/math/lean/OAI/Combinatorics/MatchingCount/`, especially `Model.lean` and `Main.lean`; the comparator configuration and `lean/docs/113.md`; and the distinct entropy, triangle-face, and binary-counting solution modules discussed below.

Independent SHA-256 identities:

| Source | SHA-256 |
|---|---|
| FPRAS `build/main.tex` | `dcf28553d442dfc53a9f90f7c52bd48c9e2e7e5e27b197aa7ca4be1c8daed703` |
| FPRAS `main.pdf` | `1510b15725ee7e92a6c543484c6c02ce7f26347a32c1a11cd66c5890b94c6de1` |
| Entropy `build/main.tex` | `8d3d0535b97e175657926d551e6816ea97a38c40a2501bb17e1be3c963a1dde0` |
| Entropy `main.pdf` | `c0b726a089502900b6b0c6b26b3d024cc55c440ce5d4abc71584b2c9ffe2fae4` |
| MatchingCount `Main.lean` | `5baa10d9bacd0be4ea26ae041a8600c9de9391abe8c0836c0ded10143054b100` |
| MatchingCount `Model.lean` | `357b41c991087fcdba5ef7f7170cdc0705d986d3bedd3ca0b4ce115df8611b90` |

`STATIC_PRIMARY_RECEIPT.json` records per-file hashes, import lists, and comparisons with pinned Git blobs and the project's source snapshots. All checked primary preprint files agreed with the pinned originals and snapshots. `PDF_INSPECTION_RECEIPT.json` records the PDF extraction and selected reading. The extracted third-party texts are reading material under `primary_reading/`, excluded by the local `.gitignore`; they are not authored public evidence.

The repository/manuscript READMEs attribute the work to OpenAI and describe the manuscript status. I treated those statements as provenance and caveats, not as evidence that the proof is correct.

## Exact theorem and dependency assumptions

The FPRAS theorem (`build/main.tex:132`, PDF p. 2) takes a finite simple undirected graph and rational `0 < ε < 1`, `0 < δ < 1/2`. It produces a nonnegative rational estimate within relative error ε with failure probability at most δ, returns zero certainly when no perfect matching exists, and bounds **every execution's bit time** by a fixed polynomial in the full input length, ε inverse, and log δ inverse. It includes the empty graph, whose count is one. Odd order and infeasibility are handled deterministically. A sparse encoding with binary vertex count is guarded by `n > 2|E|` before allocating vertex-indexed arrays.

This is an unweighted simple-graph theorem. Positive rational activities and colored edges are explicitly constructed intermediate objects, not a theorem for a succinct input with exponentially many labeled edges. Applying it to rational hafnians needs a separate exact reduction, with construction/decoding bit bounds and correct normalization. Nothing in the theorem itself formalizes that reduction.

The classical argument uses deterministic polynomial-time perfect-matching feasibility, standard finite reversible-chain spectral estimates, finite conditional expectation/orthogonal decomposition, Hoeffding bounds and amplification, and elementary finite-bit rational arithmetic. The specialized hole, cell, energy, and replica arguments are supplied in the paper. I found no call to an unknown approximate matching-count oracle inside the construction of the FPRAS itself. The deletion sampler subsequently calls the proved FPRAS and exact feasibility, which is legitimate self-reduction.

The polynomial degree and constants are extremely large. That limits practical usefulness, not the fixed-degree complexity claim. A theorem-level randomized machine existence result is not a ready-to-run efficient numerical hafnian service.

## Reconstruction of the classical proof

### Holes, path subdivision, and bounded inflation

Write `g(U)=Z(-U)/Z` for even deleted vertex sets. On a positive complete logical graph, vertex scaling gives balanced two-hole rows. The bottleneck similarity `B` is the maximum over paths of their minimum edge activity, with a floor of one. It is an ultrametric; pairing capacity `Φ_B(U)` is the maximum product of similarities in a pairing of U.

The four-hole inequality is proved by overlaying a matching with four holes with a perfect matching, following the alternating path from a specified hole, and switching. The endpoint distinguishes the three possible two-hole products, and switching preserves union edge weight and admits recovery. Thus it does not assume a correlation inequality stronger than the target.

For a strong path, the relocation proof divides by the relevant two-hole row and identifies an injective move of one hole. In its exceptional cases the four-hole inequality bounds the loss. Summing along a simple path costs at most n steps. This gives the small-hole bound needed while the auxiliary weights increase. A continuous interpolation adds distinguished parallel edges of weight `t B/D0`, with `D0=10^8(n+1)^4`; partition and hole derivatives are finite polynomial identities. The bootstrap keeps the rows inside the stated interval and gives partition inflation below two. Inserting the pairing's distinguished added edges then bounds `g(U)Φ_B(U)` for two or four holes. I checked the injective recovery, the exceptional hole cases, and the bootstrap assumptions rather than accepting the final bound alone. See TeX lines 447–707.

Each logical edge becomes a path of length `4p+1`, `p=2K+2`. Adjacent equal path activities are chosen so that one path tiling uses neither terminal and the other uses both; their weight ratio is exactly the original logical activity. Consequently the real-edge partition function is `C0 Z_λ`, and decoding real perfect matchings recovers the logical Gibbs law. The threshold components of the path bottleneck similarities form a tree. A subdivided vertex belongs to one bag or two adjacent bags. Adding bag cliques at height divided by `D=100N^2D0` creates at most two colors per endpoint pair, with controlled adjacent-label activity ratios.

Deleted vertices on a subdivided path must alternate parity for a surviving tiling. The exact deletion identity reduces them to a set R of consumed logical terminals and a product F of local factors; conflicting consumed terminals give an empty family. The threshold characterization of an optimal ultrametric pairing charges neutral interior hole pairs and consumed terminals at every height. This proves `F Φ_{B'}(U) ≤ Φ_B(R)` without enumerating optimal pairings. The two/four-hole bound lifts to the real graph. Summing over partial virtual matchings yields total inflation `I<2`. I checked the parity bookkeeping, away/home terminal factors, and the threshold charge, including activities below one. See TeX lines 708–1260.

A probe portion of activity `1/D` is split off at each logical path center. Revealing all used edges as real has probability `1/I`; revealing the sole probe for `ij` and all other used edges as real gives the two-hole statistic `g_λ(ij)/(DI)`. These are exact counting identities, not an assumed sampling capability.

### Fixed labels, good arcs, leaf repairs, and canonical cells

The label set at a cycle vertex is the set of its **original two incident cycle-edge labels**. It remains fixed after chords are added. A long odd arc is admissible when its endpoints share a label, and is good when its two leaves share a label. Through and interior tilings alternate along the original arc; closing the interior tiling with an endpoint chord gives the closed pattern. A leaf repair replaces the first and last through edges and matches the leaves, freeing both endpoints. The length-three case has distinct leaves, and its repair is an ordinary edge.

For an admissible odd subarc J, its exterior is the complement in the full original cycle. The recursive splitting argument (TeX lines 1373–1527, PDF pp. 18–20) is exhaustive:

- If the exterior is good, choose a common endpoint label P. If P never occurs along J, both endpoint-adjacent labels are the same neighbor Q of P, and Q replaces P. An odd occurrence of P permits a short middle side. If all occurrences are even, the first positive occurrence or last nonterminal occurrence permits a short middle side using the same-neighbor tree fact. If both boundary labels are P, both outer sides are short.
- If the exterior is bad, one exterior leaf lacks P. Reverse J when necessary to place it at the initial endpoint, forcing the initial label of J to be P. If the terminal label is also P, both outer sides are short. Otherwise, after the last P, the suffix avoids P and starts and ends at the same neighbor Q. The parity of that last occurrence supplies one short outer side and a good other outer side.

This creates admissible odd child arcs and guarantees a good opposite pair; when one opposite pair consists of two long arcs, the other pair is good. Recursing with the original fixed sets and full-cycle complements gives noncrossing cells, `(m−2)/2` cells and `(m−4)/2` diagonals. A chord can use any common endpoint label, consistently in its two occurrences; the auxiliary splitting witness need not be that label.

Every boundary edge is within one tree step of its side chord, and every repair within two. The four chord labels have diameter at most two. The whole local edge collection therefore has diameter at most six and activity ratio at most `3D·2^6 ≤ A0=1000D`. A common positive clamp preserves this ratio. This checks the local constant without assuming that all activities on a long arc are comparable.

### Signed cancellation, recovery, and rare guide events

The pair chain proposes local switches, color changes, and exchanges of whole discrepancy cycles between two coordinates. Symmetric proposals and Metropolis capacities yield the elementary switch/color/swap energy bounds. Cycle exchange has acceptance one in the equal-tier pair because it preserves the union weight. Long-arc conversions used in the proof are algebraic comparison terms and do not need to be chain transitions.

For a cell, let `D_C=f(O0)−f(O1)`, `Δ=f(A_P)−f(A_Q)`, and `g_J` be the canonical gain for converting one side arc. Convert an ordered opposite pair `(Y,X)` first at Y, then X; the second gain acquires a context error `E_{Y,X}`. Subtraction gives exactly

`D_C = Δ + Σ_{J∈P} g_J − Σ_{J∈Q} g_J + E_P − E_Q`.

For complementary arcs on an interior diagonal, the converted matchings coincide, while their original orientations differ. Their signed gains therefore sum to **D_C, not zero**. Boundary short sides have zero gain. Since the number of cells exceeds the number of diagonals by one, summing the cell identities yields `D_C=Σ_cells(Δ+E_P−E_Q)`. This is the pivotal cancellation; a zero-cancellation interpretation would be wrong. See TeX lines 1681–1848 and PDF pp. 22–24.

The switch encoding uses `A_P` in the first layer and a guide assembled from all through arc patterns, repaired on a good opposite pair. The input/output union multisets differ by at most four additions and four deletions, all in the comparable local edge collection, so the demand/output mass ratio is at most `A0^4`. For an error demand, the guide contains both closed patterns `C_X,C_Y`; exchanging `T_Y` and `C_Y` between layers supplies the second context without changing union weight. The good-other-pair condition is exactly what supplies repairs when X and Y are long.

Recovery records the four ordered corners, orientation, colored added/deleted edge occurrences, and finite flags. Undo the union edits; the discrepancy component at the distinguished corner is C, and its orientation recovers both inputs on C. Outside C the output layers have not changed. The deterministic quadrangulation identifies the cell. Thus the tag count is a genuine finite preimage bound, comfortably below `(10N)^30`; it is not an unsupported congestion assertion. Repeated demands remain repeated and are counted by tags. See TeX lines 1849–1974.

The error bound retains the fact that the guide contains the particular closed pattern X. If `p_X` is that guide-event probability, fixed-context demand mass is bounded by `A0^4 T π(A) p_X`. Conditional Jensen introduces `1/p_X`, which cancels this mass factor. There is no needed polynomial lower bound on a rare guide event. Through and closed patterns differ on a genuine entire alternating discrepancy component; the swapped set is not merely a segment of a larger component. Counting chord/direction marks bounds the swap sum. These facts give the error-demand energy bound and, with the signed identity and the weight-preserving cycle telescoping involution, the pair Poincaré constant `L=(10^4ND)^100`. See TeX lines 1975–2136.

### Unit refresh and replicated adjacent tiers

At unit activities, colored bag matchings are in bijection with assigning each vertex to one of its one or two bags and pairing the vertices assigned to each bag. Distinct child interfaces are disjoint. The dynamic program conditions on the number k of fixed parent-interface vertices assigned into the current bag, chooses each child's interface subset, and multiplies the child counts and a clique-pairing count. Polynomial convolution over total selected interface size avoids an exponential enumeration over children. Counts have `O(N log N)` bits. Completion-weighted sequential choices define an ideal exact refresh; the finite implementation later approximates those choices with a budgeted fixed grid. See TeX lines 2164–2245.

Common clamps at successive levels differ by a density factor at most two. The construction uses `q=32L` replicas per tier and a lazy scan of adjacent upper/guide pairs plus base refreshes. The local pair inequality applies first to additive pair functions. It is then lifted to arbitrary functions of the complete replica product by martingale differences and product ANOVA. Ordering upper slots before lower guide slots is essential: a residual component is identified by its last and penultimate slots, so distinct permitted pairs' residual components are disjoint. Their total squared norm is bounded by the whole variance. Averaging over q guides absorbs the `8L/q=1/4` residual contribution. This proves a product-chain gap; it does not assume that an additive pair bound already controls arbitrary product functions. See TeX lines 2246–2419.

The explicit minimum stationary-mass bound and lazy spectral contraction give a deterministic polynomial number of steps from a known real matching in every slot. No initial upper-tier stationary sample is assumed. The tree-bag sampler requires positive activities and the stated tree geometry, but no logical row-balance hypothesis; row balance is used for inflation/statistical success elsewhere.

### Annealing, failed histories, and bit cost

Nonedges of the original graph receive `b^(−j)`, `b=1+1/n`; a polynomial number K of stages makes their remaining contribution at most `ε/32`. Original-edge weights remain one. All logical activities stay positive. Vertex scales cancel as one common factor per perfect matching, while the observable ratios telescope the unscaled partition functions. The all-real, reweighted all-real, and single-probe observations are bounded in [0,1] and have the exact required means.

Each stage estimates the partition ratio and two-hole matrix with fresh runs. The matrix is floored/clipped, denominators have explicit zero conventions, and a symmetric one-pass maximum update restores the row balance on the accuracy event. Tightness witnesses persist through later coordinate decreases. Hoeffding, union bounds, and fresh-run total-variation couplings bound the probability of the **first** unsuccessful stage, avoiding an assumption that adaptively sampled stages are independent. The product estimate and small nonedge padding give a successful trial with probability above 0.9; an odd number of independent trials and their median give failure δ. See TeX lines 2525–2842.

The full bit claim is not inferred just from this success event. Section 9 supplies unconditional activity caps and conventions for all failed histories. Nonzero observation values are powers `(n/(n+1))^a`, with common denominator `(n+1)^(n/2)`, so empirical ratios have a polynomial bit bound independent of accumulated scales. A maximum update selects a single predecessor; following its dependency moves strictly backward in update order and gives a chain of at most n factors, rather than an exponentially branching arithmetic expression. Accumulating K stages still has polynomial bits. Bottleneck entries select existing rational activities by max/min; path profiles add bounded powers of two; clamps have rational powers with polynomial bit lengths.

Each categorical choice uses exactly k fair bits and cumulative rational intervals; its variation error is at most `2r·2^(−k)`. Zero-weight outcomes have empty intervals and are never chosen. Polynomial bounds on the number of choices and options allow a common k chosen by doubling. Coupling the rounded choices with the ideal chain adds at most ξ error to the ξ mixing error, within the conservative `3ξ` budget used earlier. There is no rejection loop or convergence-based stopping rule. Schoolbook arithmetic and Euclidean reduction, polynomial-size states/tables, fixed loop counts, and amplification give a fixed polynomial bound on every random tape. I checked the output bit bound on failed calls as well as successful ones. See TeX lines 2843–3079 and PDF pp. 37–40.

## Sampling consequence relevant to the rational follow-on

Lemma 10.2 (TeX line 3203, PDF pp. 42–44) gives an explicit unweighted deletion sampler for explicitly listed simple graphs. Exact feasibility tests ensure every selected child is feasible, including forced branches and failed count estimates. When both children are feasible, two fresh FPRAS estimates determine a ratio, with a zero-sum fallback and a fixed dyadic floor. At most the original number of edges decisions occur.

With `η=γ=τ/(8m*)`, successful ratio error is at most `η/(2(1−η))`, conditional count failure at most `2γ`, and rounding at most `2^(−t)≤η`. Coupling at each adaptive history bounds total variation by `m0·4η≤τ/2<τ`. Count-call time bounds also bound failed output lengths, so exact ratio/floor arithmetic remains polynomial on every run. The sampler always returns a valid matching on feasible input; it does not claim exact uniformity or pointwise multiplicative probabilities.

For a weighted reduction, deterministic decoding cannot increase variation. Uniform gadget perfect matchings must project to the target weighted law by an exact fiber-count identity, not simply by feasibility preservation. A rational consequence should also preserve exact infeasibility via the positive-support/gadget feasibility test. Certain output zero on infeasible inputs does not mean that a randomized count output of zero on a feasible input is an exact feasibility oracle.

## Entropy companion: what it contributes and what it does not

For a loopless labeled multigraph on `2m≥2` vertices and a feasible mean x, the companion's pointwise result is

`F(x)−(2−2/m)B(x) ≤ H(x) ≤ F(x)`,

including boundary means and parallel-edge labels. `F=−Σ x_e ln x_e`, `B=−Σ(1−x_e)ln(1−x_e)`, and H is maximum matching-law entropy at mean x. The case m=1 is equality; empty order is handled separately.

I reconstructed the central argument rather than treating entropy as an assumed bound. The polytope proof contracts a nontrivial tight odd cut and glues matching laws by their common cross-edge probabilities. Without such a tight cut, independent degree columns at an extreme point reduce components to forced matching edges; even-cycle dependence and the odd-component cut constraint exclude alternatives. For face dimension, compatible contracted directions impose at most `|C|−1` independent gluing constraints because both crossing sums are zero. The induction closes the support codimension bound `s−d≤3m−2`. Zero coordinates and forced-one edges are reduced before using fractional support, so a boundary point is not silently treated as interior.

Entropy continuity and a positive maximizing law on the relative face permit a finite exponential-family parametrization on its true tangent space. Its covariance K has image the face directions and rank d. At a positive maximum of the putative defect with coefficient `c>2−2/M`, stationarity cancels acceleration terms in the second derivative along exponential curves. Summing the positive covariance eigendirections gives

`0 ≥ d + tr(KD) = d−s+(c+1)m`,

using `K_ee=x_e(1−x_e)` and `D_ee=−1/x_e+c/(1−x_e)`. The support codimension bound and `m≤M` make the right-hand side strictly positive for `c=2−2/M+ε`. Passing to the endpoint gives the lower bound. The upper bound follows from the star/edge entropy chain rule (Shearer). I found no unsupported ambient invertibility or missing endpoint/boundary argument in this chain.

For finite real β, Section 6 (`build/sections/05-weighted.tex`, PDF pp. 19–20) defines `Z_β=Σ_M 2^(β·1_M)` and `q*=max_{x∈P}[F(x)/ln2+β·x]`. Finite Gibbs variational duality gives

`q*−(2m−2)/ln2 ≤ log2 Z_β ≤ q*`.

This is an additive logarithmic approximation of order n. It neither supplies a numerical optimizer by itself nor gives arbitrary relative ε approximation. The separate exact arithmetic algorithm for binary nonnegative integer pair multiplicities returns an integer A with `N/512^n≤A≤N`, exact zero detection, and polynomial input/output bit lengths without expanding parallel copies. This is a coarse deterministic approximation, not the rational weighted FPRAS headline. The singleton-loop appendix uses a different matching convention and a further coarse factor; it is not a hafnian diagonal contribution under the ordinary perfect-matching definition. I have not fully independently certified every optimization/odd-cut/appendix implementation lemma, and the report does not use that algorithm as a premise for the FPRAS consequence.

## Actual Lean declarations and limits of verification

`lean/ComparatorChallenges/MatchingFPRAS.json` selects `OAI.Combinatorics.MatchingCount.Main` and `OAI.MatchingFPRAS.thm_main`. The placeholder comparator file has an intentional unfinished proof; the actual selected solution at `Main.lean:21` proves `MainStatement` by obtaining a fixed machine/time bound from `LiteralPhysical.mainTime_bound` and the output/success theorems for `LiteralPhysical.mainProgram`. The comparator's permitted axioms are `propext`, `Quot.sound`, and `Classical.choice`; this configuration is not a successfully computed axiom list.

The semantic definitions are in `Model.lean:8–106`:

- `GraphInput` has n and a finite set of pairs of vertices with increasing endpoints, so the public theorem's graphs are simple, loopless, and unweighted.
- `Perfect` requires exactly one incident chosen edge per vertex; Z is the finite perfect-matching count, including the empty graph.
- The alphabet is `Fin 8`; naturals use binary numerals/delimiters, and reduced rational numerator/positive denominator are encoded explicitly. The graph input is sparse and sorted.
- `RandomMachine` has one finite transition table. A nonhalting tick is a single tape write or move, or detects halt; halting is absorbing. There is no unit-cost arbitrary integer/count/sampling operation hidden in the machine definition.
- `timeBound` is `C*(inputLength+ceil(ε⁻¹)+clog2(ceil(δ⁻¹))+1)^d`, with fixed C,d and `C>0`.
- For every valid input and **every** bit prefix of that length, the machine halts and writes a nonnegative rational. If Z=0 every prefix writes zero. The finite fraction of good prefixes is at least `1−δ`. Thus the confidence claim is actual uniform fair-bit counting, and the time claim includes failed tapes.

I traced `Machines/Wrapper.lean`, `Probability/MainLaw.lean`, `Complexity/PhysicalCost.lean`, and `Algorithm/Algorithm.lean` to the actual program and physical cost chain. The implementation uses a final positive-certificate guard instead of importing the paper's external Edmonds feasibility algorithm. `Algorithm/GuardProbability.lean` and `Tapes/GuardBits.lean` show how a positive observable certifies an original-graph matching, is identically zero for zero count, and has adequate chance on a balanced positive instance. This is a distinct implementation of certain-zero behavior with the same theorem semantics; it is not a disguised count oracle.

Critical source anchors inspected include:

| Mechanism | Actual declaration/source |
|---|---|
| Original-label odd-arc splitting and quadrangulation | `Graphs/ArcData.lean`, `Graphs/LabelCycle.lean`, `Graphs/Sets.lean:150,181` (`CycleData.quadrangulate_arc`, `quadrangulate`) |
| Cell identity and complementary-arc cancellation | `Sampling/Sewn.lean`; `Sampling/ChosenChord.lean:89` (`sum_cells_identity`) |
| Actual input recovery and finite tags | `Sampling/PM.lean:83,110` (`DemandEncoding.code_recovers`, `finiteCode_recovers`), plus actual constructions in `Graphs/Cycle.lean` |
| Closed-guide event, activated whole component, and error load | `Sampling/Through.lean:252,431` (`error_demand_load`, `ActualErrorDemand.context_load`) and its `PatternCode`/activation lemmas |
| Pair variance from real tree/weight hypotheses | `Probability/Variance.lean:252` (`CellDemands.pair_energy_inequality`) |
| Replica residual argument and concrete instantiation | `Probability/LocalVariance.lean:168` (`replica_gap`); `Machines/TreePairProposal.lean:126,179,389` |
| Fixed finite physical machine output and confidence | `Probability/MainLaw.lean`, `Complexity/PhysicalCost.lean`, `Main.lean:21` |

The pair-energy theorem's hypotheses require actual one/two adjacent bag memberships, acyclic label graph, positive heights with adjacent height ratio bounded, D at least one, the stipulated activity bounds, and a common clamp. It concludes a variance bound for the actual Gibbs law and pair kernel. A general local-pair hypothesis in `replica_gap` is instantiated from this theorem in the concrete ladder; it is not left as the global theorem's central missing premise. The formal tag presentation includes an additional anchor, producing a slightly looser polynomial bound than one paper count, still well within the chosen exponent. Some helper modules are generic or legacy infrastructure; inspecting their names is not a substitute for tracing the actual instantiation.

The static independent scan found all **415 MatchingCount modules, 66,246 lines**, in Main's local import closure, with no missing OAI imports and all identical to pinned blobs. After removing nested block and line comments, it found none of the scanned tokens `sorry`, `admit`, `axiom`, `unsafe`, `native_decide`, `implemented_by`, `extern`, or selected kernel-bypass tokens. This is a bounded lexical check, not a complete metaprogram-security audit, verification of external Mathlib, or proof elaboration. It does not certify every possible tactic/macro implementation.

Installed Lean `4.34.1` matches `lean-toolchain`; the manifest pins Mathlib to `d13f23b723b8a846827a245b89c10fc7d3f11612`. The authored import-header parser, using Lean's parser, accepted all 415 headers. It parses headers only. The direct authored `AxiomProbe.lean` failed with `unknown module prefix 'OAI'`; its search path contained only the standard toolchain library. No `#check` or `#print axioms` result was obtained. I did not fetch Mathlib, compile the source closure, invoke the comparator successfully, or establish that the reported proof is accepted by the kernel. These exact outputs are preserved in `LEAN_PROBE_RECEIPT.json`.

The entropy formalizations must also be distinguished:

- The older `OAI.Combinatorics.PerfectMatching.Main` theorem in namespace `OAI.MatchingEntropy` is the coefficient-eight comparison. It is not, by itself, the sharp `(2−2/m)` theorem.
- The refined solution is selected separately by `ComparatorChallenges/MatchingEntropyBounds.json`; `OAI/Combinatorics/MatchingEntropy/Pointwise.lean:18` has `OAI.MatchingEntropyBounds.Refined.pointwise_entropy`, with finite loopless labeled graph, `m>0`, vertex count `2m`, nonempty matching family, and x in the actual matching polytope. Its bound is the refined pointwise one, with downstream weighted variational consequences. I read these source statements and central proof calls, but did not kernel-check them.
- `OAI.Combinatorics.TriangleFace.Main` proves the selected triangle-expansion/minimal-face correspondence. That selected theorem should not be advertised as a kernel certification of every sharp global face-rank statement in the paper.
- `OAI.Computability.MatchingCount.BinarySolve` has `OAI.BinaryMatching.deterministic_approximate_counting`, asserting an actual finite-machine polynomial-time coarse binary-multiplicity count with `A≤N≤2^(9n)A` and exact-zero behavior. It is not a weighted FPRAS.

The broad catalog `formalization.yaml` did not list the MatchingFPRAS solution in the inspected search, whereas the actual comparator configuration and solution files do exist. I treat this as a catalog/selection detail, not as a missing mathematical theorem or proof of its certification.

## Independent finite falsification checks

`independent_cells.py` is authored from the primary TeX construction, not copied from the upstream program or a prior reviewer. It retains the original vertex-label sets, uses full-cycle complements, implements all good/bad-exterior splitting families and reversal, and alternates permitted common-label/repair choices. It checks admissibility, parity, both good-pair conditions, noncrossing recursive coverage, cell/diagonal counts, complementary occurrence consistency, legal through/closed/repair matchings, switch and error-guide encodings, the at-most-four union edits, and guide containment. Single-cell and global identities are checked exactly as coefficients of formal matching-value symbols, so the test is independent of a particular numerical function f.

The bounded sweep exhausted closed label walks of even length 4, 6, and 8 on five small tree families, and added 2,000 seeded cases on random trees with longer even cycles. It passed:

- 9,958 cycles (7,958 exhaustive, 2,000 seeded);
- 50,686 cells and switch encodings;
- 11,554 long-opposite-pair error encodings;
- all splitting families, including 4,634 bad-exterior cells and 2,513 reversal cases.

The maximum observed local label distance was four; the general proved bound remains six. These checks are corroborating finite evidence, not a proof of all trees/cycles or an implementation of the FPRAS. Their deterministic seed, script hash, and result are in `INDEPENDENT_CELL_RECEIPT.json`.

## Review implication

Within this assigned scope, the reconstructed classical proof supplies the upstream simple-graph count and total-variation sampler with the required bit guarantees; no substantive unreviewed central premise was found that blocks the intended rational consequence. That is a mathematical source-audit judgment supported by reconstruction and bounded attacks. It is not a kernel-success claim, proof of the follow-on gadget, or complete novelty certification.

A package may honestly state that it is a classical consequence conditional on/using this pinned upstream theorem and separately establish its exact reduction. It must keep the upstream attribution, simple-input theorem scope, sampling variation scope, and the unreproduced Lean-kernel status explicit. The exact remaining formal verification task is to elaborate the pinned actual solution with its pinned dependencies and inspect the accepted theorem/axiom output; that task was not performed here.

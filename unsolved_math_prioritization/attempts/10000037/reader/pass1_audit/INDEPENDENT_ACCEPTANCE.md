# Independent adversarial acceptance: opposite-quadrant percolation counterexample

14 October 2026 UTC. Authored mathematical audit of the exact files pinned below. This is an acceptance of a self-contained proof, not a certificate of historical novelty.

## Verdict

**ACCEPT.** The canonical manuscript proves that the universal full-supercritical uniqueness statement, in the recovered general-graph Bernoulli-bond quasi-isometry interpretation, is false. Its explicit deterministic graph G is infinite, connected, countable and simple, has maximum degree four, and is quasi-isometric to the nearest-neighbor square lattice with the source's single constant C=100. It satisfies

- p_c(G) <= 9/10 < 19/20;
- P_(19/20)(N_infinity >= 2) > 2200741829/6461571200 > 1/3.

The same witness refutes the stronger all-parameter at-most-one normalization. This implication does not need a separate critical-parameter example, and the manuscript makes no claim of critical nonuniqueness. The one-dimensional endpoint is handled separately and correctly: bounded-degree connected graphs quasi-isometric to Z have p_c=1, no infinite cluster almost surely at each fixed p<1, and one infinite cluster at p=1.

No remaining mathematical gap was identified in the canonical proof. Acceptance binds the exact bytes below; an edited manuscript needs its own change review and new pin.

## 1. Frozen artifacts and authority of the proofs

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| CONSTRUCTION_PROOF.md | 14070 | `731c8569a73f275c857991a4f97b47ee6debc2d3d46bb2399134021f65804f60` |
| PROBABILITY_AUDIT.md | 13211 | `22398f4ee4bd31e62a97be74db6b64f9b803ec1d9aea04749d303a5eb5dae7c4` |
| GEOMETRY_AND_ENDPOINT_AUDIT.md | 18186 | `81bba1a9d4dd8bd5e8e5440a706abb3ac2ca3c98c66ebcf06b71141f4293fbd6` |
| INDEPENDENT_VALIDATION.md | 11204 | `a2b0dd835fd7fc4ddc3d3d7f1de6144a67bb6c231f6e1911a24028e914fa4410` |
| validate_construction.py | 14650 | `b43bbff8c330525f385b202711acc528a44ef405e217625682fa6c9415acb9b5` |
| validation_report.json | 3022 | `699ccdc94cddbd0d7d7b5de549c6c2da6a926cb9b0264fd8e451603f7959a633` |
| SOURCE_SCOPE_ADJUDICATION.md | 10629 | `35b832e8e5ce7b253bec16e3266347f0e6e5a92d96a2bde7acb0272046b3b31d` |
| SOURCE_METADATA.json | 6452 | `7075ad1ca6e42d847b9e1eb5f286ea04d0c7148c7ec41ff4eb303135e7cf42f6` |

`AUDITED_INPUTS.json` repeats these pins in machine-readable form. The canonical theorem is governed by Section 4 of `CONSTRUCTION_PROOF.md` and Section 2 of `PROBABILITY_AUDIT.md`, which use the finite-graph parity proof described below.

**Version clarification.** Section 8 of the pinned `GEOMETRY_AND_ENDPOINT_AUDIT.md` records a cross-check of an earlier boundary-tracing presentation. That paragraph is a historical cross-check, not the governing survival proof in the accepted edition. The canonical proof and revised probability audit replaced that presentation by a fully explicit parity argument. The geometry report is retained unchanged so its version history is not silently rewritten. Its metric, gadget, bridge, and one-dimensional results are separately checked here.

During adversarial review, the probability audit was also clarified to apply closed-edge probabilities only to eligible quadrant dual paths. Counting arbitrary paths is solely an upper bound on their number. The accepted probability pin above incorporates this clarification. It is not the earlier probability-report hash.

## 2. Source fidelity and scope

The source is Itai Benjamini, *Coarse Geometry and Randomness*, author manuscript dated 30 October 2013, Open Problem 9.6, printed/PDF page 64, with the [preserved author-hosted manuscript](https://arquivo.pt/noFrame/replay/20201231041548id_/http://www.wisdom.weizmann.ac.il/~itai/stflouraug24.pdf) as the inspected primary source. Its retained PDF identity is 1,101,523 bytes, SHA-256 `aaab65b3acf65f4d21657da94464e9d5edb93969a4c353805099a220a0717cfe`.

This audit independently checked the extracted text of pages 5, 9, 32–33 and 63–65, and visually inspected the retained renders of pages 9, 63 and 64. The source's rough-isometry definition allows uniform multiplicative and additive distortion. The problem does not state a transitivity, quasi-transitivity, periodicity or stationarity requirement. The chapter sets the discussion in the supercritical regime. The graph conventions and the common-parameter independent bond model are consistent with the submitted construction.

The problem sentence itself does not explicitly state the parameter quantifier or an almost-sure qualifier. Accordingly, the accepted negative answer is expressly to the contextual full-supercritical formalization; it must not be described as refuting an express all-p quantifier printed in that sentence. The stronger all-parameter normalization is separately false by the same example. This construction does not refute a merely sufficiently-high-density uniqueness assertion: such an assertion may have a threshold depending on G.

The manuscript's dimension-two witness is enough to negate a statement quantified over all positive dimensions. It is not presented as a dimension-one counterexample. The source has not been silently restricted to additive-only rough isometry, transitive graphs, or site percolation.

## 3. Graph, metric, and iid-model audit

The graph retains internal edges of the opposite northeast and southwest quadrants and replaces every other lattice edge by a path of exactly 100 actual edges. Different paths have disjoint internal vertices. Original vertices have degree four and inserted vertices degree two; there are no graph-theoretic parallel edges or loops.

Projection to the nearer original endpoint is surjective and 1-Lipschitz from G to the lattice. Each inserted vertex is at distance at most 50 from its image, and an original lattice path lifts at cost at most 100 per step. Thus

    d_Z2(f(x),f(y)) <= d_G(x,y)
      <= 100 d_Z2(f(x),f(y)) + 100.

These estimates imply the precise source-convention inequalities with C=100. Both constants are global. No unbounded subdivision or location-dependent metric constant is hidden.

Every actual edge has the same independent Bernoulli parameter p. A coarse weak edge is open precisely when all 100 actual edges in its path are open, so its effective probability is p^100. Effective edges are independent because their actual edge supports are disjoint, even when they share endpoints. This explains the inhomogeneous effective process without changing the requested iid model.

Open connections between original vertices correspond exactly under compression and expansion. Internal vertices cannot create a bypass because they have degree two. Every infinite actual cluster contains infinitely many original vertices: finitely many original vertices meet only finitely many finite gadgets. Thus no extra infinite cluster can be hidden entirely inside partially open replacement paths, and the infinite-cluster correspondence is valid.

## 4. The decisive quadrant lemma: no boundary-tracing gap

Let C be a finite subset of the nonnegative quadrant containing its corner. Form the finite graph D of dual edges crossing primal quadrant edges with exactly one endpoint in C. At each interior dual vertex, the membership indicator changes an even number of times around the four primal corners; its D-degree is 0, 2 or 4. Every incident bottom or left boundary vertex has degree one.

Along the bottom primal ray, membership begins at one and is eventually zero. There are therefore an odd number of bottom boundary endpoints in D. Some component has an odd number of them. The handshaking lemma forces that component to have an odd number of left endpoints as well, since all interior degrees are even. It contains a simple path between a bottom endpoint (i+1/2,-1/2) and a left endpoint (-1/2,j+1/2). No other boundary vertex can be internal to this path because boundary degrees are at most one.

The path length n is at least i+j+2, hence at least two. Every edge crosses a distinct primal boundary edge when the path is simple. For a finite open cluster, those edges are closed. This argument explicitly handles disconnected C, holes, corner contacts, repeated exterior-boundary vertices, multiple axis contacts, and degenerate boundary runs. It invokes neither an unproved simple-polygon statement nor independence between a random cluster and its own boundary.

For fixed n, there are at most n eligible starting positions and at most 4*3^(n-1) self-avoiding paths from each. Only eligible paths receive probability (1-t)^n; arbitrary dual paths merely overcount their number. The union bound from n=2 yields 102/245 at t=9/10, so the quadrant corner survival probability is at least 143/245. Every claimed equality in this geometric-series calculation was independently recomputed exactly.

## 5. All possible bridges and independence

Any finite open connection from A to B can be shortened, stopped at its first B vertex, and started at its last preceding A vertex. The retained subpath has no internal A or B vertex and consists entirely of weak edges. This handles arbitrarily many earlier strong excursions, paths through either other quadrant, large detours, and every finite connection between the two prospective infinite clusters. Connectivity never requires a path through infinity; being in the same component supplies a finite path.

Every such weak bridge starts at (1,n) or (n,1), n>=1, and has length at least n+3. Counting each corner twice is harmless. Summing all eligible self-avoiding weak paths gives

    P(W) <= (8/3) (3q)^4 / (1-3q)^2,  q=p^100.

The distance grows with the start's location, so this global sum converges. This is the feature absent from a flawed uniform-width strip or parallel-half-plane barrier argument. The estimate does not assign q-probabilities to strong edges and does not assign q raised to walk length to repeated-edge walks.

At p=19/20, the binomial block inequality gives q<1/32; consequently P(W)<27/107648<1/1000. The within-A survival event, within-B survival event, and W are measurable with respect to three disjoint actual-edge families. Their full sigma-fields are independent, including the infinite events.

On simultaneous survival and W-complement there are at least two infinite actual components. Multiplication gives the strict lower bound in the verdict. The proof does not assume deterministic cluster count, the transitive 0/1/infinity law, uniqueness monotonicity, or any rough-isometry invariance theorem.

Survival was established at the smaller p0=9/10, not only at p=19/20. This supplies the essential strict inequality p_c<p. Root independence follows from opening a finite connecting path, using positive association; it does not require transitivity.

## 6. Dimension one and optional geometric strengthenings

The canonical dimension-one proof has also been audited. A quasi-isometry to Z bounds the coordinate span of every graph edge. Bounded degree and the upper metric inequality give uniformly bounded finite preimages of fixed-width coordinate bands. Thus the edge cuts across sufficiently separated integer levels are pairwise disjoint and uniformly bounded in size. For each fixed p<1 their all-closed events are independent with a common positive lower bound. Almost surely there are closed cuts in both coordinate directions arbitrarily far out, confining every open cluster to a finite band. This proves the asserted endpoint without a transitivity hypothesis.

The geometry report's optional full-orthant and additive-only gadget variants were independently checked for their stated graph, metric, effective-probability, and summable-bridge formulas. They consistently reduce survival to the now-proved quadrant lemma. They are strengthenings, not dependencies of the canonical degree-four counterexample. In particular, simply taking a product of the two-dimensional barrier with additional lattice coordinates would not suffice; the report instead uses full opposite orthants.

The probability report's reflection appendix is also a consistent alternate high-density survival argument with different constants. It is not needed for the accepted canonical theorem.

## 7. Reproduction and evidentiary limits

The pinned finite-validation script was copied to an isolated writable directory and rerun independently under ordinary Python, Python -O, and Python -OO. All three outputs were byte-identical, and the reproduced report exactly matched SHA-256 `699ccdc94cddbd0d7d7b5de549c6c2da6a926cb9b0264fd8e451603f7959a633`.

Those tests cover all 32,768 subsets of a 4 by 4 quadrant window containing the origin, including 5,293 connected sets; self-avoiding paths and weak bridges through length ten; 1,001 adversarial walks; all 128 configurations of a small gadget example; and a 3,193-vertex finite subdivision graph. These are supporting finite checks. They do not establish an infinite-cluster event or replace the deterministic parity proof and infinite union bounds.

The separately authored `recheck_exact_constants.py` uses exact rational arithmetic and explicit exceptions, and its normal, -O, and -OO outputs were also byte-identical. `INDEPENDENT_ARITHMETIC.json` records the results. The nonuniqueness lower bound exceeds 1/3 by exactly 140654287/19384713600.

## 8. Publication and novelty boundaries

This acceptance establishes the stated mathematics for the pinned authored proof. It does not establish historical priority, current openness, absence of an earlier equivalent construction, or the author's unpublished intent. A bounded negative literature search is not a novelty certificate. The primary source is a 2013 manuscript; its archival capture date is not a revision date, and its page numbering must not be replaced with the published chapter's pagination.

The deliverable consists of authored mathematical reasoning, source identification, public citations, and verification metadata. It reproduces no source PDF, dataset contents, private source material or private coordination text. Any public status should distinguish **mathematically accepted negative resolution of the stated formalization** from **historical novelty not established**.

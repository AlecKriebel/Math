# Independent mathematical audit: exact planar clique pinning

Date: 10 October 2026. Problem: 3000001 / AMR-029-0001.

## Verdict and public proof

**Accepted as correct partial results, with the source-inspection limit below. No claim of full resolution, hardness, novelty, or present-day openness is accepted.**

The distributed [partial-result proof](PARTIAL_RESULTS.md) is 13,951 bytes, SHA-256 `3b70d515da91ae807a048d4f4e79b2a77c355b1649ef34460efde2938b36ce62`. Its mathematical statements and analytic arguments are preserved in full. The [staging appendix](STAGING_OBSTRUCTION.md) has its own separate [audit](STAGING_AUDIT.md) and [acceptance](STAGING_ACCEPTANCE.json); this main acceptance does not independently cover it. This AI-assisted manuscript is unrefereed. Acceptance refers to the separate mathematical audit, not external human peer review, journal acceptance, or formal proof-assistant certification.

The objective audited throughout is the minimum cardinality of a vertex set S for which adding precisely the missing clique edges on S makes a finite simple graph generically globally rigid in the plane. It is not an edge-cost, weighted-pinning, or absolute-coordinate anchoring problem.

The accepted claims are:

1. For positive planar rigidity deficiency delta, every rigidifying S contains a rigidifying T with at most delta+1 vertices. This bound is sharp.
2. Using the credited exact already-pinned rigid-input completion algorithm, the original objective has an exact n^(delta+O(1)) algorithm. This is XP, not a uniform polynomial-time or FPT result.
3. The stated sparse-graph redundant-rigidity criterion for clique sets of size at least four.
4. On simple 3-connected cubic graphs of order at least twelve, the objective equals the feedback vertex number, with the stronger stated equivalence for each S of size at least four. The resulting tractability uses the established subcubic feedback-vertex-set algorithm.
5. On every forest of order at least four, the optimum is exactly the number of original vertices of degree at most two.
6. The explicitly stated degenerate cases and the two-separator negative control.

No mathematical correction was required in the accepted proof.

## Source inspection and scope

The audit records inspection of the relevant statements in complete primary-source files where available, with relevant pages independently rendered and visually inspected. Public source identifiers, byte hashes, version distinctions and inspection limits are recorded in [SOURCE_METADATA.json](SOURCE_METADATA.json). These are historical review observations; edition preparation performed no new scholarly-source retrieval, rehash, inspection or literature search.

- Tibor Jordán, *Rigid and Globally Rigid Graphs with Pinned Vertices*, EGRES TR-2009-05: [complete report](https://egres.elte.hu/tr/egres-09-05.pdf). The full 19-page source was available. Actual PDF page 8, printed page 7, was rendered and inspected. Lemma 4.4 assumes precisely a sparse graph and a pin set of size at least two; its formula agrees with the one used. The definitions of sparsity, incident-edge count, and generic rank were checked in context. Theorem 6.2 and Lemmas 7.6–7.8 were read in the complete report. They support the planar global-rigidity criterion and the explicit attribution of the older M-connected relaxation.
- Csaba Király and András Mihálykó, *Globally Rigid Augmentation of Rigid Graphs*: [author manuscript](https://real.mtak.hu/151592/1/Globally_Rigid_Augmentation.pdf), [published DOI](https://doi.org/10.1137/21M1432417). The full 25-page manuscript was available; page 23 was rendered and inspected. Its concluding pinning discussion explicitly includes the already-pinned constrained objective and assumes that the graph including its existing pin clique is rigid. The atom arguments and their exceptional single-edge case were checked in their surrounding sections. The inspected repository copy bears a review-manuscript footer and the [repository record](https://real.mtak.hu/151592/) labels it submitted; it must not be described as the final published PDF.
- András Mihálykó, *Augmentation problems in count matroids and globally rigid graphs*: [updated full dissertation](https://real-phd.mtak.hu/2172/1/Mihalyko_Andras_PhD_updated.pdf). The full 146-page source was available. PDF pages 3, 91, 127 and 128 were independently rendered and inspected. Page 3 records a November 2023 revision and an explanatory page added in August 2025, including corrections to an earlier general count-matroid theorem. The current Theorem 7.1 explicitly retains the needed planar theorem for simple rigid graphs of order at least six. Pages 127–128 separately give polynomial algorithms for already-pinned rigid inputs and the single-edge-completable special case. Thus this audit relies on the revised source, not an unrevised theorem with a missing hypothesis. The proof's direct handling of n<=5 covers the current lower-order boundary.
- Shuichi Ueno, Yoji Kajitani and Shin'ya Gotoh, *On the nonseparating independent set problem and feedback set problem for graphs with no vertex degree exceeding three*, Discrete Mathematics 72 (1988), 355–360: [publisher page](https://www.sciencedirect.com/science/article/pii/0012365X88902269), [DOI](https://doi.org/10.1016/0012-365X(88)90226-9). The primary publisher abstract independently confirms polynomial solvability for maximum degree three by matroid parity. **Inspection limit:** the complete original PDF was not obtained; its public PDF endpoint returned HTTP 403. The original reduction and its internal complexity proof were therefore not independently re-audited. The cubic polynomial-time corollary is accepted with reliance on this established cited theorem, not with a claim that its full original proof was inspected.

No exhaustive literature or novelty search is certified by this audit. The bounded searches do not justify declaring the arbitrary-input problem currently open.

## Analytic verification

### Small cases and the exact objective

For n<=3, generic global rigidity is completeness. Every missing edge must have both endpoints in S; hence the union of endpoints is exactly the minimum feasible S. This yields the stated n=0,1,2,3 answers, including zero for already complete graphs. For any order, a singleton clique changes no edge, so an optimum of one is impossible. For n>=4, the cited equivalence with 3-connectivity plus redundant rigidity is the correct characterization.

### Seed lemma and closure

Positive deficiency and rigidity after adding K_S imply that at least one clique edge ab is outside the closure of E(G); otherwise all of K_S would be in that closure and rank could not increase. On S, the graph consisting of ab and the two edges av,bv for each other v is a Laman graph. This includes the two-vertex case. Its edge set is a basis of the restriction to K_S, so it has exactly the same matroid closure as K_S in the complete ambient rigidity matroid. Union with E(G) preserves this rank equality.

After inserting ab, the remaining deficiency is delta-1. A two-edge group skipped because it gives no rank increase is wholly in the current closure; closure monotonicity ensures it remains spanned. Consequently the final accepted groups span the entire fan together with G, even when later groups are processed. Every accepted group consumes at least one remaining rank unit. There are at most delta-1 groups, and the corresponding vertex set has at most delta+1 vertices. Its clique contains the constructed rigid graph. There is no unjustified assumption that a group increases rank by exactly two.

For the star K_(1,m), all m leaves are forced even for ordinary rigidity: an unselected degree-one vertex remains a degree-one vertex. Selecting all leaves gives the complete graph. Since the star's rank is m and its deficiency is m-1, this proves sharpness for arbitrarily large deficiency.

### XP algorithm and constrained completion

For an optimal S, the seed lemma supplies an enumerated T contained in S. Keeping T pinned is essential. The feasible constrained completion S minus T gives an upper bound on that subproblem's optimum, while every returned completion is feasible for the original graph because the added clique is on T union P. This proves both inequalities for equality of optimal values. It does not assume that an arbitrary minimum ordinary-rigidity pin set extends to an optimal globally rigidifying set.

The enumeration count is at most n^(delta+O(1)), including when the size cutoff reaches n. Rigidity recognition and the credited constrained optimizer are polynomial. For zero deficiency the prior rigid-input algorithm applies directly. For n<=5 the direct finite check avoids inappropriate invocation of a large-order theorem.

The exceptional-case paragraph is sound: checking additional sets of cardinality zero, one, and two covers already global graphs and any graph repairable by one edge. If those checks all fail, no such edge exists; the applicable prior disjoint-atom theorem then gives both a lower bound, one newly selected vertex for each atom missed by T, and a matching completion. The revised dissertation explicitly confirms this constrained problem and its polynomial complexity. No weighted extension is needed.

### Sparse redundancy criterion

For necessity, take a nonempty X outside S. All edges incident with X are original edges. Deleting one of them leaves at most e_G(X)-1 such rows; the rows entirely outside X have rank at most 2|V minus X|-3. The complement contains at least four vertices, so the rank bound has its stated form. If there are no incident edges, rigidity already fails. Requiring full rank after deletion gives the claimed plus-one inequality.

For sufficiency, the published rank formula applies to G and also to G-f whenever f touches a vertex outside S; sparsity is preserved, and every relevant incident count falls by at most one. For f internal to S, including an edge that was already in G, K_S-f is rigid for |S|>=4. Its closure contains the deleted edge, hence contains K_S. Therefore deleting this edge from H does not decrease its rank. These two cases exhaust all edges of H. The boundary S=V is also correct: the inequalities are vacuous and H is a complete graph of order at least four.

### Cubic equivalence and cutoff

Every connected simple cubic graph other than K4 is sparse: the exceptional cardinalities two through five satisfy the explicit bounds in the proof, while for |X|>=6 the maximum-degree bound is sufficient. A K4 on four vertices in a cubic graph would be a whole component, which is excluded here.

The original 3-connectivity survives edge additions. The identity e_G(X)=3|X|-i_G(X) converts the sparse criterion exactly into the assertion that every nonempty induced subset outside S has at most |X|-1 edges, which is equivalent to acyclicity. Thus the equivalence holds for every stated S, not just an optimum.

For n>=12 a clique on at most three vertices adds at most three edges, leaving fewer than 2n-2, so it cannot be redundantly rigid. Independently, if deleting k vertices leaves a nonempty forest with c components, the edge count gives 4k>=n+2i_G(S)+2c; hence k>=4 in the stated range. The case where every vertex is deleted is harmless. Both optima therefore lie in the range in which the equivalence applies. For the finitely many smaller cubic orders, explicit small-subset checking together with an FVS enlarged to size four is a correct exact fallback. A simple 3-connected subcubic graph has degree exactly three at every vertex, so the extension of the algorithmic statement to that class is justified.

The diamond plus two isolated vertices is a valid warning against removing 3-connectivity. The four original vertices of degree at most two are forced, their clique leaves the cut pair {2,3}, and adding vertex 0 to the pin set gives a K5 plus a vertex adjacent to three clique vertices. This last graph is generically globally rigid: the clique fixes its placement up to congruence and three generic distances fix the remaining vertex. The exact optimum is five.

### Forest formula, connectivity, and the claw

Minimum degree three is necessary for generic global rigidity on at least four vertices. An unselected vertex receives no new incident edge, so every original degree-at-most-two vertex is forced. Taking all of them gives the incident-edge inequality because an induced forest has at most |X|-1 edges and each remaining vertex has original degree at least three.

The separate connectivity proof is necessary and correct. After deleting at most two vertices, any component avoiding the surviving pin clique consists entirely of original high-degree vertices and is a connected subtree. All external neighbors lie in the deleted set, and each such neighbor can have at most one edge into this subtree, or the original graph would have a cycle. This gives at most two outgoing edges. Summing the original degrees gives at least |C|+2 outgoing edges, a contradiction. This argument applies to disconnected forests and isolated vertices as well.

Finally, if there are at least two high-degree vertices, the forest leaf-count identity supplies at least four low-degree vertices; if there is one, n>=4 and fewer than four low-degree vertices force the four-vertex claw; if there are none then every vertex is selected. The claw's three leaves produce K4, resolving the only case outside the |S|>=4 sparse lemma.

## Recorded independent exact finite verification

The independent audit records checks using an independently written verifier that does not import the proof author's code. For each order at most six, it tabulates all edge subsets of the complete graph, tests the Laman inequalities, and computes rank as the maximum cardinality of a sparse edge subset by dynamic programming. This uses a different oracle implementation from greedy insertion. It uses no floating-point or probabilistic rank test. Global rigidity is checked by exact redundant rank plus connectivity after deletion of all vertex sets of size at most two.

The recorded checks all passed:

- All 33,868 labeled simple graphs of orders zero through six
- All 12 small-order objective cases, orders zero through three
- 540,696 rigidifying graph/set pairs and the same number of constructive fan checks
- 564,389 sparse-graph/set redundant-rigidity equivalences
- 3,261 forest optima, including disconnected forests
- The two-separator negative control, redundant but not globally rigid for the proposed four-element S, with optimum five

The independent finite checks supplement the general proofs. They do not establish an unrestricted theorem by extrapolation and do not constitute an implementation of the full prior polynomial constrained optimizer. Programs and raw computational outputs are not distributed; no excluded file is a premise of a mathematical conclusion. Edition preparation did not rerun these checks.

## Acceptance boundary

The arbitrary nonrigid-input optimization problem is not settled. No claim of hardness, an exact uniform polynomial algorithm, an FPT algorithm in deficiency, or a new literature result has been proved. The public edition distributes authored arguments and permitted aggregate verification and source metadata. Source PDFs, extracted source text and rendered source pages are not distributed.

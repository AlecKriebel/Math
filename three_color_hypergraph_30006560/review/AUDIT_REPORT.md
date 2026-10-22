Publication note: this is the full pre-correction audit, with filesystem references replaced by package-relative references. Its historical HOLD is cleared by NARROW_REVIEW.md. All substantive mathematical findings and release conditions are retained.

# Independent adversarial audit: rank 478 / problem 30006560

Date: 3 October 2026 UTC.

## Verdict

**HOLD for one minor, exact domain repair in Attempt 4 equation (10).** Every substantive partial theorem, counterexample, and the complete `n <= r+2` theorem passes the proof audit. The unrestricted question remains unsolved. After the repair below and manifest refresh, this is suitable to PASS as a five-attempt, unresolved partial-results package. It is not a proof of OWR Question 8 or an exact finite extremal formula.

The required repair is not a sixth attempt. No new mathematical approach was undertaken, no frozen author file was changed, and no remote write was made.

## Frozen target and reproducibility

Audited all 11 files in the supplied frozen manifest under `publication/three_color_hypergraph_30006560`.

- Every byte length and SHA-256 matches `ORIGINAL_ARTIFACT_MANIFEST.json`.
- Independently fetched all 11 files from AlecKriebel/Math at exact commit `15ab897c5cbffd82aad445211900f4ab6957ded0`; every fetched UTF-8 file equals the frozen local file byte-for-byte.
- `AUTHOR_MANIFEST.json` accounts for the other 10 files with matching sizes and digests.
- Author command `python3 verify_claims.py` succeeds, and its output equals `verification.json` byte-for-byte.
- The original review record contained an earlier checkpoint in one metadata field. The independently fetched, fully audited revision is `15ab897c5cbffd82aad445211900f4ab6957ded0`. The release manifests explicitly identify that audited revision; the corrected author bytes are listed separately.

Exact remote comparison evidence: `remote_byte_check.json`. Replay: `../verification.json`.

## Required correction

Location: `attempts/turn_04.md`, lines 42–46, equation (10).

Equation (10) is written as an unconditional supremum over nonzero nonnegative red-edge weight vectors. If `R=0`, the weight space is zero-dimensional and contains no nonzero vector. Thus the supremum is over the empty set, whereas `E_*=0`; without a special convention it is undefined as a real supremum, or is minus infinity in the extended reals. The sentence “unless T=0, which is trivial” does not state the domain restriction and does not make this displayed equality true for the empty domain.

Minimal exact repair: replace the introductory sentence before (10) with:

> If R=0, then T=E_*=0, and this case is handled separately. For R>0, optimizing the scale of a nonzero nonnegative y in (9) also yields

Keep equation (10) and its remaining proof. If `T=0` but `R>0`, the domain is nonempty and every ratio is zero, so the formula is valid. Equation (9) itself remains valid also for `R=0`, with the unique empty vector and empty sums. This is a formal boundary correction, not a failure of strong duality or of any claimed hypergraph bound.

Update the affected byte count/hash in `AUTHOR_MANIFEST.json`, regenerate the freeze, and recheck only that exact change plus the unchanged verifier. No other required mathematical repair was found.

## Primary source and scope: PASS

Independently read the official OWR Question 8/Theorem 9 text and visually inspected printed pp. 71 and 72, corresponding to PDF pages 67 and 68. The theorem really is `T <= sqrt(6RGB)` for all `r`, with `sqrt(2RGB)` known for `r=3` and conjectured for every `r`. Both coefficients are inside the radical. The successful object is an `r`-vertex set inducing at least one edge of each color in an `(r-1)`-uniform hypergraph. There is no minimum edge-cover/hitting-set quantity and no proper-coloring assumption.

Primary report: https://publications.mfo.de/handle/mfo/4435

The package's finite, simple, exactly-one-color-per-edge convention is explicit and necessary. Chao–Yu's graph Theorem 1.1 has exactly this hypothesis. Independently checked its theorem and the K4 equality example against https://arxiv.org/html/2307.15379v3 . The cone construction does not smuggle in a proper-coloring hypothesis for general input graphs.

The October 2026 paper exists at https://arxiv.org/html/2610.02165v1 . Its sections 7.1 and 7.5 concern unequal graph color counts and higher-uniformity rainbow cliques, respectively; the latter requires all clique faces to receive distinct colors and is different from the fixed-three-color partial-shadow question. The package correctly refrains from claiming a full resolution. The partial-shadow/joints framing also matches https://arxiv.org/html/2410.06498v1 . This is a bounded source audit, not a certification of global literature completeness. The acknowledged inability to read the catalogue's current body is not concealed.

## Attempt 1: PASS

For two distinct `(r-1)`-faces of one `r`-set, their union must be the full `r`-set. Distinctness follows from disjoint color families. Selecting one face in each of two colors therefore gives an injection into color pairs. This proves all three pair bounds, even in sparse hypergraphs.

For positive sorted integer counts `a <= b <= c`, `T <= ab` and `ab <= 2c` imply `T^2 <= 2abc`. If `a <= 2`, then `ab <= 2b <= 2c`. If any color count is zero, success is impossible and the result is immediate. The alleged unresolved count region is correctly restricted.

Removing a common `(r-3)`-core produces a simple graph with unchanged counts. Every successful set contains the core, and its three residual vertices must span three differently colored graph edges. The correspondence is bijective, including `r=3` with the empty core. Balanced four-class K4 blowups have counts `2q^2` in each color and `4q^3` successful sets, attaining the stated constant exactly. Coning preserves the equality and proves monotonicity of the extremal count in `r`.

## Attempt 2: PASS

The link identity counts ordered choices by color of three distinct faces in each successful set. If their deleted vertices are `u,v,w`, their common intersection is exactly the unique `(r-3)`-core `S minus {u,v,w}`. It counts `a_S b_S c_S`, not one. The inverse construction from a link rainbow triangle is exact.

Each hyperedge occurs in precisely `binom(r-1,2)` links. Both aggregation inequalities use nonnegative finite sums, and the resulting `q^(3/2)` loss is correctly disclosed. At `r=3`, `q=1`; at `r>3`, the displayed result is indeed weaker than the established sqrt(6) bound.

Recomputed the five-vertex obstruction independently. Counts are `(6,2,2)`, `T=4`, multiplicity sum `8`, first four link count triples `(4,1,1)`, last `(2,2,2)`, and link triangle counts `1,1,1,1,4`. The resource sum is `8+2sqrt(2) > 2sqrt(6)`. The formula `sum tau_A=T+U` for `r=4` correctly distinguishes the three-present-face and four-present-face successful sets.

Block aggregation is valid even when vertex sets of distinct blocks overlap. Any two distinct present faces of a successful set intersect in exactly `r-2`, so all its faces lie in the same intersection component. This gives `T=sum T_i`. For nonnegative block counts, Cauchy–Schwarz followed by expansion yields the required product-of-total-counts upper bound. Zero-color blocks contribute no successful sets. Consequently at least one block would already violate the bound if the union violated it; the connected-counterexample reduction is sound.

## Attempt 3: PASS

The simultaneous shift's absent-target rule is tested against the original entire colored family. The map from moving edges to targets is injective; absent targets cannot collide with stationary edges. Simplicity and every color count are preserved.

The four-edge cone example loses its only successful set. In the base graph the blocking edge is red 02, so green 12 stays while red 13 moves to 03. The resulting sole graph triangle is 023 and is not rainbow. This works for every `r>=3`, including the empty core.

The minimality proof exhausts all positions of `i,j` relative to the unique possible successful set in a three-edge family. When both are inside, only `S minus {i}` can move and its target remains a face of S. When `j` is inside and `i` outside, all movable faces move to the replacement r-set without obstruction. When `j` is outside nothing moves. Families with no successful set cannot suffer a strict decrease. Four is therefore minimal for the precise shift defined, without an extrapolation from finite examples.

## Attempt 4: PASS apart from the stated boundary repair

The raw red degrees are `(1,1,2,1,1,2)`, with squared sum 12 exceeding `2GB=8`.

The ownership feasible set is a nonempty finite product of simplices, with the empty product allowed when there are no successful sets. It is compact, and the objective is continuous, so a minimizer exists. The weak-duality completion of squares holds for all real weights, not just nonnegative weights.

The exchange proof establishes strong duality directly: if a positive allocation uses a red face of higher load than another available face, choose `0<epsilon<min(p(S,e),x_e-x_f)`. The objective changes by `2epsilon(x_f-x_e)+2epsilon^2<0`. Thus every positive allocation uses a minimum-load option. For `y=x`, the dual linear term sums to `sum x_e^2`, yielding equality. This also proves attainment and a nonnegative optimal dual. Unused red faces simply have optimal load and weight zero.

For `R>0`, writing `A=sum_S min y_e` and `B=sum_e y_e^2` gives `B>0` for a nonzero vector and `A>=0`. Optimizing scale gives `A^2/B`, and using the optimal load vector recovers `E_*` when `T>0`. When `T=0`, all ratios are zero. The sole missing condition is `R>0`, as above.

The fractional energy condition is only sufficient for the original conjecture, as the text correctly states. The weighted inequality is equivalent to that stronger energy condition through the proven dual, but it is unproved. In the obstruction example, the proposed private/shared allocation gives six equal loads `2/3`, energy `8/3`, and matches both Cauchy–Schwarz and the constant dual certificate. This is an exact optimum, not a numerical optimizer claim.

## Attempt 5 and full n <= r+2 theorem: PASS

An isolated vertex cannot lie in a successful set because two differently colored faces already have union equal to that set. Removal of isolated vertices is therefore harmless. If the active vertex count is less than r, there is no successful set; the proof handles this before introducing d, so no negative-dimensional shadow is used. Otherwise `d=n-r+1>=1`, and complementation gives exactly the common `(d-1)`-shadow. Complementation preserves distinctness and color-family disjointness.

The bound `T <= da` and regime `d^2 a <= 2bc` are correct. If `a>=d^2/2`, then `bc>=a^2>=d^2 a/2`. The dimension-one case has at most the empty face; with all colors positive, `T^2<=1<=2RGB`. Zero colors have T=0. Dimension two is covered by the overlap of the pair regime and the shadow regime.

For two disjoint three-triple families: choosing eight common pairs leaves exactly one incidence beyond those eight in each nine-incidence multigraph. The residual pair may itself belong to the chosen eight; the multigraph wording correctly allows this. Parity identifies its two endpoints, so the residual pair is identical on both sides. The pair-incidence multisets are equal. A vertex occurring in one triple on one side forces exactly the same triple on the other side. Thus disjointness forces each used vertex to appear at least twice. Equality of incidence multisets also ensures that neither side uses additional vertices absent from the other. Nine total vertex incidences then allow at most four vertices, on which six distinct triples cannot exist. The seven-common-pair bound follows with no finite-universe restriction.

For three disjoint four-triple families: twelve common pairs exhaust all twelve incidences of each family, so each family decomposes the same simple twelve-edge graph into four triangles. All degrees are even; degree two forces a shared triple and is impossible. Degree sum 24 and minimum nonzero degree four give at most six active vertices. Twelve distinct edges require at least six. Hence the graph is four-regular on six vertices, whose complement is a perfect matching. It is K(2,2,2), with only eight triangles, whereas three pairwise disjoint four-triple families would need twelve. This proves the eleven-common-pair bound for arbitrary ground sets.

The residual positive integer count triples are exactly `(3,3,3)`, `(3,3,4)`, `(4,4,4)`. The first two give `T^2<=49<=54,72`, respectively. The third gives `T^2<=121<128`. There is no missing integer regime. The final blockwise corollary follows from the already-proved block decomposition. No step treats a finite test as a proof of an arbitrary dimension.

## Independent replay and falsification controls

The independent audit programs import no author code.

`independent_checks.cpp` and its JSON result:

- Exhausted 2,102,622 colored hypergraph instances over all ambient n=0,...,5 and ranks r=3,...,6, using direct bitmask containment. Absent edges and all zero-color/empty cases are included. Checked the pair inequalities, target inequality, exact complement identity when defined, and exact link multiplicity identity.
- Exhausted 1,913,340 three-edge successful-family shift configurations with r=3,...,10, using n=r+2 to include all inside/outside positions of the two shift vertices. The resulting distinct colored edges always remain faces of an r-set.

`independent_controls.py` and its JSON result:

- Checked all 387,600 unordered disjoint pairs of three-triple families on six vertices; the maximum common shadow is seven, with 360 maximizing pairs.
- Examined all 4,845 four-triple families on six vertices. Exactly 15 twelve-pair shadows occur, each with two disjoint decompositions and eight total triangles; there is no third disjoint decomposition.
- Checked 2,401 rational ownership assignments on the obstruction's four two-option simplices (denominator six), finding minimum `8/3`; the supplied rational primal/dual certificate independently proves that optimum over the full continuous feasible region. Also checked 729 signed-weight weak-duality controls.
- Negative controls detect each tempting false strengthening: link multiplicity equals T; raw red squared degrees bounded by 2GB; lossless link resource aggregation; monotone simultaneous shifting; sharp constant replaced by one; and deletion of family-disjointness from either small-trade lemma.
- Rehashed all 11 frozen author files after the audit and found them unchanged.

These finite checks are corroboration and harness controls. The written arbitrary-r arguments above carry all general conclusions.

## Release conditions

1. Apply only the equation (10) domain guard and corresponding manifest/freeze updates.
2. Recheck changed bytes and deterministic verification output.
3. Keep status “unresolved after five attempts”; do not claim the full inequality, a counterexample, a finite exact extremal formula, or novelty/priority.
4. Keep source PDFs/renderings and these local audit artifacts outside the author publication manifest unless separately authorized. No remote edits, PR changes, queue changes, or additional substantive attempt occurred in this audit.

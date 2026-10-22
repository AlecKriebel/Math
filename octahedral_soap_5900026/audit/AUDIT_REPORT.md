# Independent audit: octahedral soap-film partial results

Problem 5900026 / AMR-058-0026, rank 955. Audit date: 7 October 2026.

## Verdict

**ACCEPT WITH EXPLICIT FORMULATION CORRECTIONS, as partial results only.** The corrected reading copy is mathematically accepted within its stated compact eight-face-trace model and its explicitly supported real-current relaxation. The frozen wording is not accepted unchanged as a complete definition of the latter relaxation: it omits a support condition needed by its affine certificate and leaves current regularity and generalized field pairings implicit. `CORRECTION.patch` repairs Section 0 only. It changes no numerical value, candidate, restricted theorem, dual optimum, or central contradiction.

The independently checked conclusions are:

1. The ordinary candidate has six central kites, twelve outer triangles, five interior tetrahedral junctions, and area 4√2 in the ±e_i normalization. Its unique minimum within the specified one-parameter family is at a=1/6.
2. It minimizes area among the stated finite-perimeter partitions whose positive-area adjacencies are contained in the specified eighteen-edge graph. This is a genuine globally quantified theorem in that restricted class.
3. The optima of the full-pair constant and affine divergence-free dual classes are exactly 2√3 and 2√2+2/√3. The affine proof covers every affine family, not just the displayed two-parameter ansatz.
4. The half-density average of the two candidates is a feasible real-current competitor of mass exactly 4√2. It supplies neither a better competitor nor an integrality-gap theorem.
5. A full-pair certificate of flux 4√2 cannot have all eight fields continuous at the center, subject to the comparison and compatible saturation hypotheses stated in the theorem.

**UNSOLVED remains the only justified overall disposition.** Five substantive approaches are fairly counted as 5/5. Neither unrestricted minimum is determined; equality of the ordinary and real infima is not established. No historical novelty, exhaustive literature coverage, human peer review, or formal proof-assistant verification is certified.

## 1. Frozen artifact and integrity

The retained archive is 23,055 bytes with SHA-256:

`0b0c8fc1a0101be94f32b2873c794b52479b736fffecb36cfdaf071a70726f9b`

The original manifest is 1,718 bytes with externally supplied SHA-256:

`22b61a6a8e3a1a3e0a077be3accc0b5a24311fff47440f76fe3ecea182d2b50b`

The original mathematical note is 16,565 bytes with SHA-256:

`9fed0a3be0ee43c928718a90a317529ba3833f9d4a3e2d6e2ccb4fe60d92e741`

All twelve unique archive entries match the original directory byte for byte: eleven manifest-listed payloads plus the manifest itself. There are no extra source documents, dataset records, directory entries, or private coordination files in that archive. The original verifier passes under normal and optimized Python. Both diagnostic executions reproduce the frozen JSON exactly. A fresh extraction to an unrelated temporary directory also passes.

The author's seven packet mutations are rejected in both normal and optimized verification modes, giving fourteen rejections per run. The mutation driver itself was also run under both interpreter modes. These tests are integrity controls, not evidence of the mathematical theorems. The source-derived anchor inside the mutation driver is adequate for that mutation experiment only; trust in the real packet is anchored by the separately supplied manifest hash above.

Original bytes were not edited. The patch applies to a separate copy with zero fuzz and no offset, and the result exactly matches `MATHEMATICAL_NOTE_CORRECTED.md`. `CORRECTION_RECEIPT.json` records the old/new/patch hashes and byte counts. The corrected copy deliberately retains the original historical statement that independent review was pending; this report is the subsequent audit record.

## 2. Required formulation correction

### 2.1 Compact support is a real hypothesis

Section 0 originally names real 3-currents V_s and finite-mass antisymmetric 2-currents T_st but does not explicitly require their support to lie in K=closure(Ω). The finite vertex argument proves the affine norm constraints on K only. They are false globally: for a distance-two pair at a shared-sign coordinate, x=2e_k gives

`|v_s(x)−v_t(x)|² = 8(α+2β)² = 14/3−4√6/3 > 1`.

Thus an ambient-current interpretation without support restrictions is not covered by the presented calibration proof. This observation is a counterexample to global feasibility of that affine field, not a constructed counterexample to the numerical lower bound for some alternative unrestricted-current model.

The correction explicitly requires every V_s and T_st to be supported in K. It takes V_s to be real normal 3-currents and T_st to be real finite-mass 2-currents, with T_ss=0, the stated incidence equations in R³, the sum constraint, and no pair-current mass on relative interiors of boundary faces. This is one clean precise version of the intended compact relaxation. It includes every ordinary finite-perimeter competitor and the displayed fractional mixture. No positivity restriction is imposed on arbitrary V_s; the particular mixture has nonnegative densities.

### 2.2 Pairings are specified rather than inferred

For an ordinary partition, the classical finite-perimeter Gauss–Green formula suffices. The corrected note initially takes C¹ divergence-free fields on a neighborhood of K; all constructed fields satisfy that hypothesis. Since n_st points into E_s, the outward internal boundary contribution to ∂[[E_s]] is −T_st. Hence

`∂[[E_s]] = S_s − Σ_t T_st`,

which verifies both the sign of the incidence relation and the positive boundary-flux convention.

For real currents, put ω_s=ι_{v_s}(dx₁∧dx₂∧dx₃), use a compactly supported cutoff equal to one near K, and pair the incidence equations. The defining identity for current boundaries yields

`∂V_s(ω_s)=V_s(dω_s)=0`,

because dω_s vanishes near the current support. Antisymmetry then gives

`L(v)=Σ_{s<t}T_st(ω_s−ω_t)≤Σ_{s<t}M(T_st)`.

This proves every real-current lower bound used in the note. It does not require a dual-attainment theorem. For generalized bounded fields, normal traces or cochain pairings must be specified and satisfy the comparison and saturation properties; assigning values on an area-zero set is not a proof of these properties. The corrected wording makes this limitation explicit and retains the conditional scope of the continuity obstruction.

## 3. Primal construction and parameter minimization

The four cap tetrahedra lie in distinct N octants and have disjoint interiors. Outside them, the four maximal-sign cones for P partition the remaining volume up to interfaces. In an N octant, the maximum P score is obtained by flipping a minimum absolute coordinate. A point on a lateral cap triangle opposite coordinate k has its k-coordinate no larger in absolute value than either other coordinate, so that whole triangle meets exactly the claimed inner label. The traces on the eight boundary-face interiors are correct. No volume constraint is part of this problem.

For a cap apex J_s=as, direct cross products give triangle area squared

`(6a²−4a+1)/4`.

For each central kite, its two triangles are coplanar, consistently oriented, and have area a√2/2 each. Their interiors do not overlap. Consequently A(a)=6√2 a+6√(6a²−4a+1). The quadratic is positive throughout 0<a<1/3. The numerator in the second derivative simplifies by

`6(6a²−4a+1)−(6a−2)²=2`,

giving A''(a)=12/Q(a)^(3/2)>0. The displayed derivative vanishes at a=1/6; strict convexity proves this is the unique family minimum. Substitution gives 4√2. The endpoint limits are not needed for uniqueness on the open interval.

The independent checker reconstructs every maximal-score cell by intersecting its exact rational halfspaces with the eight octahedral halfspaces. It does not reuse the author's prescribed sheet list. Exact vertex enumeration, facet ordering, and oriented tetrahedral integration yield cap volumes 1/12 and inner volumes 1/4 separately for all eight labels, totaling 4/3. It finds exactly eighteen internal facets, with twelve triangle areas √2/4 and six kite areas √2/6. The only interior polyhedral vertices are 0 and the four s/6 for s in N.

At each of these five vertices exactly four chamber scores are maximal. Their four dual vectors are a regular tetrahedron of side one: every one of their six pair distances is one. This establishes the claimed tetrahedral local geometry and the triple-sheet equal angles. The frame vertices and boundary incidences are not being counted as interior tetrahedral singularities. Equal angles and stationary flat sheets do not imply unrestricted area minimality.

Scaling is correct: the present wire edge is √2; for edge length ℓ, areas multiply by ℓ²/2 and the candidate area becomes 2√2 ℓ².

## 4. Restricted calibration theorem

The p_t=t/(2√2) vectors for t in P form a unit-edge tetrahedron. The plane opposite p_{−s} is perpendicular to it and has equation p_{−s}·z=−|p_{−s}|²/3. Reflecting p_{−s} through that plane gives −(5/3)p_{−s}=5s/(6√2), verifying the stated outer vectors.

The maximal affine scores have the claimed boundary labels. In a given N octant the comparison reduces to r+3m≥1. Replacing m by each absolute coordinate gives the four-vertex cap. Outside the chosen octant, the stated two parity cases show an outer score cannot strictly dominate. Strictness in each boundary-face interior is valid; coordinate-zero points are lower-dimensional and do not affect traces. The independent cell enumeration checks the resulting full facets, not merely sample trace points.

Every P–P pair and every Hamming-one P–N pair has distance one; there are six and twelve respectively. The other six N–N distances are 5/3, and the other four P–N distances are √(8/3). The cap-sheet normal has components proportional to (4,1,1), with its distinguished sign and coordinate; its length is √18 and the vector difference is exactly the unit inward normal. The P–P sheets have the corresponding core normal differences.

The boundary flux is 4√2. The finite-perimeter Gauss–Green identity and the graph hypothesis bound each permitted interface contribution by its area. No smoothness, connectedness, or prescribed triangulation of competitors is needed. Thus the theorem is accepted with precisely the advertised adjacency restriction. The ten failed constraints are an essential restriction: they cannot be ignored, relabeled away for arbitrary competitors, or justified by stationarity. The opposite-parity candidate itself exhibits forbidden N–N core adjacencies.

## 5. Full-pair constant and affine optima

### 5.1 Why symmetry averaging covers the entire class

Let g range over all 48 signed permutation matrices. Transform a field family by

`(g·v)_s(x)=g v_{g^{-1}s}(g^{-1}x)`.

This maps faces and their outward normals equivariantly, preserves divergence, and preserves every pair constraint. The feasible set is convex, so averaging preserves feasibility. Changing variables on the faces preserves L. This works for orientation-reversing group elements as well: the vector-field flux formulation uses the outward normal and unsigned surface area.

For a constant family the stabilizer of (1,1,1), all coordinate permutations, fixes only vectors α(1,1,1); transitivity gives αs for every label. For affine fields, a matrix commuting with all these permutations has a common diagonal entry and a common off-diagonal entry, hence is γI+βssᵀ at label s. Trace zero is 3γ+3β=0. The surviving invariant family is exactly αs+β((s·x)s−x). No independent skew-symmetric invariant matrix or extra label-dependent parameter survives.

The independent checker applies the full Reynolds average to all 96 basis coefficients of an arbitrary eight-field affine family. It verifies the general three-parameter invariant affine form, preservation of flux, and preservation of the appropriate averaged divergence. Imposing zero divergence leaves the two parameters used in the proof. This finite algebraic reconstruction supplements the group argument; it is not merely a test of one symmetric example.

### 5.2 Norm inequalities and optimality

The constant opposite-pair constraint gives |α|≤1/(2√3), and L=12α. The endpoint is feasible for all pairs, so the constant optimum is exactly 2√3.

For affine fields, every pair difference is affine in x. A convex combination of the six vertices of K therefore has difference norm no larger than the same convex combination of its vertex norms. All 28×6 vertex constraints are sufficient on the whole compact octahedron. With Hamming distance h, direct expansion gives the note's two quadratic formulas:

- Shared-sign coordinate: 4h(α±β)².
- Flipped coordinate: 4[hα²+(3−h)β²].

Every formula was independently checked as an identity in formal α,β, for all 168 label/vertex cases. At the stated α,β, the exact squared-norm inventory agrees with the frozen output:

- 36 values equal to 1.
- 24 values equal to 1/2.
- 12 values equal to 11/3−4√6/3.
- 24 values equal to 11/6−2√6/3.
- 24 values equal to 2−2√6/3.
- 48 values equal to 3/2−√6/3.

The independent inequality checker uses the rational bracket 2449/1000<√6<49/20 rather than the author's sign-aware squaring routine. It certifies every value ≤1 exactly. No floating-point tolerance is involved.

For any feasible invariant affine family, opposite labels imply |α|≤1/(2√3); a distance-two pair at the common-sign coordinate, using both vertex signs, implies |α|+|β|≤1/(2√2). Therefore

`12α+8β ≤ 4|α|+8(|α|+|β|) ≤ 2/√3+2√2`.

The stated positive parameters attain this bound and satisfy the remaining constraints. The affine flux calculation is correct: on F_s, s·x=1 and n=s/√3, giving constant density α√3+2β/√3 and total flux 12α+8β. The exact optimum is accepted. It remains far below the candidate; no claim of improvement on historical numerical lower bounds is made or warranted.

## 6. Real-current mixture and absence of cancellation

Ordinary chamber currents satisfy the corrected support, normality, sum, boundary, and incidence conditions. Averaging the two ordinary families preserves all of these linear conditions. Their density functions take values 0, 1/2, and 1 and sum to one. This is a fractional competitor, not an ordinary partition.

The stronger assertion that the geometric supports meet only in area-zero sets is true. Outer plane normals have absolute pattern (4,1,1); core plane normals have pattern (0,1,1). Those two types cannot be parallel. For outer planes, a parallel plane of the opposite configuration has the opposite offset and is distinct. Coincident core planes have their kite interiors in opposite coordinate half-planes. Every other pair of supporting planes intersects in dimension at most one.

The independent exact sheet reconstruction checks all 18×18 cross-configuration pairs. There are 306 nonparallel pairs, twelve parallel distinct pairs, and six coincident core-plane pairs. In each coincident pair, all noncentral vertices lie strictly in opposite half-planes; the polygonal interiors cannot overlap. Thus there is no positive-area cancellation. Pair-current masses add on mutually singular supports and the factor 1/2 gives exactly 4√2. Removing the densities produces support area 8√2, so this is not a smaller ordinary surface.

Together with the corrected current comparison proof, the accepted relation is

`2√2+2/√3 ≤ inf A_real ≤ inf A_ordinary ≤ 4√2`.

This is only for the stated compact model and supported relaxation. The calculation neither proves equality of the two infima nor identifies every historical meaning of fractional soap films. In particular, no passage to an unspecified mod-v model is justified.

## 7. Central-continuity obstruction

If a full-pair family has flux 4√2, both equal-area candidates saturate the comparison inequality. Its sheetwise deficit is nonnegative and has zero integral, so every positive-area sheet is saturated almost everywhere. Under the theorem's compatible trace/representative hypothesis, sequences of saturation points in each core-sheet interior approach the origin.

The six P-core sheets force every pair difference at the origin to equal (t−u)/(2√2), hence v_t(0)=c_P+t/(2√2) for all t in P. The reflected candidate gives v_s(0)=c_N+s/(2√2) for s in N. These signs remain correct under x↦−x with simultaneous label reflection.

Set d=c_P−c_N. For each t in P, the full-pair constraint with −t requires |d+t/√2|≤1. Their squared sum is

`4|d|² + √2 d·Σ_{t∈P}t + Σ_{t∈P}|t|²/2 = 4|d|²+6`.

The cross term is identically zero and the constant is six, contradicting the upper bound four. This is an exact contradiction for every d, not a rational-sample argument. Continuity at the single central point is sufficient; global continuity is unnecessary.

The theorem is accepted with its stated hypotheses. It excludes neither discontinuous bounded fields with direction-dependent limits nor other proof methods. It proves neither existence of a singular sharp calibration nor nonminimality of the candidate. It cannot be converted into a strict integrality-gap conclusion without additional duality, attainment, and regularity arguments that are not supplied here.

## 8. Sources, original problem, and access limits

The exact Problem 26 was independently inspected in indexed primary-PDF text from [Sullivan and Morgan's problem list](https://citeseerx.ist.psu.edu/document?doi=13ac2665ff2736dd27fc8780991a091b9698d8f5&repid=rep1&type=pdf). It asks about eight-region separation and the fractional-density variant. This supports treating edge-wetting-only examples as a different problem. The journal identity is independently corroborated by [Morgan's institutional publication list](https://hub.williams.edu/math/morgan/publications/), item M127, and the [DOI](https://doi.org/10.1142/S0129167X9600044X).

**The primary problem-list PDF was not freshly obtained.** CiteSeer direct access timed out, the historical author route and Berlin papers path were unavailable through the web tool, and the publisher PDF endpoint returned HTTP 403. The retained file named soap-prob.pdf is HTML. It was rejected as PDF evidence. No hash of a supposed verified original-problem PDF is claimed.

[Brakke's Numerical Solution of Soap Film Dual Problems](https://emis.de/ft/51988) was freshly downloaded during this audit as a valid 19-page PDF and byte-matched to the retained copy: 518,003 bytes, SHA-256 `9491c352f058f12bd628d52e72a108f060486821a089060b4bb98e5bfd7835c8`. Its paired-field model, symmetry reduction, fractional discussion, and octahedron section were read; printed page 285 and Figures 10–11 were rendered and visually inspected. Its computations do not constitute a proven sharp equality for the octahedron.

[Covers, soap films and BV functions](https://cvgmt.sns.it/media/doc/paper/3596/proc_pisa_2017_bpps.pdf) was freshly downloaded and matched: 1,445,654 bytes, SHA-256 `453e196ada5ecb2fa123335883c331b88d5b8a162971cded3f4df0251633a057`. The introduction and Example 4.4 were read and Figure 6 inspected visually. Their different cover and edge-wetting choices do not establish optimality under the eight fixed face traces.

The retained [Soap films and covering spaces](https://kenbrakke.com/papers/downloads/covering.pdf) is a valid PDF, rehashed at 3,245,779 bytes and SHA-256 `efdd134d52a3e2c354da53879c79271190893a0e3a799a08b5011a2265eff03f`. Its defective extracted encoding prevents relying on unreadable text; no fresh retrieval or uninspected theorem is claimed in this audit.

[Brakke's octahedral example gallery](https://kenbrakke.com/evolver/examples/octa/octafilm.htm) was read afresh. Its least-area statement is expressly limited to the displayed configurations. No Surface Evolver datafile was executed in this audit. Current search did not supply a theorem resolving the target; that is a bounded negative finding, not a proof of present global literature status.

The compact partition formulation is a precise natural realization of eight labeled boundary regions. Neither the original short problem statement nor this audit establishes equivalence with every possible geometric Plateau spanning convention. The corrected note appropriately restricts its claims to its own model.

## 9. Diagnostics and reproducibility

The author's 884 checks pass in normal and optimized Python, with byte-identical output to the frozen CHECK_RESULTS.json. The checker was read in full. Its exact arithmetic is sound, including the sign branches in q+r√6≤1. None of its correctness conditions relies on Python assert. Some output items, such as the stated tetrahedral-point count, are labels rather than independent geometric computations in the author script; the separate checker supplies an actual junction enumeration.

`independent_controls.py` is a separate standard-library implementation with **1,075 exact checks**, also passing in normal and optimized mode with identical JSON. It does not import or execute the author checker. Its principal independent controls are:

- All score-cell halfspace intersections, full boundary facets, exact cell volumes, and interior-junction enumeration.
- Exact facet areas, shared-sheet agreement, and complete 324-pair support-plane analysis.
- Formal pair-vertex quadratic identities, exact rational radical bounds, and the complete affine inventory.
- The 48-element Reynolds average on all 96 affine coefficient basis fields, including flux and divergence.
- Rejection of forbidden adjacency, opposite-pair misuse, 110% scaling, wrong apex, false central compatibility, dropped mixture density, and global affine feasibility outside the domain.

To replay in a separate working directory, keep the original packet unchanged and run:

1. `python3 authored/verify_packet.py --manifest-sha256 22b61a6a8e3a1a3e0a077be3accc0b5a24311fff47440f76fe3ecea182d2b50b`
2. `python3 -O authored/verify_packet.py --manifest-sha256 22b61a6a8e3a1a3e0a077be3accc0b5a24311fff47440f76fe3ecea182d2b50b`
3. `python3 authored/mutation_tests.py`
4. `python3 independent_controls.py` and `python3 -O independent_controls.py`, comparing both outputs to INDEPENDENT_RESULTS.json.
5. Copy the original mathematical note into another directory, apply CORRECTION.patch with `patch --batch --fuzz=0 -p1`, and compare the result byte-for-byte with MATHEMATICAL_NOTE_CORRECTED.md.

The code and replay counts are evidence supporting the written proof audit. They are not substitutes for Gauss–Green theory, formal verification, global minimization, or a duality theorem. No randomized optimizer, mesh convergence argument, or unverified numerical tolerance is used for an accepted exact conclusion.

## 10. Dataset identity, readiness, and boundaries of acceptance

Both complete input corpora were independently read, parsed, counted, and rehashed, matching the frozen metadata:

- problems.json: 68,931,837 bytes; 15,458 entries; SHA-256 `04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`.
- research_results.json: 80,334,822 bytes; 6,701 entries; SHA-256 `8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b`.

The target's retained problem and research records were inspected. The prior research is literature triage and gives no mathematical proof to resume; its unsubstantiated mod-v wording is not adopted. This audit did not independently repeat every reported remote repository/branch/PR search. Those readiness results remain bounded historical search records, not mathematical evidence or an exhaustive nonduplication guarantee.

Acceptance covers the corrected Section 0 and all five mathematical approaches with the limitations above. It does not authorize a solved status, an unrestricted minimizer claim, a sharp 4√2 full-pair certificate, a strict ordinary/real gap, or equivalence with unspecified fractional models. The audit was conducted by an independent worker without helpers. No remote publication or repository mutation was performed.

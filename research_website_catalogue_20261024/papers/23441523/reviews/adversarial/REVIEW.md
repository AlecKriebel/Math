# Independent adversarial review — Zenodo 23441523

**Conclusion: no substantive mathematical defect identified in v1.0.0 under its stated oracle and distance conventions.** The strongest supported result is the fixed-property separation in Theorem 1, with the VDF lower bound asserted along a positive rational proximity sequence. This review is AI-assisted mathematical scrutiny, not external human peer review, proof-assistant certification, or an exhaustive novelty/priority assessment.

Paper: *A polynomial versus superpolynomial gap in vertex-distribution-free graph testing*, version 1.0.0, 17 October 2026. [Public record](https://zenodo.org/records/23441523).

## Source binding and review scope

- Published five-page PDF SHA-256: `a9d81e3b765adc8ee9bee044d23008515e31bbeb57a916358f32e8d3c021a1f0`.
- Published source/verification ZIP SHA-256: `4367fad39640b11fb1809c2302a91947a9343dd8179590a51ef87e5756caa5cb`.
- Fresh acquisition receipt copied to `source-receipt.json`; all 98 extracted archive files match the ZIP byte for byte, and the archive's embedded paper PDF is byte-identical to the public PDF (`integrity.json`).

Read all five PDF pages and the entire delivered TeX. Also read the complete 277-line original mathematical proof preserved as `audit/inputs/PROOF.md`, all six supplied finite checker implementations, and the replay driver. Archived reviewer reports, root mathematical decisions, priority decisions and sibling opinions were not opened. The original proof's introductory audit-status assertion was encountered and explicitly ignored as mathematical evidence. Its construction and coupling proof were assessed directly. Fresh controls were implemented before reading the published checker implementations and import none of their code.

The load-bearing Alon–Shapira import was independently assigned to a separate primary-source subtask. Its actual theorem/model pages and concluding lower-bound proof pages were also read here. The original cited `math.tau.ac.il` host failed; the same author's accessible `cs.tau.ac.il/~asafico/subdir.pdf` manuscript was obtained. Source hashes and exact page notes are retained in `primary-import/`.

## Exact claim and conventions

The fixed property is `P = {K4-free graphs} ∩ {graphs made 3-colorable by deleting at most one vertex}`. Graphs are finite, simple and undirected. Sampled inputs are nonempty. Distance sums `D(u)D(v)` over changed unordered edges and allows **both additions and deletions** on the same vertex set; uniform distance therefore divides changed-edge count by `n²`.

The classical tester has one-sided error, identifies repeated vertex labels, does not require `n`, and uses `O(ε⁻⁶ log(1/ε))` uniform samples and `O(ε⁻¹² log²(1/ε))` adjacency calls. It is an oracle-complexity claim, with exhaustive membership search permitted.

The VDF lower bound concerns worst-case **total sample-plus-adjacency calls** of arbitrary adaptive two-sided testers. Along a positive rational sequence tending to zero, the cost is `exp(Ω(log²(1/ε)))`, even when labels, size, the complete positive rational weight vector and the heavy vertex are supplied. It does not claim a lower bound on samples alone when unrestricted adjacency calls are free, nor a runtime separation or a separation for every hereditary property.

## Adversarial proof assessment

### Classical sampling and small graphs

Heredity, edge-deletion closure, and extension by an isolated vertex follow directly from the two defining conditions. Three-colorability is contained in P. The implication used in the sampling proof is consequently correct: being far from P implies being far from three-colorability.

The partial-coloring repair estimate includes edges incident with empty-list vertices, and all remaining monochromatic edges are counted by the chosen minimizing colors. The estimate can overcount but cannot undercount. For every vertex in W, **every** feasible color removes at least the threshold number of available colors from other lists. Removing the chosen vertex's own list only strengthens the decrease.

The branching argument conditions on earlier blocks; all nodes at the current depth are already fixed under that conditioning. A union bound over fixed ternary-tree addresses does not require independence among nodes sharing the current block. A proper coloring of the whole sampled induced graph would prescribe a surviving branch, contradicting the potential decrease. Repeated labels cannot become fresh vertices on a branch.

Two disjoint sampled non-three-colorable witnesses survive any one-vertex deletion. The cross-block collision bound is `r²/n`, regardless of repetitions within either block. For small input size, the coupon-collector bound instead ensures that all vertices are seen. The two cases use the same sample budget and do not require the tester to know which case applies. The `n=1`, explicitly empty-input, and `ε>1/8` cases are addressed. The stated polynomial powers follow from `h=O(ε⁻¹)`, `ℓ=O(ε⁻²)`, `r=O(ε⁻³)`, and `M=O(r² log r)`.

### Heavy apex: arbitrary repairs, not deletion-only assumptions

For a three-colorable tail H, a minimum triangle-edge deletion leaves a three-colorable triangle-free tail, so adjoining the universal apex produces a P-member. With apex weight 1/2 and tail weights `1/(2n)`, each tail-edge edit costs `1/(4n²)`.

For an arbitrary repaired P-member F, the tail vertices still adjacent to the apex must induce a triangle-free graph in F. Keeping that restriction and isolating the vertices whose apex edges were deleted repairs H with at most `4n²δ_t+n|S|` changes. This allows tail additions and all possible apex deletions. It gives the exact factor 1/4. The proof does not silently restrict competitors to the obvious repair.

The tail three-colorability condition is essential. The triangle-free four-chromatic Mycielski graph obtained from C5 has zero triangle distance, while its universal-apex join is outside P. A light apex also invalidates the exact identity: in a K3 tail, deleting one sufficiently cheap apex edge can beat every tail-only repair. Both are explicit negative controls, not counterexamples to the correctly stated lemma.

### Tripartite cover and reduction

The cover has three parts and is always three-colorable. Every triangle projects to three distinct adjacent original vertices. Because triangle-freeness is edge monotone, intersecting a repair with the original edge set removes additions without increasing its cost. Projecting every deleted cover edge to its original edge deletes at most as many original edges and hits every surviving original triangle. The different vertex counts give the factor 1/9. The combined distance factor is therefore 1/36.

Sampling the transformed weighted graph is local and independent of H's edges. Self-pairs, apex pairs, same-part pairs and copies of the same original vertex require no query to H; every other pair requires at most one. Each sample/query execution exposes at most `s+2e≤2Q` original names. Giving the entire weight vector and vertex set leaks only the known size/construction, not unknown source edges. Adaptive choices and early stopping remain valid because the simulation is exact history by history.

### Lower-bound quantifiers and external import

[Alon and Shapira, *Testing subgraphs in directed graphs*](https://www.cs.tau.ac.il/~asafico/subdir.pdf), Theorem 4(ii), pp. 4–5, and Section 7, pp. 24–28, provide the needed two-sided superpolynomial bound and its stated undirected nonbipartite consequence. The model on p. 2 supplies `n` and allows arbitrary desired-pair queries. Their complexity convention on p. 4 counts inspected vertices with all spanned edges available. Thus a Q-call simulation using at most 2Q original vertices contradicts that stronger-information lower bound if Q is too small; no quadratic conversion loss is required in this direction. Section 7 uses random relabelling and partial-view indistinguishability against deterministic decision procedures, hence randomized adaptive testers by the distributional argument.

A constant proximity rescaling and the unordered-pair convention leave `exp(Ω(log²(1/ε)))` unchanged. Strict versus non-strict farness can be accommodated by another fixed slack factor. The supporting explicit construction supplies rational `ε_d=K/(1152m)` with `log(1/ε_d)=Θ(d)` and lower cost at least `m^(1/3)=2^{d(d+1)/3}`. No interpolation to a stronger all-ε claim is needed. A superpolynomial lower sequence already rules out any fixed polynomial upper bound in the classical complexity and `1/ε`.

### Supporting direct construction and blowup boundary

The original proof's equal-norm sphere construction has enough integer encodings, prevents carries in base `2B`, and yields the claimed progression-free set. Its arithmetic tripartite host has exactly the designated edge-disjoint triangles. The GOOD/BAD parity patterns agree on every proper subset of the three edge coordinates; BAD has sufficiently many complete triangles except with the stated exponentially small probability.

The lazy-permutation exposure argument conditions on the actual exposed host images as well as observations. Under that conditioning, an unused name remains uniformly mapped among unused host vertices. Padding a stopped exposure list restores the fixed-length uniform ordered sample needed for the union bound. The coupling stops before a whole designated triangle becomes exposed. The exceptional non-far BAD mass is subtracted in the rejection-probability comparison; it is not silently conditioned away.

Adding an isolated vertex is different from allowing arbitrary blowups. For the six-vertex wheel on a C5 rim, every doubled-vertex blowup fails P: an internal twin edge creates a K4, while six independent twin classes retain a four-chromatic wheel after any single deletion. This confirms the boundary of the positive blowup-avoidable result and prevents an incorrect appeal to it.

## Reproduction and independent checks

The delivered replay completed all six controls in ordinary and Python-optimized modes: **12 successful runs**, with checker fingerprints and exact expected mathematical outputs matched (`replay.json`). The scripts use explicit exceptions, so optimized execution does not disable their checks. These runs cover coloring/list inequalities, parameter and coupon bounds, the arithmetic construction, parity/exposure calculations, adaptive finite-query controls, exact weighted repairs and the cover bridge.

Fresh standard-library controls (`independent_controls.py`, `independent-controls.json`) passed:

- Classification of 33,866 possible repair graphs, used to minimize over arbitrary edge additions/deletions in 118 three-colorable heavy-apex cases.
- Exact triangle-deletion minima for all 75 labelled source graphs with 1–4 vertices and their tripartite covers.
- 10,731 proper partial-coloring repairs and 29,505 feasible list-potential steps.
- 11,730 exact oracle endpoint cases and 75 strictly positive rational distribution checks.
- All 64 internal-edge choices of the doubled-wheel blowup, plus the missing-tail-hypothesis and light-apex negative controls.

The larger partial-coloring and tail cases are seeded finite checks; they are not exhaustive in graph size. The asymptotic theorem rests on the proofs and the exact primary import, not these counts.

## Primary question and limits

The [original Oberwolfach report](https://ems.press/content/serial-article-files/46798), pp. 1138–1139, explicitly defines its complexity as the total number of vertex samples and edge queries and asks the stated comparison question. [Gishboliner–Shapira arXiv v5](https://arxiv.org/pdf/1905.09903v5), Section 5.3, Problem 5.6 and Proposition 5.7, confirm the later question and the restricted positive blowup-avoidable result. The terminology in the reviewed theorem therefore matches its claimed problem rather than substituting a different sample-only model.

No load-bearing proof gap remains identified in the reviewed claim. The lower bound is worst-case oracle cost, and its strengthened access still conceals the input graph's unknown edges. The upper bound does not promise polynomial running time. No empirical or numerical extrapolation is needed. The manuscript's literature-priority assertions are not certified here; a complete modern priority search and external expert review remain separate tasks. No repair, publication, Git mutation, sheet update, or outreach was performed.

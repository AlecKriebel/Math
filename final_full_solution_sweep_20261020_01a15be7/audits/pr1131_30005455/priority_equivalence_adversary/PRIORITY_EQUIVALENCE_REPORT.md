# Independent priority, equivalence and target audit of PR 1131

Audited immutable head: `bacae693a1f2a33c89565b0bd716620885831289`; base: `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc`. Problem 30005455 / OWR-12697708-008. Audit date: 21 October 2026 UTC.

## Verdict

The inspected primary sources do not supply the claimed **all-equilibrium, arbitrary-positive-rate forest bound alpha>4/3**, or the **universal equal-rate whisker bound alpha>=17/4**, as a stated theorem or a recovered direct implication. This is bounded priority evidence, not certification of novelty.

There is nevertheless a definite positive prior implication: the proof in the Holmes–Kleptsyn 2017 author manuscript already gives whisker forests for **alpha >=24**, despite its displayed theorem using >25. Merely improving 25 is therefore not a sufficient novelty claim. The candidate's 17/4 is stronger than this implicit old bound.

The original printed problem literally requests improvements of the bounds 2 and 25; its following sentence suggests sharpness at 4/3. Under the intended finite simple loopless graph convention and positive integer initial counts, the candidate answers both literal improvement requests. The conjectured sharp equal-rate whisker classification for 4/3<alpha<17/4 remains open. The immutable eight-file label “original target OPEN” conflates those two standards and should be qualified when presenting the result.

## Independence and inspected evidence

All eight actual files were freshly extracted with `git show` at the immutable head and read. Their hashes are in `immutable_head_pins.json`. This includes the candidate's historical mathematical audit, which is part of the required eight-file record. The parent supplied the suspected >24 prior-proof implication as an adversarial lead. I derived its complete bridge directly from the primary manuscript before reading any separate priority report. **No earlier priority report was read at any point.**

Fresh captures are private in `private_sources/`; source PDFs and extracted third-party text are evidence, not a publication payload. No captured or original program was executed. No person was contacted, and no Git, index, PR, GWS or other provider state was mutated.

## The positive prior bridge: 25 already improves to 24

Use weights a_i=|V|x_i and c=9/4. The HK2017 manuscript's Lemma 5 (p21, proof p23) requires alpha>81/4 and gives

    a_i in [1,1+c/alpha) union (2-2c/alpha,2].

Its Lemma 6 proof (p24) makes small edges incident to leaves whenever

    alpha > c(exp(c)+1).

For two adjacent large edges, each takes more than half the common vertex's rate if 2-2c/alpha>3/2, which holds for alpha>9. Thus large edges form a matching; together with the small-edge leaf property and the old forest theorem this gives whisker components.

All prerequisites hold at every alpha >=24. The only transcendental check can be sealed rationally. Sum exp(9/4) through degree 12; the tail starts at degree 13, and every subsequent term ratio is at most 9/56. This gives

    exp(9/4) < U = 191714244173193067 / 20206532637491200 < 29/3,
    c(U+1) = 1907286991296158403 / 80826130549964800 < 24.

The corresponding threshold upper bound is approximately 23.59740567. This is a proof consequence of the older argument, not a new mechanism. Joining the deterministic consequence with HHK2023 Theorem 1 and Proposition 1 yields the stochastic finite-graph consequence. [HK2017 manuscript](https://researchers.ms.unimelb.edu.au/~mholmes1@unimelb/Reinforced-graphs_final.pdf), [HHK2023 published paper](https://pure.au.dk/ws/portalfiles/portal/418609000/Hirsch_2023_Nonlinearity_36_3013.pdf).

## Prior overlaps and exact remaining differences

| Earlier result or mechanism | What it positively supplies | What is still needed for the candidate |
|---|---|---|
| VHHKR2016 Proposition 2(iv), printed 2500, proof 2515 | Exact sec^2(pi/(2m)) stability threshold at the uniform equilibrium on an isolated odd cycle | A statement for every supported equilibrium, arbitrary rates, nonuniform weights and attachments |
| VHHKR2016 Theorem 7, printed 2523–2524 | Complete equal-rate triangle equilibrium classification; unstable nonuniform branches; known 4/3 obstruction | Arbitrary-rate triangle and longer weighted odd cycles in arbitrary supports |
| HHK2023 Lemma 2, printed 3036 | Power coordinates and alternating even-cycle perturbation | This mechanism must be credited; arbitrary positive coefficients on the logarithmic vertex terms preserve the cancellation, so that extension is immediate |
| HK2017 Proposition 1, Lemma 4 and Corollary 7, manuscript 17–20 | Diagonal stability necessity, champion selection, least-weight leaf argument and equal-rate lower weight bound | Uniform scalar estimates excluding all nonleaf edges of weight<=3/2 down to 17/4 |
| HHK2023 Proposition 9, printed 3035 and appendix 3037–3041 | Every fully supported equilibrium on a plain path of at least four edges is unstable for alpha>2, at equal rates | Every non-whisker tree with branches and the original equal rates |
| HK2017 Example 1 | Unequal rates can preserve a diameter-four path for sufficiently large alpha | The candidate's explicit alpha 2 example is a scope illustration; the phenomenon is prior |

Primary published VHHKR2016 source: [publisher PDF via TU Eindhoven](https://pure.tue.nl/ws/portalfiles/portal/46706436/hofsstro2016.pdf), DOI [10.1214/16-AAP1153](https://doi.org/10.1214/16-AAP1153). Its preprint is [arXiv1406.0449](https://arxiv.org/abs/1406.0449), first submitted 2 June 2014; its numbering differs from the journal numbering.

The candidate's meaningful forest increment is the weighted odd-cycle step, not the appearance of the numerical constant 4/3 alone. Writing A_i=a_i^alpha, b_v=lambda_v/S_v and D_i=a_i^(1-2alpha), its extra identity and estimate are

    sum_i D_i = sum_v b_v(1/A_previous+1/A_next),
    4 sum_v lambda_v/S_v^2 <= sum_i D_i.

The latter follows from S_v>=A_previous+A_next and (A_previous+A_next)^2>=4A_previous A_next. Two real highest-frequency cycle directions then retain the earlier uniform spectral constant at every weighted equilibrium. I did not recover this general weighted conclusion in the inspected earlier sources.

There are checkable obstructions to tempting equivalence arguments:

* **Uniform does not mean all.** In an unequal-rate triangle with rates(1,2,3), equal positive edge weights would receive endpoint reinforcement totals3/2,5/2,2, so cannot be an equilibrium. The uniform-cycle theorem is not applicable after a common normalization.
* **The diagonal test alone does not sharpen2 to 4/3.** At the equal-rate unit-weight triangle with alpha=3/2, q=r=1/2 satisfies the old diagonal necessity, although the full Jacobian has a positive eigenvalue3alpha/4-1=1/8. A further mixed perturbation is essential.
* **Path containment does not permit deletion.** Removing positive branches changes the normalization S_v at each affected vertex. The restricted vector is generally not an equilibrium of the isolated path. Neither Proposition9 nor stability reduction for already-zero colors supplies the desired branched-tree theorem.
* **The old numeric proof cannot simply be quoted at17/4.** Its Lemma5 prerequisite is alpha>81/4; even its coarse endpoint-probability dichotomy needs alpha>=8. The candidate's exact intervals and analytic tail provide additional estimates.

## Exact original target and initial-count scope

The original OWR discussion begins on printed653, states the continuous-time clock model on654, and gives the two open problems on655. The >4/3 suggestion is a separate subsequent sentence. I checked printed655 both by extracted text and a rendered image. [Original report](https://ems.press/content/serial-article-files/47008).

The finite simple loopless convention is essential: a single loop survives at every exponent, contradicting even the old forest conclusion. The original discussion does not spell out all graph conventions; the candidate should retain its explicit one. Isolated vertices can be discarded.

The immutable candidate proves unit initial counts. The almost-sure support claims extend to every fixed positive integer initial vector n without assuming a stronger external theorem: from the all-one jump chain there is positive probability of selecting exactly the finite edge sequence needed to reach n after k=sum_e(n_e-1) steps. All steps have positive probability because rates and current counts are positive. The Markov property then implies

    P_one(bad asymptotic support) >= P_one(reach n at step k) * P_n(bad support).

The left side is zero; hence P_n(bad support)=0. The support event is unchanged by the finite prefix, and continuous-time scaling is unchanged by a finite time shift. This is a deduction for almost-sure claims, not an assertion of strict-stability attainment from every initial vector. No real-valued, nonpositive or looped-model extension is inferred.

## Broader adversarial literature checks

The fresh primary-body check included the published 2016,2017 author, and published 2023 sources, the original OWR report, and relevant variants. The current Holmes and Hirsch author publication pages contain 2026 material and still list the 2023 strong-regime paper; no stronger finite-graph theorem was recovered there. Exact-title/topic queries and the visible citation-family leads did not recover either claimed universal theorem. Broad WARM/forest/whisker searches often returned irrelevant ordinary-language results, so they are weak negative evidence.

Ruszel–Thacker2024, *Positive Reinforced Generalized Time-Dependent Polya Urns via Stochastic Approximation*, DOI10.1007/s10959-024-01366-w, gives dominance/fixation for an urn choosing among all its colors. It does not have the random incident-edge subset law. A two-edge WARM star has both edges forced infinitely often by its leaves, showing why global single-color fixation cannot be imported. [Primary paper](https://research-portal.uu.nl/ws/portalfiles/portal/242590471/s10959-024-01366-w.pdf).

Benaim–Benjamini–Chen–Lima2015 has bins on vertices and pairwise competition along edges; its hypergraph variant section explicitly treats the linear case. These results do not furnish either supercritical universal support theorem. [Primary preprint](https://arxiv.org/abs/1211.1247). The geodesic/trace-reinforced ant leads use successive random walks between marked endpoints, and the extremal-linkage lead uses layered fitness-based networks; their model statements do not identify either with local-clock WARM.

The Basu–Benaim2016 convergence preprint is explicitly withdrawn for technical proof/result errors, as recorded by arXiv on 23 June 2016; it cannot replace the published 2023 stochastic bridge. [Official record](https://arxiv.org/abs/1606.04569).

## Chronology, limitations and controls

Journal publication years and arXiv submission histories are distinct from document dates. The HK author manuscript says March 2017; the accessible HHK author manuscript says 13 January 2021; the earlier VHHKR manuscript says 2014. Those labels do not independently establish their first public availability. VHHKR arXiv records2June 2014; the published journal is 2016. HHK2023 records publication 28 April 2023. No claim of priority based on repository development dates or the current existence of an author-hosted file is made.

The official HK publisher page returned403; its linked author manuscript was fully accessible and freshly pinned. The HHK publisher PDF initially returned403 to a default client, then succeeded with a browser User-Agent and matches the immutable metadata hash. The Kleptsyn author page returned403. These access limits, incomplete citation coverage and inaccessible/unindexed/unpublished work prevent exhaustive priority clearance. No absence-of-search-hit argument is promoted to a novelty theorem.

The newly authored offline verifier is `verify_priority_scope.py`, SHA-256 `7a89911fe8acb5ab2134a44c5d7ea8223dc5df6ea79d3d767938ee54b30bd59e`,5739 bytes. Its detached hash was sent to the parent before execution. It reads and pins all eight immutable files and 13 fresh primary captures, verifies the exact old-proof constants and scope comparisons, and rejects three deliberate corruptions in normal, -O and -OO modes. All 12 runs behaved as required (3 positive passes; 9 negative rejections). See `PRE_EXECUTION_SEAL.json` and `OFFLINE_REPLAY.json`. This verifier does not prove exhaustive priority or independently certify every mathematical assertion in the candidate.

The strongest verified priority challenge is the old implicit >=24 whisker consequence. No positive equivalence defeating the candidate's stronger universal bounds was found. Recommended framing: **sharp finite arbitrary-rate forest threshold; substantial equal-rate whisker improvement; both literal bound-improvement requests answered; sharp whisker conjecture remains open; broad prior mechanisms credited; novelty bounded by the documented search.**

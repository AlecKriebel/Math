# Independent review: kNN observation and componentwise identifiability

**Problem:** 30002105 / OWR-11793-003.  
**Verdict:** **PASS_SCOPED_DIRECTION_AND_DISCONNECTED_SUPPORT_OBSTRUCTIONS.**  
**Recommendation:** keep the original target **unsolved, 2/5 substantive approaches**.  
**Mandatory corrections:** none.  
**Reviewed snapshot:** `PARTIAL.md`, SHA-256 `6e676a0541b0e7d489743aef5e1882feab5538da359d870344d099fa9fa31ab4`.  
**Review date:** 30 September 2026. Separate adversarial AI review using gpt-6-astra at xhigh reasoning effort; this is not human peer review or a novelty certification.

The submitted finite direction example is correct. The two fixed, globally smooth sampling laws also give a rigorous asymptotic statistical obstruction to one globally normalized density or geometry reconstruction when componentwise similarities are invisible to the graph. The argument covers even labelled directed graphs, and therefore the original undirected union observation. It does not resolve a connected-support version, an unspecified constant-factor loss, or all possible neighbor regimes.

## 1. Exact original observation and credited dependencies

I read the full original contribution and inspected the rendered printed page 1914. The source is Ulrike von Luxburg's contribution in **Oberwolfach Report 31/2012**, pp. 1914–1915, not a 2013 report. An edge is undirected and is inserted when either endpoint is a nearest neighbor of the other. Thus the union symmetrization in equation (1) is the appropriate interpretation. Neither ordering nor directions are supplied. The contribution asks for density values up to constant factors and approximate locations up to a global translation, rotation and scale. It does not formalize the regularity class, connectedness, asymptotic neighbor regime or loss. [Original full report](https://ems.press/doi/pdf/10.4171/OWR/2012/31).

The source distinctions in the submitted artifact are accurate:

- The 2013 roadmap explicitly defines directed observations in §2. Its graph-only multidimensional formula in §5 is conjectural; the authors explain two remaining proof difficulties and then prove a weaker geometrically informed version. The common-neighbor reconstruction in §7 is a sketch. The finite example here does not invalidate an appropriately approximate asymptotic interpretation of that sketch. [von Luxburg–Alamgir, published full paper](https://proceedings.neurips.cc/paper_files/paper/2013/file/eae27d77ca20db309e056e3d2dcd7d69-Paper.pdf).
- Terada–von Luxburg's Theorem 3 and Proposition 4 expressly use directed nearest-neighbor information. Their hypotheses include compact connected convex full-dimensional support, a smooth boundary, a positive continuously differentiable density, and the stated growing-neighbor regime. I checked these statements and the observation definition, without certifying every proof detail of that paper. [Published paper](https://proceedings.mlr.press/v32/terada14.html).
- Hashimoto–Sun–Jaakkola's full condition (⋆) includes almost-sure uniform equicontinuity of rescaled stationary masses. The remark immediately following the condition conjectures that this assumption follows automatically from the other conditions. Its explicit componentwise qualification agrees with the obstruction here. Theorem 2.1 and Corollary 2.3 are not an unconditional theorem for the original undirected observation. [Published paper](https://proceedings.mlr.press/v38/hashimoto15.html).
- The synchronization paper uses ordinal/directed neighbor information, despite an intermediate symmetrization. Its empirical demonstrations are not being substituted for the required universal theorem. [Cucuringu–Woodworth, author version](https://arxiv.org/abs/1504.00722v2).

The bump densities used below are not bounded below on their closed supports, and their logarithmic gradients become unbounded near the boundaries. They consequently do not contradict the stronger regularity hypotheses of the cited positive results. The artifact correctly frames them as a necessary-hypothesis diagnostic for an informal unrestricted smooth-density reading, rather than a counterexample within those positive theorem classes. Its bounded literature-search qualification is retained; this review does not assert that no later connected-support theorem exists.

## 2. Finite direction ambiguity

Multiplying the displayed coordinates by ten gives the integer configurations

$$X=(0,10,19,41),\qquad Y=(0,10,21,38).$$

All three distances from each vertex are distinct. Direct sorting gives exactly the outgoing sets stated in the artifact. Only the two arcs from vertex 3 to vertices 1 and 4 differ: one is present in the first configuration and the other in the second. The undirected union graph in both cases is $K_4$ minus the edge joining vertices 1 and 4. The common-neighbor counts for vertex 3 against vertices 1, 2 and 4 are respectively $1,2,1$.

This proves that an exact deterministic inversion from every finite undirected kNN graph to its directed graph is impossible, even with labels, dimension and $k$ known. Strict inequalities make the examples stable under sufficiently small coordinate perturbations. That finite open-set fact is not an asymptotic statistical lower bound under one fixed connected sampling density, and the submission does not claim it is.

## 3. Fixed smooth laws and the graph coupling

The bump is genuinely $C^\infty$ on all of $\mathbb R^d$: the standard function $e^{-1/t}$ for $t>0$, extended by zero for $t\leq0$, is flat at zero, and composition with $1-\|u\|^2$ preserves smoothness. Its integral is finite and strictly positive, so the normalizing constant exists. Both displayed mixture densities integrate to one; the second component's Jacobian is $s^d$ and its coefficient is $1/(2s^d)$.

The supports consist of two closed disjoint balls. Their component-radius ratios are $1$ and $s>1$, so no global similarity, including a reflection or a permutation of the components, identifies the supports. The two probability laws are fixed before $n$ varies.

The common Bernoulli labels and independent latent bump samples give the correct i.i.d. marginals. On $E_n$, a vertex has at least $k_n$ other sampled vertices in its own component. All such distances are at most $2s$, whereas every cross-component distance is at least

$$L-1-s=9s-1>2s.$$

Consequently every outgoing neighbor belongs to the same component. Within a component the coupling multiplies all distances by the same positive factor, so it preserves the entire ranking, not merely connectivity. Directed, union-symmetrized and mutual-kNN observations coincide on this same event. Distance ties have probability zero: conditioning on one or two sample points reduces any relevant equality to a sphere or a hyperplane of Lebesgue measure zero. A consistent common tie rule also suffices for the finite diagnostics.

For $k_n\leq\alpha n$ with fixed $\alpha<1/2$, the two binomial lower-tail bounds and a union bound yield exactly equation (4). In particular, $k_n/n\to0$ eventually satisfies this condition. The coupling inequality then gives the claimed total-variation convergence of the labelled graph laws. No assumption of graph connectivity inside a component is needed: separation alone is sufficient.

## 4. Random-target statistical lower bounds

Marginal graph-law convergence alone would not settle recovery of a random sample-dependent target. The submission supplies the additional joint coupling argument required for that purpose.

For the density ratio, on the fixed positive-probability event $F$ the targets satisfy

$$R_q=s^dR_p,\qquad R_q-R_p\geq\Delta>0.$$

The density values are positive and finite almost surely, since samples lie in the open supports almost surely. One can concretely choose $K$ to be the closed ball of radius $1/2$; then $m/M=e^{-1/3}$ and $\Delta=(s^d-1)e^{-1/3}$ is a valid explicit lower bound. The unknown bump normalizer cancels.

Any graph-only estimator, even randomized, can use the same auxiliary randomness under the coupling. Its two outputs agree on $E_n$. The two closed success intervals of radius $\Delta/3$ are disjoint on $F$. Therefore at least one of the two error events occurs on $F\cap E_n$, and

$$\mathbb P_p(\text{error})+\mathbb P_q(\text{error})
\geq\mathbb P(F)-\mathbb P(E_n^c).$$

No independence of $F$ and $E_n$ was used or is needed. Both error probabilities cannot tend to zero. The exact target is consistent ratio recovery, invariant under one common density multiplier. This does not silently resolve the source's ambiguous phrase about constant factors under an arbitrary fixed-error criterion.

For geometry, the four prescribed labels have probability $1/16$. The latent balls around $\pm e_1/2$ lie strictly within the unit ball and each has positive bump probability. The triangle and reverse-triangle inequalities put both relevant distances in $[3/4,5/4]$. The ratio is therefore at least $3/5$, and the coupling changes it by at least $(1-s^{-1})3/5$. The same two-output argument applies.

The final cloud-reconstruction consequence is valid with the usual nonvacuous alignment convention: an estimated cloud is aligned to the true cloud, and the error is measured in the true cloud's fixed scale. On the specified event, an aligned maximum error $\varepsilon$ changes each distance by at most $2\varepsilon$, while the true denominator is at least $3/4$. For example, for $\varepsilon<1/8$ the estimated denominator is at least $1/2$, and an elementary quotient estimate bounds the ratio error by $(32/3)\varepsilon$. Similarities preserve the ratio exactly. Hence simultaneous cloud consistency would contradict the established positive-probability ratio gap. An error definition permitting the true cloud itself to be shrunk arbitrarily without normalization would be vacuous and is not the convention used here.

## 5. Reproducible independent controls

The submitted verifier was read and replayed in a separate directory against the frozen artifact. All **11,803** assertions passed, and its receipt reproduced **byte-for-byte**.

The fresh standard-library checker imports neither the submitted checker nor any external producer software. All **124,836** independent exact assertions passed. They include:

- an integer-coordinate reconstruction of the ambiguous finite graph and all strict distance orders;
- all binary component assignments on modest deterministic interleaved clouds in dimensions 1, 2 and 3, for three nonintegral/integral scale choices;
- **3,834** component-labelled clouds and **6,912** admissible-$k$ directed-graph comparisons, including union and mutual observations;
- exact binomial event probabilities for $4\leq n\leq80$, a rational Chernoff bound obtained from a different transform, and the intersections with the fixed first two/four labels;
- Jacobian normalization, scale-free target gaps, disjoint success intervals and the geometric event's endpoint inequalities.

Run from the review directory:

```sh
python independent_checks.py > replayed_independent_results.json
cmp independent_results.json replayed_independent_results.json
python author_replay/verify.py > replayed_author_results.json
cmp author_replay/verification.json replayed_author_results.json
```

The continuous bump's normalization, all-$n$ coupling, concentration and consistency contradiction were checked analytically above. Finite controls do not establish those conclusions by extrapolation.

## 6. Final scope and publication recommendation

The partial is correct without a mandatory mathematical repair. Preserve **unsolved 2/5**, all source qualifications and the prior componentwise-identifiability attribution. In particular, do not promote this result to a connected-support impossibility theorem, an exact asymptotic direction-recovery obstruction, or a resolution for arbitrary $k_n$ and arbitrary interpretations of constant-factor recovery.

The eight publication files are listed in `review_summary.json`. Source PDFs and rendered audit images are intentionally excluded; `source_manifest.json` records the inspected files and primary links.

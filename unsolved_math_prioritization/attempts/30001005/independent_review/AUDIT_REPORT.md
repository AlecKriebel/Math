# Independent source and scope audit for 30001005

Audit date: 3 October 2026 UTC. Target: OWR-2045-001, rank 445.

## Disposition

**HOLD for an unqualified resolution of the original problem or an unqualified `already_solved` classification. PASS for the precise classical counterexample to universal short-time smoothing among locally finite integral Brakke flows, with noncompact initial data allowed.** The mathematical obstruction is valid. It does not, by itself, resolve an existential smoothing problem, a specified selected-flow problem, or self-expanding asymptotics considered separately.

The frozen manifest correctly says `original_selected_flow_problem_resolved: false`. Preserve that field. The public gate's proposed `already_solved` classification is defensible only if the project explicitly adopts the literal universal-Brakke interpretation as the entire target. It must not silently become a resolution of Ilmanen's original questions.

## Frozen input and reproducibility

The audited directory was `rank445-30001005/public`. Its MANIFEST.json SHA-256 is:

`5ad6881a360d7d391e1457fae4fd6db3af667d69bee1117bfc6006fa3ccba74e`

All seven listed payload hashes match. The standard-library `verify.py` ran successfully and its output agrees with `verify_results.json`. This checks algebra and dimensions, not source scope. No frozen public file was edited. No remote write or new research campaign was performed. The cancelled source-download operation was not retried. Available web text reads were sufficient for the source comparison; web PDF screenshots failed, so no visual PDF verification is claimed.

The cached problems.json SHA-256 independently matched:

`04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf`

I read its complete record for ID 30001005. I did not independently re-run the separate live repository/prior-attempt investigation.

## Exact catalogue target and quantifiers

The pinned statement is:

> Let $M_0\subset\mathbb R^{n+1}$ be a hypersurface with isolated point singularities modeled on regular hypercones, and let $(M_t)_{t\geq0}$ be a mean-curvature flow with initial data $M_0$. In dimensions $n\geq7$, does $M_t$ evolve by self-similar expansion asymptotically near each singular point and become smooth for a short positive time?

This fixes a flow in the statement. It does not say that the initial surface *has some* smoothing evolution. The certificate's opening paraphrase, “has a mean-curvature evolution that ...,” changes that quantifier and should be corrected. Neither the catalogue statement nor its copied original statement specifies compactness, Brakke flow, level-set flow, or outermost selection. The catalogue inserts the explicit high-dimensional restriction into its cleaned statement and combines the source's two questions into one conjunction.

Write A(M,flow) for the asymptotic-expander property and B(M,flow) for short-time smoothness. The packet proves an example with not-B in one admitted Brakke class. That refutes a universal assertion that every such datum and admitted flow satisfy A and B. It does not refute the assertion that every datum admits some flow satisfying A and B: one nonsmoothing flow does not exclude a different smoothing flow. Nor does it refute A; the example is exactly dilation invariant.

## Original OWR source

Source: Ilmanen, Relative Expander Monotonicity and MCF with Singular Initial Data, printed p.1937, PDF page 5 of the [official report](https://ems.press/content/serial-article-files/46179).

The text says “Consider a mean curvature flow” and separately asks about asymptotic expansion and smoothing. It introduces neither a compactness assumption nor an explicit weak-flow definition. It announces self-expanding tangent flows in every dimension (Theorem 1), construction with compact-replacement-minimizing expanders in every dimension (Theorem 2), and short-time smoothness of **“The flows of Theorem 2”** when n ≤ 6 (Theorem 3).

Thus Theorem 3 has a selection requirement; it does not assert that every arbitrary weak flow smooths. The one-page announcement is not enough to identify the exact class intended in every preceding sentence. The report also does not formulate an explicit n ≥ 7 open conjecture. Its dimensional cutoff is not proof that an unrestricted high-dimensional assertion is open. The packet properly treats the all-dimensional announcement cautiously, rather than supplying a published proof that was not read.

## Check against the 2024 paper

Source: Chodosh, Daniels-Holgate, Schulze, [Mean curvature flow from conical singularities](https://link.springer.com/article/10.1007/s00222-024-01296-8), Theorems 1.2–1.4, §§1.2, 2.2, 2.5–2.6.

Theorem 1.2 gives short-time smoothness of the outermost flows for 2 ≤ n ≤ 6. Theorem 1.3 identifies their forward limits with the outermost expanders. Theorem 1.4 adds uniqueness when the cone does not fatten. The paragraph following Theorem 1.2 permits higher dimensions when the outermost expanders are smooth. Section 2.6 explicitly allows possible singular sets of dimension n−7 in higher-dimensional outermost expanders.

The introduction discusses compact initial surfaces, but the displayed theorems do not list compactness, and §2.3/footnote 3 expressly accommodates noncompact data. Do not infer a blanket compactness restriction. This paper's smooth-cone definition uses a smooth embedded closed link; the Simons cone qualifies. Its strategy avoids forward monotonicity because of difficulties making that argument rigorous. These results do not prove universal smoothing for arbitrary Brakke flows.

## Independent analytic verification

Let C = {(x,y) in R4 × R4 : |x|² = |y|²}, and μ = H7 restricted to C.

1. **Admissible geometry.** Away from zero, the defining function has nonzero gradient. The link is S3(1/sqrt(2)) × S3(1/sqrt(2)), a smooth closed embedded six-dimensional hypersurface in S7. C is exactly invariant under every positive dilation, so its conical modeling is exact. It is seven-dimensional and noncompact. The relevant dimension is therefore n = 7 in the catalogue, whereas the notation in the 1998 notes uses n for ambient dimension.
2. **The vertex is genuinely singular.** If C were a differentiable embedded seven-dimensional hypersurface at zero, every v in C would lie in its tangent plane: the curve s -> sv, or the tangent-cone definition, gives this conclusion. The vectors (e_i,f_i) and (e_i,-f_i), i = 1,...,4, lie in C and span R8. Hence C cannot have such a tangent plane. There are no other singular points.
3. **Local mass.** With L = C intersect S7, H7(C intersect B_r) = H6(L) r7/7, so μ is locally finite and defines a multiplicity-one integral varifold. The finite-time/local-space integrability condition in the Brakke definition follows immediately once H = 0.
4. **Mean curvature off zero.** Put ρ = |(x,y)| and ν = (x,-y)/ρ. This is a unit field on R8 minus zero and is normal to C. Its ambient divergence is −(|x|²−|y|²)/ρ³. Because <D_νν,ν> = 0, tangential and ambient divergences agree on C. Both vanish there.
5. **No vertex contribution.** Apply first variation on C minus B_ε using a compactly supported C1 field X. The artificial inner-boundary term is bounded by ||X||∞ H6(L) ε6. The omitted tangential-divergence integral is bounded by a constant times ||DX||∞ ε7. Both vanish as ε tends to zero. Thus δV(X) = 0, including at the vertex, and the generalized curvature vector is zero.
6. **Full Brakke inequality.** Set μ_t = μ for all t ≥ 0. For a nonnegative C1 compactly supported space-time test function φ, differentiation under the locally finite integral gives the time-integral of ∂_tφ exactly. The curvature terms −|H|²φ + H·∇φ vanish. Therefore the integrated Brakke inequality holds with equality for every finite time interval, including intervals beginning at zero. There is neither an initial-data mismatch nor mass dropping.
7. **Persistence at all scales.** Every positive-time support is C, singular at zero. Moreover λ7 μ(λ^-1 A) = μ(A), so every parabolic dilation of the static flow is exactly itself. There is no positive-time neighborhood, however small, in which the vertex becomes regular. As an optional quantitative check, H6(L) = π4/2 and ω7 = 16π3/105, giving vertex density 15π/32 > 1 at every spatial scale. The checker records the correct rational coefficient, but it does not itself derive these sphere-area constants.
8. **No contradiction to self-similarity.** C = sqrt(t) C, and x-perp = 0 on the regular part. The stationary cone satisfies the expander equation in that sense. A singular self-similar flow is not a smooth self-expander.

These observations prove the advertised narrow obstruction without using area minimization, level-set uniqueness, or any unproved published theorem.

## Classical attribution

Source: Ilmanen, [1998 lecture notes](https://math.jhu.edu/~js/Math745/ilmanen.mcflow.pdf), printed pp.41–42, PDF pages 43–44. Page 41 gives the stationary product cones C_(p,q), including p = q = 4, and records their classical minimizing status. Page 42 says “Since C is stationary, one evolution is given by” the constant family M_t = C. This directly verifies that the stationary-evolution principle is classical. The nonuniqueness proposition there concerns non-area-minimizing cones; it does not supply a uniqueness theorem for the Simons cone. The packet is right not to rely on the stronger uniqueness claim from an in-preparation publication summary.

A useful scope diagnostic is that the same stationary construction with R2 × R2 already gives a nonsmoothing Brakke flow in hypersurface dimension three. Therefore a universal-Brakke reading would also conflict with the source's low-dimensional smoothing language. This reinforces the need to preserve its selection qualifier. It does not undermine the valid high-dimensional example.

## Required repairs before publication or queue closure

1. Replace the certificate's existential opening paraphrase with the actual given-flow formulation. Include the pinned statement or an exact, quantifier-preserving summary.
2. Make every headline and classification say that the refuted assertion is universal smoothing in the unrestricted locally finite integral-Brakke class. Record the counterexample dimension n = 7; a single such dimension refutes the proposed universal n ≥ 7 assertion, without claiming a separate result for every dimension.
3. Retain `original_selected_flow_problem_resolved: false`, no novelty claim, and zero proof-attempt turns. Do not change the queue to an unqualified original-problem resolution merely because the conjunction in a broadened paraphrase is false.
4. Correct the source-scope narrative if it implies the OWR abstract explicitly specified a modern outermost or Brakke class. It did not. Its Theorem 3 does explicitly restrict to the flows constructed in Theorem 2.
5. Do not turn a missing selection proof into a claim that the selected problem is false, or turn a missing high-dimensional theorem into a claim that it remains open. This audit establishes neither universal uniqueness nor a compact-data counterexample.
6. If the intended task is a substantive remaining selected-flow question, first freeze its actual flow class, hypotheses, dimension range, convergence mode, and requested conclusion. The already proved low-dimensional and smooth-outermost-expander regimes must be excluded from an open-problem claim. A possible remaining question about forward asymptotics when outermost expanders can be singular is not answered by this packet, but its current literature status has not been established in this bounded audit.
7. If a genuinely open, precisely sourced target survives that gate, the author must undertake the requested substantive attempts. The current 0/5 is a prior-result verification count; it is not evidence that such an open target has been attempted or solved. Conversely, there is no reason to invent five proof attempts for the already verified narrow false assertion.

## Recommended final label

`classical_obstruction_verified; original_scope_unresolved; publication_or_queue_resolution_hold`

The report may be released as a carefully labeled source correction and classical counterexample after the editorial repairs. Treating it as completion of an unspecified original selected-flow problem is not supported.

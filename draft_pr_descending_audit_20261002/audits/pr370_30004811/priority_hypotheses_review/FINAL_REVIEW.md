# PR370 independent priority and theorem-hypothesis audit

**Verdict: PASS for the frozen packet's expressly scoped claims. Mandatory fixes: none found.** The standard nonnegative-scalar-curvature/empty-or-minimal-boundary conjecture is a credited prior result. The unrestricted literal all-AF sentence is false, and TURN_1 supplies a valid smooth complete boundaryless counterexample. This review does not certify historical novelty, determine the exact global capacity-volume mass, or prove any broader low-regularity/all-sign/multiple-end theorem.

Frozen head: `567c2e493854b32d0cd325ad96e4c5b69c9c1e1b`. Base: `efd29c05204703acca9a0860812f54b94fae54b1`. Family: exact original source, priority, and hypothesis coverage, with adversarial counterexamples to unsupported generalization. All19 snapshot files (18 problem files plus QUEUE) match the frozen head. The10 frozen author files match author commit `1901d52ea8b47b4dd3c843cb2e02be2c520da7cb`. The two integration parents match the publication README's claim. Work stayed isolated in this review directory on main; no candidate edits, installs, Git mutations, service mutations, or external communication occurred.

## Independence and seals

The seven exact primary PDFs were downloaded independently, before opening any candidate source gate, proof, program, result, state, final report, prior review, root finding, or sibling finding. The source-first baseline was sealed at **2026-10-03 11:28:27 UTC**, SHA256 `e6915c94ef5a69a77082574eb0fc5ba42d086df0082cbf10e34bc72d3291364d`. It recorded the original conjecture, source definitions, exact theorem assumptions and versions, success/falsification criteria, and an independently derived displaced-negative-mass-ball mechanism.

Only TURN_1 was then opened for candidate mathematics. Its entire construction, actual metric energy, harmonic potential, flux, nested exhaustion, volume error, strict gap, and logical scope were reconstructed before opening any candidate program/output/state/final/prior review. The mathematical reconstruction and verdict were sealed at **2026-10-03 11:31:20 UTC**, SHA256 `1d579436e77b7e134c8a335eaaba9ee83919866e05448e35873898c47d3d726d`. The sealed mathematical verdict was pass. Later packet/software inspection confirmed rather than generated that conclusion. No root or sibling findings were used.

See SOURCE_BASELINE.md, SOURCE_BASELINE_SEAL.json, MATH_RECONSTRUCTION.md, and MATH_VERDICT_SEAL.json. The seals preserve those pre-inspection records without retroactive rewriting.

## Exact question and source coverage

The [official OWR report](https://ems.press/content/serial-article-files/46918), printed pp.2255–2258, states the conjecture on printed2257/PDF101. I also rendered and visually checked that page. The report's [metadata](https://ems.press/journals/owr/articles/8415343) confirms that the workshop ran29 August–4 September2021 and publication was26 November2022. The short report's conjecture uses a broad all-AF phrase. Its surrounding theorems carry curvature, boundary, or mass-sign conditions. Jauregui's [full underlying paper](https://arxiv.org/pdf/2002.08941), p.4 after Corollary8, explicitly conjectures the arbitrary-exhaustion upper bound under Theorem6's R≥0 and empty/minimal-boundary conditions. The candidate correctly keeps these two readings separate.

The exact normalized capacity is `(1/(4π))inf∫|∇ψ|²dV`, ψ=0 on K and ψ→1 at infinity. The report's prose omits the prefactor; its displayed isocapacitary inequality fixes the intended normalization. Jauregui equation(3) states it explicitly. Euclidean radius-R balls therefore have capacity R. The mass is the **supremum over all compact exhaustions** of the **limsup** of `r_V(K)−cap(K)`, not merely a limit along coordinate balls. Jauregui Lemma10 identifies this with the cubic-deficit expression used by BFM at p=2.

The strongest standard original-class conclusion justified by the exact sources is:

> For a smooth connected complete one-ended3-manifold with `g−δ=O₂(r⁻τ)`, τ>1/2, R∈L¹, globally R≥0, and compact boundary empty or smooth minimal, the capacity-volume mass over all compact exhaustions equals the finite ADM mass.

The credited proof chain is

`m_ADM ≤ m_CV ≤ m_iso = m_ADM`.

The first inequality is Jauregui2020 Theorem5 (which only needs eventual nonnegative scalar curvature). The middle is BFM's [published SIGMA2023 Theorem5.6](https://arxiv.org/pdf/2305.01453v2), at p=2, or directly Theorem5.5 at p=2. The last is the established Huisken-isoperimetric equality, explicitly restated with the correct boundary scope in Jauregui2020 Theorem2 and [JLU2024 Theorem6](https://arxiv.org/pdf/2408.08871). Jauregui–Lee's [paper](https://arxiv.org/pdf/1602.00732) provides the underlying proof. The separate Chodosh–Eichmair–Shi–Yu attribution is stated in Jauregui's primary source and BFM's bibliography; this audit did not rely on their independent proof as an additional theorem input.

The p=2 capacity convention matches under v=1−ψ. The cubic mass `[V−(4π/3)c³]/(4πc²)` matches `r_V−c` after the exhaustion equivalence, not by claiming a pointwise equality. Capacity diverges along an AF exhaustion by monotonicity and coordinate-ball comparison. The candidate makes these distinctions correctly.

Smooth supersets cover arbitrary compact competitors. For any compact K, choose a smooth capacity test function with energy as close to cap(K) as desired and take a regular superlevel set just below its value on K. This gives a smooth bounded superset E with cap(E) arbitrarily close from above. Volume increases, so `r_V(E)−cap(E)≥r_V(K)−cap(K)−ε`. Choose ε→0 along an exhaustion; nesting can be enforced by selecting a sufficiently late original member before each approximation. This validates the packet's smooth-competitor bridge rather than assuming that every exhaustion already has smooth boundaries.

## Conditions that must not be erased

| Source statement | Exact material assumptions/range | Audit disposition |
| --- | --- | --- |
| Jauregui2020 Th5 | Smooth O₂ AF, τ>1/2, R integrable; R≥0 outside compact set | Only a lower bound, not all-sign equality |
| Jauregui2020 Th7 | Harmonic flatness, m_ADM≥0 | Its final volume upper bound cannot be applied to negative mass |
| BFM2023 Th1.3 | Smooth complete single end; C¹_τ AF, τ>1/2; R≥0; empty/smooth compact minimal boundary; **H₂(M,∂M;Z)=0**; 1<p≤2 | The topology condition is real; the candidate does not drop it |
| BFM2023 Th5.6 | C⁰ AF, compact possibly empty boundary; 1<p≤2 | Broader upper comparison with no R or H₂ condition; this is the candidate's middle inequality |
| Benatti2025v2 Th1.2 | Smooth complete connected orientable one end; R≥0; positive Euclidean isoperimetric constant; smooth compact minimal boundary allowed; interior compact minimal surfaces excluded (footnote permits confined ones via excision); p∈[1,3) | Capacity/isoperimetric equivalence, not an unrestricted ADM theorem |
| BFM Penrose v5 Th1.4 | Complete C¹_τ AF, τ>1/2; R≥0; empty/smooth compact minimal boundary | Isoperimetric/ADM equality; current numbering is1.4, not the earlier4.13 |

The original smooth C² class is all that PRIOR_RESOLUTION claims to need. The candidate does not infer full all-p/all-C⁰/all-sign equality from these statements. Nor does it apply Benatti's theorem to the negative example. Indeed, the example has a positive Euclidean isoperimetric constant from uniform equivalence to Euclidean space, but R≥0 fails; the isoperimetric-constant assumption alone cannot rescue that attempted application.

Benatti's [v2 Section3](https://arxiv.org/pdf/2511.11155v2) identifies the sign-sensitive step in BFM2023(5.9)–(5.11). Bounding the correction integral from above is legitimate only with nonnegative multiplying mass parameter. In the claimed standard class, `m_iso=m_ADM≥0`; taking m>m_iso handles the zero case. JLU2024 supplies independent nonnegativity for every C⁰ AF end, without curvature assumptions; Benatti supplies a sign-aware refinement in a wider setting. The candidate documents the issue and uses it within a scope where the necessary sign is justified. This is not a false prior-resolution claim.

## Counterexample verification

The smooth cutoff metric `g=(1−χ(r)/r)⁴δ` on R³ is Euclidean near zero and uniformly satisfies `(1/16)δ≤g≤δ`. It is complete, connected, one-ended, orientable, and boundaryless. The end is exactly mass−2 Schwarzschild, so it has O₂(r⁻¹) decay and ADM−2. Its scalar curvature is smooth and supported in the transition annulus, hence integrable. It is negative somewhere: the compactly supported Δu integrates to the positive flux4π at infinity. This independently verifies the precise failed global assumption.

The balls `K_R=B((R/2)e₁,R)` are smooth compact nested sets, contain B(0,R/2), and exhaust R³. Their exterior lies in r≥R/2≥3. On that exterior, u and the Euclidean potential f_R are harmonic. The true metric potential is f_R/u because `div(u²∇(f_R/u))=uΔf_R−f_RΔu=0`. The metric energy density is u² times Euclidean gradient energy. Boundary values, finite energy, and uniqueness apply. Normalized flux gives capacity **exactly R−1**, without approximating the metric energy by Euclidean energy.

The solid-ball Newton integral is `2π(R²−d²/3)`, so at d=R/2 it is11πR²/6. The smooth core changes the volume by a fixed constant; the complete conformal remainder is O(r⁻²) and integrates to O(R). Thus `V_R=(4π/3)R³−11πR²+O(R)`, and `r_V=R−11/4+O(R⁻¹)`. The admitted exhaustion yields deficit−7/4 and hence `m_CV≥−7/4>−2=m_ADM`. An exact global value or optimizer is unnecessary and is not claimed.

Jauregui equation(41) supplies the credited harmonic conformal capacity transformation before that source imposes m≥0 on its separate volume rearrangement. Its use at m=−2 is legitimate; using the final nonnegative-mass upper bound would not be. The candidate credits the identity and classical Newton calculation, and explicitly leaves historical novelty unverified.

I also independently derived the general fixed-displacement family `m(1−λ²/2)`. At λ=0 it returns the centered mass; at m=0 it returns0; at m>0 it is≤m; at m<0 and λ>0 it is>m. A tangency-approaching nested exhaustion can strengthen the lower bound to m/2, but this is unnecessary for the packet and does not alter its validity. The exact mass remains uncomputed.

## Reproduction and bindings

All four frozen programs were inspected and run without modifying their bytes:

- check_turn_1.py: PASS,5,529 assertions; output byte-identical to TURN_1_CHECKS.json.
- review/check.py with the packet path and seven independently downloaded source PDFs: PASS,3,128 assertions; output byte-identical to review/CHECKS.json.
- review/portable_check.py: PASS both without raw PDFs (count0) and with them (count7).
- verify_publication.py: PASS both without raw PDFs (count0) and with them (count7).

The author manifest has9 bound files, the review manifest3, and the publication manifest17; every size and SHA256 matches. All seven independent PDF downloads match SOURCE_MANIFEST exactly. The public checks correctly label their algebraic scope; assertion totals are not treated as proofs of global capacity minimization or literature theorems. Portable behavior does not falsely report source hashes checked when they are absent. The original path/source requirement is deliberately preserved.

The separate `distinct_controls.py` integrates the **entire rational Schwarzschild volume tail** using radial solid-angle fractions, leaving the arbitrary fixed core volume as a parameter. It recovers the leading−11πR² term and the linear remainder coefficient `(30π+(45π/2)log3)R`; it verifies that changing the core alters radius only at O(R⁻²). It also computes metric flux directly on the displaced boundary, rather than using the candidate's far-field coefficient. All15 final controls pass. Its first auxiliary sign test omitted the exterior domain r>1; this caused an undecidable SymPy relation, not a candidate defect. The failure and domain correction are preserved in CONTROL_FIRST_RUN_FAILURE.md.

REPRODUCTION_RECEIPT.json, DISTINCT_CONTROLS_RECEIPT.json, and BINDING_AND_HISTORY_RECEIPT.json provide checkable receipts. The public manifest excludes its own self-binding and all raw PDFs/text/images/private reproduction files.

## Priority, historical claims, status, and remaining gaps

Exact priority dates were independently checked on arXiv and publisher metadata: Jauregui first posted2020-02-20; BFM first posted2023-05-02 and published/finalv2 on2023-11-10; JLU first posted2024-08-16; Benatti first posted2025-11-14 and v2 on2025-12-24. The supplied BFM Penrose unversioned PDF is v5 dated2024-11-20, with first submission2022-12-20; its publication is CPAM78(2025)1042–1085 as credited in Benatti's bibliography. The publisher DOI URL failed in the browser tool; the exact v5 theorem was read directly and its version history checked. Earlier theorem4.13 numbering in BFM2023 was not silently transferred to v5.

The imported frozen catalog/assessment records incorrectly call the lower bound missing; Jauregui's Theorem5 already establishes it in the relevant class. The candidate's correction of direction is supported by the original primary source. Local pre-October2 all-ref path and exact-term histories are empty. Four read-only GitHub PR searches for the ID/problem number/capacity-volume/isocapacitary, constrained to creation before October2, also return0. These partly corroborate the historical source gate. They cannot reconstruct deleted refs, the unavailable problem page, a private imported dataset, unpublished work, or the precise old remote search state. This audit does not certify every historical negative-search sentence, and it does not turn absence of a search hit into novelty. The candidate itself makes no such certification.

QUEUE's only changed cells are the target's status and turns (`already_solved`,1/5). PUBLICATION_README prominently explains that this status concerns the standard physical class and accompanies a separately scoped negative literal result. Its current publication status explicitly supersedes historical pending-review language in preserved author snapshots. No false new-positive-theorem, merger, CI-success, or exact-mass claim is found.

**Mandatory fixes: none.** Preserve the two scopes, explicit credited inputs, normalized all-exhaustion mass, and non-certification of novelty. Exact m_CV for the negative metric and historical novelty of its explicit displaced-ball observation remain unestablished and are outside the frozen claim. No broader literal all-AF equality or nonsmooth/all-p/multiple-end theorem should be inferred from this pass.

# Independent priority review: exact Oberwolfach target

**Disposition: no earlier recorded full three-summand answer was verified in this bounded search.** The proposed negative answer fits the original target. Publication should prominently credit the older mixed-kernel generator mechanism, give the three-summand proof, and avoid firstness or current-global-openness claims. There is a journal-body access limitation below; this report is not a completeness certificate for the literature.

## Independence and evidence order

This family first read the original contribution and searched its mathematical history, without reading the candidate proof. `INITIAL_TARGET_ASSESSMENT.md` was sealed at SHA256 `1361332a57717bb2fb36e9d300957eb08db390b2b465f9fd38c3430e6a5574ef`. Only afterward was the complete `../../REVIEWED_PROOF.md` read and its expected SHA256 `7f63c1f6e4f79a78b979903db59e8030a8222266a65d296a4a6fc1a29a6e2e1b` confirmed. The parent brief disclosed the proposed fields and a passed math-review verdict; that verdict was not evidence for this priority decision. No old AUDIT, SOURCE_AUDIT, acceptance, root review, or sibling report was read. No person was contacted and no PR, tracker, deposit, or Git ref was changed.

## What the source actually asks

I read the complete Laghribi contribution, joint with Aravire and O'Ryan, printed pp.248–251 of [Oberwolfach Report 5/2016](https://ems.press/content/serial-article-files/46609), and inspected a render of Question 2 on p.251. It asks the equality of the compositum kernel with the sum of the individual L/F, K/F, and F(B)/F kernels, with L/F any finite purely inseparable extension and B anisotropic over L. It places no exponent-one restriction on L and no exclusion of one-fold B or index n=1. The proposed degree-four, exponent-two L and binary bilinear Pfister B therefore lie within scope.

The report defines F(B) by the projective quasilinear quadric of v↦B(v,v). For B=⟨1,t⟩ this is precisely F(√t), a zero-dimensional integral quadric. This is a legitimate one-fold Pfister form, not a zero-fold or nonsingular quadratic Pfister substitution. The older affine convention adds a transcendental variable and does not change these restriction kernels.

## Prior art that must be credited

The primary author manuscript of Aravire–Laghribi–O'Ryan, [*Cohomological kernels of mixed extensions in characteristic 2*](https://laghribi.perso.math.cnrs.fr/cohom-kernels.pdf), dated 15 August 2019, is indexed by the [author publication list](https://laghribi.perso.math.cnrs.fr/research.html) as Journal of Algebra 542 (2020), 249–276, [DOI10.1016/j.jalgebra.2019.09.012](https://doi.org/10.1016/j.jalgebra.2019.09.012). It explicitly announces higher-exponent mixed nonsplitting. Its Definition1.3, Lemma3.1, and Theorem1.4 already supply the candidate's class-construction mechanism; I read the whole relevant §3 proof, not just an abstract. §6 Proposition6.1 and Example6.2 instead concern purely inseparable composita/regroupings.

Here is the exact specialization, also recorded in `PRIOR_ART_BRIDGE.md`. In the older notation take n=m=1, β⁴=b, f₀=1, f₁=z, and f=1+β²z. The nonzero generator term of G¹_L(1) is

    (β²z/(1+β²z))² dlog z = bz²/(1+bz²) dlog z.

Choose the old Artin–Schreier parameter a=s⁻⁴. It defines the same quadratic field as s⁻¹ since s⁻⁴+s⁻¹=wp(s⁻²+s⁻¹). Thus ξ is an exact member of the published generator family. The class and higher-exponent mixed obstruction cannot be presented as newly invented mechanisms.

The earlier [*Graded Witt kernels of the compositum of multiquadratic extensions with the function fields of Pfister forms*](https://laghribi.perso.math.cnrs.fr/Witt-kernels%28new-version%29-2.pdf), Journal of Algebra 449 (2016), 635–659, gives the positive exponent-one result in Theorem1.2. I read its introduction, hypotheses, and complete §5 proof. Its reduction explicitly uses L²⊂F; the quartic example does not satisfy that premise. Its Question8.1 is the different quadratic-Pfister function-field problem, not Question2 of the report.

## Why this is not yet evidence of an earlier full target answer

A two-field kernel larger than the sum of its two individual kernels need not remain larger after a third subgroup is added. ALO2019 Theorem1.4 does not, by its statement, exclude the F(B)/F summand. Neither its complete §3 proof nor complete §6 example discussion, the relevant portions inspected here, records that extra exclusion for an independent anisotropic bilinear Pfister slot. An additional survival argument is required. I did not locate an earlier theorem, corollary, or example already recording that exact target deduction. This is a bounded negative search result, not a proof that none exists.

The candidate provides the missing survival argument directly. Under restriction to M=L F(B), both the L/F and F(B)/F summands vanish. Every K/F summand has cyclic form [s⁻¹,c), with c in the base field. Consequently membership would require [s⁻¹,(1+β²z)/c)_M=0. Completing at s, the Artin–Schreier quadratic extension is totally ramified and its unit norms have square residues. After removing the valuation using N(θ⁻¹)=s, one obtains

    (1+β²z)/c₀ ∈ 𝔽₂(β,z,γ)²,   c₀∈𝔽₂(b,z,t)*,   γ²=t.

Put R=𝔽₂(β⁴,z²,γ²), S=𝔽₂(β²,z²,γ²). Every c₀ is u+vz with u,v∈R; 1,z are S-independent. A purported identity 1+β²z=q(u+vz), q∈S*, forces β²=v/u∈R, impossible by the odd β²-valuation. This excludes every c, not a finite sample. The independent t-slot preserves the obstruction; choosing B=⟨1,z⟩ instead would kill ξ immediately. That exact three-summand exclusion is the mathematically relevant target application.

No citation below is offered as prior proof of that exclusion. Established cyclic-algebra/norm/valuation tools remain established tools even when newly assembled for a specific question.

## Later literature, corrections, and access limits

The public query log records 53 actual search inputs, including exact title, exact question, three-summand, mixed-generator, citation, correction, and later-author searches. Several broad queries returned mostly unrelated uses of “kernel”; these are recorded as low-yield searches and do not strengthen novelty evidence. No search result snippet was treated as a theorem.

I examined the primary author bibliography through its 2026 entries. Two accessible 2025 papers of Laghribi–Maiti, [part I](https://arxiv.org/abs/2503.16859) and [part II](https://arxiv.org/abs/2504.15957), were screened by their abstracts, introduction/main-result discussion, references, and whole-text term searches. They concern rational-function-field residue/exact sequences and a norm theorem; no explicit answer to this three-kernel question was found in those screened portions. Their complete technical proofs were not audited. Likewise, the abstract and introductory scope of [Aravire–Jacob–O'Ryan, PJM306 (2020), 385ff](https://msp.org/pjm/2020/306-2/pjm-v306-n2-p01-s.pdf) concern purely inseparable kernels and higher Witt coefficients; this was a scope screen, not a full paper review.

The [publisher abstract](https://www.tandfonline.com/doi/abs/10.1080/00927872.2019.1686510) and [2023 author conference abstract](https://comca2023.ucn.cl/wp-content/uploads/2023/08/CONFERENCIASCOMCA.pdf) for *Cohomological kernels of non-normal extensions in characteristic two and indecomposable division algebras of index eight* describe quadratic/quartic purely inseparable extensions over a separable quadratic subfield. The full journal PDF returned HTTP403. It was not inspected, and potentially relevant body-level overlap remains unresolved. Its advertised mixed-generator setting overlaps prior machinery; an abstract alone does not verify or rule out an exact-target discussion.

The final ScienceDirect 2020 mixed-kernel PDF also returned HTTP403. HAL returned an HTML challenge rather than a mathematical PDF. Hence the full proof inspected is the dated author manuscript, not an authenticated comparison against final journal pagination or edits. The [2022 transfer paper](https://doi.org/10.1016/j.jpaa.2021.106930) was accessible only at indexed publisher-abstract level here; direct full-page access returned403. No body-level exclusion is claimed for it. No correction was located by the recorded searches; this does not certify that no correction exists.

## Recommendation

Continue the original review/publication process if the other mathematical and priority families agree. Frame a concise note as an explicit counterexample answering the original Question2, with the direct all-three-summand nonmembership proof. Credit ALO2019/2020 at the abstract/introduction level for the exact mixed-generator family and already-known two-field failure. Avoid “first counterexample,” “previously unknown mixed obstruction,” “still open until this work,” or any causal-independence claim. State the bounded priority/access limitations in the supporting audit. No earlier verified full-target result justifies a skip from this family's evidence alone.

Completion: 100% of this assigned bounded target/history audit; this percentage does not measure literature completeness or mathematical discovery.

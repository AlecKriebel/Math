# Priority audit: OWR-14298367-006

Audit date: 22 September 2026 (America/Los_Angeles). Publication cutoff: that date.
Status: **The unqualified originality gate does not pass.** The scalar criterion is explicitly prior art, and the full Banach-valued amplification is a short consequence of prior theorems. No source explicitly stating the exact composition-operator answer was located in this search. These are different findings: the latter does not establish priority for the former.

## What can responsibly be claimed

The candidate can supply a correct affirmative answer to the question recorded on p.1083 of [Oberwolfach Report 19/2024](https://publications.mfo.de/bitstream/handle/mfo/4214/OWR_2024_19.pdf). The question indeed asks for arbitrary prescribed complex scalar sets in the bounded-distortion dissipative setting. The priority search does **not** support advertising a new scalar criterion or an independent new amplification theorem. At most, it supports a carefully attributed note identifying the application of older results to that question, with a self-contained proof if useful. Whether this observation itself merits a research publication is an editorial judgment, not something a negative search certifies.

The audited claim must retain separability of the underlying space; the proof audit handles that scope issue separately.

## Decisive antecedents

1. **Arafat Abbar (2019), Theorem A, p.74, and Theorem 2, p.75.** [Publisher record](https://bulmathmc.enu.kz/index.php/main/article/view/55), [primary PDF](https://bulmathmc.enu.kz/index.php/main/article/download/55/93/364). Published 30 December 2019, vol.129(4), pp.73–79. Theorem A already characterizes arbitrary-Γ supercyclicity of the bilateral translation on a weighted scalar sequence space. Its proof obtains one sequence of times and allowed scalars working at every fixed coordinate. Theorem 2 supplies the corresponding Γ-supercyclicity criterion for operators on Banach spaces. Together these immediately give the candidate's vector-valued implication, as checked below. Theorem A should not be confused with Theorem 1, which states the earlier Salas results. Primary publisher text was inspected through indexed web retrieval; local download failed DNS.

2. **Arafat Abbar and Yulia Kuznetsova (2020/2021), Theorem B.** [arXiv:2005.11230](https://arxiv.org/abs/2005.11230), first posted 22 May 2020, v2 dated 28 October 2020; published in J. Math. Anal. Appl. 495(1), 124709 (2021), [DOI](https://doi.org/10.1016/j.jmaa.2020.124709). Theorem B appears on pp.3 and 21–23 of the downloaded preprint. It characterizes arbitrary-Γ dense families of translations when the generated subgroup is abelian. Applied to the discrete groups Z and Z² it independently implies the entire amplification statement, by the explicit reduction below. This route avoids reliance on the abbreviated 2019 criterion proof.

3. **Evgeny Abakumov and Arafat Abbar (2023/2024).** [arXiv:2303.12230](https://arxiv.org/abs/2303.12230), posted 21 March 2023; [journal record](https://www.sciencedirect.com/science/article/abs/pii/S0022247X24002154). The introduction explicitly credits the arbitrary-Γ bilateral-shift criterion to Abbar's 2019 paper. Theorem A establishes a stronger criterion using a nonzero projective-orbit limit point. This is independent confirmation that the candidate's scalar by-product cannot be claimed as new.

## Checkable deduction from the 2019 results

Put ω_j = c_j^(1/p). The prior scalar theorem, including the diagonal selection in its proof, yields strictly increasing n_k and λ_k in Γ\{0} such that for every j in Z,

    |λ_k| ω_(j−n_k) → 0,
    |λ_k|^(−1) ω_(j+n_k) → 0.

For the candidate's E-valued space take D = c00(Z;E). For every fixed z in D, finite summation gives

    ||λ_k S_E^(n_k) z||^p
      = Σ_(j in supp z) |λ_k|^p c_(j−n_k) ||z_j||^p → 0,

    ||λ_k^(−1) S_E^(−n_k) z||^p
      = Σ_(j in supp z) |λ_k|^(−p) c_(j+n_k) ||z_j||^p → 0.

Moreover S_E^(n_k) S_E^(−n_k) z = z. These are exactly the three hypotheses of Abbar's Theorem 2, with the dense sets both equal to D and the inverse maps restricted to D. E is assumed separable and nonzero, so the ambient sequence space is separable and infinite-dimensional. Thus it is Γ-supercyclic. The reverse implication is the familiar coordinatewise nonzero-functional factor map. This deduction does not require a new block construction. It even uses only boundedness of the forward shift, since inverse shifts of finite-support sequences remain defined.

## Independent deduction from the 2020 theorem

Use additive notation and Haar counting measure. In Abbar–Kuznetsova, translation is T_s f(t)=f(t−s). Take

    G₁ = Z,     A₁ = {−n : n≥0},     ω₁(j)=c_j^(1/p).

Their admissibility conditions hold: G₁ is locally compact, noncompact and second-countable; compact sets are finite; the weight is positive and locally p-integrable; and each allowed translation is bounded. The generated subgroup is abelian. For ε<1, the theorem's condition μ(F\K)<ε forces K=F. Their criterion therefore becomes

    |λ| max_(j in F) ω₁(j−n) < ε,
    |λ|^(−1) max_(j in F) ω₁(j+n) < ε.

Now take G₂=Z², A₂={(-n,0):n≥0}, and ω₂(j,l)=ω₁(j). Any compact F⊂Z² is finite. Apply the preceding scalar condition to its first-coordinate projection. The same n and λ satisfy Theorem B on G₂. Consequently the horizontal shift is Γ-supercyclic on

    Lp(Z²,ω₂) = ℓp(Z,c;ℓp(Z)).

To pass to an arbitrary separable nonzero complex Banach space E, choose a sequence (e_k) of unit vectors whose linear span is dense. After indexing the standard basis of ℓp(Z) by positive integers, define

    R(a)=Σ_(k≥1) 2^(−k) a_k e_k.

This is bounded, since ||R(a)||≤||a||_∞ Σ2^(−k)≤||a||_p. Its range contains each e_k up to a nonzero scalar and hence is dense. Coordinatewise application of R defines a bounded dense-range map from ℓp(Z,c;ℓp(Z)) to ℓp(Z,c;E), commuting with the shifts. A continuous linear dense-range intertwiner sends a dense Γ-orbit to a dense Γ-orbit: its image closure contains its entire dense range. This proves amplification for every E in the candidate. The easy functional quotient proves the reverse implication.

This is a direct application of the older theorem, not a claim that Abbar–Kuznetsova explicitly wrote the vector-valued formulation.

## From amplification to the Oberwolfach question

Once bounded distortion identifies the composition operator with the E-valued translation, where E=Lp(W), and the associated shift with its scalar version, either prior-art deduction finishes the equivalence for arbitrary Γ. Those coordinate identifications are elementary and are verified in the separate proof audit. Thus the target statement follows by combining earlier criteria with the bounded-distortion model. The candidate can explain this implication, but the priority record is materially different from discovering an entirely new criterion or amplification mechanism.

## Later literature screened

- **D’Aniello–Maiuriello, R- and C-supercyclicity for some classes of operators:** [preprint](https://arxiv.org/abs/2404.04028), first posted 5 April 2024 and revised 6 February 2025; [published 4 October 2025](https://link.springer.com/article/10.1007/s43037-025-00463-0). Theorem 4.5 and Corollary 4.6 concern R/C supercyclicity and form the immediate background to the question. No arbitrary-Γ assertion was located.
- **Bayart–Matheron, On the dynamics of composition operators: supercyclicity, odometers and translations:** [arXiv:2605.23736](https://arxiv.org/abs/2605.23736), first posted 22 May 2026. Sections 2.3–2.5 concern angular sectors, ordinary supercyclicity, and positive real scalars; they do not retain membership in an arbitrary prescribed Γ. The parent independently checked these sections. No direct collision was identified there.
- **Bernardes–Bonilla–Pinto, On the Dynamics of Weighted Composition Operators II:** [arXiv:2512.06425](https://arxiv.org/abs/2512.06425), first posted 6 December 2025, revised 30 May 2026; [published version](https://link.springer.com/article/10.1007/s00009-026-03136-w). Theorem 21 lists nine dynamical properties shared with an associated shift; Γ-supercyclicity is not among them. Its factor map named Γ is unrelated to the scalar set Γ in this question.
- **Alves–Botelho–Fávaro, On frequently supercyclic operators and an F_Γ-hypercyclicity criterion with applications:** [arXiv:2411.03179](https://arxiv.org/abs/2411.03179), posted 5 November 2024. The abstract and search screening concern Furstenberg families and unilateral pseudo-shifts, not the requested equivalence. This was a scope screen, not a full-paper audit.

## Search limits and publication recommendation

Queries covered exact Γ/Gamma terminology with “bounded distortion,” “dissipative,” “composition,” “bilateral shift,” “vector-valued,” and “amplification”; named papers and references were followed to primary publisher/arXiv sources. Source URLs, dates, local file checksums, and queries are recorded in `sources/priority_source_manifest.json`. No person was contacted.

A literature search cannot certify exhaustive global originality; unindexed papers and private work are outside its reach. Here the limitation is stronger than a negative search: explicit earlier theorems mathematically entail the advertised amplification, and an explicitly earlier theorem states the scalar criterion. **Do not label the priority audit “clean” for the candidate as presented.** A publication, if pursued, should describe a short attributed answer/application to the Oberwolfach question, disclose the earlier implication, and avoid a claim to priority for the general mechanism. No DOI upload or new-result release is justified by this audit alone.

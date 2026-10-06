**Current priority correction (October 6, 2026 UTC): the exact ordinary-potential negative answer is preexisting in Ferudun (2026) Theorem 1.2, DOI 10.5281/zenodo.23049958. See PRIORITY_CORRECTION.md. The following original source-scope analysis remains mathematically valid and is preserved verbatim below; its limited later-literature screening is historical, not current-openness certification.**

# Exact source gate: 30001994

Bastian Harrach, joint with Lilian Arnold, “Inverse Eddy Current Problems,” OWR11/2012, printed630–633, asks on631 whether the conductivity-potential map can be defined for arbitrary nonnegative bounded conductivity. The full official report and the complete published foundational paper were read; the question page was visually checked.

The ambient domain is R³. The transient equation is

∂t(σE)+curl(μ^-1 curl E)=-J_t,

with T>0, μ bounded and bounded away from zero, scalar σ>=0 bounded with bounded support, and divergence-free J_t in L²(0,T,W(curl)'). The source starts with zero initial data; the paper also permits E0 with div(σE0)=0. The target is the correction in E=A+∇φ_A, where A is divergence-free and

div(σ(A+∇φ_A))=0.

The exact spaces come from Arnold–Harrach, SIAM J.Appl.Math.72(2012),558–576, DOI10.1137/110831477, §2.1 and Lemma3.1:

- L²_rho={f : (1+|x|²)^(-1/2)f in L²(R³)}
- W(curl)={E in L²_rho(R³)^3 : curl E in L²(R³)^3}
- scalar Beppo–Levi W¹={u in L²_rho : ∇u in L²(R³)^3}
- W¹_diamond is the divergence-free vector Beppo–Levi space, with curl norm
- Lemma3.1 constructs a continuous linear map E↦∇u_E from L²_rho(R³)^3 into the ordinary unweighted L² curl-free fields. Its restriction supplies the correction for divergence-free A. The resulting A+∇u_A belongs to the original W(curl) solution space.

The established construction assumes conductivity bounded away from zero on a finite union of bounded Lipschitz conductor components with disjoint closures and connected exterior, contained in a fixed ball. It solves the weighted Neumann problem with componentwise mean-zero normalization and extends harmonically outside. Only the weighted gradient is intrinsic; different ordinary extensions may differ in the insulator.

The report prints Ω⊃B_R whereas the foundational paper's §3 explicitly has Ω⊂B_R and the preceding report sentence assumes bounded support. We use the explicit bounded-support formulation, document the symbol discrepancy, and do not infer any unbounded-conductor hypothesis from it. As usual the conductor and essential support are identified up to boundary sets in the source notation.

The question is not answered merely by an abstract completion of smooth gradients in the seminorm ||sqrt(σ)∇u||₂. Such a completion always permits an orthogonal projection but may fail to give an ordinary locally L² gradient or a W(curl) electric field. Any proposed solution or counterexample must distinguish those outputs.

## Current literature boundary

The full2012 paper's general §2 variational identities and uniqueness statements do not prove existence of Lemma3.1's map for all nonnegative σ; §3 imposes the additional assumptions above. Francini–Franzina–Vessella's2020 nonsmooth-conductivity theorem assumes uniform positive definiteness, as explicit in condition(1.1ii). Pauly–Picard–Trostorff–Waurick's degenerate-model treatment, published in JFA280(2021),108847, imposes in Hypothesis4.2 of the2018 preprint, or Assumption4.3 of the publisher proof, a strictly positive conductivity operator on the conducting subdomain, extended by zero, together with further closed-range/domain conditions. These are not arbitrary scalar coefficients that approach zero inside a conductor. No full-target resolution was located in the bounded primary search; this is not a claim of exhaustive worldwide openness.

## Prior-work gate

The full pinned record, dated literature assessment and individual desk note were read. The desk note identifies weighted projection versus ordinary potential as a possible obstruction but contains no proof. The campaign inventory has no prior user/campaign attempt; fresh all-state ID/code/degenerate-conductivity PR search, branch search and main attempt-path history returned no match. Dedicated sparse work is based on main1252d9d7855ab2ca7c856d644698d2863a19558e. No shared queue regeneration is used.

Source gate completed before substantive turn1. Five substantive turns are available if the original target remains unresolved; a complete candidate can proceed to separate full review earlier.

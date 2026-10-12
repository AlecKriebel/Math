# Independent review: tightness of a contact Godbillon–Vey form

**Verdict: PASS_COMPLETE_CONDITIONAL_TIGHTNESS_PROOF.** The frozen proof answers Calegari Question 13.2 affirmatively in its closed, oriented, globally defined-form setting. It does not solve Question 13.1, which asks for the existence of a suitably signed connection form. No mandatory mathematical correction is requested.

This is a separate adversarial AI review (gpt-6-astra, xhigh), completed on 2026-09-30. The argument uses established contact-topology theorems; historical priority is unconfirmed. This is not human peer review.

## Snapshot and validation

- `CANDIDATE.md`: `4ff15e7cbf742bb7fcaf329d1d31b99b1bc9d33c5e45b9ba7ca5bb3365964c33`
- Submitted `verify.py`: `705f411066e0a8968487ec02b5a8e5b4cc080afa0f7e1f53405b4727f8cca4ca`
- Submitted receipt: `b040f686d1864b7aaf968da706275c75c8192aadbe69a6a657283646d9ab484c`
- **87 submitted exact controls** replayed with byte-identical output, in an isolated copy
- **89 independent exact diagnostics** passed, including a genuine coordinate solution of the defining equation, arbitrary pointwise jets, a periodic moving-boundary correction, and its first derivatives

No author proof or source file was edited during this review. The finite controls do not prove the imported Eliashberg–Thurston or Gray theorems.

## 1. Exact question and geometric hypotheses

I read and visually inspected printed p.29 of [Calegari's original list](https://arxiv.org/abs/math/0209081), and checked Definition 1.1 on p.1. Question 13.2 inherits the minimal, taut, C², atoroidal hypotheses and nonzero Godbillon–Vey evaluation from Question 13.1. It assumes a choice for which the global connection form is contact, with the convention `dα=α∧ω`, and asks for tightness.

The candidate explicitly uses the closed oriented interpretation of the ordinary fundamental-class evaluation. The source sentence does not separately restate closedness; the proof does not silently extend to noncompact or boundary versions. A global nowhere-zero defining form supplies coorientation. The source's single transverse circle meeting every leaf implies the usual per-leaf tautness condition. Minimality excludes a spherical leaf because a compact embedded leaf would be a proper closed saturated subset. Atoroidality and the numerical Godbillon–Vey value are not otherwise needed by this stronger conditional theorem.

The regularity assumption is transparent: α and the already-contact ω are C¹, while the foliation has the source's C² regularity. No claim is made that an arbitrary connection chosen for every C² foliation is automatically a contact C¹ form. The question already assumes a contact form exists, and the argument never proves that existence.

## 2. Imported theorems and quantifiers

The [published Vogel 2011 paper](https://msp.org/gt/2011/15-1/gt-v15-n1-p03-p.pdf), printed p.42, expressly records the Eliashberg–Thurston **neighborhood** theorem: sufficiently C⁰-close contact structures to a taut foliation on a closed three-manifold are fillable and tight. I checked that page visually and read the surrounding pp.41–43. It is not merely a theorem producing one chosen tight approximation. This distinction is essential because the proof constructs its own smooth endpoint.

[Dathe–Rukimbira's primary preprint](https://arxiv.org/abs/0812.3389), p.5, Proposition 3.3, repeats the needed statement and refers to p.50 of *Confoliations*. Its Proposition 3.4 gives a related closed-defining-form argument, appropriately credited by the candidate. I did not independently retrieve the entire Eliashberg–Thurston book or reconstruct symplectic filling theory; the imported theorem is verified through these explicit primary-paper formulations.

[Vogel 2016](https://msp.org/gt/2016/20-5/gt-v20-n5-p01-p.pdf), Definition 2.2, p.2448, permits C¹ contact plane fields. Its Theorem 2.9, p.2451, is the smooth Gray theorem on a closed manifold. The candidate uses precisely that version after smoothing, not a low-regularity extension. The foliation itself is never replaced by a smooth foliation. Negative contact forms are handled by reversing the ambient orientation, componentwise if necessary; tightness and tautness do not depend on that auxiliary sign choice.

## 3. Contact pencil and the finite parameter interval

For C¹ α and ω, the equation `dα=α∧ω` implies `α∧dω=0`. The proposed distributional justification is valid: d²α is zero distributionally, while α∧ω is C¹ and its ordinary exterior derivative is continuous. The resulting continuous zero distribution is zero pointwise.

Every cross term in the contact volume of `β_s=ω+sα` then vanishes for a constant real s. In particular, `ω∧dα=ω∧α∧ω=0` and `α∧dα=0`; hence `β_s∧dβ_s=ω∧dω`. The sign convention is correct. Compactness gives a positive lower bound on its magnitude once the orientation is chosen. Contactness also ensures β_s is nowhere zero.

For positive large s, dividing the defining form by s leaves its kernel unchanged and gives `α+s⁻¹ω→α` uniformly. Since α is nowhere zero on the compact manifold, passage from forms to their kernel planes is uniformly continuous nearby. This places the endpoint in the required C⁰ neighborhood for some **finite** S. Smooth forms therefore give a finite contact isotopy from s=0 to s=S, so ordinary Gray stability transfers tightness to ω. Neither a contact structure at infinity nor Gray stability at the integrable limit is used.

For C¹ forms, fix this S first. The unperturbed contact volume has a positive uniform lower bound on M×[0,S]. Smooth approximations a to α and η to ω give a family η+sa that is uniformly C¹-close on this finite interval. The displayed estimate `2Bδ+δ²` follows from expanding the wedge product and bounding each factor, so sufficiently small errors preserve contactness for every s. The endpoint remains in the open taut-foliation neighborhood. This proves that every smooth η sufficiently C¹-close to ω is tight. It is not necessary for a to be integrable or to satisfy the original connection equation.

## 4. Adversarial audit of the disk-smoothing lemma

The candidate uses a valid overtwisted-disk criterion: Legendrian boundary, with disk tangent planes transverse to the contact planes along that boundary. This is stated on p.5 of Dathe–Rukimbira and in Vogel 2011, Definition 1.3 with its contact specialization on pp.42–43. It should not be confused with the also-common model in which disk and contact planes coincide along the boundary; the boundary-transverse criterion is equivalent in the smooth contact category and is the one explicitly used here. The candidate's C¹ assertion is formulated through smooth or C² embedded disks with this criterion, not through arbitrary C⁰ disks.

For a smooth disk and boundary γ, smooth forms θ_j approaching θ in C¹ have defects `q_j=θ_j(γ′)` tending to zero in C¹. This includes the tangential derivative: the chain rule involves the first derivatives of θ_j and the second derivative of the fixed smooth γ. A tubular neighborhood of the circle is a trivial oriented rank-two normal bundle, so the S¹×D² chart exists; angular dt is a globally defined one-form on the S¹ factor even though t is not a global real-valued function.

Subtracting `q_j(t)χ(u,v)dt` is therefore a globally legitimate smooth correction, extended by zero because χ is supported inside the tube. It tends to zero in C¹ and exactly kills evaluation on γ′. Contactness is C¹-open. Along the compact boundary, the original distinct two-planes have a uniformly positive angle; this C⁰-open property persists. The same embedded disk is consequently overtwisted for the corrected smooth structure.

For a C² disk, smooth C²-approximation of its embedding preserves embeddedness and yields C²-close boundaries. A single smooth tubular chart around a fixed nearby smooth curve suffices: the original and all sufficiently close boundaries are graphs after reparametrization. Their derivatives are uniformly bounded and their second derivatives converge. The chain rule now gives `θ_j(γ_j′)→θ(γ′)=0` in C¹. The translated cutoff in equation (7) has uniformly bounded first derivatives because the graph derivatives are bounded. Multiplying it by q_j produces a correction whose C¹ norm tends to zero. Its pullback to γ_j is exactly q_j dt, so the corrected form annihilates γ_j′ without an approximate-Legendrian argument.

The disk tangent planes and contact planes converge uniformly, so boundary transversality survives for D_j. Thus an overtwisted disk for θ would force arbitrarily close **smooth overtwisted** forms. Applying this lemma to ω contradicts the all-nearby-smooth-forms tightness conclusion from the finite pencil. There is no need to solve a Gray ODE with merely continuous coefficients, nor to assume the approximating contact forms initially preserve the Legendrian boundary.

## 5. Reproduction and disposition

From this review directory:

```sh
python independent_checks.py
python author_replay/verify.py > author_replay/replayed_verification.json
cmp author_replay/verification.json author_replay/replayed_verification.json
```

Both scripts require SymPy. The independent local model and graph tests are only diagnostics; neither is presented as a global overtwisted disk or a model for the source manifold. The analytic smoothing and compactness arguments are audited above rather than inferred from finite algebra.

The conditional tightness question is fully addressed in the stated closed setting. Recommended campaign disposition: **claimed_solved, 2/5**, with the classical theorem dependence, unconfirmed priority, and unrefereed AI-review status explicit. The existence and weak-sign questions in 13.1 remain outside this conclusion. No mandatory correction remains.

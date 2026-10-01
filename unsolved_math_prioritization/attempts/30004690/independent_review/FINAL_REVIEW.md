# Independent review: 30004690 finite-time contact-arc construction

Date: 2026-10-01. Verdict: **PASS for the full stated existence target**.

Reviewed frozen artifact: `TURN_4_CANDIDATE.md`, SHA-256

    85f04e81c5f02b1d867de50a82008c0d69ad2ecb962501ab2750a84ba473eed7

The candidate constructs smooth, strictly Kähler boundary data on P¹×∂D whose weak Bedford–Taylor HCMA solution is not twice differentiable at a specified interior point. This settles the source target, including the interior requirement. The published theorem already supplies boundary nonsmoothness for the same construction. The review certifies neither novelty nor priority, and does not authorize publication.

## 1. Source and hypothesis audit

I independently read the original OWR discussion, the full author paper, and the complete 31-page published Ross–Witt Nyström paper. The latter was retrieved and parsed successfully after resuming a timed-out transfer. Printed pp. 15–16, 24, and 28 were also inspected visually.

The source permits semipositive smooth boundary data. Published Proposition 3.4 supplies the stronger strict positivity used here. Its set S genuinely may contain a smooth curve segment, not just isolated tangency points. The construction occurs at 0<T<1, and the lifted domain at T is a smoothly bounded simply connected domain. The cited proof and Theorem 2.15 give a smooth lifted strong flow across that time. The proof of published Theorem 6.2 explicitly records nonzero limiting normal velocity.

The universal covering resolves the boundary self-contact. A chosen component projects biholomorphically onto the open fluid domain, including at T; only distinct boundary points can project to the same contact arc. Thus Green functions on the open domain pull back unchanged. This is not an assumption that the projected post-contact flow is smooth.

Appendix A, especially Theorem A.1 and Corollary A.2, establishes the smooth Green dependence needed on the lifted family. The same proof works in a smooth coordinate realization of its compact domain and collar. The one-sided family may be extended smoothly on the cover; no extension of the projected weak flow is needed.

## 2. The zero-area enlargement is valid

At an interior point q of the chosen contact arc, the two fluid pieces lie on its opposite sides. A small disc B therefore satisfies B minus S ⊂ Ω_T. The open connected domain D+=Ω_T∪B adds only a zero-area part of the contact arc and remains proper: its complement has positive area because T<1 and the area form is strictly positive.

The current identity in Proposition 2.5 makes ψ_T plus a local Fubini–Study potential distributionally harmonic on D+ away from the injection point. The zero-area set contributes no hidden line measure: ψ_T is C¹,¹ away from the pole, and the identity already gives the entire current. Weyl's lemma justifies harmonic continuation. Positive capacity of the arc does not obstruct this continuation; its absence from the measure is the relevant fact here.

For v_h=(ψ_{T+h}−ψ_T)/h, monotonicity gives v_h≤0. On D+ its Laplacian current is δ_0 plus a nonnegative absolutely continuous measure. The logarithmic coefficient is exactly one. The extremal property of the negative Green function consequently gives v_h≤G_D+. Both the direction of this inequality and the domain-monotonicity sign are correct.

Moreover, G_D+<G_Ω at every point of Ω other than the pole. The difference is harmonic after cancellation of the identical logarithmic poles. A smooth interior point of the slit is a regular boundary point from each side for G_Ω, where it tends to zero; the Green function of D+ is strictly negative there. The difference is nontrivial, and the strong maximum principle gives strictness everywhere in Ω. This step depends on a genuine arc; an isolated polar point would not suffice.

## 3. Left time curvature is finite and strictly negative

On each pre-contact smooth domain, differentiating the Dirichlet problem and using smooth fit gives ∂_tψ_t=G_Ωt. A fixed physical point w* in Ω_T belongs to Ω_t for all sufficiently late t<T. Its chosen lift is fixed because the covering map is fixed.

Smooth Green dependence on the cover gives a finite limit L=∂_tG_Ωt(w*,0) as t↑T. To check that L is nonzero, differentiate the zero Dirichlet boundary value. The derivative is harmonic, including across the fixed pole after its time-independent logarithmic term is removed, and has boundary value

    −V ∂_n G_T.

Both V and the outward normal derivative of the negative Green function are strictly positive. Hence the boundary value and its harmonic extension are strictly negative. In particular, −∞<L<0. Neither geometric curvature of the projected boundary nor regularity after contact is being silently assumed.

## 4. Independent verification of the scalar duality step

Let a(t)=ψ_t(w*), κ0=a'_−(T), and b=G_D+(w*,0). Concavity and the preceding comparison imply a'_+(T)≤b<κ0. Finiteness and concavity on an interval around T ensure continuity and finite one-sided derivatives there.

For κ in (b,κ0), T is the unique global maximizer of a(t)−κt. For κ just above κ0, the smooth pre-contact branch has a unique maximizer satisfying a'(t)=κ. Local strict concavity at T and global concavity exclude a competing distant branch.

An alternative Taylor check avoids any possible ambiguity about the meaning of a second derivative. Set δ=κ−κ0. On the plateau side δ<0 the conjugate is exactly affine. For δ>0, inversion of the pre-contact derivative gives t−T=δ/L+o(δ), and therefore

    F(κ)−F(κ0)−(1−T)δ = −δ²/(2L)+o(δ²).

The quadratic coefficient is zero from the left and positive from the right. Thus F has no second Peano derivative, and in particular is not twice differentiable. This is a stronger check than merely observing a possible discontinuity of F'' near the point.

An independently authored rational control script additionally checks 81 concave piecewise-quadratic cases, optimizing both branches and endpoints exactly. All 486 assertions pass. These controls test the signs and scalar mechanism only; the analytic proof, not those computations, establishes the PDE result.

## 5. Interior location and full target

κ0=G_Ω(w*,0)<0 and is finite for w*≠0. Therefore τ*=exp(κ0/2) satisfies 0<τ*<1. The twisting map (z,τ)↦(τz,τ) is biholomorphic near that point. Published Proposition 4.2 adds only smooth Fubini–Study and logarithmic terms there, so the failure of second differentiability transfers to Φ at (w*/τ*,τ*). Rotation by boundary τ preserves the Fubini–Study form, so the prescribed boundary data remain smooth and strictly Kähler.

This is an existence construction through a credited designer-flow theorem, rather than a closed-form polynomial example. The original target does not require such an elementary formula. The interior defect is established directly and is not inferred from nonmaximal rank.

## 6. Scope of the approval

No mathematical correction to the frozen candidate is required. Retain all of its qualifiers: positive-length contact arc, finite contact time, smooth lifted pre-contact family, no post-contact smoothness assumption, strict interior radius, and no novelty claim. Preserve the earlier unsuccessful routes and unknown historical turn count. This review is separate from author research turns.

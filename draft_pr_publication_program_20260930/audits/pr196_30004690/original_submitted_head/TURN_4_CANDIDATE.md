# Recovered substantive turn 4: a finite-time contact-arc candidate

Problem 30004690 / OWR-7155446-005. **Complete candidate; independent adversarial review required.** No correctness, novelty, or publication claim is made before review. Historical substantive-turn count remains unknown; this is documented recovered turn 4.

## 1. Candidate result and construction recipe

There exist smooth boundary data f on P¹×∂D, with ω_FS+dd^c_z f(·,τ) strictly positive for every boundary τ, such that the weak solution Φ of

    π*ω_FS + dd^c Φ >= 0,
    (π*ω_FS + dd^c Φ)^2 = 0,
    Φ|_(P¹×∂D)=f

fails to be twice differentiable at an interior point of P¹×D. This is stronger than the source's allowed semipositive boundary condition. The equation is interpreted in the Bedford–Taylor sense.

The recipe uses Ross–Witt Nyström's published construction of a Hele–Shaw flow with a **nontrivial curve segment of tangential self-contact at a time 0<T<1**, rather than a final slit at time 1. Choose their smooth Kähler potential φ from Proposition 3.4 with such a contact segment S. Let Ω=Ω_T. Choose any w* in Ω other than the injection point 0, let G_Ω(w*,0)<0 be the Green function normalized to have logarithmic singularity log|w|² at 0, and set

    κ0=G_Ω(w*,0),
    τ*=exp(κ0/2),
    z*=w*/τ*.

The claimed interior singular point is (z*,τ*), where 0<τ*<1. Take boundary data

    f(z,τ)=φ(τz),    |τ|=1.

The published duality supplies Φ. The argument below identifies a genuine one-dimensional second-derivative jump at (z*,τ*). It does not infer nonsmoothness merely from rank loss.

## 2. Exact credited inputs

The full published paper is Ross–Witt Nyström, *Applications of the duality between the Homogeneous Complex Monge–Ampère Equation and the Hele-Shaw flow*, Ann. Inst. Fourier 69 (2019), 1–30, DOI 10.5802/aif.3237.

- Proposition 3.4, pp. 15–16, constructs a smooth strictly positive form whose simply connected flow develops tangency along an arbitrary finite union of points and nonintersecting smooth curve segments. Choose a segment with nonempty relative interior. Its proof constructs the pre-contact flow as the projection of a smooth strong flow on a covering surface, smooth through the contact time on that surface.
- The proof of Theorem 6.2, p. 24, explicitly records the nonvanishing limiting normal velocity in that construction and that Ω_T locally has two pieces on opposite sides of a contact point.
- Proposition 2.5 gives the obstacle-potential identities, including C^{1,1} regularity away from the source and

      ω_FS+dd^cψ_t = 1_(Ω_t^c) ω_φ + tδ0.

- The time parameter t is concave in the envelope: for fixed w, t↦ψ_t(w) is concave. The Legendre duality in Section 4 gives

      Φ̃(w,τ)=sup_(0<=t<=1){ψ_t(w)+(1−t)log|τ|²}.

  For τ≠0, Proposition 4.2 relates Φ̃(w,τ) to Φ(w/τ,τ) by addition of smooth terms. Thus second differentiability transfers between them along this biholomorphic change of coordinates.
- Appendix A proves smooth dependence of Green functions on a smooth family of smoothly bounded domains. The same argument applies on the covering surface after choosing local coordinates or a conformal chart.

These are credited inputs, not new results claimed here. The full author version is also available at arXiv:1509.02665. The published Theorem 6.2 itself states boundary nonsmoothness; the proposed additional interior argument is below.

## 3. A zero-area contact arc enlarges the harmonicity domain

Fix a point q in the relative interior of the contact segment S. By choosing a sufficiently small coordinate disc B about q, the geometry in the cited construction gives

    B \ S subset Ω,

with fluid on both sides of S. Put

    D+=Ω union B.

This is an open connected enlargement of Ω, remains a proper domain in P¹, and adds only a zero-area piece of the contact arc. Its complement still has positive area because T<1. Both Ω and D+ therefore have Green functions with pole at 0.

By the current identity above, ψ_T plus a local potential of ω_FS is harmonic on D+ away from 0: the only new points are on S, which has area zero, so the smooth area form contributes no measure there. This is distributional harmonicity across the arc, followed by the usual removable/Weyl regularity statement. At 0 the logarithmic coefficient is T.

For any h>0 with T+h<1, let

    v_h = (ψ_(T+h)−ψ_T)/h.

The potentials decrease with t, so v_h<=0. On D+ the current identity gives

    dd^c v_h = δ0 + (1/h) 1_(Ω_(T+h)^c) ω_φ >= 0.

Thus v_h is a nonpositive subharmonic function on D+ with logarithmic pole coefficient one at 0. By the extremal characterization of the Green function,

    v_h(w) <= G_(D+)(w,0),          w in D+.             (1)

This comparison does not assume regularity of the post-contact flow, a description of Ω_(T+h), or that the arc is filled at a quantitatively controlled rate.

On Ω, domain monotonicity gives G_(D+)<=G_Ω. The inequality is strict at every interior point other than the pole. Indeed near q the original Green function tends to zero from either smooth side of the slit, while G_(D+) is strictly negative at q, an interior point of D+. Their difference is nonnegative harmonic on Ω, with removable difference at the pole, and is not identically zero; the strong maximum principle gives

    G_(D+)(w*,0) < G_Ω(w*,0).                            (2)

The positive-length contact arc is essential here. Filling a single polar contact point would not give the same strict Green-function comparison.

## 4. Finite nonzero pre-contact time curvature

For t<T close to T, w* lies in Ω_t. Smoothness of the strong flow and smooth fit at the free boundary give

    ∂_tψ_t(w*)=G_(Ω_t)(w*,0).                            (3)

One can verify (3) directly: the time derivative is harmonic away from the fixed pole, has logarithmic coefficient one, and its boundary value is zero because ψ_t and φ have matching first spatial derivatives on the moving boundary. These properties characterize the Green function.

Lift the pre-contact domains to the smooth family Ω'_t on the covering surface used in Proposition 3.4. For t<=T, the interior projection is conformal and injective onto Ω_t, so the Green functions pull back unchanged. The lifted family and its Green functions are smooth up to t=T. Hence, writing a(t)=ψ_t(w*),

    a'_-(T)=G_Ω(w*,0)=κ0,
    a''_-(T)=L

for a finite L. Moreover L<0. Differentiate the lifted Dirichlet condition G_t(x_t,0)=0 at the boundary. The time derivative H=∂_tG_t|_(T−) is harmonic, including at the pole after removing the time-independent logarithmic singularity, and has boundary values

    H = −V ∂_nG_T.

The limiting outward normal velocity V is positive, and the Hopf lemma gives ∂_nG_T>0. Therefore H is strictly negative on the boundary and in the interior. Evaluating at the lift of w* gives

    −infinity < L < 0.                                  (4)

This is a statement about the smooth lifted pre-contact flow. It makes no claim that the projected flow remains smoothly bounded after T.

## 5. The time-slope gap produces an interior plateau

Since a(t) is a finite concave function near T, its one-sided derivatives exist. Taking h↓0 in (1) and using (2) yields

    a'_+(T) <= b := G_(D+)(w*,0) < κ0 = a'_-(T).          (5)

For every κ in (b,κ0), concavity therefore makes t=T the unique maximizer of a(t)−tκ over the entire interval [0,1]. For κ>κ0 sufficiently close to κ0, (4) gives a unique maximizer t(κ)<T close to T, characterized by

    a'(t(κ))=κ.

Global concavity ensures these local maximizers are the global ones; no unknown post-contact branch can overtake them.

Define the one-real-variable restriction

    F(κ)=Φ̃(w*,e^(κ/2))
        =κ+sup_t{a(t)−tκ}.

For b<κ<κ0, this is exactly affine:

    F(κ)=a(T)+(1−T)κ,
    F'(κ)=1−T,
    F''(κ)=0.

For κ>κ0 close to κ0, smooth implicit differentiation gives

    F'(κ)=1−t(κ),
    F''(κ)=−1/a''(t(κ)).

By (4), its limiting right second derivative is −1/L>0, whereas the left second derivative is zero. The first derivatives match, but the second derivatives do not. Thus F is not twice differentiable at κ0.

Finally κ0<0, so τ*=e^(κ0/2) lies strictly inside the punctured unit disc. Proposition 4.2 and the smooth curve κ↦(w*/e^(κ/2),e^(κ/2)) transfer this failure to Φ at (z*,τ*). Adding the smooth Fubini–Study correction cannot remove a second-derivative jump. The boundary data φ(τz) remain smooth and strictly Kähler, as rotation preserves ω_FS.

This proves the candidate result, conditional only on the cited published construction and the standard potential-theoretic facts explicitly used above.

## 6. Why this evades the earlier obstructions

The final-time slit mechanisms in turns 1–3 are not used. Here the contact occurs at T<1 along a segment whose two sides are smooth boundary branches on the cover. The pre-contact Green derivative has finite nonzero time derivative. The new effect is a strict right time-slope drop because ψ_T is harmonic across a zero-area, positive-capacity contact arc. That creates a fixed-T Legendre plateau and a second-derivative jump at an interior disc radius.

The proposed singularity is not inferred from the terminal form having zero rank, and no endpoint-flat smoothing theorem is assumed. A single tangency point is insufficient for the strict comparison argument; the construction must use a genuine arc.

## 7. Review requests and stopping condition

This is a complete candidate found on recovered turn 4. Under the current research rule, further search is paused for a separate adversarial review, not declared solved in advance. The key points to challenge are:

1. The precise geometry and smooth lifted pre-contact flow supplied by Proposition 3.4 when S contains a genuine curve segment
2. Distributional harmonicity of ψ_T across that zero-area arc
3. The sign and direction of the Green comparison (1), and strictness (2)
4. The finite strictly negative left curvature (4), including the covering-surface argument
5. The global concave-duality passage and interior twisting location

If any of those fails, preserve the correction and resume the remaining recovered proof turn. No novelty or priority claim is made. The smooth boundary potential is furnished by a credited constructive theorem, not an elementary closed-form polynomial formula.

## Primary links

- Published full paper: https://www.numdam.org/item/10.5802/aif.3237.pdf
- Full author version: https://arxiv.org/pdf/1509.02665
- Original 2021 report, pp. 1321–1325: https://ems.press/content/serial-article-files/46904
- Earlier harmonic-disc duality paper: https://www.numdam.org/item/10.1007/s10240-015-0074-0.pdf

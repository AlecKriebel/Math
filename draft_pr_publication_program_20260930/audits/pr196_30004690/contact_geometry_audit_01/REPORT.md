# Family A independent adversarial report: contact geometry and potential theory

Audit completed in UTC on 2026-10-15. Scope: mathematical verification of the frozen turn-4 candidate, especially the contact construction and Green-function argument. The initial independent record was frozen before primary-source review and before reading favorable reviews or other audit families. No favorable review, archive README/status, or other new family report was read for this verdict.

## Verdict

**PASS for the assigned geometry/potential-theory dependencies.** I found no counterexample or unclosed mathematical premise in the finite-contact-arc mechanism when one uses the potential furnished by the *proof* of Ross–Witt Nyström Proposition 3.4, chooses an interior point of a nontrivial contact segment, and interprets the Green function with logarithmic coefficient one. The comparison in the candidate has the correct direction and is strict. The pre-contact curvature exists, is finite, and is strictly negative.

The argument proves a conditional geometric lemma with all its hypotheses supplied by the cited published construction. It is not a proof of historical novelty, priority, completeness of the literature, or readiness for publication. The independent Legendre/HCMA family and original-problem-contract review remain separate gates. No historical clearance is asserted here.

Two useful precision improvements are recorded below: (i) on the enlarged domain the difference quotient is actually harmonic away from the pole, not merely subharmonic; (ii) the source's punctures are chosen in components of the complement of the **closure** of the contact domain. The closure bar is lost by text extraction. Neither improvement repairs a substantive failure.

## Exact claim and credited inputs

Let ω=ω_FS have total mass one, ω_φ=ω+dd^cφ>0, and let Ω_t={ψ_t<φ} be its obstacle-defined flow. Normalize dd^c log|ζ|²=δ_0. Select φ from the constructive proof of Proposition 3.4 with a contact segment S of positive length at 0<T<1. Let Ω=Ω_T. For w∈Ω\{0}, define a(t)=ψ_t(w) and κ_0=G_Ω(w,0), where G is the negative Green function with pole coefficient one.

The assigned claim is that a'_-(T)=κ_0, −∞<a''_-(T)<0, and a'_+(T)<κ_0. These are sufficient for the candidate's scalar Legendre edge and interior second-order defect.

The following source map records the published inputs, not new results of this audit:

| Primary location | Input used |
|---|---|
| AIF 69 (2019), pp. 4, 15–16, Definition 1.2 and Proposition 3.4 | Finite contact time; prescribed segments; smooth positive form; smooth lifted strong flow. |
| Same, p. 24, proof of Theorem 6.2 | Nowhere-vanishing limiting velocity and two local fluid pieces. |
| Same, pp. 7–8, Proposition 2.5 | Concavity, spatial C¹,¹ regularity, current identity, area parameter. |
| Same, p. 12, Theorem 2.15; pp. 26–28, Appendix A | Two-sided smooth local domain family; smooth parameter dependence for Dirichlet/Green problems. |
| Same, pp. 17–18, Proposition 4.2 and Theorem 4.4 | Twisting identity and Legendre duality. |
| arXiv:1212.2337v2, manuscript p. 23, Remark 7.1 | Two-sided modified-permeability flow behind Theorem 2.15. |

Published primary full text: [Applications of the duality between the Homogeneous Complex Monge–Ampère Equation and the Hele-Shaw flow](https://www.numdam.org/item/10.5802/aif.3237.pdf), DOI 10.5802/aif.3237. Underlying author full text: [The Hele-Shaw Flow and Moduli of Holomorphic Discs, v2](https://arxiv.org/pdf/1212.2337), for the modification and two-sided existence statement. No secondary source is relied on.

## 1. Literal construction, topology, and boundary geometry

The source's Definition 1.2 is stronger than an unspecified topology change: T is in (0,1), the domains before T are smoothly bounded and simply connected, and the limiting boundary is the image of a smooth locally embedded curve with the specified tangential self-contact. Proposition 3.4 applies to a genuine smooth embedded segment, not merely a point. Its Figure 1.1 and the two-piece description on p. 24 identify the relevant fluid sides.

A visual inspection of journal p. 15 resolves an important extraction ambiguity. The punctures z_i lie in the components of P¹\overline(Ω_T), and the construction asks that overline(Ω_T)\S be connected. Replacing the first complement by P¹\Ω_T would lose the intended topology. The candidate does not make that replacement.

Let π:Σ→P¹\{z_i} be this fixed universal covering map and U_T be the selected component of π⁻¹(Ω_T). Since Ω_T is simply connected, π|U_T is a conformal bijection onto Ω_T. It is therefore injective on the limiting **open interior**. The lifted boundary is an embedded smooth closed curve. At a contact arc the two distinct lifted boundary arcs project to the same physical arc; no assertion of injectivity of the map on the closed domain is needed or true. This distinction is essential and the candidate uses it correctly.

The source applies its two-sided short-time strong-flow theorem to U_T. Thus U_t has a smooth compact boundary for t in an interval through T, even though only its part t≤T projects injectively as the physical pre-contact flow. All arguments below use this interval only to obtain left derivatives at T. They do not identify the projected t>T lifted domains with the actual weak flow after contact.

Choose q in the relative interior of one selected arc, avoid all endpoints and other contact components, and choose a sufficiently small coordinate disc B about q, disjoint from the pole 0. There are exactly two relevant local boundary branches and fluid lies on their opposite sides. Since q is in the interior of the overlap, the branches coincide on the selected subarc. Shrinking B gives B\S⊂Ω and Ω∩B=B\S. This is stronger than the statement at an isolated tangency, where an exterior cusp remains. The argument would fail if one silently replaced the segment by a point.

Set D=Ω∪B. It is open, connected, contains 0, and adds only a subset of a smooth arc to Ω. Thus its ω_φ-area remains T and its complement has area 1−T>0. In particular D is proper and Greenian: a positive-area compact complement is nonpolar. The same holds for Ω; alternatively its conformal equivalence to the smooth lifted domain directly supplies its Green function. No smoothness or simple connectivity of D is needed.

## 2. Distributional removal, including the pole

Write the obstacle current identity in the candidate's normalization as

    ω+dd^cψ_t = 1_(Ω_t^c) ω_φ + tδ_0.                         (A1)

On D the measure 1_(Ω^c)ω_φ is zero because D\Ω has area zero. Therefore, for a local potential ρ of ω,

    dd^c(ψ_T+ρ) = Tδ_0  on D.                               (A2)

Away from 0 this is a distributional harmonicity statement. The potentials are locally integrable (indeed C¹,¹ away from 0), so Weyl regularity gives an ordinary smooth harmonic function there. This is not an appeal to arbitrary removability of a positive-capacity arc: it follows from the exact current identity, which rules out an arc-supported boundary measure.

For h>0 sufficiently small, T+h<1. Obstacle monotonicity gives Ω⊂Ω_(T+h) and ψ_(T+h)≤ψ_T. Thus the difference quotient v_h=(ψ_(T+h)−ψ_T)/h is nonpositive and finite away from 0. Subtracting (A1) gives

    dd^c v_h = δ_0 + h⁻¹ 1_(Ω_(T+h)^c)ω_φ  on D.            (A3)

Because Ω_(T+h)^c∩D⊂D\Ω is itself of area zero, the extra term in (A3) vanishes. In fact

    dd^c v_h = δ_0 on D.                                    (A4)

Hence v_h is negative harmonic on D\{0}, has logarithmic coefficient exactly one at 0, and v_h−log|ζ|² is harmonic in a fixed small pole chart. The pole is fixed in time. There is no unnoticed negative measure in (A3), no division by a vanishing density, and no need to describe how rapidly the weak flow fills the contact segment.

## 3. Green comparison and strictness

The sign convention is decisive: G_D<0 in D\{0}, dd^cG_D=δ_0 there in the distributional sense, and its boundary values are zero in the Green-potential sense. Enlarging a Green domain makes this negative Green function smaller.

Here is a direct comparison that does not assume regularity of ∂D. Exhaust D by connected smoothly bounded relatively compact domains D_j containing 0 and the evaluation point. On D_j, v_h−G_(D_j) is harmonic across 0 by equal pole normalization. Its boundary upper limits are ≤0 because v_h≤0 and G_(D_j)=0. The maximum principle gives v_h≤G_(D_j). Passing to the decreasing Green-function limit gives

    v_h(w) ≤ G_D(w,0).                                      (A5)

The same exhaustion argument gives G_D≤G_Ω on Ω. Strictness is not merely strict inclusion of sets: adding a polar point can preserve G. The chosen q is a regular boundary point on either slit side of Ω. This can be seen without an exterior-cone assumption for the whole slit domain: lift each side through π to one of the two smooth boundary arcs of U_T. Conformal invariance gives G_Ω=G_(U_T)∘(π|U_T)⁻¹, and the lifted smooth-boundary Green function tends to zero on both arcs. Thus G_Ω(w_n,0)→0 as w_n→q from either local component of Ω.

In contrast q is an interior non-pole point of D, so G_D(q,0) is finite and strictly negative. The nonnegative function

    d(w)=G_Ω(w,0)−G_D(w,0)

is harmonic on Ω, including at the pole after cancellation of the logarithms. Its limit along one of the preceding sequences is −G_D(q,0)>0. It is therefore not identically zero. Connectedness and the strong maximum principle imply d(w)>0 throughout Ω. Consequently

    G_D(w,0) < G_Ω(w,0) < 0,  w∈Ω\{0}.                     (A6)

This proves the proposed strict sign, for every permitted evaluation point.

## 4. Left derivative and finite strictly negative curvature

First consider t<T near T. The chosen w lies in Ω_t for t sufficiently near T: in the lifted smoothly increasing family every fixed interior point of U_T lies in U_t eventually. Thus a(t) can be studied on smoothly moving domains containing a fixed pole and evaluation point.

The required time differentiability of ψ_t can be justified independently of an informal differentiation of envelopes. On Ω_t, subtract t times a fixed local logarithmic fundamental solution (with a smooth cutoff) from ψ_t plus a local background potential. The remaining function solves a smooth Dirichlet problem on the moving smooth domain, with smooth forcing and boundary data. Pulling back by smooth domain diffeomorphisms yields uniformly elliptic problems on a fixed compact disc. Elliptic estimates and differentiation give smooth parameter dependence away from the pole and up to the moving boundary.

Spatial smooth fit follows from C¹,¹ regularity and equality ψ_t=φ on the exterior open side. If x_t is a moving boundary point, differentiate ψ_t(x_t)=φ(x_t). The spatial gradient terms cancel, giving ∂_tψ_t=0 on ∂Ω_t. Its derivative is harmonic off 0 and has pole coefficient one. Uniqueness of the Dirichlet Green function gives

    a'(t)=G_(Ω_t)(w,0).                                     (A7)

Fix the lift x of w and the unique lift p of 0 in U_T. They are fixed points of Σ and lie in U_t for all nearby pre-contact times. Conformal invariance gives G_(Ω_t)(w,0)=G_(U_t)(x,p). There is no moving evaluation-point term: π is independent of t. Appendix A's argument extends to this smooth Riemann-surface domain by pulling the Laplace operator back to a fixed smooth disc. One may also take a conformal chart of the simply connected noncompact covering surface. Only a compact neighborhood of the lifted closure is used, so the ellipticity constants are uniform. This proves smooth Green dependence through T on the lift.

In particular,

    a'_-(T)=G_(U_T)(x,p)=G_Ω(w,0)=κ_0.                      (A8)

Let H=∂_tG_(U_t)|T with fixed x-coordinate on the surface. H is harmonic on U_T, including at p: the time-independent logarithmic singularity differentiates to zero. If x_t is any lifted boundary path with outward scalar normal velocity V, differentiation of G_(U_t)(x_t,p)=0 gives

    H = −V ∂_nG_(U_T)  on ∂U_T.                             (A9)

The flow is increasing, and its nowhere-vanishing limiting boundary velocity gives V>0 everywhere. Equivalently, Darcy's law gives a positive permeability times the positive outward derivative of the negative Green function. The Hopf lemma yields ∂_nG_(U_T)>0 at every boundary point. All functions in (A9) are smooth on a compact boundary. Thus H has strictly negative finite boundary values; the maximum principle gives H(x)<0, and smoothness gives finiteness. Hence

    −∞ < L:=a''_-(T)=H(x) < 0.                              (A10)

No assertion about a second derivative of the actual post-contact weak flow is used. A reparameterization must retain the area parameter of the obstacle flow; the construction's strong-flow and weak-flow identification supplies precisely that parameter.

## 5. Right slope and scalar consequence

For fixed w≠0, the obstacle values are finite near T and concave in t. Therefore the one-sided derivatives at this interior parameter are finite. Letting h↓0 in (A5), then applying (A6) and (A8), gives

    a'_+(T) ≤ G_D(w,0) < κ_0=a'_-(T).                       (A11)

This is the assigned mechanism. No Green function of Ω_(T+h) and no post-contact regularity is needed.

For completeness, its second-order scalar consequence can be checked without inferring differentiability failure merely from rank loss. Concavity makes T the unique maximizer of a(t)−tκ whenever G_D(w,0)<κ<κ_0. On the other side, (A10) gives the unique local inverse t(κ)<T of a'(t)=κ; global concavity makes that local maximizer global. If F(κ)=κ+sup_t(a(t)−tκ), then its left branch is affine and its right branch has quadratic expansion

    F(κ_0+ε)=F(κ_0)+(1−T)ε−ε²/(2L)+o(ε²),  ε↓0.

The corresponding expansion on ε<0 has zero quadratic coefficient. Since L is finite and negative, F has no second-order Taylor expansion at κ_0. This is stronger evidence than a rank computation. Because κ_0<0 and finite, τ=exp(κ_0/2) is in the punctured open unit disc. The twisting correction along w fixed is the smooth function log((1+|w|²)/(|τ|²+|w|²)); it extends smoothly across w=∞ in the reciprocal coordinate. Smooth boundary rotation preserves ω_FS and the strict boundary Kähler condition.

## 6. Boundary and assumption stress tests

| Check | Result and reason |
|---|---|
| T=0 or T=1 | Excluded. At T=1 the positive-area Green-domain argument and available right slopes fail. |
| Contact a single point | Insufficient for B\S⊂Ω; no claim of an interior defect follows from this argument. |
| Arc endpoints or several contacts | Choose q away from endpoints/other components. Smoothness on the lift still covers the complete boundary in (A9). |
| Contact at the injection point | Excluded by S⊂P¹\{0}; B can avoid the pole. |
| Evaluation at 0 | Excluded; a(t) and κ_0 are not finite there. |
| Evaluation near ∂Ω | Allowed for each fixed interior point; choose a sufficiently late pre-contact interval. No uniform estimate as w→∂Ω is claimed. |
| Evaluation at ∞ | Permitted on the sphere; reciprocal coordinates make both Green and twisting arguments local and smooth. A finite w can be chosen to simplify presentation. |
| D not simply connected or not smoothly bounded | Allowed. Positive-area complement and exhaustion suffice. |
| Possible boundary singular measure on S | Ruled out by (A1), not by zero area alone. |
| Post-contact cusps, overlap, topology | Irrelevant to (A3)–(A11). Only weak monotonicity and the current identity are used. |
| Closed-domain injectivity of π | False at contact and unused. Open-interior injectivity is proved above. |
| Pole coefficient/sign conventions | Fixed by dd^c log|ζ|²=δ_0. Pressure normalizations differ by positive constants only; no such constant enters (A7). |
| Smooth merely semipositive area density | Not sufficient for all Hopf/velocity claims. The construction supplies a smooth strictly positive density. |
| Circular use of desired interior nonsmoothness | None. The lift, current identity, Green comparison, and curvature are established before duality. |
| Empirical or numerical assumptions | None. This is a proof audit; no numerical experiment is offered as proof. |

## 7. Access, reproducibility, and exact remaining limits

The submitted candidate and source_record were read first. The independent initial record was sealed before source inspection. Published PDF and complete extracted text were then accessed read-only from the shared private-primary-source cache. Its verified PDF SHA-256 is `724e742d033b3401b6938011cf07ee4faf79a7d13b14d22bb9ca1a90969cc0e2` (3,158,845 bytes). Journal pp. 4, 15, 16, and 24 were rendered locally at 125 dpi and visually inspected; the images remain private/excluded. They establish the closure bars, Figure 1.1, and exact proof language. Browser full-text access independently covered the published paper and arXiv:1212.2337v2. The latter was not downloaded locally. No full article, extracted article text, or source screenshot is included in the safe authored outputs.

The proof rests on the cited published construction, standard elliptic Dirichlet theory, Weyl regularity, Hopf and maximum principles, and elementary Green-domain potential theory. Their complete foundational proofs are not rederived. The modified-permeability input was checked in its primary author text rather than inferred from a forward-only theorem. There was no access block to the relevant primary construction. No search for historical novelty or priority was performed by this family; no such clearance is implied by PASS.

**Strongest verified result:** the selected published contact construction supplies (A8), (A10), and the strict slope gap (A11), with all Green-domain and pole assumptions checked. The assigned mathematical gap is closed. Remaining project-level work is the independent HCMA/duality and exact original-problem-contract gates, historical novelty/priority review if desired, and any separately authorized publication workflow.

**Completion estimate:** 100% of this assigned contact-geometry/potential-theory audit; no percentage estimate of historical novelty or publication clearance.

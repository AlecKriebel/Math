# Early sealed independent derivation and falsifier criteria

Sealed UTC: 2026-10-01T23:30:09.879104+00:00
Family: nonlinear amplification and orbital departure. Assigned PR head: 5ac4a57e08dd72a6f16768f2288b9c0349999431. Candidate text is treated as a hypothesis, not an authority. Before sealing I read the candidate text and three primary PDFs through the web reader, but no candidate code, previous review, result receipts, sibling audits, or metadata claims. Physical main is a separate integration state; all target inspection uses immutable assigned-head blobs.

## Literal source boundary

OWR Report 32/2019, DOI 10.4171/OWR/2019/32, Anna Geyer with Dmitry Pelinovsky, printed pp. 1940–1942, studies the mean-zero 2π-periodic quadratic equation u_t+u u_x=P u and parabolic peaked profile U_*(z)=(3z²−π²)/18 on [−π,π]. The closing question explicitly says: “The proof of nonlinear instability of the peaked periodic waves is still open.” It follows linear and spectral statements in L²-related spaces and identifies the nonlinear low-regularity and linear-domain mismatch. No particular nonlinear stability norm is specified in that closing question. I will judge the candidate's stated W^{1,∞} characteristic-solution theorem; a weaker-norm nonlinear source closure is not implied.

## Independent universal argument

Let L=2π, κ=π/3, c=κ² and φ(x)=(x−π)²/6−π²/18 on [0,L], periodically lifted. Its slopes run continuously from −κ to κ on the open branch. Its zero-mean primitive p=(φ−c)φ′ has p′=φ, vanishes at the endpoints and has zero integral by oddness about π. Thus b(t,x)=φ(x−ct) is a continuous Lipschitz traveling solution and |φ′|≤κ almost everywhere.

The periodic primitive convolution kernel G(z)=1/2−z/L for 0<z<L has distributional derivative δ_0−1/L and zero mean. Therefore, on mean-zero h, P h=G*h and ||P h||∞≤(L/4)||h||∞=(π/2)||h||∞. This is an upper bound; no spectral growth rate enters.

For a nonlinear characteristic X′=u(t,X), V=u(t,X), assume the candidate's local characteristic construction provides V′=P u(t,X), continuity in the closed label interval, and X_ξ>0 before breakdown. Define r=X−ct and h=V−φ(r). Since r is absolutely continuous and φ is Lipschitz, φ∘r is absolutely continuous. Off r∈L Z the derivative is φ′(r)r′. On each level set r=jL, an absolutely continuous r has r′=0 almost everywhere on that level set. There h=V−c=r′=0 a.e., and P b at the reference crest is zero. Hence the identity h′=P(u−b)(t,X)−φ′(r)h holds a.e. even when the trajectory lies on, crosses, touches, or repeatedly meets the moving reference crest. Assigning either bounded one-sided derivative at that set has no effect on the identity. This establishes the integrated inequality without assuming global classical differentiability at the corner.

Taking the supremum over labels (X is an onto degree-one homeomorphism of the circle) gives a(t)≤a0+∫_0^t(κ+π/2)a(s)ds. Consequently a(t)≤a0 e^{At}, with A=5κ/2, while the solution exists. There is no estimate involving second derivatives and no claim of a δ-independent logarithmic lifetime here.

For the actual transported corner q=X(t,0), ζ=q−ct and q′=u(t,q). Since φ(0)=c and φ is globally κ-Lipschitz on the periodic lift, |ζ′|≤a0 e^{At}+κ|ζ|, ζ(0)=0. Integration gives |ζ|≤a0(e^{At}−e^{κt})/(A−κ). Therefore |u(t,q)−c|≤a0[e^{At}+κ(e^{At}−e^{κt})/(A−κ)]≤(5/3)a0 e^{At}. Neither q′ nor the crest value is frozen at c.

Fix smooth ρ on [0,∞), equal to one near zero, 0≤ρ≤1 and vanishing on [1,∞). With η=δ² let v0(x)=−δ xρ(x/η). Let β be fixed smooth, compactly supported strictly inside (L/3,2L/3), ∫β=1, and set v=v0−Iβ, I=∫v0. Then |I|≤δη²/2=δ⁵/2, ||v0||∞≤δη=δ³ and ||v0′||∞≤δ sup|ρ(s)+sρ′(s)|. Thus uniform C0,C1 exist with ||v||∞≤C0δ³ and ||v||_{W^{1,∞}}≤C1δ. At x=0 and L the values remain c; the right derivative is −κ−δ and the left derivative κ. The periodic initial datum is continuous, mean zero and C¹ on the closed unwrapped branch; its endpoint derivatives intentionally differ. Its large second derivative is irrelevant to this C¹ label construction.

The one-sided slope w=V_ξ/X_ξ at the transported right endpoint obeys w′=V−w², so y=w+κ solves y′=2κ y−y²+f(t), y(0)=−δ, with |f|≤(5/3)C0δ³e^{At}. Dropping −y², multiplying by e^{−2κt} and integrating gives

e^{−2κt} y(t)≤−δ+[5C0δ³/(3(A−2κ))](e^{(A−2κ)t}−1).

Choose a fixed ε=κ/10, Tδ=log(2ε/δ)/(2κ). Since A−2κ=κ/2, the positive term for 0≤t≤Tδ is at most (10C0/(3κ))(2ε)^{1/4}δ^{11/4}. Its ratio to δ tends to zero as δ^{7/4}. One explicit sufficient restriction is δ≤[3κ/(20C0(2ε)^{1/4})]^{4/7}, as well as δ<2ε and δ²<L/3. Thus, throughout the existing interval up to Tδ, the bracket is ≤−δ/2. If existence reaches Tδ, w(Tδ)≤−κ−ε.

The universal first-hitting argument requires a valid continuation criterion for bounded ||u_x||∞. Let S(t)=sup_{ξ∈[0,L]}|V_ξ/X_ξ|. A continuous endpoint slope is an essential-supremum lower bound: a one-sided interval of positive measure approximates its value, and X_ξ>0 preserves positive measure. Therefore S(t)=||u_x||∞ and S is continuous in time in label coordinates. Initially S(0)<κ+ε for small δ. If it reaches κ+ε before Tδ, that first hitting is inside the existence interval. If not, S remains bounded on every finite time before the maximal endpoint and the continuation criterion excludes an endpoint ≤Tδ, yielding existence through Tδ and hence a hitting. This is not a claim that all such solutions survive until Tδ without prior departure.

For any phase θ, ||φ′(·−θ)||∞=κ. The reverse triangle inequality on essential suprema implies ||u_x−φ′(·−θ)||∞≥||u_x||∞−κ≥ε at hitting, uniformly in θ. Endpoint values alone are insufficient without branch continuity, but the closed-branch characteristic solution supplies it. A W^{1,∞} norm dominates the derivative norm whether defined as max or sum. No strong continuity of translation on W^{1,∞}, best-phase existence, L² departure, H¹ departure, or finite-time blow-up is needed or inferred.

## Adversarial criteria fixed before seeing code/reviews

1. Falsify the amplitude estimate if chain rule requires evaluating a non-existent classical φ′ at the crest, or if crossing causes an omitted term. Include both traversal directions and positive-measure crest dwell as controls.
2. Check kernel normalization and its L¹ norm, primitive sign, traveling identity, exact A, actual q′ and crest-forcing 5/3 without fixing velocity or value.
3. Check scaling and mean correction; demand fixed cutoff/bump constants and a δ-independent threshold. A broader perturbation of amplitude order δ can invalidate this particular exponential comparison and must not be accepted as equivalent evidence.
4. Verify all exponent ratios, including δ^{11/4}, with independent algebra. Also test a deliberately too-large A and too-wide support to show the control detects a failed scale.
5. Reject any proof that assumes existence through Tδ as an independent premise, or measures only a pointwise endpoint slope rather than an essential supremum.
6. Reject any orbital argument dependent on corner alignment, a minimizer of phase, or strong translation continuity. Use the phase-independent reverse triangle inequality.
7. Demand all local construction/continuation prerequisites or explicitly condition the family conclusion on them; no weaker-norm/source closure or novelty is promoted.

## Initial assessment and progress

The amplification/departure calculation is internally coherent under the local characteristic and continuation lemmas. No defect found in this independent derivation. These lemmas remain to be checked against the full original candidate, though no second-derivative control is logically needed for this family. Audit completion estimate 35%; target discovery estimate unchanged/unknown because this audit evaluates a scoped claim rather than creates a new substantive attempt.

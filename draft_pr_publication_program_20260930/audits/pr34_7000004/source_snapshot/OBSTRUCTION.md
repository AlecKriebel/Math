# 7000004: the injective-binormal ribbon question remains unresolved here

**Outcome:** no proof or counterexample to the full target. The current literature supplies useful restrictions, but neither injectivity nor a total-torsion calculation was shown to prevent cancellation in the linking number. Model: gpt-6-astra, xhigh; checked 2026-09-30.

## 1. Exact source and necessary conventions

The source is [Ghomi, *Open Problems in Geometry of Curves and Surfaces*](https://people.math.gatech.edu/~ghomi/Papers/op.pdf), Problem1.4 on p.6, within the discussion of Nirenberg's tight-surface rigidity problem. It asks whether a smooth closed immersed curve admitting a continuous injective binormal field has nonzero linking number with its small binormal push-off.

The intended convention is a unit-length binormal direction field, viewed in the sphere, normal to a continuous choice of osculating planes. The 2019 wording itself does not explicitly impose unit length. This convention is a substantive scope clarification: normalizing an arbitrary injective nonzero vector-valued field need not preserve its injectivity. The definition permits curvature-zero points. Replacing this by the Frenet formula while assuming positive curvature would change the problem. “Twisted” means nonzero linking of the two curves; it does not merely mean nonzero torsion, nonzero twist integral, or a nontrivial loop of frames.

There is also a definitional issue for the full immersed formulation: linking requires the images of the curve and its push-off to be disjoint. This is automatic for an embedded center curve and sufficiently small normal push-off, but not for every immersed curve. This issue is a scope caveat, not a counterexample to the intended geometric question.

## 2. A directly relevant later paper

[Ghomi–Raffaelli, *Topology of closed asymptotic curves on negatively curved surfaces*](https://arxiv.org/abs/2412.19266v2), revised September2025, was published in [*Journal of Geometric Analysis*35,381 (2025)](https://doi.org/10.1007/s12220-025-02200-3).

Its Problem1.1 still asks whether zero linking is possible with an injective Gauss map in the embedded negatively curved setting. Theorem1.2 gives
\[
\operatorname{Lk}(\Gamma,n)=\operatorname{Cr}(\Gamma_u)
+\frac12\#\{t:\langle u,n(t)\rangle=0\}\operatorname{sign}(\tau_g).
\tag{1}
\]
Here \(u\) is generic, crossings are signed, and \(\tau_g\) is nonvanishing. Sections2–3 justify those hypotheses. Note1.6 explicitly warns about self-linking for self-intersecting center curves. Notes5.1–5.2 force inflections when the spherical normal is injective. The paper reports Example4.2 with injective normal and linking2; Example4.1 has linking0 but noninjective normal. The displayed spherical parametrization in Example4.2 omits a factor1/6 from each of its first two coordinates, making its printed square root nonreal. The linked [primary Mathematica notebook](https://ghomi.math.gatech.edu/MathematicaNBs/Asymptotic-Examples.nb), Second Example, The Binormal, input In[1], includes both factors. This qualifies the attribution of the reported example; neither the notebook nor its full linking-number construction was independently executed or certified here. Neither reported example is a counterexample to the target.

The complete eleven-page preprint and the corresponding published sections were inspected. Their regular, embedded setting is narrower than a merely continuous binormal along an arbitrary immersion. The paper therefore cannot be used as a solution of the full source question. No later full resolution was located in the limited current search.

## 3. Why the obvious differential-geometric shortcut stalls

Suppose temporarily that a unit binormal \(B\) is sufficiently differentiable and regular. For an arclength parametrization let
\[
T=\Gamma',\qquad N=B\times T.
\]
The identities \(B\cdot T=B\cdot T'=0\) yield the signed Darboux equations
\[
T'=\kappa_sN,\qquad N'=-\kappa_sT+\tau B,\qquad B'=-\tau N.
\tag{2}
\]
Regularity of \(B\) means \(\tau\ne0\), so \(\tau\) has constant sign. The twist of this framing is
\[
\operatorname{Tw}(\Gamma,B)=\frac1{2\pi}\int\tau\,ds.
\]
A nonzero integral here does **not** prove nonzero linking: Călugăreanu's identity is
\[
\operatorname{Lk}=\operatorname{Wr}+\operatorname{Tw},
\]
and cancellation with writhe is precisely an unexcluded possibility. Formula(1) makes the analogous gap discrete: the signed crossing term must be controlled, not merely the number of intersections of \(B\) with a great circle.

Nor may one simplify by assuming \(\kappa_s\) never vanishes. For a regular simple spherical binormal, the absolute total signed geodesic curvature is less than \(2\pi\), by Gauss–Bonnet for its Jordan domain. Equations(2) identify that integral, up to orientation, with \(\int\kappa_s ds\). If \(\kappa_s\) kept one sign, Fenchel's theorem would instead give
\[
2\pi\le\int|\kappa_s|ds
=\left|\int\kappa_s ds\right|<2\pi,
\]
a contradiction. This is the known inflection obstruction; it shows why excluding inflections discards an essential part of the problem rather than solving it.

For the original continuous field, differentiability, finite spherical length, and nonzero \(B'\) cannot simply be assumed. An approximation argument would need to preserve binormal compatibility, injectivity, closure of the center curve, and the linking invariant simultaneously. No such argument was established here.

## 4. Further source cautions

The 2019 source already warns that the earlier Kovaleva approach imposes unwarranted regularity. The 2025 paper's Note5.5 additionally disputes the older claimed formula equating linking to half the number of inflections. Accordingly, that older assertion cannot be promoted to a proof without a new audit and repair.

The upstream research report's references to planar/convex special cases are not a demonstrated partial solution of this exact injective-binormal problem. On any planar subarc with nonzero curvature, a continuous unit binormal is constant. A planar closed regular curve has such a subarc and therefore cannot satisfy the injectivity hypothesis. No prior substantive proof attempt or exact duplicate was found in the repository or source report.

## 5. Precise remaining gap and disposition

Even in the smoother embedded case, the missing step is a global argument showing that injectivity of the spherical binormal excludes \(\operatorname{Wr}=-\operatorname{Tw}\), equivalently the cancellation in(1), or an explicit counterexample satisfying all hypotheses with disjoint push-off and zero linking. The continuous/immersed formulation also requires the regularity and well-definedness issues to be addressed.

The investigation stops after one substantive route with an **unresolved** outcome. The algebra checks in `verify.py` confirm only the frame identities and twist calculation. They do not provide a global topological certificate. This artifact is neither a new theorem resolving the problem nor a claim that the literal scope caveat resolves it negatively.

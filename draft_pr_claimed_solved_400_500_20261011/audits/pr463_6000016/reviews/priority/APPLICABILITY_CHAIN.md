# Authored applicability lemmas for PR #463

UTC completion checkpoint: 2026-10-12 16:10:01 UTC. Scope: frozen PR head `982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649`, problem 6000016 only. These are the priority auditor's deductions, not quotations or a claim of historical first authorship.

## Exact family and hypotheses

Write the differentiable torus as `T²=R²/Z²` with its global coordinate vector fields `X=∂x`, `Y=∂y` and coordinate one-forms. For real `t`, set

`Dᵗ=D⁰+t dx⊗dx⊗Y`.

The single nonzero Christoffel symbol is `Γʸₓₓ=t`. The torsion vanishes. The connection matrices are constant, with `Γy=0`, so their commutator and curvature vanish. On the universal cover the diffeomorphism

`Fₜ(x,y)=(u,v)=(x,y+t x²/2)`

has determinant one, inverse `(u,v)↦(u,v-t u²/2)`, and identifies `Dᵗ` with the standard connection on the entire affine plane. Thus the affine structure is complete. Integer deck translation `(m,n)` acts in developing coordinates by

`ρₜ(m,n)(u,v)=(u+m, v+n+t m u+t m²/2)`.

In particular the linear part for `(1,0)` is

`Mₜ=[[1,0],[t,1]]`.

The torus is compact and oriented. Its nowhere-vanishing two-form `ω=dx∧dy` is `Dᵗ`-parallel: the induced connection on the determinant line has coefficient trace `Γi=0`. Equivalently `Fₜ* (du∧dv)=dx∧dy` and every holonomy matrix has determinant one. The connections depend smoothly on `t` on the fixed compact manifold and converge in every `Cᵏ` norm to `D⁰`. At `t=0`, the positive definite metric `dx²+dy²` is Hessian in affine charts.

This is precisely Baues–Goldman's developing-map family with `a=t`: arXiv math/0401257v1, 20 January 2004, printed pp.24–25; v2, 14 June 2005, printed p.20. Both version passages were visually inspected. Known-family priority alone would not prove that all Hessian metrics are impossible.

## Lemma A: prior primary theorem chain in dimension two

**Claim.** For every `t≠0`, the affine torus `(T²,Dᵗ)` has no smooth positive definite Hessian metric.

**Proof.** Suppose a positive definite Hessian metric `g` exists. Delanoë's 1989 Théorème 3, §2, printed p.67, applies to a compact locally Hessian manifold and an arbitrary nondegenerate density. Apply it with the density `|ω|`. It gives a positive definite Hessian metric `g′=g+(Dᵗ)²f`, for a globally defined smooth function `f`, and a constant `C>0`, such that `det(g′)=C|ω|²`. This statement was read in the original institutional PDF and checked visually; there is no extra “special” hypothesis in the theorem used here.

Lift `g′` to the cover and express it in the global affine coordinates `(u,v)`. Its coefficients `hij` satisfy `∂k hij=∂i hkj`. The one-forms `Σi hij dui` are closed. Since `R²` is contractible they equal `dpj` for globally defined smooth functions `pj`. Symmetry `hij=hji` makes `Σj pj duj` closed, so it equals `dΦ`. Hence `hij=∂i∂j Φ` on the whole plane. Positivity makes `Φ` strictly convex. Since `|ω|` is `|du∧dv|` in these coordinates,

`det Hess Φ=C`.

For `z=Φ/√C`, the determinant is one. Jörgens's original 1954 Satz 1, printed p.130, in the official publisher preview, bounds the sums of squares of the derivatives of `r=zᵤᵤ` and `q=zᵥᵥ` at the center of a disk by constants depending only on their center values times `R⁻²`. (His notation for `q` is `t`.) For any fixed point, the smooth entire solution is defined on disks of arbitrary radius. Letting `R→∞` gives `rᵤ=rᵥ=qᵤ=qᵥ=0` there. The mixed third derivatives are included in these four derivatives, so every third derivative of `z` vanishes everywhere. Therefore `Φ` is quadratic and `H=Hess Φ` is a constant positive definite matrix.

The lifted metric descends under deck transformations, so `Mₜᵀ H Mₜ=H`. Write `H=[[a,b],[b,c]]`. Direct multiplication gives

`Mₜᵀ H Mₜ−H=[[2tb+t²c, tc],[tc,0]]`.

The off-diagonal equality requires `tc=0`. Positivity gives `c>0`, contradicting `t≠0`. This proves nonexistence of **every** positive definite Hessian metric, through replacement of the hypothetical metric, rather than an assumption that the hypothetical metric was already parallel. ∎

No statement about indefinite metrics is used. The argument includes arbitrarily small positive or negative nonzero parameters. The lifted potential is global only on the affine-plane universal cover; a global strictly convex potential on the compact torus is neither asserted nor required.

## Lemma B: separate Shima/Fox route and access qualification

Shima, *The Geometry of Hessian Structures* (World Scientific, 2007, DOI `10.1142/6241`), Corollary 8.6, printed p.164, states that a compact oriented Hessian manifold admitting a parallel volume element admits another Hessian metric whose Levi-Civita connection equals the original affine connection. Official Google Books search-within-volume receipts separately expose the full hypothesis and conclusion at page identifier `PA164`.

**Primary-page limitation.** The auditor could not retrieve a readable image of p.164 from the publisher or four official Google Books edition previews. The image endpoints returned an “image not available” placeholder; publisher requests returned HTTP 403. Thus the corollary's page number and statement are officially snippet-confirmed, but its page and proof have not been visually inspected. Do not silently upgrade this route to full primary-page verification.

**Conditional authored application.** Assuming Corollary 8.6 exactly as officially indexed, a hypothetical `g` on `(T²,Dᵗ)` satisfies compactness, orientation, Hessian positivity, and the parallel-volume hypothesis established above. The resulting metric `g̃` has `Dᵗ g̃=0`. Its lift therefore has a constant positive definite matrix in `(u,v)`. The same deck-invariance calculation `tc=0`, `c>0`, proves `t=0`. This is independent of a need to assume completeness in the corollary's hypotheses; completeness was verified for the particular family anyway.

Fox's primary arXiv 1206.3176v2 (4 April 2013), §5.2, printed p.25, was obtained and visually inspected. It explicitly reports this replacement conclusion and attributes it to Cheng–Yau 1982, Corollary 2.3. Fox corroborates the correct existential conclusion. The original Cheng–Yau proceedings chapter has not been retrieved in full, so its exact corollary numbering and any omitted hypotheses remain a primary-source access gap. Lemma A is the fully primary-page-inspected route and does not depend on resolving either access gap.

## Given-metric overstatement excluded

For the standard flat torus and `0<ε<1`,

`g=(1+ε cos(2πx))dx²+dy²`

is positive and locally Hessian, with lifted potential `(x²+y²)/2−ε cos(2πx)/(4π²)`. The affine connection `D⁰` preserves `dx∧dy`, but `D⁰g≠0`. Thus admitting a parallel volume does **not** make the given Hessian metric parallel or make `D⁰` its Levi-Civita connection. Any such stronger reading of a recent preprint is excluded from this audit. All historical applications above need and use existence of a replacement metric.

## Exact original-question implication

The original 1998 Furuhata–Matsuzoe–Urakawa item 5(b), printed p.126, attributes the compact-Hessian deformation question to Satoru Shimizu. The question permits changing affine holonomy and seeks existence of some positive definite Hessian metric after every sufficiently small affine deformation. The smoothly marked family above starts at a compact Hessian torus and has none at every nonzero parameter. Thus the assertion is false by the known family and prior theorem chain. The credited Koszul hyperbolic special case does not cover this example: its developing image is the full plane and contains full straight lines.

The mathematical implication is checkable from published primary results predating this PR. It does not identify the first author who explicitly recognized this application as an answer to the numbered 1998 question, and makes no claim that the question was explicitly answered in a particular pre-PR publication.

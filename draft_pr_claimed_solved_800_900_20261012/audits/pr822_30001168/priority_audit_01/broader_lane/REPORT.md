# Broader theorem priority audit: PR822 / problem 30001168

This bounded audit found no earlier explicitly assembled three-dimensional violation of the exact heat maximum in the inspected primary works. It does **not** certify firstness or substantial mechanism novelty. The qualitative negative answer is a straightforward newly assembled corollary of classical conformal cylinder constructions, standard Dirichlet spectral comparison, and an elementary strict bound for the round maximum. The finite smooth example and rational certificate make that assembly concrete and checkable.

The target is Morpurgo's Conjecture 1 in OWR 2009/06, §9 item (16), printed 421–422: for every smooth positive weight on the round sphere with the prescribed volume normalization, the maximum of the scaled weighted Yamabe heat trace should not exceed the round maximum. The exact primary was retrieved and inspected. The already-recorded positive small-time coefficient in dimension three is weaker than a maximum comparison. Neither the dimension ≥4 restriction nor the adjacent monotonicity problem is resolved or counted here. [OWR primary](https://doi.org/10.4171/OWR/2009/06).

## Earlier theorem families and their exact relationship

**Conformal cylinders.** Ammann–Jammes, arXiv:0708.0529 v1 (2007), current v2 (2015), and the 2011 chapter, are decisive foundations. Theorem 1.2 makes the normalized first positive conformal-Laplacian eigenvalue arbitrarily large in every compact conformal class of dimension ≥3. Example 1 in §2.5 identifies the cylinder spectral threshold as `(n−2)^2/4`; §3.2 constructs inverse-radius conformal blowups. Theorem 4.1 instead controls a fixed index strictly below this threshold. These statements are not a published heat-maximum refutation. Nevertheless, the construction can be used directly with growing numbers of cylinder modes; excluding only Theorem 4.1 would materially understate the prior mechanism. [Current preprint](https://arxiv.org/abs/0708.0529), [chapter](https://doi.org/10.1017/CBO9780511863219.002).

**Earlier capped cylinders.** Ammann–Bär's 1999 preprint / 2000 paper constructs a smooth manifold with a product cylinder of arbitrary length and fixed surrounding pieces. Its theorem compares Dirac eigenvalues with total scalar curvature, rather than the present conformal heat functional; its metric family is not asserted there to lie in an arbitrary prescribed conformal class. It supplies earlier geometric credit. [Primary](https://arxiv.org/abs/math/9909061).

**Inverse-square transformation.** Del Pino–Dolbeault–Filippas–Tertikas, equation (9) and the transformed energy (20), explicitly give the Emden–Fowler transformation from inverse-square weighted Euclidean energy to the spherical cylinder, with shift `(n−2)^2/4` in the unweighted-energy case. Their Theorems A″ and B″ concern logarithmic Sobolev functionals and radial optimizers. They do not state the compact normalized heat-maximum comparison. This is a classical analytic explanation of the same annulus/cylinder mechanism. [Primary preprint](https://arxiv.org/abs/0912.0590), [correct published article](https://doi.org/10.1016/j.jfa.2010.06.005).

**Different normalization.** Sire–Xu Theorem 1.1 bounds eigenvalues using the first-power integral of the conformal metric weight, whereas the target fixes its `n/2` power. Pérez-Ayala Theorems 1.1 and 1.3 study extremals under the same first-power normalization. Their round maximizer statement therefore cannot be substituted into the present question. [Sire–Xu](https://arxiv.org/abs/1809.06874), [Pérez-Ayala](https://arxiv.org/abs/2011.06018).

**Bubbling and fixed eigenvalues.** Ammann–Humbert Corollary 4.2 gives the second spherical conformal eigenvalue as `2^(2/n)` times the first. The current Humbert–Petrides–Premoselli paper extends fixed-index extremization to GJMS operators. For the sphere its Theorem 1.6 gives the second invariant and nonattainment; Theorem 1.7 requires `n≥2s+5`, hence `n≥7` for the Yamabe operator. It cannot count as an `n=3` heat result. Theorem 1.2 has a unique-continuation assumption, satisfied for `s=1`, and concerns attaining a fixed-index infimum over possibly singular weights. Proposition 4.3 expressly uses Ammann–Jammes for unbounded positive eigenvalues. [Ammann–Humbert](https://arxiv.org/abs/math/0502094), [current HPP](https://arxiv.org/abs/2505.08280).

**Noncompact Yamabe minimizers.** Akutagawa–Botvinnik Theorem A assumes tame cylindrical ends and a strict cylindrical Yamabe-constant inequality (with separate positive and zero cross-section cases). Theorem D characterizes equality with the spherical Yamabe constant. Appendix Propositions 7.1–7.3 address the bottom of the noncompact spectrum and conformal scalar-curvature signs. The optimized object is an energy quotient, not the full heat trace. [Primary](https://arxiv.org/abs/math/0107164).

## Checkable bridge from the classical construction

The following is an independently assembled deduction, not a claim that the earlier papers state the target conclusion.

Choose a representative `g_b` of the round conformal class that is Euclidean near one point. Such a choice follows by a smooth positive local conformal adjustment in stereographic coordinates. This is a chosen specialization; the original round metric is not locally flat. In that Euclidean ball, select the Ammann–Jammes permitted factor `F_L(r)=1/r` on `e^(−L)≤r≤1/2`. Its annulus is the exact product cylinder `S²×[0,ℓ]`, where `ℓ=L−log 2`.

For `r≤e^(−L)`, make the additional permitted choice

```
F_L(r)=e^L f(e^L r),
```

where `f` is a fixed smooth positive radial function, constant near zero, equal to `1/x` near `x=1`, and bounded by `1/x` for `0<x≤1`. A smooth convex interpolation between the constant `1` and `1/x` gives such a function. Then the core extends smoothly through the pole and has volume

```
4π ∫₀¹ f(x)³ x² dx,
```

independent of `L`. The outer part is fixed. Consequently `V_L=4πℓ+B` for one fixed finite `B`. The published condition `F_L≤1/r` alone does **not** imply this uniform cap bound for every permissible factor; the scaled-core choice is essential to this deduction.

The resulting smooth closed metric remains in the round conformal class, so its Yamabe operator is positive regardless of transition scalar-curvature signs. Longitudinal Dirichlet sine modes constant on `S²`, extended by zero, give by standard min–max

```
λ_k ≤ 1/4+(πk/ℓ)².
```

Set `a_L=(2π²/V_L)^(2/3)` and normalize the metric by `a_L`. At time `4a_L`, conformal covariance and scaling give the lower bound

```
(4a_L)^(3/2) Tr exp(−4a_L Y_normalized)
  ≥ (16π²/V_L)e^(−1) Σ_{k≥1} exp(−4π²k²/ℓ²).
```

The decreasing-Gaussian integral comparison therefore yields limit inferior at least `√π/e`. Since the accepted author comparison bounds the round all-times maximum by `129/200<13/20<√π/e`, a sufficiently long **finite** smooth cylinder disproves the exact conjecture. The author package supplies a fully specified finite metric and rational separation instead of leaving that final length unspecified.

No special spectral-limit theorem is required. The heat contribution comes from `O(ℓ)` modes. A fixed finite collection of modes contributes at most `O(1/V_L)` after normalization and cannot supply this lower bound by itself. The broad first-eigenvalue theorem alone is also insufficient; the published geometry plus this standard spectral calculation is the useful route.

For comparison, a disjoint union of spherical bubbles with volume fractions `v_i` has scaled trace `Σ v_i F_round(t/v_i^(2/3))≤max F_round`. Thus the exact spherical-bubble limit itself does not give a strict violation. Any smooth neck effect would need an additional estimate. This elementary calculation explains why fixed-index bubbling results are not a shortcut to the present maximum comparison.

## Corpus and limitations

Nine distinct primary works were inspected in relevant portions. Eleven full PDF versions were retrieved, totaling 377 PDF pages; this is a retrieval count, **not** a claim to have read every page. Complete relevant theorem hypotheses/conclusions and the identified construction or transformation sections were read; precise locations, bytes, SHA-256 hashes, dates, and current-version information appear in `SOURCE_LEDGER.json`. Forty-one discovery queries in eleven batches, primary metadata retrievals, and failed access attempts appear in `SEARCH_LEDGER.json`. Mathematical judgments rely on the primary PDFs, not snippets or third-party reviews.

Publication and version dates are separated. For example, Ammann–Jammes v1 is August 3, 2007; its author manuscript says December 8, 2008; the chapter print date is October 20, 2011 and CUP online date November 5, 2011; current arXiv v2 is October 27, 2015. Publisher-supplied Crossref date records are retained privately. The arXiv record for the logarithmic Hardy paper has a mismatched related DOI; the title-matched publisher record and authors' publication listings identify the correct JFA article, dated October 15, 2010.

All copyrighted primary copies and extracted text remain in the ignored private source directory. No outreach, Git, PR, release, or sheet mutation was performed by this lane. The public artifacts contain the audit's own analysis and bibliographic metadata. The absence of an earlier exact statement in this finite corpus is not evidence of worldwide firstness or present openness. Recommended positioning: an explicit certified counterexample assembled from classical cylinder geometry, with its narrow exact-target contribution assessed separately from the already-known mechanism.

# Biorthogonal curvature on S² × T²: credited source resolution

Problem 6800004 / AMR-067-0004. Checked 2026-10-03.

## Exact question and answer

Does the smooth product S² × T² admit a Riemannian metric whose Levi-Civita sectional curvatures satisfy

\[
K_g^\perp(\sigma)=\tfrac12\bigl(K_g(\sigma)+K_g(\sigma^{\perp_g})\bigr)>0
\]

at every point and every tangent two-plane?

**Yes, by an existing construction of Zhiqi Chen and Hui Zhang. No original solution is claimed here.**

## Decisive source

Zhiqi Chen and Hui Zhang, *Positive biorthogonal curvature on S² × T²*, [arXiv:2609.08119v1](https://arxiv.org/abs/2609.08119v1), submitted 8 September 2026. Theorem 1.2, page 2; proof in Section 4. This is a recent preprint; the checked arXiv record lists no journal reference.

Their construction applies to every flat torus R²/Λ. On the unit sphere set Xᵢ(p)=Eᵢ×p and z(p)=p₃. For 0<ε≤1/4, use

\[
g_\varepsilon(V,a,b)=|V-\varepsilon aX_1-\varepsilon bX_2|^2+a^2+b^2,
\qquad
u_\varepsilon=1+\frac{\varepsilon^4z^2}{24(1+\varepsilon^2)}.
\]

The metric is smooth and positive definite. Theorem 1.2 proves that uε²gε has K⊥≥ε⁴/384 everywhere. Choosing ε=1/4 gives the strict uniform bound 1/98304, so it answers every quantifier in the target.

The proof computes the Levi-Civita curvature, controls the two diagonal Hodge blocks, then applies a conformal correction. It is not a torsion-connection argument. The authors explicitly distinguish Pigazzini's affine-connection preprint from this Riemannian question.

## Verification and limits

The original question was matched against Morgan and Pansu, *A list of open problems in differential geometry*, Section 4, Question 4, [author-hosted PDF](https://www.imo.universite-paris-saclay.fr/~pierre.pansu/problems_MTDG.pdf), printed page 3. Both this page and the decisive theorem page were visually inspected.

The attached check_metric.py independently differentiates the metric in stereographic coordinates and forms its Levi-Civita tensor. At six rational sphere points, every curvature-operator entry agrees exactly with the source formulas. The two Hodge blocks and the rational constants also pass. These finite spot checks are diagnostics; the cited analytic proof supplies the global quantifiers.

The pinned dataset predates this September result and only records an earlier literature survey. The live UnsolvedMath page was inaccessible (HTTP 403), so no claim is made that its current wording or status was read successfully.

## Accounting

- Original proof-attempt turns: **0/5**.
- Classification proposed: **already_solved**, with full credit to Chen and Zhang.
- Source retrieval, proof review, and diagnostic checks are verification, not a new discovery.
- Independent source/proof review passed; see audit/AUDIT_REPORT.md.
- No release, DOI, or external correspondence is part of this source-resolution packet.

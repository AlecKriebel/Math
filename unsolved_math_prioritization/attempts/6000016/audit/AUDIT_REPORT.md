# Independent full audit: Stability of Hessian Metrics

**Disposition: PASS_FULL.** The frozen argument gives a complete negative answer to the unrestricted positive-definite Hessian-metric stability question in the original 1998 item 5(b). No mathematical repair is required. This is an independent AI audit, not human peer review, a novelty determination, or an administrative publication decision.

- Target metadata: 6000016 / AMR-059-0016, rank 493.
- Audit date: 3 October 2026, UTC.
- Author accounting: one substantive proof attempt, recorded as 1/5. The audit does not count verification and packaging as additional proof attempts.
- Frozen proof SHA-256: `783f927e0e1bcc309547ad58371a64aeb4428553bfc329df22c980a2b8f0bdb0`.
- Frozen manifest SHA-256: `376b54e387e261f5dfdde1058ecf6c2fc889823a54fead31350584716848c896`.

## 1. Exact target and source gate

The auditor visually inspected the original Furuhata–Matsuzoe–Urakawa article, including its title/publication information, the entire item 5 on printed p. 126, the separate item 3(e), and the reference page. The critical page was also independently rendered from the supplied original PDF, rather than relying exclusively on the author's supplied page image or transcription.

Under Satoru Shimizu's heading, item 5(b) starts with a compact Hessian manifold and specifies deformation of its affine structures. Its decisive question is: “Does every small deformation of M admit a Hessian metric?” The printed item imposes neither fixed linear holonomy nor fixed affine holonomy, and it does not exclude flat Hessian starting manifolds or two-dimensional examples. The counterexample addresses exactly this unrestricted assertion in the standard positive-definite meaning of Hessian metric.

The next sentence of the same item separates the affirmative hyperbolic case. There the universal cover is affinely equivalent to a convex domain containing no complete straight line, and the affirmative result is attributed to Koszul [7]. The present universal cover develops onto the entire affine plane, which contains complete straight lines. It therefore lies outside that special case at every parameter, including zero. Affine completeness is not the source's hyperbolicity condition. No contradiction with the quoted positive result is claimed or needed. The auditor verified this comparison in the original problem source, but did not independently audit Koszul's entire 1968 paper.

Item 3(e), elsewhere on the same printed page, concerns radial distributions and one-conformal flatness of statistical manifolds. It is a different question, with different hypotheses and conclusion. Nothing from that item or the distinct target 6000011 is used here.

The live aggregator and repository history were not independently queried in this audit. Consequently the audit certifies the mathematics against the original printed question and the frozen target identification, rather than making a new claim about live catalogue status, exhaustive prior-attempt searches, or historical priority.

## 2. Frozen-file integrity and reproducibility

All seven files present in the author packet were read. The six entries in the frozen manifest have the recorded byte counts and SHA-256 hashes. The manifest's own externally pinned hash also matches. The original author files were not changed.

The author's `check_exact.py` was inspected and rerun. Its output is byte-for-byte identical to `exact_results.json`: **41 exact identities pass**. The count includes componentwise torsion and curvature identities; it is not 41 distinct mathematical theorems.

The separate `check_audit.py` uses connection matrices and generic metric functions to cross-check the calculation independently. It passes **61 controls: 22 integrity/reproduction controls and 39 algebraic or boundary-case controls**. It accepts an explicit `--author-dir`, uses only Python 3 and SymPy, makes no network requests, and writes no files. `audit_results.json` records its deterministic output. To rerun:

```text
python check_audit.py --author-dir /path/to/frozen/author/files
```

`author_rerun.json` records the fresh author-script output. The source PDFs, rendered pages, full source texts, raw catalogue/history records, and private context are not part of these audit deliverables.

## 3. Full mathematical review

### 3.1 Global connection, torsion, and curvature

On the fixed smooth torus, the vector fields X = ∂x and Y = ∂y and the one-forms dx and dy descend from the cover even though the real-valued functions x and y do not. Thus

Dᵗ = D⁰ + t dx ⊗ dx ⊗ Y

is globally meaningful. Adding this (1,2)-tensor to D⁰ defines a connection; symmetry in its two input slots gives zero torsion. Its connection matrices in the global frame are

```text
Kx = [[0, 0], [t, 0]],     Ky = [[0, 0], [0, 0]].
```

Their coefficients are constant and every product Ki Kj vanishes. Consequently the curvature dK + K ∧ K vanishes. This is an exact statement for every real t. The trace of each matrix is zero, so dx ∧ dy is also a parallel volume form. The latter property is supplementary, not required for the integral contradiction.

### 3.2 Developing map, descent, and completeness

The map Fᵗ(x,y) = (x, y + tx²/2) is globally invertible, with inverse (u,v) ↦ (u, v − tu²/2). The Jacobian has determinant one. Directly computing J⁻¹∂iJ recovers Kx and Ky, so the asserted connection really is the pullback of the standard affine connection.

Conjugating translation by (m,n) through Fᵗ gives

```text
(u,v) ↦ (u+m, v+n+tm u+tm²/2).
```

This map is affine, its linear determinant is one, and the composition law is exactly addition in Z². The action is conjugate as a smooth action to integer translations, hence it is free, properly discontinuous, and cocompact. The equivariance identity shows that the resulting affine structure is on the same marked smooth torus.

It is irrelevant that Fᵗ itself does not descend to a self-map of the standard torus when t is nonzero. A developing map need not do that; equivariance under the displayed affine holonomy is the correct requirement. Nonzero linear holonomy also shows that the deformation has not merely rewritten the central Euclidean structure in another affine coordinate system.

Completeness holds both from the global developing diffeomorphism and from the explicit geodesics

```text
x(s) = x₀ + as,
y(s) = y₀ + bs − ta²s²/2.
```

These solve the equations with arbitrary initial positions and velocities for all real s. No blow-up or restricted coordinate domain is concealed in the example.

### 3.3 Smallness and the topology issue

The connection coefficients vary smoothly with t, and Dᵗ tends to D⁰ in C∞ on the compact fixed torus. Independently, Fᵗ and all its derivatives converge uniformly on every compact subset of the universal cover to F⁰. Fixed lifted coordinate neighborhoods provide charts with smoothly varying affine transition maps. Thus this is a genuine smooth deformation of affine structures, not merely convergence of selected curvature or holonomy invariants.

Baues–Goldman v2, printed p. 8, topologize developing maps by precisely this compact-open C∞ convergence and then pass to the quotient deformation space. Their printed p. 20 explicitly identifies this exact polynomial family as a differentiable family of complete affine tori. Those two pages were independently rendered and visually inspected.

There is a genuine but harmless subtlety: their period coordinates send t to (0, −∛t), which is continuous but not smooth at zero. Smoothness of this particular curve in that extra differentiable coordinate structure is not a condition in the printed question and does not undo the differentiable affine family. Even if such parameter smoothness were additionally desired, replacing t by s³ gives the smooth period curve (0, −s), while the connections remain smooth and every nonzero parameter still has the same obstruction. This observation is an audit clarification; it is not a required repair of the frozen proof.

### 3.4 Central Hessian metric

At t = 0, g₀ = dx² + dy² is positive definite and locally equals the Hessian of (x²+y²)/2 in lifted affine coordinates. It is a global metric, with local potentials. The argument neither requires nor asserts a global real-valued strictly convex potential on the compact torus. Thus the starting object is a compact Hessian manifold of the required kind.

### 3.5 Necessary equation for every candidate metric

For any Hessian metric of a torsion-free flat connection, Dg is symmetric in all slots in affine coordinates, since it consists of third derivatives of local potentials. The Codazzi identity is tensorial, so it may be evaluated in the global frame X,Y, even though x,y are not Dᵗ-affine coordinates when t ≠ 0.

Write an arbitrary smooth metric on the torus as

```text
g = A dx² + 2B dx dy + C dy².
```

Its lifted coefficients are periodic because the metric and the frame are global on the fixed smooth torus. Positive definiteness implies C = g(Y,Y) > 0 everywhere. No invariance, parallelism, diagonal form, closeness to g₀, or smooth dependence of g on t is assumed.

The relevant components are

```text
(Dᵗ_X g)(Y,X) = ∂xB − tC,
(Dᵗ_Y g)(X,X) = ∂yA.
```

The minus sign arises from differentiating the covariant X slot, using Dᵗ_X X = tY. Therefore the necessary equation is exactly

```text
∂xB − ∂yA = tC.
```

The other independent Codazzi component is ∂xC − ∂yB = 0. It is consistent and unnecessary for the obstruction. The independent matrix computation reproduces both equations with arbitrary A,B,C.

### 3.6 The universal global obstruction

The one-form α = g(X,·) = A dx + B dy is global, and the preceding equation says

```text
dα = t C dx ∧ dy.
```

Integrating over the oriented torus gives 0 = t ∫ C dx dy by Stokes' theorem. Equivalently, integrate the two periodic derivatives over a unit square and cancel opposite boundary values. Because C is a continuous strictly positive function on the compact torus, its integral is strictly positive. Hence t must be zero.

For every nonzero t, this contradicts existence of any positive-definite Hessian metric. The quantifier is over all smooth metrics, not over an ansatz or a bounded family. For negative t, the same equality is contradictory; alternatively d(α/t) is a positive volume form for either sign. This is an analytic proof, not a finite-sampling inference.

Together with the smooth convergence at zero, it supplies non-Hessian affine structures in every neighborhood of a Hessian structure, even within complete volume-preserving structures. A single such compact example disproves the universal stability assertion.

## 4. Adversarial boundary controls and rejected objections

- **Global-versus-local confusion:** On the noncompact cover, JᵀJ is a positive-definite Hessian metric for Dᵗ. Its B coefficient is tx and is not periodic for t ≠ 0. The check passes locally and fails exactly at descent, as the proof requires.
- **Positivity omitted:** The global indefinite metric 2 dx dy does satisfy Codazzi. In affine coordinates its local potential is uv − tu³/3. Its determinant is −1 and C = 0, so it does not contradict the positive-definite theorem. The controls verify this boundary example.
- **Only invariant metrics excluded:** Rejected. A,B,C are arbitrary smooth periodic functions throughout the derivation.
- **Wrong covariant-derivative sign:** Rejected by the direct slot calculation and independent connection-matrix calculation.
- **A global potential is silently assumed:** Rejected. Only local Hessian potentials give the tensorial necessary identity.
- **Holonomy changes invalidate the deformation:** Rejected for the original question, which imposes no fixed-holonomy restriction. The report does not claim a fixed-holonomy counterexample.
- **Baues–Goldman period-curve nonsmoothness invalidates smallness:** Rejected for the stated topology and, if necessary, also by the cubic reparameterization above.
- **Complete developing image should be hyperbolic:** Rejected. The whole affine plane contains complete lines.
- **A quotient or gauge identification could restore Hessian existence:** Rejected. Existence of a Hessian metric is invariant under affine diffeomorphism; the direct obstruction already excludes it on these fibers.
- **A published non-Riemannian affine torus automatically means no Hessian metric:** Not used. Failure of a parallel positive metric alone would be insufficient. The independent Codazzi/Stokes argument supplies the stronger conclusion.

## 5. Attribution and final scope

The family Fᵗ is exactly the map printed in Baues–Goldman v2, §5, p. 20, with their parameter a equal to t. Their §4 gives the corresponding shear construction with coordinates exchanged. The frozen proof credits that construction prominently and does not claim its novelty. The inspected passages concern affine deformation theory and do not themselves establish the all-Hessian-metrics nonexistence assertion used here. This audit verifies the elementary additional argument; it does not claim that this application was previously unknown.

No substantive gap, counterexample to the proof, or mismatch with the printed unrestricted target was found. **PASS_FULL supports the complete negative mathematical result and the author's complete-early 1/5 disposition.** It does not independently certify the live aggregator, exhaustive literature/PR history, publication permission, or first-resolution priority. Those are separate administrative or historical gates.

## References

1. H. Furuhata, H. Matsuzoe and H. Urakawa, *Open Problems in Affine Differential Geometry and Related Topics*, Interdisciplinary Information Sciences 4 (1998), 125–127. Item 5(b), printed p. 126; reference [7], printed p. 127. [Article](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_article/-char/en).
2. O. Baues and W. M. Goldman, *Is the deformation space of complete affine structures on the 2-torus smooth?*, arXiv:math/0401257v2, 14 June 2005. Printed pp. 7–8, 14–15 and 20. [Versioned source](https://arxiv.org/abs/math/0401257v2).
3. J.-L. Koszul, *Déformations de connexions localement plates*, Annales de l'Institut Fourier 18(1) (1968), 103–114. Identified by reference [7] of source 1; the present audit uses source 1's statement of the hyperbolic special case and does not purport to re-audit this paper.

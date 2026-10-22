# Independent review: radial Hilbert-space quasiconformality and ball roundness

**Verdict: PASS for the stated partial results.** The general nonradial metric-quasiconformal-to-quasisymmetric implication remains unproved. Recommended status: **unsolved, 2/5**. No mandatory correction was found. No novelty, full solution or human peer-review claim is justified.

The reviewed frozen artifact is `PARTIAL_RESULT.md`, SHA-256 `6959883e54a2e83c75392c3eb71ccb4af6fe55c84b78cf5a8513349a784ed199`. It was not changed. This independent review used gpt-6-astra at xhigh reasoning on 2026-09-30.

## 1. Primary-source hypotheses

Kapovich’s complete Problem 49 and its preceding context were checked in the author-hosted collection dated October 24, 2007; printed p. 14 was rendered and visually inspected. The preceding Euclidean statement is about **global homeomorphisms** of \(\mathbb R^n\), with \(n\ge2\). The subsequent question asks about Hilbert spaces. The brief passage does not define “quasiball,” and the title of the surrounding problem collection does not turn this into a group-boundary realization problem. The candidate appropriately states a definite metric-QC convention and proves an explicit ball estimate rather than silently choosing a stronger geometric definition. [Original source](https://www.math.ucdavis.edu/~kapovich/EPR/problems.pdf)

Väisälä’s *The Free Quasiworld*, Banach Center Publications 48 (1999), printed p. 56, Section 1.1 and equation (1.2), uses exactly the sphere-based linear dilatation and the everywhere bound \(H(x,f)\le K\) appearing in the candidate. This is not the analytic inner/outer-dilatation normalization used in every other reference. Section 6.9, printed p. 76, explicitly states the quantitative global equivalence between that Euclidean QC convention and quasisymmetry, with constants depending on \(K\) and the finite dimension. The displayed theorem was visually checked. Section 6.8(2)(a), printed p. 75, explicitly credits the invariant-three-dimensional-subspace mechanism for radial power maps. [Published primary source](https://matwbn.icm.edu.pl/ksiazki/bcp/bcp48/bcp4814.pdf)

The same article distinguishes the general Banach-space freely quasiconformal definition from bounded metric dilatation. Its FQC results cannot simply be imported as results for the candidate’s weaker metric hypothesis. This review accepts the explicitly cited, standard Euclidean theorem as an external mathematical input; it does not claim to re-prove the full Euclidean theory or to establish a current general Hilbert-space resolution.

## 2. Ball roundness without compactness or extrema

Fix a global \(\eta\)-quasisymmetric homeomorphism, a center \(x\), and \(r>0\). The candidate’s choices are
\[
 L=\sup_{\|y-x\|<r}\|f(y)-f(x)\|,
 \qquad
 \ell=\inf_{\|z-x\|\ge r}\|f(z)-f(x)\|.
\]
Taking one sphere point \(z_0\) gives a finite positive reference distance \(b\). The quasisymmetric inequalities imply \(L\le\eta(1)b\) and \(\ell\ge b/\eta(1)>0\). When one compares a point with itself in this auxiliary estimate, the inequality is trivial because \(\eta(1)\ge1\). The latter follows by applying quasisymmetry in both orders to any two distinct equal-distance points about a center.

Crucially, comparing **every interior point with every exterior point** gives the sharper combined estimate
\(L\le\eta(1)\ell\), rather than multiplying two separate estimates and obtaining a square of the constant. Approaching \(z_0\) along an interior radius and using continuity gives \(\ell\le b\le L\). No extremum is assumed to occur.

Surjectivity supplies the inner inclusion: the preimage of any point within distance \(\ell\) of \(f(x)\) cannot lie in the exterior set. The outer inclusion is strict because the image of the open ball is open. An interior image point of distance exactly \(L>0\) would admit a small outward radial displacement still in the image, contradicting the definition of \(L\). These arguments remain valid in an infinite-dimensional Hilbert space.

As an independent check on the possible nonattainment, consider the bounded invertible diagonal operator on \(\ell^2\) with alternating weights
\[
 1+\frac1{k+2},\qquad 2-\frac1{k+2},\qquad k\ge0.
\]
Every weight is strictly between one and two. The infimum and supremum of its image norm on the unit sphere are one and two, approached along basis vectors and attained by no unit vector. Its image of the unit ball still lies between the concentric open balls of radii one and two. Thus extrema really can fail to exist in this setting; the candidate’s supremum/infimum and openness proof handles the issue directly.

The conclusion is bounded concentric eccentricity about \(f(x)\). It is not a theorem identifying every such domain with a quasiball under a stronger boundary-extension or uniform-domain definition. That limitation is correctly retained.

## 3. Radial restriction and uniform constants

For the stated increasing radial profile \(\rho\), every linear subspace \(E\) is invariant and the restriction is onto \(E\), since the inverse radial profile is defined on all nonnegative radii. This gives a global Euclidean homeomorphism whenever \(E\) is finite dimensional.

For a center in \(E\), its radius-\(r\) sphere in \(E\) is a subset of the ambient sphere. Thus the restricted supremum is no larger and the restricted infimum no smaller. At all sufficiently small radii the ambient numerator is finite by continuity at the center, and the denominator is strictly positive by continuity of the inverse at its image. Therefore the inequality of linear-dilatation quotients, and then of their limsups, is legitimate even without any compact-sphere argument:
\[
 H_{f|E}(x)\le H_f(x)\le K.
\]

Any three points of a Hilbert space of dimension at least three lie in a three-dimensional **linear** subspace after extending their span if necessary. Linearity is important because it ensures radial invariance; an arbitrary affine plane would not do. Identifying this subspace isometrically with \(\mathbb R^3\), the exact theorem in Väisälä Section 6.9 gives one control function \(\eta_{K,3}\). It is independent of the chosen triple and subspace. Applying it to every triple proves the global quasisymmetric inequality with a single control function. Dimension two uses \(\eta_{K,2}\).

This does not assume a dimension-free version of the Euclidean theorem. The dimension is fixed at three before invoking it. No finite-dimensional exhaustion, convergence of constants, compactness of Hilbert spheres or normal-family limit is used.

The smooth-profile diagnostic is also correct. Fréchet differentiation gives
\[
 Df_x=\rho'(r)P_x+\frac{\rho(r)}r(I-P_x),\qquad r=\|x\|>0,
\]
where \(P_x\) is orthogonal projection on the radial line. When \(\rho'(r)>0\), the maximum and minimum stretches are the two positive displayed eigenvalues. Dimension at least two supplies a tangential direction. Hence metric linear dilatation is bounded by \(K\) precisely when
\(K^{-1}\le r\rho'(r)/\rho(r)\le K\). Fréchet differentiability gives a uniform remainder over unit directions, so this is valid in Hilbert space, not just for individual directional derivatives. Integrating the logarithmic derivative yields the stated power bounds. At the origin image radii are equal, giving dilatation one directly, whether or not the map is differentiable there.

## 4. Dimension-one control and the remaining gap

For \(f(t)=\sinh t\), the derivative is everywhere positive, so the two-sided metric linear dilatation is one. For \(t>0\), the triple \((t,2t,0)\) has equal input distances and output ratio
\[
 \frac{\sinh(2t)-\sinh t}{\sinh t}=2\cosh t-1\longrightarrow\infty.
\]
Thus this map is not globally quasisymmetric. It is a legitimate diagnostic explaining why the dimension restriction cannot be dropped, and is not promoted as a counterexample to the intended dimension-at-least-two question.

The restriction argument does not apply to a general nonradial map. Such a map need not preserve the span of a triple or map it to a finite-dimensional Euclidean subspace. Orthogonal projection of its image can lose injectivity and the metric estimates. No step in the package supplies a replacement. Therefore the original general implication, as well as any stronger unspecified quasiball conclusion, remains unresolved here.

## 5. Reproduction and verdict

All **31,997** submitted assertions reproduce byte for byte from an isolated snapshot. The verifier SHA-256 is `3bc9604f36e649239344417507d0e4cee7e0a112ccc082a1506c9d60d0cf478a`; the reproduced receipt SHA-256 is `5a953cb094cdef1601b7900521d1d67e145abbf5b90f39e41c514139acd20eba`.

The independent checker passes **3,962** exact assertions using different radial profiles \(\rho(r)=r(1+r^2)^k\), rational orthogonal embeddings of \(\mathbb R^3\) into dimensions seven and eleven, derivative and integrated-growth checks, diagonal-ellipsoid controls for nonattainment, and exact algebraic versions of the hyperbolic-sine identity. These are supporting diagnostics. The infinite-dimensional logical steps and the published Euclidean theorem are not inferred from finite tests.

Reproduction from this review directory:

```sh
(cd author_replay && python verify.py)
python independent_checks.py
```

No mandatory correction remains. The package is suitable for publication as an **unresolved partial result, 2/5**, with the radial restriction, metric-QC convention, precise ball-roundness conclusion and cited Euclidean input kept explicit. No general QC-to-QS or novelty claim is supported.

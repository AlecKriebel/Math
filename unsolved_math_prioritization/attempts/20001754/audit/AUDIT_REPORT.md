# Independent audit: AIM Problem 1.32 / 20001754

## Verdict

**PASS_PARTIAL.** The frozen mathematical package correctly establishes the stated partial results. Five substantive approaches are documented. It does **not** prove equality of the unrestricted triangle program with Cohn–Elkies, does not produce a strict separation of their infima, and does not supply a universal objective-preserving conversion. The appropriate classification is `partial_result`, with `full_target_solved: false` and `approaches_completed: 5`.

There is no mathematical blocker. Before publication, remove the coordination-specific qualifier in the final sentence of `SOURCE_GATE.md` and regenerate the author manifest. The present verdict applies to the frozen baseline identified below; a later revision should retain an explicit hash/diff verification.

## Frozen baseline and reproducibility

Audit date: 2026-10-03 UTC.

- Author manifest SHA-256: `25d884a12f36e89140c2f53e46c32fa3efa9b7d272a414cf7b334c8acf58b57b`.
- `PROOF.md` SHA-256: `d99cdba92da50e9840d1f9bfde8cfd668dc43b3edb69e81c85c99dc0aa1df81d`.
- All six files listed in the author manifest match their frozen SHA-256 values. The detailed receipt is `HASH_VERIFICATION.json`.
- The unmodified author check script was copied to a temporary directory and executed successfully. Its generated JSON matched the frozen `exact_results.json` byte-for-byte. No author file was rewritten.
- Independent controls use a separate integer-matrix implementation, spectral Gaussian factorization, symbolic normalization, and exact rational inequalities. They pass; see `independent_checks.py` and `INDEPENDENT_CHECK_RESULTS.json`.

The finite controls supplement the following analytic audit. They do not replace all-dimensional arguments or prove an optimizer exists.

## 1. Exact source and scope

The primary AIM statement was independently inspected in an available saved copy of the [original AIM page](http://aimpl.org/discreteaf/1/). It specifies the Schwartz class on R^(2n), Fourier normalization at zero, nonnegative Fourier transform, and precisely the three lengths |x|, |y|, |x-y|. There is no |x+y| condition. Its attribution and independent-rotation question agree with the package. A fresh browser retrieval of the AIM endpoint failed, so no fresh live-page availability claim is made here.

The live [Cohn–de Laat–Salmon paper](https://arxiv.org/html/2206.15373v1) was inspected. Theorem 3.1 supplies no-gap duality; Proposition 3.5 extends the same lower bound to continuous integrable test functions. Definition 4.5 and Proposition 4.7 are the requisite product formulation and value theorem. Theorem 1.4 has the additional sum-length condition, and Remark 4.9 explicitly separates known optimum values from primal attainment. The [arXiv record](https://arxiv.org/abs/2206.15373) currently lists only v1 from 2022.

The [AIM archive](https://www.aimath.org/pastworkshops/) confirms September 24–28, 2018. Historical HTTP and repository-search outcomes in `SOURCE_GATE.md` are search-history statements, not mathematical premises, and were not all independently replayed. Neither that limited search nor this audit certifies global literature novelty or an exhaustive absence of other resolutions.

## 2. Density and scaling factors

Let d be the lattice covolume. Poisson summation in 2n dimensions gives

\[
\sum_{\Lambda\times\Lambda}f
=d^{-2}\sum_{\Lambda^*\times\Lambda^*}\widehat f
\ge d^{-2}.
\]

Every nonorigin lattice pair satisfies the triangle condition, so the first sum is at most f(0,0). Thus the square-root objective bounds reciprocal covolume. At minimum distance 1, center density has the additional factor 2^(-n), and packing density has the factor vol(B_(1/2)^n). All factors in the proof are correct.

For the product-value reduction, write v_n=vol(B_1^n). If F is normalized at minimum distance 2, then f(z)=2^(2n) F(2z) is normalized at minimum distance 1. Therefore the distance-2 product raw infimum is 2^(-2n)P(C_square). The analogous one-point scaling is 2^(-n)L_n. Consequently

\[
\Delta_{\rm prod}(n,n)=v_n^2 2^{-2n}P(C_\square),\qquad
\Delta_2(n)=v_n2^{-n}L_n.
\]

The published product equality cancels these factors exactly and gives P(C_square)=L_n^2. The Schwartz/continuous comparison is applicable because the sign sets are closed and avoid a neighborhood of zero.

The sharp cases are also correctly normalized: scaling the unimodular E8 lattice from minimum sqrt(2) to 1 gives reciprocal covolume 16; scaling the unimodular Leech lattice from minimum 2 to 1 gives 2^24. Along with the one-dimensional value 1, existing sharp one-point bounds and the lattice lower bound give triangle equality in dimensions 1, 8, and 24, without a triangle primal-attainment assertion.

## 3. Symmetry claims

**Pass.** S and R each permute the unordered squared edges x², y², (x-y)². Their six matrices have determinant of absolute value 1. For an invertible pullback A, the Fourier transform is |det A|^(-1) fhat(A^(-T)z); therefore normalization, positivity, objective, and feasibility survive these six pullbacks. Simultaneous orthogonal averaging is valid and commutes with rebasing.

The independent matrix enumeration gives six elements for <S,R> and twelve for <S,T>. The identities (SR)^3=I and (ST)^3=-I are correct. The alternative T is a genuine sign-set symmetry, but its two-generator group must not be mislabeled as six elements.

The witness (2e,-3e/2) is feasible for the triangle sign set, whereas reflecting the second coordinate gives difference length 1/2. Thus independent rotations cannot be imposed by sign-set symmetry alone.

For the stronger incompatibility theorem, JR(x,y)=(x,y-x). Invariance implies f(x,y)=f(x,y-kx) for every integer k. At x≠0 this sequence escapes every compact set, so vanishing at infinity makes f(x,y)=0. Continuity then covers x=0. This works in every stated dimension.

The six-term average of every feasible function remains rebasing invariant, with Fourier value 1 at zero; it cannot be zero. The incompatibility theorem therefore proves that this average is not independently invariant. The every-feasible-value corollary is valid, including its conditional nonuniqueness conclusion when an independently invariant optimizer exists. This is not a proof against the existence of such optimizers, nor is angular dependence evidence of a strict bound improvement.

## 4. Independent subclass and dual-support obstruction

**Pass.** For nonzero admissible x,y, independent orthogonal transformations can place them in opposite directions; their difference then has length |x|+|y|≥2. Axes already satisfy the triangle condition. Hence independent triangle feasibility implies square feasibility. Conversely, independent averaging of square-feasible functions preserves feasibility and objective. The subclass identity and sign-set sandwich follow without attainment.

For n≥2, a nonzero radial nonnegative measure supported beyond radius 1 has a support point of some radius r≥1, hence the entire radius-r sphere in its support. Two distinct points of this sphere can have separation exactly 1/2. Their pair is in the product support, since both factors assign positive mass to every neighborhood, but is outside the triangle sign set. Nonnegative tensor terms cannot cancel this support. This proves the stated obstruction.

For positive dual value, the correction measure cannot vanish: Lebesgue measure, the Fourier transform of delta_0, cannot dominate a positive atom at zero. The argument excludes radial tensor certificates, not correlated certificates, nonradial lattice combs, or equality itself. The restriction n≥2 is essential and correctly present.

## 5. Edge restriction and Gaussian counterexample

**Pass.** Fourier inversion and Fubini give the three displayed slice integrals. In particular, restricting to (x,x) pushes Fourier variables to their sum; there is no missing geometric Jacobian in the coordinate parameter x. Linear injective restrictions of Schwartz functions are Schwartz. Continuity and fhat(0,0)=1 make every zero-frequency slice integral strictly positive.

Independently diagonalizing q with a=(x+y)/sqrt(2), b=(x-y)/sqrt(2) gives

\[
q=\tfrac12|a|^2+\tfrac32|b|^2.
\]

Thus its Gaussian integral is Z(beta)=(2pi/beta)^n / 3^(n/2). Fourier transformation gives H_beta as in the proof. Since multiplication by 1-q corresponds to 1+partial_beta, the Fourier multiplier is

\[
1-n/\beta+\pi^2u/\beta^2.
\]

At beta=2n it is everywhere positive. Normalization gives c=2·3^(n/2)(n/pi)^n, agreeing with the package. The sign condition follows from 2q being the sum of all three squared edge lengths; the axis and repeated-point cases are correctly treated separately.

Each edge has q=|x|². Its Gaussian second moment gives

\[
a=\tfrac34c(\pi/(2n))^{n/2},\qquad
(a^2/c)^2=\tfrac{81}{64}(3/4)^n.
\]

At n=1 the last quantity is 243/256<1, and each increment of n multiplies it by 3/4. Therefore 0<a<sqrt(c) in every dimension. The normalized edge objective c/a is strictly larger than sqrt(c), exactly the claimed failure of the proposed sufficient conversion inequality.

Crucially, q≥r²+s²-rs=(r-s)²+rs≥1 when r,s≥1, so this example is square-feasible. It cannot establish a strict triangle-versus-Cohn–Elkies separation, and the package correctly says so.

## 6. Primal tensor and exact family optimum

**Pass.** An even one-point function negative at u has g(u)g(-u)>0 at an allowed triangle pair. Its tensor therefore fails the required sign. The proposed one-point Gaussian examples have positive normalization and nonnegative Fourier transform for beta>n/2 and are strictly negative whenever |u|>1.

For the triangle Gaussian, positive decay requires beta>0. If beta<n, its unnormalized Fourier transform changes sign; a negative normalization cannot cure that. At beta=n the zero-frequency mass vanishes. Exactly beta>n permits the required positive normalization. Rewriting the objective as

\[
c_\beta=(\sqrt3/(2\pi))^n\,\beta^{n+1}/(\beta-n)
\]

makes its logarithmic derivative n(beta-n-1)/(beta(beta-n)). It decreases until beta=n+1 and increases thereafter, with divergence at both endpoints. The unique family minimum is precisely 3^(n/2)(n+1)^(n+1)/(2pi)^n. Square feasibility applies throughout this family. No global optimum claim follows.

## 7. Classification and publication review

The five approaches in `RESEARCH_LOG.md` correspond to actual separate analyses: symmetry, product duality/support, restrictions, direct primal tensors, and exact Gaussian optimization. Counting them as five completed approaches is reasonable; it does not mean five solutions of the full problem. The package appropriately labels inherited results and disclaims priority.

No downloaded source text, credentials, private correspondence, or unrelated personal information appears in the proposed public mathematical files. Remove the final coordination-specific qualifier from `SOURCE_GATE.md` before publication, then refreeze. The audit outputs contain only mathematical review, public source links, and integrity/check evidence. No remote state was changed.

The final mathematical status remains **PASS_PARTIAL**, with the unrestricted equality and universal optimizer conversion unresolved.

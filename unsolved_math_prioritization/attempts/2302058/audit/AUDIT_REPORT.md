# Independent mathematical audit of Hellerstein Problem 2.58

**Problem:** Function Theory 2.58, identifier 2302058 / AMR-022-2058  
**Date:** 3 October 2026  
**Verdict:** **PASS for the full stated existence question as an attributed known result.**  
**Recommended classification:** already solved, affirmative; resolution credited to A. E. Eremenko (1985). One substantive verification attempt is sufficient. No new-resolution claim is supported or needed.

The proof's nonzero-value normalization is valid. It does not silently replace the prescribed circle by a line or the nonzero exceptional value by zero. The explicit uniformly quasiconformal deformation, followed by uniformization and the reciprocal transformation, closes that issue. No material mathematical gap was found.

The verdict uses Eremenko's published multi-line surface construction as an external existence theorem. That is an explicitly disclosed dependency, not an existence assertion established by the computational controls. The audit does not claim to give an independent reconstruction of the omitted sewing details in the original final remark or of Volkovyskii's type theorem.

## Source and statement verification

The complete five-page original article was inspected, including the page images rather than relying on faulty OCR. The first-page masthead gives 1985; the 1984 received date is not its publication year. The exact problem and its update were read on printed page 44 of Hayman and Lingham's 2018 edition, and bibliography entry 237 was checked.

The question requires an entire function of infinite order, a finite **nonzero** Picard exceptional value α, and absence of a path to infinity on the level set |F| = |α| along which F tends to α. An omitted value qualifies. The update credits Eremenko with an example. This supports the historical classification independently of the additional normalization argument. The original 1980 problem-list leaf was not part of the inspected evidence; the 2018 edition supplies the exact statement used here. [Hayman and Lingham, Problem and Update 2.58](https://arxiv.org/abs/1809.07200v2).

Eremenko's main theorem concerns real-image asymptotic curves. Example 2 supplies a simply connected surface without real-projection rays and makes it parabolic. The final remark on page 309 states the analogous multi-line construction, with forbidden projection lines Im w = 2πk. It imposes finiteness of logarithmic branch points over every finite-width vertical strip and then uses a horizontal stretching to meet the preceding parabolicity condition. Logarithmic singularities are ends of the inverse surface, not finite ramification points included in the regular surface. Thus the regular projection is locally univalent. [Eremenko, full article, pages 305–309](https://www.math.purdue.edu/~eremenko/dvi/naturalac.pdf).

The finite-strip property is the relevant one for the horizontal stretching: singularities can be enumerated with absolute real parts tending to infinity, counting finite multiplicities at repeated coordinates. An increasing stretch can therefore send their absolute real coordinates arbitrarily far out. Its horizontal action preserves the forbidden horizontal lines and their ray-lifting property. The original statement is terse about the multi-line sewing, but the required surface properties are actually stated there; they were not inferred just from the abstract, the single-line example, or the final exponential.

The final exponential in the source omits zero. That sentence alone, or an unsupported translation of that function, would not verify the present circle condition. The submitted proof correctly avoids that shortcut.

## Global deformation and its analytic structure

Set b_k = π/2 + kπ. The affine change A(w) = w/2 + iπ/2 takes the published forbidden levels to precisely those b_k and preserves right-going rays. Only the right-going case is needed.

For the submitted function a, the seam values agree:

- a(x) = π/6 when x ≤ 0;
- a(x) = arcsin(e^(−x)/2) when x ≥ 0;
- 0 < a(x) ≤ π/6;
- for x > 0, a′(x) = −e^(−x)/sqrt(4 − e^(−2x)), so |a′(x)| ≤ 1/sqrt(3).

Consequently a is globally Lipschitz. Put d = 1 − π/6 > 0 and Ψ(x+iy) = x + i(y+a(x)sin y). For fixed x the second coordinate has derivative at least d, and differs from y by at most π/6. It is therefore an increasing bijection of the real line. Since the first coordinate stays x, Ψ is a global bijection of the plane.

This is genuinely a bilipschitz homeomorphism, not merely a locally injective map. To see the inverse estimate explicitly, let v_j = y_j+a(x_j)sin y_j. The fixed-x lower derivative bound and the Lipschitz bound on a give

    d |y_1−y_2| ≤ |v_1−v_2| + |x_1−x_2|/sqrt(3).

Together with the unchanged first coordinate this bounds the global inverse. The forward Lipschitz estimate follows from the same bounds. Almost everywhere,

    DΨ = [[1, 0], [a′(x)sin y, 1+a(x)cos y]].

Its determinant is at least d. Its squared Frobenius norm is at most 1+1/3+(1+π/6)². Thus the stated uniform quasiconformal distortion bound is valid. The nonsmooth seam x=0 has measure zero, and global Lipschitz regularity supplies the required absolute continuity; the seam does not invalidate quasiconformality.

The change of surface structure is also sound. On every sufficiently small domain where p₀ is injective, Ψ composed with p₀ is a topological coordinate. Two such coordinates have identity transition maps on their overlap. They consequently define a Riemann surface structure with holomorphic locally univalent projection p₁. In these respective coordinates the identity between the original and new surfaces is Ψ, so its quasiconformal constant is uniform over all sheets.

## Parabolicity and existence of the entire functions

A bounded quasiconformal change preserves the parabolic type in the situation used here. This is not an appeal to invariance under an arbitrary homeomorphism.

For completeness, if the new simply connected noncompact surface were a disc, uniformizations would yield a K-quasiconformal homeomorphism T from the plane onto the unit disc. Normalize T(0)=0. The images of the annuli 1<|z|<R have moduli at least log R/(2πK). The compact set T(closed unit disc) contains some closed disc of radius r>0, while T(|z|<R) lies in the unit disc. Ring-domain monotonicity bounds all those image moduli by log(1/r)/(2π), a contradiction as R tends to infinity. The sphere is excluded by noncompactness. Uniformization therefore gives a conformal isomorphism φ from the plane onto the deformed surface.

It follows that H = p₁ composed with φ is entire and locally univalent. In particular it is nonconstant. Then q = exp H is entire and zero-free, and F = 1+exp(−H) is entire, nonconstant, and omits 1. No pole, branch cut, or unproved global logarithm is introduced at this stage.

## The exact circle and every possible path

The decisive identity is exact:

    |1+1/q|=1  iff  |q+1|=|q|  iff  Re q=−1/2,

for q≠0. Also F→1 iff |q|→infinity. Thus a hypothetical forbidden path produces x = Re H tending to positive infinity, and on a tail with x>0 it satisfies

    cos(Im H) = −e^(−x)/2.

The complete solution set of that equation is

    Im H = b_k + (−1)^k a(x),  k in the integers.

This includes both alternating families; no logarithmic branch has been omitted. These graphs are disjoint for x>0. Indeed their successive vertical gaps are at least π−2a(x) > 2π/3. Along a continuous connected tail, the graph index is locally constant and hence constant. It cannot drift between different indices by winding around zero.

Since sin b_k = (−1)^k, the displayed graph is exactly the image under Ψ of x+ib_k. Pulling the path through φ and the underlying surface identity therefore gives a continuous path in p₀^(−1)(Im w=b_k) whose real projection tends to positive infinity.

The passage from an arbitrary, possibly backtracking path to a lifted ray is justified. Because p₀ is locally univalent, this inverse image is a regular one-dimensional manifold without vertices. On any of its connected components, the real projection is a local diffeomorphism to the real line. A circular component is impossible because a continuous real coordinate on a circle has extrema. On an interval-type component its derivative has constant sign, so the coordinate is strictly monotone and maps the component homeomorphically onto an open interval. The connected tail stays in one component. Its unbounded positive projection forces that interval to contain a right half-line, yielding a forbidden lifted ray.

There is no extra escape assumption hidden in this last extraction. Along the extracted ray the continuous projection tends to infinity, so the ray leaves every compact subset of the surface. The original path was already assumed to tend to infinity in the uniformizing plane. The contradiction excludes every path in the exact level circle tending to the omitted value.

## Infinite order and the parameter α

The growth argument is valid and does not assume that order was preserved by the deformation.

If a nonconstant entire G of finite order omits 1, then G−1 is zero-free of finite order. Hadamard factorization gives G=1+exp P for a nonconstant polynomial P. For sufficiently small t>0,

    W(t) = log(2 sin(t/2)) + i(π/2+t/2)

satisfies exp W(t)=exp(it)−1 and Re W(t) tends to negative infinity as t decreases to zero. Choose a left half-plane containing the tail of W and avoiding the finitely many critical values of P. Properness of P makes its preimage an unbranched finite covering there. Since the half-plane is simply connected, each covering component supplies an inverse branch Z. The path z(t)=Z(W(t)) has |z(t)| tending to infinity and G(z(t))=exp(it). Reparametrizing t downward gives a natural asymptotic path on |G|=1 to 1.

The constructed F admits no such path, so it cannot have finite order. This also excludes order zero and every positive finite order. The argument makes no unnecessary claim about preservation of lower order.

Finally, for each specified α≠0, αF is nonconstant entire, omits α, has infinite order, and has the relevant path exactly when F does. All requested quantifiers and the nonzero condition are covered.

## Reproduction and limits

All eight frozen author files match their declared SHA-256 values. The submitted checker was copied before execution so that none of those files was written. Its 2,593 checks pass, and the reproduced JSON is byte-identical to the submitted result. Hash verification and reproduction records accompany this report.

Those checks establish finite algebraic and transcription controls. They do not establish a Riemann surface's existence, parabolicity, uniformization, absence of all asymptotic paths, or infinite order. The PASS above is based on the analytic reasoning and the identified published existence theorem, not on the check count.

One nonblocking documentation discrepancy remains: Section 6 says the script samples the deformation and its inverse, but the script does not numerically invert Ψ. It tests the deformation, determinant samples, reciprocal circle algebra, and a finite-order comparison path. The analytic inverse estimate is valid, so this wording does not affect the proof. It could be narrowed to describe the actual tests.

## Final determination

**Full PASS, with the published theorem dependency explicitly retained.** The frozen proof validly transfers the source surface to the nonzero exceptional-value circle formulation and establishes infinite order. A claim of a completely self-contained new construction would exceed what was checked, but the proposed attributed historical-resolution classification is supported. No mathematical repair is required for that classification.

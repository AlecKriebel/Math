# Independent audit B: rough-M deformation counterexample

## Decision

**ACCEPT the complete frozen v2 mathematical proof for its explicitly stated scope. No blocking correction is required.**

The accepted conclusion is failure of **summed** upper semicontinuity of the rough invariant `K.(K+D)` in unrestricted reduced multibranch delta-constant plane-curve deformations. It is a negative answer to the unrestricted literal, summed reading of OWR Questions 2-3. It is **not** a counterexample to the explicitly unibranched parametric Conjecture 3.8 in the published 2014 paper. It does not establish a novelty claim, a present-day literature-status claim, or the resolution of a fine-M conjecture.

This report independently reviews all ten proof sections, the source scope, the exact equations, algebraic and analytic flatness, simultaneous normalization, the fixed representative and boundary, every singularity and invariant, and the optional all-n extension. No other auditor's report was read, and no helpers were used. The candidate's checker was reviewed and rerun; a separate implementation was also written without importing its code.

## Audited identity

- Candidate: `plane_curve_m_30001345`, version 2
- Frozen proof: `PROOF.md`, 16,696 bytes
- Proof SHA-256: `561b189c2091eaeccccf89fdd933b2300ec676a871d7229ebfaf8c806962fe8b`
- Candidate frozen-manifest SHA-256: `199dc44fdb8de8f37024d170e6246281e1a7b6b5b7e1cdd94a21f4a1b195e478`
- Audit date: 2026-10-07 UTC

Every candidate file listed by its frozen manifest was checked against both its size and SHA-256. The proof was read in full after the author identified this freeze. The audit does not transfer automatically to later edits.

## 1. Primary-source scope and notation

### Original report

OWR printed p. 2446 visibly uses a bar over M and defines it by `K.(K+D)`. Questions 2 and 3 impose no explicit unibranch or irreducibility hypothesis; Question 3 adds delta constancy. The immediately subsequent p. 2447 considers one central singular point and several nearby singular points in a fixed transverse ball. That context supports a summed interpretation. Its later one-branch signature estimate and cuspidal/node assumptions belong to the subsequent restricted estimates, not to the text of Questions 2-3. The report's fine expression has a plus `N^2` sign. [Primary PDF, printed pp. 2446-2447](https://ems.press/content/serial-article-files/46242?nt=1).

This is a scope reading of the stated questions, not evidence concerning an unstated intended restriction. A single tracked singular section would be a different assertion: the present nearby local value along the origin is 1, rather than the total 12. Therefore the word **summed** is essential.

### Published paper

The published 2014 version requires flatness, transverse boundary and locality in Section 2. Definition 2.1 makes a parametric deformation both rational and unibranched; Conjecture 3.8 uses that term and sums nearby rough invariants. Definition 3.3 confirms `K.(K+D)` for multibranch germs. Definition 3.5 instead gives the fine invariant with a minus `N^2` sign. Remark 3.4 warns that Orevkov's other multibranch rough normalization differs by the branch count minus one. These distinctions cannot be silently merged. [Published PDF, printed pp. 574-577](https://ir.library.osaka-u.ac.jp/repo/ouka/all/50809/ojm51_03_573.pdf).

The accepted construction has nine central branches. Its normalization has nine disks, so it is rational but fails the unibranched hypothesis. The candidate correctly preserves that limitation and does not use either fine convention or the alternative multibranch normalization in its arithmetic.

### Attribution

Roulleau-Urzua Proposition 3.1, printed p. 291, identifies the classical dual Hesse equation and its twelve triple points. This was checked in the retained published PDF, including the rendered page. The equation there differs from the candidate only by an overall sign. The attribution is sound; the proof independently establishes all required incidences. [Publisher record](https://annals.math.princeton.edu/2015/182-1/p06).

## 2. Complete arrangement and its degeneration

Write the three groups as `X=qY`, `Y=qZ`, `Z=qX`, where q ranges over the cube roots of unity.

- Within each group, the three distinct lines meet at exactly one coordinate vertex. No line of another group passes through that vertex.
- Between groups, the solutions are the nine distinct points `[omega^(i+j):omega^j:1]`.
- Exactly one line of each group passes through each of these nine points.
- All incident lines are distinct, and distinct projective lines have distinct tangents at their intersection.
- These twelve triples exhaust all 36 unordered line pairs, so there are no unlisted nodes or higher multiple points.

The line `X+2Y+4Z=0` misses the coordinate vertices. At the other nine points its representative value has modulus at least `4-2-1=1`. Hence all pair intersections are affine and no two affine arrangement lines are parallel. This last fact is important: it makes the nine central directions pairwise distinct.

The affine chart substitution and scaling give exactly

`F=(x^3-y^3)(64y^3-(t-x-2y)^3)((t-x-2y)^3-64x^3)`.

I checked its factorization into the nine displayed linear forms independently using the exact algebraic field `QQ(sqrt(-3))`. There is no omitted scalar, incorrect sign, or incorrect coefficient. For `t!=0`, the invertible scaling map from the fixed affine arrangement supplies exactly the twelve ordinary triple points. At `t=0`, the same nine spatial directions meet only at the origin, producing an ordinary ninefold point. All fibers are reduced.

## 3. Flatness is established in both categories

The polynomial has x-degree nine and constant x-leading coefficient `-65`. Dividing by that nonzero scalar gives a monic equation. Thus its quotient ring is free over `C[y,t]` on `1,x,...,x^8`, and is flat over `C[t]`. This is an algebraic proof of flatness, not an inference from delta constancy.

The analytic argument also works at every point of every sufficiently small fiber. In an ambient convergent-power-series local ring, the equation is a unit times the product of the distinct plane factors passing through the point. No nonunit plane factor is a multiple of `t-t0`, because every factor has a nonzero spatial coefficient. Unique factorization implies that multiplication by `t-t0` is injective in the quotient. Over the discrete valuation ring `C{t-t0}`, this is torsion-freeness and hence flatness. Restricting to an open ball does not change the local calculation.

The distinction between the analytic open-ball family and its compact closure used for boundary statements is correctly made. The claim does not improperly treat a closed ball as a complex-analytic open set.

## 4. Finite simultaneous normalization

Each total-space component is a plane `a_i*x+b_i*y+c_i*t=0` with `a_i!=0`. Thus it is the graph

`x=-(b_i/a_i)*y-(c_i/a_i)*t`

over `(y,t)`, and is smooth and flat over the t-axis. The disjoint union of these nine planes maps finitely to the total space: its algebra is a finite direct sum of cyclic modules over the original coordinate ring.

The original ring injects into that sum because the intersection of the distinct principal prime ideals equals their product. The total quotient ring splits into the fraction fields of the nine components. The finite sum is normal and has that same total quotient ring, so it is the full integral closure. The written integrality argument is valid.

For every parameter, including zero, the spatial lines remain distinct. Base-changing this explicit normalization map to a fiber gives the disjoint union of precisely its nine smooth lines. This verifies simultaneous normalization directly, rather than assuming that normalization of a total space commutes with an arbitrary specialization. Finiteness and the componentwise local description persist under analytic restriction to the ball.

## 5. Local analytic admissibility and the fixed boundary

The proof uses the unit ball and `|t|<1/4`. The nine nonvertex chart points have squared norm at most 2; the three vertices satisfy the same bound. Therefore all scaled singularities are strictly inside the radius-1/2 ball. My exact enumeration obtains the stronger maximum chart squared norm 1, but no sharpening is needed.

For a line `a*x+b*y+c*t=0`, its squared distance from the origin is

`|c|^2*|t|^2/(|a|^2+|b|^2)`.

The exact coefficients of `|t|^2` are

`0, 0, 0, 1/37, 1/13, 1/13, 1/29, 1/17, 1/17`.

They verify, and strengthen, the proof's coarse bounds. Each line meets the closed unit ball in a genuine disk and meets the sphere transversely. No line intersections occur on the boundary, because all pair intersections were already placed inside radius 1/2. Consequently the full reduced curve is smooth and transverse along the sphere, not merely each component considered separately.

For completeness, a boundary parametrization can be built from the closest point

`p_i(t)=-c_i*t*(conj(a_i),conj(b_i))/(|a_i|^2+|b_i|^2)`

and any fixed unit vector in the complex kernel of `(a_i,b_i)`. Its circle radius is `sqrt(1-||p_i(t)||^2)`. These formulas vary smoothly in the two real parameter coordinates and give nine disjoint embedded circles throughout the disk. Along any parameter path this is an isotopy of links.

The central fiber is conical and has only the origin singular. Its sphere intersection is its local singularity link at every radius, so the apparently macroscopic unit radius introduces no locality failure. Simultaneously scaling the spatial and parameter coordinates gives arbitrarily small representatives. Thus all the source's ordinary deformation conditions are met.

Every normalized restricted fiber consists of nine disks and has total geometric genus zero. This does not mean the singular nearby union is topologically a disk. As an additional consistency check, identifying three distinct points at each of twelve triple points gives Euler characteristic `9-12*(3-1)=-15`; the connected nearby union has first Betti number 16. This does not contradict geometric genus zero, which concerns the normalization, or delta constancy. It reinforces why the later unibranched parametric hypothesis matters.

## 6. Delta and rough-M calculations

The local normalization exact sequence in the proof is correct for relatively prime reduced factors. It gives additivity of delta with the pairwise intersection multiplicity. For an ordinary r-fold point the branches are smooth and all pairwise intersection multiplicities are one, so delta is `r*(r-1)/2`.

For `r>=3`, one blowup is a minimal embedded normal-crossings resolution. The exceptional curve has self-intersection `-1`; its strict-transform intersections total r. The exceptional-supported canonical class is `K=E`, by adjunction. Therefore

`K.(K+D)=E.(C'+2E)=r-2`.

The node convention causes no difficulty and is not needed for the main example. If resolved without a blowup its invariant is zero; the displayed expression agrees.

Consequently:

- Central: delta `9*8/2=36`; rough M `9-2=7`
- Nearby: twelve triples, total delta `12*3=36`; total rough M `12*1=12`
- Semicontinuity excess: `12-7=5>0`

This is exactly the failure direction for upper semicontinuity at the central parameter. All nearby singularities are included in the fixed representative. No genus, branch, multiplicity, or singularity contribution has been discarded.

## 7. Optional Fermat extension

The all-n reasoning in Section 9 is also valid. For primitive n-th roots, the three same-group vertices have multiplicity n, and the n-squared cross-group points are ordinary triples. Distinct pairs of groups still produce the stated points uniquely, and the incidence count is exhaustive. The same infinity misses every such point by the modulus bound. All normalized components remain plane graphs: their x-coefficients are `1`, `q`, and `-(1+4q)`, all nonzero for `|q|=1`.

The same fixed-ball construction applies, and the algebraic/analytic flatness and componentwise normalization proofs continue to hold. The totals are

`3*n*(n-1)/2+3*n^2=(3*n)*(3*n-1)/2`

and rough-M excess

`3*(n-2)+n^2-(3*n-2)=n^2-4`.

For every `n>=3` this is positive and unbounded. The universal conclusion rests on the written arbitrary-n argument; the finite n=3,...,100 checker run is only a supplement. An independent n=2 control gives excess zero, as the formula predicts, so the claimed strict range is not being artificially extended.

## 8. Executable audit and failure controls

The candidate checker passed under normal Python and `python -O`; both outputs reproduced `CHECK_RESULTS.json` byte for byte. Each reports 1,515,405 exact checks and four negative controls. Most of that large count comes from finite-range pair-coverage checks; it is not a formal proof certificate.

The separate `independent_checks.py` uses SymPy 1.14.0, rational exact number-field arithmetic, and direct affine pair solving. It imports none of the candidate checker and reconstructs the line equations, intersections, complete incidence sets, polynomial product, coefficient, spatial directions, radius bounds, gradient vanishing and invariant totals. Its 248 checks passed under both normal and optimized Python with byte-identical output.

Four actual perturbed-input controls were detected:

1. Delete one line: the twelve-triple incidence requirement fails.
2. Add `x^9` to the polynomial: the required line product no longer matches.
3. Use the nongeneric infinity `X+Y+Z=0`: at least one spatial direction determinant vanishes.
4. Duplicate a line direction: a pair determinant vanishes.

Two controls guard against reporting a counterexample for every line degeneration:

- The n=2 Fermat arrangement has three nodes and four triples; delta is 15 and both central and nearby rough totals are 4.
- Nine lines `x-i*y-i^2*t=0`, `i=0,...,8`, have 36 ordinary double points for nonzero t. Delta is 36, while nearby rough M is 0 versus central 7.

No executable check is represented as certifying analytic flatness, normalization, the all-n quantifier or the source interpretation. Those were audited above as mathematical arguments.

## 9. Source-byte and inspection integrity

Both principal PDFs were independently retrieved from their public publisher/institution URLs during this audit. The OWR bytes exactly match the candidate's retained source. The OUKA response has the same byte count as the retained source but a different SHA-256. The only differences are 30 byte positions in the second PDF trailer ID, within offsets 379410-379441 inclusive. The complete layout-text extraction is byte-identical. This is not reported as raw file identity.

Relevant newly retrieved pages were rendered and visually inspected: OWR 2446-2447 and Borodzik 574-577. The retained Annals page 291 was separately rendered and inspected. Public bibliographic records were checked. Public-source metadata, exact byte comparisons and the retrieval/inspection record appear in `SOURCE_METADATA.json`. The audit packet contains no downloaded source PDFs, extracted paper text, source-page images, dataset records, or private coordination material.

## 10. Acceptance boundary and required presentation

There is no mathematical repair required in the frozen proof. The following boundaries are substantive and should remain visible in any acceptance summary:

- State the invariant as the rough `K.(K+D)` convention.
- State that the nearby value is the sum over all singularities.
- State that multibranch central fibers are allowed.
- Preserve the explicit nonclaim concerning published Conjecture 3.8, fine-M conjectures and novelty.
- Treat the result as a refutation of the unrestricted formulation, without inferring the source author's unstated intent or asserting a comprehensive current-literature resolution.

With those already-present boundaries, this is a complete, independently checked counterexample rather than a numerical candidate or an incomplete arrangement sketch.

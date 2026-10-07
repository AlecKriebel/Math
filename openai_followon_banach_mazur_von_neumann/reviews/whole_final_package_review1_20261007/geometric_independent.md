# Independent geometric and nonseparable-scope review of final candidate v1

Reviewed at: 2026-10-07T14:42:15.060953+00:00.

Frozen source: `reviews/versions/final_candidate_v1/manuscript/main.tex`, SHA-256 `46a02c0cd03f798459a9cfd8fb1cd5e03c4e599208a2a53750d3b218b7e96dc4`.

Roydor source: complete user-supplied 26-page publisher-formatted PDF `/Users/alec/Downloads/roydor2020.pdf`, SHA-256 `2320e92723841bd9414c4d846a489bbe78d01a03403b8078ca43354407cfacb4`. I read the complete 26-page extracted reading text, including the introduction, all proofs and concluding remarks, and independently rendered and visually inspected physical PDF pages 2, 6, 7, 10, 11, 12, 13, 15 and 23. These include every quantitative prerequisite used in the candidate and the published separable-predual restriction and original type-I reconstruction.

This review was conducted from the frozen manuscript and primary sources, without relying on prior favorable project reports. Its scope is the geometric reduction, source hypotheses and arbitrary-predual extension. It does not constitute a fresh audit of family 295's full cohomology proof, a Lean kernel check, a priority certification, or a metadata/license/publication review. The deformation lemma is used as the explicitly stated fixed-algebra lemma; I checked its application, transport direction, unitality and involution compatibility here, but the independent complete algebraic audit is a separate review task.

## Verdict

**PASS within this review scope: no substantive gap or unsupported nonseparable extension found.** The proof genuinely avoids the separable-predual hypothesis rather than silently deleting it from Roydor's Theorem 1.2. The fixed-source choice of `P` and `E=eOe`, followed by full-carrier rank reconstruction, supplies the needed quantifiers for arbitrary centers and arbitrary infinite type-I cardinal dimensions. No repair is required by this geometric review.

The remaining external mathematical inputs are openly attributed: the all-algebra cohomology theorem, Roydor's specified geometric estimates, and standard projection/Jordan structure theory. My verdict is conditional on those stated inputs and the independently checked deformation lemma; it is not a publication authorization or a claim of conventional human peer review.

## 1. Exact Roydor prerequisites

The source's printed Theorem 1.2, physical page 2, assumes that the fixed source algebra has **separable predual**. Its cohomological hypotheses are ordinary bounded `H^2(M,M)=0` and closed actual-image `B^3(M,M)` in `Z^3(M,M)`. The candidate correctly states this restriction and uses it only for the immediate separable case. It does not use the source's unrestricted slides as a substitute for the article proof.

The following quantitative results used in the new argument have no separability hypothesis in their statements or proofs:

| Source result | Exact relevant hypothesis and conclusion | Candidate application |
| --- | --- | --- |
| Corollary 2.4, p. 6 | Unital complex C*-algebras; ordinary distance at most `1+10^-4`; unital self-adjoint isomorphism norm parameters tend to one, with the displayed `10 sqrt(distance-1)` estimate. | Normalize each initial ordinary near isomorphism. A strict distance bound supplies an actual map, so no attainment is needed. |
| Proposition 2.13, pp. 10–11 | Unital self-adjoint onto isomorphism, both norms at most `1+t`; projections round within `r(t)=140 sqrt(t)` for `t<10^-5`; centers correspond by a *-isomorphism for `t<10^-8`; commutative source iff target is commutative. | Global central partition, noncentral projection rounding, commutative corner, and carrier proof. |
| Lemma 2.5, p. 7 | Unital self-adjoint map, norm at most `1+t`; if `x<=y`, then `T(x)<=T(y)+gamma(t)||x-y||1`, with `gamma(t)=2(1+t)sqrt(2t+t^2)`. | Apply to the unital self-adjoint inverse and projections `k<=c(k)`; their difference has norm at most one. |
| Lemma 3.1, pp. 11–13 | Same two-sided norm assumptions; `t<10^-8`; any `q` within the rounding radius of a projection `p`; onto unital self-adjoint corner isomorphism with norms at most `1+142 sqrt(t)` and `1+988 sqrt(t)`. | Fixed central pieces and the two corners inside the odd part. No parity hypothesis is needed for this lemma. |
| Theorem 3.2, pp. 13–17 | Same two-sided norm assumptions; `t<5*10^-13`; finite homogeneous type-I degrees of the source are all even. Central multiplicative/anti-multiplicative block decomposition with ordinary bilinear defects at most `3147585 sqrt(t)`. | Applied only to the fixed halving source algebra and its normalized maps. |

I also independently checked the corner isomorphism estimate. Writing `C=qT(p)q` and `Ttilde(x)=qT(x)q`, the lower bound for `Ttilde` is `(1+t)^-1-742 sqrt(t)`. Surjectivity follows by taking `x=pT^-1(y)p` and applying the triple-product estimate before compression; the error is at most `742(1+t)sqrt(t)`, less than one. Unitalization by `C^-1/2` is legitimate because `C` is positive invertible in the corner.

There is a harmless compressed calculation at the end of the source proof: its final lower bound using `986 sqrt(t)` alone does not imply the printed `988 sqrt(t)` inverse estimate throughout the entire stated `t<10^-8` range. The theorem's inverse estimate nevertheless follows directly from the sharper pre-unitalization bound:

`||(T_p^q)^-1|| <= ||C|| ||Ttilde^-1|| <= (1+t)^2/[1-742(1+t)sqrt(t)] <= 1+988 sqrt(t)`.

For the last inequality put `u=sqrt(t)<=10^-4`; after clearing the positive denominator, the difference is

`u[246-733098u-742u^2-733097u^3] > 0`.

Thus the cited estimate itself is valid, its arbitrary-predual scope is unaffected, and no manuscript correction is required. The manuscript also needs only sufficiently small parameters, where the source's coarser final inference already works. This check supplies an independent elementary justification rather than assuming that abbreviated numerical inference.

The proof of Theorem 3.2 starts with a two-by-two matrix-unit system whose diagonal projections sum to the unit. Its subsequent seven claims use finitely many operator identities, norms, rounding, and centrality estimates. They do not enumerate fibers, assume countable decomposability or separable representation, or restrict the commutant algebra's density. Consequently the even-finite-degree/halving assumption is the relevant scope restriction, not separability.

The candidate correctly records the source's Claim 4 heading typo: the off-diagonal relation must be `T(e_ij) approximately g_ij+h_ji`, which is the actual relation proved immediately above and used in Claim 7. I checked the printed page, not merely the OCR. This is a transcription issue in the source heading; the estimates used in the candidate are those of the correct argument.

The proof does not invoke Roydor's Lemma 4.3 or Theorem 1.1. In particular, it never requires applying the parity-sensitive approximate multiplicative decomposition to an arbitrary noncentral compression, or preserving infiniteness using that problematic compression invocation.

## 2. Fixed-halving transport

For central source and target projections `p,q`, the two maps of Lemma 3.1 are onto their respective full central pieces, complex linear, *-preserving, and unital for the corner units. Therefore their direct sum `F` is onto all of `W`, is unital and *-preserving, and has inverse norm equal to the maximum of the two block inverse norms. Zero blocks can simply be omitted.

Centrality of `q` makes

`y diamond z = q yz + (1-q) zy`

an associative unital C*-product on the same complete normed *-space, with the same Jordan product. Mixed block products vanish. Thus the ordinary bilinear defect of `F` for this product is the maximum of the block multiplicative and anti-multiplicative defects. This justifies the manuscript's bound

`||mu-m_V|| <= (1+988 sqrt(t))*3147585 sqrt(t)`

for `mu(x,y)=F^-1(F(x) diamond F(y))`. The pulled-back multiplication has the original unit and the required reversed-adjoint symmetry. Applying the stated deformation lemma to the **whole fixed V** is legitimate. If `Phi mu = m_V(Phi.,Phi.)`, the desired exact homomorphism is indeed `F Phi^-1` (the orientation in the manuscript is correct).

The crucial quantitative point is that the deformation constants belong to fixed `V`, not to the central `p` selected by Theorem 3.2. The argument would not be valid merely by taking arbitrary point-dependent thresholds for `pV` and `(1-p)V`; that unsupported step is absent here.

## 3. Full-carrier preservation

I reconstructed the proof independently. Let `w=c_D(k)` and `z=theta^-1(w)`. Applying approximate order to `T^-1` is permitted because it is again unital and self-adjoint, with norm at most `1+t`. Since `k<=w` are projections,

`T^-1(k) <= T^-1(w)+gamma(t)1`.

The errors `h-T^-1(k)` and `T^-1(w)-z` each have norm at most `(1+t)r(t)`, yielding exactly the candidate's estimate

`h-z <= a(t)1`, where `a(t)=2(1+t)r(t)+gamma(t)`.

This scalar tends to zero. Once `a(t)<1`, compress by `1-z`. Because `z` is central, `h(1-z)` is a projection. A nonzero projection cannot be bounded above by `a(t)(1-z)` for `a(t)<1`. Hence `h<=z`; full source carrier then forces `z=1`, and so `w=1`. The same reasoning applies to `1-h` and `1-k` because `T(1-h)=1-T(h)`.

This proof works for arbitrary projection lattices and centers. It neither assumes that the central carrier is obtained by a countable sequence nor invokes a normality assumption on the approximate map.

## 4. Odd finite type-I reconstruction

For fixed `O`, let its degree-n central summands be `z_n O` for odd finite `n>=3`. Each is a matrix algebra over its arbitrary abelian center. A choice of diagonal rank `n-1` projection in each summand gives one fixed projection `e` in the bounded product, not a family whose constants must later be minimized. Both `e` and `1-e` have full carrier, `fOf` is abelian for `f=1-e`, and `E=eOe` has only even finite degrees. The unit of `E` therefore halves.

Round `T(e)` to `q`. The complement rounds with the same radius. The carrier lemma proves `q` and `1-q` are both full in `D`. Lemma 3.1 gives onto unital self-adjoint near isomorphisms on both corners. Applying Proposition 2.13 to the abelian source corner is valid after making its **new** norm parameter small; it proves `(1-q)D(1-q)` is abelian. A full abelian projection implies `D` is type I. The second corner is handled by the fixed `E` rigidity threshold, producing an exact Jordan *-isomorphism `J:E -> qDq`.

For a full projection, the corner center map `z -> zq` is an injective onto *-isomorphism onto the corner's center. Thus the restriction of `J` induces the claimed center map `beta:Z(O)->Z(D)`. Jordan *-isomorphisms and their inverses preserve positivity: every positive element is a square of a self-adjoint element. Hence they are order isomorphisms. Any order isomorphism preserves the supremum of a bounded increasing net, so `J` and `beta` are normal. In particular, the mutually orthogonal central `w_n=beta(z_n)` sum to the whole target unit. This step does not silently replace arbitrary joins with countable additivity or require measure-space coordinates.

On `w_n qDq`, the standard central homomorphism/anti-homomorphism decomposition of an onto Jordan *-isomorphism preserves finite homogeneous degree. An anti-isomorphism of a finite matrix algebra over an abelian center preserves that degree as well (matrix transpose identifies its opposite). Therefore this full corner is degree `n-1`.

Choose its `n-1` equivalent orthogonal abelian projections summing to `w_n q`. Being abelian in the corner makes them abelian in `D`, because their individual compressed algebras are unchanged. Their corner central carrier is `w_n q`; the full-corner center identification shows their carrier in `D` is `w_n`. Similarly `w_n(1-q)` is abelian with carrier `w_n`, since `1-q` was full. The standard theorem that abelian projections with the same carrier are equivalent then supplies the missing nth equivalent projection. Their sum is `w_n`, so `w_nD` is exactly homogeneous degree n. This excludes infinite ranks and wrong finite ranks without an infinite-cardinal cancellation argument.

The matrix classification over the center gives a *-isomorphism from `z_n O` to `w_nD`. Every such *-isomorphism is isometric, so taking their bounded central direct product is well-defined and onto, regardless of unbounded finite degrees or center density. One does not have to establish a uniform bound on some arbitrarily chosen Banach isomorphisms here: exact *-isomorphisms have norm one.

## 5. Primary structure cross-check

I independently checked the relevant structural assertions against [Anantharaman–Popa's author-hosted book](https://www.math.ucla.edu/~popa/Books/IIun.pdf): Proposition 4.2.1 (printed p. 61) identifies corner centers; Proposition 5.5.2 (p. 77) gives equivalence of abelian projections with the same central support; Definition 5.5.3 (p. 78) characterizes type I by a full abelian projection; Remark 5.5.6 (p. 78) states arbitrary type-I product classification and references Takesaki V.1.27; Proposition 5.5.8 (p. 79) proves halving when there are no abelian projections. The proofs of the carrier and rank-reconstruction steps above were independently reconstructed; these sources cross-check their standard structure inputs. Roydor's section 3 introduction states the onto von Neumann Jordan homomorphism/anti-homomorphism decomposition used here.

## 6. Quantifiers and edge cases

The final central decomposition has only three pieces `A,P,O`. The center correspondence is an exact *-isomorphism, so their images are a simultaneous orthogonal partition of the target unit, not separately chosen incompatible nearby projections. Lemma 3.1 then produces near isomorphisms for those fixed sources, with parameter bounded by `988 sqrt(t)`.

All infinite type-I cardinal dimensions belong to `P`, whose unit halves; all type-II and type-III parts have no abelian projections and also halve. Finite even homogeneous parts halve directly. Finite odd parts are gathered into the single `O`. Thus no infinity-cardinal list appears in any perturbation estimate.

The only deformation thresholds are those of the at most two nonzero fixed von Neumann algebras `P` and `E`. Subsequent compression and halving norm parameters are finite compositions of functions tending to zero at zero. There are finitely many required smallness inequalities (including the article's printed quantitative cutoffs, the carrier cutoff and the two fixed deformation cutoffs). Therefore one positive initial threshold can satisfy all of them before any target algebra or orientation projection is selected. No unjustified infimum over infinitely many odd degrees or moving corners occurs.

Zero `A`, `P`, or `O` summands are omitted. If `O` is nonzero, both `e` and `1-e` are nonzero on every nonzero central component because the finite degrees are at least 3; their full-carrier assertions are therefore correct. The all-zero algebra is treated separately in the manuscript. No compactness, separability, sigma-finiteness, normality of the initial approximate map, or infimum-attainment is needed.

## Findings

There are **no required mathematical corrections in this scope**. For maximum source traceability, future exposition could name precise projection-structure proposition numbers rather than only citing the two standard books, but the assertions used are standard, correct, and sufficiently checkable; this is optional and not a gap.

I have not promoted this scoped pass to approval of the complete package. All full-package, priority, license and publication gates remain with the parent reviewer/research coordinator.

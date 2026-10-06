# Independent source, domain, and type certificate

Target: 30002145 / OWR-12008-005. Reviewed head:
`ea6b192f7e3bc094b78bbc416bf61c609ffa5b2d`.
This is a verification of known rigidity, not a proof-search attempt or novelty claim.

## Source boundary

The complete [original contribution](https://publications.mfo.de/bitstream/handle/mfo/3307/OWR_2012_36.pdf?isAllowed=y&sequence=1), pp.2247-2249, concerns a published lower-semicontinuity proof. The inclusion question explains its blow-up mechanism, rejects a simplistic separated form, and describes sufficient structure already available for a second blow-up. It supplies no autonomous global-domain conjecture. The surrounding variational domain is bounded Lipschitz; the relevant inclusion is discussed for blow-ups. Whole-space/local coverage is therefore a justified contextual interpretation, not an explicit domain stated in the extracted sentence.

The [published theorem](https://www.aimspress.com/aimspress-data/mine/2020/3/PDF/mine-02-03-018.pdf), Theorem 2.10, journal pp.399-402 (PDF14-17), assumes `u in BD_loc(R^d)` and a signed scalar Radon measure. Its two symmetric-product cases are the relevant coverage. The complete theorem and proof were read, including the irrelevant elliptic third case. The proof's smoothing does not require positivity. Positivity enters the separate tangent-measure simplification, not this classification.

## Independent smooth necessity on boxes and R^d

For any smooth strain `E=P lambda`, define

`C_ijkl = P_jl lambda_ik + P_ik lambda_jl - P_jk lambda_il - P_il lambda_jk`.

Commutation of derivatives in a symmetric gradient makes every `C_ijkl` vanish. Write `H_ik=lambda_ik`.

For `P=e1 odot e2`, the entries

`C_1212=-H_12`, `C_121j=-H_1j/2`, `C_122j=H_2j/2`,
and `C_1j2k=H_jk/2`, for `j,k>=3`, force precisely

`lambda_12=lambda_1j=lambda_2j=lambda_jk=0`.

Hence on a coordinate box, and also globally on R^d by connected coordinate slices,

`lambda(x)=h1(x2)+h2(x1)+sum_{j>=3} c_j x_j`.

Put `v=(0,0,c3/2,...,cd/2)`, choose `H1'=h1`, `H2'=h2`, and integrate using the quadratic template in the PR. Its strain is exactly this coefficient times `P`; subtracting it from `u` gives zero symmetric gradient. The identity

`partial_jk u_i = partial_j E_ik + partial_k E_ij - partial_i E_jk`

then makes that difference affine with skew derivative on any connected box, or on R^d. This establishes smooth necessity, independently of finite checking dimensions and independently of assuming the displayed templates are exhaustive.

For `P=e1 odot e1`, `C_1j1k=H_jk` for all `j,k>=2`. Thus

`lambda(x)=h(x1)+sum_{j>=2} x_j p_j(x1)`.

With `H'=h`, `P_j''=p_j`, set

`u_1=H(x1)+sum x_j P_j'(x1)` and `u_j=-P_j(x1)` for `j>=2`.

Direct differentiation cancels every mixed strain and gives `E_11=lambda`. The same zero-strain argument proves completeness modulo a rigid motion. This derivation also removes the printed parallel proof's antisymmetry index typo and factor naming inconsistency: the invariant coefficient is `lambda`, not an ambiguously reused `g`.

## Nonorthogonal inputs and all degeneracies

For independent `a,b`, complete the matrix `S=[a b c3 ... cd]` using an orthonormal basis of `span{a,b}^perp`, and put `T=S^{-T}`. Define

`y=T^{-1}x=S^T x`, `w(y)=T^T u(Ty)`.

Then `Ew(y)=T^T Eu(Ty)T`; in particular `T^T a=e1`, `T^T b=e2`. Returning to x carries the quadratic transverse vector back to `v=S(0,0,v3,...,vd)`, perpendicular to a and b, and reproduces the PR formula. A transformed skew matrix stays skew under congruence. This justifies the nonorthogonal reduction that an orthogonal rotation alone would not justify.

If nonzero `a,b` are collinear, `a odot b=k(e odot e)` with a unit e and nonzero real k; absorb k into the signed scalar measure. Negative k poses no restriction. The printed condition `a != +/-b` is insufficient without normalization: `a=2e1,b=e1` belongs to the rank-one case. The PR correctly uses independent versus parallel. A literal rank-two interpretation for that collinear pair would exclude `(4x1^3 x2,-x1^4)`, whose coefficient relative to `a odot b` is `6x1^2 x2`.

If either a or b is zero, the inclusion is `Eu=0`; the derivative identity proves rigid motion separately on each connected component. In d=1, a nonzero product spans the whole scalar strain space, so arbitrary sufficiently regular one-variable maps are permitted. In d=2, the independent case has no transverse quadratic vector. All cases are accounted for.

## Signed and nonsmooth type controls

Smooth signed control: `u=(x2*x3,x1*x3,-x1*x2)` on R^3 has coefficient `2*x3`, of both signs. Its transverse strain rules out the naive two-profile form modulo rigid motion. This also demonstrates why a positive measure theorem alone would not suffice.

Nonsmooth signed control: take `H1(t)=1_{t>0}-2*1_{t>1}`, `H2=0`, and `v=0` for `a=e1,b=e2`. Then u is locally BD and

`Eu=(e1 odot e2)[delta_{x2=0}-2 delta_{x2=1}]`,

where each hyperplane measure includes Lebesgue measure in every remaining coordinate. This is a locally finite signed measure with positive and negative singular parts. It is within Theorem 2.10 but outside any hypothesis requiring the scalar measure to be positive. The smooth symbolic checks certify neither this BV case nor full BD necessity; the primary theorem supplies the stronger type statement.

## Connected nonconvex countercontrols

Let `f(t)=exp(-1/(1-t^2))` for `|t|<1` and zero otherwise. It is smooth and flat at +/-1.

Independent case: let Omega be the union of rectangles

`(-3,-1)x(-2,2)`, `(1,3)x(-2,2)`, and `(-3,3)x(1,2)`.

This is a connected, bounded Lipschitz polygon. Set `u=(0,0)` on the left and top rectangles and `u=(f(x2),0)` on the right rectangle. Definitions agree on overlaps because f is zero above 1. Everywhere in Omega, `Eu=f'(x2)(e1 odot e2)` on the right and zero elsewhere. At `(-2,0)` and `(2,0)`, the first components differ by `exp(-1)`. Every global d=2 independent template, including a rigid motion, has the same first component at equal x2. Therefore no global pair of profiles exists on this Omega.

Parallel case: use rectangles

`(-2,2)x(-3,-1)`, `(-2,2)x(1,3)`, and `(-2,-1)x(-3,3)`.

Set u=0 on the bottom and left rectangles and `u=(x2*f'(x1),-f(x1))` on the top rectangle. Again the overlaps agree smoothly. Its strain is `x2*f''(x1)(e1 odot e1)` on top and zero elsewhere. At `(0,-2)` and `(0,2)`, the second components differ by `-exp(-1)`. A single global parallel template plus rigid motion has its second component depending only on x1, giving a contradiction.

These countercontrols demonstrate a real globalization obstruction even for connected Lipschitz domains. They do not contradict a theorem on R^d or its box-local forms. Nonconvexity alone is not the obstruction; disconnected coordinate slices are. No residual domain problem was posed or solved here.

## Bibliographic and version check

The publisher verifies Mathematics in Engineering 2(3), 386-422, published 27 February 2020, DOI `10.3934/mine.2020018`. The exact arXiv v2 was submitted 5 February 2020; v1 was submitted 4 November 2019. V2 explicitly adds signed scalar measure wording and corrects the swapped `h1,h2` arguments in the rank-two proof; the published relevant content matches v2. See `primary_version_check.json` and source hashes in `download_receipts.json`.

Rindler's [2011 paper](https://arxiv.org/pdf/1008.2089v2), Propositions 4.7 and 4.9 and Example 4.8, supplies the corresponding two-dimensional LD classification; its dependence on the earlier rigidity argument was checked in Sections 4.2-4.3. The 2016 A-free measure paper supplies a singular polar constraint. The 2016 Young-measure paper supplies good/very good singular blow-ups, including Lemma 2.14. Those results concern different types or selected blow-ups and do not replace the signed arbitrary-strain classification. Their relevant statements and proof dependencies were read. Broader BD open conjectures in the survey were not treated as part of this target.

# Independent adversarial audit: fixed-type volume product

Problem **20001282**, source **AIM-CONVEX_GEOMETRY-0014**, rank **509**. Audit date: **2026-10-03**.

## Verdict

**PASS_PARTIAL.** No blocking mathematical defect was found in the frozen package. The permitted conclusions are:

1. Every centrally symmetric three-dimensional face type except the cube and octahedron has no relative local minimum of the volume product. The package correctly presents this as a consequence of source-attributed admissible-shadow machinery, with a valid local fixed-stratum argument.
2. The entire centrally symmetric hexagonal-bipyramid stratum and its dual hexagonal-prism stratum have exactly one critical affine orbit, a strict maximum with value **12**. This includes the nonproduct realizations.
3. The universal assertion that every other face type has one critical affine orbit and that it is a maximum remains **unresolved by this work**. This audit does not establish its current literature status beyond the inspected sources.

The overall result remains **partial**, with five approaches recorded. This is neither full-problem promotion nor a novelty or priority certification. The known 2017 announcement of the eight-vertex maximum must retain its credit. No source PDF, full source extraction, private research record, or repository access is required by the audit controls.

## Frozen input and independence

The audit began after the author freeze and did not edit the author files. The SHA-256 of `FROZEN_AUTHOR_MANIFEST.json` is:

`7b6c57bd4b49dea51101bf0a34058ea83f90d925e2a138c8df0b55152e72fd72`

All six payload hashes and byte lengths in that manifest matched before and after the checks. The author's checker was run only in an isolated temporary copy; its result matched the frozen `exact_results.json`. The independent checker does not import author functions. It uses separate Gauss-Jordan supporting-plane reconstruction, facet-centroid/edge volume decomposition, exact polygon clipping for polar sections, finite re-marking checks, and second-order automatic differentiation.

The author package and this audit are separate. No branch, commit, push, pull request, or other remote write was performed. This report contains authored analysis and source links, without reproducing the source documents or private records.

## 1. Original target and source hypotheses

### Original problem

The official [AIM 2010 problem list](https://aimath.org/WWN/mahlerduality/mahlerduality.pdf), printed page 3, confirms that the relevant question is **18**, attributed to G. Kuperberg. It has a general no-local-minimum assertion and a further unique-critical-affine-orbit/local-maximum question. A product-prism calculation alone cannot answer either question for all face types. The frozen package corrects this scope rather than adopting the narrower queue wording.

### Local import: checked and applicable

The [Chen–Li–Xi–Xu v1 preprint](https://arxiv.org/pdf/2605.13795v1), printed pages 4–9, was inspected, including the definitions and complete relevant hypotheses. Proposition 3.8 supplies two-sided, nondegenerate, symmetric, face-lattice-preserving shadows with affine primal volume. Lemma 4.1 assumes only an interior minimum along such a sufficiently short shadow; it does **not** require a global minimizer over a bounded-vertex class. Lemma 5.2 classifies polytopes for which both the body and its polar admit only trivial admissible shadows. The dimension bound is Lemma 5.1.

The global-minimizer assumption occurs in the separate Lemma 4.2. The package does not import that assumption incorrectly. It replaces that global step with a valid local argument and polarity. The [arXiv v1 record](https://arxiv.org/abs/2605.13795v1) dates submission to 13 May 2026. The inspected PDF is dated 14 May 2026. The work is a preprint, and the audit does not promote it to a journal publication.

### Classical analytic input

[Meyer–Reisner, arXiv v2](https://arxiv.org/pdf/math/0606305v2), Theorem 1 and Proposition 7, was checked in the complete source; the proposition was also visually inspected. Theorem 1 gives convexity of inverse polar volume at the Santaló point for a nondegenerate shadow. Proposition 7 assumes both primal volume and inverse polar volume are affine and gives a time-affine shear representation. It is not a general assertion that any constant-product family is affine-equivalent. Here the needed two affine quantities are established first. Origin symmetry puts the Santaló point at zero throughout, so the package uses the correct polar.

## 2. General no-minimum proof: adversarial checks

### Face-type preservation

For a nonparallel facet, admissible scalar speeds restrict to an affine function on its plane, so its vertices remain coplanar under a small affine perturbation. For a parallel facet the displacement stays in its original plane; imposing no scalar-affinity condition there is correct. Strict supporting inequalities against vertices outside each facet survive sufficiently small perturbations, as do the strict convexity and vertex order of each facet polygon. The resulting deformation is two-sided and remains in the given symmetric face lattice. This addresses the principal risk that a vertex motion might merely split a nonsimplicial facet and leave the permitted stratum.

Triangulating the fixed boundary yields affine volume: in each determinant, every term with two displacement columns is zero because those columns have the same direction. Signs stay fixed on a sufficiently small interval. No global compactness or minimizer-existence assumption enters this step.

### Interior ratio argument and rigidity

Write `a(t)=|K_t|>0` and `b(t)=|K_t°|^(-1)>0`. A relative local minimum of `a/b` implies, on a short symmetric interval,

`h(t)=b(t)-[b(0)/a(0)]a(t) <= 0`, with `h(0)=0`.

Since `h` is convex, for any `x<0<y`, the convexity inequality at zero forces both `h(x)` and `h(y)` to be zero. Thus `h` vanishes throughout the interval and `b` is affine. This is the required equality regime, not an unsupported strict-convexity claim.

The resulting affine maps have the form `A_t(x)=x+t(w·x+beta)theta`. Their centers are `t beta theta`; origin symmetry forces `beta=0`. Both the tracked vertices and their affine images approach the same distinct initial vertices. Disjoint small neighborhoods therefore identify labels, giving exactly `alpha_i=w·x_i`. The trivial-speed space has dimension three because the vertices span three-space. There is no hidden continuously varying vertex permutation.

### Polarity and the relative topology

If a small admissible shadow starts at `K°`, its polar remains origin symmetric, converges to `K`, and has exactly the original face lattice because polarity reverses the preserved lattice. Its product equals the product of the shadow body. A local minimum of `K` therefore forces trivial shadows for `K°` too. The dual path does not have to be a shadow itself. Continuity of polarity for full-dimensional bodies containing the origin in their interiors is sufficient. This justifies the exact fixed-stratum quantifier needed for the original problem.

### Counting and exceptional types

The odd-speed space has dimension `V/2`; an opposite facet pair with `m` vertices contributes at most `m-3` restrictions unless it is parallel to the direction. Constraint dependencies can only improve the lower bound. Using `sum m=2E` and Euler gives

`dim A_theta >= (F-V)/2 + 2 + C_theta`.

Checking both polars yields `|F-V|<=2`, with both counts even. The three remaining cases are eliminated or classified correctly:

- If `V=F+2`, a vertex of degree at least four produces a nonsimplicial dual facet. A direction parallel to that facet gives a fourth admissible dimension. Otherwise the body is simple; Euler forces `(V,F)=(8,6)`. Three pairs of opposite supporting planes define a parallelepiped.
- If `F=V+2`, polarity gives an affine octahedron.
- If `F=V`, a facet with at least five vertices, or an edge shared by two quadrilateral facets, gives `C_theta>=2`. The latter counts two distinct opposite facet pairs, since adjacent facets cannot be opposite. With neither event possible, Euler gives four triangular facets. Every quadrilateral edge borders a triangle, so `4q<=12`; symmetry gives even `q<=2`. Full dimension forces `V=F=6`, impossible because six centrally symmetric vertices are an affine octahedron with eight facets.

The count works on nonsmooth or singular general realization strata because the argument only needs the constructed admissible paths. It does not presume a smooth coordinate chart for every face type. The resulting general no-minimum conclusion passes.

## 3. Full bipyramid chart and the finite affine quotient

### Coverage and antipodal marking

In the hexagonal-bipyramid lattice the two degree-six vertices are intrinsically distinguished. Central inversion must exchange them. On the equatorial six-cycle it must act by the three-step rotation: a reflection either fixes a vertex or exchanges the endpoints of an edge, both impossible for inversion in a full-dimensional origin-symmetric polytope. Thus the cycle can indeed be marked

`u,w,v,-u,-w,-v`, with poles `+a,-a`.

The facet `conv(a,v,-u)` has a supporting plane excluding zero, so `a,u,v` are linearly independent. Mapping `u,v,a` to the standard basis removes all linear freedom in this marked realization. The determinants of consecutive facet cones at the positive pole are `q,p,1,q,p,1`. Coherent boundary orientation makes their signs agree with the third one, proving `p,q>0`; this does not assume that the equator is planar.

### Exact open chamber

Solving the three displayed facet equations for each pole gives exactly the normals in the frozen proof. The strict inequalities on the remaining vertices reduce to

`|r| < p+q-1` and `|p-q|+|r| < 1`, with `p,q>0`.

For example, the facet through `e1,w,sigma e3` requires `|1-p-sigma r|<q`; the corresponding facet through `w,e2,sigma e3` requires `|1-q-sigma r|<p`; the facet through `e2,-e1,sigma e3` requires `|-p+q+sigma r|<1`. Combining both signs yields the stated chamber. The listed twelve supported triangles form the required bipyramid boundary. Conversely, the prescribed marked incidence enforces these strict inequalities. The chamber is therefore necessary and sufficient for the marked type.

There are only 24 possible choices from the six starting equatorial vertices, two cyclic directions, and two poles. Every change is a rational invertible re-normalization with a nonzero determinant on the chamber. Hence this is a complete three-dimensional marked chart; the unmarked affine moduli are its finite quotient. The independent controls checked all 24 markings at each of 175 realizations. A finite marking quotient introduces no extra stationary orbit. At the symmetric maximum, nondegeneracy means the Hessian on the marked lift, which is the appropriate interpretation even if the quotient has finite isotropy.

### Transverse parameter and dual prisms

When `r!=0`, the equatorial vectors `e1,e2,w` span three-space. Affine equivalences preserve the distinguished pole pair and equatorial vertex set, so they cannot make that equator planar. This rules out removing `r` by relabeling or an affine coordinate change. The missing transverse parameter in a planar-product treatment is genuine.

Polarity sends the full stratum to the full dual prism stratum. In these finite-vertex/facet coordinates it is a smooth local invertible operation: supporting normals are obtained from nonsingular linear systems and the inverse operation is polarity again. Thus it preserves criticality as well as product and local extrema. It is unnecessary, and false, to assume that every combinatorial prism is affinely a product.

## 4. Volumes, stationary points, and degenerations

The twelve signed facet-cone determinants give `|B|=2(p+q+1)/3`; their lack of `r` dependence is correct. In the polar, each height section is a square clipped by the strip `|px+qy+rz|<=1`. The strict chamber ensures that at every height only the two same-sign corners are removed and the mixed-sign corners remain. Integrating the two quadratic removed areas yields

`|B°|=8-2[(p+q-1)^2+r^2/3]/(pq)`.

The factor `1/3` in the transverse term and the total three-dimensional product normalization are correct. Separate exact clipping and Simpson integration of the section areas matched the polar hull volumes in all 175 independent cases. Since the section area is quadratic on this chamber, this integration is exact, not numerical quadrature evidence. For a planar base and interval of height parameter `a`, the product is `4P(H)/3`, independently of `a`.

With `s=p+q`, `d=p-q`, the open domain is `s>1+|r|`, `|d|+|r|<1`. Its denominator `s^2-d^2` is strictly positive. Direct differentiation independently confirms:

- `P_r=-8(s+1)r/(9pq)`, forcing `r=0` at any critical point.
- At `r=0`, `P_d=-32(s+1)(s-1)^2 d/[3(s^2-d^2)^2]`, forcing `d=0`.
- On `d=r=0`, `P_s=16(2-s)/(3s^3)`, forcing `s=2`.

All prefactors asserted nonzero are indeed nonzero in the open domain. This eliminates every stationary point except `(p,q,r)=(1,1,0)`, rather than only finding a candidate. The exact Hessian in `(s,d,r)` is `diag(-2/3,-2,-8/3)`. Mixed terms vanish, and all eigenvalues are negative. Both the derivative elimination and Hessian therefore support full-stratum strict maximality.

The global upper bound also passes: first remove `r^2`, then maximize `pq` at fixed `s`, then use `8+4/s-4/s^2=9-(s-2)^2/s^2`. Equality requires precisely the same point. At any other or critical point, a sufficiently small increase of `|r|` stays inside the chamber and lowers the product, independently excluding local minima for these two strata.

The lower-bound subtraction and its two-case estimate in the frozen proof are algebraically correct and strict in the open chamber. The explicit path `p=q=1`, `0<=r<1` already attains every value in `(32/3,12]`. At `r=1`, the hull has six quadrilateral facets and is an affine cube, so this endpoint cannot count as an interior minimum of the bipyramid stratum. Other equality walls likewise lose the marked bipyramid incidence. Unbounded chart directions do not create an unexamined finite critical point. No boundary point is promoted into the open domain.

## 5. Five approaches and claim discipline

The five recorded routes are substantive and have the stated limitations:

1. The global Mahler lower bound alone does not rule out higher constrained local minima. The scalar polynomial counterexample has the claimed stationary points and values.
2. The planar-product route is correct but covers only a proper subset of the full prism stratum.
3. The transverse three-parameter route closes that coverage gap for the two specified dual types.
4. An isolated antipodal-pair shadow works for simplicial types with more than six vertices; a basis can be fixed while a further pair moves. The mixed-face obstruction is real.
5. Coordinated admissible speeds remove that obstruction for the no-minimum assertion. They do not prove the universal stationary-point classification.

In particular, neither the absence of minima nor the existence of a decreasing direction near a stationary point implies uniqueness of stationary points; saddles remain a logical possibility for the other types. No unpublished universal-critical claim is hidden in the conclusion.

The [2017 BIRS lecture](https://archive.birs.ca/files/2017/17w5074/files/Alexander_Banff.pdf), PDF pages 33–35 and 65–70, independently confirms the prior announcement of the symmetric eight-vertex maximum, the regular-hexagon double cone, and the value 12. The frozen source gate correctly avoids silently turning this conference evidence into a verified theorem in a particular journal article. No priority conclusion follows from a bounded negative literature search. Repository duplicate-search claims were not re-certified as exhaustive by this mathematical audit.

## 6. Reproducible controls and limitations

Run:

```sh
python3 audit_controls.py /path/to/frozen/public
```

With the original adjacent directory layout, the argument may be omitted. Python 3 standard library only; no network, symbolic package, downloaded data, or source PDF is required. The expected author-manifest digest is pinned in the checker. It checks all author payload hashes before and after replay and independent work.

The checker also passed from an unrelated working directory after both the checker and the author package were copied into a temporary layout. The saved `audit_controls.json` records:

- 81 author rational cases replayed in a temporary copy
- 175 independent primal hulls and 175 polar hulls
- 175 independent exact clipped-section integrations
- 4,200 re-marking/affine-equivalence checks
- 179 positive and negative marked-chamber controls, including failed positivity
- 140 nonzero-transverse controls that reject the planar-only formula
- 10 positive/negative-determinant affine-polar transport checks, including rejection of the wrong polar transform
- 4 boundary-incidence controls
- exact critical-point gradient and Hessian, plus a noncritical planar control
- product-height normalization checks

The checker distinguishes the **marked** incidence outside the chamber. Outside it, the same unlabelled bipyramid type may sometimes reappear with different distinguished poles; facet counts alone would be an invalid negative control. The code does not make that mistake.

Finite checks do not prove universal coverage, analytic shadow rigidity, or literature completeness. Those responsibilities are separated above. No formal proof assistant was run, and this audit does not certify all results in the cited preprint. The elementary local derivation and count were checked directly; only the clearly identified classical analytic result is imported without re-proving its full theorem.

## Final disposition

**PASS_PARTIAL; no blocking correction requested.** Preserve the frozen mathematics, source attributions, preprint qualification, five-approach record, and explicit unresolved universal-critical assertion. The audit report, portable checker, saved result, and audit manifest may accompany the author package. Full solution status or priority claims are not authorized by this audit.

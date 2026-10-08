# Variationally minimizing maps on ideal hyperbolic complexes

## Audit derivative notice

This is an explicitly corrected derivative of the frozen report. The frozen original is unchanged. This audit does not spend another approach: the original five-approach limit and unresolved full target remain. The changes state the trace convention and make the admissibility assumption in the uniqueness argument explicit; the compatible-isometry case retains its energy conclusion but its map-identification conclusion is conditional. See CORRECTION_CONTEXT.md and the accompanying patch.

## Status and scope

**Partial results and obstruction checks only. No proof or counterexample of the full conjecture is claimed.** There is no novelty claim. These notes concern equality of the two variational minima; existence and regularity results already in the literature are credited rather than reclassified as a solution.

Let X be a finite connected two-dimensional complex obtained by gluing triangle sides, with connected vertex links and at least two incident face sides at every edge. Remove its vertex set S. Give M=X\S two complete ideal hyperbolic metrics σ and τ. Every face is an ideal hyperbolic triangle, and side identifications are isometries. All maps below preserve each specified face and edge, not merely the collection of cells.

Write Y for the source's finite-energy simplicial Sobolev class and D for its facewise-diffeomorphic subclass. Face traces on a common edge must match the prescribed edge map in the Sobolev trace sense; independent changes to measure-zero edge values do not define new admissible competitors. This trace convention does not by itself identify different side incidences of a self-glued face. The full target and its allowed complexes, including source-permitted self-identifications, are retained. Use

\[
 E(f)=\sum_T\int_T |df|_{\sigma,\tau}^{2}\,dA_\sigma.
\]

There is no factor 1/2. Equality means equality of the continuous representatives, not equality of arbitrary representatives altered on null sets.

The OWR source states the conjecture using D. The full paper introduces the weak closure \(\overline D\), constructs its minimizer v, and proves that v is a diffeomorphism on each **open** face. Its unrestricted minimizer u has additional edge regularity. Thus weak closure, interior diffeomorphism, and smooth invertibility on the closed face must not be conflated. The exact target is u=v for every permitted X,σ,τ; showing u is facewise diffeomorphic is the source's equivalent formulation. [1, pp. 2520–2522; 2, Definition 15, Theorems 27 and 31, Conjecture 28]

We use the source's constructed regular maps, including properness and degree one. The distinctions between interior face, nonpunctured edge, and deleted vertex remain in force.

## 1. Strict convexity identifies a missing energy equality

### Lemma 1 (uniqueness conditional on admissible interpolation)
Suppose f and g are continuous finite-energy minimizers in Y, C² in every open face. Suppose f is analytic there and its restriction to every open face is proper of degree one. Assume in addition that the pointwise geodesic interpolation in the chosen abstract target triangles gives a continuous admissible map in Y for every interpolation parameter. Then f=g. A sufficient condition is that both maps preserve the same specified side incidence in each face representative and their common Sobolev traces are compatible with the gluing. When a face has self-identified sides, preservation of a quotient edge alone must not be substituted for this condition.

**Proof.** On each face, join f(z) to g(z) by the geodesic inside the target ideal triangle and denote the interpolation by f_t(z). Triangles and their sides are geodesically convex. Under the stated interpolation hypothesis, these facewise geodesics glue to an admissible map f_t. Under the sufficient side-incidence condition, both endpoints on each source side lie in the corresponding same target side, and the side isometries identify the resulting edge geodesics. Convexity on one abstract face, by itself, does not prove this compatibility when sides are self-identified. Convexity of hyperbolic Dirichlet energy gives

\[
 E(f_t)\le (1-t)E(f)+tE(g)=m.
\]

Minimality gives the reverse inequality, so the energy is constant in t.

Here is the strictness argument, localized to avoid any differentiation under an integral over a cusp. In a relatively compact open patch of a face, put V=∂_t f_t. The second variation density of the unhalved energy along a pointwise geodesic variation is

\[
 2\sum_{i=1}^{2}\left(|\nabla_iV|^2+
 |V|^2|d f_t(e_i)|^2-\langle V,d f_t(e_i)\rangle^2\right).
\]

The curvature is −1, and every summand is nonnegative. If df has rank two at z and f(z)≠g(z), the curvature terms have positive sum at t=0. They remain positive on a smaller patch and a short t-interval. Consequently the energy on that patch is strictly convex on that interval. The energy on its complement is convex, by the same pointwise geodesic convexity inequality integrated over the complement. Their sum cannot be constant. Therefore f=g at every rank-two point of f.

A smooth proper degree-one map onto a two-dimensional face has a rank-two point: otherwise Sard's theorem contradicts surjectivity. The analytic Jacobian is consequently not identically zero; its nonzero set is dense in the connected open face. Continuity gives f=g on that face and then on its sides. Do this on every face. ∎

**Consequence.** Put m=E(u) and n=E(v). Once n=m is proved and the interpolation hypothesis for u and v is verified, Lemma 1 identifies u and v. A sequence d_k∈D with E(d_k)→m would suffice for the energy equality n=m, since m≤n≤E(d_k); equality of the maps still uses the interpolation hypothesis. But weak convergence alone supplies only lower semicontinuity, not such an energy-recovery sequence. Constructing that sequence for a folded u is an unproved extra assertion. Convexity solves uniqueness after equality of energies and admissibility of interpolation have been established; it does not establish either missing requirement merely from quotient-cell preservation.

The proof above assumes the quoted properness/degree and regularity hypotheses and the explicit interpolation hypothesis. It is not a general uniqueness claim for arbitrary nonsmooth, nonproper maps or other target curvatures.

## 2. What target variations really test

Let v minimize over the diffeomorphic class or its weak closure. In a compact neighborhood of one edge, let its common edge trace be h(s). Assume temporarily that its face restrictions are C² up to that edge. Let ν_j be the outward conormal in incident face j and write

\[
 B(s)=\sum_j\langle\partial_{\nu_j}v,\mathbf t(h(s))\rangle_\tau,
\]

where s is source arclength and t is target unit tangent, chosen consistently. The first variation formula and facewise harmonicity show that postcomposition by a compactly supported, cell-preserving target flow with edge velocity ζ(t) gives

\[
 \int_e B(s)\,\zeta(h(s))\,ds=0. \tag{2.1}
\]

Postcomposition preserves the diffeomorphic class. For the weak-closure case, use the source topology and a compactly supported smooth flow with bounded derivative and inverse derivative in the finite local charts. Local Sobolev compactness gives strong convergence of the maps and weak convergence of their derivatives after a subsequence; the chain rule then identifies the weak limit of the compositions. The maps are unchanged outside the target support. This supplies the required weak-closure stability; it is not a general assertion that every nonlinear operation is weakly continuous. Properness makes the affected source region compact. Smooth tangential edge vector fields extend on each adjacent page to a compatible cell-preserving flow; support is kept away from the vertices.

### Lemma 2 (conditional recovery of full balance)
Under the regularity just specified, if h is a C¹ diffeomorphism of edges with positive derivative, then B=0 distributionally.

**Proof.** Given a compactly supported smooth test η(s), set ζ=η∘h^{-1}. This is C¹ and compactly supported. Approximate it uniformly by compactly supported smooth functions in a fixed compact interval. Since B is locally integrable, (2.1) passes to the limit and yields ∫Bη=0. ∎

This does not prove that v satisfies those hypotheses. In particular, if h is constant on an interval I, every test ζ∘h is constant on I. Such tests cannot distinguish fluxes on I having equal integral. One cannot infer all domain-edge tests from (2.1) without a further argument. Nor may the stronger edge regularity proved for u be transferred to v before identifying the maps. Even after obtaining local balance, a global noncompact comparison must justify its limiting step.

## 3. Edge orientation and a local obstruction to a shortcut

Use upper-half-plane target coordinates (A,B), with metric (dA²+dB²)/B², and a conformal domain coordinate (x,t) in a compact page neighborhood of an edge x=0. The target edge is A=0; the page lies in A>0. A smooth harmonic map satisfies

\[
 \Delta A-\frac{2}{B}\nabla B\cdot\nabla A=0.
\]

For the degree-one face map, A is positive in the page interior: the strong maximum principle rules out an interior zero unless A is identically zero, which is incompatible with degree one. Its coefficients are bounded on a sufficiently small compact neighborhood. The Hopf boundary lemma therefore gives A_x(0,t)>0. Since A(0,t)=0 and B(0,t)=h(t),

\[
 \det D(A,B)(0,t)=A_x(0,t)h'(t). \tag{3.1}
\]

Positive metric factors do not change this sign. Thus an interval where h'<0 produces an orientation-reversing collar. The balance condition instead involves the sum of B_x over the pages. It is not a sign condition on h'.

The following exact flat example demonstrates the gap in trying to obtain that sign purely from local harmonicity, page preservation and balance. It is deliberately **not** a counterexample to the ideal hyperbolic problem.

Take N Euclidean half-disks, all glued along their straight diameter x=0, and a book of N full Euclidean half-planes as target. On every page use

\[
 F(x,t)=(x,\ t^3-t-3tx^2). \tag{3.2}
\]

Both components are harmonic. The common trace is (0,t³−t), and the tangential component's inward normal derivative is −6tx, hence zero on the edge. So the balance condition holds for any N. The first component is positive for x>0, preserving the page. But

\[
 \det DF=3t^2-1-3x^2,
\]

which is negative near (0,0) and positive, for example, at (x,t)=(1/4,1). Use half-disks of radius 2. The map folds despite being analytic and balanced.

It even minimizes the Euclidean Dirichlet energy among page-preserving competitors with its own data on the outer semicircles. Write a competitor as F+W pagewise. Integration by parts makes the energy cross term zero: W vanishes on each outer semicircle; the normal target component of W vanishes on the glued edge; the tangential normal derivative of F is zero there. Hence

\[
 E(F+W)-E(F)=\sum_j\int |DW_j|^2\ge0.
\]

The argument first applies to smooth competitors and then by Sobolev approximation. The outer boundary data, compact book domain and flat target differ from the conjecture. This example invalidates the proposed local implication, not the global conjecture.

## 4. Area calibration: an exact restricted result

Let f be a smooth proper degree-one face map with finite energy, mapping open face to open face and boundary sides to their specified sides. Orient each face separately, with the same choice in source and target. In oriented orthonormal frames write

\[
 Df=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad
 e(f)=a^2+b^2+c^2+d^2,\qquad J_f=ad-bc.
\]

The exact identity is

\[
 e(f)-2J_f=(a-d)^2+(b+c)^2\ge0. \tag{4.1}
\]

The degree formula gives ∫_T J_f dA=π, because an ideal hyperbolic triangle has area π. On this noncompact domain the formula follows first for compactly supported target area forms and then by exhaustion; |J_f|≤e(f)/2 supplies integrable domination. Thus for q faces,

\[
 E(f)=2\pi q+\sum_T\int_T\big((a-d)^2+(b+c)^2\big)\,dA. \tag{4.2}
\]

The expression in frames measures the anti-conformal part and is independent of the compatible oriented frame choices.

### Proposition 3 (compatible facewise isometry case)
If there is a cell-preserving map F from (M,σ) to (M,τ) that is an isometry on every face and belongs to D, then E(u)=E(v)=E(F)=2πq for the source's regular degree-one minimizers. If the interpolations comparing u to v and u to F satisfy Lemma 1's admissibility hypothesis, then u=v=F.

**Proof.** F has energy 2πq and belongs to D. Equation (4.2) applied to u and v bounds their energy below by 2πq, while minimality bounds it above by E(F). Both energies equal E(F). Under the extra interpolation hypotheses, Lemma 1 applies first to u and v and then to u and F, giving the conditional map identification. ∎

In particular the energy conclusion applies to identical metrics, with F the identity; identification with that particular map still uses the stated interpolation hypothesis. This is an explicitly restricted result; existence of such an F for arbitrary shear parameters is false. For general metrics the nonnegative anti-conformal defect in (4.2) need not vanish. Comparing its infimum in two different map classes is just the missing variational problem again.

## 5. Finite-energy cusps can contain arbitrarily remote folds

A separate possible shortcut would be to argue that finite energy, properness and degree one force a cusp map to become injective. They do not, even in an actual hyperbolic cusp sector.

Let C={0<x<w, y≥Y} with metric (dx²+dy²)/y², with Y>0. Set

\[
 q(y)=y+2\sin^2(y-Y),\qquad G(x,y)=(x,q(y)). \tag{5.1}
\]

We have q(Y)=Y, q'(Y)=1, q≥y and q'∈[−1,3]. Extend G by the identity immediately below y=Y. The seam is C¹ and the map is W^{1,2}; smoothness at that seam is not asserted or needed. It is proper and preserves both vertical sides. The homotopy q_r(y)=y+2r sin²(y−Y), 0≤r≤1, is uniformly proper, fixes y=Y and joins G to the identity. Consequently G has relative degree one.

Conformal invariance in the source gives the exact energy integral on the sector:

\[
 E(G;C)=w\int_Y^\infty \frac{1+q'(y)^2}{q(y)^2}\,dy
 \le 10w\int_Y^\infty y^{-2}\,dy=\frac{10w}{Y}. \tag{5.2}
\]

At y−Y=3π/4+kπ, q'=−1. At y−Y=π/4+kπ, q'=3. Thus folds occur at arbitrarily large height although every tail has arbitrarily small energy.

The same formula can be placed in compatible horocyclic sectors around a puncture and glued to the identity on the compact remainder, whenever such common-height cusp charts are chosen. The sector construction itself already refutes the analytic implication being tested. It does **not** produce a minimizing or harmonic map: in these coordinates the second harmonic-map equation would require

\[
 q''+\frac{1-q'^2}{q}=0,
\]

which fails, for instance where y−Y=π/4. Hence it is not a counterexample to the conjecture. A valid cusp argument must combine harmonicity with new uniform orientation or trace control, rather than rely on small tail energy alone.

## Remaining gap and verification boundary

None of the five mechanisms establishes E(u)=E(v), excludes all edge backtracking for u, or derives unconstrained stationarity for v without extra hypotheses. The full conjecture remains unresolved by this work. The special isometry energy equality, its conditional map identification, and the obstruction examples are not substituted for it. For complexes with self-identified sides, the admissibility of the facewise geodesic interpolation is a separate condition in the uniqueness reduction, not an automatic consequence of preservation of quotient cells.

The companion verifier checks finite polynomial identities, selected exact rational values and constants used above. It does not verify PDE existence, the Hopf lemma, strict convexity, the degree formula, source theorems, or the original conjecture. Normal and optimized Python runs are robustness checks, not independent mathematical proofs. The accompanying independent audit checks the corrected scope and additional exact identities; it does not certify the analytic source theorems or solve the original conjecture.

## Sources and literature boundary

1. B. Freidin (joint work with V. Gras Andreu), “Harmonic maps between ideal hyperbolic complexes,” in *New Trends in Teichmüller Theory and Mapping Class Groups*, Oberwolfach Report 40/2018, pp. 2520–2522. [Official report](https://ems.press/content/serial-article-files/46762), [DOI](https://doi.org/10.4171/owr/2018/40).
2. B. Freidin and V. Gras Andreu, *Harmonic maps between ideal 2-dimensional simplicial complexes*, [arXiv:1810.06714v1](https://arxiv.org/abs/1810.06714), published in *Geometriae Dedicata* 208 (2020), 129–155, [DOI](https://doi.org/10.1007/s10711-020-00514-w). The inspected proof version is the 27-page arXiv PDF; closure notation was visually checked, not inferred from plain-text extraction.
3. B. Freidin and V. Gras Andreu, *Harmonic maps between 2-dimensional simplicial complexes 2*, [arXiv:2110.13043v1](https://arxiv.org/abs/2110.13043). Its separate existence/regularity assertions do not identify the two minima in the inspected preprint. The published article is *Harmonic maps between 2-dimensional simplicial complexes: conformal and singular metrics*, *Geometriae Dedicata* 218, 22 (2024), [publisher page](https://link.springer.com/article/10.1007/s10711-023-00871-2). The publisher exposed a subscription preview; the full published text was not inspected.
4. B. Freidin, *Balanced homogeneous harmonic maps between cones*, *Pacific Journal of Mathematics* 331(2) (2024), 283–329, [official PDF](https://msp.org/pjm/2024/331-2/pjm-v331-n2-p04-p.pdf). The checked scope concerns homogeneous cone maps and their degrees, not a stated resolution of the global equality above.

Bounded current-source searches were performed on 2026-10-08. No full resolution was verified in the inspected material. This is neither a comprehensive literature survey nor a certification of openness or priority. Download hashes and inspection locations are in SOURCE_MANIFEST.json; source PDFs and extracted text are excluded from this packet.

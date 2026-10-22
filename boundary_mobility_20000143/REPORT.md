# Mobility counts on two fourfolds: audited partial refinements

Date: 2026-10-21. Problem identifier 20000143; queue rank 1858.

## Status and scope

**UNSOLVED broad question; accepted partial surface refinements only.** The original target asks for improved growth estimates on Gr(2,4) and P²×P², not specifically the generated boundary-count theorem. The original AIM endpoint failed live retrieval; source wording/identity remain corpus-recovered, not live-recertified. No novelty certification is made. The known geometric mechanisms below belong to the published literature, principally Lehmann's Example 1.10 and its cited Schubert-rigidity results. Our work audits the generated finite formulas, gives explicit all-m refinements of its subsequence bounds, and establishes two small exact refinements. No copied source document or private coordination material is included here.

### Conventions

Everything is over C. Classes are integral numerical classes of effective algebraic **surfaces**, unless stated otherwise. An effective cycle is a finite sum of integral surfaces with positive integer multiplicities. Its support, not its scheme-theoretic multiplicity, contains points. Ordinary mc(γ) is the maximal number q such that a family of effective cycles of class γ has dominant q-point incidence map to X^q. Equivalently general ordered q-tuples can be covered. This does not restrict to integral representatives or one linear system, and is not parameter-space dimension. The zero cycle has mc(0)=0. Rational coefficients require integral multiples. No positive top-dimensional class is included: its support already contains arbitrarily many points.

For X=P²_x×P²_y, let A and H be the respective hyperplane pullbacks. A³=H³=0 and A²H²=1. An effective surface has class aH²+bAH+cA² with nonnegative integral coefficients. H² is a first-factor plane over y, A² the opposite plane. For Q=Gr(2,4) in its Plücker embedding, P²=σ₂+σ₁,₁; each Schubert generator is a plane of degree one. Put h_Q(d)=(d+1)(d+2)²(d+3)/12.

For surfaces on a fourfold, raw growth exponent ρ, cycle Iitaka dimension κ, and mobility volume are distinct: κ=2ρ and mob(α)=24 limsup_m mc(mα)/m². Published baseline: raw exponent 1 on the product's H²,A² face and AH ray, 3/2 on either open mixed face, 2 on big surfaces; on Q the two boundary rays have exponent 1 and big classes exponent 2. We do not claim these exponents as new.

## Results established in this audit

1. mc(aH²+cA²)=a+c, and mc(bAH)=2b, for all nonnegative integral coefficients.
2. The finite strip mc(aH²+AH)=a+2 holds for all integers a≥0; exchange factors for its symmetric version.
3. If a,b>0 and α=aH²+bAH, let s=floor(sqrt(ma)) and r=floor(mb/(2s)). Whenever r≥1,

   mc(mα) ≥ (r+1) binom(s+2,2)−2 + (ma−s²) + 2(mb−2rs).

   Therefore mc(mα) ≥ (b√a/4)m^(3/2)−O_{a,b}(m) for all sufficiently large m, and in particular **liminf** mc(mα)/m^(3/2)≥b√a/4. The generated attempt only states a limsup along a square subsequence. This is a quantifier improvement of that attempt, not a claim of a new published asymptotic theorem.
4. mc(mσ₂)=mc(mσ₁,₁)=m, using published multirigidity. In addition mc(P²)=4.
5. For β=uσ₂+vσ₁,₁ with positive integral u,v, t=min(u,v), and d=floor(sqrt(mt)),

   mc(mβ)≥h_Q(d)−2+m(u+v)−2d².

   Thus liminf mc(mβ)/m²≥t²/12 and mob(β)≥2t². Again this supplies an all-m version of the generated lower bound, not an equality or sharpness claim.

Each lower bound can be replaced by its maximum with an elementary reducible-cycle bound: ma+2mb on a mixed product face, and m(u+v) on Q.

## Approach 1: nonmixed product face and multiplicity accounting

Let V be an integral surface and resolve it. The pullbacks of A,H are nef, and the three surface coefficients are A², AH, H², hence nonnegative. If the AH coefficient vanishes, write A²=u, H²=v, AH=0. Hodge index gives uv≤0, so uv=0. They cannot both vanish because A+H is ample on V. Suppose u>0. The orthogonal complement to the big nef A is negative definite; H is orthogonal to A and has square zero, so H is numerically zero. Its associated projection is constant: a nonconstant image has a curve on V mapping nontrivially, on which H has positive degree. Thus V is a first-factor plane, necessarily primitive. The other case gives the opposite plane.

Nonnegativity forces every component of a cycle of class aH²+cA² onto this face. Counting multiplicities gives a+c planes at most. A general tuple has distinct coordinates in both factors; each plane contains at most one tuple member. Conversely assign a points to first-factor fibers and c to opposite fibers. This proves equality. The factor-plane classification is already in Lehmann Example 1.10; we give its finite-count consequence, not a newly discovered mechanism.

## Approach 2: product components and an exact thin mixed strip

If [V]=wAH is integral, both projections have dimension one: their dimensions cannot be two because the corresponding squared hyperplane intersection vanishes, nor zero because AH>0. Thus V=C×D for integral plane curves of degrees d,e, and w=de. A plane degree-d curve contains at most R(d)=binom(d+2,2)−1=d(d+3)/2 general points. Consequently C×D contains at most min(R(d),R(e)) members of a general point-pair tuple. If d≤e, R(d)≤2de because d+3≤4e. For a cycle Σμ_i(C_i×D_i), assign each point to one containing component. Then total capacity≤Σ2d_ie_i≤Σ2μ_i d_ie_i=2b. Pairing 2b general point-pairs and using the product of their two coordinate lines realizes equality. This verifies the generated formula and explicitly retains multiplicities.

For the strip aH²+AH, coefficient nonnegativity shows exactly one integral component has positive AH coefficient, equal to one and multiplicity one. Call it V, with [V]=uH²+AH. Its y-image is an integral curve C: the H² intersection is zero, and positive AH rules out a point. If e=deg C and k is the positive degree in P²_x of the generic fiber curve over C, intersection with A and H gives 1=ke. Hence e=k=1 and C is a line. V contains at most two members of a general tuple, by their y-coordinates. Every other component is a first-factor plane, with total multiplicity a−u. Capacity is at most a−u+2≤a+2. The sum of a fibers and a line product realizes a+2. This does not claim novelty beyond a simple finite deduction from the projection geometry.

General-position details: only finitely many degrees and partitions arise for a fixed class. Choose the tuple in the intersection of the corresponding nonempty open sets where each subset imposes independent conditions on each relevant plane-curve linear system. The argument is not assuming independently general coordinates conditional on a subsequently chosen component.

## Interpolation lemma used in approaches 3 and 5

On W=P¹×P² write h(R,S)=(R+1)f(S), f(S)=binom(S+2,2), with R,S≥1. There exist two sections of O(R,S) through h(R,S)−2 general points with no common divisor. Likewise O_Q(d), d≥1, has a coprime two-section pencil through h_Q(d)−2 general points.

Proof of the first statement: general points impose independent linear conditions, leaving two sections. If a fixed effective divisor has bidegree (i,j), and contains l of the imposed points, then l≤h(i,j)−1. The residual system retains two independent sections through the other points, so h(R,S)−2−l≤h(R−i,S−j)−2. A contradiction follows from

h(i,j)+h(R−i,S−j)≤h(R,S)

for every nontrivial proper split. For j=0 the difference is i f(S)−i−1≥0 (i≥1); j=S follows by interchanging summands. For 0<j<S set U=f(S)−f(j), V=f(S)−f(S−j). The difference equals (i+1)U+(R−i+1)V−f(S), which is ≥U+V+min(U,V)−f(S), since R≥1. If j≤S−j this is f(S)−f(j)+2(f(S)−f(S−j))−f(S)≥0 because 2(f(S)−f(S−j))=j(2S−j+3)≥f(j). The other ordering is symmetric. A trivial residual degree has only one section and cannot occur. The simultaneous general-point independence used above involves finitely many splits and subsets.

For Q, Pic(Q)=ZP. A fixed part has degree 1≤e≤d−1; the same argument uses h_Q(e)+h_Q(d−e)≤h_Q(d). Discrete convexity makes the left side largest at e=1 or d−1, and h_Q(d)−h_Q(d−1)≥h_Q(1)=6 for d≥2. For d=1 no nontrivial split exists. Properly intersecting the two divisors gives an effective codimension-two cycle through the chosen points, including when it is reducible.

## Approach 3: quantitative resolved projection, with all-m remainders

Blow up {p}×P²_y. Projection from p gives g:Bl_p(P²_x)×P²_y→W=P¹×P²_y, a flat P¹-bundle, and blowdown φ. For L the first hyperplane on W, g*L=φ*A−E. We have φ_*g*(LH)=AH, since EH maps to a curve and hence pushes to zero as a surface; φ_*g*(H²)=H².

A coprime O_W(r,s) pencil has curve intersection class 2rs LH+s²H² and passes through h(r,s)−2 general points. Flat pullback then proper pushforward gives a surface of class 2rs AH+s²H² covering that many general X-points. The rational map X⇢W is dominant; the general points avoid its indeterminacy locus and push to a general tuple, and their inverse images are contained in the pulled-back cycle. The exceptional locus cannot remove these points upon pushforward.

Take s=floor sqrt(ma), r=floor(mb/(2s)), so both deficits ma−s² and mb−2rs are nonnegative integers. Use the established exact counts for the residual H² and AH classes, on disjoint subsets of the original general tuple. Addition of effective cycles proves the stated all-m formula. Since s=√(ma)+O(1) and r=(b/(2√a))√m+O(1), its cubic leading term rs²/2 is (b√a/4)m^(3/2), with O_{a,b}(m) error. For fixed a,b, r≥1 eventually. An explicit sufficient condition is m≥4a/b², together with m≥1; then mb≥2√(ma)≥2s.

The original sequence m=4ad² is recovered exactly by s=2ad, r=bd, with no remainders; it gives (bd+1)binom(2ad+2,2)−2. Thus the generated constant and class arithmetic are valid. The blowup construction itself is Lehmann's known construction, not our invention.

## Approach 4: Grassmannian rigidity and first interior class

Use published multirigidity of the two Schubert surface rays, as summarized in Lehmann Remark 6.3 with references to Robles–The and Robles. An m-multiple is a sum of ruling planes with total multiplicity m. A Q-point corresponds to a line in P³. Two general such lines are skew. They neither pass through a common point nor lie in a common plane, so no Schubert plane of either type contains two general Q-points. Conversely a plane of either ruling can be chosen through any Q-point. Therefore each boundary count is exactly m.

For P²=σ₂+σ₁,₁, the interpolation lemma with d=1 gives mc(P²)≥4. To show equality, an integral surface of Plücker degree two spans a projective space of dimension at most three by the standard projective degree bound deg(V)≥codim_span(V)+1. Thus it cannot contain five general Q-points, which span P⁴. A reducible degree-two effective surface cycle is a pair of planes, counted with multiplicity. Every plane on Q is in one of the two Schubert rulings, so such a cycle covers at most two general points. These exhaust possibilities because every nonzero integral projective surface has positive integral degree. Thus mc(P²)=4. The standard degree bound follows, for instance, by successive general hyperplane sections to a nondegenerate integral curve and its generic hyperplane section, whose span requires at least codimension-plus-one points; it is used only for this low-degree exact check.

## Approach 5: interior complete intersections and rounding

The coprime O_Q(d) pencil gives class d²P² and capacity h_Q(d)−2. For β=uσ₂+vσ₁,₁ set t=min(u,v), d=floor sqrt(mt). Add mu−d² and mv−d² ruling planes, each through one additional general point. Both numbers are nonnegative. The resulting class is exactly mβ and its capacity is h_Q(d)−2+m(u+v)−2d². Since d⁴=m²t²+O_t(m^(3/2)), the leading coefficient is t²/12 and the normalized mobility lower bound is 2t². This also verifies the generated subsequence m=td₀², where d=td₀. No upper asymptotic coefficient or optimality is established.

## Approach 6: can unequal bidegrees improve the mixed-face constant?

This is a substantive obstruction check on the chosen construction, not an upper bound on arbitrary cycles. Suppose two divisors on W have bidegrees (r₁,s₁) and (r₂,s₂). Their intersection consumes H²-budget s₁s₂ and AH-budget r₁s₂+r₂s₁. At leading cubic order the number of general points they can both contain is at most (1/2)min(r₁s₁²,r₂s₂²). Set T to that minimum. Then

r₁s₂+r₂s₁ ≥ T(s₂/s₁²+s₁/s₂²) ≥ 2T/√(s₁s₂),

where the last step is s₁³+s₂³≥2(s₁s₂)^(3/2). Under budgets s₁s₂≤ma and r₁s₂+r₂s₁≤mb, this yields T/2≤(b√a/4)m^(3/2). Equality is attained in the leading-order optimization by equal bidegrees saturating both budgets. Consequently simply replacing the pencil by two unequal divisors does not improve this leading constant in the regime where all degrees scale like √m. Degenerate or multiscale regimes and arbitrary families are not claimed controlled by this calculation. In particular this cannot establish a global sharp coefficient.

## Verification, attribution, and remaining obstacles

`check_exact.py` is deterministic exact-integer regression testing. `CHECK_RESULTS.json` records 736,400 product pencil splits; 44,850 quadric splits; 44,451 admissible mixed rounding cases; 6,859 square-subsequence identities; 90,000 quadric rounding cases; and component-budget dynamic programming through 300. The dynamic program uses the elementary product-component capacity bound, not a geometric oracle. These finite checks supplement but do not prove the geometric results. Small cases give mc(AH)=2, mc(H²+A²)=2, mc_Q(P²)=4, and mc(4(H²+AH))≥10.

The generated principal surface formulas pass this audit, subject to the stated characteristic-zero and published-multirigidity inputs. Its wording suggesting candidate novelty should be softened: no independent novelty certification is available, and the component classifications and blowup method are already published. The all-m lower bounds are refinements of its exposition, not a settlement of the broader original question. Additional other-dimensional generated statements have not been re-proved here and are not acceptance-certified by this report.

What remains unresolved here: sharp mixed-face leading constants and matching upper bounds; actual mobility volumes for general big surface classes on either fourfold; a full quantitative answer in all cycle dimensions; and a thorough current-literature novelty assessment. Exact growth exponents alone were already known. The broad AIM request therefore remains PARTIAL in this work.

### Primary sources and provenance

- Brian Lehmann, *Iitaka dimension for cycles*, Trans. Amer. Math. Soc. 371 (2019), 4815–4835, Example 1.10, Theorem 6.1, Remark 6.3. https://arxiv.org/abs/1708.02957 and https://sites.bc.edu/lehmann/wp-content/uploads/sites/36/2019/12/iitakadim.pdf . Author-hosted PDF inspected during source verification and mathematical review.
- Brian Lehmann, *Volume-type functions for numerical cycle classes*, Duke Math. J. 165 (2016), 3147–3187. https://arxiv.org/abs/1601.03276 . Definitions and normalization checked against the published source.
- Colleen Robles and Dennis The, *Rigid Schubert varieties in compact Hermitian symmetric spaces*, https://arxiv.org/abs/1102.1966 ; Colleen Robles, *Schur flexibility of cominuscule Schubert varieties*, https://arxiv.org/abs/1203.0328 . Their application here is through Lehmann's explicit summary, not a claim of independently re-proving or fully inspecting those papers.
- AIM Positivity of cycles, section 2 item 2.3: http://aimpl.org/poscycles/2/ . Live endpoint unsuccessful in source recovery; original wording and item identity retain the corpus-only caveat.

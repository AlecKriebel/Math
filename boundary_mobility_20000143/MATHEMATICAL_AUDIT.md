# Independent audit of surface mobility estimates

Date: 2026-10-21. Scope: complex varieties, integral effective numerical surface classes on P² × P² and Gr(2,4). This is an authored mathematical audit, not an independent historical or novelty certification. The source gate controls identification and status of the broad AIM problem; its original live endpoint was unavailable. The specialized statements below cannot resolve the broad historical question by themselves.

## Verdict

The generated attempt's principal surface equalities and lower estimates pass mathematical review, subject to the standard published multirigidity input for the Grassmannian upper bounds. Its square-subsequence lower constants are correct. The proposed integer-rounding extension strengthens those lower estimates to liminf statements with the same constants, without claiming sharpness. Exponents 1, 3/2 and 2, factor-plane/product classification, the mixed-face blowup mechanism and Schubert multirigidity are prior literature, not new discoveries.

No fatal surface-proof gap was found. The original novelty language is not accepted as established novelty. Other-dimensional auxiliary assertions are not included in this surface acceptance.

## 1. Conventions and quantifiers

Put A = p_x^*O(1), H = p_y^*O(1). The class H² is P²_x × {y}, A² is {x} × P²_y, and AH is a product of lines. For an integral surface V with class uH²+wAH+vA², its intersections with A², AH, H² are respectively u,w,v. These numbers are nonnegative. On Q = Gr(2,4), P² = σ₂+σ₁,₁; σ₂ parametrizes lines through a point and σ₁,₁ parametrizes lines in a plane of P³.

Mobility is the capacity to contain a general tuple of ambient points in an effective cycle, allowing reducibility and positive multiplicity. It is not the parameter-space dimension. The finite lists of degree bounds appearing below allow a single general open condition to work simultaneously for all relevant degree choices and all subsets of the given tuple. Constructions through arbitrary general tuples give dominant incidence families: one can use the algebraic parameter spaces of divisors/planes and their products, or the finite-type Chow space of the fixed degree. General-point assertions are not silently replaced by assertions about special tuples.

Multiplicity uses class without increasing support. Thus it never improves any upper-bound point capacity. To combine lower bounds, partition the complete general tuple into disjoint subsets and use one construction on each; each subset remains general. This justifies addition of capacities, without assuming that a prechosen cycle contains additional general points.

## 2. Exact product boundary counts

For an irreducible surface with w=0, resolve V and pull back A,H. The Hodge-index inequality (AH)²≥A²H² gives uv=0. Both cannot vanish because (A+H)² has positive degree on V. If u>0, then A is big and nef and H lies in its orthogonal complement with H²=0; negative definiteness forces H numerically trivial. The morphism to the second P² is consequently constant: a positive-dimensional image would give positive degree on an appropriate curve. Thus V is the primitive first-factor plane. The symmetric case gives the opposite factor plane.

Every cycle of class m(aH²+cA²) therefore consists of factor planes with total multiplicity m(a+c). Distinct coordinates of general point-pairs permit at most one point on each such plane; selecting one plane per point attains the bound. Hence mc(m(aH²+cA²))=m(a+c), including the zero-class case m=0 under the usual mc(0)=0 convention.

If V has class qAH, both projection images are curves, since A²=H²=0 and AH>0. An integral surface contained in the irreducible surface C×D equals C×D. Its class is de AH, with d,e positive curve degrees. Such a component contains at most min{d(d+3)/2,e(e+3)/2} points of a general tuple. This is at most 2de: assuming d≤e, d+3≤4e. Summing over components and retaining their multiplicities yields the upper bound 2m for class mAH. Pairing 2m general point-pairs and taking products of the two joining lines gives equality. Thus mc(mAH)=2m. Restricting the optimization to irreducible cycles would be a different problem and is not legitimate here.

## 3. Coprime interpolation pencils

For W=P¹×P² let h(R,S)=(R+1)binom(S+2,2), R,S≥1. General points impose independent conditions on H⁰(O(R,S)) until it is exhausted. For N=h(R,S)−2 points, the vanishing space has dimension two. Suppose its pencil has fixed divisor F of bidegree (i,j), where (i,j)≠(0,0) and the residual class is nonzero. If F contains r of those points, generality implies r≤h(i,j)−1. At the other N−r points, two independent residual sections vanish, so N−r≤h(R−i,S−j)−2. A trivial residual class cannot have two independent sections and is excluded directly.

The inequality h(i,j)+h(R−i,S−j)≤h(R,S) contradicts those two bounds. It holds for every such proper effective decomposition. For j=0 the difference is i binom(S+2,2)−(i+1)≥0, and j=S follows by interchanging the two summands. For 1≤j≤S−1 write f(s)=binom(s+2,2), U=f(S)−f(j), V=f(S)−f(S−j). The difference is (i+1)U+(R−i+1)V−f(S), at least U+V+min(U,V)−f(S). If j≤S−j, the latter is 2V−f(j)≥0, since 2V=j(2S−j+3)≥f(j); interchange j and S−j otherwise. Thus the pencil has no fixed divisor, and its two generators intersect properly in a curve.

For Q, Pic(Q)=ZP and h_Q(d)=(d+1)(d+2)²(d+3)/12. The identical argument uses h_Q(e)+h_Q(d−e)≤h_Q(d), 1≤e≤d−1. Discrete convexity makes the left side largest at an endpoint, and h_Q(d)−h_Q(d−1)≥h_Q(1)=6 for d≥2. For d=1 there is no proper positive decomposition. A residual degree-zero pencil is again impossible. Accordingly h_Q(d)−2 general points lie on a proper complete-intersection surface of class d²P².

This is an incidence/interpolation proof, not an inference from the dimension of the space of pairs of sections. It requires no smoothness or irreducibility of the resulting intersection.

## 4. Mixed product face and integer rounding

Blow up {p}×P²_y and map g:Bl_p(P²_x)×P²_y→P¹×P²_y by the pencil through p. If L is the P¹ hyperplane and E the exceptional divisor, g*L=φ*A−E. The bundle g is flat. Pulling back an effective curve therefore gives an effective surface, and φ pushes it to an effective surface cycle. The exceptional EH term is contracted to a curve, so φ_*g*(LH)=AH and φ_*g*(H²)=H².

A coprime pencil of bidegree (r,s), r,s≥1, consequently yields a surface of class s²H²+2rs AH through (r+1)binom(s+2,2)−2 general points. The rational map X⇢W is dominant, so the image of a general tuple is general and avoids the indeterminacy locus. Each such lifted point survives in the support of the pushed-forward cycle. Taking r=bd and s=2ad proves precisely

mc(4ad²(aH²+bAH)) ≥ (bd+1)binom(2ad+2,2)−2.

Its leading numerator is 2a²bd³, and (4ad²)^(3/2)=8a^(3/2)d³. The stated limsup lower constant b√a/4 is correct.

The rounded extension also passes. For α=aH²+bAH and m with r≥1, set s=floor(√(ma)) and r=floor(mb/(2s)). Both residual coefficients ma−s² and mb−2rs are nonnegative integers. Add that many first-factor planes and line products respectively, using one additional general point per plane and two per line product. This proves

mc(mα) ≥ (r+1)binom(s+2,2)−2 +(ma−s²)+2(mb−2rs).

As m→∞, s/√m→√a and r/√m→b/(2√a), hence the normalized leading term is b√a/4. Thus liminf mc(mα)/m^(3/2)≥b√a/4. For the finitely many m with r=0, this pencil construction is not asserted; the elementary residual-only construction remains available. The asymptotic statement is unaffected. Interchanging factors proves the opposite mixed-face version. No matching upper leading constant is supplied.

## 5. Grassmannian rays and interior lower estimates

The external geometric input is multirigidity of σ₂ and σ₁,₁. It was checked in Lehmann's Iitaka paper, Remark 6.3, which identifies σ_(n−2,0) and σ_(j,j) as multirigid. At n=4 these include the two surface rays. This audit uses that stated published input; it does not independently reprove the complete Robles–The/Robles classification.

Every effective mσ₂ or mσ₁,₁ cycle is a sum of the corresponding planes, with total multiplicity m. Two general points of Q represent skew lines of P³; neither ruling plane can contain both. Selecting a ruling plane through each point attains mc(mσ₂)=mc(mσ₁,₁)=m.

For β=uσ₂+vσ₁,₁ and t=min(u,v)>0, a degree-td pencil contributes t²d² in each coefficient. Appending td²(u−t) and td²(v−t) ruling planes gives exactly td²β and at least h_Q(td)−2+td²(u+v−2t) points. Dividing by (td²)²/24 gives mob(β)≥2t², as claimed.

More generally, for any m≥1 put d=floor(√(mt)). A degree-d pencil and the nonnegative residual ruling-plane coefficients give

mc(mβ) ≥ h_Q(d)−2+m(u+v)−2d².

Since d⁴/m²→t², liminf mc(mβ)/m²≥t²/12, and multiplication by 24 again gives mob(β)≥2t². These are lower bounds only; no equality or optimality follows.

## 6. Attribution and scope restrictions

The published exponent inventory is not a new result. Lehmann, “Iitaka dimension for cycles,” Example 1.10 already provides the product-face classification and mixed-face blowup mechanism; Theorem 6.1 and Remark 6.3 cover the Grassmannian rays. The exact elementary counts may be useful explicit consequences, but absence from a targeted search does not establish novelty. The rounding argument is an audited quantitative elaboration, not a certification of new research priority.

All accepted assertions here are over C. Surface resolution and the cited rigidity/Iitaka results are used in that setting. No blanket positive-characteristic extension is certified. Rational classes require divisible integral multiples; no finite-count meaning is assigned to arbitrary real multiples without an integrality convention.

For surfaces on these fourfolds κ=2ρ, while mob(α)=24 limsup mc(mα)/m². These must not be conflated. The original broad problem covers numerical cycle classes generally; acceptance of these particular surface refinements is partial quantitative progress, not a full resolution of the original problem.

Public primary references: Brian Lehmann, “Volume-type functions for numerical cycle classes,” https://arxiv.org/abs/1601.03276; Brian Lehmann, “Iitaka dimension for cycles,” https://arxiv.org/abs/1708.02957. Original classification sources cited through the latter: https://arxiv.org/abs/1102.1966 and https://arxiv.org/abs/1203.0328.

## 7. Two additional exact finite checks

The proposed strip formula mc(aH²+AH)=a+2, for every integer a≥0, also passes. By coefficient nonnegativity there is a unique irreducible component with positive AH coefficient, its coefficient and multiplicity both being one. Its H² intersection is zero and its AH intersection positive, so its second-factor image is an integral curve C. The intersection AH on this component equals deg(C) times the positive integer A-degree of its generic fiber over C. Thus deg(C)=1. It can contain at most two of the projected coordinates of a general tuple. All remaining components have AH coefficient zero and A² coefficient zero, hence are first-factor planes. If the distinguished component uses u of the H² coefficient, at most a−u such planes remain. The upper capacity is at most a−u+2≤a+2. The matching construction uses a first-factor planes and one line product on a disjoint pair of points. The factor-swapped formula follows as well.

The proposed exact formula mc_Q(P²)=4 also passes. Its total Plücker degree is two. An integral projective surface of degree two spans a projective space of dimension at most three, by the standard elementary bound degree≥codimension+1 for a nondegenerate integral projective variety. It therefore cannot contain five general Q-points, which span P⁴. If the cycle has more than one component or a component of multiplicity greater than one, its degree-two budget forces its support to consist of at most two linear planes; every plane in Q is one of the two rulings and contains at most one point of a general tuple. The lower bound four is the d=1 coprime-pencil construction. The span-degree bound concerns integral surfaces in their actual linear spans, not the dimension of their parameter spaces.

## 8. Final authored report review and reproducibility

The authored REPORT.md's additional unequal-bidegree optimization was checked separately. If T=min(r₁s₁²,r₂s₂²), then r₁s₂+r₂s₁≥T(s₂/s₁²+s₁/s₂²)≥2T/√(s₁s₂). Under the stated class budgets this gives T/2≤b√a·m^(3/2)/4. The report correctly limits its leading-coefficient conclusion to all degrees scaling like √m, because lower-order Hilbert terms need not be lower order in arbitrary degenerate regimes. It does not improperly promote this construction-specific bound to a global mobility upper bound.

The REPORT.md degree-span explanation is adequate as an invocation of the standard nondegenerate degree bound; the exact low-degree conclusion is correct. All six approaches were read. The all-m error term O_{a,b}(m) and the sufficient condition m≥max(1,4a/b²) for r≥1 were checked. No change to the report was required for mathematical acceptance.

The supplied check_exact.py was independently read and rerun successfully. It reproduced CHECK_RESULTS.json exactly: 736400 product-pencil splits, 44850 quadric-pencil splits, 44451 admissible mixed rounding cases, 6859 square-subsequence identities, 90000 quadric rounding cases, and component-budget dynamic programming through 300. The dynamic program is an upper-capacity arithmetic consistency check, not an independent proof that each high-degree component capacity is geometrically attained. The report states the relevant limitation. Separately, the pencil inequalities were also independently enumerated before running that script.

Acceptance concerns mathematical correctness of the stated surface refinements and truthful partial-status restrictions; it does not certify novelty, settle all dimensions, or verify a live canonical AIM statement. The public package inventory identifies the exact publication files; the verification receipt records the accepted-input to publication transformation. The broad AIM question remains UNSOLVED.

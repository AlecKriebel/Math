# A four-fifths retention obstruction for canonical Bose–Chowla lifts

12 October 2026. Independently audited correction edition of a construction-specific theorem. The source candidate is preserved unchanged; see AUDIT_BOSE_RETENTION.md for the corrections and acceptance scope. No novelty claim. No publication or repository mutation is part of this packet.

## Main theorem and scope

Let p tend to infinity through odd finite-field orders. With F, K=F(θ), θ²=δ nonsquare, generator g, q=p²−1 and λ≠0 as in Part I, let B be the full p-element affine Bose–Chowla set in either the positive canonical integer lift or the positive canonical single-coset half-integer lift. Every subset B′⊂B with B′∩(B′+B′+B′)=∅ satisfies

    |B′| ≤ (4/5 + o(1)) p.

The error is uniform over translations, unit dilations, and the two lift conventions separately. Since 4/5<sqrt(2/3), this passes that benchmark for this specific construction. It proves no bound for arbitrary Sidon sets, noncanonical lifts, longer ambient intervals, or mixed lattice cosets, and does not resolve Erdős 864. No effective field-order threshold is claimed.

The proof has two established external inputs: polynomial Dirichlet L-function RH, already used in the accepted carry proof copied as BOSE_CARRY_DEPENDENCY.md; and tame rank-one character-sum RH on curves, applied through tensor induction as precisely described in Part I. These are established theorems, not unproved hypotheses. The new argument and its use of those inputs are independently accepted in the accompanying audit report, subject to its precise construction-specific scope.

Part I proves all conditional source/target laws, enumerates the exceptional fibers and character resonances, and establishes uniform weighted incidence bounds. Part II gives an explicit smoothed coupling with mass approaching 1/5 and aggregate degree at most one. It applies directly to arbitrary deleted subsets; no geometric model or equidistribution is assumed for the deletion pattern. The same coupling and a dual certificate show that 1/5 is the exact optimum of this continuum fractional first-moment method, without claiming optimality for actual subsets.

## Part I. Full conditional incidence theorem

# Conditional incidence laws for canonical Bose–Chowla lifts

12 October 2026. Mathematical research note; no repository mutation or publication. This extends the accepted carry proof by a standard rank-one character-sum theorem on curves. It is not a proof of the interval conjecture.

## Statement and conventions

Let F have odd order p, K=F(θ), θ²=δ a nonsquare, q=p²−1, and let g generate K*. Let λ≠0 and ε∈{0,1/2}. Use the accepted positive canonical lifts B, with μ=λ²g^(2ε). Write X_a=B_a/q∈(0,1]. Let S(a) count ordered genuine equalities B_a+B_b+B_c=B_d with a fixed in one prescribed source role, and let T(d) count the same equations with d fixed in the target role.

Uniformly in F, δ, g, λ, ε and all indicated points:

- Except for at most two source points a, S(a)=p(1−X_a)²/2+o(p).
- The at most two exceptional source points have S(a)=0 exactly.
- Except for at most one target point d, T(d)=pX_d²/2+o(p).
- The exceptional target, if present, has at most two modular triples, so T(d)≤2.

In particular, the upper laws S(a)≤p(1−X_a)²/2+o(p) and T(a)≤pX_a²/2+o(p) hold uniformly at every point, with absolute errors that are o(p). Repetitions are included throughout.

## 1. Fixed source: the two genuine exceptions

Fix a and write M=μ(θ+a)=uθ+v. For b∈F put U=ub+v and V=vb+uδ. For U≠0 the remaining coordinates are

    c=(1−V)/U,   d=Uδ+Vc.

If U=0,V=1, every c is permitted with d=c. As in the accepted proof, this occurs precisely when N(M)=−u. The condition is quadratic in a with leading coefficient N(μ)≠0, so it gives at most two a-values.

In this exceptional case u≠0 and b0=−v/u satisfies M(θ+b0)=1. The complete fiber is exactly the union

    b=b0, d=c;     c=b0, d=b.

(The two lines intersect once.) Every genuine zero-carry equation on either line would require B_a+B_b0=0. Positivity excludes this. Thus S(a)=0, although the modular fiber has 2p−1 points.

## 2. Fixed source: ordinary fibers and the collision fiber

When N(M)≠−u, the fiber has p or p−1 points. The accepted factorization is

    θ+c=−conj(M)(b−r)/(ub+v),   r=θ+1/conj(M).

For Fourier frequencies n,m in the b,c log coordinates, use the multiplicative character χ with χ(g)=exp(2πi/q). Outside the collision r=−θ, the quadratic minimal polynomials for −θ and r are distinct. The accepted squarefree-modulus CRT argument bounds every nontrivial pair χ^n,χ^m by 4√p, once p is large relative to fixed |n|,|m|. The possible linear denominator is included with zero at its root.

The collision r=−θ is exactly M=1/(2θ), hence u=1/(2δ),v=0. It is not a norm exception. Here b≠0 and

    c=δ/b,   d=(b+δ/b)/2,
    θ+c=θ(θ+b)/b.

The Fourier sum, apart from a unit scalar, is

    Σ_{b∈F*} χ^(n+m)(θ+b) χ^(−m)(b).

It is a Dirichlet character sum with one irreducible quadratic and the linear factor T. It can be principal only if q divides n+m and p−1 divides m. For a fixed nonzero pair (n,m), this is impossible once p is sufficiently large. Consequently this fiber also has every fixed nonzero Fourier coefficient O(√p), with bound 2√p. This is why it must not be treated as a permanent obstruction merely because arbitrary high-order character pairs can resonate there.

After division by p, all nonexceptional fixed-source fibers therefore converge uniformly to Haar measure in their two free log coordinates.

## 3. Fixed target: a genus-at-most-one curve

Fix d and write

    R=(θ+d)/μ=sθ+t,   s,t∈F,   R≠0.

The target fiber is

    ab+ac+bc+δ=s,
    abc+δ(a+b+c)=t.

Eliminating c gives the bidegree (2,2) equation in P¹×P¹

    F(a,b)=a²b²−δ(a²+b²)−s ab+t(a+b)−δ(s−δ)=0.       (A)

For a+b≠0, c=(s−δ−ab)/(a+b). If a+b=0 at an F-point, equation (A) forces s=δ−a²≠0, and the unique valid third coordinate is c=t/s. Thus this plane model represents every affine F-point of the original target fiber uniquely. The second factor a²−δ that arises on substituting b=−a has no F-roots.

The projective model can also be described directly in (P¹)³ by homogenizing

    ∏(a_i+θ)=R,   ∏(a_i−θ)=conj(R).

Its boundary consists of the six points P_ij, i≠j, at which a_i=−θ, a_j=+θ and the remaining coordinate a_k=∞. No two coordinates can simultaneously be infinite. All six are distinct, and all are smooth: at P_ij use local parameters x=a_i+θ, y=a_j−θ, z=1/a_k. The defining equations have linear parts 2θx−Rz and −2θy−conj(R)z, which have rank two. Moreover x,y,z all vanish to order one. This model is birational to the (2,2) model; take the normalization of either model to resolve any remaining finite singularities. Its genus is at most the arithmetic genus (2−1)(2−1)=1. Boundary points are unaffected by normalization.

## 4. Exactly one geometrically reducible target parameter

As a quadratic in b, (A) has discriminant

    D(a)=4δa⁴−4ta³+(s²+4δs−8δ²)a²
         +(4δ−2s)ta+t²−4δ²s+4δ³.

The leading coefficient is nonzero. Equation (A) is geometrically reducible exactly when D is a polynomial square over the algebraic closure. The quadratic coefficients have no common polynomial factor: at a=±θ, the linear coefficient t−sa is nonzero because N(R)=t²−δs²≠0. Thus the usual discriminant test has no missing vertical component.

If t≠0 and D=(2θa²+A a+B)², coefficient comparison gives A=−t/θ and B=θ(s−2δ); comparing the a² coefficient then gives t²=δs², impossible.

If t=0, coefficient comparison gives

    (s²+4δs−8δ²)²−64δ³(δ−s)=s³(s+8δ)=0.

The case s=0 is impossible because R≠0. Therefore the only reducible value is

    R=−8δθ.

At that value

    F(a,b)=[ab+3δ+θ(a−b)][ab+3δ−θ(a−b)].

Frobenius exchanges the two components. Any F-point must lie on both, so a=b and a²=−3δ. The original equations then force c=a, also in characteristic 3. Hence there are at most two triples, exactly the triples (a,a,a) with a²=−3δ. Since d↦(θ+d)/μ is injective, at most one target d is exceptional.

All other targets are geometrically irreducible. They need not all be smooth: in characteristic 3 there can be a whole family of singular irreducible fibers. Normalization handles these uniformly. The arithmetic genus is one, so the discrepancy between sums over the affine curve and its normalization is O(1), uniformly; the total singularity delta invariant is at most one.

## 5. External input and the extension-field character

External input: for a smooth geometrically connected curve U over F with smooth completion of genus h, a geometrically nonconstant, rank-one, finite-monodromy, tame lisse character sheaf with at most r geometric punctures has trace sum of absolute value at most (2h−2+r)√p. Finite monodromy gives weight zero and tameness makes every Swan conductor zero.

A directly inspected primary source is Lei Fu and Daqing Wan, *A Class of Incomplete Character Sums*, arXiv:1303.3650v3 (6 January 2025), https://arxiv.org/pdf/1303.3650v3. Proposition 1.2 provides the tensor-induction trace identity for an arbitrary geometrically connected scheme. Proposition 4.1 and Theorem 4.2 provide the curve estimate with genus, boundary and Swan conductors. The rank-one Kummer calculation in section 2 identifies its geometric monodromy. The present proof supplies the curve geometry and nontriviality check, rather than invoking a generic character-sum estimate without these hypotheses. The v3 correction concerns Theorem 4.6, which is not used here.

For clarity, apply tensor induction from K to F to the Kummer sheaf attached to χ and

    f=(a+θ)^n(b+θ)^m

on the normalization with the six boundary points removed. Its F-Frobenius trace at an F-point is exactly χ(f), by the tensor-induction trace identity. After base change back to K, it is the tensor product of the Kummer sheaf for χ,f and that for χ^p,conj(f). Equivalently its geometric Kummer function is

    f·conj(f)^p.

This identity also follows directly from the function-field construction: conjugating a q-th-root torsor by the nontrivial constant-field automorphism changes the root-of-unity character χ into χ^p. The tensor-induction proof is valid on the curve's function field, not just on a rational base.

At P_12 (a=−θ,b=+θ,c=∞), the valuation of this function is n+pm. At P_21 it is m+pn. If |n|,|m|<p−1, both absolute values are less than q. If both were divisible by q, they would both vanish, forcing n=m=0. Thus for every fixed nonzero Fourier pair and sufficiently large p, the induced sheaf is geometrically nonconstant. This argument is independent of the generator: replacing g multiplies all exponents by a unit modulo q, which does not change divisibility.

The sheaf has rank one, finite monodromy of order prime to the characteristic, and is tame at all six boundary points. With h≤1, its trace sum has magnitude at most 6√p. Passing from the normalization back to the original finite fiber costs O(1). The constant Fourier coefficient is p+O(√p) by the ordinary curve bound. All constants are independent of R, μ and g. Hence every nonexceptional fixed-target fiber is uniformly equidistributed in its first two log coordinates.

## 6. Moving triangles, half cosets and endpoints

The Fourier statements give uniform convergence on every fixed continuous test function on T². The parameter X in the carry conditions varies with the point. To obtain a uniform statement for these moving sets, partition X∈[0,1] into a fixed finite mesh. Triangle inclusions sandwich each moving triangle between neighboring mesh triangles. Their Haar measures differ by O(mesh size). Apply the fixed-set convergence at the finitely many mesh points, then send mesh size to zero. Triangle boundaries have zero Haar measure.

For a fixed source with normalized value X, a genuine zero-carry configuration corresponds, outside coordinate seams, to free positive coordinates y,z with y+z<1−X. Its area is (1−X)²/2.

For a fixed target of normalized value X, its first two source coordinates y,z determine the third coordinate modulo one. Genuine equality occurs exactly on y+z<X, apart from seams and boundaries. Its area is X²/2.

The half coset introduces only constant phases and the already-correct algebraic parameter μ=λ²g; none of the character arguments divide by two modulo q. For the integer lift, the one possible zero-residue point is represented by 1 rather than 0. On a nonexceptional source fiber, fixing either free source to this point leaves at most one solution, while fixing the target to this point leaves at most two by strong Sidonicity. Thus its seam correction is O(1). On any fixed-target fiber, fixing one source to the seam point leaves at most two ordered pairs, hence the total seam correction is O(1). Exceptional source fibers were already handled exactly. The value X=1 is therefore included: the source count is zero; the target count is p/2+o(p) at a nonexceptional target and is at most two at the possible exceptional target. In all cases the uniform target upper bound remains valid.

These observations prove all the stated uniform conditional incidence laws and their upper-bound versions.

## 7. Uniform degrees for a smooth interior edge weight

Let Δ={ (x,y,z)∈R³ : x>0,y>0,z>0,x+y+z<1 }. Fix any nonnegative continuous function W with compact support in Δ, and extend it by zero to all R³. Give each genuine ordered equality B_a+B_b+B_c=B_d weight W(X_a,X_b,X_c). Define the four role-degree profiles on [0,1] by

    D1(x)=∫_[0,1]² W(x,y,z) dy dz,
    D2(x)=∫_[0,1]² W(y,x,z) dy dz,
    D3(x)=∫_[0,1]² W(y,z,x) dy dz,
    D4(x)=∫_[0,1]² W(y,z,x−y−z) dy dz.

Because W is zero outside Δ, the last integral automatically restricts to y,z>0 and y+z<x. All four profiles are nonnegative continuous functions. These formulas do not assume W is symmetric in its source coordinates.

For each i≤3, fixing a point of normalized coordinate x in source role i gives weighted degree pDi(x)+o(p), uniformly at every nonexceptional source point. It gives weighted degree zero at either norm-exceptional source point. Fixing a target of coordinate x gives weighted degree pD4(x)+o(p), uniformly at every nonexceptional target point. The exceptional target contributes at most 2||W||∞.

Consequently, in all four roles and at every vertex, the pointwise upper bound

    weighted role-degree ≤ pDi(x)+o(p)

holds uniformly. The little-oh error may depend on the fixed function W but is independent of the finite field, generator, translation, half coset and vertex. In particular the total weight of edges containing a vertex of coordinate x is at most

    p[D1(x)+D2(x)+D3(x)+D4(x)]+o(p).

Repeated appearances of a vertex only make this union bound safer.

Proof of the uniform weighted assertion: the families of functions W(x,·,·), W(·,x,·), W(·,·,x), and (y,z)↦W(y,z,x−y−z), as x varies in [0,1], are compact subsets of C(T²) in the uniform norm. This follows from continuity of the zero extension and uniform continuity on a fixed compact set. They define continuous periodic functions because the support stays a positive distance from each source-coordinate seam. Uniform fixed-test-function equidistribution therefore extends to these entire families: choose a finite uniform-norm net, apply equidistribution to its finitely many members, and use the uniformly bounded fiber masses for the net error. The source and target fiber theorems then give the claimed profiles. The support condition removes all carry-boundary and representative-seam ambiguities, and the explicit exceptional-fiber bounds provide the uniform upper bounds there.

For completeness, the accepted global carry equidistribution also gives total edge weight

    p² ∫_Δ W(x,y,z) dx dy dz + o(p²).

Thus these degree laws can be used with any fixed continuous compactly supported smoothing of a proposed coupling on the simplex. The estimates are stated for each fixed W; no interchange with a field-dependent shrinking smoothing scale is asserted. A two-stage limit (first p→∞ for fixed W, then improvement of the smoothing) is valid.


## Part II. Smooth coupling and deletion

# Exact one-fifth weighted deletion certificate

12 October 2026. Authored exact continuum coupling certificate, independently audited in this correction edition. This file proves the continuum weight construction and its arbitrary-subset covering consequence. The full uniform weighted per-point source and target incidence laws are proved in Part I. No publication or repository mutation is part of this file.

## Application of the proved weighted incidence input

For the canonical Bose–Chowla p-point lifts of Part I, every integer triple-sum-free retained subset satisfies

    |B'| <= (4/5 + o(1))p.

Thus this construction-specific deletion obstruction is strictly stronger than retention sqrt(2/3)p. It does not prove the corresponding bound for arbitrary strong Sidon sets or arbitrary lifts.

## 1. Precise weighted incidence input

Let S be the open zero-carry simplex

    S={(x,y,z): x,y,z>0, x+y+z<1},   w=x+y+z.

For every fixed nonnegative smooth compactly supported W on S, let M be its integral with respect to dx dy dz, and let D_W(t) be the sum of the four one-coordinate marginal densities of the measure W dx dy dz, with coordinates x,y,z,w.

The needed input is:

- The total weighted number of ordered zero-carry equations is p²(M+o(1)).
- At a seed vertex b whose normalized coordinate is t=b/q, the sum of its four weighted role incidences is at most p(D_W(t)+o(1)), uniformly in b and the allowed seed choices.

Part I proves this upper bound at every vertex, including the explicit exceptional fibers. More generally, O(1) exceptional vertices with O(p) total weighted incidence each would suffice, as would errors whose sum over all p seed vertices is o(p²). The constants may depend on the fixed W. In particular, no uniformity over a shrinking smoothing parameter is required.

For any deleted set D_B whose complement has no zero-carry equation, weighted coverage gives

    p²(M+o(1)) <= p sum_{b in D_B} D_W(b/q)+o(p²).

Therefore a weight with D_W<=1 proves |D_B|/p>=M-o(1), regardless of the deleted set's geometry.

## 2. An exact singular coupling of mass one fifth

Take t uniform on [0,1/5]. Randomly permute the source triple

    {t, t+1/5, 3/5-t},

using each of the six permutations with equal probability, and set

    w=4/5+t.

The sum of the three source coordinates is w identically. Before the random permutation, the three source coordinates are uniform on [0,1/5], [1/5,2/5], and [2/5,3/5], respectively. After permutation, each source marginal is uniform on [0,3/5]. The target marginal is uniform on [4/5,1].

Give this probability distribution total mass 1/5. Then each source marginal density equals 1/3 on [0,3/5]. Their sum is one on that interval. The target marginal density equals one on [4/5,1]. Consequently the aggregate incidence density is

    1_[0,3/5] + 1_[4/5,1],

which is at most one almost everywhere. The singularity of this coupling must be removed before applying continuous test-function equidistribution; it cannot simply be inserted as a test density.

## 3. Rigorous smoothing with no incidence overload

Fix 0<eta<1/20, put s=1-4eta, and let epsilon=eta/10. Transform each source coordinate X by

    X'=sX+eta,

and the target by

    W'=sW+3eta.

The additive equation is preserved. Assign the transformed distribution total mass s/5. Each transformed source marginal still has density 1/3 on its interval, because both its interval length and total mass were scaled by s. The transformed target marginal still has density one on its interval.

Now add independent random variables Z1,Z2,Z3 to the three sources, where every Zi has an even, nonnegative C-infinity probability density supported in [-epsilon,epsilon]. Add Z1+Z2+Z3 to the target. The equation is again preserved identically.

The resulting law on the three source coordinates has a nonnegative C-infinity density W_eta: it is the convolution of a finite compactly supported source measure with the product of three smooth compactly supported probability densities. Its integral is exactly

    M_eta=s/5=(1-4eta)/5.

The support stays strictly inside S. Indeed all source supports are contained in

    [eta-epsilon, 3s/5+eta+epsilon]
      =[9eta/10, 3/5-13eta/10],

and the target support is contained in

    [4s/5+3eta-3epsilon, s+3eta+3epsilon]
      =[4/5-eta/2, 1-7eta/10].

These intervals lie inside (0,1) and are disjoint: the gap between the target's lower endpoint and the sources' upper endpoint is 1/5+4eta/5>0.

Each source marginal is the convolution of a density bounded by 1/3 with a probability density, hence remains bounded by 1/3. The target marginal is the convolution of a density bounded by one with the probability density of Z1+Z2+Z3, hence remains bounded by one. Since their supports are disjoint, the total four-role incidence density satisfies

    D_{W_eta}(x)<=1 everywhere.

Thus W_eta is an admissible fixed smooth nonnegative weight of mass (1-4eta)/5 and aggregate incidence at most one.

## 4. Consequence and order of limits

Apply weighted coverage for any fixed eta:

    |D_B|/p >= (1-4eta)/5-o_eta(1).

First let p tend to infinity, with uniformity in the allowed seed parameters. Then let eta decrease to zero. It follows that

    liminf |D_B|/p >=1/5,
    |B'| <=(4/5+o(1))p.

There is no interchange of a shrinking test function with the asymptotic incidence estimate. Equivalently, for any desired error delta>0 choose a fixed eta sufficiently small, and then choose p sufficiently large for that one fixed smooth W_eta.

Repetitions of source entries, and repeated role incidences at a deleted vertex, do not cause a gap: the covering inequality counts all roles and only overcounts destroyed equations. All weights are fixed and bounded when eta is fixed, so the allowed exceptional vertices remain negligible.

## 5. Sharpness of the weighted first-moment relaxation

The function

    h(x)=(3/5-x)_+ +(x-4/5)_+

is a feasible fractional vertex cover of the continuum zero-carry hypergraph and has integral exactly 1/5. Indeed, if x+y+z=w<=4/5, then

    h(x)+h(y)+h(z) >=9/5-w>=1.

If w>=4/5, then the same source lower bound and h(w)>=w-4/5 give

    h(x)+h(y)+h(z)+h(w) >=9/5-w+w-4/5=1.

Also

    integral h = (1/2)(3/5)^2+(1/2)(1/5)^2=1/5.

For any nonnegative weighted edge measure with aggregate marginal D<=1, integration of the covering inequality gives

    total edge mass <= integral h(x)D(x)dx <=integral h=1/5.

The smoothed coupling approaches this mass, proving that the supremum of the continuum smooth fractional matching problem is exactly 1/5. Thus no proof based solely on optimizing nonnegative edge weights with aggregate incidence bounded by one can improve the one-fifth deletion constant. Stronger conclusions need additional information, such as genuinely useful multi-point overlap constraints, not just a different first-moment weight.

This fractional optimizer is not claimed to be the density of an actual triple-sum-free subset. It certifies the limitation of this relaxation, not the sharp extremal constant for Bose–Chowla subsets.

## Narrowed public edition notice

All mathematical arguments, hypotheses, examples, substantive audit discussion and corrections above are retained. This edition removes unpublished artifact identifiers and related provenance metadata, replaces obsolete locators, and updates editorial history only. The scope of each theorem and review is unchanged. Exact reversible redaction records and private integrity inventories remain local and are not distributed. [EDITION_MAP.md](EDITION_MAP.md) describes the changes; [PRESERVATION.json](PRESERVATION.json) records mathematical-text preservation without republishing redacted identifiers. [PUBLIC_DEPENDENCIES.json](PUBLIC_DEPENDENCIES.json) identifies only distributed mathematical texts and already-published dependencies. [VERIFICATION.json](VERIFICATION.json) gives aggregate diagnostic results without program or diagnostic-file identities. No source document, executable code, raw per-case collection, dataset contents, private source, personal information or coordination record is included.

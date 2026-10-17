# Candidate proof: a two-tail order automorphism

Written 2026-10-17 20:24 UTC. Status: candidate; not yet promoted. Completion estimate 45% toward a verified apparently original complete solution, conditional on full definition/priority audits. Internal adversaries have checked the central mechanism, but fresh full-package reviews are still required.

## Precise theorem under explicit hypotheses

Let A_I be the group of all increasing homeomorphisms of [0,1] which are affine with positive slope on some right neighborhood of every x in [0,1). Let A_R be the group of all increasing homeomorphisms of R which have the same finite-point property and which agree with a positive affine map on some initial ray. All slopes are allowed; no rank or order is imposed on the target.

Let G=D_<2>([0,1]) be the group of locally right 2^Z-affine increasing homeomorphisms which are identity near both endpoints. There is an automorphism alpha preserving either of the two Dlab bi-orders on G such that, for every embedding e of G in A_I or A_R, no target element u implements alpha by conjugation.

If the standard interval and extended-real Dlab groups are all subgroups of these two explicit master groups (as the 1968 definition and indexed 1999 left-germ definition indicate), this theorem gives an affirmative answer to the corrected Kourovka 21.149, with a stronger embedding quantifier. That scope implication is a gate requiring primary-source reconciliation.

## 1. Ambient support and germ facts

Every element of A_I or A_R has its support components well ordered from left to right. To prove this, take any nonempty subfamily and the infimum a of its left endpoints. At finite a, continuity implies that a is fixed: if it were moved, a neighborhood would belong to one support component, and no component endpoint could approach a from the right. A positive affine right germ at a is either identity or has slope different from 1. In the identity case there is an empty right interval of support, contradicting the infimum. In the other case there is a support component beginning exactly at a and no other beginning sufficiently close on the right, so the chosen subfamily must contain that component. At a=-infinity, a nonidentity eventual affine germ has an initial support component containing a whole initial ray; all other components start to its right. An identity germ bounds all support below. Either way a nonempty subfamily has a first member.

At finite fixed a the right slope is a homomorphism from the stabilizer of a to the abelian positive multiplicative reals. At the left end of the real line, the eventual affine germ is a homomorphism A_R -> Aff_+(R); the latter is metabelian. Hence every perfect subgroup has trivial image in this germ group. Every element of a perfect subgroup of A_R fixes an initial ray. In A_I, every element of a perfect subgroup fixes an initial interval because its slope germ at 0 is trivial. Thus all support components of elements of e(G) have finite left endpoint.

The group G is nonabelian simple, hence perfect, by Dlab's simplicity theorem. For every nonempty open interval L=(a,b) with 0<a<b<1, G(L)={f in G: closure(supp f) is compactly contained in L} is isomorphic to G by an affine change of coordinates. It too is nonabelian simple and perfect. This is the only substantive external group theorem used.

## 2. Perfect centralizers have disjoint support

Suppose q has well-ordered support components with finite left endpoints, and P is a perfect subgroup commuting with q. Every p in P permutes the support components of q in increasing order, hence fixes each setwise: a well-ordered set has no nontrivial increasing bijection. On a component J=(a,b), every p fixes finite a. The slope homomorphism P -> R_(>0) is trivial, so p is identity on a right neighborhood of a. Since p commutes with fixed-point-free q|J, propagate this identity along q-iterates to every point of J. Indeed one direction of iteration sends every point toward a. Thus P fixes supp(q) pointwise.

For disjoint L,M, G(L) and G(M) commute. The preceding paragraph applied to each q in e(G(L)) and P=e(G(M)) shows that their full supports are disjoint. This is independent of any group order on the target.

## 3. Least local action components

For a subgroup B of increasing homeomorphisms, an action component means a component of the complement of the common fixed set of B. The subgroup B preserves each such component individually, since its finite boundary points are common fixed points.

The action of e(G) on each nontrivial action component is faithful: the restriction kernel is a proper normal subgroup of simple G. Fix 1!=f in G. Each action component contains a support component of e(f), and these support components are well ordered. Therefore the e(G)-action components have a least member J0.

For any interval L as above, e(G(L)) acts nontrivially on J0 by faithfulness of G there. Its restrictions to its own action components are faithful, by simplicity of G(L). Fixing any nonidentity local element and applying the same support argument gives a least e(G(L))-action component within J0; denote it K(L). These are genuine global action components, since the boundary of J0 is fixed by the whole e(G).

For disjoint L,M, K(L) and K(M) are disjoint by section 2. For each g in G, conjugation gives

    K(gL)=e(g)K(L).

Here e(g) preserves J0, and an increasing homeomorphism sends a least component to a least component.

## 4. Uniform orientation

The group G acts transitively on finite increasing tuples of distinct interior points. To verify this without a transitivity citation, prescribe such a tuple map and add the same outer endpoints c,d containing both tuples in (c,d). On each successive segment, let r>0 be target length divided by source length. Choose adjacent powers 2^k<=r<=2^(k+1). Realize that average by two affine pieces with these slopes, with proportions (2^(k+1)-r)/2^k and (r-2^k)/2^k. The result joins prescribed endpoints, is strictly increasing, and is identity outside [c,d]. Degenerate zero-length pieces are omitted. It is a finite PL member of G.

In particular, any positively separated pair L<M of relatively compact intervals can be mapped to any other such pair. Equivariance and the fact that e(g) is increasing imply a uniform dichotomy: either K(L)<K(M) for every L<M with a gap, or K(M)<K(L) for every such pair. Equality or overlap is impossible by disjoint support. Only positively separated pairs are needed below.

## 5. Explicit two-tail normalizer

For m>=0 let b_m=2^(-2m-2), a_m=b_m/2. Put C_m=(a_m,b_m) and D_m=(1-b_m,1-a_m). Thus C_(m+1)<C_m and D_m<D_(m+1), with positive gaps.

On the closure [a,b] of each C_m and D_m put a positive two-slope bump

    h(x)=a+2(x-a),                 a<=x<=a+(b-a)/3,
    h(x)=b+(x-b)/2,               a+(b-a)/3<=x<=b.

Put h(x)=x elsewhere. The formulas agree at the breakpoint, fix a,b, and give h(x)>x throughout (a,b). Each compact subinterval of (0,1) meets only finitely many bumps, so h and h^-1 are locally finite PL there with slopes in 2^Z. Shrinking bump lengths ensure continuity at 0 and 1, so h is an increasing homeomorphism of [0,1].

Set alpha(f)=h^-1 f h. Every f in G is identity near the two endpoints. On its compact interior support, composition with h and h^-1 preserves local right 2^Z-affinity. Thus h normalizes G and alpha is an automorphism. At the first support point of a nonidentity f, conjugating the affine right germ by the affine right germ of h preserves its slope. The first support point is transported increasingly, so alpha preserves both Dlab bi-orders, which Dlab characterizes by that first right slope.

For each L=C_m or D_m, h(L)=L, so alpha(G(L))=G(L), and alpha restricted to G(L) is nonidentity. For the latter, choose x in L with h(x)!=x and a small open V compactly contained in L with V disjoint h^-1(V). A nontrivial finite two-slope bump f supported in V has alpha(f) supported in h^-1(V), so alpha(f)!=f.

## 6. No target conjugator

Suppose e(alpha(f))=u^-1 e(f)u for every f in G. The element u normalizes e(G), hence permutes its action components increasingly and fixes their least member J0. For L=C_m or D_m, it normalizes e(G(L)) and therefore fixes the least local component K(L) setwise.

The restriction of u to K(L) cannot be the identity. Otherwise e(alpha(f)) and e(f) have the same restriction there for every f in G(L), and faithfulness of the simple local group's action on K(L) gives alpha(f)=f for every such f, contradicting section 5. Thus u has a nonempty support component lying entirely inside K(L): its finite endpoints are fixed by u, and infinite endpoints present no escape across the interval boundary.

If the uniform orientation of section 4 is preserving, the C_m give infinitely many strictly descending intervals K(C_m). If it is reversing, the D_m give infinitely many strictly descending intervals K(D_m). In either case choose a support component of u inside each. These components form a strictly descending sequence, contradicting section 1. No u exists.

## Dependencies and unresolved promotion gates

The support proof above is proposed as self-contained. Dlab 1968 supplies simplicity and the two source bi-orders. Exact 1999 master-group definitions, all intended ambient groups, originality relative to Gong--Yang--Zeng and subsequent literature, and repeated fresh full-document adversarial review are still required. A true finite-local-but-not-eventually-affine real target would invalidate the scope: a twisted diagonal construction can absorb automorphisms there, which is why the endpoint condition must never be omitted.

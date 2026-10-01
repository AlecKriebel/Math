# Author turn 5: nonabelian strand weights need a separate welded descent check

**Final substantive turn; original bundle unresolved, 5/5.** 2026-10-01.

This turn uses the actual ordered strand-weight construction in the source's reference, rather than the scalar whole-crossing model of Turn 4. It derives the extra welded relation and applies it to two concrete primary-source examples. A generic virtual cocycle in the general-second-component example fails to descend; the surviving subfamily transfers to a twist-second pair. A separate example retains genuinely noncommuting coefficients, so no conclusion that welded cocycles must be abelian is drawn.

## 1. Ordered strand coefficients and a general descent test

Let H be any group, with coefficients multiplied on the right as an oriented strand is traversed. A decorated color is (x,u) in X×H. Given maps f,g:X²→H, encode the classical and virtual crossings by

    Rhat((x,u),(y,v))
       = ((r_1(x,y),v), (r_2(x,y),u f(x,y))),

    Shat((x,u),(y,v))
       = ((s_1(x,y),v g(x,y)), (s_2(x,y),u g(x,y))).    (1)

At a classical crossing only the underpassing strand acquires f; at a virtual crossing both strands acquire the displayed g. This is the product convention described in Farinati–Garcia Galofre, Section 1.2 and Definition 20. It is not the scalar factor assigned to a whole tensor basis vector in Turn 4. Their Definition 9 supplies virtual 2-cocycle conditions; the examples below also have their virtual identities checked directly through (1).

Assume that (1) already gives a virtual-braid action and that the undecorated pair r,s is welded. A direct comparison of Shat_1 Rhat_2 Rhat_1 and Rhat_2 Rhat_1 Shat_2 shows that it descends to the welded group in the convention of the preceding turns if and only if both identities hold for all x,y,z:

    g(r_1(x,y), r_1(r_2(x,y),z)) = g(y,z),             (Wg)

    f(x,y) f(r_2(x,y),z)
      = f(x,s_1(y,z))
        f(r_2(x,s_1(y,z)),s_2(y,z)).                   (Wf)

To verify necessity, mark the three initial strands by u,v,w. In the left word, their final coefficient products are respectively f(x,y)f(r_2(x,y),z), g(r_1(x,y),r_1(r_2(x,y),z)), and that same g. In the right word they are the right side of (Wf), g(y,z),g(y,z). The undecorated outputs already agree. Taking the initial coefficients to be the identity gives necessity, and the same calculation gives sufficiency for arbitrary u,v,w. Adjacent copies then give all welded relations; disjoint pairs act on disjoint strands. No coefficient commutation was used in this derivation.

Thus satisfying virtual Reidemeister moves, by itself, is not enough to make a cocycle a welded invariant. The original source question concerns this additional quotient.

## 2. The primary general-second-component example

Use the published paper's **Example 25**, pp.536–537 (the arXiv draft numbers it differently). Let X=F_2, let h(x)=x+1, and set

    r(x,y)=(y,x),       s(x,y)=(h(y),h(x)),
    f(x,y)=a if x differs from y, and 1 otherwise,
    g(x,y)=1.                                         (2)

Here a is any element of a coefficient group H. The source presents its universal cyclic form with a of infinite order; this gives a virtual cocycle and a virtual linking-type invariant. The unweighted pair itself is welded: it belongs to the commuting-permutation family in Turn 1.

For the decorated action, however, (Wf) at x=y=z=0 is

    1 = a².                                           (3)

Consequently the infinite-cyclic virtual example does **not** descend to a welded representation in this convention. It cannot be used as a ready-made positive answer to Q1.

Conversely, a²=1 is sufficient. In (2), the left exponent in (Wf) is

    e=[x differs from y]+[x differs from z],

whereas the right exponent is 2−e. Their difference is one of −2,0,2. All other weighted virtual relations were valid already, and (Wg) is trivial. Hence (2) is welded precisely when a²=1. This holds inside any ambient group H; its coefficient image here remains cyclic and is not a genuinely nonabelian example merely because H may be nonabelian.

## 3. The surviving weights still transfer locally

The relevant twist-second pair and weights are

    R(x,y)=(h(y),h(x)),      t(x,y)=(y,x),
    f′(x,y)=a if x=y, and 1 otherwise,
    g′(x,y)=1.                                         (4)

The corresponding virtual cocycle is the published paper's Example 36. Its extra welded condition is again precisely a²=1, by (Wf).

For every strand number n, change only the colors by

    H_n((x_i,u_i))_i=(h^(i−1)(x_i),u_i)_i.             (5)

A direct adjacent-coordinate calculation conjugates the decorated (2) action to (4). The coefficient f in (2) is invariant under simultaneous h, and f(x,h(y)) equals f′(x,y), so no outside-coordinate weight remains. This conjugacy is valid as a virtual action for every a and as a welded action exactly for the surviving a²=1 subfamily.

Therefore this concrete general-s example, after the necessary welded quotient is imposed, still gives no obstruction to replacing s by twist. This is an exact result about the displayed cocycles, not a classification of all nonabelian cocycles on all welded pairs.

## 4. A genuinely noncommutative control survives welding

The same primary paper's Examples 11 and 35 give X={0,1}, r=s=twist, and coefficient group

    H=Free(a,b) × <z>,

where z commutes with a and b but a and b do not commute. The nonidentity weights are

    f(0,1)=a, f(1,0)=b,
    g(0,1)=z, g(1,0)=z^(-1),

with all diagonal weights equal to 1. These are credited published virtual cocycles.

They also satisfy the extra welded equations: (Wg) is tautological for two twists; (Wf) says that f(x,y) and f(x,z) commute for fixed x. On this two-color set each such row contains only 1 and one of a,b, so it holds without requiring ab=ba. The own checker retains reduced words in the free group and a separate central z exponent, verifying all virtual and welded identities without abelianizing a,b.

This control rules out the false extrapolation that the welded quotient necessarily kills all noncommutative information. It already has twist second component, so it does not answer whether a *general* s can provide something unavailable from a twist-second pair.

## Final outcome after five substantive turns

The manuscript now separates set actions, complex permutation modules, characteristic-three modules, scalar local cocycles, ordered nonabelian strand cocycles, and the virtual versus welded relation. It contains positive all-n subclasses, a genuine field-qualified unweighted counterexample, a complete finite scalar-weight classification, and a concrete virtual-to-welded descent calculation.

It does **not** decide the general source Q1 about the representation-theoretic relevance of arbitrary second components with admissible local cocycle weights. It also does **not** settle Q2 under an intended characteristic-zero linear-representation convention for every welded pair. The OWR contribution does not specify a coefficient field; the characteristic-three theorem is preserved as a conditional reading and scoped partial, not silently promoted to the complex question. No nonexistent set-action isomorphism, raw nonlocal gauge, or virtual-only example is claimed as a linear welded counterexample.

Proposed original-target status: **unsolved, 5/5**, pending independent review of all retained partials. Completion estimate25%. No sixth author search turn, novelty claim or outreach. Further advancement would require a general invariant or intertwiner theorem in a specified weighted category and a field-qualified resolution of the second question, not a change of categories after the fact.

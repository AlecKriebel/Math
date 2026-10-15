# Author turn 1: transport is not tensor locality

**Partial; both source questions remain unresolved.** 2026-10-01. This turn separates exact representation transport from the additional local-pair realization required by the source, and proves a commuting-permutation subclass of its second question.

## Conventions and the selected bundle

Use left actions and composition with the rightmost map applied first. Write r_i and s_i for adjacent-coordinate copies of bijections r,s:X²→X². A welded pair in the convention used here satisfies the braid relations for r and s, s_i²=1, the mixed relation

    s_1 r_2 s_1 = s_2 r_1 s_2,

and the welded relation

    s_1 r_2 r_1 = r_2 r_1 s_2.                         (1)

Disjoint-coordinate relations then hold automatically. These are the relations in Damiani's Proposition 3.14 and Bartholomew–Fenn's first forbidden move, after the same generator naming. The opposite forbidden move is not silently imposed. All solution examples below are bijective and nondegenerate.

Source Q1 concerns local 2-cocycle-enriched representations and does not fix a single coefficient/equivalence convention. Source Q2 separately concerns unweighted representations with the ordinary rack-derived first component r′. The announced violin reduction to r^(s) with twist second component is not Q2: r^(s) need not equal r′.

For a precise restricted version of Q1, take a commutative field K and scalar weights a,b:X²→K*. On K[X^n] put

    R_i e_x = a(x_i,x_(i+1)) e_(r_i x),
    S_i e_x = b(x_i,x_(i+1)) e_(s_i x).                (2)

Here the weight constraints mean exactly that the displayed matrices satisfy every welded relation. Knot Reidemeister-I normalization is an optional extra, not a braid relation. This scalar model does not exhaust the nonabelian strandwise cocycles in the source's reference to Farinati–Garcia Galofre.

## 1. Exact general transport lemma

Let a group G act on a set Y, and let c:G×Y→K* satisfy

    c(gh,x)=c(g,hx)c(h,x).

Then rho(g)e_x=c(g,x)e_(gx) is a representation. If H:Y→Y′ is an equivariant bijection, relabeling the basis by H conjugates it to

    rho′(g)e_y=c(g,H^(-1)y)e_(gy).                     (3)

The cocycle equation follows immediately by substituting H^(-1)(gy)=gH^(-1)y. Conversely each monomial representation with the specified underlying G-action gives such a cocycle by reading its coefficient at every basis vector. Thus arbitrary action-cocycle enrichments transport through any unweighted action isomorphism.

This is not a solution of Q1. If Y=X^n, the coefficient c(g_i,H^(-1)y) can depend on coordinates other than y_i,y_(i+1), or depend on i or n. A local pair realization by fixed a′,b′ requires the stronger condition that the coefficient for each generator type be one and the same function of those two coordinates, for every adjacent slot and every strand number. For a fixed underlying relabeling, this condition is both necessary and sufficient, by (2).

A diagonal change of basis e_y↦d_n(y)e_y changes the coefficient in (3) to

    d_n(gy)/d_n(y) * c(g,H^(-1)y).                     (4)

Therefore a failure of raw locality is only a failure of that chosen transport; it is not a counterexample allowing other gauges, other relabelings, or arbitrary linear isomorphisms. The source's distinction between a global action isomorphism and local cocycle invariants is genuine.

## 2. Where the missing conjugacy freedom lives

Fix any known intertwiner J_n between the classical B_n-actions induced by r and r′, for example a guitar map in a compatible convention. Let

    T_(i,n)=J_n s_i J_n^(-1).

All of these operators satisfy the required welded relations together with r′_i. They are not thereby known to be adjacent copies of a single q:X²→X².

Any other set bijection H_n conjugating r_i to r′_i has the form H_n=C_n J_n, where C_n commutes with all r′_i. This follows by multiplying the two intertwining identities; the converse is immediate. Accordingly Q2, in the set-action category, is equivalent to finding one involutive local solution q and, for each n, such a classical-action centralizer C_n with

    C_n T_(i,n) C_n^(-1) = q_i   for every i.           (5)

Equation (5) identifies the precise gap. Showing that a particular guitar map produces a nonlocal T does not exclude some other C_n and q. Conversely allowing arbitrary T_(i,n) simply restates the known classical conjugacy and drops the local-pair requirement.

This criterion is a reduction, not a claim that the resulting centralizer problem is easier or solved. General linear representation isomorphisms have still more freedom than these set bijections.

## 3. An affirmative commuting-permutation subclass of Q2

Let f,g,h be pairwise commuting permutations of an arbitrary set X. Put

    r(x,y)=(f(y),g(x)),
    s(x,y)=(h(y),h^(-1)(x)).                            (6)

Both are nondegenerate YBE solutions, s is involutive, and the pair is welded. These assertions follow by applying each length-three word in (1) and the two braid relations to (x,y,z); the only rearrangements needed are the stated commutations. No finiteness hypothesis is used.

In the rack-type convention r′(x,y)=(y,x*y), the derived rack is

    x*y=f g(x),       r′(x,y)=(y,f g(x)).               (7)

For a direct identification, conjugate r on X² by J_2(x,y)=(x,f(y)). It yields exactly (7), as does the usual left-action version of the derived-rack formula. The rack operation is self-distributive because it is the constant-action rack of the permutation f g.

For all n define

    J_n(x_1,...,x_n)=(x_1,f(x_2),...,f^(n−1)(x_n)).    (8)

At adjacent slots i,i+1, a direct calculation gives

    J_n r_i J_n^(-1) = r′_i,
    J_n s_i J_n^(-1) = q_i,
    q(x,y)=(h f^(-1)(y), f h^(-1)(x)).                (9)

All outside coordinates are unchanged, and the formula does not depend on i or n. Thus (X,r′,q) is a welded pair, and (8) gives an isomorphism of all the unweighted welded-braid actions and their linearizations. Its relation identities can either be checked directly using commutations or obtained by conjugating the original ones in X³. The finite checker exercises the direct identities as well as the conjugacy.

This settles Q2 for this explicit subclass, including arbitrary cardinality and non-involutive r. It does not handle general nonconstant translation actions.

## 4. A corresponding weighted sufficient condition

The same commuting family has a simple violin-type relabeling

    H_n(x_1,...,x_n)=(x_1,h(x_2),...,h^(n−1)(x_n)).

It sends s_i to the ordinary twist and r_i to copies of

    R(x,y)=(f h^(-1)(y), h g(x)).                      (10)

Suppose the scalar weights in (2) already satisfy the welded relations and are invariant under simultaneous application of h:

    a(hx,hy)=a(x,y),   b(hx,hy)=b(x,y).                (11)

Then the transported coefficients are local and slot-independent:

    a′(x,y)=a(x,h^(-1)y),    b′(x,y)=b(x,h^(-1)y).     (12)

Indeed H_n^(-1) presents the two input colors as h^(-(i−1))x and h^(-i)y, and (11) removes the common power. Hence these weighted representations also arise from the twist-second pair (X,R,flip), with the transferred weights. Relation validity follows by conjugation and does not have to be assumed again for (12).

Condition (11) is sufficient, not asserted necessary or implied by the welded cocycle equations. For arbitrary weights or the source's nonabelian strandwise cocycles, this conclusion has not been proved. In particular the existence of a convenient subclass cannot answer the existential relevance question Q1.

## Outcome

The transported-representation route has an exact locality/gauge gap. Q2 has a complete affirmative proof for commuting permutation solutions, and Q1 has a restricted sufficient condition under which s remains dispensable. Neither supplies a proof or counterexample for the full two-question source bundle.

Substantive author turns: 1/5. Estimated completion toward the full target: 15%. Next mechanisms should test genuine nonlocal welded pairs and invariants under *all* admissible intertwining choices, rather than mistake one failed guitar gauge for a counterexample. Published guitar/violin frameworks and permutation solutions are credited; no novelty claim is made.

# Attempt 1 of 5: delete non-rainbow signatures and try to force a proper core

## Target and conventions

For a coloring chi:E(K_n)->[q], call a triangle's type its multiset of three actual edge colors. Every permutation of the three triangle edges comes from a vertex permutation, so two triangles are color-isomorphic exactly when their types agree. The question forbids vertex-disjoint triangles of equal type, including monochromatic and two-color triangles. Properness is not assumed.

The attempted route is to discard a small exceptional vertex set and apply the elementary q-color lower bound to a proper induced clique.

## A fully proved quadratic obstruction

There are exactly q^2 possible non-rainbow types: q monochromatic types {a,a,a} and q(q-1) types {a,a,b} with a!=b. For every realized non-rainbow type choose one triangle, and let S be the union of all chosen vertices. Then |S|<=3q^2.

Every triangle of K_n-S is rainbow. Otherwise its type has a chosen representative in S, producing disjoint color-isomorphic triangles. Every two incident edges in K_n-S therefore have different colors: if xy and xz shared a color, xyz would not be rainbow. Consequently, if m=n-|S|>=2, then m-1<=q. The conclusion also holds when m<=1. Thus

    n <= 3q^2+q+1,
    g(n) >= ceil((sqrt(12n-11)-1)/6).

This is an elementary independent proof of the baseline square-root order, not an improvement on the stronger lower bound announced in the 2026 report.

## Why the proposed linear upgrade does not follow

A tempting claim is that one can choose the representatives so their union has O(q) vertices. Nothing above gives this: the q(q-1) different ordered repeated/singleton-color pairs must not be silently collapsed to q colors. The forbidden pairs only constrain triangles of the same complete type. Two triangles with the same repeated color a and different third colors b,c may be disjoint.

A genuine sufficient missing theorem is: every admissible q-coloring has a vertex set S of size at most Cq meeting all non-rainbow triangles. If proved, the same argument gives n<=(C+1)q+1. This is a conditional reduction, not an established transversal bound. Proper-coloring theorems are inapplicable before this step.

## Check of the standard upper construction

Start from a monochromatic K_5. Add the other n-5 vertices one at a time. At each addition, give every edge from the new vertex to previous vertices a fresh private color. A triangle outside the initial K_5 has a unique latest-added vertex, and its two edges to earlier vertices have that vertex's private color. The remaining edge has an earlier color, so the repeated color identifies this common vertex in every triangle of the same type. Such triangles cannot be vertex-disjoint. Monochromatic triangles are confined to the five-vertex core. Therefore g(n)<=1+(n-5)=n-4 for every n>=5.

More generally, g(m+t)<=g(m)+t for any admissible seed on m vertices and t>=0. Improving a fixed seed only changes the constant deficit; it does not by itself disprove either asymptotic conjecture.

## Verdict

No resolution. The proper-core deletion proof yields a rigorous baseline bound and pinpoints the missing O(q) transversal estimate. The standard n-4 upper bound is certified with its n>=5 domain. This substantive proof attempt counts as 1/5; source retrieval and literature review did not count.

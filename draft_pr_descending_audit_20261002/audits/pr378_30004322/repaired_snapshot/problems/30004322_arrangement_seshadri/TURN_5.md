# Turn 5: an infinite weighted Fermat subfamily

Fifth and final substantive author turn. Original conjecture remains unresolved. This is an explicit infinite class of reduced complex line arrangements, with an exact Seshadri value and an optimal fractional cover by its own components. Full Fermat values and the general Bézout method are credited to Pokora, Example 3.4 following Proposition 3.3 (https://arxiv.org/pdf/1711.09364v3). No historical novelty is certified.

## 1. Construction and exact incidence

Let q be any positive integer, n=5q, and ζ a primitive n-th root of unity. Start with the three Fermat pencils

    A_a: x=ζ^a y, B_b: y=ζ^b z, C_c: z=ζ^c x,

where indices belong to Z/nZ. Retain in each pencil exactly the indices whose residue modulo 5 belongs to R={0,2,3}. There are 3q retained lines per pencil and 9q distinct lines in total. Let Z be the full singular set of this subarrangement.

Grid intersections are indexed by (a,b,c) with a+b+c=0 in Z/nZ. Their incidence with the retained arrangement is exactly the number of retained indices. The residue triples with three retained indices are 000 and the six permutations of 023. Those with exactly two retained indices are the three permutations of 221 and the three permutations of 334. Each fixed residue triple summing to zero modulo 5 has q² lifts summing to zero modulo n: choose the first two indices arbitrarily in their q-element residue classes, and the third is uniquely determined.

Thus Z has 7q² triple grid points, 6q² double grid points, and three coordinate vertices of multiplicity 3q. In particular

    |Z|=13q²+3.                                           (1)

There are no other intersection points. Every pair of lines in one pencil meets at its coordinate vertex; every pair in different pencils belongs to a unique grid triple. All three centers remain singular, including q=1.

A retained line of residue 0 loses exactly 2q original grid points: the two other indices must have residues 1,4 or 4,1 for both lines to be deleted. A retained line of residue 2 loses q grid points (other residues 4,4); a line of residue 3 loses q (other residues 1,1). Including its center, their respective numbers of singular points are

    3q+1 for residue 0, and 4q+1 for residues 2 or 3.       (2)

These are exact cyclic-incidence counts, with no general-position assumption.

## 2. Weighted cover and the Seshadri constant

Give each retained residue-0 line weight 1/3, and each retained residue-2 or residue-3 line weight 1/2. The total weight is

    τ=3(q/3+2q/2)=4q.                                    (3)

At a 000 grid point the coverage is 1. At a 023 triple point it is 4/3. At a double point of type 221 or 334 the two retained lines each contribute 1/2, giving coverage 1. At each coordinate vertex the coverage is 4q/3≥1. Hence this is a fractional cover of every point of Z.

For any integral curve C other than a retained component, weighted Bézout gives

    4q deg(C) ≥ Σ_{p∈Z} mult_p(C).

Indeed each line not equal to C has intersection multiplicity at p at least mult_p(C), and the sum of its weights through p is at least one. Thus every such curve meeting Z has Seshadri ratio at least 1/(4q). This includes every auxiliary projective line; consequently an auxiliary line contains at most 4q points of Z. By (2), retained residue-2 or residue-3 lines contain 4q+1 points. Therefore, with the source's maximum taken over ALL projective lines,

    mpl(Z)=4q+1,       ε(P²,O(1);Z)=1/(4q+1).             (4)

The curves computing this constant are exactly the 6q retained lines of residue 2 or 3. Residue-0 components have smaller point count, and every noncomponent curve has the strict larger lower bound 1/(4q).

This is an all-degree conclusion. The finite computations below support the incidence proof; no bounded search substitutes for Bézout.

## 3. Exact optimality within the component-cover problem

Assign dual point weights as follows: weight 1/q to every 000 grid point, weight 1/(2q) to every double grid point, and zero to all 023 grid points and coordinate vertices. Their total is

    q²/q + 6q²/(2q)=4q.                                  (5)

A retained residue-0 line contains q of the 000 points and no double points, so its total dual weight is 1. A retained residue-2 or residue-3 line contains no 000 points and exactly 2q double points, so its total dual weight is again 1. The latter count follows by placing the other retained index in either of the two remaining pencils: its residue must equal that of the fixed line, with q choices in each case. The third index is deleted.

For any nonnegative component weights covering Z, interchange the finite line/point sums. The weighted coverage inequalities, multiplied by the dual point weights, give total component weight at least 4q. Together with (3), this proves the arrangement-component fractional-cover optimum is exactly 4q. This does not assert optimality when arbitrary auxiliary lines are allowed; their dual constraints have not all been checked.

Uniform weight 1/2 on all 9q components costs 9q/2, strictly worse. For q≥3 this uniform cost exceeds mpl(Z)=4q+1, so the nonuniform certificate succeeds where the simple uniform-half-weight sufficient test does not certify the value. This is a limitation of that test, not a counterexample to the source conjecture.

## 4. Relation to turn 4 and final scope

The full 15q-line Fermat arrangement has the credited value 1/(5q+1). This subfamily deletes 6q lines and changes the exact value to 1/(4q+1). Thus the sufficient small-deletion inheritance criteria in turn 4 cannot simply be extended to all deletions. The new value still agrees with the original line-arrangement conjecture.

The checker enumerates the cyclic incidence exactly for q=1,...,30, verifies every primal and dual constraint, the point and line counts, and the pair-incidence identity. It uses rational arithmetic only. These finite controls are not an assertion that arbitrary arrangements have been classified. The complete five-turn packet leaves the original unrestricted conjecture unresolved, with no sixth author search.

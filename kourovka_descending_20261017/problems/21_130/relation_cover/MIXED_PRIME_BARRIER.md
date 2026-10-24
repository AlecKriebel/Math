# A seven-point obstruction to primary collision-preserving modeling

This is a method obstruction, not a counterexample to21.130 and not a novelty claim.

Take A={0,1,2,3,4,7,9} in the additive cyclic group C15. Suppose a map f:A→P into an abelian p-group preserves every equality of sums of two distinct elements of A. Translating f by f(0), assume f(0)=0. Write t=f(1). The following equations all involve four distinct vertices:

- 0+3=1+2 and 0+4=1+3 give f(3)=t+f(2), f(4)=2t+f(2).
- 1+4=2+3 then gives f(2)=2t, hence f(3)=3t and f(4)=4t.
- 0+7=3+4 gives f(7)=7t.
- 0+9=2+7 gives f(9)=9t.
- 7+9=0+1 in C15 gives 15t=0.

If p=3, multiplication by5 is invertible on P, so3t=0 and f(3)=f(0). If p=5, multiplication by3 is invertible, so5t=0 and f(9)=f(4). For every other p, multiplication by15 is invertible, so t=0 and all vertices have the same image. Thus no such map is injective for any p. In particular, even a theorem for all subsets of all finite abelian p-groups cannot automatically settle the mixed-prime case by an injective map preserving the collision relations.

The actual subset has the rainbow cycle (0,1,2,3,7,4,9), with successive sums (1,3,5,10,11,13,9) modulo15. Therefore the failed reduction does not imply failure of the original conjecture.

The argument requires only preservation of the displayed disjoint-edge collisions, rather than all possible Freiman relations or a group homomorphism. It is consequently an obstruction to the specific primary-model reduction used in the algebraic route, with its exact hypothesis stated.

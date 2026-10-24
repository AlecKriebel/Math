# Exact scl of the P4 disk-promotion countermodel

Prepared October 24, 2026 UTC. This is an exact value for one chain in a previously tractable subclass, used to certify a mechanism obstruction. It is not a solution of 21.127 or an originality claim.

Use G=<a,b,c,d | [a,b]=[b,c]=[c,d]=1>, and the real chain

    C=[ab,d]+[d,a].

Then

    scl_G(C)=1.

**Upper bound.** The explicit graph-of-tori construction in `FIXED_GRAPH_FLOW.md` gives a four-holed sphere with two outer boundary labels [ab,d], [d,a], and two retained interior boundary labels freely homotopic to b and b^{-1}. Those last two boundary components can be joined by an annulus mapped to the b-circle. The surface stays connected, retains Euler characteristic -2, and has two boundary components, so its genus is 1. It is admissible for C with degree 1 on each of its two prescribed loops. The chain surface formula gives scl_G(C)<=(-chi)/2=1. No nonzero homology is capped by a disk: the two opposite inner boundaries are paired by an actual annulus.

**Lower bound.** Define a homomorphism to the free group F(x,y) by

    a -> x, b -> x^{-2}, c -> 1, d -> y.

The three defining commutation relations are respected. Write h=[x,y]. The images of the two chain terms are

    [x^{-1},y] = x^{-1} h^{-1} x,
    [y,x] = h^{-1}.

Thus the image chain is 2h^{-1} in the homogeneous chain space B_1^H(F(x,y)), where conjugate elements represent the same chain class. Homogeneity, inversion symmetry, and the established free-commutator value scl(h)=1/2 give scl(2h^{-1})=1. Monotonicity under the displayed homomorphism gives scl_G(C)>=1, proving equality.

This confirms that indiscriminate promotion of the separately adjustable pieces in that fixed graph would miss an actual positive scl cost of 1. The matching formula correctly retains two persistent exceptional pieces per degree. It does not prove that every graph of pieces for every word admits a finite encoding.

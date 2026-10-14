# Author turn2: odd-side restrictions and all complex character zeros

**Partial necessary conditions, not a tiling theorem.** 2026-10-01.

The grid reduction in turn1 permits exact lattice colorings for every allowed congruent rectangular tiling. Throughout, W,H are positive integer target dimensions, all eight D4 orientations are allowed, and P is the verified corner-cut tile.

## 1. Stripe restrictions on an odd tiling

Color a cell(x,y) with (-1)^y. The three rows of P have lengths4,4,6, so one horizontal tile has signed sum6; an integer translation can change its sign. Its x-stripe sum is0 because each row has even length. For a quarter-turned tile the two conclusions interchange. Thus every tile whose length-six direction is horizontal contributes either+6 or-6 to y-stripes and0 to x-stripes; a vertical tile contributes0 and either+6 or-6 respectively.

If the number N of tiles is odd, WH=14N has exactly one factor2. Hence exactly one side is odd, and the other is2 modulo4. Suppose H is odd and W is even. The rectangle's y-stripe sum is W and its x-stripe sum is0. Consequently6 divides W. Moreover the signed count of horizontal tiles is W/6 and the signed count of vertical tiles is0. The vertical tile count is even; the horizontal count is odd. Combining with W=2 modulo4 gives

    W=6k with k odd; H odd; 7 divides kH; N=3(kH/7).

In particular **every odd rectangular tiling would use N congruent to3 modulo6 tiles**, and its even side would be6 modulo12. If W is the odd side, interchange W and H. These conditions do not rule out all possibilities.

## 2. Complete classification for multiplicative complex colorings

Let S_m(t)=1+t+...+t^(m-1). The exact tile polynomial is

    p(x,y)=S_4(x)S_3(y)+x^4(1+x)y^2
          =(1+x)[(1+x^2)S_3(y)+x^4 y^2].

A nonzero complex pair(x,y) defines the cell character x^i y^j. A character annihilates every translated, rotated and reflected tile precisely when all eight oriented tile polynomials vanish. Translations only multiply by a nonzero monomial.

**Claim.** The common zero set in(C*)² is exactly

    {(-1,z): z^6=1, z≠1} union {(z,-1): z^6=1, z≠1}.      (1)

It has nine points, since(-1,-1) lies in both sets.

Proof. Compare p(x,y) with its vertical reflection y²p(x,y^-1). Their difference is x^4(1+x)(y²-1). Thus at a common zero, either x=-1 or y=±1.

If x=-1, the quarter-turned polynomial p(y,-1)=S_6(y) must vanish, so y is a nontrivial sixth root of unity. If x≠-1 and y=-1, p(x,-1)=S_6(x), giving the symmetric family.

The remaining case is x≠-1,y=1. Dividing the polynomial and its horizontal reflection by1+x gives the two equations

    x^4+3x²+3=0,       3x^4+3x²+1=0.

Their difference forces x^4=1, and the first then forces x²=-4/3, a contradiction. There are no further common zeros.

Conversely, at x=-1 every horizontal reflection/orientation has the factor1+x; every quarter-turned orientation reduces, up to a nonzero monomial, to S_6(y), which vanishes at the listed roots. The other family is symmetric. This checks all eight orientations, not just translations. QED.

## 3. Exact reach and limitation of these colorings

The rectangle polynomial is S_W(x)S_H(y). Vanishing at every point of(1) is equivalent to

    both W,H even, or
    W odd and6 divides H, or
    H odd and6 divides W.                                 (2)

Indeed S_m(-1)=0 exactly for even m. If W is odd, the first family in(1) requires S_H(z)=0 for every nontrivial sixth root, equivalent to6|H; the other case is symmetric. Both odd sides cannot pass the test.

Thus the stripe condition is exactly the obstruction furnished by **all single multiplicative complex characters that annihilate every allowed tile**. Once an odd rectangle has its even side divisible by6, these particular characters give no further restriction. This is not a completeness result for all additive invariants: integral/modular colorings, derivative or polynomial methods, boundary words and geometric packing restrictions are not classified here. Neither(2) nor the area condition is sufficient for a positive tiling.

For example6×7 passes the character and area conditions and would require3 tiles; no positive tiling is inferred. The independent finite checks verify oriented polynomial identities modulo the cyclotomic polynomials and the dimension test. The proof of the complete nonzero complex zero classification is the preceding algebra, not a sampled numerical root search.

## Remaining route

An odd solution must occur among a much narrower set of dimensions and counts, but infinitely many candidates remain. The next attempts will test a finite-width exhaustive search and a boundary/periodic construction route. Any negative finite search will remain bounded, and any torus or signed certificate will remain distinct from the required positive rectangle.

Substantive author turns:2/5. Estimated completion25%. Original unresolved; no novelty claim.

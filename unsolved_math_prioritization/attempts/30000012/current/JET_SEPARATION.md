# Finite incidence does not give initial-data separation

## Compact projective test family

Fix a line Y⊂P³. Let S₀ be the projective bundle over the dual P³ whose fibre over a plane H is the P⁵ of nonzero quadratic forms on H, up to scalar. It carries the family of plane conic cycles. The space S₀ is smooth, compact and eight-dimensional, and the family covers P³. Replace S₀ by the normalization S of its image in the cycle space. This removes redundant descriptions of degenerate conics; it is an isomorphism over the open locus of smooth conics, so dim S=8.

For H not containing Y, set y(H)=H∩Y. The condition that a conic in H contain y(H) is one nonzero linear condition on its quadratic equation. Thus the main incidence component C has dimension 3+4=7. Its general member is smooth and intersects Y at exactly one point. Because H is transverse to Y, the conic is not tangent to Y. Planes containing Y form a one-dimensional subset of the plane parameter space; conics in such planes contribute dimension six and lie in the closure of the main incidence component. Indeed, choose an intersection point with Y and deform H through that point while deforming the conic equation. There is no further incidence component of dimension seven.

The order-zero data of a general incident conic are its point in Y, a one-dimensional target. The first-order normal data are that point and a line in the two-dimensional normal fibre, a two-dimensional target. For a smooth conic the tangent cone gives the same first-order data. Consequently their generic fibres on C have dimensions at least six and five, respectively. None of these maps is generically finite.

Here N_{Y/P³}=O(1)⊕O(1), so the original positivity hypothesis holds. This refutes automatic initial-data separation even when incidence is generically finite and non-tangential. It does not refute the dimension bound: P³ is projective.

## A higher-jet lemma

Let U be a connected complex manifold of dimension d and let a_j∈O(U), j∈N, be a countable collection that jointly separates points. Then some finite subcollection has differential of rank d on a nonempty open subset.

Proof. Let r be the largest rank attained by any finite subcollection, and choose a finite map A of rank r at a point. After shrinking, A has constant rank r. For each j, the map (A,a_j) has rank at most r, so da_j vanishes on the tangent spaces of A's local fibres. Each a_j is therefore constant on a connected local fibre. If r<d, such a fibre contains distinct points, contrary to joint separation. Hence r=d. For the selected finite map, its d-th exterior differential is a holomorphic section that is nonzero somewhere, so its zero set has empty interior on connected U. Thus its full-rank locus is open and dense. ∎

Apply this to the Taylor coefficients of an analytically varying local graph, including the coordinates of its centre. If its complete graph germ determines the parameter, finitely many coefficients give generic local separation. For distinct reduced irreducible global cycles, equality of a nonempty open germ forces equality of the cycles. This explains why higher jets can recover parameters missed by tangent data, whenever such a graph chart and effective local parameterization are available. The conclusion is generic local separation. It does not assert that a map on an arbitrary noncompact chart has globally finite fibres, nor that the coefficient functions extend meromorphically to the compact parameter space.

## Why this does not complete the global argument

Take Y={(0,0,z)}⊂C³ and the local curves

    X_(a,b,c): (x,y,z)=(u, a+b u², c).

Incidence is a=0. Its point is (0,0,c) and its tangent direction is (1,0,0); both forget b. The second derivative of y recovers 2b. For the normal-plane equation P=y−a−b x², the formal expansion

    log(P/P(0,0)) = log(1−y/a+b x²/a)

has x² coefficient b/a and y² coefficient −1/(2a²). Thus the shape parameter first appears below the maximum pole order available at that homogeneous degree. A finite-jet separation statement alone gives no global sections whose pole orders and cancellations preserve this lower-order information. Constructing such globally controlled sections is the missing step in this route.

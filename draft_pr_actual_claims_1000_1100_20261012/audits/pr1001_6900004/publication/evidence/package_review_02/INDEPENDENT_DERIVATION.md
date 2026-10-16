# Independent derivation before consulting prior review verdicts

The reviewed quantifiers are positive n,d, simple graphs on one fixed labelled vertex set, all placements in X=(R^d)^n, and connected components of fibre-homeomorphism equivalence preserving every coordinate sign including zero. Literal equality of partitions is the comparison. No relabelling, ambient homeomorphism or quotient is silently inserted.

## Present-edge direction

For edge e=ij the coordinate vector u_e, with a positive e coordinate and every other coordinate zero, is a stress iff the two endpoint force vectors are zero, iff p_i=p_j. If a fibre homeomorphism preserves signs, the image of u_e has positive e coordinate and zero elsewhere, and therefore is another nonzero scalar multiple of u_e. This support exists in the target iff its e endpoints coincide. Surjectivity gives the converse. Thus the diagonal Delta_ij is invariant under the whole equivalence relation. Its decomposition into equivalence classes induces a union of their connected components. No continuity of stress-space assignment in P is needed for this direction.

## Missing-edge direction

Choose a nonzero vector a, place i=t a and j=0, and every other labelled k at (k+1)a. The range [-1/2,1/2] separates all vertices other than i,j. Since ij is absent, every graph edge remains noncollapsed throughout the path. With any orientation, the equilibrium operator for these collinear points is the tensor injection of the scalar operator B D_t with a, where B has opposite incidence signs and D_t contains oriented lengths. Nonzero a makes this tensor injection faithful. Therefore the stress kernel is exactly ker(B D_t). Each length remains nonzero with constant sign. T_t=D_t^{-1}D_0 is diagonal, invertible, coordinatewise positive and satisfies B D_t T_t=B D_0. Its inverse is D_0^{-1}D_t. These are genuine linear homeomorphisms and preserve positive, negative AND zero signs.

Every placement on the continuous path is therefore equivalent to its placement at t=0. The entire path lies in the same equivalence class, rather than merely having equivalent endpoints. The continuous image of a connected interval is connected in that equivalence class's subspace topology. Any connected subset lies in a single connected component; hence the path is contained in one stratum. At t=0 it meets Delta_ij; at t=1/4 it does not. Thus Delta_ij cannot be a union of complete strata. No path connectedness of all strata is being assumed.

Identical partitions have exactly the same collision diagonals which are unions of pieces, so the two directions recover each edge. The converse for equal edge sets is immediate. This is not a comparison of stress coordinate spaces of two different graphs.

## Boundary audit

For n=1 there is only the empty simple graph. For the edgeless graph the stress fibre is the zero vector space, X is connected, and for n>=2,d>=1 each collision diagonal is proper, so it is not a union of the sole whole-X stratum. For n=2 the missing-edge construction needs no other points and works directly. Isolated vertices impose zero equations, causing no obstruction. Full collision, deficient affine span, self intersections, disconnected graphs and dense cyclic graphs are retained. Dimension d=1 uses the same argument. Dimension d=0 must be excluded: X is a singleton and every graph has the same partition. The selected witness line is a subset of the full space; it does not restrict the whole partition. Parallel edges and loops lie outside the stated simple-graph quantifiers.

Equal nullity is insufficient: K3 on a line with exactly one collided pair has nullity one, as does a distinct placement, but the collided fibre supports that pair's singleton whereas the separated fibre does not. The written proof uses this support, not any nullity assertion in a source example.

## Ambient-equivalence boundary

For a forest, remove a leaf. If its edge is noncollapsed, leaf equilibrium sets its weight to zero; if collapsed its weight is arbitrary but exerts no force at either endpoint. Repeating gives precisely the coordinate subspace spanned by the collapsed edges. Sign-preserving equivalence classes are therefore exactly equal collapsed-edge subsets.

For path G=12,23,34 and star H=12,13,14, q1=p1, q2=p2, q3=p1+p3-p2, q4=p1+p4-p3 gives q2-q1=p2-p1, q3-q1=p3-p2 and q4-q1=p4-p3. The inverse is p1=q1, p2=q2, p3=q1*(-1)+q2+q3 and p4=-2q1+q2+q3+q4. It is a homeomorphism of X in every positive d. Collapsed-edge subsets correspond exactly, so whole equivalence classes and, by a homeomorphism's preservation of connectedness and its inverse, their connected components correspond. Path and star have distinct degree multisets. This verifies that arbitrary ambient comparison admits nonisomorphic graphs even though literal equality is rigid.

## Preliminary conclusion

No gap in the universal mathematical theorem or path/star example is found. Whether this scoped literal equality theorem matches an unwritten intended comparison is a separate source issue and must not be claimed from this proof. The package explicitly retains this limitation.

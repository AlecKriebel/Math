# Turn3: all dimensions with a laminar upper-constraint representation

AI-assisted proof candidate, independent review pending. Original unresolved3/5. This uses the classical balanced-sign property of laminar set systems, proved directly below; no novelty claim is made.

## 1. Class and statement

Let L be a laminar family of subsets of V: any two members are disjoint or one contains the other. Suppose

B={x in[-1,1]^V: x(V)=0, x(S)<=k_S for S in L},

where every k_S is a nonnegative integer. Then B has a vector v such that v and−v are both vertices. Thus the original conjecture holds for base polyhedra admitting this representation. The proof in fact does not need the additional base-polyhedron assumption for this class.

Nonnegative bounds ensure0 is feasible. No bound is assumed strictly positive; zero constraints and odd-cardinality blocks are handled explicitly. Coordinate bounds are the cube's. This does not assert that every base polyhedron has a laminar representation: greedy tight-set chains are local descriptions of a vertex, not globally sufficient inequalities.

## 2. Zero-bound atoms

Adjoin V as a zero set and let Z consist of V and the members S of L with k_S=0. For each Z in this laminar family, let its children be the maximal proper zero subsets it contains, and define its residual atom

R_Z=Z minus the union of its zero children.

Ignore empty residual atoms. These atoms partition V. Imposing x(Z)=0 for all zero sets is equivalent to imposing x(R_Z)=0 for every residual atom, by subtracting child sums and proceeding up the inclusion tree.

For a positive-bound set S, let Z be its smallest zero ancestor (V exists). Every proper zero descendant which meets S is either inside S or contains S, by laminarity; minimality of Z excludes the latter for maximal zero children. Thus S consists of its residual portion S intersect R_Z plus whole zero children and possibly their nested contents. On the zero-equality face,

x(S)=x(S intersect R_Z).

Restrictions of the positive sets to each residual atom form a laminar family there.

## 3. Balanced signs inside each atom

**Lemma.** For a laminar family on a finite set R, there is a vector v in{−1,0,1}^R with v(R)=0, at most one zero coordinate, and |v(A)|<=1 for every set A in the family. If |R| is even there are no zeros; if odd there is exactly one.

Proof. Add R and all singleton sets, and use the inclusion tree. At each node pair the unpaired leaves returned by its children, arbitrarily, passing at most one unmatched leaf upward. Every leaf is eventually in one pair except for possibly a single unmatched leaf at the root. Assign the two members of every pair opposite signs; assign0 to the root's unmatched leaf, if it exists. For any node, pairs wholly within it cancel, and at most one of its leaves was passed upward to be paired outside or made zero. Hence its signed sum has absolute value at most1. All root pairs cancel and its remaining leaf has value0. This proves the lemma in both parity cases.

Apply this lemma independently in every residual atom. The resulting global vector v satisfies all zero equalities. Every positive-bound set has signed sum between−1 and1 by Section2, and k_S>=1. Hence both v and−v satisfy every upper inequality and both belong to B.

## 4. Both feasible vectors are actual vertices

At v, every nonzero coordinate saturates a cube bound and is fixed in any face containing v. Every residual atom has at most one zero coordinate. Its total is fixed at0 by the zero-set face equations, so any such remaining coordinate is uniquely fixed as well. Thus the active cube bounds together with zero-set equalities determine v uniquely; v is a vertex of B.

The same reasoning applies to−v: the same zero coordinates remain, the signs of saturated cube bounds are exchanged, and the zero equalities still hold. Therefore−v is a vertex too. This proves the all-dimensional theorem without confusing feasible opposite points with opposite vertices.

The method includes arbitrary nested zero bounds and does not require0 to lie in the relative interior of B. It is algorithmic once the laminar family is given: the tree pairing is linear in the explicit tree size. No claim is made that one can find a laminar representation of an arbitrary base polyhedron or that this class exhausts the conjecture.

## 5. Exact controls

The standard-library checker generates nested/disjoint families with arbitrary zero versus positive integer bounds, constructs the residual atoms and pairing, checks both feasibility and the active-constraint full-rank vertex certificate using exact rational elimination. It includes odd atoms, empty residuals, nested zeros and singleton cases. These finite cases supplement the all-dimensional proof.

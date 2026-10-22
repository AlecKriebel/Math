# Turn 3: singular-nerve operations which cannot improve the ratio

## Direction and outcome

After excluding closed-manifold nerves, we test common operations that produce more singular or higher-dimensional nerves. Clique inflation, coning and clique-sums preserve the relevant coefficient bounds exactly or by a maximum. Joins do not improve the ratio and, when both factors are infinite, fail the hyperbolicity condition. This rules out an entire construction class but leaves general singular flag-no-square nerves open.

We use the credited punctured-nerve formula from turn2. The multiplicity operation below is related to the graph-product viewpoint in Cashen–Dani–Schreve–Stark, Section3; the explicit all-puncture argument is supplied here without a novelty claim.

## 1. Clique inflation preserves every puncture profile

Let L be a finite flag complex with vertex set V. Replace each vertex v by a nonempty finite clique F_v of m_v vertices. Between two different fibers include all edges exactly when their base vertices are adjacent in L. Call the resulting flag complex L[m]. Thus a simplex is any nonempty subset of the union of fibers above a simplex of L.

Let sigma' be a simplex of L[m], including the empty simplex, and define

    A={v in V: the whole fiber F_v is contained in sigma'}.

A is a simplex of L, possibly empty, because it is contained in the projection of sigma'. The induced vertex-deleted complex L[m] minus sigma' is itself an inflation of the induced complex L minus A, with every surviving fiber nonempty. Its projection onto L minus A is a homotopy equivalence. To prove this explicitly, choose one surviving vertex in every fiber to define a simplicial section. The projection followed by this section is contiguous to the identity: a face and its selected representatives together still lie over the same base simplex and form a face. Linear interpolation inside that face gives a homotopy. The opposite composition is the identity on the base.

Conversely every simplex A of L is obtained by taking sigma' to be the union of its whole fibers. Therefore the two collections of punctured nerves, although with repetitions, have exactly the same homotopy types. In particular for every coefficient ring R their reduced-cohomology nonvanishing profiles agree. Applying the punctured-nerve formula gives

    vcd_Z(W_{L[m]})=vcd_Z(W_L),
    vcd_Q(W_{L[m]})=vcd_Q(W_L).                (1)

This proof retains the partial-fiber deletions: a fiber is removed from the base only when all its vertices are deleted. Merely projecting sigma' itself would give the wrong puncture.

Clique inflation also preserves the no-induced-square condition in both directions. An induced square in L lifts by choosing representatives. Conversely an induced square upstairs cannot use two vertices in one fiber. Opposite vertices cannot share a fiber because they would be adjacent. Adjacent vertices cannot share a fiber because their identical adjacency to other fibers would create a diagonal. Its four distinct projections therefore form an induced square in L. Thus inflation preserves hyperbolicity of the associated right-angled Coxeter groups, but cannot alter their rational/integral ratio.

This explains why changing multiplicities to increase conformal dimension, as in the recent literature, is not by itself a route to the source's coefficient-ratio target.

## 2. Coning raises nerve dimension but not group dimension

Let CL=L*{a} be the cone. In a puncture that does not delete a, the remaining complex is again a cone and has no reduced cohomology. A puncture that deletes a together with a base simplex tau leaves exactly the base puncture L minus tau. Hence both maxima in the punctured-nerve formula are unchanged. Equivalently W_CL=W_L×C2, so its torsion-free finite-index dimensions are unchanged.

A cone adds no induced square, since the apex is adjacent to every other vertex. Repeated cones can make arbitrarily high-dimensional singular or contractible nerves while leaving both group dimensions unchanged. In particular the dimension of a nerve or its lack of global cohomology is not an adequate proxy for vcd.

## 3. Clique-sums use a maximum, not an accumulating torsion gain

Suppose L=L_1 union L_2, where each L_i is full, their intersection K is a simplex (the empty simplex is allowed), and there are no edges between the vertices outside K on different sides. Assume first that both sides have vertices outside K. Every simplex sigma of L lies on one side. For every puncture, its pieces are the corresponding punctures of the L_i and their intersection is the simplex on the remaining vertices of K, or is empty.

For reduced cohomology in degrees j>=1, Mayer–Vietoris gives a direct sum of the cohomology of the pieces, since that intersection has no positive or reduced degree0 cohomology. The only additional possible contribution is in reduced degree0 when the intersection is empty. Thus, writing D_R for the virtual dimension over R=Z or Q,

    D_R(L) <= max(1,D_R(L_1),D_R(L_2)).

For the reverse inequality, each special subgroup W_{L_i} embeds in W_L. Intersecting a torsion-free finite-index subgroup with it gives a torsion-free finite-index subgroup of W_{L_i}. Restriction of a projective group-ring resolution to a subgroup remains projective, so cohomological dimension cannot increase on passage to a subgroup. Also the proper two-sided sum is infinite: a generator from each outside part generates C2*C2, which has an infinite cyclic finite-index subgroup. Therefore D_R(L)>=1. Altogether

    D_R(L)=max(1,D_R(L_1),D_R(L_2)).            (2)

If one side equals K, the union is simply the other side and no extra1 is introduced. This handles the finite/trivial degeneration.

Flagness is preserved, and an induced4-cycle meeting both outside parts would have to use two vertices of K as its other vertices; their edge is a diagonal. Thus the sum is flag-no-square if both pieces are. Formula(2) nevertheless prevents a ratio improvement: if each piece has q_i>=(2/3)d_i, then max(1,q_1,q_2)>=(2/3)max(1,d_1,d_2).

## 4. Joins and direct products

The join L_1*L_2 gives W_{L_1}×W_{L_2}. If neither nerve is a simplex, choose a nonedge in each. The four endpoints form an induced square in the join, so the resulting group is not hyperbolic. This is the combinatorial form of the Z² obstruction.

Even ignoring hyperbolicity, products do not improve the desired ratio when starting from groups satisfying the2/3 bound. For torsion-free groups of finite type and finite cohomological dimension, field Künneth gives

    q(G_1×G_2)=q_1+q_2,

while tensoring integral projective resolutions gives

    d(G_1×G_2)<=d_1+d_2.

The rational equality follows by tensoring the group-ring cochain complexes: nonzero top rational classes have nonzero tensor product, and there are no classes above the sum. We do not assume integral additivity, which can fail. Consequently q_1+q_2>=(2/3)(d_1+d_2)>=(2/3)d(G_1×G_2). An integral dimension drop only increases the ratio.

## 5. A closed construction class excluded

Start with finite simplex nerves and finite flag closed-PL-manifold nerves. Apply any finite sequence of clique inflations, cones and clique-sums along full simplices. Every resulting nontrivial torsion-free finite-index group satisfies q/d>=2/3, by turn2 and(1),(2). If all seeds are flag-no-square, these operations preserve the needed hyperbolicity. Thus introducing these kinds of singularities, adding many vertices, or increasing conformal dimension cannot yield the requested example.

This is not a classification of flag-no-square complexes. Gluing along a non-simplex full subcomplex, altering local homology more substantially, or other constructions remain outside the theorem.

## 6. Exact controls

The checker verifies the puncture projection, simplicial section and contiguity face-by-face for a fully doubled pentagon and for a one-fiber inflation of the flag projective-plane model. Every old puncture must be realized; partial-fiber punctures are included. Exact rational and finite-field profiles are computed for the small inflated/coned models and proper clique-sums of cycles. Explicit square detection verifies the hyperbolicity assertions and the join obstruction.

The projective-plane seed still fails no-square, as recorded in turn2; its use here tests the topological inflation theorem, not hyperbolic eligibility. The all-ring assertion is proved by the homotopy equivalences, not by extrapolating from a few tested fields.

The original is unresolved after three turns. The fourth direction must investigate torsion patterns that are not reducible to these operations and their actual boundary realization constraints.

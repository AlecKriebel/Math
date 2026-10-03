# Turn 2: punctured Coxeter nerves and exclusion of closed manifold nerves

## Direction and outcome

The source's known equality examples suggest replacing their2-dimensional coefficient-sensitive nerves by higher-dimensional ones. We analyze this route using the full deleted-simplex invariant. For every finite flag triangulation of a closed connected PL manifold, the associated right-angled Coxeter groups have ratio1 or n/(n+1), so this whole class cannot beat2/3. Simply increasing the manifold-nerve dimension makes the ratio worse. A separate exact square certificate shows why naive barycentric flagification cannot certify hyperbolicity.

## 1. The credited punctured-nerve formula

Let L be a finite flag complex and W_L its right-angled Coxeter group. Let Gamma be a torsion-free finite-index subgroup. The Davis complex is contractible, has a cocompact W_L action with finite stabilizers, and has dimension dim(L)+1. Coxeter groups are virtually torsion-free; equivalently one may fix any such Gamma for what follows.

The Davis compact-support decomposition gives

    cd_R(Gamma)=1+max{j: reduced H^j(L minus sigma;R)!=0
                         for some simplex sigma, including the empty one}. (1)

We use R=Z or Q. For the empty complex, the usual reduced degree-minus-one convention gives the finite-group case correctly. The formula is credited, not reproved from the entire Davis complex here. Its statement and hypotheses were read in Davis, *The Geometry and Topology of Coxeter Groups*, second-edition author PDF, Section8.5, Theorem8.5.1 and Corollaries8.5.3–8.5.5, printed143–144. The rational version also follows by flat rationalization of that decomposition; Example8.5.8 explicitly illustrates it.

The simplex removed in(1) is its **closed geometric simplex**, not merely its open interior. Combinatorially L minus sigma deformation retracts to the full subcomplex on vertices outside sigma. In barycentric coordinates, every point outside the closed simplex has a positive sum of coordinates on vertices outside it; normalize those coordinates and linearly diminish the coordinates on sigma. The whole homotopy stays in the point's original simplex and never enters sigma. This proves the stated computational reduction.

Testing only H^*(L;R), or deleting arbitrary vertex subsets rather than the prescribed simplices, changes the invariant.

## 2. Closed orientable manifold nerves

Suppose L triangulates a closed connected orientable PL n-manifold M, n>=1. Its top ordinary cohomology over Z and Q is nonzero. The empty-simplex term of(1) gives cd_Z(Gamma)>=n+1 and cd_Q(Gamma)>=n+1. The Davis complex gives the reverse upper bound. Thus

    (cd_Q(Gamma),cd_Z(Gamma))=(n+1,n+1).        (2)

In particular larger dimension and large conformal dimension inside this class cannot improve the source ratio.

## 3. Closed nonorientable manifold nerves

Suppose instead that M is a closed connected nonorientable PL n-manifold, necessarily n>=2. Ordinary top cohomology is

    H^n(M;Z)=Z/2,     H^n(M;Q)=0.              (3)

This is classical Poincaré duality with the orientation local system. The integral empty-simplex term and the Davis dimension bound again give cd_Z(Gamma)=n+1.

For every nonempty simplex sigma, choose a sufficiently small closed PL regular neighborhood N(sigma). A regular neighborhood of the collapsible simplex is an n-ball. Its mapping-cylinder neighborhood structure gives a deformation retraction of M minus sigma onto the compact punctured manifold P=M minus int(N(sigma)). The latter has nonempty boundary. Poincaré–Lefschetz duality gives H^n(P;Q)=0. Therefore every term in(1) has zero rational cohomology in degree n, and cd_Q(Gamma)<=n.

For the reverse bound it is enough to remove one vertex and its ball neighborhood. Excision and the cohomology sequence of(M,P) contain

    H^{n-1}(P;Q) → H^n(M,P;Q) → H^n(M;Q).

The middle group is Q, from the relative cohomology of an n-ball and its boundary; the last group is zero by(3). The first map is therefore onto, and H^{n-1}(P;Q) is nonzero. Formula(1) yields cd_Q(Gamma)>=n. Altogether

    (cd_Q(Gamma),cd_Z(Gamma))=(n,n+1),
    cd_Q/cd_Z=n/(n+1)>=2/3.                    (4)

The equality case is n=2. For a3-dimensional nonorientable nerve the pair is(3,4), not the desired(2,4). The argument uses an actual closed PL manifold nerve; it is not asserted for arbitrary singular complexes or arbitrary high-dimensional compacta.

If the1-skeleton of L has no induced4-cycle, W_L is hyperbolic by the standard right-angled Moussong criterion and Gamma meets the source's hyperbolicity condition. Equations(2),(4) hold regardless of that criterion, so restricting to the hyperbolic members does not escape the exclusion. This is a scoped application of the credited formula, not a general answer for all hyperbolic groups.

## 4. Why barycentric subdivision is not a hyperbolization step

Barycentric subdivision makes any simplicial complex flag: its vertices are nonempty faces, and pairwise comparability is exactly the condition for a simplex. It does **not** generally make the associated Coxeter group hyperbolic.

Suppose an original edge with endpoints a,b lies in two distinct triangles tau_1,tau_2. In the barycentric subdivision the four vertices

    {a}, tau_1, {b}, tau_2

form an induced4-cycle. Consecutive elements are comparable, while the two singleton endpoints are incomparable and the two distinct triangles are incomparable. Thus there are all four cycle edges and neither diagonal. Every triangulated closed surface has such an edge. Its barycentric nerve therefore fails the no-square criterion.

This is a geometric eligibility obstruction, not a numerical failure: even if the full cohomological computation gives(2,3), that particular barycentric Coxeter example cannot be advertised as hyperbolic. The original known hyperbolic equality examples use constructions with the required curvature; they are not recertified by this barycentric model.

## 5. Exact finite controls

Two flag nerves are checked exhaustively over every simplex deletion:
- the12-vertex icosahedral sphere, which is flag and has no induced4-cycle;
- the31-vertex barycentric subdivision of the6-vertex projective-plane triangulation, which is flag but has explicit induced4-cycles.

The checker verifies manifold vertex links, two-triangle edge incidence, signed boundary-square identities, ordinary rational and mod2 Betti numbers, and the rational/mod2 homology of every prescribed puncture. These support(2),(4) in the stated models. The integral dimension calculation in the general proof uses(3) and the credited Coxeter formula; it is not inferred from a rational rank alone. The6-vertex unsubdivided projective plane is only an initial triangulation, not treated as a flag nerve.

The explicit sphere gives ratio1; the projective-plane flag model gives2/3 but fails the hyperbolicity gate. No source counterexample is produced. The next direction must leave closed-manifold nerves and track torsion through genuinely singular complexes while retaining the no-square condition.

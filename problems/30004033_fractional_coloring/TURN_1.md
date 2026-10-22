# Turn 1: exact path boundary signatures at the target density

## Purpose and disposition

We attempt to reduce the weighted/fractional target to a smaller cubic core by controlling the correlation between boundary colors of a degree-two chain. The exact extension theorem below supplies necessary and sufficient boundary conditions, not merely a uniform independent-set estimate. It yields elementary restrictions on a vertex-minimal counterexample. The original problem remains unresolved, 1/5 substantive author turns.

These are elementary rederivations used to investigate a route toward the conjecture; no novelty is claimed. Goddard--Xu's work already develops boundary-intersection methods and proves the stronger known result that a series-parallel graph's fractional chromatic number is determined by its odd girth. Dvorak--Lidicky--Postle also use degree-two reductions, within a different, strengthened 11/4 demand theorem. Neither cited theorem proves the planar 8/3 target.

## 1. Normalization and exact path signature

An r-coloring assigns measurable sets of measure r in [0,1] to vertices, adjacent sets being disjoint (sets can be changed on null sets). Work with 0 <= r <= 1/2. For a path of L edges with fixed endpoint sets A and C of measure r, put t=|A intersect C|. Let I_L(r) be the set of feasible t. Importantly, feasibility holds for **every** pair of endpoint sets having this intersection measure.

**Theorem 1.** For k >= 1,

    I_(2k)(r) = [max(0,(2k+1)r-k), r],

and for k >= 0,

    I_(2k+1)(r) = [0, min(r,k(1-2r))].

These intervals include all their endpoints. The case L=1 is {0}.

**Proof.** Assume I_L=[ell,u]. Fix endpoint sets A,C for a path of L+1 edges, and let B be the penultimate set, disjoint from C. Write s=|A intersect B|. We must choose an s-subset of A minus C, and an (r-s)-subset of the complement of A union C. Those two available measures are respectively r-t and 1-2r+t. Consequently such a B exists exactly when

    max(0,3r-1-t) <= s <= r-t.

All such choices are possible because Lebesgue measure is nonatomic. The induction hypothesis then colors the first L edges with the prescribed A,B. Conversely every extension gives such an s in [ell,u]. Since 2r<=1, intersecting the two intervals is equivalent to

    max(0,3r-1-u) <= t <= r-ell.

Thus I_(L+1)=[max(0,3r-1-u),r-ell]. Starting with I_1={0} proves the displayed formulas by induction. The same construction proves sufficiency for the fixed endpoint sets, rather than just for some representatives. No probabilistic independence assumption is made. QED.

For r=3/8 this becomes

    I_1={0}; I_2=[1/8,3/8]; I_3=[0,1/4];
    I_L=[0,3/8] for every L>=4.

The two nontrivial short-chain conditions point in opposite directions. An isolated degree-two vertex needs its two neighbor sets to overlap by at least 1/8. A two-vertex chain needs its endpoint overlap to be at most 1/4. An arbitrary outside coloring need not satisfy either.

## 2. Consequences for a smallest counterexample

Suppose the target is false and G has the fewest vertices among finite planar triangle-free subcubic counterexamples.

1. G is connected, has no cutvertex, and has minimum degree at least two. Components can share a common palette. At a cutvertex, color each smaller side and identify their equal-measure cutvertex sets by a measure-preserving rearrangement, applied to every set on that side. Equivalently, refine their finitely many color-pattern atoms and couple the conditional distributions given membership at the cutvertex. This constructs a common coloring. Isolated vertices and leaves extend a smaller coloring since 1-r>=r.
2. G is not a cycle. Even cycles admit r=1/2. For an odd cycle of length 2k+1>=5, take all cyclic rotations of a maximum independent set, uniformly; every vertex has marginal k/(2k+1)>=2/5>3/8, and trim each color set to measure 3/8. Trimming preserves disjointness.
3. G has no three consecutive degree-two vertices. In a connected non-cycle graph, the maximal degree-two chain containing them has distinct endvertices (otherwise the attachment endvertex is a cutvertex), and at least four edges. Delete its internal vertices, color the smaller induced graph, and use Theorem 1 to extend for arbitrary end sets.
4. Every pair of adjacent degree-two vertices lies on a 5-cycle. Write the chain u-x-y-v with x,y of degree two. The ends u,v are distinct, since a coincidence would create a triangle. Delete x,y. If uv is already an edge, its endpoint overlap is zero and the length-three path extends. Otherwise, if u,v have no common neighbor in the remaining graph, add uv along the deleted path. This preserves planarity, simplicity, triangle-freeness, and maximum degree at most three, and yields a smaller graph. Its coloring has endpoint overlap zero, so again it extends. The only remaining case is a common neighbor z, yielding the 5-cycle u-x-y-v-z-u.

These reductions do not prove that G is cubic, and do not eliminate cubic girth-five graphs. They also do not justify replacing the universal weight condition by the unweighted independence ratio.

## 3. Verification and next obstruction

`turn1/check_paths.py` independently enumerates finite palette sets and walks in their disjointness graph; it does not use the interval recurrence to generate attainable intersections. It compares all attained terminal intersection sizes with the theorem for each palette size 2 through 10, all positive demands at most half the palette, and lengths 1 through 12. Additional rational checks compare the recurrence and closed forms for denominators through 50 and lengths through 30. These finite controls supplement the universal proof.

The next substantive obstruction is compatibility of several boundary correlations around a cubic core. One interval per path does not establish a globally consistent distribution on all boundary vertices. In particular, the known series-parallel theorem means that merely extending this calculation through a series-parallel decomposition would not address the remaining K4-minor cases.

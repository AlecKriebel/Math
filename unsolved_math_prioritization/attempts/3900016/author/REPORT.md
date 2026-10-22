# Distinct areas in convex-polygon triangulations: partial bounds and corrected scope

## Status and conventions

This is an incomplete investigation, not a solution or a novelty claim. Five substantive approach families were used. The exact extremal function, the sharp bounded-lattice function, and the question of unavoidable triple repetitions remain unresolved here. The proofs below are self-contained elementary partial results. A bounded literature search did not establish their novelty or the current best bounds.

Eddie Grove's 6 March 1990 question, preserved by David Eppstein's Geometry Junkyard, asks for a large guaranteed number of distinct triangle areas in a vertex triangulation of every convex polygon. It also singles out polygons in planes in three-dimensional space, with integer vertices in a cube of side m and an integer normal whose coordinates have magnitude at most m. It asks separately whether some polygon forces three equal-area triangles in every triangulation. The host and proposer are different people. [Original problem](https://ics.uci.edu/~eppstein/junkyard/tri-diff-areas.html).

Throughout, a convex n-gon has n distinct extreme vertices, n >= 3. Thus it is strictly convex as a polygon: no three of its vertices are collinear. Only diagonals between its existing vertices are allowed; there are no additional vertices. Every triangulation has n-2 nondegenerate triangles. Write

    D(P) = max over triangulations T of P of |{area(Delta): Delta in T}|,
    t(n) = min over convex n-gons P of D(P).

The minimum exists in the elementary sense that the nonempty set of possible integer values of D(P) is a subset of {1,...,n-2}. A nonsingular affine map preserves all area equalities and multiplies every area by one common positive factor, so it preserves D(P).

For an integer m >= 1, let L(n,m) be the class of such polygons whose vertices are in [0,m]^3 intersected with Z^3 and lie in a plane with a nonzero primitive integer normal u satisfying ||u||_infinity <= m. Set

    t_L(n,m) = min over P in L(n,m) of D(P),

only when L(n,m) is nonempty. Translating the cube by an integer vector changes nothing. This adopts side length m; a convention with m grid points per side instead replaces the side-length parameter by m-1. An m-only guarantee over all feasible n cannot exceed 1, because the class contains triangles. Any nontrivial m-only variant must retain an additional size assumption.

## 1. Maximum triangles and strict cap descent

### Lemma 1: strict cap bound

Let P have at least five vertices, and let ABC be a maximum-area triangle among all triples of its vertices. Each of the three caps cut off by its sides, on the side away from the opposite triangle vertex, has area strictly smaller than area(ABC). Consequently every triangle in such a cap has smaller area.

Proof. Affinely normalize A=(0,0), B=(1,0), C=(0,1). Maximality implies that every vertex X=(x,y) satisfies

    |x| <= 1, |y| <= 1, |1-x-y| <= 1.

These inequalities hold throughout P by convexity. In the cap below AB, y <= 0; the inequalities give x <= 1 and x+y >= 0, hence x >= -y >= 0. This cap lies in the triangle with vertices A, B, E=(1,-1), whose area equals area(ABC)=1/2.

If a closed convex cap contained in that triangle has the same area, it is the whole triangle: omission of any point of the larger triangle, by separation and closure, omits a positive-area portion. Thus equality requires E to belong to P. Since E is an extreme point of that containing triangle and belongs to the cap, E is a vertex of P.

If E is a vertex, apply maximality also to triangles EAX and EBX. These give |x+y| <= 1 and |1-x| <= 1. Together with the previous inequalities they imply

    0 <= x <= 1, 0 <= x+y <= 1.

This is exactly the parallelogram with vertices A,E,B,C. It is contained in P because its four corners belong to P, and contains P by the inequalities. Hence P is that parallelogram and has only four extreme vertices, a contradiction. The other caps are handled by permuting A,B,C. QED.

### Proposition 2: logarithmic guarantee

Define the integer function G by G(3)=G(4)=1 and, for n >= 5,

    G(n) = 1 + G(ceil((n+3)/3)).

Then t(n) >= G(n). Equivalently, if N_j=(5*3^(j-1)+3)/2, then G(n) is the least integer j >= 1 such that n <= N_j.

Proof. Select a maximum-area triangle. The numbers of other polygon vertices on its three boundary arcs sum to n-3, so one cap has at least ceil((n-3)/3)+2 vertices. Recurse in that cap and triangulate the other caps arbitrarily. Lemma 1 makes the newly selected area strictly greater than every area obtained recursively; the chosen triangles have disjoint interiors and coexist in a triangulation. Induction, and monotonicity of G, give the stated bound. The thresholds obey N_1=4 and N_j=3N_(j-1)-3, which yields the formula. QED.

For example G(n)=2 for 5 <= n <= 9 and G(n)=3 for 10 <= n <= 24. This mechanism only follows one cap. It provides no control of collisions between distinct caps, so does not establish the hoped-for linear guarantee.

## 2. What local diagonal flips do and do not prove

Suppose a triangulation has at least three triangles of area a, two adjacent across a diagonal. Their union is a convex quadrilateral. Flipping its diagonal replaces these two triangles by areas b,c with b+c=2a. If at least one of b,c is absent from the old area palette, the number of distinct areas increases: a still occurs in the untouched third triangle and every other old value is unchanged.

If both the old pair and the new pair have equal areas, the quadrilateral is a parallelogram. For a direct verification normalize the old diagonal endpoints to (0,0),(1,0), and the other two vertices to (x,h),(y,-h), h>0. The new areas are h(x+y)/2 and h(2-x-y)/2; convexity makes both positive. They are equal exactly when x+y=1, the parallelogram condition.

The obstruction is precise. The new areas can both belong to the old palette, and three repeated-area triangles need not contain an adjacent pair. Maximizing the distinct-area count therefore does not, by this argument, force multiplicity at most two. No claim that this flip process solves Grove's repetition question is made.

A fan from a prescribed vertex is also insufficient. Take the origin and consecutive equally spaced points on a circular arc of angular length less than pi. Their convex hull in this order is a strictly convex polygon, and the fan at the origin has equal-area triangles. Rational examples are obtained with a rational rotation matrix; the checker verifies one eight-vertex instance. This does not rule out a better fan based at another vertex or a better triangulation.

## 3. A square-root guarantee by compatible rainbow packing

### Lemma 3: one base sees at most two vertices of each area

In a strictly convex polygon Q, fix a boundary edge AB. For any positive a, at most two other vertices X satisfy area(ABX)=a.

Proof. All such vertices are on the same side of the line AB, and the equation specifies one parallel line at a fixed positive distance. A line contains at most two extreme vertices of a convex polygon. QED.

### Theorem 4: universal packing bound

Every convex n-gon has a triangulation with k distinct areas for some integer k satisfying

    n <= 4k^2 + 3k + 2.

In particular, writing B(n) for the least integer k >= 1 with that inequality,

    t(n) >= max(G(n), B(n)),
    B(n) = ceil((sqrt(16n-23)-3)/8).

Proof. Start with P as a single unselected convex face. Whenever an unselected face contains a vertex triangle whose area is not among the already selected areas, insert that triangle's sides, select the triangle, and retain its nonempty caps as unselected faces. At every stage all inserted diagonals are noncrossing. The procedure terminates because it selects a new triangle face each time and any noncrossing diagonal subdivision can be completed to a triangulation with only n-2 triangles.

Let k be the number of selected triangles at termination, d the number of inserted internal diagonals, and r the number of unselected faces. Then

    d <= 3k,       k+r=d+1,       r <= 2k+1.

Write the unselected face sizes as s_1,...,s_r. Counting edge incidences gives

    3k + sum_i s_i = n + 2d,
    n = k+2 + sum_i (s_i-2).

If an unselected face contained a triangle with a new area, the procedure would not have terminated. Its entire triangle-area palette is therefore contained in the selected k-element palette. Applying Lemma 3 to one of its boundary edges gives s_i-2 <= 2k. Thus

    n <= k+2+2kr <= k+2+2k(2k+1) = 4k^2+3k+2.

Complete each residual face by arbitrary diagonals. All selected triangles persist, so the final triangulation has at least k distinct areas. Solving the quadratic gives B(n); no numeric square-root calculation is needed by the implementation. QED.

The bound is asymptotically sqrt(n)/2. It is an elementary verified lower bound, not a claimed best-known result. The loss occurs because there may be O(k) residual faces, each with O(k) vertices. This proof does not replace that product by a linear bound and does not give matching extremal polygons.

## 4. The actual three-dimensional lattice case

### Proposition 5: exact area units and projection

Let P have integer vertices in a plane with primitive integer normal u. For every vertex triangle its cross product is k*u for some nonzero integer k. Its Euclidean area is |k|*||u||_2/2. Projection deleting a coordinate j with u_j != 0 is injective on the plane, preserves convexity and triangulations, and preserves equality and inequality of triangle areas.

Proof. The cross product is an integer vector parallel to u, say lambda*u. Bezout's identity supplies integers b_j with sum_j b_j*u_j=1. Thus lambda=sum_j b_j*(lambda*u_j) is an integer. The norm formula gives the area. The projection has trivial kernel on the plane's direction space because its kernel is the jth coordinate axis and u_j != 0. Its projected doubled area is |k*u_j|, so it scales all areas by the same nonzero factor. QED.

This is an exact reduction to a planar integer polygon with congruence constraints and coordinate bounds; it is not a replacement by an arbitrary unbounded planar integer polygon.

### Proposition 6: spectrum and mass bounds in a cube

Put U=||u||_infinity and K=floor(m^2/U). Every vertex triangle has integer area unit |k| in {1,...,K}. If S=2*area(P)/||u||_2, then S is a positive integer and

    S <= floor(2m^2/U).

For every triangulation containing q distinct areas,

    q <= min(n-2, K),
    S >= (n-2) + q(q-1)/2.

Proof. Choose j with |u_j|=U and project onto the other two coordinates. The image lies in a square of side m. Any triangle in that square has doubled area at most m^2: the absolute determinant attains its maximum at square corners, by maximizing an affine function in each scalar coordinate, and the corner maximum is m^2. Therefore |k|*U <= m^2. The whole projected polygon has area at most m^2, giving S*U <= 2m^2. A triangulation expresses S as a sum of n-2 positive integer units. If q distinct units occur, their minimum possible sum is 1+2+...+q, and each of the n-2-q remaining units is at least 1. This gives the mass bound. QED.

The lower bounds G(n) and B(n) continue to apply to t_L(n,m). The arithmetic formulas are upper constraints for individual polygons, not a sharp universal lower bound. They do not determine t_L(n,m).

## 5. Exact small cases and finite spectra

### Proposition 7

    t(3)=t(4)=1,        t(5)=t(6)=2.

The same values hold for t_L(3,m),t_L(4,m) when m>=1, and t_L(5,m),t_L(6,m) when m>=2.

Proof. The triangle case is immediate. A unit square gives the quadrilateral upper bound 1. Proposition 2 gives the lower bound 2 for n=5,6. To prove matching upper bounds, use the following integer polygons in the plane z=0, all in the square [0,2]^2:

    P5 = ((0,0),(1,0),(2,1),(1,2),(0,1)),
    P6 = ((0,0),(1,0),(2,1),(2,2),(1,2),(0,1)).

Use doubled areas. The total area of P5 is 5. Its five ear areas, at the listed vertices, are (1,1,2,2,1). Every pentagon triangulation has two nonadjacent ears and one remaining triangle. Two ears of doubled area 2 cannot both be chosen, because those ears are adjacent. Choosing two area-1 ears leaves an area-3 triangle; choosing areas 1 and 2 leaves another area-2 triangle. Thus every triangulation has exactly two distinct areas.

For P6, the doubled area of a vertex triangle is determined by the unordered cyclic gaps between its vertices: gap type (1,1,4) has area 1, type (1,2,3) has area 2, and type (2,2,2) has area 3. These are all partitions of 6 into three positive integers. If a triangulation contains an area-3 triangle, it is the alternating central triangle, and its complement consists of three area-1 ears. Otherwise every area is 1 or 2. The total doubled area is 6 and there are four triangles, so this second case necessarily has two of each. In both cases the number of distinct areas is 2. The normal (0,0,1) satisfies the stated bounds. QED.

For all n>=4 one also has t(n)<=n-3: in a regular n-gon every triangulation has at least two ears, all ears have the same area, and there are n-2 triangles. For completeness the ear fact follows from the dual tree of a triangulation: it has n-2 vertices and n-3 edges, and its leaves correspond to ears. A finite tree with at least two vertices has at least two leaves. This upper bound is not sharp already at n=6.

### Exact recurrence for a fixed polygon

For vertices numbered 0,...,n-1 in counterclockwise order, let F(i,j) be the family of area sets arising from triangulations of the consecutive subpolygon i,...,j. Set F(i,i+1)={empty set}. For j>=i+2,

    F(i,j) = union over i<k<j of
             {A union B union {area(i,k,j)}:
              A in F(i,k), B in F(k,j)}.

Every triangulation has one triangle incident to boundary edge ij; its third vertex k splits the remaining triangulation into the two indicated subpolygons. Conversely these pieces glue to a triangulation. Thus D(P)=max{|A|: A in F(0,n-1)}. The family may be exponentially large; this is an exact bounded-instance method, not a polynomial-time algorithm or a proof of the extremal function.

The rational-pentagon obstruction explored during this approach was false: the explicit P5 above is already an integer counterexample to the proposed distinction. No classification of all pentagons is asserted.

## Verification and remaining gap

The included standard-library checker uses exact integers and rational numbers, explicit runtime guards rather than Python assertions, Catalan enumeration, an independently generated ear-deletion enumeration for the small witnesses, exact cap/packing checks on a bounded polygon suite, and exact three-dimensional cross products. It has no network dependency and reads no source corpus. See VERIFICATION.md for executed environments, counts, negative controls, and limitations.

The mathematical proofs establish the displayed lower bounds, exact values through n=6, and the arithmetic reductions. Finite checks do not quantify over all real convex polygons. The full problem requires determining the worst-case optimum for general n and the correctly normalized bounded-lattice class, with matching upper and lower bounds. The separate possibility of an unavoidable triple repeated area is not decided. All five substantive approaches are spent; the terminal research status is exhausted 5/5, with partial results only.

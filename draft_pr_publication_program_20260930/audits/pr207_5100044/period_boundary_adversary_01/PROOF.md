# Independent proof of the PR207 repetition boundary

The inverse polygon here has straight edges joining the inverted vertices, and polygon area is the algebraic shoelace area. This review concerns only the proposed boundary construction. It neither assumes nor rechecks the original least-period-divisible-by-four theorem. The two input artifacts are pinned in SOURCE_PINS.json. No mathematical report by another reviewer was read.

## Exact setting

Let E be x²/8 + y²/5 = 1, let C be x²/(32/9) + y²/(5/9) = 1, and let F=(√3,0). Both ellipses have squared focal distance 3. Their squared semiaxes are positive and satisfy 32/9<8 and 5/9<5, so C is a strict nondegenerate inner ellipse. The confocal parameter is λ=8−32/9=5−5/9=40/9.

Set a=2√2, b=−4√2/3, h=5/3, and P=((a,0),(b,h),(b,−h)). Write M=−P with exactly this ordering. A direct substitution places every vertex of both triangles on E. The vertex sets of P and M are disjoint, so these are distinct oriented orbits even after cyclic relabeling.

## A continuous forward triangular family, derived without invoking a porism

Scale (x,y)=(2√2 X,√5 Y). Then E becomes the unit circle and C becomes the ellipse with semiaxes 2/3 and 1/3.

For q=(cos θ,sin θ) and u=(cos φ,sin φ) on the unit circle, the chord has a unit normal of angle (θ+φ)/2 and signed distance cos((φ−θ)/2) from the origin. Its line is tangent to the normalized C exactly when

    9 cos²((φ−θ)/2) = 4 cos²((φ+θ)/2) + sin²((φ+θ)/2).

Expanding yields the symmetric bilinear condition

    3 X U + 6 Y V = −2.                                      (1)

For q=(X,Y) on the unit circle define A=3X, B=6Y, D=A²+B² and S=√(D−4). Since 9≤D≤36, S is positive everywhere. The two solutions of (1) on the unit circle are

    r = [−2(A,B) + S(−B,A)]/D,
    s = [−2(A,B) − S(−B,A)]/D.                              (2)

They are continuous real functions of q, have norm one, and are distinct. Neither equals q because 3X²+6Y²≥3 whereas (1) would require −2.

The coordinate products of r and s satisfy

    r_x s_x = (4−B²)/D,       r_y s_y = (4−A²)/D.

Consequently

    3r_x s_x + 6r_y s_y
      = (36−3B²−6A²)/D
      = −2,

where X²+Y²=1 was used in the final equality. Thus r and s are also joined by a tangent chord. Every q gives a closed triangle (q,r,s) all three of whose sides touch C.

The orientation is forward and consistent. No pair of its vertices can be antipodal, since the left side of (1) for u=−q is −3X²−6Y²≤−3. Hence det(q,r), det(r,s), and det(s,q) never vanish. By continuity their signs are constant on the circle. At q=(1,0), (q,r,s)=((1,0),(−2/3,√5/3),(−2/3,−√5/3)), and all three determinants are positive. Therefore (q,r,s) is counterclockwise for every q. The positive affine scaling preserves this orientation. Each tangent contact lies on its chord segment because C lies strictly inside the outer ellipse.

At q=(1,0), scaling the triple gives P. At q=(−1,0), (2) gives the central negative of the first triple, hence M. Taking q=(cos θ,sin θ) for 0≤θ≤π explicitly joins P to M through one continuous forward family of distinct-vertex triangular tangent polygons.

## Why the whole family obeys Euclidean billiard reflection

Tangency alone to an arbitrary conic would not establish the reflection law after affine scaling. Here confocality supplies the needed exact identity.

For p=(x,y) on E put N=(x/8,y/5). Let v=(u,v_y) be a unit direction and n=(−v_y,u) its unit perpendicular. On E,

    8n_x² + 5n_y² − (n·p)² = 40 (N·v)².                    (3)

This follows by expanding and using x²/8+y²/5=1. A line in direction v through p is tangent to C precisely when

    (8−λ)n_x² + (5−λ)n_y² = (n·p)².

Since n is unit, (3) shows |N·v|=√(λ/40)=1/3. Both tangent rays from p pointing into E therefore have N·v=−1/3. Also ||N||²≥1/8>1/9, so these are two distinct directions with opposite nonzero tangential components. If one of them is w, the incoming direction from its neighboring vertex is −w. Reflection in the tangent line of E sends −w to the other inward direction. Thus the ordered family (q,r,s) satisfies the Euclidean specular law at every vertex.

For the particular P and M, the independent checker also verifies the vector reflection formula directly at all six vertices:

    v_out = v_in − 2 (v_in·N) N / ||N||²,
    v_in·N = 1/3,       v_out·N = −1/3.

There is no reliance on the proposed script's reflection checks.

## Tangency contacts and least period

For P's three oriented edges the exact contact points are

    (8√2/9,5/9),       (−4√2/3,0),       (8√2/9,−5/9).

Their segment parameters from the first endpoint of each edge are respectively 1/3, 1/2, and 2/3. For M they are the central negatives, at the same three parameters. Hence the actual segments, not merely the extended lines, touch C. The checker verifies each contact lies both on the corresponding line and on C.

The directed billiard state returns after three reflections because its collision sequence closes and its initial outgoing edge is recovered. All three collision vertices are distinct, so it cannot return after one or two collisions. Its least collision period is exactly three. Repeating the ordered vertex list four times retains this least period; the list has length twelve.

## Independent signed-area calculation

For a triangle use A(p0,p1,p2)=det(p1−p0,p2−p0)/2. This gives

    A(P)=A(M)=h(a−b)=50√2/9.

A unit inversion centered at F is F+(p−F)/||p−F||². Omitting the common final translation F does not change polygon area. Put c=√3, U=a−c, V=b−c, and D1=V²+h². For P the inverse vertices after omitting that translation are

    (1/U,0),       (V/D1,h/D1),       (V/D1,−h/D1).

Thus its inverse signed area is

    h/(U D1) − Vh/D1² = (8√2−√3)/80.

The inversion denominators before cancellation are 11−4√6 at the first vertex and (28+8√6)/3 at the other two vertices, all strictly positive. The analogous computation for M uses U=−a−c, V=−b−c, and h replaced by −h. Its denominators are 11+4√6 and (28−8√6)/3, also strictly positive, and its inverse signed area is

    (8√2+√3)/80.

The independent checker crosschecks these triangle-difference determinants with the homogeneous identity

    2A(I(P)) = Σ_cyclic det(p_i−F,p_(i+1)−F) d_(i+2) / (d0 d1 d2),
    d_i=||p_i−F||².

Both inverse signed areas are positive, so taking absolute values for these two individual triangles gives the same two products.

Consequently

    A(P) A(I(P)) = (80−5√6)/72,
    A(M) A(I(M)) = (80+5√6)/72,

and their difference is −5√6/36, which is strictly negative.

For algebraic polygon area, each traversal contributes the same shoelace sum. Four traversals multiply each area by four and each area product by sixteen. The displayed-length-twelve products are therefore

    (160−10√6)/9       and       (160+10√6)/9,

with exact difference −20√6/9≠0. The checker verifies the repeated-list sums directly as well as the scaling identity.

## Scope and adversarial conclusion

No mathematical error was found in the proposed construction or its stated exact values. The supplied script did not itself display a proof of connected same-family membership; the explicit construction and confocal reflection identity above supply that proof independently.

This is a counterexample only to a reading that admits repeated shorter cycles as displayed-N billiard polygons and applies the claim merely because the displayed N is divisible by four. It does not give a least-period-twelve billiard orbit and does not contradict an assertion whose hypothesis requires least period divisible by four. This audit does not choose the intended reading of any source wording and does not verify the original primitive theorem. The sixteen-fold product scaling specifically uses algebraic/shoelace area with traversal multiplicity, as in the proposed construction; a convention using area of a geometric union would require its own statement.

Reproduce the exact computations with:

    /opt/homebrew/bin/python3.11 independent_boundary_audit.py

The run producing INDEPENDENT_RESULT.json passed 118 exact checks under SymPy 1.14.0.

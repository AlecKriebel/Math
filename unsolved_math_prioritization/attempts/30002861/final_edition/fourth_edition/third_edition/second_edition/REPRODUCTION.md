# Mathematical reproduction conventions

This note fixes sufficient conventions to check the second-edition proofs and finite rational example independently. All arithmetic on the finite example is over the rational numbers; decimal rounding and numerical rank tolerances are unnecessary. The general assertions require the proofs and their independent audits, not merely finite checks.

## 1. Inputs labels and incidence

Use [SECOND_PASS_CERTIFICATE.json](SECOND_PASS_CERTIFICATE.json). A rational string p/q means the exact fraction with integer numerator p and nonzero positive denominator q. Integer strings are exact integers. Indices are zero-based.

The vertex order is O₀,…,O₅,I₀,…,I₅,Q₀,…,Q₅, with numerical indices 0,…,17. Triangle triples are oriented counterclockwise and have the order shown in the certificate and construction proof. An undirected edge is the sorted pair of its endpoint indices; order all 45 distinct pairs lexicographically. Retained row order is 0,…,11. Jet columns are (f₀,g₀x,g₀y,f₁,g₁x,g₁y,…,f₁₇,g₁₇x,g₁₇y).

For vectors a,b use det(a,b)=aₓbᵧ−aᵧbₓ. Each Qᵢ is recovered by intersecting the lines Oᵢ₋₁Oᵢ and Oᵢ₊₁Oᵢ₊₂. More generally, for A+t(B−A)=C+s(D−C),

    t = det(C−A,D−C) / det(B−A,D−C).

Every denominator used for this example is nonzero. Substitution gives precisely the six displayed Q coordinates.

[FINITE_WITNESSES.json](FINITE_WITNESSES.json) lists all positive doubled triangle areas, each edge's incident face indices, all twelve counterclockwise interior fans, and an active spanning tree. These values are consequences of the exact inputs, not additional assumptions.

## 2. Exact conforming disk verification

For every oriented triangle (a,b,c), compute det(P_b−P_a,P_c−P_a) and require it to be strictly positive. There are 28 triangles and 45 distinct edges; exactly 39 edges have two incident triangles. The six one-triangle edges join Q₀,…,Q₅ cyclically. Their boundary graph must be connected with degree two at every boundary vertex.

To check any two triangles, intersect their three closed left half-planes. An explicit rational procedure starts with one triangle's vertex polygon and clips it successively by each oriented edge line of the other triangle. For an oriented clipping line AB, set h(X)=det(B−A,X−A). On a segment XY meeting h=0, the intersection point is

    X + h(X)/(h(X)−h(Y)) · (Y−X).

Keep the portions with h≥0, preserve boundary points, and remove repeated consecutive points. Degenerate intersections consisting of one point or a segment must be retained. All 378 unordered triangle pairs must intersect in exactly the convex hull of their common listed vertices: the empty set, one vertex, or their common edge. This checks crossings, overlap, and accidental non-face contact, including contact involving collinear edges.

For every vertex v, form its link graph by taking the opposite edge from each triangle containing v. Require a connected cycle at each interior vertex and a connected path at each boundary vertex. Verify triangle adjacency is connected, the boundary is one cycle, and V−E+T=18−45+28=1. The positive triangles, exact pairwise face intersections, and these manifold/disk conditions certify the full conforming polygonal disk. Nothing depends on a plotted appearance.

## 3. Determinant row convention and jet blocks

For each interior vertex v, a positively oriented incident triangle (v,a,b), or its cyclic rotation, places b immediately counterclockwise after a in the neighbor fan. Start at the least numbered neighbor and follow this successor relation around the fan. Write the result as w₀,…,wₙ₋₁. Set dᵢ=P_wᵢ−P_v and aᵢ=det(dᵢ,dᵢ₊₁)>0, with subscripts modulo n.

All twelve interior fans are even; vertices 7,9,11 have degree four, and the others have degree six. For each incident edge define

    r_v,wᵢ = (−1)^i det(dᵢ₋₁,dᵢ₊₁)/(aᵢ₋₁aᵢ).

All other entries in row v vanish. This is the accepted first-pass row divided by its nonzero factor a₀. The coefficient convention in the certificate is exactly this one, so direct rational comparison checks all 540 entries of its 12-by-45 matrix R.

The only nonzero jet block in row v is at vertex v:

    H_v,f = sum_i r_v,wᵢ,
    H_v,gx = (1/2) sum_i r_v,wᵢ (dᵢ)_x,
    H_v,gy = (1/2) sum_i r_v,wᵢ (dᵢ)_y.

Every other block is zero. These formulas determine all 648 entries of H. Independently check the three second moments sum_i r_v,wᵢ(dᵢ)_x², sum_i r_v,wᵢ(dᵢ)_x(dᵢ)_y, and sum_i r_v,wᵢ(dᵢ)_y²; each is zero.

## 4. Short exact rank certificates

Every nonzero column of R has exactly two nonzero endpoint entries. There are 27 such active edges, all among the twelve interior vertices; the other 18 columns vanish. The active spanning tree in FINITE_WITNESSES is

    (0,1), (0,5), (0,6), (0,7), (1,2), (1,8),
    (5,4), (5,11), (6,10), (2,3), (2,9).

Its eleven edges connect all twelve rows. Therefore the active graph is a single closed component. Along an oriented edge v→w any left dependency z obeys

    z_w/z_v = −r_vw/r_wv.

More precisely, the same equation without division, z_w r_wv=−z_v r_vw, shows that a zero coordinate propagates to every vertex. A nonzero dependency is consequently determined by its value at a root, and every coordinate is nonzero.

For the sign matrix sign(R), substitute the vector

    (1,−1,−1,−1,−1,1,1,1,−1,1,−1,1).

Each column pairing cancels. The tree bounds the left nullity by one, and this vector attains it. Thus rank sign(R)=11 and every sign-cycle product is positive.

For the actual rational matrix, the oriented cycle 0→1→7→0 has successive propagation ratios

    −4575/8239,   −977/688,   153/563.

Their product is 683875575/3191327216, positive and unequal to 1. A nonzero dependency would return to its starting coordinate multiplied by this unequal number, which is impossible. Connectedness then implies the whole left nullspace is zero, proving rank R=12. No large determinant or floating-point rank is needed. Since there are only twelve rows, adjoining H also has rank 12.

The accepted exact reduction Rm=Hj therefore proves arbitrary quartic Hermite interpolation on this mesh. The example demonstrates a limitation of sign-only reasoning; it is not a counterexample to quartic interpolation.

## 5. Full remaining coefficient system

The accepted [first-edition derivation](first_edition/QUARTIC_REDUCTION.md) and [audit](first_edition/QUARTIC_AUDIT.md) give complete Bernstein conventions. On an oriented triangle use the normalized degree-four Bernstein basis

    B_abc = 4!/(a!b!c!) · λ₀^a λ₁^b λ₂^c,     a+b+c=4.

A vertex coefficient is f_v. A coefficient with exponent 3 at v and exponent 1 at w is f_v+g_v·(w−v)/4. Share one edge-middle coefficient c220 across both incident triangles, and give each triangle three independent c211 coefficients indexed by its exponent-two corner. This leaves E+3T=129 unknowns after the 54 arbitrary jets have been prescribed.

To assemble a direct derivative matrix, order edges lexicographically and, for each interior edge (v,w) with v<w, choose normal n=(−(w−v)_y,(w−v)_x). Order the two incident triangles by their indices, and subtract the first triangle's derivative from the second's. Evaluate n·∇ at v+(w−v)/3 and v+2(w−v)/3, in that order. Barycentric coordinates come from the inverse of the matrix with columns (x_v,y_v,1) for that triangle's vertices. Differentiating the displayed basis gives every entry rationally. A simultaneous reversal of a two-row sign or another consistent edge order does not change ranks.

There are 78 equations and 129 remaining-coefficient columns. The associated 54 jet columns are moved to the right side. Across each interior edge, the traces are identical by the shared Bernstein coefficients and endpoint jets. The difference of transverse derivatives is a cubic vanishing at both endpoints, so its evaluations at 1/3 and 2/3 determine its two remaining coefficients. Equivalently, in normalized coordinates it has the form

    (12/γ) x(1−x)[(1−x)L_v+xL_w],     γ≠0,

where L_v,L_w are the two residual Bernstein equations in the baseline audit. Evaluations at 1/3 and 2/3 give an invertible 2-by-2 change of equations. Thus the 78 evaluation equations are exactly the full residual C1 system, not a sampled substitute for it.

For the exact minor in [FINITE_AUDIT_CERTIFICATE.json](FINITE_AUDIT_CERTIFICATE.json), use the preceding construction with interior parameters 1/4 and 3/4 instead. Order the 129 columns by all 45 lexicographic edge-middle coefficients followed by triangle 0's three c211 coefficients, triangle 1's three, and so on; within a triangle follow its listed vertex order for the exponent-two corner. Retain all 78 rows in the lexicographic-edge, increasing-parameter order just specified. Select the 78 zero-based columns listed as full_BB.pivot_columns, in their given order. The determinant of this square matrix is exactly the nonzero rational full_BB.minor_determinant. This convention pins the determinant itself, not merely its nonvanishing. The certificate's input hash refers to the included SECOND_PASS_CERTIFICATE.json. Its reduced-row scaling at index v means the included construction-certificate row divided by independent row v; the same factor applies to H. The independent fan starts at the first outgoing ray in counterclockwise order from the positive horizontal axis, using the upper half-plane (including the positive horizontal ray) before the lower half-plane; within each half-plane, determinant signs order rays. All displayed scaling factors are +1 or −1. Its checkerboard signs use face 0 colored +1 and neighboring faces oppositely colored.

An independent calculation in the construction audit verifies rank 78 before and after adjoining the jet columns. The same rank follows mathematically from the fan elimination and the short R certificate: there are q=12 even interior vertices and no singular row, so the eliminated corner rank is 2E_I−q=66 and the remaining rank is 12, totaling 78. This is an independently auditable route to the rank result without distributing the large derivative matrices.

## 6. Generic identity checks

For the pure-gradient lemma set d₀=(1,0), d₁=(0,1), d₂=(a,b), d₃=(c,d), D=ad−bc. Expand r=(−acD,bdD,cd,−ab). Its second moment is zero and its first moment is (ac(d−b−D),bd(D+c−a)). The proof handles b=0, c=0, and bc≠0 separately under a<0,d<0,D>0. Passing polynomial identities alone does not replace that inequality argument.

For normalized edge balance take v=(0,0), w=(h,0), u=(p,q), z=(r,−t), with h,q,t>0. Expand D_v=rq+pt and D_w=h(q+t)−rq−pt. The transverse line intersects at P=(rq+pt)/(q+t), and the signed dependency ratio is P/(h−P). For each triangle express the opposite vertices in barycentric coordinates and check the three two-term homogeneous equations. Their common nonzero solution is the projective concurrency point, including the case with coordinate sum zero. The proof that face balance implies all-cycle balance uses the disk topology.

For the symmetric family, substitute its displayed coordinates into the three determinant equations for edges (O₁,I₁),(I₀,I₁),(O₁,I₂), with opposite pairs (O₀,I₂),(O₀,I₂),(O₂,I₁). Direct expansion yields F₁,F₂,F₃ and

    bF₁−bF₂−eF₃ = s[r(eb+b+e)−2eb].

The argument then uses r>1/2, 0<e<1, 0<b<r and nonzero dependency coordinates. The accepted proof also excludes a smaller closed component; verifying only the twelve-row symmetry equations would omit that essential quantifier.

## 7. Acceptance and limits

[THEORY_AUDIT.md](THEORY_AUDIT.md) and [CONSTRUCTION_AUDIT.md](CONSTRUCTION_AUDIT.md) contain the mathematical acceptance arguments and exact checked scope. The finite certificate can be reproduced from this note and its rational inputs with any exact-arithmetic method. Programs and implementation-dependent output are not required public dependencies.

The public manifest establishes file identity, not mathematical validity. Neither a matching hash, the sign-balanced example, the known dimension formula, nor a compact quadratic spline proves a general quartic resolution.

# Independent universal GKZ/fan audit of PR55

The claim audited is the equality of the two explicit polytopes in original CANDIDATE.md, equation (4), for the smooth complete very ample toric embedding of degree at least two described there. This is a proof audit, separate from the finite polynomial controls and from any claim of priority. No other new review or old reviewer/checker was used to derive this audit.

## Imported input and its hypotheses

The cited GKZ primary book was personally read at printed pp.219–222, 299–302, 345–346, 361–365. The decisive primary facts are Chapter 11 Theorem 1.3(a), p.345, identifying the regular determinant with the ordinary discriminant for smooth XA; Theorem 3.2, pp.361–362, giving alternating massive vectors as vertices; Theorem 3.4(a), p.363, giving the secondary fan refinement; and Proposition 3.7, p.365, explicitly identifying the normal cone at the D-equivalence vertex as the union of the corresponding triangulation cones. These are established imported theorems; this review does not claim to reprove all their algebraic foundations.

Chapter 11 Theorem 3.2 assumes simplicity (or dimension at most three) and index one on every face. Here the product polytope is Delzant. At a Delzant vertex, its primitive edge vectors form a lattice basis, and their first lattice steps belong to the complete set of lattice points in Q. The primitive edges within a face generate the induced face lattice. The same is true for the product with the standard simplex. Consequently, the candidate's full induced face normalization agrees with the lattice normalization in GKZ, and the required face indices are one. The embedded product variety is smooth. This is stronger than quasi-smoothness: Chapter 11 Theorem 1.6 gives polynomiality in the quasi-smooth case but explicitly does not give equality with the ordinary discriminant there. Replacing smoothness by mere simplicity/index-one is an unsupported extension.

## Height sign and the precise vertex label

GKZ Chapter 7 defines its coherent heights using the upper hull and concave interpolation. Its Definition 1.4, p.219, and Theorem 1.7(c), p.221, identify those cones with maximizing normal cones of the secondary polytope. Therefore a lower height h in the candidate corresponds to the book's upper height -h. Maximizing against -h is minimizing against h. No reversal of the claimed minimizer is needed.

The label is more than an unlabelled fan refinement. Proposition 3.7 gives the label explicitly. An alternative derivation checks it directly: Chapter 11 Theorem 1.3(b) expresses the regular determinant as the alternating product of the principal determinants of the face configurations, with sign given by face codimension. Chapter 10 Theorem 1.4, p.302, gives the leading principal-determinant monomial for each coherent face triangulation. Under a generic height, every factor has a unique leading monomial. Taking the alternating product subtracts or adds their exponent vectors. Each face contributes exactly its top-dimensional massive simplices, so the result is the alternating massive vector m_U. Leading monomials multiply and divide in the fraction field. Theorem 3.2 guarantees that in this case the regular determinant is a polynomial and that the resulting coefficient is nonzero. Thus m_U is the actual minimizing discriminant exponent. This derivation does not use the Hurwitz equality or Sano's analytic support formula.

For a height on a wall, choose one perturbation direction away from the finite circuit hyperplanes. The combinatorial signs are constant for all sufficiently small positive perturbations. Hold the resulting triangulation fixed. Its minimizing inequalities persist as the perturbation tends to zero. This yields a weak minimizing face and does not incorrectly assert uniqueness on the wall.

## Product refinement and unused points

For generic w on A, the lower convex envelope g_w has triangulation T as its domains of linearity. For equal-column heights on B, any convex representation of (x,y) has total height at least g_w(x). Multiplying a realizing convex combination for x by the simplex barycentric coefficients of y attains that value. The lower cells are precisely the products of the T simplices with the standard simplex.

All A-points unused by a generic T lie strictly above its lower envelope. Their finitely many positive gaps stay positive under a sufficiently small perturbation. Thus they cannot appear as vertices of the refined lower cells. The same applies to their copies in B. The perturbation refines the old product cells: the supporting inequalities with nonzero gaps retain their signs, while the tied cell configurations are triangulated by generic circuit signs. No assertion that every triangulation of P is a product triangulation is involved.

## The finite product identity

For a j-simplex sigma in a j-face of Q and an l-face E of the standard simplex, k=j+l. The product lattice is the induced lattice, E has normalized volume one, and the normalized product volume is binom(k,j) times Vol(sigma). The affine barycentric coordinate associated to a vertex a of sigma takes values zero or one on every allowed product vertex. Volume-weighted centroid additivity over a finite simplex subdivision then gives total incidence-weighted volume

    (k+1)/(j+1) * binom(k,j) * Vol(sigma)
    = binom(k+1,j+1) * Vol(sigma).

This is a finite valuation identity, with no K-energy or asymptotic formula. Summing over the binom(n,l+1) simplex faces, and over the unique j-faces supporting each massive simplex, gives original equation (6). Lower-dimensional overlaps have zero k-volume and cause no duplicate k-simplex contributions. Nonunimodular cells retain their full volume factor. Unused points contribute zero on both sides.

Taking the alternating massive sum gives coefficient c_(n,j) in equation (9). Its nth forward difference is that of binom(j+r,j+1), a polynomial of degree j+1. It vanishes for j<=n-2. For j=n-1 the nth difference is one with the outer negative sign; for j=n it is binom(n,1)=n. Hence every permitted product refinement has projection n*eta_(T,n)-eta_(T,n-1). The n=1 case reduces to the interval discriminant vector eta_(T,1)-eta_(T,0), including coarse triangulations that omit interior lattice points.

## Both inclusions, without circularity

Each regular T has a sufficiently small generic product refinement U. The GKZ theorem puts m_U in the discriminant polytope, so its projected identity proves H(Q) is contained in pi D(P).

For every generic testing w in the smaller coordinate space, the refinement U above gives a minimizing m_U at the equal-column height. The functional at that height is exactly the pullback of w under pi. Therefore the minimum over pi D(P) is attained at the corresponding Hurwitz model vector. That vector is in H(Q), so the two minima are equal. The minima of fixed compact polytopes are continuous in w; generic w is dense because the exceptional set is contained in finitely many circuit hyperplanes. Equality of all minima gives equality of the closed convex polytopes by separation.

Sano's established analytic theorem is not used to supply the minimizing inequality, a normal cone, or a target polytope inclusion. It identifies the source's named Hurwitz model and its smooth scope. If one wants to deduce the Hurwitz model theorem afresh from the comparison, the independently known geometric identification of the Hurwitz form with the Segre hyperdiscriminant may be used solely for that naming step; it is not the combinatorial comparison argument itself. The resulting proof is combinatorial within the established GKZ framework. It does not replace the foundations of discriminants and their Newton polytopes.

## Boundary of the finding

The proof does not address arbitrary singular XA, incomplete or sparse embeddings, lattice-index defects, or foundation-free combinatorics. Degree at least two ensures the geometric hyperdiscriminant is a nonconstant hypersurface under the source's hypotheses; degree-one/constant-discriminant conventions are not required for this scoped conclusion. The ordinary dual of X can be defective without defeating the relevant Segre hyperdiscriminant, whose existence under this scope is an imported established source result. The argument allows nonextreme projected vertices and does not prove that every regular product triangulation produces an extreme projected point. Neither this audit nor the finite controls certify historical novelty or the problem's current literature status.

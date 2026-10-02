# Turn 3: local isolation for a general smooth primal surface of every degree at least three

AI-assisted mathematical proof candidate; independent review pending. Third author turn. The deformation-to-quadric argument is explicitly credited to Kaminski, Fryers and Teicher, Recovering an algebraic curve using its projections from different points, JEMS7 (2005),145–172, Proposition4, printed153, https://ems.press/content/serial-article-files/31537 . Their theorem concerns projections of one curve. We rederive the differential implication for actual surface frontier points, and use their polar complete intersection to verify its hypothesis. We do not transfer the paper's global curve result to arbitrary silhouette solutions.

## 1. Generic geometric data

Let X=V(f) be a general smooth degree-d surface in P3_C, d>=3. Choose two general distinct centers outside X. By a projective coordinate change use coordinates (x:y:z:w) and cameras

pi1(x,y,z,w)=(x,y,z), pi2(x,y,z,w)=(x,y,w).

The centers are c1=(0,0,0,1), c2=(0,0,1,0), and their baseline B is {x=y=0}. The true fundamental matrix F0 has entries (F0)12=1,(F0)21=-1 and all others zero, up to scalar.

A smooth point p of X has a tangent plane containing both centers exactly when

f(p)=f_z(p)=f_w(p)=0.

Denote this frontier scheme by Z. For general choices it is a reduced complete intersection of degrees (d,d-1,d-1), with d(d-1)^2 points, none on B. The tangent planes are distinct, the corresponding points on both apparent contours are smooth, and the intersections of the dual contours with their epipolar pencil lines are simple.

Here the genericity assertions have the following standard geometric justification. The polar linear system on a smooth X has no base points. Its associated Gauss morphism pulls back O(1) to the ample O_X(d-1), hence is finite (a contracted curve would have degree zero for this ample bundle). In characteristic zero, successive general polar divisors are transverse by Bertini/generic smoothness. A general line in dual P3 avoids the at-most-one-dimensional singular and parabolic/bitangent loci of the general dual surface, and meets its smooth locus transversely. The two general camera planes through it give ordinary contour tangencies. Equivalently these are the ordinary, non-event configurations in the primary contour-duality source, Kohn–Sturmfels–Trager, Proposition4.2 and surrounding discussion. Centers may be selected generally along the baseline to avoid the finitely many additional bad contact directions. These are open conditions; none requires assuming the desired epipolar rank.

## 2. No quadric through the baseline and frontier scheme

The saturated ideal of the reduced projective complete intersection Z is (f,f_z,f_w). Indeed these form a homogeneous regular sequence of height three; its one-dimensional graded quotient is Cohen–Macaulay and has no irrelevant torsion, hence the ideal is saturated. Reducedness of the projective scheme then identifies it with the vanishing ideal of these points.

If d>=4, every generator has degree at least3. Consequently no nonzero quadric vanishes on Z, even without requiring it to contain B.

If d=3, the degree-two part of the ideal is exactly the span of f_z and f_w. Restricting to B gives the two partial derivatives of the binary cubic f(0,0,z,w). They are linearly independent whenever that binary cubic is not a pure cube of one linear form: a linear dependence of its derivatives says the polynomial is constant along one nonzero direction, so after a linear coordinate change it is a multiple of the cube of the other coordinate. A general baseline has squarefree nonzero cubic restriction and therefore independence. No nonzero combination of f_z,f_w vanishes identically on B. Thus also for d=3 there is **no nonzero quadric containing Z union B**.

This is a statement about the actual frontier points of the true smooth surface, not arbitrary matched tangencies at another compatible F.

## 3. An infinitesimal epipolar deformation would produce such a quadric

Keep both contour curves fixed. Because the tangency divisors at the true solution are reduced and their contact points smooth, individual epipolar tangencies and contact points have holomorphic local branches as the epipoles move. A local compatibility deformation pairs the corresponding branches; the permutation is locally constant. Let v1(p),v2(p) be their image point branches for each p in Z, and let dotF be any Zariski tangent vector to the rank-two compatibility locus at F0. These branch equations can equivalently be differentiated over the dual numbers, so the argument covers tangent vectors which do not integrate to curves.

The equation v2^T F v1=0 differentiates to

dotv2^T F0 v1 + v2^T dotF v1 + v2^T F0 dotv1 = 0.

Each dotvi is tangent to its fixed image contour. At an epipolar contact the corresponding epipolar line is precisely that tangent line; hence the first and third terms vanish. This includes the projective lift's scalar derivative because the point itself lies on the tangent line. Therefore

pi2(p)^T dotF pi1(p)=0 for every p in Z.

The tangent equation to det(F)=0 at F0 is dotF33=0. It says the quadric

Q_dotF(x,y,z,w)=(x,y,w) dotF (x,y,z)^T

vanishes identically on B. Written explicitly it is

dotF11*x²+(dotF12+dotF21)*xy+dotF22*y²+dotF13*xz+dotF23*yz+dotF31*xw+dotF32*yw.

These seven monomials are a basis for quadrics containing B. Thus the map from the tangent space of the rank-two matrix cone to these quadrics is onto and its kernel is exactly the line spanned by F0. It induces an isomorphism on projective tangent spaces. By Section2, Q_dotF=0; hence dotF is a scalar multiple of F0 and the projective tangent vector is zero.

The local compatibility scheme consequently has zero tangent space. Its local ring is C by Nakayama's lemma, so the true fundamental matrix is an isolated reduced solution. Equivalently, the full extended-Kruppa coefficient system has differential rank seven there.

## 4. Result and precise limitation

For every d>=3, at a general smooth degree-d primal surface and general distinct cameras, the true epipolar geometry is locally uniquely determined by the pair of exact full algebraic contours. This supplies the local smooth-primal transversality missing from the imported report. The proof uses all complex frontier points, not only the two visible outer tangencies of a convex real silhouette.

No global uniqueness or finiteness of every algebraically compatible F follows from this local statement alone. At another solution the reconstructed matched points need not lie on the true surface or its polar complete intersection. Applying Section2 there would be invalid. Nor does the theorem assert a stable numerical procedure for noisy or clipped data. Quadrics d=2 remain ambiguous, consistently with the credited conic theory.

## 5. Exact supplementary controls

The checker verifies the canonical matrix-to-quadric linear map and its one-dimensional kernel, evaluates it at rational points, checks the cubic derivative restriction test for a finite collection of cubics, and computes the degree-two dimensions predicted by the complete-intersection generators. These are finite controls; the transversality and complete-intersection proofs above establish the general assertions. Classical deformation, polar and Jacobian ingredients are credited; there is no novelty certification.

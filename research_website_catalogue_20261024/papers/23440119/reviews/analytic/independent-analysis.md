# Independent analytic reconstruction (early sealed artifact)

Record: Zenodo 23440119, DOI 10.5281/zenodo.23440119, version 1.0.0 dated 17 October 2026. Reviewer lane: analytic; GPT-6.1 Sol, Ultra as assigned; no children.

This document was completed before any deposited verification script, verification output, earlier review, favorable audit, or other review family's scientific opinion was inspected. Its inputs are the actual five-page manuscript and original primary literature definitions/attributions. The original PDF was read fully as extracted text and all five pages were visually inspected. The fresh Zenodo PDF is byte-identical to the initial local copy.

Original sources bound to this analysis:

- PDF SHA-256: `ad9864c08642737e4459673749c1db6d2e3dafb521f323fb1071f157f8110eb0` (73062 bytes).
- ZIP SHA-256: `d97ba7ed1057518e3bd499d88182c64767e912d589ed8574092c0ebc7a27c06e` (134250 bytes). It has not yet been used scientifically at this early seal.
- Intake raw record SHA-256: `5bd50929ec74a1f59373a01d7a07c970fded3fef0febc1da8915e96903255a4b`; intake receipt retrieval 2026-10-25T05:22:38.577833+00:00.

## Literal target and success criteria

Let p(x,y,z)=xy^2-z^3 and K={(x,y,z) in R^3: x,y,z>=0, p>=0}. Theorem 1 says:

1. K is closed, convex, pointed, conic, with nonempty interior, and is defined by homogeneous polynomial inequalities.
2. For every a in int K, F(a)=25[-log p(a)-log z] is a normal barrier with parameter 100: C^3, convex and closed after extension by +infinity outside int K, boundary-divergent, self-concordant, and F(lambda a)=F(a)-100 log lambda for every lambda>0. The paper also asserts the gradient dual-norm identity equals 100 at every interior a.
3. For every a in int K, every h in the *closed* cone K, and every u in all of R^3, D^3 F(a)[h,u,u]<=0. This is stronger than checking h=u, checking h interior, checking only finite samples, or checking Hessian convexity.
4. There do not exist a homogeneous real polynomial H in three variables and a real vector e with H(e)>0 such that every univariate H(v+te), v in R^3, has only real roots and its closed hyperbolicity cone is exactly K. H has no degree restriction and need not equal p or zp.

The abstract's existential interpretation is checked against Tunçel's original Open Problem 1, whose stated algebraicity means homogeneous polynomial inequalities. No claim about every regular cone, spectrahedral projections, hyperbolic affine spheres, optimal barrier parameter, or exhaustive first priority is substituted for these targets. Success requires universal analytic arguments with exact identities and complete boundary cases; samples cannot supply it.

## 1. Geometry

For x,y>0 let m=x^(1/3)y^(2/3). Direct second differentiation gives

    Hess m = -(2/9)x^(-5/3)y^(-4/3) [ [y^2,-xy],[-xy,x^2] ].

The matrix is the outer product (y,-x)(y,-x)^T, hence nonnegative. Thus m is concave; its continuous extension is concave on the closed orthant (approximate both arguments by positive arguments in Jensen's inequality). The hypograph z<=m intersected with z>=0 is convex and equals K. The displayed defining inequalities prove closedness and positive homogeneity; K intersect (-K)={0} follows from nonnegative coordinates; (2,1,1) is strictly feasible. Every strict point x,y,z>0, p>0 has an open feasible neighborhood. Conversely a point with any zero coordinate or p=0 lies on a defining boundary and has no open feasible neighborhood. Thus int K is exactly the strict locus the paper uses. In particular, the origin, flat face z=0, and axis edges are included in K but not its interior.

## 2. Normality reconstructed through the slack

At a fixed interior base define g=z^3/y^2>0 and delta=x-g>0, so f=-log delta-2log y-log z. For a direction d put b=dy/y, c=dz/z, w=[dx-g(3c-2b)]/delta, v=sqrt(6g/delta)(c-b), ell=c-4b. These are linear forms in d at the fixed base.

The expansion (1+c epsilon)^3(1+b epsilon)^(-2) gives

    Dg=g(3c-2b),
    D^2g=6g(c-b)^2,
    D^3g=6g(c-b)^2(c-4b).

Consequently delta'=delta w, delta''=-delta v^2, delta'''=-delta ell v^2. The elementary logarithm chain rule yields

    D^2 f[d,d]=w^2+v^2+2b^2+c^2,
    D^3 f[d,d,d]=-2w^3-3wv^2+ell v^2-4b^3-2c^3.

The first is positive definite, because zero forces b=c=w=0 and then d=0. This proves convexity on the convex interior and ensures inverse Hessians exist.

Polarization of the cubic gives exactly the manuscript's mixed expression. With N(d)^2=w_d^2+v_d^2+2b_d^2+c_d^2, weighted Cauchy-Schwarz gives |ell_d|<=3 sqrt(2b_d^2+c_d^2)<=3N(d). The four groups have respective upper bounds 2,3,3,2 times N(h)N(u)^2:

- |-2 w_h w_u^2|<=2 N(h)N(u)^2.
- |w_h v_u^2+2w_u v_h v_u|<=3 N(h)N(u)^2 (bounding each product suffices).
- (|ell_h|v_u^2+2|ell_u v_h v_u|)/3<=3 N(h)N(u)^2.
- |4b_h b_u^2+2c_h c_u^2|<=2 sqrt(2b_h^2+c_h^2)sqrt(2b_u^4+c_u^4)<=2N(h)N(u)^2. The last inequality follows by expanding (2b_u^2+c_u^2)^2>=2b_u^4+c_u^4.

Therefore |D^3 f[h,u,u]|<=10N(h)N(u)^2. For F=25f, its norm is 5N, and the bound becomes 250N(h)N(u)^2=2||h||_F||u||_F^2. This is the mixed definition in Dahl-Tunçel-Vandenberghe Section 2.2 and implies the scalar standard inequality. The constant 100 is not claimed optimal.

Since zp has homogeneous degree four, F(lambda a)=F(a)-100log lambda. Differentiating gives Hess F(a)a=-grad F(a), while a^T Hess F(a)a=100. Thus grad F^T(Hess F)^(-1)grad F=100 exactly, and Cauchy-Schwarz gives the gradient inequality in every direction if required.

At a finite boundary limit, continuity gives zp=0: if z>0 and p>0, the nonnegative constraints force x,y>0 and the point would be interior. Along an interior sequence the product is positive and tends to zero, hence F tends to +infinity. The extension by +infinity is convex (convex interior plus convex f) and lower semicontinuous at the boundary; points outside the closed cone have neighborhoods disjoint from the domain. Thus it is closed. The definition of normal barrier in Nesterov-Tunçel, equations (1.3),(1.9), matches this use. Boundary at infinity is not part of the finite-boundary requirement.

## 3. Universal negative curvature reconstructed from the generic log formula

A positive diagonal D=diag(alpha,beta,gamma) with alpha beta^2=gamma^3 preserves K, its interior, and arbitrary u under invertible transport. It satisfies f(Dq)=f(q)-4log gamma. Holding D fixed while differentiating, the trilinear derivative transports by D. At any base (x,y,z) choose D=diag(y^2/z^3,1/y,1/z); this sends it to (r,1,1), r=xy^2/z^3>1. No global transitivity assumption is needed; r is retained.

For h in K and h_y>0, set t=h_z/h_y>=0. Then

    h=h_y(t^3,1,t)+(h_x-h_z^3/h_y^2)e_x,

with nonnegative coefficients by h_x h_y^2>=h_z^3. If h_y=0, necessarily h_z=0 and h=h_x e_x. This exhausts all cone directions including zero, t=0, and both coordinate axes. Linearity in h makes these generators sufficient.

For h=(t^3,1,t), s=r-1, independently construct the curvature matrix as follows:

    n=grad p=(1,2r,-3),
    B=Hess p=[[0,2,0],[2,2r,0],[0,0,-6]],
    A=Dp[h]=t^3+2r-3t,
    b=B h=(2,2t^3+2r,-6t),
    C=D(Hess p)[h]=[[0,2,0],[2,2t^3,0],[0,0,-6t]].

The generic chain rule, independently of the manuscript's expanded entries, gives

    M=-s^3 D^3 f[h]
     =2A nn^T-s(bn^T+nb^T+AB)+s^2 C+2s^3 t e_z e_z^T.

Expanding gives all six displayed manuscript entries. My independently written, standard-library sparse-integer-polynomial program checks all six identities, the two minor identities, the two square identities (with division cleared), the shift of the remainder, and the separate endpoint and Gram identities exactly. No rational/numerical tolerances occur.

Writing P and R literally as in the paper, those identities imply M_11>0 for t!=1, the second leading minor equals 4s(t-1)^2P, and det M=8s^4(t-1)^2R. For 0<=t<1 all terms in P and in R/(t+2) are nonnegative, their constant terms strictly positive. This includes t=0 where R=6(s+1)>0 despite the zero coefficient on s^2. At t=1, P=R=6s^2>0. For t>1 the square decompositions have strictly positive remainders: the P remainder becomes 8v^3+45v^2+72v+24>0 at t=1+v, and the R remainder is 3(t-1)^3(8t^2+13t+3)>0. Its divisor 8t/(t+2) is positive there; it is not used at t=0. Hence all three leading minors are positive for t!=1 and Sylvester's positive-definite criterion applies.

At t=1 the matrix is 2s^2 times diag(0,L), where

    L=[[2r+1,-3],[-3,r+2]], det L=(r-1)(2r+7)>0.

It is nonnegative of rank 2, with nullspace precisely span(e_x). Strict Sylvester cannot be used at this point, but the paper explicitly supplies this separate block certificate. For h=e_x the direct chain rule yields

    -s^3 D^3 f[e_x]=2(1,2,-3)(1,2,-3)^T
                         +6s(0,1,-1)(0,1,-1)^T >=0.

These are independent of any limit t->infinity. The zero direction gives zero. Strict bases s>0 are the full required domain; s=0 is outside it and is not silently divided through. Congruence transport, nonnegative sums, and positive scaling by 25 prove D^3 F(a)[h,u,u]<=0 for exactly the full stated quantifiers.

## 4. Excluding arbitrary hyperbolicity polynomials

Assume H is homogeneous, hyperbolic in e, H(e)>0, and its closed cone equals K. Its degree is arbitrary. e belongs to int K, so e_x,e_y,e_z>0 and p(e)>0. The boundary of a hyperbolicity cone lies in H=0: roots of H(x-lambda e) have a fixed nonzero leading coefficient; continuity from the positive-root region gives nonnegative roots on its closure, and all roots strictly positive would be an interior point. Thus every curved boundary point (z^3/y^2,y,z), y,z>0, vanishes under H.

Multiply H(z^3/y^2,y,z) by a sufficiently large power of y to clear denominators. A polynomial vanishes on the nonempty open positive quadrant and hence identically. The remainder theorem over R(y,z) gives (x-z^3/y^2)|H. The primitive polynomial y^2x-z^3 is irreducible over R(y,z)[x] because it is linear there; its content over R[y,z] is 1 since gcd(y^2,z^3)=1. Gauss's lemma therefore gives p|H in R[x,y,z]. This rules out an escape by using extra inequalities, a higher degree H, or multiplying p by another factor.

For the fixed v=(0,0,1), put a=(e_x e_y^2)^(1/3)>b=e_z>0. Then

    p(v+te)=a^3t^3-(1+bt)^3
     =[(a-b)t-1][(a^2+ab+b^2)t^2+(a+2b)t+1].

The quadratic discriminant is -3a^2<0. Since p(e)>0 and H(e)>0, the restricted p and H are nonzero polynomials of their expected degrees; polynomial multiplication cannot cancel the nonreal roots contributed by p. H(v+te) therefore violates hyperbolicity. Every prospective e is covered, not just a chosen direction.

This is a polynomial-hyperbolicity obstruction. Hildebrand's phrase hyperbolic affine sphere is a differential-geometric use of the word and does not imply existence of H.

## 5. Corollaries, falsification attempts, and limits

The manuscript's supplemental diagnostic for f_0=-log p at base (5,1,1), h=(8,1,2), is independently reproducible: subtracting 2s^3t from the (3,3) entry of M, then s=4,t=2, gives determinant -24576. Thus the -log z term is substantive for this displayed certificate. This is an exact counterexample to unaugmented negative curvature, not a counterexample to Theorem 1.

Attempts aimed at hidden assumptions: domain axes; h_y=0; h=0; t=0; t=1; s down to 0; arbitrary u; fixed-versus-varying normalization; positive-definite-versus-semidefinite criteria; the gradient bound; closedness of the extended barrier; arbitrary-degree H; arbitrary e; product-factor cancellation; curved boundary denominators; and primitive irreducibility. None yields a substantive gap in the literal theorem. The proof needs no empirical or model assumptions, approximate numerics, optimization solver, or external input.

Primary definitions independently read: Tunçel's three-page author manuscript including Open Problems 1 and the hyperbolicity/normal/negative-curvature context; Nesterov-Tunçel Sections 1 and 6 definition and equivalences; Dahl-Tunçel-Vandenberghe Sections 2.2, 3.1, 6; Hildebrand Theorem 3.2 family 5 including its displayed family and context; Roy-Xiao definition and Theorem 2 formula. With (p,q)=(3,3/2), (x1,x2,x3)=(x,z,y), Hildebrand's family agrees exactly. Roy-Xiao with n=2, alpha=(1/3,2/3) gives exactly the parameter-3 B displayed on manuscript page 2. Those two are attribution/comparison checks, not logical dependencies of the self-contained construction. No exhaustive priority conclusion follows.

Independent conclusion at early seal: the literal main mathematical theorem is supported by a complete analytic proof, with exact verification artifacts; no substantive defect found. This is an independent AI review, not external human review or proof-assistant certification. Final review still requires full deposited-support inspection, primary provenance binding, and an integrity seal. Publication clearance is false; only the parent/human process can make a publication decision. Follow-up recommendation is null under the high-bar default.

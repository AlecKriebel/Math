# Fixed-camera curve compatibility with epipole base divisors

Alec Kriebel, with AI assistance. 4 October 2026.

**Disposition: unsolved.** This is an unrefereed, scoped algebraic result, not a resolution of every meaning of AIM Algebraic Vision Problem 1.25. No novelty or priority claim is made. The clean fiber-product argument and gcd bound are established background. The principal additional calculation recorded here is a divisor-overlap formula for the degree of each triangulated component and the multiplicity of the baseline when image curves contain epipoles.

## 1. Scope and notation

Work over an algebraically closed field k of characteristic zero. A camera is a rank-three linear rational map P^3 --> P^2. Fix two cameras with distinct centers. Independent projective changes of world and image coordinates put them in the form

    P[a:b:s:t] = [a:s:t],    Q[a:b:s:t] = [b:s:t].                 (1)

Indeed, the centers can be chosen as two basis vectors; the two-dimensional space of linear forms vanishing at both centers supplies the common coordinates s,t. The centers are cP=[0:1:0:0] and cQ=[1:0:0:0]. Both image epipoles have coordinates e=[1:0:0]. The baseline is L=V(s,t), and T=P^1 with coordinates [s:t] parametrizes its plane pencil.

Let X=V(f) and Y=V(g) be integral, reduced projective plane curves of degrees m,n. Their normalizations are Xbar,Ybar. Write alpha=mult_e(X), beta=mult_e(Y), taking multiplicity zero when e is absent. These are plane-curve multiplicities. They are not camera-center multiplicities of a reconstructed curve.

An integral world realization means an integral reduced curve C in P^3 with the Zariski closures of its rational P- and Q-images equal to X and Y. C is allowed to pass through camera centers. A birational realization has both rational projections of degree one. These definitions do not require real points, positive depth, a chosen world degree, or a smooth embedded world curve.

On Xbar, the sections s,t of nu_X^*O_X(1) have a common effective zero divisor E_X. Its coefficient at a branch over e is min(ord(s/a),ord(t/a)). The sum of these branch multiplicities is alpha, since intersection with a general line through e computes the multiplicity of a reduced plane curve. Thus deg E_X=alpha. Define E_Y similarly, with degree beta.

Removing these fixed divisors gives morphisms

    rho_X:Xbar -> T,  rho_Y:Ybar -> T.

The map rho_X is constant exactly when X is a line through e. Otherwise it is finite, separable and has degree r=m-alpha>0. Similarly q=n-beta>0 for Y when Y is not an epipolar line. These assertions follow from the moving linear series of degree m-alpha and the fact that a nonconstant map of projective integral curves is finite.

Unless a section explicitly says otherwise, neither X nor Y is an epipolar line. No smoothness or general-position assumption on X,Y is imposed.

## 2. The proper correspondence, including singular images

Let D=Xbar x_T Ybar be the scheme fiber product. It is a reduced projective curve, finite and surjective over both factors. To see reducedness, the two finite maps to the smooth curve T are flat; the generic tensor product of their separable function fields is reduced. On the smooth surface Xbar x Ybar, D is a nonzero effective Cartier divisor, hence Cohen--Macaulay with no embedded associated points. Generic reducedness therefore gives reducedness. Each component dominates both factors: a finite morphism cannot map a one-dimensional component to a point.

For each irreducible component D_j, let Z_j be its normalization. **D is not generally normal**; normalizing the two factors does not normalize their fiber product. Put

    a_j=deg(Z_j -> Xbar),    b_j=deg(Z_j -> Ybar),
    h_j:Z_j -> T,           N_j=deg h_j.

The epipolar incidence open set with neither image an epipole is isomorphic to P^3 minus L. For instance, on the common t != 0 chart, an incident pair ([x:lambda:1],[y:lambda:1]) is sent to [x:y:lambda:1]. The s != 0 chart gives the other inverse, and the two agree. Consequently every Z_j triangulates birationally onto an integral world curve C_j. The rational map from Z_j extends to a morphism because Z_j is a smooth projective curve and P^3 is proper; Section 4 constructs it explicitly.

Conversely, every integral world realization is one of these C_j. Its joint image off L is a curve in the incidence correspondence; on the dense loci where the image normalizations are isomorphisms it determines a component of D. The open triangulation inverse forces the same world curve. Thus no further integral world curves are hidden between these finitely many components.

In particular, weak algebraic existence is automatic in this nonconstant-pencil regime. Birational realizability is equivalent to an isomorphism

    alpha_map:Xbar -> Ybar,    rho_Y o alpha_map = rho_X.         (2)

For necessity, normalize C and factor its degree-one projections through the normalizations of its images. Finite birational maps between smooth projective curves are isomorphisms. For sufficiency, the graph of (2) is a component of D and triangulates birationally to both images. Unlike in the epipole-avoiding regime, m=n is not necessary: (2) requires r=q, while m and n may differ.

## 3. Moving-degree component arithmetic

Let h=gcd(r,q). Degree multiplication gives r a_j=q b_j=N_j, whence there are positive integers k_j with

    a_j=(q/h) k_j,   b_j=(r/h) k_j,
    N_j=lcm(r,q) k_j,   sum_j k_j=h.                            (3)

The last equality follows because the reduced fiber product has total degree q over Xbar: sum a_j=q. This also proves that there are at most h components, and coprime moving degrees force one component.

This is the standard component-degree argument, not a new gcd theorem. Hidalgo--Reyes-Carocca--Vega, Proposition 2.6 [3], proves the gcd bound through the same lcm divisibility of monodromy-orbit sizes. Their proof supplies the partition immediately. Camera reconstruction via the epipolar fiber product already appears in the proof of Theorem 3 of Fryers--Kaminski--Teicher [2].

**Warning.** N_j is the moving pencil degree. It need not equal deg C_j. Equation (3) alone does not compute a world degree when an image meets an epipole.

## 4. Exact world degree and camera-center corrections

On Z_j define the effective divisors

    A_j = pullback(E_X),       B_j = pullback(E_Y).

Their degrees are alpha a_j and beta b_j. For two effective divisors, min and max are taken coefficient by coefficient on this same curve Z_j. It is not enough to compare their total degrees.

### Theorem 1 (divisor-overlap formula)

For every component above,

    deg C_j = N_j + deg max(A_j,B_j)                            (4)
            = m a_j + n b_j - N_j - deg min(A_j,B_j).

The fixed divisors of the two camera projections on the normalization of C_j are

    base(P|C_j) = (B_j-A_j)_+,
    base(Q|C_j) = (A_j-B_j)_+.                                  (5)

In particular,

    mult_cP(C_j) = deg(B_j-A_j)_+,
    mult_cQ(C_j) = deg(A_j-B_j)_+,                              (6)
    deg C_j - mult_cP(C_j) = m a_j,
    deg C_j - mult_cQ(C_j) = n b_j.

The fixed divisor of the baseline pencil [s:t] on C_j is max(A_j,B_j).

#### Proof

Write H=h_j^*O_T(1), and take its two basepoint-free generating sections S,T. The pullback of the image hyperplane bundle from X is H(A_j), and from Y is H(B_j). If d_A,d_B denote the canonical sections of O(A_j),O(B_j), the image maps can be written

    [x:d_A S:d_A T],       [y:d_B S:d_B T],

where x is a section of H(A_j), y a section of H(B_j). These triples have no common zero. The line-bundle isomorphisms may be chosen so that the displayed pairs agree with the given rho maps; any common scalar is absorbed in x or y.

Triangulation is represented by four sections of H(A_j+B_j):

    [x d_B : y d_A : d_A d_B S : d_A d_B T].                   (7)

At a point with coefficients u,v in A_j,B_j, if u>0 then x is a unit in a local frame, and if v>0 then y is a unit. Since S,T have no common zero, the common zero order of the four sections is exactly min(u,v). This remains true when u or v is zero: the corresponding other coordinate is a unit. Therefore cancellation of the common divisor min(A_j,B_j) makes (7) a basepoint-free morphism with hyperplane bundle H(max(A_j,B_j)). Its image is C_j and it is birational by the triangulation argument. Taking degrees proves (4).

After this cancellation, the P-coordinate triple has common order v-min(u,v)=(v-u)_+, and the Q-coordinate triple has common order (u-v)_+. This proves (5). For an integral space curve, the degree of the fixed divisor of all hyperplanes through a point equals its multiplicity at that point: on each normalization branch a general linear combination has the minimum order of the local coordinate functions, and summing those orders gives the general hyperplane intersection multiplicity. This proves (6). The same local calculation for s,t gives u+v-min(u,v)=max(u,v), proving the baseline assertion. QED.

### Corollary 2 (bounds)

    max(m a_j,n b_j) <= deg C_j <= m a_j+n b_j-N_j.              (8)

The upper equality holds exactly when A_j and B_j have disjoint support. Equality with the lower bound holds exactly when the smaller-total-degree divisor is bounded above coefficientwise by the other (either ordering is allowed when their degrees are equal).

When alpha=beta=0, (4) becomes deg C_j=N_j and recovers the imported clean-case law. If just one of alpha,beta is zero, the world degree equals the degree of the image-hyperplane bundle on the other side; it need not equal N_j.

## 5. Saturated cone intersection and the baseline cycle

Let

    I=(f(a,s,t), g(b,s,t)) in k[a,b,s,t],
    J=I:(s,t)^infinity.                                       (9)

### Theorem 3

Under the non-epipolar-line assumptions, I is a complete intersection of degrees m,n. J is radical and its projective irreducible components are exactly the world curves C_j. If ell is the cycle multiplicity of L in V(I), with ell=0 when L is not a component, then

    ell = alpha beta + sum_j deg min(A_j,B_j).                 (10)

Thus tangential overlap at the epipoles contributes beyond the product of their ordinary multiplicities.

#### Proof

The two cone polynomials are irreducible: f remains irreducible after adjoining b, and g after adjoining a. If they were associates, their common polynomial would be independent of both a and b, hence would be an irreducible binary homogeneous form. Over k this is linear and gives an epipolar line, excluded by hypothesis. They therefore form a regular sequence, and their projective intersection is pure one-dimensional with no embedded components.

Outside L, (9) identifies with the incidence construction on X x Y. Its generic points lie in the smooth loci of X and Y and in the separable, unramified parts of their pencil maps, so it is generically reduced. An irreducible component outside L cannot project to a point under one camera: it would be a camera ray, whose image under the other camera is an epipolar line. The assumptions exclude this. Hence these components all dominate both images and are precisely the C_j.

Saturation removes exactly the primary components supported on L. The other primary components have multiplicity one by generic reducedness; a primary ideal with generic length one is its prime ideal. This proves radicality of J and the asserted component list. No assertion is being made about the unsaturated scheme being reduced at L.

The complete-intersection cycle has degree mn. Its off-baseline components each have coefficient one. Summing (4) and using sum a_j=q, sum b_j=r, sum N_j=rq yields

    sum deg C_j = rq+alpha q+beta r - sum deg min(A_j,B_j)
                = mn-alpha beta - sum deg min(A_j,B_j).

Since deg L=1, subtracting from mn proves (10). If either epipole is absent, the corresponding divisor is zero and (10) gives ell=0, consistently with direct restriction to L. QED.

Equations (9) give a finite exact procedure over effective coefficient fields of characteristic zero: compute the saturation and its geometric minimal primes, then degrees and singular loci. An integral lift of a specified degree exists precisely when one of these components has that degree. An embedded smooth lift exists precisely when one of the component curves is smooth. Computing a smooth normalization alone does not establish smoothness of its embedded image. This procedural statement is not a new elimination algorithm or an efficient uniform complexity bound.

## 6. Exact examples distinguishing the corrections

All examples use the cameras (1). The script verifies homogeneous identities, ideal equalities after saturation, and the stated base-divisor arithmetic.

### 6.1 Unequal image degrees with birational projections

Let X have equation a=t, and let Y have equation b s=t^2. Then X avoids its epipole, while Y is a smooth conic through its epipole. Their degrees are 1,2, but r=q=1. The world conic is parametrized by

    [u:v] -> [u v : u^2 : v^2 : u v].                          (11)

Its P-image is [u:v:u] after cancelling v, and its Q-image is [u^2:v^2:u v]. Both are birational. It passes through cP once. Here N=1, deg A=0, deg B=1, so (4) gives degree 2. Equal ordinary image degrees are therefore not a necessary condition outside the clean regime.

### 6.2 Coincident epipole divisors: a double baseline

Take f=a t-s^2 and g=b t-s^2. Both images are smooth conics, alpha=beta=1 and r=q=1. Their epipole divisors pull back to the same point. The only proper world component is

    a=b,  a t=s^2,
    [u:v] -> [u^2:u^2:u v:v^2].                               (12)

Its degree is 2, whereas N=1. The raw intersection contains the baseline with multiplicity 2. At its generic point, a,b and a-b are units; subtracting the equations gives t=0 and then s^2=0, displaying length 2. Equations (4),(10) give 1+1=2 and 1+1=2 respectively.

### 6.3 Disjoint epipole divisors: a twisted cubic

Take f=a t-s^2 and g=b s-t^2. The two pulled-back epipole divisors are distinct points. The proper component is the twisted cubic

    [u:v] -> [u^3:v^3:u^2 v:u v^2].                            (13)

It has degree 3 and passes through each camera center once. At the generic baseline point, the linear parts a t and b s are independent, so the baseline is reduced, of multiplicity 1. Equations (4),(10) give degree 1+2=3 and multiplicity 1. Thus two ordinary degree-two images can have a degree-three birational realization.

### 6.4 A family testing arbitrary epipole orders

For m,n>=2 and integers 0<=i<m, 0<=j<n, set

    E=u^i v^(m-1-i),  F=u^j v^(n-1-j),
    A=u^m+v^m,         B=u^n+2v^n.

The image curves are a E(s,t)-A(s,t)=0 and b F(s,t)-B(s,t)=0. These are irreducible by primitivity and linearity in a or b. Their parametrizations [A:E u:E v] and [B:F u:F v] are basepoint-free and birational because their pencil coordinate is [u:v]. Thus their degrees are m,n, their epipole multiplicities are m-1,n-1, and r=q=1.

Their unique proper world component is represented before cancellation by

    [A F:B E:E F u:E F v].

The exact common factor is gcd(E,F). Hence its degree is

    m+n-1-min(i,j)-min(m-1-i,n-1-j),                           (14)

and (10) predicts baseline multiplicity (m-1)(n-1) plus the two displayed minimum terms. This checks both common-basepoint cancellation and unequal center orders. The finite computations do not replace the universal proof above.

### 6.5 A fiber product of normal factors can be nonnormal

The clean smooth conics a^2=s t and b^2=s t yield two conics a=b and a=-b. They meet at [0:0:1:0] and [0:0:0:1]. On the t=1 chart the local equation is a^2-b^2=0, a node in characteristic zero. Thus D has smooth factors but is not normal. Z_j in this note means the normalization of an actual component, not merely a fiber product of normalizations.

## 7. The constant-pencil and coincident-center cases

These elementary cases complete the weak-existence criterion for integral images and rank-three cameras, under the algebraic definition in Section 1.

If exactly one image is an epipolar line, there is no integral world realization. For if there were one, its common pencil map would be constant from that image and nonconstant from the other. If both images are epipolar lines, a realization exists exactly when they belong to the same epipolar plane. In that case a line in that plane avoiding the two centers realizes both birationally. If the pencil parameters differ, no world point off L can project to both curves densely.

If the cameras have the same center, there is an invertible projective transformation H with Q=H P. Existence is then equivalent to Y=H X. A hyperplane avoiding the center identifies with the first image plane under P, and the lifted plane curve gives a birational realization. A rank-deficient linear map is not a camera in the convention used here.

These statements do not classify realizations by arbitrary prescribed degrees in the constant-pencil or coincident-center cases, or handle nonreduced/reducible images under every possible reconstruction convention.

## 8. Why branch data and base field cannot be suppressed

### 8.1 Known branch-data obstruction, with an independent exact enumeration

Over C, six distinct simple branch values admit 40 isomorphism classes of connected degree-three covers of genus one. This is established classical material, discussed in Corollary 2.5 of Agostini et al. [5], not a contribution of this note. The verifier independently enumerates the corresponding six-tuples of transpositions in S3: product identity, transitive generated action, modulo simultaneous conjugation. It finds 240 tuples, 40 orbits, all of size 6.

By Riemann existence and Riemann--Hurwitz these are nonisomorphic covers with identical simple branch divisor. A degree-three line bundle on a smooth genus-one curve is very ample, and the two-dimensional pencil defining the cover sits in its three-dimensional complete linear series. Thus they are realizable as projections of smooth plane cubics from a point outside the cubic. Choosing any two distinct classes shows that equality of epipolar branch divisors does not imply birational fixed-camera compatibility. This blocks a branch-discriminant-only replacement for (2).

### 8.2 Real quadratic twists already obstruct birational compatibility

Over R, take the clean smooth conics

    X:a^2=s t,       Y:b^2=-s t.                               (15)

Their branch values coincide, and over C the two covers are isomorphic by b=i a. Over R their function fields over the pencil are R(z)(sqrt(z)) and R(z)(sqrt(-z)), which are distinct quadratic extensions because -1 is not a square in R(z). Hence there is no real birational realization. Both image conics have nonempty real loci. Their canonical world intersection has only the two real points [0:0:1:0] and [0:0:0:1], since its equations imply a^2+b^2=0. In particular it has no real world arc realizing either full real image curve.

There can even be no real world point: the clean smooth real conics

    a^2+s^2=t^2,       b^2+(s-3t)^2=t^2                        (16)

have real pencil ranges [-1,1] and [2,4] on t=1, and neither has real points at t=0. Their complex fiber product exists, but there is no real incident pair. This separates existence of a complex algebraic reconstruction, existence of an R-defined curve, and a visible real reconstruction.

### 8.3 Inseparability changes the component count

In characteristic 2, the clean smooth conics a^2=s t and b^2=s t have inseparable degree-two pencil maps. Their intersection contains (a-b)^2=0 and is a double conic, not a reduced union. Counting reduced components gives sum k_j=1 instead of gcd(2,2)=2; the generic multiplicity 2 restores the cycle-weighted equality. The characteristic-zero hypothesis is used precisely to avoid this inseparable failure. No wild-ramification extension is claimed.

## 9. What remains unresolved and what is actually checked

The source question does not define a single compatibility predicate. This note gives rigorous criteria for integral reduced algebraic realizations over an algebraically closed characteristic-zero field, including epipole and center degeneration, and explicit tests distinguishing several other meanings. It does not certify a full answer for arbitrary real visible arcs, uncertainty/noise, nonreduced image schemes, general reducible reconstruction conventions, or prescribed-degree/smoothness classification in every degenerate camera regime. It does not infer smoothness of an embedded curve from its normalization. These qualifications prevent changing the broad AIM record to a solved status.

The finite verifier checks polynomial identities and saturation examples, a rational family with varying epipole orders, generic-baseline local lengths, the known 40-class monodromy count, and field-sensitive counterexamples. It is not a formal proof assistant, does not establish priority, and does not enumerate every integral image pair.

## References and provenance

[1] AIM, Algebraic Vision, Reconstruction, Problems 1.25 and 1.4. http://aimpl.org/algvision/1/ . The live source was inspected on 4 October 2026. The imported title describes an AI partial rather than the original question.

[2] M. Fryers, J. Y. Kaminski, M. Teicher, Recovering an Algebraic Curve Using its Projections From Different Points. Applications to Static and Dynamic Computational Vision. arXiv:math/0208099, Theorem 3 and its proof; journal version DOI 10.4171/JEMS/25. https://arxiv.org/abs/math/0208099 . The paper explicitly uses the epipolar fiber product and monodromy to obtain the generic true/ghost decomposition.

[3] R. A. Hidalgo, S. Reyes-Carocca, A. Vega, On the fiber product of Riemann surfaces, arXiv:1611.07880, Proposition 2.6. https://arxiv.org/abs/1611.07880 . The gcd component bound and its orbit-degree argument are prior work.

[4] F. Rydell, I. Sundelius, Projections of Curves and Conic Multiview Varieties, arXiv:2404.03063, Sections 3 and 4.1. https://arxiv.org/abs/2404.03063 . Back-projected cones and equations for conic-image compatibility are prior work.

[5] D. Agostini, H. Markwig, C. Nollau, V. Schleis, J. Sendra-Arranz, B. Sturmfels, Recovery of Plane Curves from Branch Points, arXiv:2205.11287, Corollary 2.5 and Section 3; Discrete & Computational Geometry 72 (2024), 451--475, DOI 10.1007/s00454-023-00538-5. https://arxiv.org/abs/2205.11287 . The 40-count and branch-data nonuniqueness are expressly credited.

The UnsolvedMath imported reports for numeric IDs 20000185 and 20000188 were read as untrusted research aids. They already contain the clean correspondence/cover criterion, moving degrees and necessary center-degree identities. This note is not an independent discovery claim for those statements. Its proof of the overlap calculation is included in full for checking. Source PDFs, source-page copies, and corpus contents are not redistributed.

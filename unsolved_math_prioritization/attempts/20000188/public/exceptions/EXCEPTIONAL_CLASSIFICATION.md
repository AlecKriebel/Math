# Exceptional epipolar images and projection-degree bookkeeping

Author-created mathematical analysis, shared pass 1/5, 2026-10-16. Scope is exactly CONTRACT.md: complex, two fixed distinct rank-three pinhole cameras, reduced integral image and world curves, closure of rational images. This is a case-completion theorem within that residual, not a novelty claim or resolution of every interpretation of the AIM question. No third-party source text is included.

## 1. Coordinate convention

After projective coordinate changes, write

- world coordinates [x0:x1:x2:x3];
- centers A=[1:0:0:0], B=[0:1:0:0];
- pi1=[x1:x2:x3], pi2=[x0:x2:x3];
- baseline L={x2=x3=0};
- image epipoles e1=e2=[1:0:0].

The epipolar plane with parameter [s:t] is {t*x2-s*x3=0}; its images are the corresponding epipolar lines in the two image planes. Image curves have irreducible homogeneous equations f1 and f2, of degrees d1 and d2. Their back-projected cones are S1={f1(x1,x2,x3)=0} and S2={f2(x0,x2,x3)=0}.

## 2. Exact epipolar-line alternative

**Theorem E.** If one prescribed image is an epipolar line, a world lift exists if and only if the other prescribed image is the corresponding epipolar line. In that event every lift is an integral plane curve in the common epipolar plane Pi, except that a line through either center is excluded. There are no other lifts.

**Proof.** An integral lift of an epipolar line is contained in its inverse-image plane Pi by closure. The other camera maps Pi into the corresponding epipolar line, and its image must be a curve by the contract. Hence the other prescribed integral image curve is exactly that line. Conversely, every integral curve in Pi whose maps are nonconstant has those two lines as image closures. A positive-dimensional integral fiber of a pinhole projection is a line through its center. Thus nonconstant image fails exactly for lines through either center. This also excludes L, whose image closures are points. A degree at least two integral plane curve is never one of those fibers. QED.

Consequences:

1. Exactly one epipolar-line image: no lift.
2. Two noncorresponding epipolar-line images: no lift. Their cone intersection is L, which is contracted by both cameras.
3. Two corresponding epipolar lines: positive-dimensional, unbounded-degree families; finite component enumeration cannot classify this case.

## 3. Complete exceptional numerical spectrum

Inside Pi choose coordinates [X:Y:Z] with A=[1:0:0], B=[0:1:0], L={Z=0}. For an integral degree-n plane curve W other than a contracted line, put m1=mult_A(W) and m2=mult_B(W), where an absent center has multiplicity zero. If r_i is the generic degree of the i-th projection, then

    r1=n-m1,    r2=n-m2.

**Theorem N.** There exists an integral lift of degree n with projection degrees (r1,r2) if and only if

    n >= 1,    1 <= r1,r2 <= n,    r1+r2 >= n.

Equivalently, 0<=m_i<=n-1 and m1+m2<=n.

**Necessity.** Projection from a point of multiplicity m removes m from the degree of the pencil of lines through that point, giving r=n-m. The baseline is not a component of W. Bezout with the baseline gives m1+m2<=n, since local intersection with a line is at least the curve multiplicity. This includes n=1, when both multiplicities must vanish.

**Sufficiency.** Let V be the vector space of homogeneous degree-n forms with multiplicities at least m1,m2 at A,B. Its monomial basis consists of X^i Y^j Z^k satisfying

    i+j+k=n,    j+k>=m1,    i+k>=m2.

It contains Z^n, X*Z^(n-1), and Y*Z^(n-1). It also contains X^(n-m1)*Y^m1 because n-m1>=m2. Thus it has no fixed divisorial component: the last monomial and Z^n are relatively prime. The first three sections meet the exact irreducible-Bertini test: the zero divisors of X*Z^(n-1) and Y*Z^(n-1) have the isolated intersection component [0:0:1], outside the divisor of Z^n. The Stacks Project, Lemma 37.32.3, therefore gives a nonempty open of geometrically irreducible members. The squarefree locus is also a nonempty open: Z^n+X^(n-m1)*Y^m1 is squarefree, since its Z derivative is n*Z^(n-1) and it is not divisible by Z. Exact multiplicity m1 is a nonempty open condition because X^(n-m1)*Y^m1 achieves it; exact m2 similarly follows from Y^(n-m2)*X^m2. Their intersection with the irreducible, squarefree opens is nonempty over C. Such a member is an integral W with exactly the desired numerical data. QED.

Primary external lemma used, checked 2026-10-16: [Stacks Project, Bertini, Lemma 37.32.3](https://stacks.math.columbia.edu/tag/0G4C). Its only role here is the stated irreducible general-member implication; the verification of its hypotheses and all camera conclusions are the present derivation.

**Family dimension.** The allowed forms form a projective space of dimension

    binom(n+2,2) - binom(m1+1,2) - binom(m2+1,2) - 1.

The two forbidden monomial triangles are disjoint because m1+m2<=n. Exact multiplicity and integrality cut out a nonempty open. Even degree-one lifts form a two-dimensional open family. Accordingly, the correct output is this parameter-family description, not a finite list of individual world curves.

## 4. Exact smooth-existence spectrum and member test

**Theorem S.** For corresponding epipolar-line images:

- If n=1, a smooth lift exists precisely for (r1,r2)=(1,1).
- If n>=2, a smooth lift exists precisely when each r_i belongs to {n-1,n}.

**Necessity.** Every point on a smooth embedded plane curve has multiplicity one. Thus each m_i is zero or one. Degree-one curves through a center are contracted and inadmissible.

**Sufficiency.** Start with a smooth degree-n plane curve, for example the Fermat curve X^n+Y^n+Z^n=0 for n>=2. It has infinitely many points and its complement is nonempty. Choose ordered distinct points P1,P2 whose membership/nonmembership in this curve matches the requested m_i in {0,1}. A projective automorphism carrying P1 to A and P2 to B produces a smooth degree-n curve with exactly the desired center incidences, hence multiplicities. For n=1 choose a line avoiding both centers. QED.

For a supplied homogeneous polynomial F defining an integral member, embedded smoothness is decidable directly: the projective common zero set of F_X,F_Y,F_Z must be empty. Equivalently the homogeneous ideal generated by the partials has irrelevant-ideal saturation equal to the unit ideal. In characteristic zero Euler's identity already puts F in the partial-derivative ideal. This checks the embedded curve, not merely its normalization.

This is an explicit closed numerical criterion for existence of smooth members, plus an exact polynomial criterion for an individual member. It does not quantify over an uncomputed world lift.

## 5. General center correction, including singular branches

**Proposition C.** For every admissible integral world curve W, not only the planar case, with world degree n, image degrees d_i and projection generic degrees r_i,

    n = r_i*d_i + mult_{c_i}(W),    i=1,2,

where absent centers have multiplicity zero.

**Proof.** On the normalization nu:T->W, the three camera sections belong to nu^*O_W(1), of degree n. Their common base divisor is supported precisely over the corresponding center. Its coefficient at a normalization branch p is the minimum vanishing order of the three affine coordinate functions at that center. Removing this divisor gives the basepoint-free line bundle of the map to the prescribed image curve; its degree is r_i*d_i. A sufficiently general linear form through the center has on each branch precisely that minimum valuation. Summing these local intersection numbers gives the Hilbert-Samuel curve multiplicity at the center. Hence the degree of the base divisor is exactly mult_{c_i}(W), proving the formula. QED.

Warnings:

- Merely subtracting one for center incidence is wrong for singular W.
- If W is smooth, then n-r_i*d_i is necessarily 0 or 1, but this numerical condition alone does not prove smoothness elsewhere.
- Contact with L and multiplicity at a center are different. The baseline ideal has only two of the three camera coordinates, so its branch order can be larger.

## 6. Center/baseline incidence and contracted components

- A lies in S1 intersection S2 exactly when e2 lies on image curve C2.
- B lies in S1 intersection S2 exactly when e1 lies on image curve C1.
- L is a component of the cone intersection exactly when both epipoles belong to their image curves, provided there is no common cone surface.
- Any noncenter point of W intersection L projects to both epipoles, so both epipoles must belong to their image curves.
- If neither image is an epipolar line, the only possible one-dimensional cone-intersection component contracted by either camera is L. Indeed any other contracted curve is a line through one center and its other-camera image is an epipolar line. Integral non-epipolar images cannot contain that line.

The only common-surface case is Theorem E's common epipolar plane. To see this, each cone polynomial is irreducible. If they have a common surface, they are proportional, so the common polynomial depends on neither x0 nor x1. A nonconstant irreducible homogeneous polynomial in x2,x3 over C has degree one, precisely the matching epipolar-plane case.

When the cones have no common surface, an integral lift must equal a reduced irreducible one-dimensional component of their intersection; a proper closed subset of such a component cannot still be a curve. Conversely, every such component on which both projections are nonconstant has exactly the prescribed image curves. Hence the only infinite-family exception is the common plane already classified.

## 7. Complete-intersection multiplicities

If neither image is an epipolar line, the cone intersection is a complete intersection of degrees d1,d2. Every component other than L has scheme multiplicity one. For proof, choose a generic epipolar parameter: the image-to-pencil maps are finite separable maps of curves in characteristic zero, so they are unramified at generic points. On an off-baseline affine chart with coordinates (a,b,t), the cone equations have nonzero partial derivatives respectively in a and b, hence meet transversely at each generic nonbaseline component.

Let mu_L be zero if L is absent, or otherwise the length of the cone-intersection local ring at the generic point of L. Then

    sum_{valid reduced components W} degree(W) = d1*d2 - mu_L.

A complete intersection is Cohen-Macaulay and has no embedded associated components. Its degree cycle is therefore accounted for by these components and the possible multiple baseline. The multiplicity mu_L can be computed exactly by local algebra over C(lambda): set x1=1, x0=lambda and take the local length at (x2,x3)=(0,0) of

    C(lambda)[x2,x3]_(x2,x3) / (f1(1,x2,x3), f2(lambda,x2,x3)).

In an implementation, use an effective coefficient field containing the input coefficients; the mathematical theorem itself holds for arbitrary complex coefficients.

**Counterexample to a naive baseline subtraction.** Let

    f1=x1*x3-x2^2,    f2=x0*x3-x2^2.

Both image epipoles are smooth (multiplicity one), but their tangent directions agree. The intersection consists of the smooth residual conic

    x0=x1,    x1*x3=x2^2

and a double baseline. At its generic point the local ideal is equivalent to (x3-x2^2, x2^2), of length two. Thus d1*d2=4=2+2, and mu_L is not the product 1*1 of image-epipole multiplicities. The conic avoids both centers, maps birationally onto both images, and meets L at [1:1:0:0].

## 8. Status and limits

The exceptional epipolar-line branch is fully classified with proofs of both directions, exact degree/projection spectrum, positive-dimensional family description, and embedded-smooth existence/member tests. General center, contraction, and scheme-degree bookkeeping is supplied for integration with the non-epipolar classification and local smoothness work. Nothing in this note claims novel clean-case monodromy, arbitrary-field coverage, real visibility, or a full original-source resolution.

## 9. Explicit branch formula for baseline multiplicity

Suppose neither image is an epipolar line and both contain their epipoles. Enumerate the analytic branches a of C1 at e1 and b of C2 at e2. Let m_a,m_b be their branch multiplicities. Tangent lines at the two epipoles are compared through the fixed identification of their epipolar pencils. When a,b have corresponding tangent lines, let q_a and q_b be their intersection multiplicities with those tangent lines. These are finite and strictly larger than m_a,m_b: an analytic branch equal to a line would force its integral global curve to be that excluded epipolar line.

Then the generic cone-intersection multiplicity along L is

    mu_L = sum_{branch pairs (a,b)} M(a,b),

where

    M(a,b) = m_a*m_b                         if the tangents differ,
    M(a,b) = min(m_a*q_b, m_b*q_a)           if the tangents correspond.

**Direct proof.** At the generic baseline point the two transverse image germs differ by a generic scalar dilation with parameter lambda. Distinct tangents give the usual product of branch multiplicities. For a common tangent, choose transverse local coordinates x,y so the tangent is y=0. Branch a has a Puiseux parameterization x=t^(m_a), y=c_a*t^(q_a)+higher terms, and similarly b. Under dilation, each leading Puiseux coefficient for y as a function of x is multiplied by lambda^(1-q/m). This exponent is nonzero because q>m. Thus if the first exponents of the two branches are equal, generic lambda prevents cancellation for every pair of conjugate leading coefficients; if the exponents differ, cancellation is impossible anyway. The intersection multiplicity is therefore m_a*m_b times the smaller first Puiseux exponent, namely min(m_a*q_b,m_b*q_a). Summing branch-pair intersection multiplicities proves the formula.

**Independent consistency check.** Let s_i=mult_ei(C_i), and let k_i=d_i-s_i be the epipolar-cover degree. At a branch with tangent parameter t0, the ramification degree of the epipolar map is a=q_a-m_a. For a corresponding branch pair write a=q_a-m_a and b=q_b-m_b. The normalized local fiber product of u^a=v^b has g=gcd(a,b) branches, each pulling back the two epipole base orders to m_a*b/g and m_b*a/g. Hence its total minimum-base contribution is min(m_a*b,m_b*a). Summing the triangulation-divisor degree formulas in GLOBAL_CLASSIFICATION.md gives

    sum degree(W) = d1*d2 - s1*s2
                    - sum_{corresponding tangent pairs} min(m_a*b,m_b*a).

Comparison with the complete-intersection degree cycle yields exactly the preceding branch formula, because m_a*m_b+min(m_a*b,m_b*a)=min(m_a*q_b,m_b*q_a). This second derivation was independently checked in the shared audit.

The formula needs first tangent contact orders, not all higher Puiseux terms. It also explains why merely knowing image-epipole multiplicities does not determine the amount of baseline scheme multiplicity.

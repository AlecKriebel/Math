# Embedded smoothness for the complex fixed-camera residual

Authored local result, shared pass 1/5, 2026-10-16. This addresses the adopted contract in `../CONTRACT.md`; it is not a novelty claim or a solution of every interpretation of AIM Reconstruction Problem 1.4. All curves and points below are over C, and curves called integral are reduced.

## 1. Coordinates and the finite candidate setting

Put the distinct rank-three cameras, by independent projective coordinate changes, in the form

- pi_1([X0:X1:U:V]) = [X1:U:V], with center O1=[1:0:0:0];
- pi_2([X0:X1:U:V]) = [X0:U:V], with center O2=[0:1:0:0].

The baseline is L={U=V=0}, and both image epipoles have coordinates e_i=[1:0:0]. This coordinate change preserves embedded smoothness.

For now assume that neither prescribed integral image curve C_i is an epipolar line. Let nu_i:D_i -> C_i be its normalization, and let f_i:D_i -> P1 be the everywhere-defined extension of the epipolar map [A:U:V] -> [U:V]. Since C_i is not an epipolar line, f_i is nonconstant and finite. Form the reduced fiber product T=(D_1 x_{P1} D_2)_red, find its irreducible components, and normalize each component. Write B for one such smooth connected projective curve and h_i:B -> D_i for its maps.

There is a canonical triangulation morphism R:B -> P3. On the open set where neither image is an epipole, it is the usual unique triangulation of the image pair. It is nonconstant and birational onto its image W: off the baseline, the original image pair determines the world point uniquely; at a generic image point the normalization maps are isomorphisms. Thus R is the normalization of the integral world curve W. In particular, this is not an arbitrary unknown lift supplied as input. B and R are calculated from the two given image curves.

The global classification report establishes that these W are exactly the admissible world curves in the present non-epipolar case. Section 8 also gives a separate direct elimination route that does not depend on that parametrization for its smoothness decision.

## 2. Uniform local triangulation formula

Fix p in B and a local parameter z at p. Choose local trivializations of the pulled-back image hyperplane line bundles. Write the two image maps as

    [a_i : q_i s : q_i t],

where [s:t] is the common epipolar map near p, s and t are regular and at least one is a unit, and each displayed triple has at least one unit. Thus q_i vanishes exactly where the i-th image is e_i. Put k_i=ord_p(q_i), a nonnegative integer. If k_i>0, then a_i is a unit.

The triangulation before common-factor cancellation is

    [a_2 q_1 : a_1 q_2 : q_1 q_2 s : q_1 q_2 t].                 (2.1)

Its exact common order of vanishing is min(k_1,k_2). Indeed, when both k_i are positive the a_i are units; when only one is positive the other corresponding first coordinate is a unit; when neither is positive one of the last two coordinates is a unit. Divide all four coordinates by z^min(k_1,k_2). The resulting tuple has at least one unit and defines R regularly at p.

The construction is invariant under the choices: changing a local image representative, epipolar representative, or uniformizer only rescales the homogeneous tuple by a unit after the common factor has been removed. The generic image identities extend through the cancellation. No camera projection is asserted to be defined at its center.

## 3. Exact center and baseline criteria

The following table exhausts the local possibilities:

| Orders | World limit | Branch multiplicity in P3 | Immersion at p |
|---|---|---|---|
| k_1=k_2=0 | outside L | see Section 4 | see Section 4 |
| k_2>k_1 | O1 | k_2-k_1 | k_2-k_1=1 |
| k_1>k_2 | O2 | k_1-k_2 | k_1-k_2=1 |
| k_1=k_2=k>0 | L minus {O1,O2} | min(k,ord_p(rho-rho(p))) | k=1 or rho'(p) is nonzero |

In the last row,

    rho = (a_1 q_2)/(a_2 q_1)

is a unit after canceling the equal powers of z, and the limiting point is [1:rho(p):0:0]. The order of the identically zero function is infinity. Derivatives and first-order conditions are taken in a local parameter; their vanishing does not depend on the parameter.

### Proof at O1

Assume k_2>k_1, so a_2 is a unit. In the chart X0=1 the regular local coordinates of R are

    Y=(a_1/a_2)(q_2/q_1),  Z=q_2 s/a_2,  H=q_2 t/a_2.

If k_1>0, a_1 is a unit and ord(Y)=k_2-k_1, whereas min(ord(Z),ord(H))=k_2. If k_1=0, ord(Y)>=k_2 and min(ord(Z),ord(H))=k_2. In either case the minimum coordinate order is k_2-k_1. That minimum is the multiplicity of this parametrized reduced branch and equals 1 precisely when the derivative of R is nonzero. The proof at O2 is symmetric.

If k_1>0 and the O1 branch is immersive, its tangent is the baseline: Y has order 1 and both transverse coordinates have order at least 2. If k_1=0 and k_2=1, the tangent is not the baseline and its pi_1-direction is the non-epipolar first image point. These statements concern the tangent line at the center, not a value of the undefined projection there.

### Proof at an interior baseline point

When k_1=k_2=k>0, both a_i are units. In the X0=1 chart the coordinates are

    (rho, q_2 s/a_2, q_2 t/a_2).

The last two have minimum order k, proving the table after subtracting the limiting first coordinate rho(p). If k=1 the tangent is transverse to L; if k>1 and rho'(p) is nonzero the tangent is L. If both first-order tests fail, this branch is singular even if it is the only branch mapping to that point.

### Branch multiplicity versus point multiplicity

For a reduced curve in a smooth ambient variety, a general local hyperplane has intersection order on a normalization branch equal to the minimum order of its ambient coordinate functions. The multiplicity of the whole curve at the point is the sum of these branch orders. Consequently the complete center formulas are

    mult_O1(W) = sum over p in B with k_2>k_1 of (k_2-k_1),
    mult_O2(W) = sum over p in B with k_1>k_2 of (k_1-k_2).

These include singular, multibranch centers. In particular, W is smooth at O1 exactly when there is one such p and its order difference is 1. Merely having total normalization smooth, or having each local branch immersed, is insufficient if several points of B map to O1.

## 4. Points away from the baseline, including singular image points

When k_1=k_2=0, choose s=1 locally and write lambda=t/s. Then U is a valid world affine chart and

    R = [a_2/q_2 : a_1/q_1 : 1 : lambda].                     (4.1)

The branch is immersive exactly when at least one of

    d(a_2/q_2), d(a_1/q_1), d(lambda)

is nonzero at p. The branch multiplicity is the minimum order of the differences of these three functions from their values at p. There is no smooth-image hypothesis in this statement.

A useful fully local version starts with p_i in D_i over one epipolar value lambda_0. Choose a local affine coordinate at lambda_0, including a coordinate at infinity when needed, and let e_i be the ramification index of f_i at p_i. After a characteristic-zero formal or analytic unit change, the fiber-product equation is u_1^{e_1}=u_2^{e_2}. If g=gcd(e_1,e_2), its reduced germ has g normalization branches; on each, the orders of u_1 and u_2 are respectively

    epsilon_1=e_2/g,   epsilon_2=e_1/g.

The g local branches may lie on different global irreducible components, so the selected global component must be tracked.

Suppose neither p_i lies over an epipole, and let mu_i be the multiplicity of the particular image branch nu_i(D_i,p_i) in the image plane. Formula (4.1) gives

    multiplicity of the corresponding world branch
       = min(epsilon_1 mu_1, epsilon_2 mu_2).                 (4.2)

Indeed, in image affine coordinates (a_i/q_i,lambda), mu_i is the minimum of the two coordinate orders. Pullback multiplies orders by epsilon_i, and the lambda coordinate agrees on the two sides.

Thus immersion is equivalent to epsilon_1 mu_1=1 or epsilon_2 mu_2=1. If both image branches are smooth, this is equivalent to e_1 dividing e_2 or e_2 dividing e_1. If both selected image branches are singular, their paired world branch cannot be smooth away from the baseline.

This is only the branch-immersion test. Different normalization branches above singular raw image points, and different local branches of the epipolar fiber product, can still give the same world point. They must pass the separation test in Section 5.

At an epipole, if b_i is the order of the epipole base divisor on D_i at p_i, then the orders in Section 3 are k_i=epsilon_i b_i. This supplies the center and baseline orders directly from the two image branches and the local fiber-product branch.

## 5. The global branch-separation condition

For any B under consideration, the following are equivalent:

1. Its reduced integral world image W is a smooth embedded projective curve.
2. R:B -> W is an isomorphism.
3. R is injective on geometric points and dR is nonzero at every point of B.

Necessity follows because R is the normalization. For sufficiency, R is a nonconstant proper map of projective curves, hence finite, and it is birational. At any point p where dR is nonzero, one affine world coordinate has nonzero derivative. The complex inverse function theorem expresses the local image as a graph over that coordinate, so this branch is smooth. Injectivity and properness ensure there is no other image branch at that point. Therefore every point of W is smooth, and the normalization is an isomorphism. This argument also explains the algebraic criterion in terms of one branch and a nonzero tangent.

A pair of distinct immersed branches with different tangent lines is an ordinary double-point candidate, not a smooth point. Equal tangent lines do not rescue it. For smoothness, branches must be separated as points of P3, not merely have distinct tangents. Conversely, intersections with a different world component of the full cone intersection do not make the selected component itself singular.

For nonbaseline world points, equality under R is equivalent to equality of both raw image points. For baseline points, the common epipolar value is not recoverable from the world point. Center and baseline collisions must therefore be compared across all relevant epipolar fibers, not just within each fiber separately.

## 6. A finite, image-determined smoothness algorithm

Define a finite subset S of P1 as the union of:

- branch values of f_1 and f_2;
- f_i-values of all points of D_i lying above singular points of C_i;
- f_i-values of all points of D_i lying above e_i, if e_i belongs to C_i.

For every normalized global fiber-product component B, let f_B=f_i h_i and E=f_B^{-1}(S). Both S and E are finite and are obtained from the prescribed image data.

**Finite criterion.** W=R(B) is smooth if and only if:

(a) all points of E have pairwise distinct values under the canceled map (2.1); and
(b) every point of E passes the immersion test of Section 3 or 4.

These comparisons are made within the selected B only. Points on different normalized global components are not compared: two individually smooth admissible world curves may intersect. If E is empty these conditions are vacuous and W is smooth.

**Proof that no omitted points can fail.** Over P1 minus S both f_i are etale; both image normalization maps are locally isomorphisms onto smooth image points; and neither image is an epipole. The fiber product is smooth there. Its point is uniquely determined by the two raw image points, so R is injective there, and its local derivative is nonzero because the epipolar coordinate itself is a local parameter. A world point reached from outside E cannot also be reached from E: it is off the baseline and its uniquely recovered epipolar value is outside S. Hence all collisions and all ramification are detected by (a) and (b).

This is a finite exact test, not a condition asking whether an unspecified smooth lift exists. It requires normalizations, irreducible factorization, finite fibers, and first-order jets of an explicit map. Local Puiseux expansions provide one implementation; function-field/normalization algorithms provide another. Orders k_i and leading coefficients determine limits, and only the first nonconstant coefficient after cancellation is needed for the immersion test. Equality of the finitely many image coordinates is an exact algebraic comparison.

The word "computable" presumes an effective exact presentation of the input coefficients, for example algebraic numbers, or an exact coefficient-field oracle with factorization and equality. Arbitrary complex constants supplied only as approximate decimals do not support an unconditional exact equality or smoothness decision. The mathematical criterion holds for all complex inputs independently of their representation.

## 7. Exceptional epipolar-line case

The preceding normalized cover construction is intentionally restricted to nonconstant epipolar maps. If one image is an epipolar line, the world curve is contained in its epipolar plane. Its other nonconstant image must be the corresponding epipolar line in the other image plane. Thus a line/nonline pair, or two noncorresponding epipolar lines, has no admissible world curve.

For two corresponding epipolar lines, the admissible world curves are all integral curves in their common plane except lines through either camera center. A chosen plane curve has the usual reduced plane-curve smoothness test. For its world degree n and projection generic degrees r_i,

    r_i = n - mult_Oi(W).

A smooth plane curve has center multiplicities in {0,1}. Hence its smooth spectrum is r_i=n-epsilon_i with epsilon_i in {0,1}, requiring r_i>=1; for n=1 this forces epsilon_1=epsilon_2=0. For n>=2 every such incidence choice is realizable by a smooth plane curve. The companion exceptional-case report supplies the existence proof and the full singular spectrum.

## 8. Independent prime-ideal/Jacobian decision procedure

Let F_i be the irreducible homogeneous equation of C_i, and form

    I=(F_1(X1,U,V), F_2(X0,U,V)) in C[X0,X1,U,V].

Except when both cones are the same epipolar plane, their irreducible hypersurface equations have no common factor. Therefore their common support has finitely many irreducible curve components. Compute the homogeneous reduced minimal primes of I. Discard L and any component whose generic image under a camera is a point or whose image closure is not the prescribed curve. In the non-epipolar case, the nonbaseline prime components are exactly the candidate W from Section 1.

For a candidate prime P, take generators of P, not merely generators of I. On each of the four projective affine charts, dehomogenize them to an ideal P_j in three variables. Let J_j be their Jacobian matrix. Since the curve is reduced, integral, and one-dimensional, its singular set in that chart is defined by

    P_j + (all 2-by-2 minors of J_j).

The curve is smooth exactly when all four of those chart ideals have empty zero loci (equivalently, each is the unit ideal after exact algebraic computation). This follows from the tangent-space criterion: the Zariski tangent space has dimension 3-rank(J_j), and a reduced curve point is regular exactly when that dimension is 1.

**Essential warning.** The original cone intersection may be nonreduced along a component or may have other components meeting a selected smooth component. Its unreduced complete-intersection Jacobian can therefore falsely reject a smooth candidate. One must first select the reduced prime component. For example, the cones X1 V-U^2=0 and X0 V-U^2=0 have a smooth residual conic and a multiple baseline; the full-intersection Jacobian is deficient at their intersection even though the conic is smooth.

This prime-ideal test is finite and independent of normalization choices. It is an especially direct fallback for machine certification; the preceding local formulas explain the geometric failure modes and expose the exact center/baseline corrections.

## 9. Claims and remaining audit boundary

Proved here: the canceled local map; exact center/baseline branch multiplicities; off-baseline singular-image multiplicity; injectivity-plus-immersion equivalence; the finite exceptional-set reduction; and the reduced-prime Jacobian algorithm. These results include all singular-image branches and both kinds of baseline behavior. They do not infer smoothness from a smooth abstract normalization, use the Jacobian of an unreduced union, or count a contracted baseline as an admissible curve.

The independent acceptance is recorded in ../audit/INDEPENDENT_AUDIT.md. The classification of all global candidates, global degree formulas, coincident-plane existence spectrum, and prior-literature/novelty limits are supplied by companion reports.

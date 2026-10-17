# Finite algebraic reconstruction criterion

## Scope and status

This is a standard-algebraic-tools synthesis for two fixed distinct rank-three pinhole cameras over the complex numbers, with prescribed reduced integral projective image curves. It is not a novelty claim for cone intersection, primary decomposition, Hilbert polynomials, normalization, or the Jacobian criterion. It allows image singularities and epipoles, world curves through the centers, and intersections with the baseline. A world curve is required to be integral and to have each prescribed image as the closure of its rational image.

The finite algebraic criterion below is valid over C. Executing it as a terminating exact algorithm requires an effective coefficient presentation, such as algebraic-number coefficients and absolute decomposition over Qbar, or a field with certified exact arithmetic and the requisite effective decomposition. It is not an exact-decision algorithm for arbitrary floating-point samples or unspecified arbitrary complex-number oracles.

## 1. Normal form and exceptional split

After independent projective coordinate changes, write world coordinates [x:y:u:v] and cameras

P([x:y:u:v])=[y:u:v],  Q([x:y:u:v])=[x:u:v].

Their centers are c_P=[1:0:0:0] and c_Q=[0:1:0:0]; the baseline is L=V(u,v). Both epipoles have image coordinates [1:0:0]. Let image equations be irreducible homogeneous f(y,u,v) and g(x,u,v), of degrees m and n, and set F=f(y,u,v), G=g(x,u,v), R=C[x,y,u,v]. The pullbacks remain irreducible because adjoining an unused variable preserves primality.

The two surfaces share a surface component if and only if F and G are proportional. Such a common polynomial is independent of x and y, hence is a homogeneous binary irreducible polynomial, hence linear over C. Consequently the unique common-surface case is a pair of matching epipolar image lines. Their common pullback is the corresponding epipolar plane H.

If one image is an epipolar line, every possible world curve is in its epipolar plane. Its other nonconstant image must be the matching epipolar line. Therefore an epipolar-line image paired with anything else has no admissible world curve.

The remaining case is that neither image is an epipolar line. The pullback equations have no common factor and form a regular sequence, so their projective intersection is a pure one-dimensional complete intersection of degree mn.

## 2. Exact finite list in the proper-intersection case

Assume neither image is an epipolar line. Form

K = radical((F,G) : (u,v)^infinity)

and compute its absolute homogeneous minimal primes P_1,...,P_r. Every P_j has height two. Then

{all admissible integral world curves} = {Proj(R/P_j): 1<=j<=r}.

Here saturation is by the baseline ideal (u,v). Saturation by the product uv is not the same operation in general: it removes whole components in either coordinate hyperplane. In the present neither-epipolar-line case no retained component can lie in either such epipolar plane, so one can separately prove that product saturation gives the same candidate list; that shortcut must not be imported into the exceptional plane family. Saturation by (u,v) removes a whole baseline component but does not remove points of any other component that happen to lie on the baseline or at a camera center: for a nonbaseline prime P, P:(u,v)^infinity=P.

### Proof

Every admissible world curve lies on both cones and is not the baseline, whose two images are points. It is a one-dimensional integral closed subset of a pure one-dimensional intersection, so it is an irreducible component, and saturation retains it.

Conversely, each retained component lies on both cones. A curve contracted by a linear projection from a point must be a line through that point: its dense open points all lie in a single camera ray, and closure is that line. A nonbaseline line through c_P has, under Q, an epipolar-line image. It therefore cannot lie in Q's cone when Y is integral and is not an epipolar line. The same argument applies to c_Q. Thus both maps on a retained component are nonconstant, and their image closures, being integral curves contained in X and Y, equal X and Y.

The list is nonempty. On a generic epipolar plane, with parameter t=u/v, f(y,t,1) and g(x,t,1) define nonzero finite separable extensions of C(t). Their tensor product is a nonzero finite reduced algebra, and each field factor gives a retained component. The degree of f in y is m-mult_epipole(X)>0, and similarly for g. A zero moving degree occurs precisely for an epipolar line, already separated above.

No unknown lift is quantified over in this procedure: all inputs to the decomposition are explicitly computed from the given cameras and image equations, and the candidate set is finite, with at most mn members.

## 3. Exact world and projection degrees

For C_j=Proj(R/P_j), compute its Hilbert polynomial

Hilb_j(k)=delta_j k + 1 - p_a(C_j).

Then delta_j is its world degree. Let mu_P,j and mu_Q,j be its Hilbert-Samuel multiplicities at the camera centers, with multiplicity zero if the center is not on the curve. The generic projection degrees are exactly

a_j=(delta_j-mu_P,j)/m,  b_j=(delta_j-mu_Q,j)/n.

These are positive integers. Thus a prescribed triple (delta,a,b) is attainable if and only if it occurs in this finite computed list.

### Proof of the center correction

On the normalization of C_j, the three camera coordinate forms are sections of a degree-delta_j line bundle. Their common base divisor is supported over the camera center. Its coefficient on a normalization branch is the minimum of the orders of the three coordinate forms. A generic linear combination attains these minima simultaneously. The sum of these minima is the intersection multiplicity with a generic hyperplane through the center, namely the Hilbert-Samuel multiplicity of the curve at that center. Removing this divisor leaves the pullback of O_X(1), whose degree is a_j m. This gives the identity, including singular centers and multiple branches.

The local multiplicity is effective: in an affine chart containing the center, compute the associated graded tangent-cone ideal of the local curve ring using a local standard basis, then its Hilbert-Samuel polynomial. The initial ideal must be formed from the entire ideal, not only from the displayed generators. An alternative is the length of the local ring modulo a generic linear form; a one-dimensional integral local ring is Cohen-Macaulay.

### Multiplicities of the raw cone intersection

Every nonbaseline component is generically reduced: over the generic epipolar parameter its coordinate algebra is a tensor product of separable finite field extensions. Consequently its multiplicity in the raw complete intersection is one. Any remaining component is the baseline, so

sum_j delta_j = mn - length(R_(u,v)/(F,G)R_(u,v)),

where the last term is interpreted as zero when the baseline is not a component. In particular, it is zero unless both image epipoles lie on their image curves. Shared tangent directions can increase this baseline multiplicity; it must not be replaced blindly by the product of image epipole multiplicities. Each delta_j is at most mn.

## 4. Computable embedded smoothness

Take a finite homogeneous generating set h_1,...,h_s of P_j and its Jacobian matrix J_j with four columns. Let I_2(J_j) be the ideal of its 2-by-2 minors and let M=(x,y,u,v). Then

C_j is smooth if and only if (P_j + I_2(J_j)) : M^infinity = (1).

Equivalently, dehomogenize in each of the four projective charts and test whether the corresponding curve ideal plus codimension-two Jacobian minors has empty zero set, by a Groebner basis/unit-ideal computation. This uses the vanishing ideal of the individual reduced component. Applying the Jacobian criterion only to F,G instead tests the full possibly nonreduced or reducible intersection and is not an equivalent selected-component test.

Necessity and sufficiency are exactly the Jacobian criterion over the perfect field C: a curve in an affine three-space chart is smooth at a closed point precisely when its Jacobian has rank two. The projective saturation removes only the irrelevant affine-cone origin. Thus a smooth reconstruction with prescribed degrees exists if and only if at least one matching list entry passes this test. This is a finite test from the given equations, including singularities on the baseline and at the centers.

### Optional normalization certificate

Normalization is not needed by the preceding test. As an independent alternative, normalize the reduced affine curve ring in each chart and compute the finite module quotient Abar/A. The embedded curve is smooth exactly when these quotients vanish on all charts: for curves over C, normal local rings are regular and regularity is smoothness. Merely finding a smooth normalization is vacuous for integral complex curves and is insufficient. The actual normalization morphism must be an isomorphism. Implemented normalization algorithms are standard prior art, for example Greuel–Laplagne–Seelisch.

## 5. The infinite epipolar-plane family

When both images are matching epipolar lines, all admissible world curves are integral plane curves in H other than lines through either camera center. Let delta>=1 and a,b>=1. The exact degree feasibility conditions are

1 <= a,b <= delta,  a+b >= delta.

Indeed their center multiplicities are mu_P=delta-a and mu_Q=delta-b. Each is at most delta-1 for an integral plane curve, and Bezout with the baseline gives mu_P+mu_Q<=delta unless the curve is the baseline, which is inadmissible.

For sufficiency, in plane coordinates [x:y:z] with centers [1:0:0] and [0:1:0], consider the degree-delta linear system with these two prescribed lower multiplicities. Its base locus is contained in the two centers: z^delta is nonzero off the baseline, while the allowed binary monomial x^(delta-mu_P)y^mu_P is nonzero at other points of the baseline. The system contains z^delta, x z^(delta-1), and y z^(delta-1), so it gives a two-dimensional image and is not composed with a pencil. Bertini irreducibility gives a general integral member. Exact multiplicities are nonempty open conditions: for example x^(delta-mu_P)z^mu_P achieves the first exact multiplicity and satisfies the second lower bound because delta-mu_P>=mu_Q. The symmetric monomial treats the other center. Their nonempty open conditions intersect the general-integral open subset. Degree one forces a=b=1 and is handled by a line avoiding both centers.

For embedded smoothness, delta=1 again requires a=b=1. For delta>=2, a smooth plane curve has multiplicity either zero or one at either center, so the exact smooth feasibility condition is

a,b belong to {delta-1,delta}.

All four choices occur: a general degree-delta plane curve through precisely the selected subset of the two centers is smooth, including at these assigned simple base points; it avoids the others. For delta>=2, these simple-point conditions satisfy the general integral feasibility inequalities.

## 6. Effective decision procedure

1. Check the rank and distinct-center hypotheses; change to the displayed normal form by exact linear algebra if convenient.
2. Check whether each image is a line through its epipole. If exactly one is, or both fail to match, output no reconstruction. If they match, apply the explicit infinite-family degree and smoothness formulas in section 5.
3. Otherwise form F,G and K by baseline-ideal saturation and radical; compute absolute minimal primes.
4. For each prime compute delta, the two local center multiplicities, a,b, and the saturated Jacobian singular-locus ideal.
5. Return all resulting degree triples with a smoothness flag and defining prime ideals. Test any requested restrictions against this finite output.

All steps are standard exact algebraic operations under the coefficient hypothesis stated at the start. An implementation must distinguish absolute primes from primes over the initial number field and must retain exact certificate data. Complexity may be high; no efficiency guarantee is asserted.

## Public references

- J. Y. Kaminski, M. Fryers, M. Teicher, Recovering an algebraic curve using its projections from different points, JEMS 7 (2005), 145–172, section 3.4, Theorem 2: https://ems.press/content/serial-article-files/31537
- S. Agarwal, A. Pryhuber, R. R. Thomas, Ideals of the Multiview Variety, arXiv:1812.09470v2, introduction and Theorems 3.7, 4.9: https://arxiv.org/pdf/1812.09470v2
- Macaulay2, PrimaryDecomposition documentation: https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/PrimaryDecomposition/html/index.html
- Macaulay2, degree(Ideal): https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_degree_lp__Ideal_rp.html
- G.-M. Greuel, S. Laplagne, F. Seelisch, Normalization of Rings (2009): https://arxiv.org/abs/0904.3561
- Stacks Project, Curves, Lemma 33.43.8: https://stacks.math.columbia.edu/tag/0A22
- Stacks Project, Bertini theorems, Lemma 37.32.3: https://stacks.math.columbia.edu/tag/0G4C

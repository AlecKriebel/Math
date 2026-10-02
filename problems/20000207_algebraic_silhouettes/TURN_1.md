# Turn 1: explicit full-rank local epipolar compatibility for dual sections

AI-assisted mathematical proof candidate, independent review pending. Original broad source question unresolved; first author turn. The extended-Kruppa/dual-section setup and low-class count are credited to the imported research report and the primary sources listed in SOURCE_GATE.md. The result here is a concrete transversality certificate in the unrestricted dual-surface family. It does not establish the same property for duals of general smooth primal surfaces.

## 1. Local compatibility coordinates

Work over C, in characteristic zero. Let S=V(Phi) in dual projective3-space with coordinates (s:t:z:w), and fix the camera planes H1={z=0}, H2={w=0}. Their common line is L={z=w=0}. Suppose f(s,t)=Phi(s,t,0,0) is a nonzero squarefree binary form of degree delta. Write

g(s,t)=partial_w Phi(s,t,0,0), h(s,t)=partial_z Phi(s,t,0,0).

The input dual image curves are Gamma1=S intersect H1 and Gamma2=S intersect H2. Candidate epipoles correspond to candidate lines in these planes. Near L these lines have unique graph equations w=a s+b t in H1 and z=c s+d t in H2. Their binary restriction forms are

q1(a,b;s,t)=Phi(s,t,0,a s+b t),
q2(c,d;s,t)=Phi(s,t,c s+d t,0).

A candidate epipolar projectivity between the lines is a PGL2 element M near identity. The extended-Kruppa condition is that q1 and q2 composed with M be proportional, with the scalar nonzero. The two epipoles contribute four parameters and PGL2 three, the usual seven-dimensional rank-two fundamental-matrix chart. This parameterization is locally one-to-one: a rank-two fundamental matrix determines its two kernels and its induced isomorphism between their pencils; conversely these data determine its bilinear epipolar relation up to scale.

At (a,b,c,d,M)=(0,0,0,0,I), compatibility holds with both forms f. On a coefficient chart where a fixed coefficient of f is nonzero, equality of their projective coefficient vectors is a regular system of delta equations. Its differential is a linear map to V_delta/<f>, where V_delta denotes binary forms of degree delta.

## 2. Differential criterion

The seven differential columns, up to individual signs, are the classes of

s g, t g, s h, t h, s partial_t f, t partial_s f, s partial_s f - t partial_t f.

Indeed differentiating the graph substitutions gives the first four. The tangent space of PGL2 is sl2, whose standard three generators give the last three. Scalar changes of the form disappear in the quotient by f. Choices of representatives or projective coefficient charts change these columns by an invertible coordinate transformation and terms proportional to f, so rank is intrinsic.

If these seven classes are independent, the candidate compatibility solution is reduced and isolated at the true data. To see this without merely counting equations, choose seven output coordinates with an invertible Jacobian minor. The complex analytic inverse-function theorem says their simultaneous zero near the point is that point. Algebraically the local maximal ideal modulo its square vanishes in the solution local ring; Nakayama's lemma makes that local ring C. Remaining equations cannot create a local branch. This proves local uniqueness at this one true solution, not global uniqueness among distant compatible matrices.

## 3. An exact certificate for every delta >= 7

Choose

f=s^delta+t^delta,
g=s^(delta-3)t^2,
h=s^(delta-5)t^4.

These have the required degrees delta,delta-1,delta-1. The form f is squarefree over C. The first four columns are the monomials with t-exponents 2,3,4,5. The next two have t-exponents delta-1 and 1, with nonzero coefficient delta. The final column is delta(s^delta-t^delta). Modulo f this becomes 2delta s^delta. These seven exponent classes 0,1,2,3,4,5,delta-1 are distinct for delta>=7. Together with f, the seven unquotiented columns are linearly independent. Hence the rank is exactly seven for every such delta.

A corresponding polynomial is

Phi = f + w g + z h + terms in (z,w)^2 of total degree delta.

All these higher-normal-order terms leave the seven-column certificate unchanged. In particular this is genuine compatibility data obtained by restricting one dual equation, rather than two unrelated arbitrary plane curves.

## 4. Generic and geometric scope

The nonzero minor is polynomial in the coefficients of Phi. Thus for every delta>=7 the full-rank condition is a nonempty Zariski-open condition in the vector space of degree-delta dual equations, with the fixed distinct camera planes. Smooth surfaces, smooth plane sections and transversality to L are also nonempty open conditions in this irreducible parameter space: for example the Fermat hypersurface establishes simultaneous smoothness of the surface and these coordinate-plane sections, with squarefree common restriction. Intersecting these nonempty opens is nonempty. Consequently the local isolation conclusion holds for a general smooth degree-delta **dual** surface and these two camera planes. A projective coordinate change extends the statement to a general distinct plane pair.

A smooth dual surface of degree at least2 is nondevelopable, and biduality gives a primal surface X=S^vee. A smooth section S intersect Hi means Hi is not a tangent plane to S, so the corresponding center is outside X. The dual-plane-section description then identifies Gamma_i with the dual of the contour contributed by smooth points of X, in the conormal/algebraic sense. This construction does not assert that X is smooth. Full visible silhouettes may also involve singularities or occlusion; they are not replaced by these complex contour equations without additional hypotheses.

Thus the theorem closes the differential-rank gap for an unrestricted dual-degree family. It leaves open the imported report's sharper smooth-primal family, the complete set of global compatible F's, finite-versus-unique recovery, and physical real visibility. In particular an isolated true solution alone does not rule out another positive-dimensional component elsewhere. The source's broad wording is not silently strengthened into or identified with this partial theorem.

## 5. Reproducibility and credit

The standard-library checker computes all eight coefficient columns including f, exact rational ranks for delta7 through80, and evaluates the derivative columns by independent first-order substitution. It also checks deficient small-degree controls; these do not infer impossibility of other constructions. The displayed monomial argument, rather than the finite range, proves all delta>=7. No novelty or priority claim is made. Classical projective camera geometry, contour duality, the extended-Kruppa setup and Jacobian criterion are credited; only the explicit scoped certificate is presented as this turn's mathematical work.

# Manuscript-first adversarial reconstruction for record 23392409

This reconstruction follows my complete reading of the actual six published PDF pages, all 285 controlling TeX lines and six fresh individually viewed page renders. No foreign scientific body, supplied program/certificate/results, inventory assessment, current peer/root scientific findings or archived opinion has been read. The native version field is absent; I do not invent a version number. This is a new independent scientific lane, despite my unrelated acquisition/editorial/stage roles.

## Exact hypothesis and success criterion

The manuscript claims existence, not an exact enumeration theorem. At exponent 16 there is one fixed ordered sextuple of six distinct real algebraic boundary points with both alternating triples noncollinear, at least one admissible incoming center Z, and at least five pairwise distinct admissible outgoing centers X. Every selected center differs from every boundary vertex. The six appropriate opposite-side power equalities must hold exactly for that same boundary. Additional stated certificate claims include noncollinearity of all 20 boundary triples and avoidance of every boundary-pair line by selected centers.

The boundary is explicitly crossed. The claimed counterexample therefore concerns the primary realization convention permitting crossings, not proper embeddings. The paper claims at least five intersections of two appropriate construction curves with a common focus and a negative example for the cited at-most-three expectation in that convention. It does not determine the exact total number, a universal maximum, the alpha<1 regime, or firstness. Actual primary conventions and exact scope remain to be checked after this freeze.

Success requires a universal geometric/algebraic implication from strictly certified finite inequalities; numerical plots or floating-point roots alone are insufficient. A substantive defect in the actual construction, sign certificates, fixed-boundary logic or primary domain would defer the actual claim. I will not silently replace it with a smaller or differently interpreted theorem.

## Independent distance lift: Gram determinant mechanism

Set A=0, B=(b,0), C=(c,d), with the exact rational values in the paper and lambda>0. Let s=|X|^16, u=s^(1/8), v=(s+lambda)^(1/8), w=(s+1)^(1/8), always the nonnegative real roots. These are squared distances, not distances. With

alpha=B.B, beta=B.C, gamma=C.C, Delta=alpha*gamma-beta^2=(bd)^2>0,

r1=alpha+u-v, r2=gamma+u-w,

define the scaled residual

F(s)=gamma*r1^2-2*beta*r1*r2+alpha*r2^2-4*Delta*u.

This is a Gram/adjugate quadratic form rather than an implementation of the paper's solved x,y residual. The vector X is the unique vector with 2B.X=r1 and 2C.X=r2. Its squared norm is the first three terms divided by 4Delta. Consequently F=4Delta*G and has the same zeros and signs. At a zero, |X|^2=u and the two linear identities give |X-B|^2=v, |X-C|^2=w. All three are nonnegative; taking eighth powers proves the original powered-distance equations with no negative-root or squaring branch. Conversely every real solution gives this unique s and this Gram lift.

Distinct s necessarily give distinct X because s=|X|^16. There is also an independent stronger injectivity witness: x(s)=b/2-[(s+lambda)^(1/8)-s^(1/8)]/(2b) is strictly increasing for s>=0, by strict concavity of t^(1/8), and remains strictly below b/2 at every finite s. Thus a branch cannot be counted repeatedly at different sign brackets.

The table's six increasing finite cutpoints would prove five distinct roots by continuity if their strict alternating signs are actually certified. No monotonicity of F/G, uniqueness inside a bracket or exact total root count is needed. These endpoint signs are not yet independently computed at this initial seal.

## Centered positive-polynomial boundary mechanism

I will independently isolate the boundary parameters through r=1/2-t, not by evaluating the difference of two nearly equal large even powers. Put V=r^2+h^2+1/4. Then

((t-1)^2+h^2)^8-(t^2+h^2)^8
= (V+r)^8-(V-r)^8
=16*V^7*r+112*V^5*r^3+112*V^3*r^5+16*V*r^7.

This identity follows by binomial cancellation. For r>=0 its right side is a polynomial with positive coefficients and positive derivative; it is odd in r. Since all three specified right sides 1, lambda and 1-lambda are positive and each q is nonzero, each boundary root is a unique positive r, hence a unique t<1/2. It tends to infinity with r. A rational upper bracket still needs an explicit exact sign check. This provides a separate stable construction/uniqueness route for the same algebraic points. The sign of h is retained in point coordinates even though the defining polynomial depends on h^2.

The original global convexity proof is consistent: g''(t)=16(t^2+h^2)^6(h^2+15t^2)>0 for the nonzero h used. Therefore g(t-1)-g(t) is strictly decreasing, with leading term -16t^15. The q=0 and h=0 degenerate extensions are not assumed; all actual input q and heights must be checked.

## Exact face compatibility as a cycle constraint

Write the ordered edge powers as (a,f,f+lambda,g,g+1-lambda,a+1), derived from the three exact boundary defining equations. The alternating sums agree exactly. The three incoming face equations are a linear potential-difference system on the odd triple. Its incidence matrix has rank two and one cycle relation. Choosing

r1-r3=M=a-f, r5-r3=L=g-f-lambda

makes the third equation exact because M-L=a-g+lambda. This is an algebraic identity, not an interval test for zero. Similarly the outgoing equations reduce exactly to qB-qA=lambda and qC-qA=1, with the third face following from their difference.

Thus the common-focus solutions serve the same fixed constructed boundary, and the incoming center can be chosen independently afterward without changing it. No generic flip-existence theorem is required. The odd algebraic roots are fixed constants; enclosure variables must never be interpreted as freely selected new boundary values at different endpoints.

## Incoming lift and domain

Translate by A3 and put B'=A5-A3, C'=A1-A3. Their Gram determinant is det(B',C')^2. The incoming residual has exactly the same Gram form with shifts L,M. If L,M>0 and the determinant is strictly positive, it is continuous throughout the stated s interval. Strict opposite signs at 1/100 and 11/1000 would give an actual incoming center for the same exact boundary.

For coordinate enclosures I can use the dual vectors

dualB=(gamma*B'-beta*C')/Delta,
dualC=(alpha*C'-beta*B')/Delta,

Y=(alpha*dualB+gamma*dualC)/2
 +(dualB+dualC)*u/2-dualB*v/2-dualC*w/2.

Combining the shared u coefficient before interval evaluation avoids treating duplicate occurrences as unrelated. The identity is derived from the Gram system; its use is not a change of boundary. Validated interval ranges must exclude zero denominators and negative radical arguments.

## Distinct falsification families and exact remaining gaps

1. **Real branch and powered-distance equivalence.** Attack incorrect use of squared vs ordinary distance, negative eighth-root branches, an s<0 domain, or a rank-deficient focus system. The Gram derivation above is the proof mechanism; actual constants must satisfy Delta>0. A found real solution not represented by s, or a zero producing a wrong original equation, would falsify equivalence.

2. **Counting and multiplicity.** Attack double-counted centers, overlapping or reordered brackets, endpoint zeros, an infinite fifth point, or an unjustified exact-five conclusion. Strict endpoint signs, disjoint finite intervals and injectivity provide the correct at-least-five result. Endpoint signs remain to be independently validated.

3. **Algebraic boundary isolation and orientation.** Use the centered odd positive polynomial to isolate all three parameters independently. Attack height-sign mistakes in coordinates, missing scaling by |q|^16, additional real roots, or numerical replacement of an algebraic specification. Rational isolating endpoints and polynomial signs remain to be produced.

4. **One-boundary simultaneous quantifiers.** Attack independent choices from interval boxes, changing the sextuple between residual endpoints or outgoing branches, and loss of dependence in L/M. The exact symbolic edge cycle handles simultaneity; all strict inequalities must hold uniformly over enclosures containing the one fixed algebraic tuple.

5. **Incoming existence and all six faces.** Attack a wrong translation, determinant sign/order, shifted-radical domain, swapped L/M, or a third equation justified only by an enclosure containing zero. The Gram system plus rank-two cycle algebra reconstructs all six exact equalities. Strict incoming signs and bounds still need certification.

6. **Degenerate points and lines.** Verify six boundary vertices are distinct, both alternating triples are noncollinear, and each selected center avoids all boundary vertices. The stronger all-20-triples and all-15-pair-lines claims require explicit oriented-area bounds. Positivity of lambda gives x<b/2 for every outgoing point, excluding A1/A5 once their boxes lie to the right; A,B,C and A3 require their respective exact exclusions. Incoming and outgoing selected centers are also separated if the claimed incoming x box is confirmed, because it lies right of b/2.

7. **Crossing and embedding scope.** Certify the four strict orientation signs for the two indicated boundary segments. A zero orientation or endpoint intersection cannot establish a strict crossing. A genuine strict crossing rules out a proper embedding for every central-point choice, but does not invalidate a crossing-permitted realization. The actual primary definition may impose further nondegeneracy or domain conditions; it must be read directly after this seal.

8. **Large-radius conditioning and finite validity.** At s=10^16 use exact u=100 and concavity bounds for the tiny differences, or the Gram expression with rigorous rational root bounds. Never decide signs by subtracting rounded large radicals. The stated rational limiting norm gives a separate analytic tail check; its integer arithmetic still needs checking. Continuity at s=0 is harmless even though a derivative diverges there; selected brackets are positive.

9. **Independent certificate kernel.** I plan dyadic enclosures obtained by three outward integer-isqrt square-root stages for eighth roots, rather than the described native decimal-grid eighth-power search. Combined with the centered boundary polynomial, Gram residuals and exact oriented areas, this yields materially independent arithmetic and expression structure. Correctness requires proving each enclosure by integer inequalities, testing signed multiplication/squares/division, and retaining any ambiguous-sign failure rather than forcing a sign.

10. **Primary convention and credit interfaces.** After the initial seal, read the actual cited quad/realization definitions and exact common-focus remark/question. Check whether full construction curves or restricted arcs are counted, whether crossings and selected degeneracies are permitted, and whether the two curves genuinely share the required focus. Read the weighted-distance interfaces before accepting the credit comparison. No unsuccessful search can certify firstness or present openness.

11. **Supplied code and certificate scope.** Only after my own proof/exact-test freeze will I read the complete selected program and requirements and inspect its actual imports, defaults, I/O and optimized-mode guards. I own the sole bounded native replay. It must use unchanged isolated bytes and compare the whole actual expected output/certificate, preserving stderr and failures. A successful program cannot replace the geometric proof or primary-domain check, and internal bookkeeping is not an independent-theorem count.

## Initial disposition and next evidence

The algebraic reduction, fixed-boundary logic, branch selection, monotonic boundary-root mechanism and at-least-five implication are reconstructed. I have not yet independently certified the numerical inequalities, excluded every geometric degeneracy, checked primary conventions or audited the supplied program. These are explicit remaining validation tasks, not assumed conclusions. No substantive defect is established at this point, and no PASS is inferred from the manuscript's own certificate claims.

I will first complete my own exact diagnostic and proof record, freeze those results, then inspect actual primaries and selected source support. Root130 is CLOSED; no scientific findings from this lane will be released before its explicit opening. Follow-up remains null unless a separate high-bar case emerges.

# Independent core reconstruction

Recorded UTC: 2026-10-17T23:15:05.987844+00:00

Exposure before this note: parent task assignment; filenames from a restricted `rg --files` of `inputs/`; exactly `inputs/PROOF.md`, SHA256 c4608dbf5f9e39b398f7db20100273fdab085598382293f8224488585015f658 (10412 bytes). No prior AUDIT, ACCEPTANCE, acceptance/root report, other reviewer report, STATUS, MANIFEST, README, SOURCE_METADATA, or SOURCE_DEPENDENCIES content was read. PROOF's internal audit endorsement was observed as part of the source, but is excluded as evidence.

## Core deduction, before source lookup or computational checking

Fix an integer m >= 2 and suppose the stated smooth connected cavity surface H_q in the half ball exists, with area q and first positive eigenvalue exceeding T=q(q+m-1). The boundary disjoint union has one zero from each of the two connected components. For the sphere the dimension of degree-l homogeneous polynomials in m+1 variables is C(l+m,m). Harmonic decomposition removes |x|^2 times degree-(l-2) polynomials, giving d_l=C(l+m,m)-C(l+m-2,m), with the second summand zero at l=0,1. The function l(l+m-1) is strictly increasing for nonnegative integer l, because the successive difference is 2l+m > 0. Thus sphere modes strictly below T are exactly degrees 0,...,q-1. Telescoping the dimensions leaves C(q+m-1,m)+C(q+m-2,m), including q=1 under the zero convention. Call this N. The cavity contributes exactly one mode below T. Consequently exactly N+1 full boundary modes lie below T and the next mode, numbered N+2 with 1-based indexing, equals T. The entire T eigenspace has sphere multiplicity d_q; no cavity ties occur under the strict gap. q=1 gives N=1, k=3, and the two preceding zeros, providing an immediate indexing control.

For q>=m, each top binomial coefficient is at most (q+m)^m; hence N+2<=2(q+m)^m+2<=2^(m+2)q^m. The final inequality is deliberately loose: q+m<=2q and 2<=2^(m+1)q^m. Raising to 2/m gives k^(2/m)<=2^(2+4/m)q^2. The exact leading N asymptotic is 2q^m/m!, so k^(2/m)/q^2 tends to (2/m!)^(2/m), but only the elementary upper bound is needed.

Write A=q+rho, V=volume, alpha=1+2/m=(m+2)/m, and beta=m/(m+1). Then I=A/V^beta and I^alpha=A^alpha/V^((m+2)/(m+1)). The half-ball cavity gives v<=V<=omega with v=omega(1-2^(-(m+1)))>0. Therefore the denominator D=I^alpha+k^(2/m) is at most K A^(1+2/m)+C q^2, where K=v^(-(m+2)/(m+1)) and C=2^(2+4/m). The numerator F=T A^(2/m)>=q^2 A^(2/m). Hence D/F<=K A/q^2+C/A^(2/m), which tends to 0 for fixed m and fixed rho,K,C. Since F,D are positive, F/D tends to +infinity. In m=2 the first term is order q^-1 and the second also order q^-1; for m>2 the second order q^(-2/m) is slower. No common-domain Weyl limit enters this deduction. A fixed-domain Weyl statement says nothing about this moving-domain family.

For arbitrary finite real coefficients a,b, positivity of X=I^alpha and Y=k^(2/m) gives aX+bY<=M(X+Y), with M=max(0,a,b). Once F/(X+Y)>M the target bound fails. Thus failure for positive constants already rules out every finite real pair, including zero and negative coefficients. This extension does not depend on dividing by a possibly nonpositive proposed right side.

## Independent vulnerabilities to test

1. Any additional cavity eigenvalue below T invalidates the exact k=N+2 choice. A cavity eigenvalue equal to T does not invalidate the first index; it only increases the multiplicity at T.
2. Omitting the additional cavity zero shifts to k=N+1 and returns a value strictly below T. Counting sphere modes <=T in N shifts the advertised index past the entire T cluster if the cavity next positive eigenvalue is chosen larger than the next sphere level.
3. Multiplicity and binomial conventions require explicit q=1, q=2 controls; expressions with negative upper indices are not unrestricted generalized binomial coefficients.
4. Raising a bound to power 2/m is monotone only for positive quantities, which hold here. Taking an mth power makes the combinatorial inequality rational/integer checkable.
5. The normalization exponent for volume is (m+2)/(m+1), not (m+2)/m. Scaling by t in Euclidean space multiplies lambda by t^-2, area by t^m and volume by t^(m+1); every term in the intended inequality is invariant.
6. Geometry: connectedness of the open exterior inside the outer ball follows by joining a path to the first encounter with radius 3/4. Any path outside radius 3/4 remains in a full annular region when clipped appropriately. The cavity closure must stay inside the half ball for volume and disjoint boundary statements. This is justified if H_q is compact inside that open ball and bounds its bounded complementary component.
7. The existence input is the crucial independent mathematical dependency. The spectral deduction alone does not construct a smooth H_q and numerical multisets cannot certify its existence. This review will not treat toy spectral computations as a numerical smooth construction.

Initial checkpoint completion estimate: 25% toward an independent spectral/counting/asymptotic validation, with source scope and exact adversarial checks still pending.

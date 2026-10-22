# Independent mathematical falsification review

## Scope and outcome

The claim reviewed is the fixed-caustic, strictly nested, nondegenerate confocal **elliptical** billiard theorem with genuine least collision period N divisible by four. The fixed winding is coprime to N and is oriented with 0<tau<N/2. Area is algebraic shoelace area in traversal order. Inversion has unit radius about an original focus and acts on vertices, which are then joined by straight segments. Hyperbolic/degenerate caustics and arbitrary repeated lists of displayed length 4n are excluded. The circle is a separate elementary extension.

I found no mathematical defect in the real proof or the retained complex proof within that scope. This conclusion comes from checking the analytic arguments, not from interpreting finite residuals as a universal certificate. The exact unrestricted repeated-list assertion is false for the connected triangular family below, as the current package states. The positive theorem and the repetition limitation are already known from Ferudun. No novelty is inferred from this verification.

## Real proof: normalization, coefficients and domain

Stachel's canonical theorem supplies P(w)=(-a sn w,b cn w), a=alpha dn(v)/cn(v), b=beta/cn(v), delta=2v=4K tau/N. Since the real parameter traverses the ellipse exactly once modulo 4K, closure and coprimality give the actual least period. Put m=N/2 and ell=2K/m. For N divisible by four, m is even and tau is odd. The m-step shift is antipodal. Moreover gcd(tau,m)=1, so the m summands of S permute the uniform real grid modulo 2K. This does not assume a uniform eccentric-anomaly advance.

For an edge centered at u, the half determinant of the two original endpoints is

    ab sn(v) cn(v) dn(u)/(1-k² sn²(v) sn²(u)).

The dn addition formula converts this to C_A[dn(u-v)+dn(u+v)]/2, with C_A=ab sn(v)cn(v)/dn(v). Thus the N-edge sum is C_A times the N-vertex dn sum, or 2 C_A S(w). The factors of two in the manuscript are correct. For a star, these are signed determinants; with this forward orientation they are positive because the nested caustic contains the origin.

The real focal square is (a+c sn w)², with a+c sn w>=a-c>0. It is the square of a positive distance, rather than a complex Hermitian norm. Dividing the translated endpoint determinant by the **square** of the product of positive focal distances gives the stated E(u). In particular the coefficient C_0=b sn(v)dn(v)cn⁴(v)/alpha³ has dimension inverse area, while C_A has dimension area. Their product is dimensionless, as the invariant must be. The antipodal E(u)+E(u+2K) addition gives the displayed B, including the V(V+2U) term.

The local identity can be checked as a polynomial identity in x=sn²(u), after multiplying by dn(u)H², H=U²-k²V²x. I independently formed its three coefficient equations and solved them without importing the package checker. With r=k², the solution is precisely a0=q/(U-V)², a1=(Lambda-a0)/2, and 4 sn(v)cn(v)dn(v)a2=(V²-U²t)/[(U²-rV²)(U-V)]. INDEPENDENT_EXACT.py records this separate elimination. The reciprocal-dn addition identities and the derivative of sn(u)cn(u)/H give the derivative multiplier 4 k² sn(v)cn(v)dn(v)V. There is no lost W, sign or factor of two.

The real hypotheses give 0<k<1 and 0<v<K, so sn(v), cn(v), dn(v), q and k-prime are positive. Also

    U=(1-k²)+k²q²>0,
    W=1-k²t²>0,
    U-V=2t(1-k²)>0,
    U²-k²V²=(1-k²)W²>0.

Consequently U>|kV|, H>0, and all actual denominators are nonzero. There is no division by V. This is a genuine domain argument, not a numerical observation. In the exceptional case V=0, cn(delta)=0 and 0<delta<2K force delta=K. Coprimality then gives N=4,tau=1. The coefficient a2 is finite, while F'(u+K)-F'(u-K)=0 by the 2K period. The direct reduced polynomial (1-k²tx)=q+t(1-k²x) and the axial area calculation verify this case without taking a limit.

Finite cyclic reindexing makes the two F sums equal and cancels the derivative difference. Hence the surviving coefficient is a0+2a1=Lambda. The quarter-shift formula dn(u+K)=k-prime/dn(u) yields R(u)=2C_0 Lambda S(u+K)/k-prime. Positivity of Lambda is explicit: the numerator bracket p(t)=r²(t³+t²)-5rt+r+2 decreases on (0,1), and p(1)=2(1-r)²>0. An independently checked positive-term expression is 2(1-r)²+5r(1-r)q+r²q²(4-q), useful also for stable numerical evaluation.

## Fourier/Landen completion

For a fixed 0<k<1 the dn Fourier coefficients decay geometrically, so absolute and uniform convergence on the real line legitimizes summation over the finite grid. Filtering retains Fourier indices divisible by m. With rho=exp(-pi K-prime/K), the transformed nome is rho^m, not a root of rho. If kappa has that nome, K_m=K(kappa) and lambda=m K_m/K, then both the constant Fourier coefficient and every remaining frequency match

    S(w)=lambda dn(lambda w,kappa).

In particular lambda ell/2=K_m, so the quarter shift gives S(w)S(w+ell/2)=lambda² kappa-prime. The remaining phase shift is exactly (K+v)/ell=(m+tau)/2, a half-integer. This establishes the universal phase constancy and the explicit positive value 4 C_A C_0 Lambda lambda² kappa-prime/k-prime. This step supplies the universal conclusion; samples and finite symbolic algebra cannot replace it.

Central negation is an ordered cyclic half-orbit shift and exchanges the foci. Simultaneous negation preserves area, so both focal inverse areas coincide. Reversal negates both signed areas and preserves their product. Repeating an admitted primitive cycle r times multiplies each shoelace sum by r, and the product by r². For the axial N=4 orbit, A=2ab and A_inverse=2/(ab), giving the credited value 4. For the circle, direct regular-star shoelace areas give N² sin²(2pi tau/N)/4, with no appeal to a degenerating-torus limit.

## Retained complex proof

I separately checked the native PROOF.md Sections 2–7. This route is viable on the torus X=C/(ell Z+4iK-prime Z). The 4iK-prime period matters: dn is anti-periodic under 2iK-prime, not periodic there. The proof uses the correct character.

For S, each reduced pole class has exactly one contributing grid summand, because the grid is primitive modulo 2K. Thus the poles at p=iK-prime and p+2iK-prime are simple, with nonzero residues -i and +i. Evenness and the imaginary anti-period force zeros at p+ell/2 and p+2iK-prime+ell/2. These are finite distinct points; the degree-two zero divisor makes them the only zeros and makes them simple. The half-shift product therefore has no poles on a compact torus. Its constancy is not being inferred merely from finite periodicity.

For generic V nonzero, B's possible poles on the base 2K by 4iK-prime torus arise from reciprocal dn at r=K+iK-prime and its imaginary translate, and from H=0 at r±delta and their translates. At r the H value is U²-V²=(U-V)(U+V)>0; here U+V=2q dn²(v)>0. Thus those poles are at most simple. On the sn² torus H has a double pole at p and exactly two simple zeros r±delta: the shift sn(r+z)=dn(z)/(k cn(z)) verifies the zeros, which are distinct unless delta=K, excluded in the generic case. Squaring H allows at most double poles there. At the common poles of sn,cn,dn, the numerator has pole order at most four and dn H² order five, making B removable. These observations exhaust its singularities.

The reflection formulas sn(2r-u)=sn(u), dn(2r-u)=-dn(u) imply B(2r-u)=-B(u). Therefore the two Laurent coefficients of order minus two at r±delta are opposite. Both shifted locations lie in the same cyclic delta orbit, with one contribution of each type at every possible reduced pole; the double terms really cancel in R. Nonadjacent vertex coincidences or disappearing leading coefficients do not invalidate this upper-order argument. R has at most the two stated simple poles on X.

When V=0, the separately displayed B=2C[q/dn+t dn]/U² has only simple poles. For m=2,ell=K, the p and r real classes coincide in X. The same two-pole conclusion holds. Matching one residue against S(u+K), and using the common anti-period for the second residue, removes all poles. A holomorphic difference on compact X is constant; its anti-period makes that constant zero. This supplies R=C_R S(u+K). The half-grid relation then completes the proof just as in the real route. No unsupported assertion equivalent to the target invariant is used.

The extra complex-function samples in INDEPENDENT_GEOMETRY.py check the reflection, reduced period, anti-period and half-grid product for five cases, including N=4 and a primitive star. They support arithmetic consistency only. The preceding divisor and Laurent arguments, rather than those samples, establish completeness.

## Exact connected primitive-three obstruction

Under (x,y)=(2sqrt(2)X,sqrt(5)Y), the outer ellipse becomes the unit circle and the inner ellipse has axes 2/3 and 1/3. For distinct circle endpoints z=(X,Y),z'=(U,V), let n_chord=(V-Y,X-U) and s=n_chord dot z. A fresh rational two-parameter calculation gives

    s²-(4/9)n_chord,x²-(1/9)n_chord,y²
      = |z-z'|² (3 X U+6 Y V+2)/9.

The scalar factor is positive for a genuine chord, proving the claimed tangency equivalence. This also addresses the distinction between a conic-support identity and an actual distinct-endpoint chord.

Put n=(3X,6Y), D=|n|² and Jn=(-6Y,3X). Since 9<=D<=36, the two stated neighbors (-2n±sqrt(D-4)Jn)/D are continuous, distinct unit-circle points, neither equal to z. Their mutual chord is tangent as well, checked exactly. Three distinct circle points cannot be collinear. The ordered orientation at z=(1,0) has determinant 10sqrt(5)/9>0 and persists. Moving z along a half-circle sends the full ordered triple continuously to its central negative; the signs and ordering are consistent throughout.

The physical reflection identity follows directly from outer incidence. Expanding its left side gives vy²(8-x²)+vx²(5-y²)+2xy vxvy. Replacing 8-x² by 8y²/5 and 5-y² by 5x²/8 gives 40(x vx/8+y vy/5)². The independent exact script checks this full-family identity using outer incidence alone. For a unit caustic-tangent direction the left side is 40/9. The two inward tangent directions therefore have normal component -1/3 and opposite tangential components, proving Euclidean specular reflection. Since the inner ellipse is strictly nested and convex, each tangency contact lies inside its outer chord. Three distinct collision points establish least period three.

Fresh exact full-translation inversion and shoelace calculations give both original areas 50sqrt(2)/9 and inverse areas (8sqrt(2)∓sqrt(3))/80. Fourfold repetition gives length twelve, retains least period three, and has product difference -20sqrt(6)/9. Exact support, internal contacts and the reflection law were checked at all six displayed collision vertices. This is a valid family counterexample to the unrestricted listed-length claim and is compatible with the positive theorem.

## Computational evidence and its limits

The fresh package harness passed 77 identities ordinarily and under -O, plus the documented damaged-factor, damaged-decomposition, wrong-focus-sign, NaN, existing-output and precision controls. A separate ordinary geometry run matched its stored default result byte for byte. The optional stress run passed at 150 digits. Fifteen additional invalid-input controls were rejected under -O, including exact NaN/infinity/nonzero residuals, geometric NaN/infinity, inversion-center collision, invalid period types, invalid moduli and precision boundaries.

The reviewer script INDEPENDENT_EXACT.py now checks 61 exact identities, including a distinct coefficient solve, chord tangency factorization, full-family reflection algebra, contacts and areas. Its ordinary and optimized outputs agree byte for byte. Its first development run stopped because SymPy could not infer symbolic positivity of sqrt(b²+c²)-c; the N4 fixture was reparametrized rationally, with the limitation recorded in the research log. This was a reviewer-script inference failure, not evidence of a package defect.

The independently authored geometry script imports no package program or stored result. At every step it obtains the next collision from a tangent contact to the normalized caustic, and then independently checks the Euclidean reflection law. It covers every coprime forward winding for N=4,8,12,16,20,28, each at k=0.37 and 0.91 and at three phases: 38 families, 114 target phase samples. It checks contacts, incidence, closure, winding, absence of earlier returns, both foci, positive signed areas and the explicit constant. Its largest observed absolute residual is 4.02331561731e-97 at 100 digits. Five groups of complex-identity samples have largest residual 1.8421393652e-99. These are floating-point residuals, not interval enclosures, all-parameter error bounds, proof-assistant results or human peer review.

# A critical-axis repair family is admissible but cannot minimize

16 October 2026. Final pass for the unchanged E-6322 benchmark. The family below is a diagnostic search route, not a counterexample. Its nonaffine boundary trace meets the frozen full smooth diffeomorphism requirement. A weak fiber-pressure obstruction rules out every member with the stated finite-energy parameters, even though all leading preimages of the third target axis are critical.

## 1. Family and parameter range

On the unit ball B_1 in R^3, write z=x_3, rho^2=x_1^2+x_2^2, r=|x| and t=z^2/r^2. Choose

    m>1/2,  beta>2m,  delta>0,
    s=2m+beta>3,  gamma=s-3,
    2 gamma+delta<3.

Define y(0)=0 and, for r>0,

    y_1=r^{m-1}x_1,
    y_2=r^{m-1}x_2,
    y_3=z rho^2 r^{beta-3}+z r^{beta+delta-1}.       (1.1)

A concrete member has (m,beta,delta)=(3/4,9/4,1/4), for which gamma=3/4 and 2 gamma+delta=7/4. Its first two gradient rows are unbounded near zero, so its rejection does not depend on the earlier whole-map C^{1,1/2} regularity criterion.

## 2. Exact determinant and permitted trace

Direct cylindrical differentiation gives

    J_y=r^gamma { (1-t)[m+(beta-3m)t]
                 +r^delta[m(1-t)+(beta+delta)t] }. (2.1)

Because beta>2m, the first square bracket is bounded above and below by positive constants; the same is true of the correction bracket. Consequently

    J_y is comparable to r^gamma[(1-t)+r^delta],    (2.2)

with constants depending only on the parameters. In particular J_y>0 away from zero.

On the unit sphere, (1.1) has trace

    g(x)=(x_1,x_2,x_3(1+x_1^2+x_2^2)).

This is the trace of the global smooth orientation-preserving diffeomorphism

    G(X)=(X_1,X_2,X_3(1+X_1^2+X_2^2)),
    det DG=1+X_1^2+X_2^2>0.

Its inverse divides the third coordinate by 1+X_1^2+X_2^2. The ball and the entire prescribed boundary thus satisfy the frozen data assumptions, with a genuinely nonaffine trace.

## 3. Finite energy and determinant degeneration

Since beta>2m>m and delta>0, |Dy| is bounded by C r^{m-1} for 0<r<1. The strain-sixth-power integral is finite because m>1/2. The elementary polynomial bounds |cof F|^3<=C|F|^6 and (det F)^2<=C|F|^6 make both other positive terms integrable.

The leading angular zero in (2.2) occurs at the two poles. There 1-t=sin^2 theta is quadratic in angular distance, and sphere area is comparable to theta dtheta. Therefore

    integral_{S^2} [(1-t)+epsilon]^{-2} d sigma
        is comparable to epsilon^{-1},   0<epsilon<1.

For example, near a pole the substitution u=theta^2 reduces the integral to a fixed multiple of integral_0^c (u+epsilon)^{-2}du. Thus

    integral_{S^2} J_y(r theta)^{-2} d sigma
        is comparable to r^{-2 gamma-delta}.

The radial barrier integral is finite exactly when 2 gamma+delta<3. The maps in (1.1) consequently lie in the full admissible class. Also J_y<=C r^gamma tends uniformly to zero as r tends to zero, so ess inf J_y=0.

These facts by themselves would not establish a counterexample: minimality is the missing condition, and it is false below.

## 4. The limiting axis is entirely critical

The exact weighted leading profile is

    U_1=r^{m-1}x_1,
    U_2=r^{m-1}x_2,
    U_3=z rho^2 r^{beta-3},

with weights (m,m,beta). Under componentwise annular rescaling, the repair vanishes in C^1 on every compact annulus. In annular coordinates xi, the exact relation is

    Y_{k,3}(xi)=U_3(xi)+r_k^delta xi_3 |xi|^{beta+delta-1}.

The limiting determinant is

    J_U=r^gamma(1-t)[m+(beta-3m)t].                 (4.1)

It is positive off the polar axis and zero on that axis. Since U_1=U_2=0 only when rho=0, every leading preimage of the third target axis is critical. Moreover U_3=0 on those rays. Thus the regular-axis-preimage argument from the earlier passes cannot be applied directly to this profile, and no positive local degree at its nonisolated zero is assumed.

## 5. The necessary pressure equation still applies off the axis

Suppose y were stationary under all compactly supported smooth variations in a punctured neighborhood of zero, as every full-class minimizer would be. On an annular patch with J_U>0, its rescaled gradients converge in C^1 and stay in a compact subset of GL^+(3) after normalization. The ordinary Euler equation is valid there.

For the third stress row, the barrier scale is

    tau_3=2m-2-3 gamma,

whereas all positive-degree stresses are O(r_k^{4m+beta-5}). Their exponent difference is

    (4m+beta-5)-tau_3=4 gamma>0.

Dividing the weak third-row equation by r_k^{tau_3} and passing to the limit gives

    div[J_U^{-3}(cof DU)_3]=0                     (5.1)

on every positive-J patch. At a local diffeomorphism chart X=U(x), the cofactor identity changes (5.1) into

    partial_{X_3}[J_U(U^{-1}(X))^{-3}]=0.

The determinant is therefore constant along every sufficiently short fiber of (U_1,U_2). This is a local statement on positive patches, so critical target-axis preimages create no obstacle to using it.

## 6. Non-axis fibers force an impossible parameter pair

Fix a nonzero transverse target radius q=|(U_1,U_2)| and its azimuth. On a positive-z branch of the fiber,

    q=rho r^{m-1},
    rho^2=q^2 r^{2-2m},
    t=1-q^2 r^{-2m},
    r>q^{1/m}.

This is a regular curve: r is its radial parameter, and DU is invertible there. Since U_1 and U_2 are fixed, U_3 has nonzero derivative along each sufficiently short portion, and those portions map to vertical target segments.

Substituting into (4.1) gives the exact fiber determinant

    J_U=q^2[(beta-2m)r^{beta-3}
            -(beta-3m)q^2 r^{beta-2m-3}].          (6.1)

Constancy on any open r interval forces the coefficients of its two distinct differentiated powers to vanish:

    (beta-2m)(beta-3)=0,
    (beta-3m)(beta-2m-3)=0.                        (6.2)

The two powers differ by 2m>0, so cancellation on an interval is impossible. Because beta>2m, the first equation gives beta=3. The second then becomes (3-3m)(-2m)=0, hence m=1. This exceptional pair has gamma=2, contradicting 2 gamma+delta<3 for every delta>0.

Thus (5.1) fails for every parameter tuple under consideration. No member of (1.1) is stationary on any punctured neighborhood of zero. In particular none is a full-class global or local minimizer.

This also supplies a rigorous strict-descent conclusion, even without writing a closed-form competitor: failure of the smooth limiting weak equation gives a compact test on a positive-J patch with nonzero normalized first variation. For sufficiently small physical annuli the corresponding first variation for y is nonzero. Choosing its sign and then a sufficiently small parameter strictly lowers the full energy; compact gradient bounds preserve the determinant constraint and the full boundary trace.

## 7. Scope of the rejected route

This family includes the balanced example listed in Section 1, also ruled out by `DEGENERATE_TANGENT_OBSTRUCTIONS.md`. The present fiber calculation rejects subcritical members as well, where s+3m<6 and that general balanced/superbalanced theorem does not apply. For instance (m,beta,delta)=(3/5,2,1/4) has gamma=1/5 and s+3m=5<6.

The calculation does not reject every critical-axis or angularly degenerate profile. A different profile could satisfy the local fiber-pressure identity, and then still require all other Euler equations and a full-class global comparison certificate. No such minimizing map has been obtained in the five passes. General irregular boundary degeneration also remains unsettled.

All conclusions hold for arbitrary fixed positive coefficients a,b,c,d. No exponent, data class, or comparison class in the benchmark has been modified.

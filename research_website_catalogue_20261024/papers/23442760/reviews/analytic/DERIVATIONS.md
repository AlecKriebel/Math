# Additional independent derivations and falsifiable checks

The universal main construction and lower proof are fully reconstructed in REPORT.md and were already present in INITIAL_RECONSTRUCTION.md before primary reading. This document records an independent source-interface calculation and diagnostic distinctions; it does not change the manuscript or repair its theorem.

## Older endpoint ingredient: actual applicability and normalization

Totik–Varga's endpoint parameter a=0 is allowed. With psi(v)=sqrt(v), the right limit is zero, psi(v)<=sqrt(2)psi(v/2), and integral_1^infinity psi(v)/v^2 dv=2. Their polynomial P_m has degree <=m, P_m(0)=1, sup_[0,1]|P_m|<=2 and |P_m(t)|<=A exp[-c(m^2t)^(1/4)] for t>0. No assertion about an arbitrary pushforward measure being doubling is needed here.

By the classical interval Markov inequality, sup|P_m'|<=4m^2 on [0,1]. Thus for h=1/(8m^2), P_m(t)>=1/2 on [0,h]. Compose with the manuscript's u=g/G and square: R_m=P_m(u)^2. The denominator is at least F(h)/4. On the core the first moment is at most 4hF(h). On dyadic shell j the tail estimate and the independently established F(t)<=(t/h)^n F(h) give a contribution at most

    h F(h) A^2 2^(n+1) 2^(j(n+1)) exp[-2c(2^j/8)^(1/4)].

The sum over j>=0 converges: its ratio tends to zero because the negative exponential in 2^(j/4) dominates linear j(n+1). Its bound is independent of m, K and a for fixed n and the theorem's constants. Divide by F(h)/4 to obtain O_n(m^-2). Since deg(P_m(u))<=2m, m=floor(r/2) gives a feasible global square for r>=2, with the constant density covering r=1. Multiplication by G gives the same scoped quadratic upper rate, with a different nonexplicit constant. This confirms the manuscript's stated deduction from older endpoint ingredients. It does not certify that any prior paper explicitly printed the full convex-body theorem or assign firstness to this deduction.

The use of a main explicit Dirichlet kernel avoids importing this approximation theorem. The classical theorem's proof was read, but its older symmetric-polynomial references were not independently re-proved. This is a contextual alternative, not a new load-bearing import.

## Quantitative exact examples, not optimization certificates

For K=[0,1], f=t, the actual theorem proxy is u=(t+t^2)/2 with H=0, gamma=1, G=2. Exact integration of A_m(u)^6 for m=1,...,5 gives normalized objective values approximately 0.132742, 0.0582233, 0.0322386, 0.0203320, 0.0139435 at square-root degrees 6m. These are feasible witness errors, not exact H_(6m). Every numerator/normalizer is stored as a rational number. The universal upper constant is deliberately much larger.

On the standard triangle x,y>=0,x+y<=1, f=x+y-xy is nonnegative, nonconvex (Hessian eigenvalues +/-1), minimized at the corner zero. Here H=1, gamma=3/2, g=x+y+(3/2)(x^2+y^2), G=5/2 (convex g has maximum at a vertex). The exact monomial formula integral x^i y^j=i!j!/(i+j+2)! yields witness errors approximately 0.212948 and 0.0992381 for m=1,2, with L=4 and square-root degrees 8m. The check exercises a nonsmooth body, nonstationary boundary minimizer, and nonconvex objective simultaneously, while the proof covers all such bodies independently.

For an interior minimizer, f=(t-1/2)^2 has H=2, gamma=2, G=1/2 and u=4(t-1/2)^2. The m=2,L=3 square gives error approximately 0.00453930. Constant objectives have identically zero error and need no computation.

The exact Hilbert moment pencils for t on [0,1] at orders one through five have characteristic polynomials proportional to shifted Legendre P_(r+1)(2z-1). This tests the normalization/order interface and independently ties selected finite optimum problems to the classical endpoint setting; it is not asserted to prove the all-r spectral theorem.

## Meaning of negative controls

The deliberate changes test necessary interfaces, not just parser success. L=n+1 makes the infinite shell ratio one; choosing one extra m at r=2L breaks the root-degree budget; removing the normalizer changes total mass; an odd exponent can make the density negative; replacing the kernel argument breaks its trigonometric polynomial identity; replacing (r+1)^2 by r^2 fails the endpoint reproducing-kernel dimension; arbitrary measures can have zero near-minimizer mass (e.g. delta_1) even when the body is an interval. All seven are detected. They are not defects in the actual manuscript.

## Classical lower-proof identities at all degrees

For completeness, Rodrigues gives orthogonality to every polynomial of degree below j after j integrations by parts: (x^2-1)^j has zero endpoint derivatives through order j-1. Its leading coefficient is c_j=(2j)!/[2^j(j!)^2]. A further integration-by-parts calculation gives

    integral_-1^1 P_j^2 = (c_j/2^j) integral_-1^1 (1-x^2)^j
                       = (c_j/2^j) 2^(2j+1)(j!)^2/(2j+1)!
                       = 2/(2j+1).

The beta integral in the middle can also be obtained by integration-by-parts recursion starting with integral 1=2. Expanding the manuscript's finite integral representation (all odd cosine powers integrate to zero; the average of cos^(2k) is binomial(2k,k)/4^k) reproduces the Rodrigues polynomial coefficients. Its integrand base has squared modulus x^2+(1-x^2)cos^2(theta)<=1. This establishes the uniform |P_j|<=1 at all j; the finite Gram tests are diagnostics rather than the justification of this universal identity.

An arbitrary measure with full support also need not satisfy the particular exponent-n growth estimate: on [0,1] take dmu=2t dt and u=t. F(t)=t^2, so F(1)=1 exceeds (1/(1/2))^1 F(1/2)=1/2. This is only a failure of the asserted Lebesgue scaling transfer; it is not a claim that this full-support weighted hierarchy cannot have quadratic convergence by another argument.

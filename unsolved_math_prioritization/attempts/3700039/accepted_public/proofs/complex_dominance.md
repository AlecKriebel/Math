# Fifth and final shared pass: arbitrary complex phases under second-harmonic dominance

## Result and scope

The phase-coherence gap in the accepted fourth-pass dominance theorem closes. The result below permits both complex amplitudes to vary arbitrarily and continuously with phase. No phase function, winding restriction, differentiability of amplitudes, fixed angular axis, or rigid drift is required.

The unrestricted periodic-triple assertion and the original normalized-supremum conjecture remain unresolved. No historical novelty is claimed. It uses the exact angular identity established in the [fourth-pass relative-phase proof](../baseline/accepted_public/proofs/relative_phase.md) and independently accepted in the [full independent fourth-pass audit](../baseline/accepted_public/audits/relative_phase_acceptance.md). The source target remains A. Eremenko, *Conjectured inequality for subharmonic functions*, 4 April 2015, https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The theorem proved here concerns the periodic cyclic subclass stated explicitly below.

## 1. Exact theorem

Let rho, omega > 0 and let n >= 1 be an integer. Let c be a continuous real 2 pi-periodic function, and A,B continuous complex 2 pi-periodic functions satisfying

    |A(s)| <= |B(s)| for every s.

For j=0,1,2 define

    H_j(s,theta) = c(s) + Re[A(s) exp(i(n theta+2 pi j/3))
                           + B(s) exp(2i(n theta+2 pi j/3))].

Suppose

    L H_j >= 0 in distributions,
    L = (omega partial_s+rho)^2 + partial_theta^2.

Write an overbar for normalized s-average and let

    M(s) = integral_0^(2 pi) med_j H_j(s,theta) dtheta,
    k = 3 sqrt(3)/(2 pi),
    Gamma = 6 sqrt(2)/(8+sqrt(2)).

Then

    overline[M/(2 pi)] >= ((Gamma-k)/2) overline[|A|]
                       >= (1/80) overline[|A|].                 (1)

The last inequality is strict whenever A is not identically zero, because Gamma-k>1/40. In particular:

- if A is not identically zero, M(s)>0 at some phase;
- if A is identically zero, M(s)=2 pi c(s)>=0 at every phase.

Thus the some-phase theorem holds for two arbitrary complex amplitudes under second-harmonic modulus dominance. In fact their full-torus average median is nonnegative, with the quantitative gap (1). Zeros, changing winding, nonuniform phase, both frequency resonances, and merely continuous distributionally admissible coefficients are included.

## 2. The modal L1 coercivity lemma

### First-order statement

For any smooth complex 2 pi-periodic function u, any real a, and omega>0,

    integral |omega u'+a u| ds >= |a| integral |u| ds.           (2)

To avoid dividing by zero, set R_epsilon=(|u|^2+epsilon^2)^(1/2). Then

    Re[conjugate(u)(omega u'+a u)/R_epsilon]
      = omega R_epsilon' + a |u|^2/R_epsilon.

Integrate around the period. The derivative integrates to zero. Taking the absolute value of the integrated identity and using |u|/R_epsilon<=1 gives

    |a| integral |u|^2/R_epsilon ds
      <= integral |omega u'+a u| ds.

Dominated convergence as epsilon decreases to zero proves (2), including zeros of u and a=0.

### Second-order statement

For r>0 define

    T_r=(omega partial_s+rho)^2-r^2.

Its commuting factorization is

    T_r=(omega partial_s+rho-r)(omega partial_s+rho+r).

Apply (2), first to v=(omega partial_s+rho+r)u with a=rho-r, and then to u with a=rho+r>0. This proves

    integral |T_r u| ds >= |rho^2-r^2| integral |u| ds.         (3)

There is no division by rho-r. At rho=r this remains the valid, possibly uninformative, inequality 0<=integral |T_r u|. The constant is sharp for nonzero constant u when rho!=r. The lemma does not assume that u has constant phase or nonzero modulus.

### Independent inverse interpretation

For a!=0 the periodic inverse of omega partial_s+a has the fixed sign sign(a):

    a>0: R_a f(s) = integral_0^infinity exp(-a t) f(s-omega t) dt;
    a<0: R_a f(s) = -integral_0^infinity exp(a t) f(s+omega t) dt.

The formulas are bounded convolutions on periodic functions or measures. Differentiation/integration by parts gives (omega partial_s+a)R_a f=f. Each kernel's total variation is 1/|a|, since its absolute mass equals the displayed exponential integral. The periodic homogeneous equation has no nonzero solution for a!=0. Hence, away from rho=r,

    T_r^(-1)=R_(rho-r) R_(rho+r)

has the constant kernel sign sign(rho-r), and its total variation is exactly 1/|rho^2-r^2|. The composition of two positive kernels, multiplied by the one overall sign, has no cancellation; its mass is the product of the two masses. This confirms (3), including the negative-factor regime rho<r. The proof of the theorem uses (2)-(3), so no inverse or resonance exclusion is needed.

## 3. Positive forcing controls mean moduli, not moduli of means

First take smooth coefficients. Write

    f_0=(omega partial_s+rho)^2 c,
    f_1=T_n A,
    f_2=T_(2n) B.

At every s, the forcing of H_0 is the nonnegative degree-two trigonometric polynomial, with x=n theta,

    p_s(x)=f_0(s)+Re[f_1(s) exp(ix)+f_2(s) exp(2ix)]>=0.

For any nonnegative polynomial p(x)=p_0+Re(u exp(ix)+v exp(2ix)),

    |u| <= sqrt(2) p_0,       |v| <= p_0.                    (4)

For the first bound, rotate x so u becomes |u|, and add p(3 pi/4)+p(5 pi/4). The two second-harmonic contributions cancel, giving 2p_0-sqrt(2)|u|>=0. For the second, choose x_0 with Re(v exp(2ix_0))=-|v|, and add p(x_0)+p(x_0+pi); the first harmonic cancels, giving 2p_0-2|v|>=0. Zero coefficients cause no difficulty. These tests occur after the forcing is smooth; no distribution is restricted to a curve.

Average (4) in s and apply (3), once with r=n and once with r=2n. Since the derivatives of periodic c average to zero,

    |rho^2-n^2| overline[|A|]
       <= overline[|f_1|] <= sqrt(2) rho^2 overline[c],

    |rho^2-4n^2| overline[|B|]
       <= overline[|f_2|] <= rho^2 overline[c].               (5)

These are estimates of mean moduli. The accepted fourth-pass cancellation example therefore does not contradict them: its complex mean can vanish while its mean modulus remains positive.

### Continuous coefficients and measure-valued forcing

Let eta_epsilon be a nonnegative smooth approximate identity on the s-circle and convolve c,A,B in s. Temporal convolution commutes with L and preserves positivity of its distributional forcing. The convolved coefficients are smooth, and the convolved forcing is a smooth function of s and theta: it remains a finite trigonometric polynomial in theta and all of its time coefficients are smooth. A smooth nonnegative distribution is pointwise nonnegative. Thus the preceding proof gives (5) for c_epsilon,A_epsilon,B_epsilon.

Periodic convolution preserves overline[c] exactly. Uniform convergence of the continuous coefficients gives convergence of their modulus integrals. Passing to the limit proves (5) for the original continuous coefficients. There is no need for |A_epsilon|<=|B_epsilon|: dominance is used only after (5) has been proved and the original coefficients have been recovered. This avoids an otherwise invalid assumption that temporal mollification preserves complex modulus dominance.

## 4. A uniform all-ratio lower bound

Set

    C=overline[c], X=overline[|A|], Y=overline[|B|],
    t=n^2/rho^2>0.

By dominance, Y>=X>=0. Dividing (5) by the positive rho^2 gives

    C >= |1-t| X/sqrt(2),
    C >= |1-4t| Y >= |1-4t| X.                              (6)

Introduce positive weights

    w_1=8/(8+sqrt(2)), w_2=sqrt(2)/(8+sqrt(2)), w_1+w_2=1.

Because |1-t|>=1-t and |1-4t|>=4t-1, the weighted sum of (6) yields

    C >= [w_1(1-t)/sqrt(2)+w_2(4t-1)] X
      = [3 sqrt(2)/(8+sqrt(2))] X
      = (Gamma/2) X.                                        (7)

This single certificate works for every t>0. At rho=n the first inequality in (6) is vacuous but the second gives C>=3X. At rho=2n the second is vacuous but the first gives C>=3X/(4sqrt(2)). Both exceed the bound in (7). No resonance has been inverted or excluded, and no temporal winding integer occurs.

For clarity, Gamma>9/10 is equivalent to sqrt(2)>24/17, which follows from 578>576. Also pi>3 and sqrt(3)<7/4 give k<7/8. Hence

    Gamma-k>9/10-7/8=1/40.                                  (8)

The exact envelope minimum is at t=(2+sqrt(2))/(8+sqrt(2)), where the two terms in (6), with Y=X, coincide. This shows only that (7) is optimal for these two relaxed envelopes, not that the theorem's constant is optimal.

## 5. Apply the accepted invariant angular median identity

For each phase with B!=0, the accepted fourth-pass identity is

    M(s)/(2 pi)=c(s)-(k/2) Re[A(s)^2/B(s)].                  (9)

If B=0, dominance forces A=0; define A^2/B=0 there. This quotient extension is continuous because

    |A^2/B|=|A|^2/|B|<=|A|<=|B|.

Replacing x by n theta traverses n full angular periods and leaves the normalized angular mean unchanged; there is no additional factor n.

Pointwise,

    Re(A^2/B)<=|A|^2/|B|<=|A|,                              (10)

with the same convention at zeros. Average (9), then use (7) and (10):

    overline[M/(2 pi)]
      = C-(k/2) overline[Re(A^2/B)]
      >= (Gamma/2)X-(k/2)X
      = ((Gamma-k)/2)X.

This proves (1). The median of three real inputs is 1-Lipschitz in their maximum norm, so M is continuous. When A is not identically zero, X>0 and the positive average forces a strictly positive phase.

If A is identically zero, the angular median of the remaining cyclic pure second harmonic has zero angular average, also directly from (9), so M=2 pi c. Angular averaging of L H_j>=0 gives (omega partial_s+rho)^2 c>=0. The positive periodic scalar inverse is

    c(s)=integral_0^infinity t exp(-rho t) f(s-omega t) dt

for smooth nonnegative forcing f; nonnegative periodic mollification and uniform convergence prove c>=0 for the continuous distributional case. Thus this degenerate case has nonnegative median at every phase.

No median is commuted with time averaging. The nonlinear identity is applied to the original coefficients one phase at a time, and only the resulting scalar equality and pointwise envelope are integrated.

## 6. What closes and what remains unresolved

The fourth-pass proof controlled |overline[A]| only after a fixed-axis sign reduction. General first-axis motion defeats that control, as the accepted admissible cancellation example demonstrates. The first-order L1 coercivity lemma instead controls overline[|A|] directly by the positive forcing budget. It does the same for B, and the incompatibility of the two modal constants supplies the uniform gap. Phase gauges, derivatives of arguments, winding numbers and nonvanishing assumptions are unnecessary.

The theorem includes arbitrary continuous complex A and B satisfying |A|<=|B|; they can have zeros and nonuniform or changing phase. It includes any rigid drift as a special case by absorbing exp(i m s) and exp(2i m s) into A and B. It is strictly stronger than the fourth-pass fixed-first-axis dominance theorem and strengthens its some-phase conclusion to a quantitative full-torus-average statement.

This closes the requested phase-coherence gap in the dominance region only. Outside |A|<=|B| the accepted invariant angular identity is false, so the present proof does not establish an unrestricted two-complex-amplitude theorem. Arbitrary independent triples, the unrestricted periodic some-phase assertion, and the original normalized-supremum conjecture remain unresolved here. No counterexample to any of those assertions is claimed.

## 7. Verification

The companion exact verifier passes 30 checks and rejects four negative controls, with byte-identical output in normal, -O and -OO modes. It checks factorization, the regularized derivative identity, positive-polynomial tests, normalized coefficients, all-ratio convex weights, both resonance substitutions, rational gap, and the distinction between a mean modulus and a modulus of a mean. It includes negative controls for the incorrect modulus-of-mean substitution and preservation of complex dominance under mollification. These checks complement the analytic proof of (2), the distributional smoothing argument, and the accepted fourth-pass angular identity; they do not replace them.

The [independent fifth-pass acceptance](../audits/complex_dominance_acceptance.md) distinguishes the signed-mass check label from the absolute total-variation proof. The [author certificate](../certificates/phase_author.json) and [independent audit certificate](../certificates/phase_audit.json) retain their separate roles.

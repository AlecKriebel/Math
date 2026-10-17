# Third shared pass: a phase-averaged dual certificate for changing two-harmonic shapes

## Result and scope

**The unrestricted periodic some-phase assertion and the original normalized-supremum conjecture remain unresolved.** This third shared substantive pass proves the some-phase assertion for an explicit genuinely shape-changing cyclic two-harmonic class. It uses positive tests averaged over the entire phase circle, rather than the fixed finite torus-point pairings excluded in the accepted second pass. No uniformly negative counterexample is produced. No historical novelty claim is made.

The source target remains A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The homogeneous and harmonic cases are credited prior cases. The exact two-harmonic median formula below follows by rescaling the sector computation in the accepted first-pass report [first-pass theory report](../baseline/two_pass/proofs/first_pass_theory.md), Section 3. The scalar positivity argument is the accepted second-pass argument in [second-pass periodic report](../baseline/two_pass/proofs/second_pass_periodic.md), Section 1. These baselines are used explicitly, rather than claimed as new results of this pass.

Let rho, omega > 0. Both s and theta have period 2 pi, and

    L = (omega partial_s + rho)^2 + partial_theta^2.

The periodic target asks whether continuous real H_0,H_1,H_2 with L H_j >= 0 in distributions necessarily have some s for which

    M(s) = integral_0^(2 pi) med_j H_j(s,theta) dtheta >= 0.

## 1. Exact affirmative theorem

### Theorem

Fix any positive integer n and any integer m (including zero). Let a,b,c be arbitrary continuous real 2 pi-periodic functions of s, and define

    H_j(s,theta) = c(s)
       + a(s) cos(n theta + m s + 2 pi j/3)
       + b(s) cos(2n theta + 2m s + 4 pi j/3),       j = 0,1,2.

If L H_j >= 0 in distributions, then M(s) >= 0 for at least one phase s.

No sign, derivative, finite temporal Fourier bandwidth, nonresonance, or small-modulation assumption is imposed on a,b,c. In particular, resonant rho is allowed and a/b may change with s. The two angular harmonics retain their displayed fixed relative axes, with an optional common rigid helical drift m s. General time-varying relative angular phases or nonuniform angular drift are not included.

There is a stronger quantitative conclusion in the nondegenerate sign case a(s)>0, b(s)>0 for all s. Define

    k = 3 sqrt(3)/(2 pi),
    kappa = 2 - sqrt(2),
    d = 3(1+sqrt(2))/8,
    delta = d - k > 1/40.

For positive a,b, put

    F(a,b) = a^2/(2b),                         0 < a <= b;
             -b + 2a - a^2/(2b),              b <= a <= 2b;
             b,                               a >= 2b.

Writing an overbar for the normalized phase average (2 pi)^(-1) integral ds, one has

    overline[M/(2 pi)] >= delta * overline[F(a,b)] > 0.       (1)

Thus a positive phase exists in this sign case. The same conclusion holds if a<0 everywhere and b>0, with |a| in F.

### Why this is beyond the previous affirmative classes

The relative amplitudes a(s)/b(s) may vary arbitrarily within the subharmonicity constraint, so these profiles need not have a common fixed angular shape times one amplitude and one rotation. Both n and 2n occur. Unless one term vanishes, they do not have a common sign-reversing angular shift. The proof works at every temporal frequency omega and integer common drift m, with no fixed-forcing or large-omega hypothesis.

## 2. The exact median formula and its two linear majorants

Let a,b>0 and consider the cyclic triple

    a cos(x+2 pi j/3) + b cos(2x+4 pi j/3).

Its normalized angular median is

    (2 pi)^(-1) integral med_j(...) dx = -k F(a,b).           (2)

One way to verify (2) directly from the accepted harmonic diagnostic is to set r=b/a and multiply its triple r cos(x+2 pi j/3)+r^2 cos(2x+4 pi j/3) by the positive factor a^2/b. Its three regimes r<=1/2, 1/2<=r<=1 and r>=1 give exactly the three displayed branches of F. Replacing x by n theta + m s at a fixed phase leaves the normalized circle integral unchanged.

Changing a to -a is the angular shift x -> x+pi and therefore leaves the integral unchanged. Negating the entire triple negates its median. Consequently, for b != 0 and arbitrary a,

    normalized median = -k sign(b) F(|a|,|b|),              (3)

where F(0,b)=0. If b=0, the normalized median is zero by the common half-period sign reversal. If a=0, the same is true for the sole second harmonic.

For positive a,b,

    0 < F(a,b) <= b,
    F(a,b) <= kappa a.                                      (4)

For completeness, set x=a/b. Then F/b equals x^2/2 on [0,1], -1+2x-x^2/2 on [1,2], and 1 on [2,infinity). The upper bound by 1 follows immediately. For the other bound:

- on [0,1], x^2/2 <= x/2 <= kappa x;
- on [1,2], kappa x - (-1+2x-x^2/2) = (x-sqrt(2))^2/2;
- on [2,infinity), 1 <= kappa x, since 2 kappa > 1.

The value kappa is the exact maximum of F(a,b)/a, attained when a/b=sqrt(2). No sampled angular quadrature enters these facts.

## 3. Positive phase-circle tests give the required lower bound

First suppose a,b>0 everywhere. Set

    A = overline[a], B = overline[b], C = overline[c],
    K = overline[F(a,b)], lambda^2 = n^2 + omega^2 m^2,
    q = rho^2/lambda^2.

Equation (4) implies

    B >= K, A >= K/kappa.                                   (5)

Set x=n theta+m s. In these coordinates the profile is c(s)+a(s)cos x+b(s)cos(2x), and the operator is

    (omega partial_s + omega m partial_x + rho)^2
        + n^2 partial_x^2.

The map (s,theta) -> (s,x) is a finite covering of tori because n,m are integers. Testing with nonnegative functions pulled back under this covering shows that the transformed forcing is a nonnegative distribution. Its phase average is therefore nonnegative. Periodicity eliminates every term containing a partial_s derivative, leaving the smooth angular polynomial

    G(x) = rho^2 C + (rho^2-lambda^2) A cos x
              + (rho^2-4 lambda^2) B cos(2x)
              - 2 rho omega m A sin x - 4 rho omega m B sin(2x)
         >= 0.

The positive symmetrization [G(x)+G(-x)]/2 removes the two sine terms. Hence

    rho^2 C + (rho^2-lambda^2) A cos x
             + (rho^2-4 lambda^2) B cos(2x) >= 0.           (6)

The averaging and symmetrization take place before evaluation at any angle, so no restriction of a general distribution to a slice is used. Divide (6) by lambda^2 for the following cases. When m=0, this reduces to ordinary full-phase averaging at fixed theta.

### Case 0 < q <= 1

Evaluate (6) at x=0:

    C >= (1/q-1) A + (4/q-1) B >= 3 B >= 3 K.               (7)

### Case 1 <= q <= 4

Evaluate (6) at x=pi:

    C >= (1-1/q) A + (4/q-1) B.

Put alpha=1-1/q, so 0<=alpha<=3/4 and 4/q-1=3-4alpha. By (5),

    C >= [alpha/kappa + 3 - 4alpha] K
      >= (3/(4 kappa)) K.                                   (8)

The last expression is the minimum over alpha in [0,3/4], because 1/kappa<4.

### Case q >= 4

Evaluate (6) at x=3 pi/4. Here cos x=-1/sqrt(2) and cos(2x)=0. Therefore

    C >= (1-1/q) A/sqrt(2)
      >= 3 A/(4 sqrt(2))
      >= [3/(4 sqrt(2) kappa)] K = d K.                      (9)

Both constants in (7),(8) exceed d, so every case gives C>=dK. Equation (2) now yields

    overline[M/(2 pi)] = C-kK >= (d-k)K,

proving (1). The strict rational lower bound delta>1/40 can be seen without decimal approximations: sqrt(2)>7/5 gives d>9/10, while pi>3 and sqrt(3)<7/4 give k<7/8. Hence d-k>9/10-7/8=1/40.

These constants are convenient rigorous bounds. No optimality claim is made for the gap d-k or for the testing angles.

## 4. Removing all sign hypotheses

The angular average of every H_j is c(s). Angular averaging of L H_j gives

    (omega partial_s+rho)^2 c >= 0

in distributions. The unique periodic inverse of this scalar operator is positive:

    c(s) = integral_0^infinity t exp(-rho t) f(s-omega t) dt

for smooth right-hand side f, with positivity for distributional data obtained by nonnegative periodic mollification and uniform convergence. Thus c(s)>=0 at every s.

If b(s)<=0 at any phase, (3), including its zero case, gives M(s)/(2 pi)>=c(s)>=0. If a(s)=0 at any phase, the single-harmonic formula gives M(s)/(2 pi)=c(s)>=0.

The only remaining case has b>0 everywhere and a nowhere zero. Continuity on the connected phase circle forces a to have a constant sign. If that sign is negative, the fixed angular translation theta -> theta+pi/n changes a to -a while leaving b unchanged, preserving L-subharmonicity and M. We are then in the positive-amplitude case of Section 3, which actually gives a positive phase. This proves the theorem for all continuous real a,b,c.

No smoothness approximation is needed in the phase-averaged step: a,b,c have well-defined averages, the two temporal derivative terms average to zero distributionally, and (6) is a smooth function. The scalar positivity argument is the same mollification-valid argument already audited in the second pass.

## 5. Duality interpretation and precise remaining obstruction

The geometric test supports are full phase circles (or paired full helical covers for m != 0), but the actual distributional pairings use nonnegative smooth angular tests pulled back under (s,theta) -> (s,n theta+m s). Full-phase averaging first produces the smooth polynomial G; only then is G evaluated at the selected angle. Equivalently, take the limit of smooth nonnegative approximate identities concentrated about that angle after averaging. For n>1, the full inverse-image cover, with its normalized multiplicity, is included. No direct pairing of a measure-valued forcing with a singular measure is asserted. These tests are not finite positive sums of torus point evaluations, so the [accepted Green-function obstruction](../baseline/two_pass/proofs/second_pass_periodic.md) does not apply.

In this class, the exact median deficit has two global linear majorants, F<=b and F<=kappa a. Once strict negativity would force both amplitudes into one positive cone, a phase-averaged forcing test provides a linear lower bound on C that exceeds that deficit. This is the essential feature of the argument. Averaging the profiles and commuting the median with that averaging would be invalid and is not used.

For arbitrary changing angular shapes, this proof supplies neither the sign-cone reduction nor linear majorants controlled by common positive forcing tests. It also does not cover general nonuniform common rotations, arbitrary relative phase rotations of the two harmonics, or arbitrary independent functions instead of the displayed cyclic triple. The stronger claim that every admissible triple has nonnegative full-torus average median has not been proved or refuted here. The theorem proves the required some-phase conclusion only for its stated subclass.

The general periodic some-phase assertion, escaping-frequency flat frontiers, and the full normalized-supremum conjecture therefore remain open in this shared pass.

## 6. Verification artifacts

The [author exact certificate](../certificates/cyclic_author.json) checks the symbolic rescaling of all three median branches, the sharp kappa envelope, the constant identities, the helical averaged operator and positive symmetrization, all three test evaluations, and the endpoint minimization. The [independent cyclic audit](../audits/cyclic_acceptance.md), with its [exact certificate](../certificates/cyclic_audit.json), reconstructs the sector integrals directly, the full operator before averaging, all sign and resonance cases, and targeted invalid controls. The analytic arguments above and in that audit are required for distributional positivity, continuity, and passage from average positivity to a phase.

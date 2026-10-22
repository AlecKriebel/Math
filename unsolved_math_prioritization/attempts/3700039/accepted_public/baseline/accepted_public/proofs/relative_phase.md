# Fourth shared pass contribution: arbitrary relative phase under second-harmonic dominance

## Scope and result

The unrestricted periodic some-phase assertion and the original normalized-supremum conjecture remain unresolved. This contribution proves a nonperturbative relative-phase extension of the accepted third-pass theorem. No historical novelty is claimed.

The target and credited prior cases are those of A. Eremenko, *Conjectured inequality for subharmonic functions* (4 April 2015), https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The [accepted third-pass report](../baseline/corrected_public/proofs/cyclic_two_harmonic.md) and [corrected audit](../baseline/corrected_public/audits/cyclic_acceptance.md) establish the fixed-relative-axis theorem and the distributionally legitimate phase-circle/helical averaging procedure. The new angular identity below is derived directly, including complex coefficients, rather than inferred by commuting a median with phase averaging.

### Theorem

Let rho, omega > 0, n >= 1 an integer, and m any integer. Let a,b,d,c be continuous real 2 pi-periodic functions satisfying

    a(s)^2 <= b(s)^2+d(s)^2                         for every s.

Set x_j=n theta+m s+2 pi j/3 and

    H_j(s,theta)=c(s)+a(s) cos(x_j)
                         +b(s) cos(2x_j)+d(s) sin(2x_j), j=0,1,2.

If L H_j >= 0 in distributions, where

    L=(omega partial_s+rho)^2+partial_theta^2,

then the angular median integral M(s) is nonnegative for at least one phase s.

There is no sign, temporal bandwidth, differentiability, or small-modulation restriction. In particular, the second harmonic may have any continuous time-varying complex coefficient. Its relative phase need not be constant, close to zero, or a rigid drift. The restriction is that its modulus dominates that of the first harmonic. The first harmonic's axis remains fixed in the displayed rigid helical frame.

At every phase, with R^2=b^2+d^2, the exact normalized median is

    M(s)/(2 pi)=c(s)-k a(s)^2 b(s)/(2 R(s)^2),
    k=3 sqrt(3)/(2 pi),                              (1)

where the fraction is defined as zero if R=0 (then a=0). At fixed s, the theta integral traverses n complete periods of x, so its normalized value equals the normalized x integral; there is no additional factor n.

If a is nowhere zero and b>0 everywhere, define

    K(s)=a(s)^2 b(s)/(2 R(s)^2),
    Gamma=6 sqrt(2)/(8+sqrt(2)).

Then the stronger quantitative bound is

    average_s M(s)/(2 pi) >= (Gamma-k) average_s K(s) > 0,   (2)

and Gamma-k>1/40. This gives a strictly positive phase in this sign cone.

## 1. An invariant exact complex-coefficient identity

For arbitrary complex A,B with |A|<=|B| and B!=0, let

    q_j(x)=Re(A exp(i(x+2 pi j/3))+B exp(2i(x+2 pi j/3))).

Then

    average_x med_j q_j(x)
       =-k Re(A^2 conjugate(B))/(2 |B|^2)
       =-(k/2) Re(A^2/B).                            (3)

For B=0 the dominance hypothesis gives A=0, and the median is zero. Formula (3) is rotationally invariant: replacing A,B by A exp(i alpha), B exp(2i alpha) leaves the expression unchanged. In particular,

    |average_x med q_j| <= k |A|^2/(2|B|) <= k |A|/2.       (4)

The exact signed projection in (3), rather than only the modulus estimate (4), is what supplies the sign reduction and phase-averaged coefficient control below.

### Direct root-and-primitive proof

An angular translation makes A=a>=0. Write the resulting second coefficient as b-i d, and R=sqrt(b^2+d^2). First assume a<R. Let

    f_j(x)=a cos(x+2 pi j/3)+b cos(2x+4 pi j/3)
                                 +d sin(2x+4 pi j/3).

Their sum is zero. For the pair j=0,1 set t=x+pi/3. Then

    f_0-f_1=sqrt(3) g(t),
    g(t)=a sin t+b sin(2t)-d cos(2t).

Put

    u(t)=b sin(2t)-d cos(2t),
    v(t)=b cos(2t)+d sin(2t),

so u^2+v^2=R^2. At a root of g the common value of f_0,f_1 is

    V(t)=(a cos t-v(t))/2,

and

    g'(t)=a cos t+2v(t).

There are precisely four simple roots modulo 2 pi. Indeed, at a=0 this is immediate. A double root would satisfy a sin t=-u and a cos t=-2v, giving

    a^2=u^2+4v^2>=R^2,

which is impossible throughout the homotopy from 0 to a<R. No roots can appear, disappear, or collide on the compact circle. Also a simultaneous equality V=0 would give a sin t=-u and a cos t=v, hence a^2=R^2. Thus no triple tie occurs. At a=0 one has V g'=-v^2<0 at every root; continuity of the roots consequently gives

    sign(V) sign(g')=-1                              (5)

at all four roots for a<R.

Choose the periodic primitive

    F_j(x)=a sin(x+2 pi j/3)+(b/2) sin(2x+4 pi j/3)
                                  -(d/2) cos(2x+4 pi j/3).

For this pair its primitive difference is

    h(t)=F_0-F_1
        =-sqrt(3)[a cos t+v(t)/2].

At a simple crossing with V>0, the third value is -2V<V and the median is the smaller member of the crossing pair. The contribution of that boundary to the piecewise primitive integral is sign(g') h. At V<0 the third value is larger and the median is the larger member, reversing that contribution. Therefore every crossing contributes sign(V)sign(g')h. The three unordered pair families give equal sums by cyclic translation. By (5),

    integral_0^(2 pi) med_j f_j(x) dx = -3 sum_{g(t)=0} h(t).  (6)

This formula counts each switch once: a simple pair crossing with no triple tie changes the median, and the pair families are disjoint. Periodic primitives cancel all remaining interval boundaries.

Let beta=b-i d and z=exp(i t). The root equation is

    beta z^4+a z^3-a z-conjugate(beta)=0.

All its four roots are the four simple unit-circle roots just identified. Newton's identities give

    S_1=sum z=-a/beta,
    S_2=sum z^2=a^2/beta^2.

Consequently

    sum h=-sqrt(3)[a Re(S_1)+(1/2)Re(beta S_2)]
         =sqrt(3) a^2 b/(2R^2).

Substitution into (6), followed by division by 2 pi, proves (1)'s oscillating term when a<R. The boundary a=R follows by taking a increasing to R: the median is 1-Lipschitz in its three inputs, so its angular integral is continuous, including crossing collisions and triple ties. Negative a is handled by x -> x+pi, which leaves the second harmonic unchanged. Finally undo the rotation of A: a^2 b=Re(A^2 conjugate(B)), proving (3).

This argument is algebraic and continuous; it uses no sampled quadrature, optimization, or conjectured relative-phase extremality.

## 2. The scalar mean and sign reduction

Angular averaging of L H_j >= 0 yields

    (omega partial_s+rho)^2 c >= 0

in distributions. The positive periodic scalar inverse from the accepted second and third passes gives c(s)>=0 everywhere. Briefly, for smooth forcing f its inverse is

    c(s)=integral_0^infinity t exp(-rho t) f(s-omega t) dt.

The homogeneous equation has no nonzero periodic solution; nonnegative periodic mollification and uniform convergence prove the continuous distributional case.

If a vanishes at any phase, (1) gives M/(2 pi)=c>=0 there. If b<=0 at any phase, (1) also gives M/(2 pi)>=c>=0. The only case that could have negative medians at every phase has a nowhere zero and b>0 everywhere. Continuity makes the sign of a constant. A single fixed shift theta -> theta+pi/n makes a positive if necessary, preserving the second harmonic and L.

In this remaining case K is continuous and strictly positive. Since a<=R and 0<b<=R,

    K<=b/2,                 K<=a/2.                 (7)

For A_0=average_s a, B_0=average_s b and K_0=average_s K, this gives

    A_0>=2K_0,              B_0>=2K_0.               (8)

No averaging of nonlinear medians has been asserted here: (7) is integrated before being used.

## 3. Positive degree-two forcing tests

Use the helical coordinate x=n theta+m s. Write

    h(s,x)=c(s)+a(s)cos x+b(s)cos(2x)+d(s)sin(2x),
    lambda^2=n^2+omega^2 m^2.

The n-sheeted torus covering pulls nonnegative smooth tests back to admissible nonnegative tests. Thus

    Qh >= 0,
    Q=(omega partial_s+omega m partial_x+rho)^2+n^2 partial_x^2

distributionally, exactly as in the accepted third-pass averaging argument. Average over the full s-circle. Every partial_s derivative vanishes. With C_0=average c and D_0=average d, the result is the smooth nonnegative polynomial

    G(x)=rho^2 C_0+Re(U exp(i x)+V exp(2i x)) >= 0,

where

    U=(rho^2-lambda^2+2i rho omega m) A_0,
    V=(rho^2-4lambda^2+4i rho omega m)(B_0-i D_0).          (9)

The drift-imaginary terms in (9) must be retained. Unlike the fixed-axis third-pass proof, no reflection is used to discard them or the imaginary second coefficient.

### Elementary coefficient bounds

For any nonnegative degree-two trigonometric polynomial

    p(x)=p_0+Re(u exp(i x)+v exp(2i x)),

one has

    p_0>=|u|/sqrt(2),          p_0>=|v|.              (10)

For the first inequality, rotate x so the first term is |u|cos x, then add the evaluations at x=3 pi/4 and x=5 pi/4. The second-harmonic contributions cancel exactly, giving 2p_0-sqrt(2)|u|>=0. For the second inequality choose x_0 with Re(v exp(2i x_0))=-|v| and add evaluations at x_0 and x_0+pi; the first-harmonic terms cancel, giving 2p_0-2|v|>=0. Zero coefficients cause no problem.

These are positive tests of the already-smooth full-phase average. They are not a restriction of a distribution to a curve or a universal finite torus-point pairing of profiles.

Apply (10) to (9), and put q=rho^2/lambda^2>0. Since A_0,B_0>0,

    C_0 >= |q-1| A_0/(sqrt(2) q)
        >= sqrt(2) |1-1/q| K_0,

    C_0 >= |q-4| B_0/q
        >= 2 |1-4/q| K_0.                           (11)

Here |B_0-i D_0|>=B_0, and the drift terms only increase the two coefficient moduli compared with the real-part lower bounds used in (11). Both substitutions from (8) have nonnegative coefficients.

## 4. A uniform gap without resonance exclusions

Set t=1/q. Each absolute value in (11) bounds its displayed signed linear expression. Form the convex combination with weights

    w_1=8/(8+sqrt(2)),       w_2=sqrt(2)/(8+sqrt(2)).

Their weighted sum is independent of t:

    w_1 sqrt(2)(1-t)+w_2 2(4t-1)
          =6 sqrt(2)/(8+sqrt(2))=Gamma.

Thus (11) implies C_0>=Gamma K_0 for every q>0, including q=1 and q=4. Integrating (1) now proves (2).

For an exact convenient gap, Gamma>9/10 is equivalent to sqrt(2)>24/17, which follows from 578>576. Also pi>3 and sqrt(3)<7/4 imply k<7/8. Therefore

    Gamma-k > 9/10-7/8 = 1/40.

K_0>0 in the remaining sign cone, so the average median is strictly positive. Continuity of the median integral gives a positive phase. Together with the zero and opposite-sign cases of Section 2, this proves the theorem.

No inversion of the full two-variable operator is used, so integer rho and angular resonances are included. The argument works directly for continuous coefficients because the only temporal derivatives used are distributionally averaged over a full period.

## 5. Genuine extension and exact remaining limitations

The second coefficient b(s)-i d(s) is arbitrary subject only to modulus dominance. Its relative phase can vary nonuniformly or wind around the full circle. For example,

    rho=omega=n=1, m=0,
    H_j=5+(1/2)cos(theta+2 pi j/3)
             +cos(2theta+4 pi j/3-s)

has |a|=1/2, |B|=1 and a genuinely changing relative phase. Its forcing is

    5-4cos(2theta+4 pi j/3-s)+2sin(2theta+4 pi j/3-s)
       >=5-2sqrt(5)>0.

This example just illustrates membership and admissibility; it is not used to prove the theorem. More general continuous amplitude changes and arbitrary drift m are covered by the theorem.

The invariant identity (3) does apply slice-by-slice to two arbitrary complex coefficients A(s), B(s) whenever |A(s)|<=|B(s)|. The some-phase proof presently requires the first coefficient to have the displayed common rigid axis. With a general changing first axis, averaging can cancel that coefficient, and (8) no longer supplies its required positive linear average. Strict negativity restricts Re(A^2/B), but it does not by itself make A lie in a fixed half-plane. No solution to that remaining phase-coherence issue is asserted.

Likewise, outside |A|<=|B| the four-unit-root identity used here no longer has the stated form. No global assertion that arbitrary relative phase is dominated by its aligned-axis counterpart is needed or claimed. The unrestricted two-complex-amplitude problem, general periodic triples, and the original normalized-supremum conjecture remain open here.

## 6. Verification

The [exact author certificate](../certificates/relative_author.json) verifies the pair differences, common-value identity on crossings, primitive differences, root polynomial and Newton sums, collision exclusions, invariant formula, two linear envelopes, helical averaged coefficients, positive test cancellations, convex-weight identity, exact gap inequalities, and the illustrative example's forcing. Its checks use explicit exceptions and run unchanged under Python optimization flags. The analytic root-continuation, distributional averaging and scalar inverse arguments above are part of the proof; symbolic checks are not substitutes for them.

The full [independent audit](../audits/relative_phase_acceptance.md) and its [exact certificate](../certificates/relative_audit.json) separately test the proof and its limits.

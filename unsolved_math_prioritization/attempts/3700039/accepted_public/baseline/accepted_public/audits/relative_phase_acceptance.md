# Independent acceptance: arbitrary relative phase under second-harmonic dominance

## Decision and exact scope

**Accepted. No theorem-level or proof correction is required.** The exact complex-amplitude cyclic median identity is valid for every pair |A|<=|B|, including all zero and boundary degeneracies. The stated some-phase theorem is valid for every continuous real periodic a,b,d,c satisfying a²<=b²+d², every integer n>=1 and m, and all rho,omega>0. It permits an arbitrary time-varying second-harmonic axis while the first-harmonic axis is fixed in the specified rigid helical frame.

In the positive sign cone, the quantitative conclusion is also accepted:

    average_s[M(s)/(2 pi)] >= (Gamma-k) average_s K(s) > 0,
    K=a²b/[2(b²+d²)],
    Gamma=6 sqrt(2)/(8+sqrt(2)), k=3 sqrt(3)/(2 pi),
    Gamma-k>1/40.

The numerical value Gamma-k approximately 0.0743332858 is only descriptive. The proof of the displayed strict rational bound is exact.

This is an adversarial audit of the fourth shared contribution, not a fifth research pass. It does not establish the unrestricted two-complex-amplitude some-phase assertion, the general periodic-triple assertion, or the original normalized-supremum conjecture. It makes no historical novelty claim.

The [full relative-phase proof](../proofs/relative_phase.md) preserves every audited mathematical claim. Its [exact author certificate](../certificates/relative_author.json), the [independent certificate](../certificates/relative_audit.json), and the [corrected third-pass audit](../baseline/corrected_public/audits/cyclic_acceptance.md) have distinct roles.

Source credit remains A. Eremenko, *Conjectured inequality for subharmonic functions*, 4 April 2015, [author-hosted source](https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf). Its title, date and formulation were checked against the public PDF. No third-party source text is copied into this package.

## 1. Independent angular normalization and sign conventions

Put zeta=exp(2 pi i/3), and consider

    q_j(x)=Re(A zeta^j exp(ix)+B zeta^(2j) exp(2ix)).

The three values sum to zero because 1+zeta+zeta²=0. Their median has period 2 pi/3 by cyclic permutation. Adding a common c adds c to the median, and a common angular translation leaves its integral unchanged.

For A!=0, translating x by minus arg(A) makes the first coefficient a=|A| positive and the second coefficient beta=B exp(-2i arg(A)). Write beta=b-i d, so its real contribution is b cos(2x)+d sin(2x). This minus sign in beta is essential. If A=0, no rotation is needed. Then

    a² Re(beta)=Re(A² conjugate(B)), |beta|=|B|.

At a fixed s, the substitution x=n theta+m s traverses n full angular periods as theta runs through 0 to 2 pi. Its Jacobian 1/n cancels those n periods. Consequently the normalized angular mean is unchanged; no extra factor n occurs.

## 2. Strict-dominance roots: all crossings and their orientation

Assume 0<=a<R, R=|beta|>0. For the pair (0,1), write t=x+pi/3 and

    g(t)=a sin t+b sin(2t)-d cos(2t),
    u(t)=b sin(2t)-d cos(2t),
    v(t)=b cos(2t)+d sin(2t).

Direct trigonometric subtraction gives f_0-f_1=sqrt(3) g. At a root of g the common value and transverse derivative are

    V=(a cos t-v)/2,       g'=a cos t+2v,
    u²+v²=R².

At a=0 the second-harmonic sinusoid g has exactly four simple zeros modulo 2 pi. A multiple zero at a parameter value would satisfy

    a sin t=-u, a cos t=-2v,
    a²=u²+4v²=R²+3v²>=R².

This is impossible throughout the closed homotopy interval 0<=a'<=a<R. The implicit-function theorem continues each root; compactness of the circle and absence of collisions prevent births, deaths or escape. Thus there are exactly four simple roots for every strict-dominance ratio. The associated quartic provides a separate upper bound of four, so no unaccounted root family is possible.

A triple tie would require V=0 as well as g=0, giving

    a sin t=-u, a cos t=v, hence a²=R².

Thus every strict-dominance pair crossing is separate from every other unordered pair crossing. Each family contributes four events, for exactly twelve distinct pair events around the circle. At each event the tied values lie both above or both below the third value -2V, so the median necessarily switches between the crossing pair.

The switching sign can be checked without a diagram. The integral over adjacent intervals contributes the primitive of the incoming branch minus that of the outgoing branch. Let h=F_0-F_1. If V>0, the third value is lower and the median chooses the smaller crossing value. For g'>0 the switch is 0 to 1 and contributes h; for g'<0 it contributes -h. If V<0 the median chooses the larger value and the signs reverse. The contribution is therefore sign(V) sign(g') h.

At a=0, V=-v/2 and g'=2v, so Vg'=-v²<0. Along every continued root, neither V nor g' vanishes in the strict-dominance region. Hence their product stays negative and each boundary contributes -h. This argument also covers a=0 itself. It does not assume b>0 or constrain d.

The three unordered pair families are cyclic translates with the same oriented sum. Reversing the orientation of a pair changes both g and h and leaves its contribution unchanged. Periodic primitives cancel the artificial initial/final cut and all non-switching interval boundaries. Consequently

    integral med_j f_j(x) dx = -3 sum_{g(t)=0} h(t).

The factor three counts unordered pair families exactly once; it does not double count ordered pairs.

## 3. Quartic, Newton sums and all boundary degeneracies

The actual periodic primitives are

    F_j=a sin(x+2 pi j/3)+(b/2) sin(2x+4 pi j/3)
                          -(d/2) cos(2x+4 pi j/3).

Their difference at the chosen pair is h=-sqrt(3)[a cos t+v/2]. With z=exp(it), multiplication of g=0 by 2iz² gives exactly

    beta z⁴+a z³-a z-conjugate(beta)=0.

The four roots just counted are all the roots of this degree-four polynomial and all lie on the unit circle. Newton's identities for its monic coefficients yield

    S_1=sum z=-a/beta,   S_2=sum z²=a²/beta².

It follows that

    sum h=-sqrt(3)[a Re(S_1)+(1/2)Re(beta S_2)]
         =sqrt(3) a²b/(2R²).

The normalized median is therefore -3 sqrt(3) a²b/(4 pi R²). Undoing the angular rotation proves the claimed invariant identity

    average_x med q_j(x) = -3 sqrt(3)/(4 pi) Re(A²/B)

for |A|<|B|. Both the conjugation implicit in 1/B and the factor 1/2 relative to k are correct.

The report correctly takes a continuous limit at |A|=|B| rather than reusing the simple-switch formula at triple ties. The boundary can be classified explicitly. For a=R>0 put kappa=a/beta, so |kappa|=1. The quartic divided by beta factors as

    z⁴+kappa z³-kappa z-kappa²=(z+kappa)(z³-kappa).

The three roots z³=kappa are precisely the triple ties for this pair. The fourth root z=-kappa coincides with one of them exactly when kappa²=-1, equivalently b=0. For b!=0 all four roots are simple, but three are triple ties among the original profiles; the strict-region switch-count argument must not be applied there. For b=0 there is one double root and two other simple roots. No higher collision occurs because z³-kappa has three simple nonzero roots. This exhausts the boundary degeneracies.

For fixed B and A approaching any such boundary, the three profiles converge uniformly. The median map is 1-Lipschitz in the maximum norm, so its angular integral converges. The rational expression on the right also converges when B!=0. Thus all boundary cases, including the double-root case, are covered without making a false assertion about their switch orientations.

If B=0, dominance forces A=0 and all three oscillating profiles vanish. Moreover

    |Re(A²/B)| <= |A|²/|B| <= |B|

throughout the nonzero domain, proving joint continuity at (A,B)=(0,0) with value zero. A pure second harmonic has zero median mean, also seen directly by the common sign reversal x->x+pi/2. A negative real first coefficient is absorbed by x->x+pi, leaving the second coefficient unchanged.

## 4. Scalar positivity, zeros, signs and linear envelopes

Angular averaging of L H_j>=0 gives (omega partial_s+rho)² c>=0 distributionally. The correct positive scalar inverse has shift s-omega t:

    c(s)=integral_0^infinity t exp(-rho t) f(s-omega t) dt.

For smooth periodic f this follows by composing the positive first-order resolvent twice. The homogeneous solutions exp(-rho s/omega)(C_1+C_2 s) contain no nonzero periodic member. For a continuous c and nonnegative distributional forcing, convolve with a nonnegative smooth periodic approximate identity. Each mollified forcing is nonnegative, the smooth inverse gives c_epsilon>=0, and uniform convergence yields c>=0 at every phase. No distribution is evaluated at an individual phase.

The exact formula is

    M/(2 pi)=c-k a²b/[2(b²+d²)].

At R=0 the fraction is continuously defined as zero. If a vanishes anywhere, its median mean equals c>=0 there. If b<=0 anywhere, the oscillating contribution is nonnegative there. These cases include b=0 with nonzero d and all possible zeros of R.

Only a nowhere zero and b>0 everywhere can remain if all phases were negative. Continuity forces a to have constant sign; one fixed translation theta->theta+pi/n makes it positive if necessary. A phase-dependent rotation has not been introduced. Now K=a²b/(2R²)>0 continuously, and

    b/2-K=b(R²-a²)/(2R²)>=0,
    a/2-K=a(R²-ab)/(2R²)>=0,
    R²-ab=R(R-a)+a(R-b)>=0.

Thus A_0=average a>=2K_0 and B_0=average b>=2K_0, with K_0=average K>0. Both envelope constants are sharp separately: a=b=R>0,d=0 gives equality in both. Their inequalities are integrated before any forcing estimate is made. This is not Jensen's inequality or an exchange of median and phase averaging.

## 5. Full helical operator and legitimate distributional tests

Let T(s,theta)=(s,n theta+m s). For integer n>=1 and m this is an n-sheeted torus covering. It preserves normalized integration because the number of sheets compensates its angular Jacobian. For every smooth nonnegative phi(s,x), phi composed with T is an admissible nonnegative test. The formal-adjoint chain rule gives

    L* (phi composed with T)=(Q* phi) composed with T,
    Q=(omega partial_s+omega m partial_x+rho)²+n² partial_x².

Since H_0=h composed with T, the distributional pairings imply Qh>=0. No single-valued inverse theta=(x-ms)/n is assumed. This argument needs only continuity of h.

To expose every drift and coefficient-mixing term, put lambda²=n²+omega²m². The full expansion is

    Qh=(omega²c''+2rho omega c'+rho²c)
      +[omega²a''+2rho omega a'+(rho²-lambda²)a] cos x
      -[2omega²m a'+2rho omega m a] sin x
      +[omega²b''+2rho omega b'+(rho²-4lambda²)b
                       +4omega²m d'+4rho omega m d] cos(2x)
      +[omega²d''+2rho omega d'+(rho²-4lambda²)d
                       -4omega²m b'-4rho omega m b] sin(2x).

The independent verifier checks this expression and the original-coordinate chain rule. In particular, changing m's sign changes the mixed and linear-drift terms, while m² stays unchanged.

Test Qh against functions phi(x) independent of s. All partial_s derivatives integrate to zero around the periodic circle. The result is the smooth nonnegative trigonometric polynomial

    G=rho² C_0+Re(U exp(ix)+V exp(2ix)),
    U=(rho²-lambda²+2i rho omega m)A_0,
    V=(rho²-4lambda²+4i rho omega m)(B_0-iD_0).

The second real coefficient is (rho²-4lambda²)B_0+4rho omega m D_0, and its sine coefficient is (rho²-4lambda²)D_0-4rho omega m B_0. Omitting or reflecting away these terms before the modulus argument would change the proof. The report retains them correctly.

Positivity of G follows first as a distribution and then pointwise because it is a smooth polynomial. Point evaluation is only used at that later stage, or equivalently as a limit of nonnegative smooth angular tests. There is no restriction of a general distribution to a curve and no pairing of two singular measures. This remains distinct from the earlier excluded universal finite-point pairing of profiles.

A concrete regularity test is available. Take rho=omega=n=1,m=0 and

    c=10+(1/10)|sin s|, a=1/2, b=1, d=(1/10)|sin s|.

These coefficients are continuous and some are not C1. Writing y=|sin s| and v=sign(sin s)cos s, the regular forcing is

    10+(1/5)v-3cos(2x)+[-(2/5)y+(1/5)v]sin(2x),

bounded below by 31/5. At s=0,pi the measure part is

    (1/5)[1+sin(2x)] sum delta_s,

which is nonnegative since 1+sin(2x)=(sin x+cos x)². All cyclic translates are admissible. This example confirms that the stated scope genuinely includes measure-valued temporal second derivatives; the proof does not silently require smooth coefficients.

## 6. Positive coefficient tests, sharpness, all ratios and resonances

For a nonnegative p(x)=p_0+Re(u exp(ix)+v exp(2ix)), rotate x to make the first coefficient |u| real. The sum of its values at 3pi/4 and 5pi/4 equals 2p_0-sqrt(2)|u|: both second-harmonic parts cancel, including an imaginary coefficient. Thus p_0>=|u|/sqrt(2).

Choose x_0 with Re(v exp(2ix_0))=-|v|. Adding the antipodal values x_0 and x_0+pi cancels the first harmonic and gives p_0>=|v|. These tests are valid also when a coefficient is zero. The constants are sharp:

    (cos x+1/sqrt(2))²=1+sqrt(2)cos x+(1/2)cos(2x),
    2cos²x=1+cos(2x).

Their separate sharpness does not imply simultaneous attainment for the data of this theorem or optimality of the final theorem constant.

Apply the tests to G and set q=rho²/lambda²>0. The exact squared moduli are

    |U|²=A_0²[(rho²-lambda²)²+4rho²omega²m²],
    |V|²=(B_0²+D_0²)[(rho²-4lambda²)²+16rho²omega²m²].

Dropping nonnegative terms gives the stated lower bounds, including negative m:

    C_0/K_0 >= sqrt(2)|1-1/q|,
    C_0/K_0 >= 2|1-4/q|.

Here A_0,B_0>=2K_0 were substituted only with nonnegative coefficients. The use |B_0-iD_0|>=B_0 is valid because B_0>0. There is no lower bound on a complex mean substituted for a mean modulus.

Set t=1/q. The positive weights 8/(8+sqrt(2)) and sqrt(2)/(8+sqrt(2)) sum to one. The absolute values dominate the signed lines sqrt(2)(1-t) and 2(4t-1), whose weighted sum is the constant Gamma. This proves C_0>=Gamma K_0 for all t>0 in one certificate, without a missing interval.

As an additional ratio check, the two absolute-value envelopes attain their common minimum at

    t_*=(2+sqrt(2))/(8+sqrt(2)),
    q_*=(8+sqrt(2))/(2+sqrt(2)).

At this point both equal Gamma. Thus Gamma is the best bound obtained from these two relaxed scalar envelopes; no optimality for the full theorem is asserted. At q=1 the second bound gives C_0>=6K_0. At q=4 the first gives C_0>=3sqrt(2)K_0/4. Both exceed Gamma K_0, so neither resonance endpoint is a gap. As q approaches zero or infinity the same signed-line certificate remains valid. The proof divides only by rho²,lambda²,q and positive K_0, never by q-1 or q-4.

The rational gap is correct: sqrt(2)>24/17 follows from 578>576 and is equivalent to Gamma>9/10. From pi>3 and sqrt(3)<7/4 one has k<7/8. Therefore Gamma-k>9/10-7/8=1/40. Only the scalar mean operator is inverted, so integer rho and angular resonances cause no full-operator inverse obstruction.

Finally the exact slice identity yields average_s[M/(2pi)]=C_0-kK_0. The strict bound and K_0>0 force a strictly positive phase. Continuity of the median integral follows again from its Lipschitz dependence on the continuous profiles. Together with the zero and opposite-sign cases, this proves the stated nonnegative some-phase conclusion.

## 7. Adversarial scope and nonlinear-averaging controls

### Dominance is necessary for this exact identity

For A=2,B=1, the cyclic median on the sector 0<=x<=pi/3 is the branch 2cos(x-2pi/3)+cos(2x-4pi/3). Its sixfold sector integral gives normalized mean -k. The dominance formula would give -2k, so it cannot be extended to |A|>|B|. This is verified by exact integration and by independent branch selection.

### No commuting of median and temporal averaging

Two admissible examples within the present dominance class give opposite changes between K_0 and the same nonlinear expression evaluated at averaged coefficients. In both, rho=omega=n=1,m=0,c=10.

1. With a=1/2+(1/4)cos s,b=1,d=0, one has K_0=9/64 while K(A_0,B_0,D_0)=1/8. Their difference is 1/64. The forcing is at least 10-3-3/4>0.
2. With a=1/2,b=1,d=cos s, one has K(s)=1/[8(1+cos²s)]<=1/8, strictly on a set of positive measure, whereas K(A_0,B_0,D_0)=1/8. The forcing is at least 10-3-6>0. Thus K_0<1/8.

These reject both proposed general Jensen directions and exact interchange even inside the current theorem class. The accepted proof uses only pointwise linear envelopes followed by linear averages.

### A general changing first axis remains outside the some-phase proof

The invariant slice identity alone does not supply the required positive linear average of a first coefficient. A particularly explicit admissible cancellation example is

    phi(s)=s+(1/4)sin(2s),
    A(s)=exp(i phi(s)), B(s)=A(s)²,
    rho=omega=n=1, m=0, c=27.

Here |A|=|B|=1 and Re(A²/B)=1, so K=1/2 at every phase. Yet A(s+pi)=-A(s), hence average A=0. The first axis is genuinely nonrigid: phi'=1+(1/2)cos(2s) is not constant, and no integer rigid drift can make the nonvanishing first coefficient real at all phases. The first forcing coefficient has modulus at most 25/4 and the second at most 20, so the full forcing is at least 27-25/4-20=3/4>0. Thus admissibility itself does not prevent this cancellation.

This is a counterexample to the missing envelope |average A|>=2average K, not a counterexample to an unrestricted some-phase theorem. Its median is positive because c is large. The fourth-pass report correctly excludes any claimed resolution of this phase-coherence problem.

### Strict positivity is limited to the stated cone

For rho=2,n=1,m=0,a=c=d=0,b=1, every cyclic profile is harmonic for L and its forcing is zero. The pure second-harmonic median mean is zero at every phase. This defeats any unconditional strengthening of the theorem to a strictly positive phase. The accepted statement only makes that strengthening when a is nowhere zero and b>0.

## 8. Reproducibility and preservation

The author finite calculations were independently rerun in normal, -O and -OO modes. All 34 checks and four negative controls passed; all three generated results equal the [supplied certificate](../certificates/relative_author.json) byte for byte.

The independent verifier reconstructs the full median crossing algebra, boundary factorization, Newton sums, complex projection, both sharp coefficient tests, full helical differential operator and covering chain rule, both amplitude-mixing signs, scalar inverse direction, all-ratio constant, resonance endpoints and exact rational gap. It also certifies the adversarial examples above. Explicit exceptions enforce all checks under Python optimization.

The separate numerical diagnostics reconstruct roots of the actual pair differences, sort the resulting angular intervals, choose the actual median branch at each midpoint, and integrate its elementary primitive. They do not use the report's orientation sign or its final Newton-sum median formula. The diagnostic suite has 355 complex-amplitude cases, including zero amplitude, both dominance endpoints, near-boundary ratios, arbitrary phases, and varied scales; 30 additional root/orientation cases; and five intentionally false formula variants rejected by the branch oracle. These diagnostics are corroboration only. The analytic continuation and distributional arguments above are necessary parts of the acceptance.

The independent verifier runs byte-identically in normal, -O and -OO modes. The [independent certificate](../certificates/relative_audit.json) records the final check counts and numerical maximum residual. The full mathematical text and exact certificates are bound by the reader manifest.

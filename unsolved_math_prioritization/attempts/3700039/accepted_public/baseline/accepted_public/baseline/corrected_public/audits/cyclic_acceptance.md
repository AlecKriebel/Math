# Independent acceptance: cyclic two-harmonic phase duality

## Decision and exact scope

**Accepted. No theorem-level correction is required.** The displayed cyclic two-harmonic theorem is valid for arbitrary continuous real periodic amplitudes, every positive integer angular frequency n, every integer rigid helical drift m, and all rho, omega > 0. The claimed positive-cone quantitative bound is also valid:

    average_s[M(s)/(2 pi)] >= (d-k) average_s F(|a|,b),
    d = 3(1+sqrt(2))/8,  k = 3 sqrt(3)/(2 pi),
    d-k > 1/40,

whenever b>0 and a is nowhere zero. In that case the right side is strictly positive. The zero and other sign cases yield the stated existence of a nonnegative phase, without an unjustified strict-positivity conclusion.

This is an adversarial reconstruction of the third shared substantive pass, not another research pass. The unrestricted periodic some-phase assertion and the original normalized-supremum conjecture remain unresolved. No source or historical novelty claim is made.

Reviewed inputs are the third-pass [cyclic two-harmonic proof](../proofs/cyclic_two_harmonic.md) and its 24-check verifier; the accepted second-pass report and independent audit provide the scalar-positive-inverse and finite-point-obstruction baselines. This acceptance reconstructs the median-sector calculation independently, rather than assuming the first-pass formula merely because the third-pass verifier rescales it.

Source credit remains A. Eremenko, *Conjectured inequality for subharmonic functions*, 4 April 2015, https://www.math.purdue.edu/~eremenko/dvi/subh1.pdf. The credited homogeneous and harmonic cases are not being presented as new results.

## 1. Domain, cyclic symmetry, and the scalar mean

Both variables lie on the 2 pi-periodic torus. For

    L = omega^2 partial_s^2 + 2 rho omega partial_s
        + rho^2 + partial_theta^2,

consider

    H_j(s,theta) = c(s) + a(s) cos(n theta+m s+2 pi j/3)
                         + b(s) cos(2n theta+2m s+4 pi j/3).

Integer n and m make this expression periodic. The restriction n>=1 ensures that the angular modes have zero angular mean and that the covering used below is nondegenerate. Each H_j is an angular translate of H_0 by 2 pi j/(3n); L commutes with these translations. It would suffice to assume positivity for H_0, but the stated theorem assumes all three and is consequently valid.

Angular averaging commutes distributionally with L and gives

    (omega partial_s+rho)^2 c >= 0.

Here is a self-contained proof of the consequent c>=0. For smooth periodic f, the resolvent

    Rf(s) = integral_0^infinity exp(-rho t) f(s-omega t) dt

satisfies (omega partial_s+rho)Rf=f by integration by parts. Composing this positive kernel with itself gives

    R^2 f(s) = integral_0^infinity t exp(-rho t) f(s-omega t) dt.

The homogeneous equation has solutions exp(-rho s/omega)(A+B s), so its only periodic solution is zero. Thus R^2 is the periodic inverse. If c is only continuous and its distributional image is nonnegative, convolve c with a nonnegative smooth periodic approximate identity. Each resulting right-hand side is nonnegative; the smooth inverse formula makes every mollified c nonnegative. Uniform convergence of the mollified c proves c>=0 everywhere. This argument does not attempt to evaluate a measure-valued forcing at an individual phase.

The sign of the temporal shift is s-omega t. Neither the incorrect opposite orientation nor inversion of the full two-dimensional L is used.

## 2. Independent angular median calculation

Fix positive a,b. Put p(v)=a v+b(2v^2-1). The three inputs are p(cos(x+2 pi j/3)). Their median is even and has period 2 pi/3, so its integral is six times its integral on 0<=x<=pi/3.

On this sector write

    X=cos x, Y=cos(x-2 pi/3), Z=cos(x+2 pi/3).

Then X>=Y>=Z, X+Y+Z=0,

    1/2<=X<=1, -1/2<=Y<=1/2, -1<=Z<=-1/2,

and direct subtraction gives

    p(X)-p(Y)=(X-Y)(a-2b Z),
    p(Y)-p(Z)=(Y-Z)(a-2b X),
    p(X)-p(Z)=(X-Z)(a-2b Y).

The first difference is nonnegative, in fact positive away from an endpoint tie. Set t=a/(2b).

- If a>=2b, then t>=1. The median is p(Y) throughout the sector.
- If b<=a<=2b, put alpha=arccos(t), so 0<=alpha<=pi/3. The median is p(Z) on [0,alpha], and p(Y) on [alpha,pi/3]. Indeed p(X)>=p(Z) throughout this regime, whereas p(Y)-p(Z) changes sign when X=t.
- If 0<a<=b, put alpha=arccos(t) and beta=2 pi/3-alpha, so pi/6<beta<=pi/3. Now p(Y)<=p(Z) throughout the sector. The median is p(Z) on [0,beta], and p(X) on [beta,pi/3], with the crossing determined by Y=t.

At a=b and a=2b the two descriptions agree; ties make no difference to the integral. Integrate each selected branch using

    P_j(x)=a sin(x+2 pi j/3)+(b/2) sin(2x+4 pi j/3).

The three unnormalized integrals are respectively

    -3 sqrt(3) b,
    -3 sqrt(3) [-b+2a-a^2/(2b)],
    -3 sqrt(3) a^2/(2b).

For the two crossing regimes these follow directly by substituting cos(alpha)=a/(2b), sin(alpha)=sqrt(1-a^2/(4b^2)), and beta=2 pi/3-alpha into the primitive. The square-root terms cancel. The independent verifier performs these sector integrations from the addition-law primitives, without the harmonic rescaling used by the author.

Consequently the normalized angular median is -k F(a,b), with exactly the stated F and k. The branch values at a=b and a=2b are b/2 and b, respectively.

Replacing x by n theta+m s leaves the normalized circle integral unchanged at every fixed s: the theta integral traverses n complete periods, and the starting point is irrelevant. There is no extra factor n in the normalized answer.

## 3. Every sign and zero case

Changing a to -a equals the common angular translation x->x+pi, since the second harmonic is unchanged. Negating all three inputs negates their median. It follows that, for b!=0,

    normalized angular median of the oscillating triple
        = -k sign(b) F(|a|,|b|).

For a=0 or b=0, a common half-period sign reversal of the sole remaining angular harmonic gives zero integral. If both vanish, the median is identically zero. These facts also agree with the continuous limits of the piecewise formulas.

Translation invariance of the median under adding the same c gives M(s)/(2 pi)=c(s) plus this oscillating contribution. Therefore:

1. If b(s_0)<=0 for some s_0, then M(s_0)>=0 because c(s_0)>=0 and the oscillating median is nonnegative.
2. If a(s_0)=0 for some s_0, then M(s_0)=2 pi c(s_0)>=0.
3. In the only remaining case, b>0 everywhere and a never vanishes. Continuity on the connected phase circle forces a to have a constant sign. If negative, translate theta by pi/n once and for all to make it positive, preserving L and all median integrals.

This exhausts the real-amplitude theorem, including all sign changes and all possible zeros. The same reasoning shows why uniformly negative phases would necessarily lie in the positive cone after the fixed symmetry. A phase-dependent sign flip is neither necessary nor permissible in this argument.

The strict positive-cone conclusion cannot be extended indiscriminately to zero amplitudes. For example, rho=n=omega=1, m=0, a=1, b=c=0 gives three harmonic profiles, zero forcing, and median integral zero at every phase.

## 4. The envelopes and their direction

Let x=a/b>0. Then F/b equals x^2/2 on [0,1], -1+2x-x^2/2 on [1,2], and 1 on [2,infinity). All branches are positive for x>0. The first is at most 1/2, and on the middle branch

    1-(-1+2x-x^2/2)=(x-2)^2/2.

Thus F<=b. With kappa=2-sqrt(2), the first branch satisfies F/b<=x/2<=kappa x, the middle branch satisfies

    kappa x-(-1+2x-x^2/2)=(x-sqrt(2))^2/2,

and on the last branch 1<=kappa x because 2 kappa>1. Hence F<=kappa a. Equality in the second envelope occurs at x=sqrt(2), so the stated sharpness of kappa is valid.

For A=average a, B=average b and K=average F(a,b), integration gives

    A>=K/kappa, B>=K.

These are lower bounds on positive amplitude averages. Substitution into a lower bound for C is legitimate only when their coefficients are nonnegative. The three q cases below enforce exactly this condition.

No Jensen assertion is available or needed. In fact, with b=1 and continuous positive a(s), the two examples

    a(s)=1/2+(1/4) cos s:  K-F(A,1)=1/64,
    a(s)=3/2+(1/2) cos s:  K-F(A,1)=-1/16

give opposite directions. Both can be made admissible within this theorem by taking rho=omega=n=1, m=0, c=10. Their forcing is bounded below by 10-3-3/2>0. Thus even admissibility does not rescue a universal exchange of F with phase averaging. The proof uses the pointwise linear envelopes before averaging, not F evaluated at averaged amplitudes, and never interchanges the median with phase averaging.

## 5. Distributional helical averaging

Let x=n theta+m s and h(s,x)=c(s)+a(s)cos x+b(s)cos(2x). The map

    T(s,theta)=(s,n theta+m s)

is an n-sheeted smooth covering of tori. Pullback preserves normalized torus integration: the n sheets compensate the Jacobian n. For any smooth nonnegative test phi(s,x), phi composed with T is an admissible nonnegative test on the original torus. Applying the chain rule to the formal adjoint in the distributional pairing proves

    L H_0 >=0 implies Q h>=0,
    Q=(omega partial_s+omega m partial_x+rho)^2+n^2 partial_x^2.

This is also valid by first taking smooth periodic mollifications and then passing to distributions. There is no global single-valued inverse theta=(x-m s)/n being assumed.

The full expanded operator is

    Qh = [omega^2 c''+2 rho omega c'+rho^2 c]
       + [omega^2 a''+2 rho omega a'+(rho^2-lambda^2)a] cos x
       - [2 omega^2 m a'+2 rho omega m a] sin x
       + [omega^2 b''+2 rho omega b'+(rho^2-4lambda^2)b] cos(2x)
       - [4 omega^2 m b'+4 rho omega m b] sin(2x),
    lambda^2=n^2+omega^2 m^2.

This expansion fixes both the mixed derivative coefficients and drift signs. The independent verifier checks the entire expression and the original-coordinate chain rule, not just the averaged version.

Define the phase average of the distribution by testing Qh against phi(x)/(2 pi), with no dependence on s. Every partial_s derivative integrates to zero on the periodic circle. With C=average c, the result is exactly

    G(x)=rho^2 C+(rho^2-lambda^2)A cos x
                      +(rho^2-4lambda^2)B cos(2x)
         -2 rho omega m A sin x-4 rho omega m B sin(2x).

Averaging a nonnegative distribution gives a nonnegative distribution. Here that distribution is the explicitly smooth trigonometric polynomial G, so G>=0 at every x. Its positive reflection average, [G(x)+G(-x)]/2, is consequently nonnegative and is

    rho^2 C+(rho^2-lambda^2)A cos x
                  +(rho^2-4lambda^2)B cos(2x).                 (*)

The sine drift does not vanish merely by integrating s; it vanishes at the later positive reflection step. Omitting it prematurely is wrong, though the final even polynomial in the report is correct. Positive or negative m and m=0 are all covered.

The report's description of these dual tests as measures on full phase circles or helices has the correct geometric meaning, with one useful technical clarification: evaluation at x=x_0 is done after averaging has produced the smooth G. Equivalently it is the limit of pairings with nonnegative smooth angular approximate identities around x_0, pulled back by T. It is not a direct, undefined pairing of a measure-valued forcing with another singular measure. For n>1 the inverse image is the appropriate union/cover of helical curves; that multiplicity is already included by normalized integration.

## 6. Every q regime, including endpoints and resonance

Since n>=1, lambda^2>0; put q=rho^2/lambda^2>0. Divide (*) by lambda^2. It becomes

    q C+(q-1)A cos x+(q-4)B cos(2x)>=0.

For 0<q<=1, evaluation at x=0 gives

    C >= (1/q-1)A+(4/q-1)B >= 3B >= 3K.

Both coefficients used here are nonnegative. The slack over 3B is (1/q-1)(A+4B)>=0.

For 1<=q<=4, evaluation at x=pi gives

    C >= (1-1/q)A+(4/q-1)B.

Put alpha=1-1/q in [0,3/4]. Both amplitude coefficients are nonnegative, so

    C >= [alpha/kappa+3-4alpha]K >= [3/(4kappa)]K.

The final inequality follows from the exact slack

    alpha/kappa+3-4alpha-3/(4kappa)
       =(3/4-alpha)(4-1/kappa)>=0.

For q>=4, evaluation at x=3 pi/4 kills cos(2x) exactly, while cos x=-1/sqrt(2). Thus

    C >= (1-1/q)A/sqrt(2)
      >= 3A/(4sqrt(2)) >= 3K/(4sqrt(2)kappa) = d K.

The first reduction's slack is A(q-4)/(4sqrt(2)q)>=0. Finally 3>d and 3/(4kappa)>d, so all three regimes imply C>=dK.

At q=1 the exact test is C>=3B; at q=4 it is C>=3A/4. There is no division by q-1 or q-4. Actual angular resonance of the original L when rho is an integer does not obstruct this argument either: no full L inverse is used anywhere. Only the scalar mean operator is inverted, and rho>0 makes that inverse well-defined. Possible zero harmonic coefficients do not require compatibility assumptions beyond the given L H_j>=0.

By the exact median formula,

    average_s[M/(2 pi)]=C-kK >= (d-k)K.

The rational strict bound is sound: sqrt(2)>7/5 gives d>9/10, while pi>3 and sqrt(3)<7/4 give k<7/8. Therefore d-k>9/10-7/8=1/40. These bounds need no floating-point approximations and do not claim optimality.

In the positive cone F(a,b)>0 continuously on a compact phase circle; hence K>0. The median is 1-Lipschitz in its three inputs, so M(s) is continuous. Its strictly positive average forces a strictly positive phase. Together with Section 3 this proves the full some-phase theorem.

## 7. Why the finite-point obstruction does not apply

The accepted second-pass obstruction says that no fixed finite positive combination of values of H can be nonnegative throughout the unrestricted noninteger-rho L-subharmonic cone. Its proof exploits a negative logarithmic Green-function singularity localized at a selected torus point.

The current argument does not assert such a point-value inequality. It first applies positive tests to the forcing on full phase circles, then uses the finite angular spectrum to obtain a smooth angular average and evaluates that average. It additionally uses the restrictive cyclic median formula and the positive-cone envelopes. These hypotheses are absent from the unrestricted finite-point assertion. Thus there is no conflict even where both theorems apply. At integer rho the earlier inverse-based obstruction is not invoked at all.

The exact second-pass mixed-sign example also does not invalidate the present conclusion. It disproves positivity at every phase for general cyclic profiles; this theorem asserts some-phase positivity for a smaller fixed-axis two-harmonic class. The current proof does not establish nonnegative full-torus median average for every admissible triple or for every sign-changing member of its own class.

General time-dependent relative axes, arbitrary nonuniform common angular drift, independent triples without this cyclic form, and unrestricted changing angular spectra remain outside the theorem. No Fourier-bandwidth limit, smallness assumption, nonresonance condition or differentiation assumption has been silently added to the stated continuous-amplitude result.

## 8. Reproducibility and falsification coverage

The supplied 24-check author verifier was copied to a separate replay directory and run under normal Python, -O and -OO. Its outputs match one another and the supplied [exact certificate](../certificates/cyclic_author.json) byte for byte. The author certificate was verified against its exact regenerated result.

The independent verifier constructs the median-sector primitives directly, checks ordering difference identities and branch junctions, reconstructs the full helical operator including amplitude derivatives, checks its pullback and even projection, establishes each q-interval slack and the resonance endpoints, and checks the envelope constants. It uses explicit exceptions, so optimization flags cannot suppress checks. Its algebraic certificate does not replace the analytic distribution, positivity and existence proofs given above.

Targeted negative controls reject a wrong median small-branch factor, reversed middle-branch sign, wrong scalar inverse shift, premature drift removal, omission of omega^2 m^2 in lambda^2, a spurious second-harmonic contribution at 3 pi/4, and omission of sign(b). Continuous admissible examples reject both proposed Jensen directions. A harmonic zero-median example rejects an overextended universal strict-positivity conclusion. These are exact symbolic or rational controls, not sampled numerical evidence.

No extra research branch, unrestricted resolution claim, copied third-party source text, or remote publication is part of this audit.

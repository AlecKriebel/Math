# An analytic counterexample to the unrestricted global-attractor maximizer assertion

**ID 4900006 / AMR-048-0006. Status:** complete counterexample candidate to the record's unrestricted formulation; historical/source scope must remain explicit. Independent review pending. Two substantive approaches used. No novelty or human peer-review claim.

## 1. Which assertion is addressed?

The imported record asks about every smooth dissipative system with a compact global attractor: must the supremum of local Lyapunov dimension occur at an equilibrium or an unstable periodic orbit? No genericity, chaos, transitivity or Lorenz-system hypothesis appears in that formulation. The answer to this unrestricted assertion is negative by the explicit system below.

This is **not** a resolution of the Lorenz-specific question in [Eden, 1989](https://www.numdam.org/article/M2AN_1989__23_3_405_0.pdf), Question3 on printed p411, nor of a refinement restricted to chaotic or typical self-excited attractors. Eden's pp408–409 define local/global exponent sums and ask related critical-trajectory questions. [Kuznetsov–Mokaev, 2018](https://arxiv.org/abs/1807.00235), SectionII, discuss strange attractors and a separate typical-system refinement. Those extra scopes must not be silently identified with the record's unrestricted quantifier. The original thesis was not recovered in this audit.

A later unrestricted formulation appears in [Parker–Goluskin, arXiv:2510.14870v2](https://arxiv.org/abs/2510.14870v2), Definition2.3 and the discussion after equation(18). Its fixed-global-index expression differs from the usual pointwise Kaplan–Yorke convention. We compute both below, separately. The counterexample works for both expressions, without interchanging a limit and a supremum.

## 2. The system

On R5=C times C times R, let z1,z2 be complex coordinates and w real. Put

    f(s)=-(s-1)(s-4)/(1+s^2),
    dot z1=[f(|z1|^2)+i] z1,
    dot z2=[f(|z2|^2)+i sqrt(2)] z2,
    dot w=-100w.                                            (1)

This is a real-analytic autonomous vector field on all R5 because its denominators are positive. In polar coordinates, each nonzero complex coordinate obeys

    dot r = g(r):=r f(r^2),       dot theta=omega,

with omega=1 or sqrt(2). In particular angle and radius are uncoupled.

### Completeness and dissipation

For s>=0,

    -4 <= f(s) <= 3/2,
    f'(s)=(5+6s-5s^2)/(1+s^2)^2.

The lower bound follows from f(s)+4=(3s^2+5s)/(1+s^2)>=0; the upper bound follows from f(s)=-1+(5s-3)/(1+s^2) and s/(1+s^2)<=1/2. Thus |dot r|<=4r, which prevents finite-time blowup in either time direction. The angular and w equations are also complete. The system defines a smooth complete flow.

It is strictly volume contracting everywhere. One oscillator's divergence is 2f(s)+2s f'(s). Dropping the negative term in the numerator of 2s f'(s) gives

    2s f'(s) <= (10s+12s^2)/(1+s^2)^2 <= 5+3=8.

Here s/(1+s^2)^2<=1/2 and s^2/(1+s^2)^2<=1/4. Hence total divergence is at most 11+11-100=-78<0. The counterexample does not rely on using an expanding ambient flow under an ambiguous meaning of dissipative.

### Exact compact global attractor

Let D2={z in C:|z|<=2}. The compact global attractor is

    A=D2 times D2 times {0}.                                 (2)

Indeed the radius equilibria are0,1,2. The radial velocity is negative for0<r<1, positive for1<r<2, and negative forr>2. All radii above2 decrease to2; inside[0,2], complete trajectories stay in that interval in both directions. Thus A is invariant under the complete flow.

For a bounded set of initial conditions with radii at most R, scalar uniqueness preserves radial order. Its maximum distance in each radial coordinate from[0,2] is bounded by max(r(t;R)-2,0), which tends to zero. The w-distance decays exponentially. Therefore A attracts every bounded set uniformly. It is minimal among closed sets with that property: because phi_t(A)=A, any closed set attracting the bounded set A must contain A. This establishes the usual global-attractor definition, not merely a locally attracting torus or an arbitrarily enlarged invariant set.

## 3. All equilibria and periodic orbits

The only equilibrium is(0,0,0). A nonzero complex coordinate cannot be stationary because its angular speed is nonzero.

A periodic trajectory must have constant radii: a nonconstant solution of the one-dimensional autonomous radial equation is strictly monotone and cannot be periodic. Every nonzero constant radius is1 or2. If both complex coordinates are nonzero, periodicity would require a positive T with T and sqrt(2)T both integer multiples of2pi, impossible. Thus there are exactly four periodic orbits: radius1 or2 in either complex coordinate, with the other coordinate zero and w=0.

The two radius1 circles are unstable. The two radius2 circles are stable. There are no other periodic or equilibrium candidates hidden elsewhere in the attractor.

## 4. Exact local exponent classification

For a single oscillator the three relevant asymptotic types are

    O=(-4,-4),       U=(3,0),       S=(0,-24/17).              (3)

TypeO occurs at r=0 and for0<r<1; typeU occurs at r=1; typeS occurs for1<r<=2. To verify these claims rather than estimate exponents numerically, note first that

    f(0)=-4,       g'(1)=3,       g'(2)=-24/17.

At r=0 the derivative is e^(-4t) times a rotation. At a constant nonzero radius the derivative, in moving orthonormal radial/angular frames, is diagonal with entries e^(g'(r)t) and1.

At a nonconstant radius r0, the same moving-frame derivative has entries

    partial r(t;r0)/partial r0 = g(r(t;r0))/g(r0),
    r(t;r0)/r0.                                              (4)

The first equality follows by differentiating the scalar flow, or by comparing the variational equation with d(g(r(t)))/dt=g'(r(t))g(r(t)). Since theta(t)=theta0+omega t has no radial dependence, there is no shear term. Standard one-dimensional linearization at the simple limiting radius gives rate-4 for both entries when r tends to0; when r tends to2 the first has rate-24/17 and the second rate0. Equivalently these rates follow by integrating g(r)/r near0 and g(r)/(r-2) near2, whose limits are-4 and-24/17. Thus all limits exist.

The five-dimensional exponent list is the sorted union of one type from(3) for each oscillator, together with-100. Because the moving-frame changes are orthogonal, this calculation is directly about singular values and also gives the exterior-power exponent sums. No regularity/ergodicity assumption or numerical Lyapunov estimate is being inserted.

In particular the torus

    T={|z1|=|z2|=1,w=0}

has exponents(3,3,0,0,-100), and every trajectory on it is aperiodic. Its finite-time singular values are exactly e^(3t),e^(3t),1,1,e^(-100t) for every t>0.

## 5. Pointwise Kaplan–Yorke convention

At each point, let j be the largest index with nonnegative sum of its first j exponents; the local dimension is j plus that sum divided by the negative next exponent, with dimension0 when the first exponent is negative. Zero exponents are included in the nonnegative partial sum. The six unordered type combinations give

    OO: 0;
    OU: 11/4;
    OS: 1;
    UU: 203/50 = 4.06;
    US: 4+27/1700;
    SS: 2.                                                   (5)

For example OU has sorted spectrum(3,0,-4,-4,-100), while US has(3,0,0,-24/17,-100). The largest value in(5) is203/50, achieved exactly at the U,U torus. The equilibrium has value0; the unstable periodic orbits have value11/4; the stable periodic orbits have value1. Therefore no equilibrium or periodic orbit attains the supremum.

## 6. Fixed-global-index expression

Now use the convention of Parker–Goluskin Definition2.3, also corresponding to the fixed index in Eden's local expression(3.4): let M_k(x) be the sum of the k leading local exponents, and take the smallest global index j for which sup_A M_(j+1)<0. The classification above gives

    sup_A M1=3,   sup_A M2=sup_A M3=sup_A M4=6,
    sup_A M5=-94.

Thus j=4, and the lowest local exponent is always-100. The expression whose supremum is taken is

    D4(x)=4+M4(x)/100.

Its maximum is again203/50 on the aperiodic U,U torus. Its values on the only competing orbit types are

    equilibrium OO: 96/25;
    unstable periodic OU: 79/20;
    stable periodic OS: 4-8/85.

All are strictly below203/50. These fixed-index values are not relabeled as the pointwise dimensions in(5). The same unrestricted maximizer assertion fails under this second convention too.

Finally, define the finite-time singular-value Kaplan–Yorke expression using the same nonnegative-partial-sum convention specified in Section5, with value0 when the first exponent is negative. Under this explicit convention, the torus and all equilibrium/periodic cases have exact exponential singular values, so their values equal(5) for every t>0. The printed Kuznetsov–Mokaev equation(5) instead uses a strict-positive partial-sum index and does not specify the zero-leading-exponent case; its printed formula agrees directly for the positive-leading torus and unstable-periodic cases, but the stable/neutral values1 and2 here use our stated convention and are not attributed to that formula. Thus for every positive time the spatial supremum is at least203/50, while all equilibrium and periodic candidates have the strictly smaller constant values above. Consequently inf_(t>0) sup_A dim_L(t,x)>=203/50 for our explicit nonnegative convention. No equality with203/50 is claimed for the finite-time spatial supremum or its infimum, and no limit/supremum interchange is used.

## 7. Scope of the conclusion

The counterexample answers the literal all-smooth-dissipative-global-attractor question negatively. It is not a chaotic/transitive attractor example and makes no claim about generic systems, Lorenz parameters, typical self-excited attractors, or a thesis statement that was not recovered. Any historical conjecture with extra hypotheses requires its own source analysis. The stronger phrase “Eden's conjecture is solved” without these qualifications is not justified by this package.

The exact verifier checks the scalar identities, dissipation inequalities on rational controls, all exponent combinations and both dimension conventions. The all-size analytic proofs of completeness, global attraction and orbit classification are written above, not inferred from simulation. No novelty or human peer review is claimed. Work used the inherited native runtime without model/reasoning changes; its exact model identifier was not exposed.

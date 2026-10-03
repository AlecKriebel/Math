# Global geometry and transport obligations

This independent argument was begun from the literal primary question. Its examples below test general transport and compactness implications; none is a counterexample in the atoroidal/minimal/nonzero-GV target regime.

## Global admissible functions versus local gauges

Fix a connected cooriented foliation and a global nonvanishing defining form alpha. A global transverse field N with alpha(N)=1 exists, e.g. the metric dual of alpha divided by its squared norm. For another global defining form with the same coorientation, the ratio lambda=alpha-prime(N) is a positive global function and alpha-prime=lambda alpha=exp(f) alpha. If a 1-form theta wedges to zero with alpha, then theta=theta(N) alpha globally. Thus globally admissible smooth variations can be parameterized by real functions f and g whenever the smooth setting is justified. There is no missing additional closed 1-form modulo alpha: equality of the defining relation forces its wedge with alpha to vanish.

This algebraic parameterization does not supply a sign-preserving gauge normalization. In particular, normalizing the defining form to alpha(N)=1 chooses a single defining form for that fixed N; it cannot discard other rescalings in a sign-existence problem without proving sign preservation. Choosing omega(N)=0 is a legitimate affine slice for omega at fixed alpha, but the sign of the GV density is not generally unchanged by moving to that slice. Local transport solutions on charts also require global compatibility; partitions of unity add derivative errors.

For smooth cooriented data, write d alpha=alpha wedge omega. Multiplying alpha by exp(f) admits omega-f=omega-df, and the affine freedom at fixed alpha is omega+g alpha. All conclusions involving derivatives here are explicitly conditional on enough regularity; the classical C² target is not thereby reduced to the smooth subcase.

## Two honest conditional transport subproblems

Fix a positive volume form Omega on a closed oriented 3-manifold. Put omega wedge d omega=q Omega. Define fields by i_V Omega=d omega and i_W Omega=alpha wedge omega. Both are tangent to the foliation and divergence-free: alpha wedge d omega=0 follows by differentiating the defining relation, and d(alpha wedge omega)=d(d omega)=0. The following are separate one-function subproblems, not a complete two-function solution:

- Rescale alpha by exp(f), choose omega-f=omega-df: the new density is q-V(f).
- Keep alpha fixed, choose omega+g alpha: the new density is q+W(g).

The exact exterior-form identities are simple and useful, but global existence of f or g producing weak sign is not automatic. For either divergence-free field Z, every invariant probability measure mu satisfies integral Z(u) d mu=0 for a C¹ function u, by differentiating flow invariance. Hence q+Z(u)>=0 requires integral q d mu>=0 for every such mu. If the latter integral is zero, continuity and nonnegativity imply the resulting density is zero on the support of mu. On a periodic orbit, the same requirement follows by integrating a derivative over its period. If the desired density is a specified constant c, the necessary condition is integral(q-c) d mu=0 for every invariant measure, not only normalized volume.

These restrictions may obstruct one subproblem. They do not obstruct all two-function gauges. Changing f changes the affine characteristic field from alpha wedge omega to alpha wedge (omega-df), up to the positive rescaling. A counterexample to Q13.1 requires an invariant obstruction for every admissible choice, plus an actual foliation with all stated hypotheses. The present diagnostic supplies neither. If Z vanishes, Z(u)=0 there; for the geometric V and W just defined, q also vanishes at those zeros, so arbitrary negative q at a stationary point is not an admissible geometric counterexample.

## Dense characteristics still do not imply solvability

Here is a complete analytic control outside the foliation target. On the 2-torus with coordinates of period 2 pi, let X=partial_x+a partial_y, where a=sum_{j>=1}10^(-j!) is irrational. For n>=4 put Q_n=10^(n!), P_n=Q_n sum_{j<=n}10^(-j!), and k_n=(-P_n,Q_n). Then

    0 < k_n dot (1,a) < 2 Q_n^(-n).

The strict positive tail and arbitrarily accurate rational approximants prove irrationality: if a=A/B, a nonzero error has size at least 1/(B Q_n), contradicting this bound for large n. Orbits of this irrational linear flow are dense. Define

    b(x,y)=sum_{n>=4} Q_n^(-floor(n/2)) cos(k_n dot (x,y)).

This real function is smooth and has zero mean. For each derivative order r, the tail is bounded by a convergent sum of a constant times Q_n^(r-floor(n/2)); finitely many early terms pose no problem. Were X u=b solvable even by a distribution, its Fourier coefficient at k_n would have modulus greater than

    (1/4) Q_n^(n-floor(n/2)).

Distributional Fourier coefficients have some fixed polynomial-growth bound, whereas these lower bounds exceed every such polynomial as n grows. This contradiction proves that dense smooth characteristics and zero mean are insufficient. This is not a GV foliation counterexample, and its torus does not satisfy the target atoroidal requirement.

## Weak sign, compactness, and regularity

Weak nonnegative sign with nonzero integral does not imply strict positivity. The periodic density 1+cos(x) is nonnegative, has positive integral, and vanishes on x=pi. Therefore a contact-only obstruction, including a nowhere-zero tangent-field/Euler-class obstruction, cannot be promoted to the weak-sign question. Any claimed global compactness argument must provide a topology strong enough to pass the defining equation and density to the limit, and preserve a nowhere-zero defining form. Merely taking f_n=-n gives positive defining forms exp(f_n) alpha whose coefficient limit is the zero form; local smooth admissibility alone gives no such preservation. Gauge functions can also grow or lose derivative bounds while densities improve.

The source explicitly includes C² foliations and the classical GV invariant at that regularity. A result proved for smooth forms may be preserved as a conditional partial reduction. To answer the exact target, one must define the low-regularity representatives and justify the extra derivatives or an appropriate weak formulation, global approximation, and pointwise-sign attainment. We neither claim that C² makes the invariant undefined nor assert a specific regularity convention that the primary did not state.

## Exact global gap

No verified statement above supplies a globally admissible pair of gauge functions with a weak-sign density for every target foliation. Conversely, no verified obstruction survives every gauge on an actual minimal taut atoroidal example with nonzero pairing. The unresolved choice is a global, constrained, sign-attaining representative problem, not merely a cohomology calculation or a local first-order identity. The central existence problem is therefore retained, not transferred into an unsupported claim and counted as solved.

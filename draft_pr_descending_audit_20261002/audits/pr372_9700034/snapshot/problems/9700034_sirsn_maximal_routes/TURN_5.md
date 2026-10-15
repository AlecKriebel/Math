# Author turn 5: mixtures and an affine-deformation obstruction

**Final substantive turn, original unresolved 5/5.**
This turn tests a genuine model-building route rather than an abstract scalar
law. It proves a countable-mixture reduction and rules out a natural
anisotropic-mixture construction starting from one bounded-stretch SIRSN.
It does not construct a counterexample or prove universal integrability.
No sixth author search follows the final freeze.

For a planar SIRSN law P write

    Delta(P)=E_P D,       p(P)=p_P(1),
    H(P)=E_P sup_i len R(0,U_i),       b(P)=Delta(P)+p(P).

Every b(P) is finite and at least one by the ordinary axioms; H may be
infinite. Endpoints are sampled independently, as in the original question.

## 1. Countable mixtures are legitimate SIRSNs

Let P_j be genuine SIRSN laws and let w_j>0 sum to one. Choose J with
P(J=j)=w_j, then sample the entire route process according to P_J. If

    sum_j w_j Delta(P_j)<infinity,
    sum_j w_j p(P_j)<infinity,                          (1)

the mixed law P is a SIRSN and

    Delta(P)=sum_j w_j Delta(P_j),
    p(P)=sum_j w_j p(P_j),
    H(P)=sum_j w_j H(P_j),                              (2)

where the last equality is allowed to be infinite.

Indeed, feasible compatible routes and consistent measurable FDDs are
preserved by a countable mixture. Each invariance holds conditional on J,
so holds after averaging; no transformation of J is necessary. Independent
Poisson sampling can still be made after choosing J. The finite-lambda
major-road intensities average linearly, and monotone convergence as lambda
increases gives the second equality in (2). The first and third are direct
conditioning and Tonelli. The first-moment and major-road requirements
follow from (1); their usual sampled-network consequence remains valid.
The original definition imposes no spatial ergodicity. Mixtures need not be
ergodic, so this argument must not be silently transferred to a class with
that extra requirement.

**Uniform-bound equivalence.** The following two assertions are equivalent:

(A) H(P)<infinity for every ordinary planar SIRSN law P.

(B) There is a finite universal constant C such that

    H(P) ≤ C [Delta(P)+p(P)]

    for every ordinary planar SIRSN law P.

Only (A)⇒(B) needs proof. If (B) fails and no P already has H(P)=infinity,
choose genuine laws P_j with H(P_j)/b(P_j)≥4^j. Set

    Z=sum_(j≥1) 2^(−j)/b(P_j),
    w_j=2^(−j)/[Z b(P_j)].                              (3)

Because b(P_j)≥1, 0<Z≤1, and the weights sum to one. The mixture has
sum_j w_j b(P_j)=1/Z<infinity, but

    sum_j w_j H(P_j) ≥ Z^(−1)sum_(j≥1)2^j=infinity.

It is a valid SIRSN contradicting (A). Each component has finite H and thus
finite maximum almost surely; so the resulting counterexample would still
have a finite maximum almost surely, with infinite mean. This proves the
equivalence.

The construction is conditional on actual laws with unbounded ratios. The
numerical assignment of arbitrary triples (Delta,p,H), or the scalar mixture
of turn 3, does not supply those laws. No existence assumption is smuggled
into this reduction.

## 2. Test a concrete deformation family

Take one fixed isotropic SIRSN P_0 with deterministic bounded stretch C_0:

    len R_0(x,y) ≤ C_0 |x−y|                            (4)

for each fixed pair almost surely, hence simultaneously for each countable
sample used below. Aldous's binary hierarchy, with its speed parameter
fixed, is a credited example. Put Delta_0=E D_0≤C_0. Let Gamma=R_0(0,(1,0))
and define its transverse variation

    c_0=E[total variation of the y-coordinate along Gamma].

Assume c_0>0. In fact a nondegenerate SIRSN cannot have Gamma straight almost
surely: the no-initial-segment property in Aldous Proposition 5.1 excludes
straight routes between sampled Poisson endpoints; invariance in position,
angle and scale transfers the same probability to every fixed distinct pair.
A continuous injective path between (0,0) and (1,0) with zero transverse
variation lies on that line and is the straight segment as a set. Thus the
source property gives c_0>0; finiteness and c_0≤Delta_0 follow from (4).
Keeping c_0>0 explicit also makes the argument independent of any stronger
claim about route regularity.

For lambda≥1 put A_lambda=diag(lambda,1). Transport every route and its
endpoints by this linear map, and then rotate the whole resulting network
by an independent uniform angle. Denote the law by P_lambda.

### These deformations really are SIRSNs

Invertible linear maps preserve finite-length non-self-intersecting feasible
routes and compatibility. They preserve translation invariance after the
corresponding inverse translation in the original process. Scalar dilations
commute with A_lambda, so scale invariance remains. The outer random rotation
restores rotational invariance. Measurable FDDs and consistency are preserved.

A transformed route between x,y has length at most

    ||A_lambda|| C_0 |A_lambda^(−1)(x−y)| ≤ C_0 lambda |x−y|,

so the first route moment is finite, and

    H(P_lambda) ≤ C_0 lambda.                           (5)

For the major-road condition, a transformed path element at distance at
least r from both transformed endpoints came from one at distance at least
r/||A_lambda||. Thus the transformed major-road process is contained in
A_lambda E^0_(r/||A_lambda||), using the naturally transformed Poisson sample
and then its infinite-intensity limit. Length increases by at most
||A_lambda||, while area increases by det A_lambda. Consequently

    p(P_lambda) ≤ [||A_lambda||²/det A_lambda] p(P_0)
                = lambda p(P_0)<infinity.               (6)

The outer rotation does not change this upper bound. In particular the
family is a genuine deformation family, unlike the earlier scalar examples.
Up to scale factors and rotations, it also covers orientation-preserving
global linear distortions of P_0, since P_0 is scale- and rotation-invariant.

## 3. Anisotropy forces the ordinary route moment to grow too

We show that the large maximum bound in (5) cannot be separated from the
one-route statistic by taking lambda large. Write V_x,V_y for the total
coordinate variations along Gamma, so E V_y=c_0 and E V_x≤Delta_0.
For a unit vector v at angle phi, invariance gives the route to dv the law
of d times Gamma rotated by phi. Its expected horizontal variation is at
least

    d (|sin(phi)| c_0 − |cos(phi)| Delta_0).              (7)

This follows pointwise by applying |a+b|≥|a|−|b| to the projected tangent
of every line segment and summing; the arclength limit gives the same fact
for the feasible countable-segment route.

To calculate Delta(P_lambda), average the unrotated transformed route
length over a uniform Euclidean unit vector u. Put w=A_lambda^(−1)u,
d=|w|, and phi=arg(w). On the angular event |u_y|≥1/2, of probability 2/3,

    d≥1/2,       |cos(phi)|≤2/lambda.

If lambda≥8Delta_0/c_0, then |cos(phi)|≤c_0/(4Delta_0)≤1/4 and
|sin(phi)|≥3/4. Equation (7) is therefore at least d c_0/2≥c_0/4.
Applying A_lambda multiplies horizontal variation by lambda, and total
length dominates that variation. Averaging over u gives

    Delta(P_lambda) ≥ lambda c_0/6
             when lambda≥8Delta_0/c_0.                 (8)

For smaller lambda use only Delta(P_lambda)≥1. Combining (5),(8), and
Delta_0≥1 proves the uniform ratio bound

    H(P_lambda) ≤ K Delta(P_lambda),
    K=8 C_0 Delta_0/c_0,       lambda≥1.                (9)

For large lambda the ratio bound 6C_0/c_0 is even smaller than K; for small
lambda, C_0 lambda≤K and Delta(P_lambda)≥1.

**No-go corollary for this construction.** Any countable mixture of the
P_lambda that is a SIRSN and has finite ordinary route moment automatically
has finite H, by conditioning and (9). Thus heavy-tailed global anisotropy
of a fixed bounded-stretch SIRSN cannot produce the counterexample sought
in §1. The constants depend on the fixed base law, notably c_0. This does
not rule out varying base models whose transverse variation tends to zero
relative to their other statistics, or genuinely local deformations.

No converse to (6), no independence of maximum and anisotropy, and no
Euclidean route-length triangle inequality was used.

## 4. Final disposition and exact remaining paths

The mixture route is valid only after obtaining actual SIRSN models with
unbounded H/(Delta+p). The natural fixed-base affine family fails by (9).
No alternative family with the required ratio has been constructed, and
no universal estimate in (B) has been established.

After five genuine author turns, the original remains **unsolved 5/5**.
The packet contains: a credited uniform Poisson-model corollary; an FDD
increment criterion; visibility and pair-correlation criteria; unconditional
geometric localization; and the mixture reduction with an affine no-go
result. The scalar counter-controls do not satisfy the SIRSN axioms, and
no full geometric counterexample is claimed. All historical author files
are preserved. Source comparison, verification and the pending independent
review do not create a sixth proof-search turn.

Concrete remaining mechanisms are a quantitative bound on terminal endpoint
pieces and finite exterior excursions, or a genuine model family with a
diverging normalized maximal expectation. The present positive results and
method obstructions do not settle either mechanism. Historical novelty is
unverified; classical mixture and projection arguments and the source's
bounded-stretch/no-initial-segment facts are credited.

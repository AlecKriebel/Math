# Independent adversarial mathematical audit

Checkpoint: 2026-09-23 04:06 UTC. Completion estimate for this bounded audit: 100%.

## Verdict and scope

The candidate's mathematical conclusion is correct for the product metric on
`S^1 x R`, for every fixed measurable essentially bounded open-loop torque.
I found no substantive counterexample or missing pendulum hypothesis. The
argument is a valid application of an existing theorem, with one small
presentation repair concerning eventual confinement. It is not a new
resolution of an open problem.

I independently checked the algebra, solution regularity, exceptional-set
quantifiers, and edge cases, and visually inspected printed pages 1583,
1587, and 1588 of Angeli and Praly's paper. Proposition 2 has the required
conclusion; Section III.A already applies it to this pendulum with arbitrary
positive parameters a and b. The normalized case is a=b=1.

Source: David Angeli and Laurent Praly, *Stability Robustness in the Presence
of Exponentially Unstable Isolated Equilibria*, IEEE TAC 56(7), 1582-1592,
[DOI 10.1109/TAC.2010.2091170](https://doi.org/10.1109/TAC.2010.2091170),
[public author-paper copy](https://liberzon.csl.illinois.edu/teaching/angeli-praly-almost-ISS-on-manifolds.pdf).

## Exact algebraic certificates

Put s=sin(theta), c=cos(theta), H=omega^2/2+1-c and
V=H+omega*s/2. Using s^2+c^2=1 gives the identities

```
V - H/2   = ((omega+s)^2 + (1-c)^2)/4,
3H/2 - V = ((omega-s)^2 + (1-c)^2)/4.
```

Thus H/2 <= V <= 3H/2, so V is nonnegative and proper. Along the
unforced dynamics, the stronger exact certificate is

```
-Vdot - (omega^2+s^2)/4
    = (omega+s)^2/4 + (1-c)*omega^2/2 >= 0.
```

Consequently Vdot is strictly negative except when omega=s=0. These are
exactly the downward stable equilibrium and the upright saddle. The
characteristic polynomials lambda^2+lambda+1 and lambda^2+lambda-1, and
the eigenvalues given in the candidate, are correct.

For forced dynamics, Hdot=-omega^2+omega*d. Young's inequality and

```
(-H/2+1) - (-omega^2/2) = omega^2/4+(1+c)/2 >= 0
```

prove the candidate's scalar comparison inequality and resulting limsup
bound. No simulation is needed to establish these identities.

## Small repair: eventual confinement

The source's Definition 2 asks for eventual confinement inside a fixed
closed ball. A limsup bounded by R does not alone imply eventual confinement
inside that *same* radius R. Add any fixed positive margin to the candidate's
radius before claiming this hypothesis. This does not change the result.

An independent, simpler repair follows directly from variation of constants:

```
|omega(t)| <= exp(-t)*|omega(0)| + (1+D)*(1-exp(-t)),
D = ess sup |d|.
```

Eventually |omega(t)| <= D+2, so the product distance is eventually at most
sqrt(pi^2+(D+2)^2) <= sqrt(pi^2+4)+D. This has the required constant plus
class-K form and also establishes forward completeness. Applied after any
initial time, it supplies the source's all-initial-times formulation.

The candidate's theorem paraphrase should retain the source's regularity
assumptions rather than present a weakened general theorem. This causes no
problem here: the actual field is jointly smooth in state and input.

## Independent check of the local null-set mechanism

There is an elementary pendulum-specific verification of the delicate local
measure claim, independent of a perturbed stable-manifold construction.
Fix one input d and choose 0<r<pi/2. In coordinates u=theta-pi, consider
initial conditions whose trajectories stay in |u|<=r forever. This is a
Borel set: it is the intersection, over nonnegative rational times, of
continuous-flow preimages of the closed angular strip.

At each fixed initial angle there is at most one initial velocity in this
set. To see this, suppose two such trajectories have the same initial angle
and different velocities. Label them so their differences q=u_2-u_1 and
p=omega_2-omega_1 satisfy q(0)=0 and p(0)>0. The common input cancels:

```
qdot = p,
pdot = k(t)*q - p,
k(t) = integral_0^1 cos(u_1(t)+tau*(u_2(t)-u_1(t))) dtau >= cos(r)>0.
```

Positivity is forward preserved: q(t)>0 and p(t)>0 for t>0. Fix t1>0;
then q(t)>=q(t1)>0 thereafter. Integrating
pdot>=cos(r)*q(t1)-p shows that p is eventually bounded below by a positive
constant. Hence q grows without bound, contradicting |q|<=2r.

Every vertical fiber therefore has at most one point. Fubini's theorem
implies zero area. Initial conditions eventually confined to this strip
form a countable union of inverse images of such null sets at integer
times. The finite-time maps are C^1 diffeomorphisms, so those inverse images
are null as well. The variational determinant is exp(-t), confirming
nonsingularity.

This proves the *local eventual-trapping exception is null*, even for a
large fixed input. It does not independently prove that every remaining
small-input trajectory eventually reaches the downward attracting region;
that global step still uses the cited theorem. It is supporting verification,
not a claim of a new standalone proof.

## Boundary and falsification checks

- **Zero input:** the upright equilibrium and its stable manifold must be
  exceptional because gamma(0)=0. They have zero area. A claim covering every
  initial condition would be false.
- **Small constant torque:** for 0<|a|<1, the stable equilibrium shifts to
  theta=arcsin(a), omega=0. Its positive-area basin forces any admissible gain
  to satisfy gamma(|a|)>=|arcsin(a)|. The existential theorem allows this.
- **Large torque:** persistent rotation does not contradict the statement.
  Angular distance on S^1 is bounded by pi, and velocity has the bound above.
  The same claim on the real angular covering space would fail for large
  constant torque; the specified cylinder is essential.
- **Measurable or rapidly switched torque:** the lifted field is globally
  Lipschitz in state, and additive input is locally integrable. Caratheodory
  solutions are unique and absolutely continuous; the energy inequalities
  hold almost everywhere. Smoothness of d is not required.
- **Input on a half-line:** extend d by zero for negative times to match the
  source's whole-line convention. This does not alter any forward solution
  or increase the input norm.
- **Quantifier order:** the exceptional set may depend on the entire fixed
  input. The proof does not establish a single null set valid for all inputs
  or robustness under arbitrary state feedback. The candidate uses the
  correct order.

## Strongest verified result and remaining gap

For the normalized pendulum there exists a class-K gain gamma, independent
of d, such that for each measurable d in L-infinity there is an
input-dependent area-zero set B_d with

```
limsup_(t -> infinity) dist((theta(t),omega(t)),(0,0)) <= gamma(||d||_infinity)
```

for every initial condition outside B_d. This is fully supported as a
corollary of the published theorem. No central mathematical gap remains in
that application after the elementary eventual-confinement clarification.
The audit is not a machine-checked reconstruction of every cited theorem;
symbolic scripts can verify the displayed certificates, not replace the
published robustness theorem.

No new research is warranted to settle this exact question. An accurately
attributed verification note or status correction is appropriate. A paper
claiming a new open-problem resolution, or a priority-clean original result,
would be inappropriate because the earlier paper already treats the same
equations and conclusion.

## Final artifact review

Checkpoint: 2026-09-23 04:11 UTC. Completion estimate: 100%.

Reviewed `AUDIT.md` and `verification/verify.py` after assembly and ran the
verifier using Python 3. It passed all 11 reported checks, including rejection
of the deliberately false energy identity. The sparse rational polynomial
operations, trigonometric reduction, differentiation, and certificates agree
with the written argument; their advertised scope is correctly limited to
algebra.

The explicit globalization is valid: for D<=1, the comparison estimate gives
uniform entry of each compact initial set into H<=4. Then V<=3H/2<=6<7,
and the only equilibrium V-values, 0 and 2, do not lie on V=7. Thus the chosen
proper sublevel meets the small-input theorem's requirements. The stated
flow pullbacks and countable compact exhaustion preserve nullity.

The proposed stitched gain is continuous at delta, vanishes at zero, and
dominates the required bound on either side. Its additional term is strictly
increasing both below and above delta, so strict monotonicity holds even if
the imported beta were merely nondecreasing. No remaining mathematical
defect or publication-priority overclaim was found in these two artifacts.

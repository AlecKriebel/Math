# Resonant NLS heat baths: model separation and an elementary drift obstruction

**Upstream ID:** 30003150 (OWR-14609-007). **Status:** original target unresolved; source specification hold. **Substantive approaches:** 2/5. **Independent review:** pending. This is a source audit and restricted diagnostic, not a new invariant-measure theorem.

## 1. Exact target and source limitations

The primary source is Andrea Nahmod's contribution, pp. 1549–1551 of [Oberwolfach Report 27/2016](https://doi.org/10.4171/OWR/2016/27). Its endpoint reservoirs have temperatures T1<Tn; at equal temperatures it asserts invariance of a Gibbs density proportional to exp(-H/(2T)). It asks for smoothness, uniqueness and ergodicity, then discusses n=3 and announces a Lyapunov/control strategy. The report does not display the stochastic generator, diffusion coefficients, precise state space or boundary convention. Its opening announces a construction, so treating the entire passage simply as an unqualified open conjecture loses source context. The report is about finite-dimensional resonant NLS here; the next contribution concerns water waves. The dataset's water-wave literature assessment is misplaced.

A theorem for an unspecified replacement bath cannot settle this question. No thermodynamic limit, infinite-mode limit, inviscid limit, or Sobolev-space assertion is established here. For n=3, the natural reduced action/relative-phase variables have five real dimensions, but the report itself does not specify that reduction or whether zero-action faces are excluded.

## 2. Later primary result and why it does not transfer automatically

Hani, Li, Nahmod and Staffilani, [arXiv:2505.16018v1](https://arxiv.org/abs/2505.16018v1), Theorem 1, prove existence and polynomial total-variation convergence for a deliberately modified three-mode system. Its quantifiers fix beta0>1, gamma>0 and T1>0, require sufficiently large T3, and choose a suitable phase-noise coefficient g. Sections 1.3–1.4 explicitly say their modified equal-temperature system does not preserve the Gibbs measure and leave more natural reservoirs for future investigation. The phase space is Omega=R_+^3 times T^2, treated away from zero actions in the Lyapunov analysis. Longer chains are excluded. This is a substantial credited result, but neither arbitrary temperature separation nor the original coupling is covered. The arXiv record inspected on 2026-09-30 lists v1, submitted 2025-05-21; no journal acceptance is asserted. The full analytic proof is not independently reconstructed here.

In the modified equation (1.8), the unforced middle action obeys the exact finite-variation identity

    dI2/dt = -2 I2 (I1 sin(theta1) + I3 sin(theta3)).                 (1)

Its endpoint actions have drift 2 Ij I2(sin(thetaj)-gamma)+gamma(Tj-Ij^3) and diffusion coefficient sqrt(gamma Tj Ij/2). The two relative phases have additional noise sqrt(gamma)g(I2,thetaj). Thus the theorem is not an assertion about endpoint additive Langevin noise in the original complex coordinates. The paper's prose before (1.8) contains apparent phase-index typos; all calculations below use the displayed middle-action equation (1), not those prose indices.

## 3. Restricted proposition: middle-action-only drift cannot control overheating

Consider any Markov diffusion on the open state space (0,infinity)^3 times T^2 whose middle coordinate has (1), with no stochastic differential in that coordinate. Its other coefficients may be arbitrary. Let V=F(I2), where F is C1. Then the generator applied to this function is

    LV = -2 I2 F'(I2) [I1 sin(theta1)+I3 sin(theta3)].                (2)

There is no second-order contribution because I2 has zero quadratic variation. The formula also follows pathwise by the ordinary chain rule and so does not need a C2 assumption on F.

Fix any middle action r>0 and positive endpoint actions a,b. At theta1=theta3=-pi/2 the right side is +2r(a+b)F'(r); at theta1=theta3=pi/2 it is its negative. Consequently LV cannot be strictly negative at every phase for this fixed triple of actions, regardless of the sign of F'(r). If F'(r)=0 it vanishes at every phase. In particular no such function can satisfy a strict negative generator bound throughout a high-middle-action region containing all phases. An increasing F has positive drift at the first configuration. For F(r)=r^p, p>0, this is 2p(a+b)r^p; for F(r)=exp(lambda r), lambda>0, it is 2lambda(a+b)r exp(lambda r).

This is only a pointwise obstruction for this restricted ansatz. It does not obstruct a phase-dependent Lyapunov function, a time-averaged drift inequality, or the published Feynman–Kac construction. Also V=F(I2) alone is not coercive on the full state space because endpoint actions can diverge while I2 stays fixed.

## 4. Restricted proposition: positivity is not a boundary uniqueness theorem

Suppose a path solves (1) on [0,t] and the coefficient

    A(s)=I1(s)sin(theta1(s))+I3(s)sin(theta3(s))

is integrable on that interval. The integrating-factor formula is

    I2(t)=I2(0) exp(-2 integral_0^t A(s) ds).                        (3)

For strictly positive initial I2 this stays positive on every such finite interval. It says nothing about long-time approach to zero or explosion of the other coordinates. If a larger-state-space extension has a well-defined integrable A on the face I2=0, the same formula makes that face invariant. Such an extension is not supplied by this argument: action-angle coordinates degenerate when a complex mode vanishes. Nor does invariance of a face alone prove existence of a stationary probability supported there. One must not import or exclude boundary stationary measures without specifying the original process.

## 5. What the later convergence theorem implies, conditionally

A standard elementary implication clarifies the uniqueness quantifier. Let P_t be a Markov semigroup on a measurable state space, pi a probability, and suppose P_t f(x) tends to pi(f) for every bounded measurable f and every state x. If nu is any invariant probability on that same state space, then

    nu(f)=integral P_t f(x) nu(dx) -> pi(f)

by bounded convergence, hence nu=pi. No finite Lyapunov moment assumption on nu is needed. Total-variation convergence in the cited theorem supplies this premise on its own specified state space. Unique invariant probabilities are extremal among invariant probabilities, giving ergodicity in that convention. This argument supplies no smooth-density regularity and does not extend convergence to omitted boundary states or to a different generator. Smoothness requires separate regularity/hypoellipticity hypotheses.

## 6. Exact unresolved gap and stopping point

Recover a fully specified original Gibbs-preserving bath model and its state space; establish recurrence against both high-middle-action trapping and low-middle-action freezing; then prove the appropriate irreducibility/regularity and uniqueness on that same space. General n, all T1<Tn, a smooth density, and any infinite-dimensional limiting statement remain unproved here. The 2016 announcement and the 2025 modified-model theorem are recorded without silently identifying their dynamics. The source-transfer route stops at this mismatch; the elementary drift route stops at the phase-dependent recurrence problem. Neither is a complete resolution.

## Verification and attribution

The accompanying checker verifies exact signs for rational action/exponent parameters, the scalar chain-rule coefficient, and integrating-factor algebra for piecewise-constant coefficients. These are diagnostic controls, not SDE simulation, a Lyapunov existence certificate or a reconstruction of the cited analytic proof. The proofs above are the certificate for their limited statements. No novelty or human peer review is claimed. Work used the inherited native runtime; no model or reasoning-setting change was made, and its exact model identifier was not exposed to this worker.

# Independent adversarial review: variational state accuracy and adjoints

**Final verdict: PASS_SCOPED_OBSTRUCTION.** The single requested initial-data clarification has been made and independently diff-checked. No mandatory correction remains. The free-particle construction is correct, and no repair to that construction is required. The original general-method question remains unresolved, one substantive attempt. This is an independent AI review, not human peer review.

Frozen PARTIAL.md SHA256: **1507718a1ff872f5e25a2ba79a0e564d24c33a4f69949dc746d5e7c369a9ebb4**. The author file was not edited. All3,310 submitted assertions reproduce byte-for-byte. A separately written checker passes1,118 symbolic and exact-rational controls.

## 1. Required precision clarification

Section2's sufficient C1 estimate should explicitly assume matching exact/discrete initial states, or an initial error of order h^r. Otherwise its error recursion includes an uncontrolled initial-error term. This is the standard implicit initial-value assumption, and the explicit obstruction already satisfies it. No other correction was identified. The author added precisely that hypothesis. The entire diff was checked, the unchanged verifier replayed, and the refreshed receipt differs only in the artifact hash. Final covered PARTIAL.md SHA256: **255db0059f6c1f9ff93a7bad95c06f0d81cc29111013a61173b7dc2ff710274a**. The archived replay intentionally retains the original reviewed snapshot.

## 2. Original source and credited results

I read the full Ober-Blöbaum contribution, printed pp.631–633 of OWR12/2015, and visually checked p.632. It asks for a general variational-integrator commutation result without defining a universal numerical-method class or listing all uniform regularity assumptions. A partial counterexample outside conventional smooth method classes therefore cannot automatically settle the original question.

Campos–Ober-Blöbaum–Trélat's published2015 Theorem5.2 indeed concerns the specified convergent sG method with positive weights, the listed primal hypotheses and a positive control-Hamiltonian Hessian. Its conclusions explicitly reserve adjoint convergence for future work. The submitted distinction between exact matching of discrete optimality systems and convergence of a boundary-value optimality problem is justified.

I checked Section3.2 of the full published Tran–Southworth–Leok2024 PDF, including Theorem3.3 and Proposition3.3 and their proofs. The cotangent-lift uniqueness concerns the discrete pairing for arbitrary tangent perturbations. The order-transfer proposition uses variational equivariance and sensitivity/cost regularity. This is not equivalent to merely deriving a mechanical state map from a discrete action. Their discussion also explicitly permits order transfer from a suitable linearization error estimate without the named equivariance property.

The full2026 control-Lagrangian source's Theorem3.7 and Proposition3.8 are explicitly about its specified low-order family and sufficient differentiability. The Patrick–Cuell source treats the zero-step singularity by smooth desingularization. These statements support the artifact's limits, rather than a claim that every positively stepped regular discrete action is covered by the existing conventional-method theory. No full independent audit of the unrelated PDE or general boundary-value convergence results is asserted here.

Primary links:
- [OWR12/2015](https://publications.mfo.de/bitstream/handle/mfo/3459/OWR_2015_12.pdf?isAllowed=y&sequence=1)
- [Campos–Ober-Blöbaum–Trélat2015](https://www.ljll.fr/~trelat/fichiers/CamposOberBlobaumTrelat_DCDS2015.pdf)
- [Tran–Southworth–Leok2024](https://doi.org/10.1007/s00332-024-10071-1)
- [Control-Lagrangian2026 paper](https://doi.org/10.1007/s11044-025-10138-1)
- [Patrick–Cuell](https://arxiv.org/abs/0807.1516)

## 3. Positive-step discrete Lagrangian

I independently differentiated F and K_h. The derivative K_h' is strictly increasing, has derivative between h and2h, and tends to both infinities because its linear term dominates the bounded arctangent term. It is therefore a global smooth bijection for each h>0. The Legendre-transform definition supplies a smooth translation-invariant type-I discrete Lagrangian. Differentiating its envelope cancels the inverse-function derivative terms, giving both discrete momenta equal to P_h(Q−q). The mixed derivative is minus the reciprocal of K_h'', hence never zero. The resulting phase-space step is the claimed global shear.

The mechanical shear is symplectic, and the exact discrete adjoint is its cotangent lift. I also checked the full four-dimensional cotangent Jacobian, including the second derivative of the shear in its costate component; it preserves the canonical cotangent symplectic form. Thus the defect is not a failure of the lift's exact discrete-gradient identity.

## 4. Uniform action/state estimates and limiting failure

The identity F(z)=integral from0 to z of arctan(t)dt proves that F is even, nonnegative and bounded by pi|z|/2. For bounded velocities |v|≤M and0<h≤1, the inverse relation gives |p−v|≤pi h^2/2. The action difference is exactly minus h(p−v)^2/2 minus h^5 F(p/h^2). In particular its absolute value is bounded by

    (pi M/2) h^3 + (3 pi^2/8) h^5.

This verifies the stated uniform action-value estimate with an explicit constant; it makes no derivative inference. Momentum is preserved exactly, so iteration gives the displayed full-horizon state formula without a stability approximation. The state error is globally bounded by pi T h^2/2, even without a compact initial-momentum restriction. At fixed nonzero momentum, its h^2-scaled limit is nonzero, so the second order is genuine.

Differentiating the exact discrete iterate gives the extra sensitivity T/(1+p_0^2/h^4). At p_0=0 it equals T for every mesh. With zero initial state and terminal gradient(1,0), the exact and discrete terminal states coincide but the earlier covectors differ by T−t_k in the second component. The terminal covectors themselves agree. Thus this is an error propagated backward from a common terminal objective, not an error in the terminal condition.

The stated second momentum derivative of the step perturbation equals−1/(2h) along p=h^2. This rules out a jointly smooth extension through zero step size and explains why differentiating a value error estimate loses its order. The qualification excluding standard uniformly smooth method families is mathematically necessary and is prominent in the submission.

## 5. C1 criterion and optimal-control embedding

With the initial-data clarification, the conditional estimate is valid. The state recursion gives global error O(h^r). The derivative comparison at the two trajectories is O(h^(r+1)), using the O(h) spatial Lipschitz constant of the exact short-time derivative. Products of the step derivatives stay uniformly bounded because each factor is at most1+Ch. The noncommuting product telescoping identity has O(1/h) summands and therefore yields a global sensitivity error O(h^r). The terminal-gradient Lipschitz bound finishes the adjoint estimate. Running-cost augmentation is valid only when the same hypotheses hold for that enlarged state, as stated.

The unactuated control embedding has a genuinely unique zero control: its quadratic running cost is strictly minimized there, while all states are determined by the fixed initial value. The state-constraint derivative is block triangular with identity diagonal blocks when differentiated against x_1,...,x_N. Hence it has full row rank. Direct KKT stationarity gives the same discrete covectors. If x_0 is treated as fixed rather than constrained, lambda_0 is the recovered initial gradient rather than a separate decision-variable multiplier; the nonvanishing error at every positive early mesh point is unaffected. The note correctly claims no failure of convergence of the primal control, which is identically zero.

## 6. Reproduction and remaining scope

The submitted standard-library verifier was replayed in author_replay/ and its receipt is byte-identical. The independent SymPy checker verifies differentiation and the action identity, positive Legendre Hessians, mechanical and cotangent symplecticity, full-horizon shears, complete state-constraint rank and KKT stationarity, every sampled mesh costate, and noncommuting matrix-product telescoping. These finite diagnostics supplement the analytic estimates and do not constitute a scheme classification.

The original record must remain unsolved1/5. The certified result disproves the weaker implication based only on positive-step smoothness, regular variational structure and second-order state accuracy. A counterexample or theorem for a precisely specified conventional smooth method class, with its force/cost/control discretization and stable optimality conditions, remains absent. No novelty claim or human peer review is implied.

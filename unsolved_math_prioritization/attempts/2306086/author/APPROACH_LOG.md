# Five-approach record

Date: 2026-10-05 UTC. Target: 2306086 / Function Theory 6.86.

Completion percentages below are subjective estimates toward an explicit full nonreal-point quantitative solution, not theorem confidence, calibrated probabilities, or claims about the source's exact intended sharpness requirement. The qualitative existence theorem is separately complete as an authored candidate proof.

## Approach 1: exact extremal controls and the radial obstruction

Checkpoint 07:13-07:16 UTC. Estimated quantitative completion: 10%.

Mechanism: differentiate the two real Koebe maps exactly and subtract the hyperbolic center in the source inequality. Outcome: both attain |A|=4 on the real diameter, and both have squared nonreal deficit 48(Im z)^2/|1-z^2|^2. This rules out any strictly smaller radius-only constant that is supposed to hold at every point with the same modulus.

Remaining gap: the original question fixes the point, so real-axis extremizers do not settle nonreal evaluation. Treating the radial obstruction as a counterexample to all possible improvements would be a quantifier error.

Artifact: PROOF_PARTIALS.md Sections 1 and 3; exact Koebe and real-axis controls.

## Approach 2: area-theorem equality rigidity plus compactness

Checkpoint 07:16-07:20 UTC. Estimated quantitative completion: 30%.

Mechanism: the normalized Koebe transform identifies A/2 with its second Taylor coefficient. The odd exterior square-root construction and area theorem recover both |a_2|<=2 and its exact Koebe equality case. A real-symmetric equality image must be a real slit complement, hence a real Koebe map, whose nonreal deficit is positive. Compactness then turns strictness for each function into a uniform strict gap over the whole class at a fixed nonreal point.

Outcome: complete qualitative strict-improvement proof, also uniform on compact subsets of D away from the real diameter.

Remaining gap: compactness alone gives no explicit gap or sharp formula. The source says "can be improved" without defining the desired quantitative strength, so this is a scope-sensitive result rather than an automatic full-resolution claim.

Artifact: PROOF_PARTIALS.md Sections 2-4.

## Approach 3: real automorphism covariance and geometric reduction

Checkpoint 07:18-07:22 UTC. Estimated quantitative completion: 35%.

Mechanism: normalized real Koebe transforms act bijectively on S_R and rotate A by an explicitly unimodular factor. The sharp modulus depends only on delta=|Im z|/|1-z^2|, reducing the question to z=i t. The two-slit map z/(1-z^2) produces an exact competing lower bound 8delta.

Outcome: exact one-dimensional reduction and lower envelope max(4sqrt(1-3delta^2),8delta). Two independent limits force the gap to vanish as delta approaches 0 or 1/2. At i/2 the two-slit map strictly beats both Koebe maps, so a Koebe-only answer fails.

Remaining gap: this is a lower bound, not the desired upper bound. Neither covariance nor the two examples establish the sharp extremizer.

Artifact: PROOF_PARTIALS.md Sections 5-6; exact covariance and two-slit controls.

## Approach 4: convex-hull and typically-real relaxation

Checkpoint 07:19-07:23 UTC. Estimated quantitative completion: 35%.

Mechanism: inspect whether extreme-point methods for real univalent classes can linearize the derivative ratio. Public author-hosted Koepf paper Section 4 was inspected as related context; the actual obstruction here is proved independently. The average of the two Koebe maps is typically real but has an interior critical point at i(sqrt(2)-1).

Outcome: exact failure of the naive convex-hull relaxation. The ratio f''/f' develops a pole in the relaxed class, so its linear extreme points cannot be substituted for the nonlinear univalent optimization. This is a concrete falsification of a proposed route.

Remaining gap: a variational method preserving injectivity, or a valid nonlinear extremal theorem, is still needed. No linear-support theorem is asserted to apply to f''/f'.

Artifact: PROOF_PARTIALS.md Section 7; quadratic-field critical-point control.

## Approach 5: switched real-symmetric Loewner controls

Checkpoint 07:20-07:27 UTC. Estimated quantitative completion: 30%.

Mechanism: evolve holomorphic derivative jets under a two-atom real-symmetric Herglotz field, with two control intervals followed by a Koebe/starlike tail. The family is rigorously admissible; a finite-dimensional floating-point search evaluates it.

Outcome: at i*0.45 the search returns about 3.61249 for |A|, compared with about 3.04599 for the elementary lower envelope. Similar improvements appear at t=0.3, 0.5, and 0.7. Recomputing the returned controls at tighter tolerances gives the saved values, but no interval arithmetic or verified ODE enclosure was used.

Remaining gap: the numerical comparisons are not certified lower-bound theorems. There is no proof that two switches suffice, no global upper bound, and no sharp extremizer. Continuing optimization would be more search rather than an independent audit.

Artifact: PROOF_PARTIALS.md Section 8; explore_loewner.py; LOEWNER_EXPLORATION.json.

## Freeze and disposition

Five substantive approach families are recorded. No remote mutation has been made. The strongest proved result is qualitative strict improvement at every fixed nonreal point, accompanied by exact scope obstructions and lower bounds. Full explicit/sharp quantitative resolution is not claimed. Independent audit should first examine the equality-rigidity argument, compactness quantifiers, covariance phase, and the distinction between the source's literal question and stronger sharpness formulations.

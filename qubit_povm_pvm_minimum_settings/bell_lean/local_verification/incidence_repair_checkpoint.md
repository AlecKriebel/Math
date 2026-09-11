# Incidence algebra repair checkpoint

2026-09-11T01:52:34Z. Assigned uphill/algebra/finite-duality subgoal: 100% compiled; overall paper certification is a separate unfinished goal.

Pinned Lean 4.19.0 successfully built Bell.UphillDirection, Bell.IncidenceAlgebra, and Bell.FiniteLinearAlgebra together (incidence_chain_build.log). Original theorem contracts were preserved, with reserved lambda variable renamed by the parent task. No axioms or placeholders were added.

Repairs: explicit rank-one and compatibility-map evaluation lemmas; imports for finite product dimension and calculus operations; vector literal and single-coordinate evaluation; correct matrix-scalar multiplication lemma; explicit linear-map extensionality; proof-preserving bilinear algebra simplification; finite-coordinate polynomial smoothness proof.

Strongest verified statements: a positive normalized uphill endomorphism exists under the stated three-constraint hypotheses; the exact stationary score-gap identity holds; polynomial incidence constraints are smooth; every compatible target metric differential has a metric increment via algebraic annihilator duality. Remaining physical/global integration is in downstream modules and is not asserted by this checkpoint.

## 2026-09-11T02:04:53.917744+00:00 — physical bridge checkpoint

Assigned algebra and local physical reconstruction subgoals: 100% compiled. Overall paper certification remains in progress in downstream reduction/assembly modules.

Actual production targets Bell.DeterministicGap, Bell.IncidenceScores, Bell.FrameRealization and Bell.GramLift now compile on Lean 4.19.0. Exact original theorem contracts are retained; the intended two operator fields in UnnormalizedAssemblage were separated because the incoming grouped syntax incorrectly parsed one as a function. Added a direct steeringFrame_mulVec evaluation lemma. The general matrixPair_mul_frames theorem was moved unchanged from IncidenceDifferential into IncidenceAlgebra with the calculus agent’s agreement, reducing the physical-frame dependency.

The local Gram-map strict derivative, explicit right inverse, implicit-function lift, open physical positivity conditions, pointwise POVM reconstruction, and physical-maximum transfer now have checked proofs. Selected dependency audits in IncidenceChainAxioms.lean report only propext, Classical.choice and Quot.sound; no sorryAx or custom axioms. The production build logs are incidence_scores_build.log, frame_realization_build.log and gram_lift_build.log. Independent temporary probes used exact copied prerequisites while production dependencies were unavailable; their duplicate sources were removed after the actual builds passed.

# PR302 independent family C review criteria

Frozen before reading the original mathematical source, candidate theorem, candidate proofs, or prior review conclusions. Created 2026-10-05 04:16 UTC. Reviewer: independent subagent /root/pr302_original_scope.

## Target and independence

The target hypothesis is that the submitted theorem in PR302 (original head eb6e0e999521d84a65f9857d338cad76b84d30db, originally claimed_solved, author budget 2/5) resolves the actual original problem, rather than a stronger-data or restricted-model substitute. No past review reports or other families' conclusions will be read before reaching an independent assessment.

## Success criteria

1. Read the complete official Markus Reiß contribution (with Chorowski, Gobet, and Hoffmann) in OWR24/2017 pages 1507–1509 and authenticate its official bibliographic identity. Record its exact mathematical question, context, and stated assumptions.
2. Read the complete proposed theorem, assumptions, construction, implementation, and examples in TURN_1 and TURN_2. Classify every mathematical and statistical restriction relative to the original source.
3. Determine whether the observations assumed by the theorem are actually available in the original experiment. Distinguish a stationary law, finitely many transition-density measurements, a single fixed sampling lag, noiseless access to spectral functions, noisy point clouds, and derived quantities estimated from the same trajectory.
4. Attempt to falsify claims at model boundaries: generic versus arbitrary diffusion; reversible versus nonreversible dynamics; known versus unknown invariant density; scalar/isotropic versus anisotropic diffusion; smoothness and boundary regularity; prescribed ellipticity/norm bounds; reflection and no-flux conditions; dimension and topology; stationary versus nonstationary starts; loss and convergence notion; finite versus growing spectral truncation.
5. Check that eigenfunctions, eigenvalues, tensor reconstruction, data differentiation, and finite-dimensional fitting are identified and stable under the actual information assumed. Identify unproved uniqueness or conditioning that transfers the central difficulty.
6. If a general resolution cannot be verified, state the strongest checkable restricted theorem and the exact unresolved original question. A counterexample or explicit information mismatch is preferred to a vague concern.

## Evidence and closure

Primary technical sources only, no outreach. Own-directory writes only; no Git, shared index, configuration, tracked status, services, or submitted snapshot mutations. Save downloaded source bytes and exact URLs, full text extraction, source/input/output inventories, and genuine native argv/cwd/PID/UTC/full stdout/stderr receipts for any subprocess tests. Record 0–100% completion toward this review independently of discovery claims. Freeze closed outputs after a report and verdict. A PASS requires all mandatory scope and observability checks; unresolved central assumptions yield HOLD with a precise repair or remaining gap.

# Quadratic-chain characterization of the Aubry set

This is an AI-assisted, unrefereed mathematical draft. Acceptance means one independent internal AI mathematical reconstruction accepted the stated partial result with a correction and explicit standard imports. It is not human peer review or formal proof-assistant certification. This is a prose proof-and-audit edition, not a computational reproduction package. No novelty, priority, or worldwide-current-openness claim is made.

## Accepted partial theorem

Let M be a nonempty compact connected smooth Riemannian manifold without boundary and f a smooth vector field, with flow phi. For L_f(x,v) = |v-f(x)|²/2, the projected zero-class Aubry set equals the quadratic-chain recurrent set R_2(f). Here x belongs to R_2(f) when, for every lower flight-time bound T > 0 and every epsilon > 0, it has a returning chain with flight times at least T and sum of squared jump lengths below epsilon.

The tangent Aubry set is {(x,f(x)): x in R_2(f)}. Every critical viscosity solution is constant exactly when R_2(f) = M; after fixing u(x_*) = 0, this is uniqueness of zero. The same criterion holds for the reversed drift by path reversal and a separate application of the theorem.

The general implication from ordinary chain recurrence to quadratic-chain recurrence remains unresolved by this work. This is a partial result for 20002465 / AIM-PDES-0077, not a solution of the full original problem.

## Read the complete argument

- [PROOF.md](PROOF.md): the full mathematical reconstruction, quantitative estimates, graph lift, strict strong-chain separation, uniqueness proof, smooth-circle viscosity counterexample and unresolved boundary.
- [AUDIT.md](AUDIT.md): editorial acceptance checks and dependencies for that one reconstruction; not a second independent mathematical audit.
- [ACCEPTANCE.md](ACCEPTANCE.md) and [ACCEPTANCE.json](ACCEPTANCE.json): the exact accepted claims, rejected claim and acceptance limits.
- [SOURCES.json](SOURCES.json): public bibliography, PDF hashes and sizes, and precise retrieval/inspection history.
- [VERIFICATION.json](VERIFICATION.json): byte-authentication and finite-regression boundaries.
- [MANIFEST.json](MANIFEST.json): all eight filenames and hashes of the other seven. Its own digest is pinned separately in the draft-PR body.

## Essential correction

The identity H_{-f}(x,p) = H_f(x,-p) does not give a viscosity-solution bijection u -> -u. On the smooth circle flow f(theta) = sin(theta) partial_theta, u(theta) = min{0,2 cos(theta)} solves H_f = 0, but -u fails the supersolution test for H_{-f} at theta = pi/2. PROOF.md gives every touching-test detail. The valid repair uses A_t^{-f}(y,x) = A_t^f(x,y), which implies equal projected Aubry sets.

Standard weak-KAM foundations are explicit imports. The AIM original was compared through primary-domain parsed PDF text, but its PDF-byte download returned HTTP 403 and a screenshot was unavailable. FFR preprint v1 was selectively inspected; its journal PDF was not inspected. The complete source documents, executable code, raw outputs, source datasets and private coordination material are excluded.

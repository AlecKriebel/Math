# Borderline soliton–potential interactions

**Problem:** 30001591 / OWR-4429-002, queue rank 978.
**Disposition:** unsolved, five substantive mathematical approaches completed (5/5).
**Manuscript status:** authored AI-assisted partial research record; not human-peer-reviewed or formally verified. No research-novelty, priority, or complete-literature claim. Independent audit is pending.

## Target and exact scope

The equation is u_t+(u_xx-lambda u+a(epsilon x)u^m)_x=0 on R_t x R_x, m=2,3,4. The question asks for the forward-time behavior at the critical parameter lambda=lambda_tilde of the solution incoming in H^1 as Q(x-(1-lambda)t) at minus infinity. The relevant limiting order is fixed sufficiently small epsilon>0, then t->+infinity. The corpus's bare positive smooth-potential formulation omits hypotheses used by the cited theorems; see SOURCES.md. The statements proved here carry explicit assumptions and do not silently solve the broader formulation.

## Results and limitations

PARTIAL_RESULTS.md gives full proofs of:

1. The exact critical auxiliary modulation orbit and its conditional logarithmic escape law.
2. Nonexistence of nonzero H^1 stationary states for strictly increasing coefficients, plus a cubic positive-energy forward-compactness obstruction.
3. Exact energy matching, the unique pure transmitted scale, and quadratic defect degeneracy.
4. Signed-integral restrictions under extra L^1 control, including the exact quartic cancellation lambda_tilde=1/4 and a broad-tail counterexample to an H^1-to-L^1 inference.
5. The perturbed modulation invariant identity, opposite outcomes for arbitrarily small invariant changes, and finite-initialization bias.

The main missing ingredient is an all-late-time PDE modulation/radiation analysis at equality. An auxiliary logarithmic orbit does not establish logarithmic PDE escape. Conservation laws do not select a branch. No endpoint statement is inferred from the off-threshold theorems or from a finite computation.

## Reproduction

Python 3 with SymPy is required. Run `python3 -B verify_packet.py` from this directory. This checks frozen payload hashes and byte counts, reruns all 43 exact algebra controls, rejects three deliberately incorrect algebraic identities, and compares the replay output with CHECK_RESULTS.json. The finite checks support the written proofs; they do not certify the PDE target.

TURN_LEDGER.json records the actual chronological mathematical-result checkpoints. Reading sources, exact algebra replay, source checks, and packaging are not additional approaches. PUBLIC_SOURCE_METADATA.json identifies retrieved public source bytes without including those sources. No copied source PDFs/text/images, raw corpus records, or private coordination are part of this packet.

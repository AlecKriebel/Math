# Restricted continuum transport result

Problem 30004632 (queue row 1850, OWR-4990379-002) remains **UNSOLVED** in its general form. Five approaches were investigated. This package gives an accepted restricted sufficient condition, not a general solution or novelty claim.

For the original alternating pair-local algorithm, uniform midpoint source grids on [0,1], two fixed target atoms, weakly converging feasible initial plans, and C^1 cost traces whose difference D has -D' >= gamma_min > 0, the actual weak plan trajectories converge at entropy scale n epsilon_n -> eta. For finite positive eta the continuum trajectory sorts globally by coth(gamma_min/(4eta)); eta=0 sorts by time 1, including vanishing positive entropy; eta=infinity freezes. Quadratic cost gives gamma_min=2(b-a). One partition update has time 1/n.

Read RESEARCH.md for the full proof, FIVE_APPROACHES.md for the research audit, and SOURCE_GATE.md for the exact open-question scope. Independent proof audits are preserved in three audit reports; the earlier conservative zero-entropy estimate is superseded by the n-update proof. Known zero-entropy odd-even sorting is explicitly credited to existing literature. No strong convergence of microscopic fractions, positive-entropy finite-grid exact sorting, or general PDE uniqueness is claimed.

## Reproduce

Use Python 3 with NumPy and SymPy (recorded versions in VERIFICATION_METADATA.json). From this directory run:

    python -B verify.py
    python -O -B verify.py

The verifier replays all three complete result files in both interpreter modes, rejects real mathematical mutations, and rejects missing, altered, added, and nested-MANIFEST inventory tampering. Only this directory's root MANIFEST.json is outside its own hash inventory; its hash is recorded separately in the freeze receipt. All checks use explicit guards effective under -O. Finite and symbolic tests supplement, and do not replace, the analytical proofs. Floating-point full-output replay is intended for the recorded Python/library environment.

SOURCE_METADATA.json contains only public scholarly PDF hashes and sizes. No copied source PDFs/text, dataset records, private extract fingerprints, or private coordination files are included.

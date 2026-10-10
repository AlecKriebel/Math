# Checks and their limits

The standard-library check_exact.py performed 884 exact finite checks. Both normal and Python optimized mode passed, with byte-identical JSON output. No correctness condition depends on a Python assert.

Coverage:

- All twelve candidate outer triangle areas squared, all twelve halves of the six central kites, coplanarity and orientation, all four outer chamber volumes.
- The exact one-parameter critical-point and convexity polynomial identities.
- All twenty-eight pair distances for the restricted constants, the eighteen allowed edges, outer sheet incidences and normal directions, and a rational grid of strict boundary-label samples.
- All 168 full-pair affine norm checks at the six vertices of the octahedron. Inequalities involving √6 use exact rational sign-aware squaring, not floating-point tolerances. Convexity extends these finite vertex checks to the entire octahedron in the written proof.
- Exact affine flux, divergence coefficients, active constraints, support half-plane tests for the fractional mixture, and the central contradiction's quadratic identity.
- Five deliberately false alternatives rejected: treating forbidden adjacencies as bounded, treating opposite restricted pairs as bounded, scaling the affine certificate by 110 percent, replacing the apex parameter by 1/5, and asserting compatible central bounds.

These tests do not establish arbitrary finite-perimeter partition theory, the divergence theorem for all generalized currents, or the symmetry reduction by code. Those arguments are written explicitly for independent mathematical review. Boundary-grid samples supplement a symbolic trace proof; they do not replace it. No Surface Evolver run, interval mesh computation, or global optimizer was performed. None of these checks certifies an unrestricted minimum.

The complete file manifest can be checked by verify_packet.py. Its expected manifest SHA-256 must come from a separately retained freeze record; a manifest that is modified together with its payload is not a trusted anchor. Inventory verification includes this verification script itself. No network or external dependencies are needed to replay the authored packet.

The packet additionally provides mutation_tests.py, which checks seven payload/inventory/anchor corruptions in both normal and optimized modes. These are integrity controls, not mathematical counterexamples.

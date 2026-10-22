# Verification scope

The written proofs are primary. The checker uses only Python's standard library and exact integers, rational arithmetic, and polynomial identities. It checks:

1. The nonlinear dissipation derivative, convexity/coercivity expressions, Fenchel equality, and Lyapunov identity on 24 rational states.
2. Scalar fixed-flux entropy, energy-gap, mass, and weighted-potential identities on 16 rational states.
3. The explicit fixed-flux formula, positive finite-time lower bound, reaction equation, and large-time gradient bound on 60 rational states.
4. Polynomial radial divergence and zero-total-forcing identities in dimensions 2 through 9, plus rational sample checks.
5. Exact gluing, mean-zero forcing, support separation, flux and primitive identities for the degenerate construction, and 340 rational state checks. Its perturbation has positive mean-zero L2 norm, so the two limiting normalized potentials differ. The example explicitly fails strict initial positivity.
6. Seven input-domain negative controls, status guards, absence of `assert` statements, and every payload hash and byte count.

These are bounded regressions of displayed algebra, not proofs by finite testing of an infinite-dimensional theorem. Transcendental averaging/limits, local elliptic theory, variational compactness arguments, and general PDE statements require the written arguments and source hypotheses.

The same payload is tested under normal Python, `-O`, and `-OO`. Required-read-only mode insists on effective UID 1000, checks writability flags, actually attempts a new file creation in the packet, and actually attempts write-opening every existing file. Each attempt must fail with PermissionError. An external before/after hash comparison verifies that bytes stayed unchanged.

The external harness also requires rejection of output inside the packet, rejection of a writable packet in required-read-only mode, successful output to a new external path, and rejection of a deliberately modified report under `-OO` with the original pins unchanged. That rejected copy is not distributed.

The freeze is permission-read-only and hash-pinned. It is not kernel-level immutable storage: the owner can change permissions. No checker rewrites its payload. A separate verification receipt records the actual test results; this document alone does not certify that a run occurred.

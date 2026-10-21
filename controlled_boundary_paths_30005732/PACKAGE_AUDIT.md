# Independent package audit

Review date: 2026-10-21. Disposition: PASS for the explicitly scoped partial results; original problem remains UNSOLVED.

## Mathematical scope

The research and mathematical-audit files were compared with their authored inputs. Their packaging changes are editorial and do not alter the proofs or assumptions. The strengthened continuous-speed example in RESEARCH.md was independently checked directly.

1. The weak area inequality assumes a bounded finite-perimeter space-time set, inward reduced-boundary normal, L1 endpoint traces, and a projected effort measure with density at most M. The homogeneous effort is max(|nu_x|-nu_0,0), including horizontal boundary pieces. BV slicing and distributional differentiation give DA >= P dt - M dt; planar isoperimetry gives the displayed scalar inequality. Singular nonnegative increments are permitted, and no BV-to-AC upgrade is asserted. Scalar comparison is localized to a positive comparator and then extended to extinction by traces. This is not a statement about arbitrary topological representatives or an unspecified weak admissibility class.
2. At critical budget M=2 pi R, the stationary disk is an area-minimizing comparator. The explicit theorem citation supplies area domination in its stated admissible class; the separate BV proof supplies it under the hypotheses above. Translations with center speed at most one retain exactly the same area and effort. The optimality assertion is restricted to hard-budget, nonnegative running/terminal area objectives, not arbitrary penalized-effort costs.
3. The continuous-speed center proportional to |t-t0|^(3/2) has speed defined at every time, satisfies beta>-1 under its displayed bound, and admits joint C1 normal coordinates. At a label pointing in the translation direction, its normal-path derivative has size at least a positive constant times sqrt(h), contradicting the O(h) estimate forced by joint C1,1 regularity. The conclusion is failure of universal A5 regularity of every optimizer, not failure of normal trajectories.
4. The kink-center example is confined to the weak a.e.-time formulation. It obstructs a C1 covering parametrization at the reversal but still admits unique AC normal paths. The stationary smooth optimizer remains available for the same initial disk and budget in both translated examples.
5. The exact graph waiting-time solutions and compact-boundary extension are admissible examples only, not proved optimal. The annulus component-loss example is also admissible only. The package preserves these limitations.
6. The shrinking-disk extinction formula and square-root asymptotics check out. Radial paths remain absolutely continuous up to their limiting point despite unbounded speed; no boundary-valued continuation into the empty set or nondegenerate endpoint cylinder is asserted. Positive-area pre-extinction geometry is smooth.
7. Smooth reparametrization and AC flow results retain their sufficient hypotheses. The superposition discussion does not manufacture a conserved boundary measure from perimeter alone. Neither the general optimal AC-trajectory problem nor existence of a regular optimal selection is claimed resolved.

## Sanitization and source claims

The package contains authored mathematical exposition, public citations, source identification, and hashes/byte counts/match results. It contains no copied source PDFs, dataset contents, source-page images, credentials, personal data, or private coordination files. Historical retrieval metadata is distinguished from fresh retrieval; the inspected arXiv survey text is distinguished from later publication metadata. This audit did not independently retrieve sources again and makes no claim of exhaustive literature coverage.

The audited research file is 16832 bytes with SHA-256 c7332f802bb701ed763abbedd530f078d905c4c7ec19c8e391a4008dcc619759. The audited mathematical-audit file is 11158 bytes with SHA-256 d80508ea8dbe35cc3522c75dcd7c4263f8cb9e4bd9b2416a37a3a0e424b403a5.

## Integrity controls

The verifier was inspected and independently run against an unmodified prepared inventory and isolated modified copies. Both ordinary Python and Python -O returned success for the unmodified inventory and nonzero failure for each of these six controls: modified file contents, missing file, unexpected file, symlink substitution, duplicate manifest record, and parent-directory traversal path. All 14 mode/case outcomes matched expectations. Checks use explicit exceptions rather than assertions, so optimization does not disable them.

These tests verify inventory and SHA-256/byte consistency only. They do not verify mathematical theorems, authenticate a publisher, or provide a cryptographic signature. The manifest excludes itself; an externally recorded manifest digest is needed to pin its inventory. This audit file must be included when the final manifest is regenerated, and both ordinary and optimized verification must pass on that final package.

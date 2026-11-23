Editorial note: The complete authored text is preserved below. Only references to undistributed operational artifacts, their identities, locations and replay directions have been replaced with descriptive prose. Mathematical arguments, evidence counts, corrections and limitations are retained. This prose edition identifies its distributed files and public scholarly sources. Historical conditions in the source record are distinguished from current dependency status in ACCEPTANCE_AND_DEPENDENCIES.md.

# Fresh verification of this recovery edition

Both checkers completed under ordinary Python, -O, and -OO. After removing the recorded optimization-mode integer, each checker's three outputs are identical. All checks use explicit exceptions and failure exits, not removable assertions.

## Word-relaxation checks

- All 88,560 labeled words over {0,1,2}, lengths three through ten, are enumerated without symmetry reduction.
- Queue-based reachability agrees with the exact predecessor criterion on every word.
- All genuine three-color words survive the relaxation.
- A separate binary nonswitch-gap classifier agrees on all exactly-two-color words.
- Every surviving odd binary word has at least three nonswitches and satisfies the exact gap bound.
- The three-nonswitch sharpness examples pass at order five and every odd order from seven through 101.
- Eight malformed inputs, including Boolean and floating-point colors, are rejected.
- Seven fixed controls and three explicit witnesses reject intentionally overstrong claims.

These are checks of the word relaxation, not a search over actual tournament completions. They do not establish the unrestricted conjecture on the tested orders. The all-order claims rest on the mathematical proofs.

## Incidence-deletion checks

111 fixtures are checked: an empty graph (core only, no source conclusion), a singleton, a stable seven-vertex colored circulant, an extension with a deficient source and sink, seven transitive examples, and 100 deterministically seeded colored tournaments of orders five through nine.

For every fixture, exhaustive enumeration of all deletion schedules yields one terminal set. It agrees with both extreme deletion orders and with the union of all stable induced subsets. The extension control distinguishes old vertices retaining their witnesses from an arbitrary superset being stable. Six malformed matrices are rejected, including Boolean and floating-point cells.

The fixtures need not be cyclic-rainbow-free. The tests concern deletion order, not source existence or the cited source incidence theorems.

## Boundaries

The b=8 specialization of the incidence corollary requires the separately accepted finite certificate. No files, acceptance bytes, or finite-search results are recreated here under their historical hashes. Fresh independent review must refer to this recovery edition's manifest.

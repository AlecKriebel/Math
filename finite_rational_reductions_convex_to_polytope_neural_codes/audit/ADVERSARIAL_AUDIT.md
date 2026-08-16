# Adversarial audit

Audit date: 2026-08-15.

## Verdict

**PASS for the submission package and retained theorem suite.**

**NO PASS, and no claim, for universal polyhedralization or a curved-only convex code.**

## Load-bearing attacks

1. **Cap threshold equality.** Points with cap coefficient exactly `1/2` are excluded by strict interior. A point cannot lie in two strict caps because two coefficients larger than `1/2` would sum to more than one. Points with no dominant apex retain an old word.
2. **Mixed apex combinations.** The cap proof uses independent height coordinates and a projection estimate; it does not assume that one apex dominates every point of the ambient hull.
3. **Deletion ordering.** Missing core words are deleted in nondecreasing cardinality, so strict superwords selected from a minimal maximal-word family have not yet been deleted.
4. **Binary-meet strictness.** Inclusion-minimality implies removing any selected maximal word strictly enlarges the intersection; partitioning the family yields two strict surviving superwords whose meet is the deleted word.
5. **Bridge extension.** The source segment is covered on `[0,1]`; openness gives a slightly larger open interval. Endpoint equality classes, including simultaneous events, are kept together under rationalization.
6. **Lower-dimensional arrangement cells.** The fixed-arrangement proof uses relative openness and weak separation in the affine hull; it never assumes a full-dimensional outside cell.
7. **Tangent cells.** A cell whose closure meets the selector can still be wholly outside. Weak separation is used with strict inclusion on the selector side, avoiding a false positive-margin assumption.
8. **Protected inactive witnesses.** Every new neuron polytope lies inside its source neuron. An inactive source witness is therefore outside the new polytope, even though the witness simplex for its own word may cross excluded-neuron boundaries.
9. **Trivial neurons.** Neurons occurring in no codeword are deleted before the protected-supercode construction and restored by lower-dimensional polytopes with empty ambient interior.
10. **Compact carriers.** Every unwanted nonempty carrier lies in at least one protected compact neuron polytope and hence is compactly contained in the ambient interior. Empty carriers require no repair.
11. **Atlas coverage.** The atlas covers the complete closed carrier by interiors of source-contained patches, so strict-boundary points are not omitted.
12. **Naive repair failure.** Exact rational clipping confirms that a later independent hull recreates the forbidden word; synchronized enlargement realizes exactly the target calibration.
13. **Nerve/code distinction.** No proof substitutes nerve preservation for atom-code preservation.
14. **Retraction firewall.** The retracted global good-core subdivision, universal stable lifting, and intersection-completion retraction are explicitly excluded.
15. **Verifier scope.** The scripts replay finite calibrations only; the manuscript states that universal proofs are mathematical, not exhaustively verified by computation.

## Residual expert-review risks

- The full projection inequality in the cap construction deserves independent geometric checking.
- The weak-separation-to-interior step in the fixed-arrangement theorem is subtle for tangent lower-dimensional cells.
- The convention crosswalk should be checked against both the published morphism paper and erratum.
- The priority status of the binary-meet normal form and fixed-arrangement theorem should be confirmed by domain experts.

No central mathematical defect was found in the retained proofs after the corrections listed in the theorem ledger and source map.

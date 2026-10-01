# Independent first-pass criterion

Sealed initial criterion: 2026-10-01 18:11 UTC. This file was written after reading only the frozen SOURCE_STATUS.md, source_record.json and snapshot_manifest.json, plus the initial primary-paper metadata/definitions returned by the web tool. No historical review, root conclusion, or sibling report has been consulted.

## Exact target

For each integer j >= 0, every compact PL pseudomanifold X of dimension 4j+2, with integral orientation of its regular stratum and the mod-two lower-middle link Witt condition, must have zero Witt class for its nonsingular middle intersection pairing over F2. The target uses the usual convention of no boundary and no codimension-one singular strata. These conventions and any reduction from nonnormal/disconnected spaces require checking, rather than assumption.

## Candidate mechanism and independent burden

The candidate's proposed direct mechanism is: integral orientation implies local link orientability; the Goresky-Pardon odd Steenrod identity on an appropriate intersection cohomology domain implies zero middle self-intersection; a nonsingular alternating F2 form is hyperbolic and hence Witt trivial. This audit passes that route only if each arrow is justified for the exact target, including j=0.

Required checks:

1. Read complete primary definitions, theorem statements, and proofs for the local orientability implication and odd-square identity, including the operation's perversity and degree domain. Identify the coefficient system and hypotheses actually used.
2. Distinguish a valid middle intersection pairing from an ordinary cohomology pairing and from a potentially degenerate image pairing. Show explicitly how the source's domain represents every vector in the target pairing.
3. Check whether integral orientation implies orientability of every link without orienting singular strata, choosing coherent link orientations, or assuming trivial orientation monodromy.
4. Track connectedness and normality restrictions. A normalization claim about cobordism alone is insufficient if the direct pairing route silently needs it; an explicit preservation/isomorphism argument or a source theorem is required.
5. Verify all j >= 0, including dimension 2, vanishing-dimensional middle space, disconnected target, and singular spaces. Show the finite-dimensional symplectic-basis argument without relying solely on an Euler characteristic parity claim.
6. Try to falsify the adapter using mod-two oriented but integrally nonorientable examples, nonorientable strata with orientation-twisted link bundles, operation-degree mismatches, and stronger local-square-free hypotheses.

## Decision rule

Pass only when the exact target follows from checked primary results and explicit elementary adapter deductions. Qualify a pass if the candidate is correct but omits a necessary convention or explanatory adapter. Block the route if its central step needs an unsupported equivalent/stronger assertion. No numerical form probe can substitute for a universal geometric implication. No priority claim is made.

Initial completion estimate for this family audit: 15%. The estimate measures finished falsification/verification work, not confidence or progress toward a new discovery.

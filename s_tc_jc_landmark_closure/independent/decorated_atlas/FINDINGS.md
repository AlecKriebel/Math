# Independent primitive-atlas findings

## Verdict

**VERIFIED:** the bounded primitive gate is closed for 4, 5, 6, and 7 ports
under the corrected locked definition of `S_TC`.

**VERIFIED AFTER CORRECTION:** the predicate
`selected_retains_strong_core` is classified using all selected reticulation
sinks and containment of at least one minimum repair. The pre-correction
primitive release had no dummy-completion classifier; its failure and former
manifest hash are preserved.

**LIMITATION PRESERVED:** this predicate decides retention of the original
primitive core as a strong factor, not intrinsic selected `S_TC` membership
after arbitrary `red_*`. Omitting a cycle sink gives an exact counterexample:
the cycle core is lost but the selected restriction reduces to a strong
three-leaf tree. The earlier semantic overclaim and its manifest hash are
preserved.

The generator, canonicalizer, admissible-rooting census, decorated-relation
contract, displayed-tree compiler, and verifier are independent of the
historical atlas code. Final manifests bind the corrected definitions lock,
including the requirement that `S_TC` have at least one admissible rooting.

## Decisive result

The exact universe contains 148,479 labelled primitives and 19,290 decorated
ordinary-triangle-redirection relations. There is no collision among the
148,479 sufficient displayed-parameter signatures. Hence no nonisomorphic,
non-`T` equal-signature candidate survives in this primitive universe.

This result is deliberately narrower than the desired JC classification.
Unequal displayed-parameter signatures are not separation certificates. The
following remain outside this task and unresolved here:

- saturated model-ideal and open-stochastic comparison of every unequal
  directed relation;
- bounded-support promotion to arbitrary subdivisions;
- one-sided containment;
- local-to-global identifiability.

## Verification status

- Primary exact producer: passed for p4 through p7.
- Independent end-to-end contract verifier: passed.
- Independent p7 reviewer: `ACCEPT_PRIMITIVE_GATE`; no P0/P1 findings.
- Independent p7 raw enumeration: matched all accepted and rejection counts.
- Nested selected-core reviewer: stale-certificate finding resolved; its later
  intrinsic-`S_TC` semantic overclaim was separately corrected and preserved.
- Mutation-sensitive contract: all 17 mutations rejected at p4 and p7.
- Byte-identical clean regeneration: 24 files reproduced exactly.

The active manifest body hash is
`fea4e1876d422234c7c25a7cc39a8e50a3e2a29eadac5b1d9fc4a4dc0f3c8f2a`.

The dummy-rule correction promotes `6, 38, 126, 310` completion-target rows
from false negatives to `selected_retains_strong_core` at 3, 4, 5, and 6
selected outgoing ports, respectively. These are target-row counts, not full
decorated relation counts. Existing fully selected primitive `T` relation
counts do not change. No generic intrinsic selected-`S_TC` claim is made.

See `EXHAUSTIVENESS.md`, `ADVERSARIAL_REVIEW.md`,
`ADVERSARIAL_REVIEW_DISPOSITION.md`, `SELECTED_STRENGTH_CORRECTION.md`,
`SELECTED_STRENGTH_REVIEW_DISPOSITION.md`, `VERIFICATION_TRANSCRIPT.md`, and
`certificates/manifest.json` for the proof boundary and content hashes.

# Adversarial Review Result

## Independent review

An independently launched read-only reviewer examined the clean-room logic,
recomputed the mathematical certificates without importing project code, and
actively tried to falsify both release conclusions.

Its initial verdict was `ACCEPT_WITH_CORRECTIONS`. It independently confirmed:

- all 64 zero-sum quartet assignments satisfy split-complement equality;
- all 112 noncomplement unordered mask pairs are separated by a JC
  zero/nonzero-factor assignment;
- the positive rational section for `(x_left,x_right) -> x_left*x_right` is
  exact and interior;
- the two quarantined rooted graphs independently reduce to the same labelled
  mixed graph;
- their raw descriptors and pullbacks differ while normalized ones agree.

It found three release-harness defects, none of which falsified the mathematics:

1. source and manifest hashes had become stale after concurrent source and log
   edits;
2. the AST source check could accept a required assignment hidden below
   `if False`;
3. the quarantined graphs did not themselves exercise a root arc entering a
   reticulation, despite wording that implied they did.

## Corrections

The final package:

- recomputes certificates in memory and compares their exact bytes by default;
- regenerates only when explicitly invoked with `--regenerate`;
- excludes literal-dead branches and nested-function declarations from its AST
  source checks and includes a dead-code mutation;
- adds an independent LSA-valid, strongly tree-child quartet fixture in which
  one root arc enters a reticulation;
- checks both switchings and all 64 zero-sum assignments for that fixture,
  including the inactive-parent mask pair `(15,0)`;
- relocates the root to a pendant edge, independently reduces both
  presentations to the same standard mixed graph, checks normalized-descriptor
  equality, and checks exact pullback factorization for all 15 JC coordinates;
- records exact source and review-artifact hashes in a fail-closed manifest.

The final adversarial rerun and its disposition are recorded in the research
log and deterministic certificates.

## Preserved final-call-site defect and correction

A narrow follow-up reviewer found one further harness defect after the first
corrections. The reachability helper recognized `if False` but not the
truth-equivalent `if 0`, while the call-site audit accepted the existence of
correct graph-ID calls without excluding additional live wrong calls. An
in-memory mutation therefore left correct calls below `if 0`, changed the live
calls to mixed-code arguments, and incorrectly passed. The reviewer returned
`REJECT` for that intermediate harness. The active primary compiler itself was
not affected.

The final verifier preserves and rejects that exact regression. Literal AST
conditions are evaluated by `ast.literal_eval`, and the call-site audit now
requires exactly two live calls in the structural source/target positions,
with `(source_graph,source_graph_id)` and
`(target_graph,target_graph_id)` respectively. The mutation is recorded as
`source_wrong_live_graph_ids_with_if_zero_correct_decoys` in
`certificates/mutation_certificate.json`.

## Final reviewer verdict

A fresh read-only reviewer checked only the corrected regression, the exact two
live call-site bindings, the first-class invariant-input hashes, and the
check-only wrapper. It found no blocker and returned `ACCEPT`. This acceptance
is scoped to the zero-sum descriptor/cache and graph-specific bounded-atlas
convention gate; it does not certify the full landmark theorem.

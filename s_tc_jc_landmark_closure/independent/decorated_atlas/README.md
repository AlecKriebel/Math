# Independent primitive decorated atlas

This directory is a clean-room implementation of the primitive local atlas
needed by the landmark level-2 JC closure program.  It imports no historical
network enumerator, graph canonicalizer, Fourier engine, signature table, or
separator selector.  Historical files are not runtime inputs.

The implementation has four deliberately separate layers:

1. `graphcanon.py` canonicalizes finite coloured mixed graphs and returns the
   winning raw-to-canonical vertex and edge transports.
2. `primitive.py` derives cycle and theta ported blobs from the degree and
   cyclomatic constraints, enumerates every directed local presentation, and
   filters by the locked narrow-standard and local `S_TC` conditions.
3. `fourier.py` derives displayed switchings, descendant masks, and exact JC
   Fourier coordinate polynomials directly from each graph.
4. `relations.py` canonicalizes an ordered source-target disjoint union with
   side colours and explicit port-matching edges.  A target graph by itself is
   never a relation identifier.

`build_atlas.py` emits content-addressed manifests and
`verify_contract.py` regenerates and checks them.  `mutation_tests.py` alters
the load-bearing bindings and requires every mutation to be rejected.

The final scoped verdict and proof of exhaustiveness are in `FINDINGS.md` and
`EXHAUSTIVENESS.md`. `ADVERSARIAL_REVIEW.md` is the preserved independent
review; its minor findings and corrections are tracked separately in
`ADVERSARIAL_REVIEW_DISPOSITION.md`.

`SELECTED_STRENGTH_CORRECTION.md` records two later adversarial corrections.
The certified predicate `selected_retains_strong_core` depends on selected
sink coverage and containment of a minimum repair, never on the mere presence
of dummy leaves in one completion. It is only a fixed-core retention predicate:
it does not classify intrinsic selected `S_TC` membership after arbitrary
induced-network reduction.

The nested review's stale-certificate finding and the later semantic
correction are closed in `SELECTED_STRENGTH_REVIEW_DISPOSITION.md`. Exact final
commands, hashes, mutation results, and byte-identical regeneration are in
`VERIFICATION_TRANSCRIPT.md`.

## Mathematical scope

For `p` boundary ports, a primitive nonroot factor has one distinguished
incoming boundary and `p-1` outgoing boundaries.  The default bounded universe
uses `p=4,5,6,7`, matching the rigid-support sizes required by the surrounding
closure program.  The generator itself accepts any `p>=3`.

The finite grammar is exhaustive for literal simple binary level-2 blobs:

- cyclomatic number one gives a cycle, with one port on every cycle vertex;
- cyclomatic number two gives a theta graph, with two cubic poles and three
  internally disjoint pole-to-pole paths; every non-pole path vertex has one
  port, and simplicity permits at most one empty path word.

Reticulation placement and every orientation satisfying the binary bidegrees
are enumerated rather than inserted from a catalogue.  Strong tree-childness
is checked on the resulting mixed graph by the locked arrow-tail condition and
also on the generating directed presentation. The independent rooting census
uses the corrected nonvacuous definition: at least one admissible rooting must
exist, and every admissible rooting must be tree-child.

The emitted `displayed_parameter_signature` is a *sufficient* exact
parameter-permutation equality certificate: equal signatures yield identical
complete JC port tensors after an explicit edge permutation and independent
reticulation-choice flips/permutation.  Its converse is not asserted.  In
particular, absence of a non-`T` collision for this signature is not by itself
a complete stochastic-atlas theorem.

The selected-completion audit is a separate layer. It derives the five
contracted directed cores and their minimum repairs from these primitive
graphs, preserves both the dummy-repair failure and the later intrinsic-`S_TC`
semantic overclaim, and regenerates exact core-retention bucket changes for
three through six selected outgoing ports. Its rows are completion-target
presentations, not complete decorated source-target relations.

## Replay

```sh
python3 build_atlas.py --ports 4 5 6 7 --output certificates
python3 verify_contract.py certificates
python3 mutation_tests.py certificates --fixture-port-count 4 --output mutation_transcript_p4.json
python3 mutation_tests.py certificates --fixture-port-count 7 --output mutation_transcript_p7.json
python3 verify_contract.py certificates --regenerate
```

For a quick smoke replay use `--ports 4 5`.

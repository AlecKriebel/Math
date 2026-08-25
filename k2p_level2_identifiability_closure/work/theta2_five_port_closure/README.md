# Primitive theta2 five-port K2P closure

This directory is the graph-derived, fail-closed closure of the missing
five-port `theta2` primitive source gate.  It does not read the frozen
four-port descriptor or rank pickles.

The generator enumerates all four minimum repairs, 6,138 target completions,
and 120 physical port permutations: 2,946,240 raw directed presentations.
Every raw presentation is assigned exactly once to a pointwise topology
exclusion, an exact rank exclusion, an exact quadratic separation, or a
labelled semi-directed isomorphism.

The 80 raw isomorphism presentations are not all treated as physical
terminals.  Exactly 24 have no target dummy role.  The other 56 are expanded
under the fixed-full restoration theorem to all 576 six-port children and,
for the 32 surviving isomorphic continuations, all 288 seven-port children.
Every physical path ends in a pointwise displayed-quartet separation or an
exact full labelled semi-directed isomorphism.

## Reproduction

From the repository root, using the referee environment:

```sh
.venv/bin/python -B work/theta2_five_port_closure/generate_theta2_ledger.py
.venv/bin/python -B work/theta2_five_port_closure/verify_theta2_ledger.py --quick
.venv/bin/python -B work/theta2_five_port_closure/verify_theta2_ledger.py
.venv/bin/python -B work/theta2_five_port_closure/test_mutations.py
```

The default verifier performs a fresh-path regeneration.  The frozen evidence
is bound to the legacy compiler and canonicalizer hashes printed in its rank,
restoration, and summary records.  The verifier requires those legacy bindings
exactly, changes only those provenance fields to the locked current compiler
and canonicalizer, deterministically reconstructs the two affected gzip files
and their summary metadata, and then compares the fresh run byte-for-byte.
Every other generated artifact must remain byte-identical to the frozen file.
The quick mode checks hashes, schemas, every raw ID, every class membership,
certificate references, the symbolic tree--sunlet identity, and the complete
restoration path grammar.  Both generator and verifier reject optimized
Python mode because assertions are load-bearing in the imported compiler.

Generated files are under `artifacts/`:

- `raw_directional_ledger.jsonl.gz`: all 2,946,240 raw presentations;
- `exact_rank_certificates.json.gz`: 120 exact lower-and-upper rank proofs;
- `class_partition.json.gz`: all 480 source-indexed survivor classes and raw
  transports;
- `direct_proof_certificates.json.gz`: topology witnesses, 96 exact
  quadratics, 32 base mixed-vertex isomorphism maps, and the explicit 80-raw
  anchor table;
- `fixed_full_restoration_closure.json.gz`: 56 roots, 864 physical child
  paths, exact transports, canonical relation classes, and full isomorphism
  maps;
- `theta2_five_port_summary.json`: claim scope, censuses, and hashes;
- `mutation_report.json`: adversarial rejection report.

The exact mathematical claim and its boundary are stated in `PROOF.md`.

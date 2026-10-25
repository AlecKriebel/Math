# K2P three-port cycle fixed-full closure

This directory closes the dummy-bearing primitive cycle roots that are not
covered by the no-dummy three-sunlet gate.  It is generated from the primitive
graph grammar and contains a complete directional ledger, exact topology and
quadratic certificates, explicit labelled transports, an independently coded
full replay, and fail-closed mutations.

## Certified census

- Base raw directions: **13,440**.
  - 7,452 strict tree/sunlet exclusions;
  - 5,964 fixed-full restoration roots;
  - 8 no-dummy labelled isomorphisms;
  - 16 no-dummy ordinary triangle relations.
- Physical completions of all 5,964 roots: **536,364**.
  - 535,920 displayed-quartet exclusions;
  - 300 strict tree/sunlet exclusions;
  - 132 exact quadratic directional exclusions;
  - 12 labelled isomorphisms;
  - zero unresolved.
- The 132 quadratic rows form exactly **54 descriptor-pair classes**, with
  42 classes represented twice and 12 represented four times.
- Physical probe anchors: 24 base terminals plus 12 restored isomorphisms,
  each with a unique exact labelled transport.

The theorem and its fixed-full logic are stated in `PROOF.md`.  In particular,
this package does not infer a child relation from an abstract selected parent.
It fixes one putative full containment first and enumerates the actual physical
positions of all omitted labels in those same two networks.

## Replay

From the repository root:

```sh
PYTHONHASHSEED=0 .venv/bin/python -B \
  work/cycle_three_port_closure/generate_cycle_closure.py

PYTHONHASHSEED=0 .venv/bin/python -B \
  work/cycle_three_port_closure/verify_cycle_closure.py

.venv/bin/python -B work/cycle_three_port_closure/test_mutations.py
```

On the reference M1 MacBook Pro, generation and independent verification each
take about 1.5--2 minutes.  The compressed artifact directory is about 6 MB;
the 536,364-row full ledger expands to about 229 MB and is always streamed.
The mutation suite also performs a complete replay under `python -O`.

## Files

- `generate_cycle_closure.py`: primary graph-derived generator.
- `verify_cycle_closure.py`: independently written fail-closed regeneration.
- `cycle_common.py`: byte-stable serialization and exact graph utilities.
- `test_mutations.py`: omission, role, placement, certificate, transport, and
  optimized-mode tests.
- `artifacts/base_raw_ledger.jsonl.gz`: all 13,440 base directions.
- `artifacts/restoration_roots.jsonl.gz`: all 5,964 physical roots.
- `artifacts/full_completion_ledger.jsonl.gz`: all 536,364 full completions.
- `artifacts/quadratic_certificates.json`: the 54 exact degree-two classes.
- `artifacts/topology_witnesses.json`: pointwise topology witnesses.
- `artifacts/transport_certificates.json`: exact terminal transports.
- `artifacts/physical_anchors.json`: all 36 physical anchor presentations.
- `mutation_certificate.json`: fail-closed mutation and `-O` replay result.

All certificate identifiers are structural and independent of Python hash-set
iteration order.

# Independent spot checks

These checks rerun seven referee-owned derivation/test families against the
fourth-revision sealed payload without importing reviewed-package modules.
They cover the physical domains, tree--sunlet and triangle geometry, bridge
gauges and capped gluing, representative four-port witnesses, full
restoration/probe censuses plus semantic samples, the Krawczyk/rank boxes and
cherry inverse, and the revised cut derivation. They are bounded checks, not a
substitute for the package's exhaustive producer/verifier graph.

The executed suite used the already-frozen scripts at the absolute paths
recorded in `results/fresh_spots_20260829_fourth/SUITE_REPORT.json`.  Exact
byte copies are retained in `frozen/`; their SHA-256 values equal the hashes
recorded by the execution report, making the referee-owned implementation
self-contained in this audit folder.

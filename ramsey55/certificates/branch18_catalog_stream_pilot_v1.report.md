# Branch-18 streamed catalog pilot

Date: 2026-07-23 (America/Los_Angeles)

**REPRODUCIBLE COMPUTATIONAL OBSERVATION; NO NEGATIVE CLAIM.**

The complete `R(4,5,24)` catalog was streamed from its audited source without
being retained on disk. The stream contained exactly 352,366 records and
16,913,568 bytes, with SHA-256
`83ca4028f206b2fa4315ef219b8c2c57c7835209673dd8183d8fb4353bd4fdd0`.

For each edge count in
`116,119,122,124,127,129,131,132`, the first record in stream order was
selected. Each graph supplied an exact branch-18 cube:

- vertex 0's 42 incident primary variables fixed its degree to 18;
- the 276 variables inside its 24-vertex antineighbourhood fixed the
  complement of the selected `R(4,5,24)` graph;
- 585 primary variables remained unfixed.

One persistent CaDiCaL 1.9.5 instance was loaded with the audited 65,403
variable, 2,052,132 clause base formula. Every 318-assumption cube received a
50,000-conflict constructive budget. All eight returned
`BUDGET_EXHAUSTED`; none returned SAT or observational UNSAT.

The sample used catalog lines
`37900,264,18,1,5,4372,46204,297776`, respectively. Per-cube wall times
ranged from 4.10 to 11.87 seconds. Peak resident memory was 2,434,547,712
bytes. No proof or catalog artifact was written.

This benchmark shows that the exact catalog decomposition is technically
streamable at low storage cost, but a naïve 50,000-conflict pass does not
quickly terminate these sample cubes. It gives no evidence for nonexistence
in any cube or in branch 18.

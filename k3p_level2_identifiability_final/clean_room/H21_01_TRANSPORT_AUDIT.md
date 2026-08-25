# Hardened H21 and Fourteen-Orbit Clean-Room Audit

Audit timestamp: 2026-08-24 22:39 PDT
Status: **PASS within this component's stated scope**
Global K3P theorem status: **not asserted by this component alone**

## Outcome

The H21 transport repair remains mathematically valid, and the two
certification defects found by the adversarial audit are now closed.

- The corrected verifier contains zero Python `assert` nodes. Every
  load-bearing condition uses an explicit, non-optimizable terminal check.
- Optimized Python is refused immediately at import, before any input is read.
- All five active frozen inputs are bound to fixed SHA-256 values before JSON
  parsing; the old read-and-reread tautology is gone.
- `port_permutation`, `source_incoming_role`, and `target_incoming_role` are
  reconstructed and bound to the graph presentation.
- All 38 raw-member Fourier coordinate transports are replayed, not only the
  fourteen representatives.
- Each rank label is bound to a square minor of the same size, to the selected
  observable set and coordinate labels, and to valid parameter columns.
- The five target rank upper bounds are independently reconstructed from the
  target parameterizations. No target upper-bound integer is accepted on
  trust.

The historical verifier is preserved byte-for-byte at SHA-256
`ee5e29a2cd795d9389e8e1257ebdb9eeaa4256fb5d03e07f230bf82ba555ef91`.
Its original H21-01 failure is still reproduced exactly. The historical defect
remains the use of rooted-DAG automorphisms instead of root-suppressed
semi-directed mixed automorphisms, together with failure to conjugate a base
target automorphism into the displayed frame.

## Independently reconstructed target upper bounds

| Orbit | Source minor | Target minor | Target upper bound | Exact mechanism |
|---|---:|---:|---:|---|
| `H21-02` | 11 | 10 | 10 | Ten rational generators `U,V,Z,D,I,A0,B0,A,B,rho`; eleven exact cross-multiplied identities on the dense open set `e2C*e2G*D*I != 0` |
| `L20-02` | 14 | 12 | 12 | Exact ordinary three-sunlet marginal compression to twelve generators |
| `L21a-02` | 11 | 10 | 10 | Selected sunlet projection uses ten generators; `A_G,B_G` are absent |
| `L21b-02` | 11 | 10 | 10 | Selected sunlet projection uses ten generators; `A_G,B_G` are absent |
| `L23-01` | 14 | 12 | 12 | Exact ordinary three-sunlet marginal compression to twelve generators |

For H21-02, the verifier constructs all ten generators directly from the
independently compiled target parameters. The rational generator `rho` is
represented as the exact pair `e2C/e2G`; the coordinate formulas are verified
by cross-multiplication, including the declared saturation factors. For each
sunlet case, all edge-class collapses and the surviving inheritance variable
are reconstructed, then the compressed map is matched against every edge,
inheritance-parent, and three-port permutation of the canonical ordinary
sunlet map. The actually used generator set is derived from the selected
coordinates and compared with the frozen generator names.

## Exact replay census

The mandatory gate verifies:

- 6 source supports;
- 831 selected-incoming and 1,983 dummy-incoming target completions;
- 14 canonical orbits and all 38 raw members;
- the complete seven-coset H21 partition, with the unique isomorphic coset
  omitted from the six nonisomorphic records;
- 2 pre-lock sink-swap separators;
- 5 transported H14 quartics and 4 remaining exact quartics;
- 5 exact directed-rank source/target minors and 5 reconstructed target upper
  bounds; and
- exact, disjoint coverage of all fourteen orbit IDs.

## Mutation campaign

Nine mutations were rejected and none was accepted:

1. changed `port_permutation`;
2. changed `target_incoming_role`;
3. weakened a target rank claim;
4. weakened a target dimension upper-bound claim;
5. changed H21-02 to the former `101 > 100 = 100` labels while retaining the
   original minors;
6. made the target minor nonsquare;
7. changed the selected observable set;
8. ran the verifier under optimized Python; and
9. changed one byte of an active certificate input.

Two positive controls also passed: an AST scan found zero `Assert` nodes in the
corrected verifier, and the historical verifier retained its exact fixed hash.
The deterministic record is `CLEAN_ROOM_MUTATION_RESULTS.json` at SHA-256
`5544969046337b3f5adcbfaf698bde34908f1f5c971597dc79a7fbad7a65297c`.

## Mandatory replay

Run:

```text
clean_room/verify_clean_room.sh
```

The measured checkpoint on the M1 MacBook Pro was:

```text
historical replay                 0.09 s
corrected fourteen-orbit replay  1.73 s
transport regression replay      1.80 s
mutation suite                    2.77 s
total mandatory runner            6.50 s
peak RSS                         96,256,000 bytes
CLEAN_ROOM_FULL_GATE_PASS
```

Artifact hashes at this checkpoint:

```text
becacec117734248047cded6f84d5996ad91c7531be36b1d8db8eec57653740b  verify_h21_transport_and_fourteen_orbits.py
aa3a97442854d7df8b6d4b3bfa02e9f2d18d4eaa4a0838fdd33738e00ea6a063  test_h21_transport_regression.py
114b7d7e4a694e7b8bfaca212bf45846b034e6b22b6b95c0c0fe3a4314eec2a8  test_clean_room_mutations.py
5544969046337b3f5adcbfaf698bde34908f1f5c971597dc79a7fbad7a65297c  CLEAN_ROOM_MUTATION_RESULTS.json
ea76278d7fac941726b00c137408b8874ff0aeed56bb17b33bfa05c3a2d80857  verify_clean_room.sh
```

There is no remaining gap within the H21/fourteen-orbit clean-room scope. This
component deliberately does not claim that unrelated topology, cut-recovery,
probe, gluing, manuscript, or release gates have passed.

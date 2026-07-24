# Certificates

No global UNSAT certificate exists in this repository.

## Certified fixed-core result

`exoo42_extension_sat.report.md` records a certified one-vertex-extension
UNSAT result for `data/exoo42_constructed.g6`.

- CNF: 42 variables, 2,318 clauses, SHA-256
  `ff372bd968015eb1ee027459679ba2528d0a8c566034e51f37d3f9671bb78160`
- Explicit-unit proof SHA-256:
  `e30cf3871b12322f3627ab1115d66b72078fc52d0fa30f0036ab9668f624bf66`
- Compact independently replayed proof SHA-256:
  `fd8c5e9886c77ae83d604d34a35e11f7c8bde91215719dc627f95daa6e14c232`

Both proof formats encode complete DPLL trees. The compact checker independently
decodes graph6, reconstructs all original clauses, performs original-clause
unit propagation, and checks both children at every branch.

## Certified \(k=1\) replacement family

`core_completion_all42/` contains deterministic CNFs and checked proof trees
for all 42 ways to delete one vertex from Exoo42 and add two new vertices while
preserving the remaining 41-vertex induced core.

- 42 UNSAT, 0 SAT, 0 timeouts
- 83 variables per instance
- 6,652–6,702 clauses per instance
- 104,058 total checked proof records
- generator summary SHA-256:
  `37f277e236e1f31cec6327eb279f6bccafbdafd32b85b9809fa5735d3e92493b`
- checker summary SHA-256:
  `6b1c1caa25ddf546c104aff20bd5856f23b340dda5c6924e961fc0e8a42051e4`
- independent CNF-set check summary SHA-256:
  `88a9b61872192a083e0068011919ea882b83e53bc4455e2f9cb31f9278b44326`
- coverage-enforcing proof recheck SHA-256:
  `2e54833a541382f894c16d92b493bb40434cbbe661ac42ab77ada3b38443e14e`
- coverage-enforcing formula recheck SHA-256:
  `2e31e66986bfcdce5607983b415c27d198075e0b1556614a97c6c067d0b6c5a8`

No symmetry reduction was used. Each result is scoped to its explicitly
recorded fixed 41-vertex core.

## Certified first \(k=2\) benchmark

`core_completion_k2_delete_00_01.report.md` records the checked UNSAT result
for the fixed 40-vertex core obtained by deleting original vertices 0 and 1
and adding three new vertices.

- 123 variables and 13,338 clauses
- CNF SHA-256:
  `d0678b8c71edeaa5a9e3e99170d6d35fb655a1da2873355eda4116208d03488c`
- checked tree SHA-256:
  `a469ea000c190c7b639a819ffdaec81a191ba5f2f037a86fbe4f814ba03887a0`
- 19,734 proof records accepted
- independent direct five-subset reconstruction: 13,338 matching clauses,
  zero missing, zero extra

This covers one fixed core only. The other 860 two-vertex deletion pairs were
not run.

## Certified residual-focused fixed-boundary neighborhoods

`residual_lns_report.md` and `residual_lns_boundary_expansion_report.md`
record four checked UNSAT neighborhoods around the current \(E=2\) candidate:

- 19 free edges, 356 clauses, 17 checked proof records
- 66 free edges, 4,868 clauses, 47 checked proof records
- 80 free edges, 5,408 clauses, 77 checked proof records
- 86 free edges, 5,775 clauses, 83 checked proof records

The independent checker directly reconstructed all formulas from the base
graph and exact free-edge lists, with zero missing or extra clauses. All
unlisted edges were fixed. These certificates do not prove unrestricted local
or global nonexistence.

## Certified incident neighborhoods

The first 60-second attempt recorded in
`residual_lns_incident_six.report.md` timed out, but a later proof-producing
solver run closed the same byte-identical 237-variable formula.

- Original \(E=2\) base, residual union
  \(\{3,4,7,38,41,42\}\): 49,461 clauses, certified UNSAT.
  - CNF SHA-256:
    `bfa9d9e3edea9a5ac332614fc76984c9d287b1e8bf39d282199a09aab2b9c014`
  - DRAT SHA-256:
    `e7c8da6188c304e79ca2ca9bc077d261ed7536b3e4b3ec1181bebb006547c654`
  - LRAT SHA-256:
    `592d2ce4df932c6332af5b2523b4fbaaf6d394d14aa639c74b303f1bf1195209`
- Constructive-search \(E=2\) base, residual union
  \(\{2,4,24,25,26,42\}\): 49,677 clauses, certified UNSAT.
  - CNF SHA-256:
    `e470ed2a4a1fe316b8cce77ab2e3f1c4f6ceb9d57b37e1e076f780e77a919867`
  - DRAT SHA-256:
    `bb7cdeecfaabdddd96117d1bd3463cf5699ffd84959787d5fdcd55d18423bb70`
  - LRAT SHA-256:
    `df22449c12fcb20fb2140a1fa3f8ffe3f10bc4716c957e10b4518a0de821c5c3`

For both formulas, `drat-trim` accepted the DRAT trace and generated an LRAT
proof accepted by `lrat-check`. The exact commands, transcripts, and
toolchain hashes are in `residual_completion_workflow.report.md` and
`residual_lns_incident_alt_six.report.md`. Both conclusions fix the other
666 graph edges and are not global nonexistence results.

## Certified aggregate core radius six

`residual_completion_workflow.report.md` also records the stronger aggregate
statement around the original \(E=2\) base:

- all 237 edges incident to \(\{3,4,7,38,41,42\}\) are unrestricted;
- at most six of the remaining 666 core edges may differ from the base.

The resulting direct Ramsey-plus-counter formula has 5,544 variables and
1,934,472 clauses and is certified UNSAT. An independent checker rebuilt
every clause, and adversarial metadata tests fail closed.

The retained Zstandard-compressed DRAT is
`core_radius6_glucose3.drat.zst`, 68,702,255 bytes, SHA-256
`0fbd59057b014662a8aa1030c18616836ccfa98734a36bcd11a9195c4042b418`.
It passes `zstd -t` and decompresses to the checked raw proof SHA-256
`1bfc9fc9f8df0b042a3df72e0c422b84c914eb46cc216811b6c9abc147c67e26`.
The checked LRAT is regenerated from that DRAT using the pinned tools.

This proves a radius-six exclusion relative to one labeled core, not
unrestricted order-43 UNSAT. A valid graph in this labeled framework would
have to change at least seven of those 666 core edges.

## First proof-guided radius-seven cut

`residual_lns_incident_six_plus_core_top7.report.md` records the first
preregistered experiment on the next admissible shell. It frees all 237
original boundary edges plus the seven highest occurrence-ranked core edges
from the independently reproduced DRAT input core.

- 244 variables and 52,148 independently reconstructed clauses
- CNF SHA-256:
  `cfbf69f7bb7646235ba195dae92aae38532ee7d869ef4f1b653c074c05cd4b42`
- DRAT SHA-256:
  `c1f75abad12de12f2db0e8fa30d3840320f54212a20679f22f42b1f5228ffeae`
- LRAT SHA-256:
  `8e4c2ed3f44a55ee205a97015ac9d8a1d405927747bb4b97ffa22b9b9f1d07cc`

Both proof checkers returned `VERIFIED`. This closes one selected
seven-core-edge cut while fixing the other 659 core edges; it does not close
the full radius-seven shell.

The aggregate radius-seven formula has 6,203 variables and 1,935,789
independently matched clauses, but its strict 120-second Glucose3 replay
returned `TIMEOUT`. `core_radius7_glucose3.timeout.json` correctly records no
proof and no LRAT. Exact commands and hashes are in
`core_radius7.report.md`. This is neither SAT nor UNSAT.

## Direct unrestricted \(n=43\) instance

`direct_ramsey43_generation.report.md` records the generated and independently
reconstructed global edge-variable CNF:

- 65,403 variables
- 2,052,132 clauses
- 90,311,307 bytes
- CNF SHA-256:
  `141de0a9714fb40e100508031b37fa555bf2fbdefd13c2dee4c04141c159bcb1`

This certifies the encoding artifact only. It has not been solved.

An UNSAT claim will require:

1. deterministic instance generation,
2. solver/version/options and exact command,
3. DRAT, LRAT, or comparable proof,
4. independent checker output,
5. instance and proof hashes, and
6. a human-readable encoding equivalence proof.

## Certified prime-order automorphism cycle types

`prime_automorphism_cycle_type_exclusions.report.md` records three new
complete cycle-type exclusions:

- \(19^2 1^5\): 57 variables and 95,752 clauses;
- \(17^2 1^9\): 87 variables and 106,800 clauses;
- \(11^3 1^{10}\): 123 variables and 172,110 clauses.

Each exact orbit CNF was independently reconstructed clause-for-clause. Each
Glucose3 DRAT proof passed `drat-trim`, and each derived LRAT passed
`lrat-check`. No added symmetry-breaking clauses or degree lemmas occur in
these three formulas.

The same report gives checked elementary exclusions for
\(23^1 1^{20}\), \(29^1 1^{14}\), \(31^1 1^{12}\),
\(37^1 1^6\), \(41^1 1^2\), and \(13^3 1^4\). Together with the
existing certified \(43^1\) circulant exclusion, this covers every
prime-order cycle type with prime at least 23.

The machine-readable audit is
`results/verification/prime_automorphism_cycle_type_coverage_v1.json`.
It deliberately reports `classification_complete: false` and lists all 54
uncovered lower-prime cycle types. These results do not prove that a
hypothetical order-43 Ramsey graph is asymmetric.

## Certified E=2 isomorphism collapse

`e2_near_miss_isomorphism_collapse_v1.report.md` classifies the fixed corpus
of 22 exact E=2 near misses. Nauty 2.9.3 dense and sparse labeling agree on
three isomorphism classes and two classes modulo complement.

Deleting any vertex in the four-vertex intersection of the two conflicts
gives a valid order-42 Ramsey graph. All 88 resulting deletions pass direct
all-five-subset and independent recursive-bitset checks. They reduce to two
classes modulo complement, both already represented by lines 42 and 256 of
the supplied catalog. This is an exact finite-corpus result, not a global
classification or nonexistence proof.

`catalog42_lines42_256_exact_e2_extensions.report.md` strengthens the basin
description in the fixed-core direction. For each labeled catalog core 42
and 256, exactly two of all \(2^{42}\) new-vertex neighborhoods have at most
two conflicts, and both have exactly two. Independent formula reconstruction
and checked DRAT/LRAT proofs establish completeness. This remains a
two-fixed-core statement.

`catalog42_all328_e2_extension_screen.report.md` extends that fixed-catalog
analysis to every supplied core. Exactly lines 42 and 256 are satisfiable at
the \(E\le2\) threshold. The other 326 formulas have retained DRAT proofs,
each accepted against its independently reconstructed CNF by pinned
`drat-trim`; the two SAT models passed exhaustive order-43 five-set checks.
The result manifest records every formula/proof hash and terminal status.
Together with the two-core exact enumeration, this makes the four recorded
neighborhoods the complete \(E\le2\) extension set across this 328-graph
catalog.

Every fixed-core UNSAT certificate here applies only to its explicitly
identified core and is not a proof that no \((5,5;43)\)-graph exists.

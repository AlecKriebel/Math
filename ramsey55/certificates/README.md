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

## Incident-neighborhood timeout

`residual_lns_incident_six.report.md` records the exact 237-variable formula
that frees every edge incident to the six residual-conflict vertices. The
formula was independently reconstructed, but its bounded solve returned
`TIMEOUT` at 60 seconds. No proof exists and no SAT/UNSAT claim is made.

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

Every fixed-core UNSAT certificate here applies only to its explicitly
identified core and is not a proof that no \((5,5;43)\)-graph exists.

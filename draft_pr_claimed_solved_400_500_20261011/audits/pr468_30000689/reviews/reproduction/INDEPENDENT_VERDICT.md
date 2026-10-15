# PR468 / problem 30000689: independent finite reproduction audit

Date: 2026-10-12 UTC. Assigned reproduction audit completion: **100%**.
This completion percentage concerns the reproduction assignment, not resolution
of the open problem. No newly commissioned review was read before this verdict.

**Verdict: finite computations PASS; the original verification programs need
the supplied runtime-check hardening for robust distribution.** All recorded
outputs reproduce exactly. Independently reformulated controls agree with the
recorded finite examples and with an additional bistellar sequence. No finite
counterexample was found. This is not a verdict on the universal proof, source
theorems, category transitions, novelty, priority, or preprint readiness.

## Integrity and reproduction

The two frozen checker programs were inspected before execution. They use the
Python standard library, have no network operations or file writes, and send
their results to stdout. The author program is deterministic. The prior audit
uses an explicitly seeded pseudorandom sequence with fixed integer-labelled
face sets and floating-point selection weights.

All **24 hash/byte-size manifest entries** match, covering the published payload
and the frozen author/prior-audit manifests. All **15 distinct frozen files**
were fingerprinted before and after the work and remain byte-identical.
Manifest integrity is internal consistency, not evidence of mathematical truth
or independent provenance.

Both scripts run successfully in ordinary Python and with `-O`; each stdout is
byte-identical to its recorded result file. The author stdout SHA256 is
`2e82d4e60eaebd950b5f1763cbe0854f88f244a4dab34de395bb1124e61936a4`.
The prior-audit stdout SHA256 is
`455b2a632604159a9abf35d3e62091740808d2cd101b24d568f81fc7c7d9b1f7`.
Commands, Python version, output hashes and execution times are recorded in
`reproduction_results.json`. Byte reproduction was checked directly, not merely
by parsing the expected JSON and re-serializing it.

## Exact finite scope of the frozen controls

| Control | What is actually checked |
| --- | --- |
| Stellar examples | Four explicit stellar subdivisions, d=1,2,3,4; the designated missing face, its codimension-one boundary, completion of the d-skeleton, face counts and h-vector symmetry |
| Quotient dimensions | Four dense-graded quotient dimensions for each of d=1,2, using Vandermonde parameters over the finite field F101; eight ranks total |
| Flores cycles | Deleted-product mod-2 cycle closure and moment-curve intersection parity for the full d-skeleton on 2d+3 vertices, d=1,2,3,4; 15,70,315,1386 top cells |
| Flag control | One barycentric face-poset model, d=2: 104 nonempty-face vertices and 3084 comparable triple cliques |
| Metastable bound | Arithmetic comparison 4d>=3d+3 for integers d=1,...,8; the external embedding theorem is not verified by this comparison |
| Prior audit move walk | 100 bistellar transitions from the boundary of a 5-simplex, seed 49830000689; all p=0,...,4 types occur, with counts 9,20,28,30,13 |
| Prior audit complements | 3542 local cone/complement tests of reduced H0 and H1 over F2; these homology checks do not certify contractibility or integral acyclicity |
| Prior audit missing faces | 824 persistent missing-triangle checks, 28 p=q=2 augmentation identities, and 70 p=3,q=1 deleted-product chain witnesses with odd pairing |

The computations test particular finite complexes obtained by valid combinatorial
moves. They do not recognize arbitrary topological spheres, distinguish exotic
PL structures, verify low-dimensional manifold facts, establish a universal
van Kampen obstruction, or infer characteristic-zero/generic algebraic results
from ranks at particular finite primes.

## Optimization defect and its repair

The author script has **9** removable `assert` statements and the prior-audit
script has **18**. Python with `-O` removes every one. Nine mutations of actual
computed mathematics were tested:

- Retain the designated missing face in the source complex.
- Zero the Vandermonde relation coefficients.
- Increase the returned modular rank by one.
- Suppress all author moment-curve crossings.
- Treat every triple of barycentric vertices as comparable.
- Return empty filling chains from the prior audit.
- Increase the computed complement reduced H0 by one.
- Suppress all prior-audit witness crossings.
- Replace the computed paired-boundary triangles by the empty set.

Every mutation is rejected in ordinary Python. **Every mutation exits successfully
with `-O`.** These are actual altered constructions/calculations, not just changed
expected constants. The last paired-boundary mutation can preserve the entire
recorded stdout under `-O`, so comparing aggregate JSON alone does not detect it.
Several output fields are hard-coded affirmative summaries after assertions:
for example the author's cycle reports evaluation one even when a mutation has
computed zero crossings. An optimized success exit therefore has no reliable
verification meaning in the originals.

Separate copies in `hardened/` replace all 27 assertions with explicit calls to
`require`, which raises `RuntimeError` on a false condition. Each original
condition and its evaluation order are preserved; no frozen file was changed.
Both hardened programs reproduce the recorded bytes normally and optimized.
All **18** hardened mutation executions (nine faults, two modes) reject through
the intended finite mathematical condition. The failure messages are captured.

- Hardened author checker SHA256:
  `0002aaabc31a551f138c38bcd7e8d126befc50338deef75bdbf54451f11a7cce`.
- Hardened prior-audit checker SHA256:
  `ac9cd205f24bed1ed80a83d826b107c2f6bb21a7360033c320daa58b304254e8`.

This repair makes the existing conditions durable. It does not turn these finite
conditions into a proof verifier or certify their universal sufficiency.
`hardening_results.json` and the two patches record the repair.

## Independently formulated controls

`check_bitmask_controls.py` imports neither frozen script. It reconstructs the
finite examples using different data structures and calculations:

- Direct bitmask face membership for the stellar subdivision, instead of
  generating replacement facets and closing them under subsets.
- Exponent-vector monomials and dense modular Gaussian elimination, instead of
  combinations-with-replacement monomials and sparse row reduction. All eight
  original quotient dimensions agree over each of F7, F101 and F103: **24 rank
  computations**, including the +1 augmented dimension jump.
- Rational moment-curve affine dependence coefficients
  c_i=1/product_{j!=i}(t_i-t_j). Every circuit verifies the exact power-sum
  identities through the ambient dimension. Intersections are read from the
  positive/negative circuit supports rather than testing alternating positions.
- Graph breadth-first paths for one-dimensional fillings and dense augmented
  boundary-equation reduction for triangle fillings, with explicit rechecking
  of each returned triangle-chain boundary.
- A separately seeded 100-transition bistellar sequence. All five move types
  occur, with counts **9,20,30,28,13**. It checks **3548** complements,
  **580** persistent missing triangles, **30** middle-move augmentation
  identities and **52** explicit transferred deleted-product cycle witnesses.
  Every witness has the prescribed missing-face pairing and odd intersection
  evaluation. Across both families, **251** rational circuit unions are checked.

All four stellar face/h-vectors, Flores cell counts/crossing counts, and the
barycentric triple-chain count agree with the frozen outputs. The independent
normal and optimized runs have identical output bytes.

The small F2 rank routine was separately checked against enumeration of the
entire image for every 2x3 and 3x3 F2 matrix: **576 matrices**. A disconnected
path request and an unfillable triangle-boundary request both reject. Six actual
faults in this independent program (missing face retained, wrong rank, wrong
rational coefficient, empty triangle filling, empty mapped product chain,
wrong complement Betti number) reject in both modes: **12 executions**.
The captured failures identify the intended condition rather than syntax or
import errors. See `bitmask_results.json` and
`bitmask_verification_results.json`.

## Distribution recommendation and remaining boundary

If a verification package is prepared, preserve the historical frozen files and
their manifests, distribute the hardened programs as separately identified
versions, include their patches, and document that the outputs are finite
consistency evidence only. The independent bitmask program may be included as an
additional control. Its scope statement must remain visible.

The `mutation_fixtures/` directory contains intentionally false computations and
must not be distributed as result-bearing verification scripts. Failure logs
and mutation-test descriptions may be included if labelled as negative controls.
No queue, PR, git index, shared branch, remote repository, publication service,
or external communication was changed by this audit.

The strongest result verified here is reproducibility and independent agreement
of the specified finite controls, plus durable rejection of the tested faults.
The exact remaining gap is the full universal proof and its source/category/
priority review, assigned elsewhere. Nothing in this report closes that gap.

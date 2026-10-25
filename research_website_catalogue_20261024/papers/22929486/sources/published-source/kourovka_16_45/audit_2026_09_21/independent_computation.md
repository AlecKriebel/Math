# Independent finite computational verification

Checkpoint: 2026-09-22 04:07 UTC (2026-09-21 local project date). Completion of the assigned finite-verification scope: **100%**. All exact checks pass; no finite counterexample to a manuscript assertion was found.

## Independence and claim

The audit script `independent_check.py` was written from `proof.tex` before reading any bundled verification implementation. It uses only Python's standard library, exact modular integer arithmetic, and fresh matrix and affine group generation. It does not load any archived table, reported invariant, solver output, or supplied subgroup list. The only inputs are the explicit matrices and witnesses printed in the manuscript. After the independent implementation passed, the supplied `make verify` pipeline was run and its output retained in `supplied_make_verify.log`.

The falsifiable finite claim was that the specified matrices and subgroup witnesses have the orders, intersections, and irredundancy properties claimed, and that the complete complement subgroup lattice certifies the indicated complement invariants. The universal upper bound for every action of the affine group is a structural theorem; this audit does not claim to enumerate the full affine subgroup lattice or to establish publication priority.

## Results

- The two generators over the field of 29 elements generate exactly 120 determinant-one matrices, and satisfy A² = B³ = (AB)⁵ = −I.
- Simultaneous generator closure constructs the claimed isomorphism from SL₂(5); all 14,400 products are checked. A separately constructed permutation quotient has image of order 60, kernel {I,−I}, and all 14,400 products checked.
- An extension search enumerates all **76 actual subgroups**, with subgroup-order distribution 1:1, 2:1, 3:10, 4:15, 5:6, 6:10, 8:5, 10:6, 12:10, 20:6, 24:5, 120:1. Starting with the identity subgroup, every element outside every discovered subgroup is adjoined; each subgroup is therefore reached along one of its finite generating sequences. This is a completeness argument, not a count based on a catalogue.
- All **1,215,450** four-member families of proper subgroups are checked. None is meet-irredundant. All **67,525** three-member families are checked; precisely 900 are irredundant, all have normal bottom, and none has trivial bottom. An irredundant larger family would contain an irredundant four-member subfamily. Including the whole group cannot yield an irredundant nonempty family. Together with the explicit witnesses, these facts certify μ′(H) = b(H) = 3 and b_f(H) = 2.
- There is exactly one involution. Every even-order subgroup contains {I,−I}; every odd-order subgroup has order 1, 3, or 5.
- Every one of the **30** line stabilizers has order 4, is cyclic, and acts faithfully on its line. The explicit complement triple generates H and has omission subgroup orders 8, 12, and 20; its common omission intersection is {I,−I}. Each pair subgroup has core {I,−I}.
- Direct affine generation produces **100,920** elements. The independent four-element witness generates the whole group, and omitting its respective elements gives orders **120, 6,728, 10,092, 16,820**. Each omitted element is absent from the corresponding generated subgroup. Their common intersection is exactly the two displayed zero-translation central matrices, and the displayed translation conjugate lies outside that intersection.
- The faithful three-family has subgroup orders **58,58,58**, the exact displayed two-element pairwise intersections, and trivial total intersection. The complement meets its conjugate by the indicated nonzero translation trivially, directly checking the manuscript's core argument at that point.
- The characteristic-11 boundary construction generates a complement of order 120. Its specified four subgroups have orders **110,110,242,605**, trivial common intersection, and deletion intersection orders **11,11,5,2**. Thus the warning that the result does not extend blindly to this characteristic is independently verified.

## Cross-implementation comparison

The supplied Python and C++17 verification pipeline exits successfully. The audit exports every subgroup as a canonical set of actual matrices, with no dependency on implementation-specific numbering. `compare_independent.py` confirms exact set equality with all four independent targets: the archived Python certificate, freshly generated Python certificate, archived C++ export, and freshly generated C++ export. This compares membership, not merely subgroup orders or counts.

The scripts' runtime is recorded for provenance only; timestamps and runtime are intentionally variable. No floating-point optimization, network service, GAP catalogue, or formal proof assistant is required for these checks.

## Reproduction

From the problem folder:

```sh
python3 audit_2026_09_21/independent_check.py
make verify
python3 audit_2026_09_21/compare_independent.py
```

Python must be run without `-O`, because assertions perform the validation. The independent checker writes `independent_check_results.json` and `independent_subgroups.json`. It has no third-party dependencies. The supplied verifier additionally requires a C++17 compiler.

## Exact remaining gap

There is no remaining failed or unperformed finite check within this assigned scope. Mathematical acceptance of b(G) ≤ 3 and μ′(G) ≤ 4 still requires reviewing the structural arguments in the manuscript; the independently verified finite facts are consistent with and sufficient as inputs to those arguments. Novelty and the interpretation of the original problem require separate source review.

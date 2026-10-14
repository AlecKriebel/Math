# Reproducible finite checks

The full replay passed: **21 checks, 51 executions**, with every result matching its frozen expected JSON byte for byte. The assembly replay used Python 3.12.14 and SymPy 1.14.0. This verifies reproducibility of the included finite computations. It is not a new mathematical audit or a proof of the unresolved construction.

## Running the collection

Use Python 3.12 and SymPy 1.14.0 for the recorded environment. The only nonstandard dependency is pinned in requirements.txt. The runner and scripts do not retrieve source documents or use a dataset. From the reader directory run:

    python run_checks.py --optimized --output /tmp/eisenstein-checks.json

To replay only selected checks:

    python run_checks.py --only C15 C16 --optimized

The runner verifies each script and expected-output hash, copies the script to a fresh temporary directory, runs it there, and compares its complete result with checks/Cxx/expected.json. Temporary outputs cannot overwrite frozen evidence or the original proof workspace. Omitting --optimized runs every selected script once normally. If a supplied ID is unknown, a process fails, a pin changes, or result JSON differs, the runner fails explicitly.

Scripts using Python assert run only normally, with PYTHONOPTIMIZE unset. Scripts with explicit runtime checks can also run under -O and -OO. The distinction is recorded in CHECK_INVENTORY.json. Optimization is never presented as meaningful validation for assertion-based scripts.

## What the checks establish

The scripts test exact finite identities, residue-field arithmetic, local and component matrix conventions, finite induced modules, and explicit examples. Written proofs remain necessary for CM descent, source normalization, global projective-module arguments, continuous cohomology, localization, and every imported theorem. No check computes the missing arithmetic K2 cocycle residues, the remaining Gaussian cusp values, arbitrary number-field K2, or the full symbol-to-homology comparison. A formal unsolvable smoothing family in a finite module is not an arithmetic counterexample.

## Check catalogue

### C01 CHECK_TRANSFER_IDENTITY.py

[Script](checks/C01/CHECK_TRANSFER_IDENTITY.py) · [Frozen output](checks/C01/expected.json)

19 finite group/subgroup cases; 1,550 pair checks. General transfer identity is proved in the audit; tests are sanity checks.

Supports: P09, P11. Internal review: A4.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `3cd2278974f88b1c9e76642a6caebbd149420278fb20f45528f035115e39327a`.

### C02 CHECK_EXAMPLES.py

[Script](checks/C02/CHECK_EXAMPLES.py) · [Frozen output](checks/C02/expected.json)

Four exact residue examples, reduced forms at discriminant -23, and a retained p-group action example. No actual cocycle values.

Supports: P12. Internal review: A6.
Replay modes: normal. Dependencies: Python standard library.
Script SHA-256: `87a9f44a2948114b6c4434373e1ce720fe83d4cf02f924a13eb6604795142584`.

### C03 check_matrix_identities.py

[Script](checks/C03/check_matrix_identities.py) · [Frozen output](checks/C03/expected.json)

825 samples; 3,450 bad-coset/first-degeneracy, 550 higher-depth, 275 missing-branch and 1,425 good-coset equations. Local matrix checks do not prove global fractional-ideal membership or K2 values.

Supports: P13. Internal review: A7.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `46f2f50cb5924cfd1886efc5d54273a7e28e2fb750d707bed8196452fee850ae`.

### C04 CHECK_NORMALIZATION_IDENTITIES.py

[Script](checks/C04/CHECK_NORMALIZATION_IDENTITIES.py) · [Frozen output](checks/C04/expected.json)

Exact projector, 287 first-stage and 1,722 residual-defect finite cases. Ordinary Python only; assertions disappear in optimized mode.

Supports: P14. Internal review: A8.
Replay modes: normal. Dependencies: Python standard library.
Script SHA-256: `985c8eaf4889a389f7d91c63e7c3b17ea25d32d6c484c26b1e27c0e7a6a4e9ac`.

### C05 check_unit_ray_square.py

[Script](checks/C05/check_unit_ray_square.py) · [Frozen output](checks/C05/expected.json)

541 CRT quotient models, 460 with nontrivial unit correction. Independently replayed normal, -O and -OO; explicit runtime checks survive optimization.

Supports: P15. Internal review: A9.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `77d423944a238b7d87fed7209562b00af8d30f17e61042017a23a32912181c98`.

### C06 check_exact_theta_residue.py

[Script](checks/C06/check_exact_theta_residue.py) · [Frozen output](checks/C06/expected.json)

Division-polynomial degree/weight, F8 arithmetic, 8 coordinate pairs and 32 eligible SL2(Z/4) matrices. Ordinary Python only. Does not independently compute the Hilbert class polynomial or actual cocycle.

Supports: P16, P17. Internal review: A10.
Replay modes: normal. Dependencies: sympy.
Script SHA-256: `d6cfdf97200ce6711e6a8059af80d09fb52d6eff3ee4a8a26bd6e149116d6728`.

### C07 check_theta_relations.py

[Script](checks/C07/check_theta_relations.py) · [Frozen output](checks/C07/expected.json)

Author checker independently replayed in ordinary Python and matches AUTHOR_CHECK_REPLAY.json; assertions retained. Checks finite theta algebra, not unrestricted roots or geometric calibration.

Supports: P18. Internal review: A11.
Replay modes: normal. Dependencies: Python standard library.
Script SHA-256: `943ebd648fd8c868c3df89a18439f5dfa6c07bf5f00023e0d8cfbd757e01c1c1`.

### C08 check_independent_algebra.py

[Script](checks/C08/check_independent_algebra.py) · [Frozen output](checks/C08/expected.json)

63 quadratic-residue-ring ideal cases, cyclic-seven wedge coefficients and a torsion model demonstrating the rejected cancellation implication. Ordinary and -O recorded with explicit runtime checks.

Supports: P18. Internal review: A11.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `69aaac6f573d2459498fa0fe4e8d9f7a58bccc124129ed1486a3b1ba1f392d3b`.

### C09 check_kernel_incidence.py

[Script](checks/C09/check_kernel_incidence.py) · [Frozen output](checks/C09/expected.json)

Kernel incidence at q=5,25,7; SL2(F5) transfer over 120 group elements and non-Cartesian zero-cycle defect. Ordinary Python replay; uses assertions, no optimized-mode theorem check asserted.

Supports: P19. Internal review: A12.
Replay modes: normal. Dependencies: Python standard library.
Script SHA-256: `bec06c4d20ddcfcd478ad7d10dbc732a351e95ac1e46712b0c509fbd2322a7e8`.

### C10 check_arithmetic_descent.py

[Script](checks/C10/check_arithmetic_descent.py) · [Frozen output](checks/C10/expected.json)

Exact scalar gcd, local norm squares, p-good definition-modulus residues, norm46/smoothing2115, discriminant400 and inert121 ambient support. Ordinary Python replay; uses assertions.

Supports: P20, P21. Internal review: A13.
Replay modes: normal. Dependencies: Python standard library.
Script SHA-256: `00902d4a96733b9944ef84764aecb04cd182c4f523548b83467e7efd0e4eac1d`.

### C11 check_independent_pass4.py

[Script](checks/C11/check_independent_pass4.py) · [Frozen output](checks/C11/expected.json)

Independent incidence at q=2,3,5,7,25; all six SL2(F2) arguments, five nonzero corrections; finite-field constants and inert121 ambient support. Final frozen script has explicit runtime failure checks; normal, -O and -OO replays agree. Structural theorem proofs remain in the written audits.

Supports: P19, P20, P21. Internal review: A12, A13.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `aae70b93d0b182d2070e9dc343bd8a20ebaa0effbb49d08ccc79c011974b980c`.

### C12 CHECK_EXACT_IDENTITIES.py

[Script](checks/C12/CHECK_EXACT_IDENTITIES.py) · [Frozen output](checks/C12/expected.json)

Gersten coefficient expansion, 8 cyclic-four pairs, unit/congruence invariance, 652 finite closed walks, factors576/48/624 and residue exponents. Ordinary, -O and -OO independent replays agree; explicit runtime checks remain active.

Supports: P23, P24. Internal review: A15.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `6b94f1489eba0cd93d8fa7dd7426b3ceab8b2c87b5724d889f3658458d56e88d`.

### C13 check_inverse_component_algebra.py

[Script](checks/C13/check_inverse_component_algebra.py) · [Frozen output](checks/C13/expected.json)

Exact inverse-coset, semilinear, higher-depth, principal scalar and component-permutation algebra. No CM K2 values or global ideal principalization.

Supports: P25, P26, P27. Internal review: A16.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `2b656ad835d35c80eb7eea0533009a377f3a2faa02d2aa7d89c8b4b6cdd88fb2`.

### C14 check_transport_conventions.py

[Script](checks/C14/check_transport_conventions.py) · [Frozen output](checks/C14/expected.json)

Independent transfer, scalar, omitted-branch and class-shift convention checks. No arithmetic K2 values.

Supports: P25, P26, P27. Internal review: A16.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `7ef90533547b2215b23e942a38bdf771501c80a72ae507ae64b6fe0b94a7afd7`.

### C15 CHECK_SYMBOL_ADVANCE.py

[Script](checks/C15/CHECK_SYMBOL_ADVANCE.py) · [Frozen output](checks/C15/expected.json)

Cyclic orders 2 through 15, exact exterior identities, order-seven formal functional, finite content orbits and local/CRT projection determinants. No global homology or number-field K2.

Supports: P28. Internal review: A17.
Replay modes: normal, -O, -OO. Dependencies: sympy.
Script SHA-256: `6edd54e89cc9805e1d33e31b30e44c626d750ea1c376163cc0f184ec8c85396d`.

### C16 check_residue_obstructions.py

[Script](checks/C16/check_residue_obstructions.py) · [Frozen output](checks/C16/expected.json)

204 induced-module cases, including 190 with nontrivial five-Sylow, and finite congruence examples. No actual arithmetic residue or continuity calculation.

Supports: P29, P30. Internal review: A18.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `d594c2bb4d1071b12d760faaaff20c407caa3bbe817f2b8d5456a32f337fb8a8`.

### C17 check_content_marginals.py

[Script](checks/C17/check_content_marginals.py) · [Frozen output](checks/C17/expected.json)

Independent integer quotient ring counts and general local projection determinant checks.

Supports: P28. Internal review: A17.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `bc12daf9fb585423ad1ddf52df3b442ee8b2a4dc5400c3cd030578c355108791`.

### C18 check_cyclic_exterior.py

[Script](checks/C18/check_cyclic_exterior.py) · [Frozen output](checks/C18/expected.json)

Independent exact sparse-exterior identities for cyclic orders 2 through 17, including degenerate sign classes and double-delta witness.

Supports: P28. Internal review: A17.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `cb325529f05be421efdf0e32eba70d4b30b07c93cc1f04e7189a8fbbc90fb677`.

### C19 check_exceptional_smoothing.py

[Script](checks/C19/check_exceptional_smoothing.py) · [Frozen output](checks/C19/expected.json)

Nine local depth minima, three final ray examples and 125 compatible formal families. Formal test failures are not actual arithmetic obstructions.

Supports: P31, P32. Internal review: A19.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `51bc95a2b49999ee17ee24ca1dad8ffe611ca1e740d0122eb4285e82705c48c2`.

### C20 CHECK_CUSP_REFLECTIONS.py

[Script](checks/C20/CHECK_CUSP_REFLECTIONS.py) · [Frozen output](checks/C20/expected.json)

1,922 conjugations, 3,599 primitive rows, 8,628 diamond solutions, 111,150 valuation boxes, 48 thresholds, 48 exceptional-unit cases and seven Gaussian ray checks. No K2 cusp values.

Supports: P33, P34. Internal review: A20.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `59e7af2626395be0c771644ee86c091cacbf8fade300de6327783c1cafb5ec37`.

### C21 check_cusp_criterion.py

[Script](checks/C21/check_cusp_criterion.py) · [Frozen output](checks/C21/expected.json)

Independent 28,679 primitive local rows and 538,083 valuation vectors in 6,174 boxes. No K2 value or global compactification computation.

Supports: P33, P34. Internal review: A20.
Replay modes: normal, -O, -OO. Dependencies: Python standard library.
Script SHA-256: `eb30a07330408039f7bc4702616e71720a9e4ff9e9128df004fb05ab97bf6ada`.

## Earlier review coverage and assembly replay

Historical review claims are preserved in the individual acceptance reports. This edition adds a direct isolated replay of the listed frozen scripts and compares their output with frozen snapshots. The recorded run is in REPLAY_RESULTS.json. No missing theorem is inferred from successful replay.

# Exact 9--12-vertex incident-boundary completion portfolio

Date: 2026-07-23 (America/Los_Angeles)

## Outcome

No order-43 Ramsey graph was found.

The preregistered portfolio completed all 16 exact SAT searches. Two
9-vertex boundaries returned `UNSAT`; the other 14 searches exhausted their
registered conflict budgets. No SAT model was emitted.

The two negative returns are **reproducible computational observations only**.
They have no proof certificates and therefore are not certified
nonexistence statements. The 14 budget-exhausted searches are unresolved.
This finite portfolio does not change any Ramsey-number bound.

The independently reconstructed result audit accepted every formula
fingerprint, every plan/result binding, all status counts, and all coverage
identities.

## Scope and deterministic selection

The bases are catalog lines 1 and 2, representatives of the two
complement-isomorphism classes in the retained 22-graph exact-\(E=2\) corpus:

| Class | Catalog line | Conflict colour | Six-vertex conflict union | Base SHA-256 |
|---|---:|---|---|---|
| class01 | 1 | independent | 1,3,11,25,35,37 | `c168d89376f939653c4a7d1f9da4c5800fb9379bf2c4a5cd7db226fce8789a85` |
| class02 | 2 | clique | 8,19,25,27,29,30 | `4e18e027c3211898569ae8a2113ff6e62c1bffd6bb9d2f413930225109547da4` |

Every boundary contains its base's entire conflict union. The two nested
selection policies were computed before production:

- `near_pressure` greedily covers five-sets with exactly one or nine edges
  that are still disjoint from the conflict union.
- `row_diversity` starts with the largest near-conflict load and then greedily
  maximizes the minimum Hamming distance between full adjacency rows.

The resulting six-vertex extra sequences are:

| Class | Policy | Ordered extra sequence |
|---|---|---|
| class01 | near_pressure | 17,39,33,32,23,42 |
| class01 | row_diversity | 26,28,0,8,32,41 |
| class02 | near_pressure | 28,41,12,0,38,35 |
| class02 | row_diversity | 12,22,17,20,34,2 |

Prefixes of length 3, 4, 5, and 6 give incident boundaries of size 9, 10,
11, and 12. All edges incident to any boundary vertex are free; every other
edge is pinned to the base. These sizes contain exactly 342, 375, 407, and
438 free edges, respectively.

The two SAT engines were cross-assigned to base/policy tracks. Conflict
budgets by boundary size were 400,000, 300,000, 200,000, and 150,000. Runs
were sequential (`jobs=1`) and proof logging was disabled.

## Exact production records

| Instance | Incident vertices | Solver | Clauses | Status | Conflicts | Solve s |
|---|---|---|---:|---|---:|---:|
| class01_near_pressure_k09 | 1,3,11,17,25,33,35,37,39 | MapleChrono | 113,742 | observed UNSAT | 312,264 | 138.855 |
| class01_near_pressure_k10 | 1,3,11,17,25,32,33,35,37,39 | MapleChrono | 141,999 | budget exhausted | 300,000 | 142.812 |
| class01_near_pressure_k11 | 1,3,11,17,23,25,32,33,35,37,39 | MapleChrono | 173,767 | budget exhausted | 200,000 | 49.108 |
| class01_near_pressure_k12 | 1,3,11,17,23,25,32,33,35,37,39,42 | MapleChrono | 209,088 | budget exhausted | 150,000 | 17.754 |
| class01_row_diversity_k09 | 0,1,3,11,25,26,28,35,37 | Glucose3 | 114,705 | budget exhausted | 405,445 | 146.007 |
| class01_row_diversity_k10 | 0,1,3,8,11,25,26,28,35,37 | Glucose3 | 143,469 | budget exhausted | 300,036 | 53.369 |
| class01_row_diversity_k11 | 0,1,3,8,11,25,26,28,32,35,37 | Glucose3 | 175,340 | budget exhausted | 200,330 | 17.452 |
| class01_row_diversity_k12 | 0,1,3,8,11,25,26,28,32,35,37,41 | Glucose3 | 210,696 | budget exhausted | 150,099 | 11.659 |
| class02_near_pressure_k09 | 8,12,19,25,27,28,29,30,41 | Glucose3 | 113,553 | budget exhausted | 400,698 | 101.704 |
| class02_near_pressure_k10 | 0,8,12,19,25,27,28,29,30,41 | Glucose3 | 141,724 | budget exhausted | 305,085 | 76.405 |
| class02_near_pressure_k11 | 0,8,12,19,25,27,28,29,30,38,41 | Glucose3 | 173,602 | budget exhausted | 200,102 | 46.185 |
| class02_near_pressure_k12 | 0,8,12,19,25,27,28,29,30,35,38,41 | Glucose3 | 208,932 | budget exhausted | 150,399 | 21.266 |
| class02_row_diversity_k09 | 8,12,17,19,22,25,27,29,30 | MapleChrono | 114,462 | observed UNSAT | 185,176 | 39.482 |
| class02_row_diversity_k10 | 8,12,17,19,20,22,25,27,29,30 | MapleChrono | 142,839 | budget exhausted | 300,000 | 85.192 |
| class02_row_diversity_k11 | 8,12,17,19,20,22,25,27,29,30,34 | MapleChrono | 174,977 | budget exhausted | 200,000 | 34.184 |
| class02_row_diversity_k12 | 2,8,12,17,19,20,22,25,27,29,30,34 | MapleChrono | 210,930 | budget exhausted | 150,000 | 16.658 |

Total production wall time was 1,039.550 seconds. Coverage was 16/16, with
two proof-free `UNSAT` returns, 14 budget exhaustions, zero SAT returns, and
zero candidate artifacts.

The two observed closed boundaries are structurally different and cover both
retained complement classes:

```text
class01 near_pressure k=9:
1,3,11,17,25,33,35,37,39

class02 row_diversity k=9:
8,12,17,19,22,25,27,29,30
```

## Formula fingerprints

The independent checker reconstructed the incident edge map and every
five-set clause without importing the production generator. It matched these
full stream hashes:

```text
class01_near_pressure_k09  f0af70db210dcb5a155190fe9b970560db58e09aa3d6ffb0ce8295bbaa79e7c7
class01_near_pressure_k10  7300b4d6c1f1b85179ca7bce7037919e966c73ad14931f4c8737bcb53165614a
class01_near_pressure_k11  ad1c309bfd0b8fe774ac4b3b589eee703a2ebaa862c96f29e63944240c8dd380
class01_near_pressure_k12  cb06831ffee98b8c2b66f6e17cb5bbd0f65ce941333313a4769e21aa162b9260
class01_row_diversity_k09  1da3a0cffa0bc8e4ce5a06d745aa70523c44cf621607509ec5acbb34464671a4
class01_row_diversity_k10  778b7c773c0731c6967f66416041cdb4b3d07050791b75bd9f5ef8fe06be93cc
class01_row_diversity_k11  5678d3883cccf285aa3149c36c57d52baae9d73d37831b776eead96e9bc7cede
class01_row_diversity_k12  6ac83c1adb062d9b26b22545d58239420f84a04242dbd25fc30dc290bce83d44
class02_near_pressure_k09  fc36733e14c492015e080d376d6565f2125c885af2965aeb680e8341472a661a
class02_near_pressure_k10  b4330e0b6b843acba0d1f615a8ae21ba230383b6f35ce94d2808e7484cb7a478
class02_near_pressure_k11  ee0fa509ebe11b4c094aa9e28edb2a9842d9fbbd104989d78dc252ca7de5c7ce
class02_near_pressure_k12  827359f55b676724a38414985448f9ba665d56ad6ecf5a0cf0cdf25d1348df1a
class02_row_diversity_k09  74a1f62392dd96a3be848705b23d06acc36cbb42c1f049ca219ffcf7dd15b945
class02_row_diversity_k10  932915b6fc627b7ce6c14be5db779cdc056893bf7d90664102e84e9b98bf9f07
class02_row_diversity_k11  99688a6402ee66e415ec4b752e8993099d87e3b00b3c85787179b2c6ddd4c566
class02_row_diversity_k12  32af5cac97fc36795888f545b2e1d866fe73f308fa2f6f5790be98f6e220aab8
```

## Artifact hashes

```text
production source
b8f903ddc3a9ddb3a4464c4e14f40aae69ddd422997c7637f421c257b17fcb69

independent checker
e6cad18d02100e63cc085263219744504d0e07935e5f7d7118c5e0b281edbf5c

tests
8286bfb5b2a678f40f2b44dea9d8941fe44ee107a0e9eb1deb194f2c99f95f3e

frozen plan
9a002eae81f5ce72cea27f07dad3cd5e74a47d828fa4121e0bb5dc47904cbbf7

preproduction plan audit
9ca50bdd0564e27dfd80e09ec926a54f33ffde0d4b2a2b3a9aac170e948255d1

production result
cb5dbbcd815278643ef05e9e082ffabd9f956493da67965aa8a96bdf417d6e4d

independent result audit
f1250cf0b6cff12c851ab305ec6e099e204c6796147b3ceef116a74c4afa9c93
```

Had a SAT assignment appeared, the runner was preregistered to reconstruct
the full graph immediately and require agreement among embedded all-five-set
enumeration, the standalone Python all-five-set verifier, and the separately
implemented C++ recursive-bitset verifier before recognizing a construction.
That path was not exercised because no SAT assignment appeared.

# Certified exclusion of cycle type \(13^2 1^{17}\)

## Result and claim boundary

The symmetry-broken exact CNF is **CERTIFIED UNSAT**. Therefore no
\((5,5)\)-Ramsey graph on 43 vertices admits an automorphism with cycle type
\(13^2 1^{17}\).

This result does **not** cover the different cycle type \(13^1 1^{30}\), does
not exclude all order-13 automorphisms, and does not establish a global Ramsey
bound.

## Structural reduction

The base orbit formula has:

- 195 edge-orbit variables: 59 orbits of size 13 and 136 singleton orbits;
- 76,132 unique five-set signatures;
- 152,264 Ramsey clauses;
- unsymmetrized DIMACS SHA-256:
  `089d798347c2e991ce4c3c45aa879600e3edceabae7e97bae7079b6f9a7255e3`.

Every vertex of a 43-vertex \((5,5)\)-Ramsey graph has degree in 18--24. For
one of the 17 fixed vertices, write its degree as

\[
13m+d_F,
\]

where \(m\in\{0,1,2\}\) counts adjacent moved cycles and \(0\le d_F\le16\) is
its degree in the fixed subgraph. The degree interval forces \(m=1\) and
\(5\le d_F\le11\).

The 17 fixed vertices may be relabeled so that incidence with the first moved
cycle is a true prefix. Exchanging the two moved cycles selects a prefix of
size at most eight. This yields exactly the nine group sizes 0 through 8.
The single certificate CNF adds only 51 clauses:

- 34 clauses enforcing exactly one adjacent moved cycle per fixed vertex;
- 16 clauses sorting the first-cycle incidence bits;
- 1 unit clause making the ninth bit false.

The independent checker reconstructed the base orbit formula separately,
reconstructed all 51 clauses, compared all 152,315 clauses in order, and
validated the complete nine-case symmetry cover.

## Certificate

- CNF: 4,782,467 bytes, SHA-256
  `0a333f157833291de463c02bc4632ae9f66c0515b94cbd9e4b2d5a10260cc318`;
- Glucose3: UNSAT after 265 conflicts;
- DRAT: 2,793,954 bytes, SHA-256
  `8f299aea27d59c0a3142ebb533a96a70d828b526f964efd57d424da940d2b568`;
- `drat-trim`: `s VERIFIED`;
- LRAT: 1,000,439 bytes, SHA-256
  `b7c01d9f20673a2433722ab86288430ae2967861b811c99583763ad6aac03032`;
- `lrat-check`: `c VERIFIED`.

Pinned tool hashes and complete checker transcripts are in
`order43_automorphism13_two_cycles_symmetry_broken_glucose3.result.json`.

## Reproduction

```sh
python3 src/automorphism13_two_cycle_certificate.py \
  --cnf certificates/order43_automorphism13_two_cycles_symmetry_broken.cnf \
  --metadata certificates/order43_automorphism13_two_cycles_symmetry_broken.metadata.json

python3 verify/automorphism13_two_cycle_symmetry_cnf_check.py \
  certificates/order43_automorphism13_two_cycles_symmetry_broken.cnf \
  --metadata certificates/order43_automorphism13_two_cycles_symmetry_broken.metadata.json \
  --result results/verification/order43_automorphism13_two_cycles_symmetry_cnf_check.json

PYTHONPATH=/tmp/ramsey55-pysat.4YSXId \
  /opt/homebrew/opt/python@3.11/bin/python3.11 \
  src/certify_cnf_glucose.py \
  certificates/order43_automorphism13_two_cycles_symmetry_broken.cnf \
  --proof certificates/order43_automorphism13_two_cycles_symmetry_broken_glucose3.drat \
  --lrat certificates/order43_automorphism13_two_cycles_symmetry_broken_glucose3.lrat \
  --result certificates/order43_automorphism13_two_cycles_symmetry_broken_glucose3.result.json \
  --time-limit 60 --proof-check-time-limit 120
```

The focused test suite is
`python3 -m unittest -v tests/automorphism13_two_cycle_tests.py`.

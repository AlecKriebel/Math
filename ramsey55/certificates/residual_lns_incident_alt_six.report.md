# Alternative six-vertex incident-neighborhood certificate

Date: 2026-07-23

## Scope

The constructive 237-edge search produced
`results/best_candidates/incident_lns_seed_20260726.g6`, an order-43 graph
with \(C_5=2\), \(I_5=0\), and residual clique union
\(\{2,4,24,25,26,42\}\). This experiment frees every edge incident to those
six vertices and fixes the other 666 edges to that candidate.

**CERTIFIED:** no assignment of these 237 free edges is a
\((5,5;43)\)-graph. This is a fixed-boundary statement only; it is not global
order-43 nonexistence.

## Deterministic generation

```sh
python3 src/residual_lns_sat.py \
  results/best_candidates/incident_lns_seed_20260726.g6 \
  --free-incident-vertices 2,4,24,25,26,42 \
  --output certificates/residual_lns_incident_alt_six.cnf \
  --metadata certificates/residual_lns_incident_alt_six.metadata.json
```

The instance has 237 variables and 49,677 clauses: 25,860
clique-prevention clauses and 23,817 independent-set-prevention clauses.

An independently written direct-subset reconstructor matched every clause in
the exact order:

```sh
python3 verify/residual_lns_cnf_check.py \
  --graph results/best_candidates/incident_lns_seed_20260726.g6 \
  --cnf certificates/residual_lns_incident_alt_six.cnf \
  --free-incident-vertices 2,4,24,25,26,42
```

The check reported zero missing or extra clauses.

## Proof production and checking

The pinned certification pipeline ran Glucose3 from Python-SAT 1.9.dev7,
checked its ASCII DRAT trace with `drat-trim`, converted the accepted core to
LRAT, and checked that proof independently with `lrat-check`:

```sh
python3 src/certify_cnf_glucose.py \
  certificates/residual_lns_incident_alt_six.cnf \
  --proof certificates/residual_lns_incident_alt_six_glucose3.drat \
  --lrat certificates/residual_lns_incident_alt_six_glucose3.lrat \
  --result certificates/residual_lns_incident_alt_six_glucose3.result.json \
  --time-limit 600 \
  --proof-check-time-limit 1200
```

Glucose returned UNSAT in 0.275337 internal seconds with 9,801 conflicts,
13,610 decisions, and 192,539 propagations. `drat-trim` accepted a core with
5,421 input clauses and 5,273 of 9,802 lemmas using 182,741 resolution steps;
all retained lemmas were RUP. `lrat-check` then reported `VERIFIED`.

## Hashes

- Candidate graph6:
  `c0a8d2de5e7efa1abc6848c71e61019579ff31d8958fcce70f257d725792c337`
- CNF:
  `e470ed2a4a1fe316b8cce77ab2e3f1c4f6ceb9d57b37e1e076f780e77a919867`
- Metadata:
  `59494b5cc1f218d53390406242fe36e6c10fe63b042526e9817c251ff317a3db`
- DRAT, 1,024,310 bytes:
  `bb7cdeecfaabdddd96117d1bd3463cf5699ffd84959787d5fdcd55d18423bb70`
- LRAT, 1,806,516 bytes:
  `df22449c12fcb20fb2140a1fa3f8ffe3f10bc4716c957e10b4518a0de821c5c3`
- Certification result:
  `24d0b6a4b9997f6af9f7bb2ea7c47af2fb1fc80a1bbef6bccc3076266bb5e5e1`

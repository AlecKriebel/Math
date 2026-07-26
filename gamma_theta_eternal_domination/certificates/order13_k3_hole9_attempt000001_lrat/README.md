# Order-13, parameter-three, `hole9` certificate candidate

## Current status

`CANDIDATE_PENDING_INDEPENDENT_HOSTILE_AUDIT`

This directory freezes a promising but not yet accepted certificate for the
exact `hole9` CNF.  The original final-v3 production attempt correctly ended
as `RETRYABLE_NONCLAIM`: CaDiCaL returned exit 20 and wrote a strict
`s UNSATISFIABLE` result, but the first raw forward check treated
drat-trim's ignored pseudo-unit-deletion warning as fatal and exited 80.

No claim is recovered from that failed phase.  Instead, a fresh diagnostic
operation used the already reviewed strict binary parser to remove all
deletion records, producing a new additions-only proof.  The frozen candidate
then passed:

1. forward drat-trim verification with `-i -f -W -U`, so every retained
   lemma is RUP and warnings are fatal;
2. backward RUP-only conversion to LRAT with `-i -W -U -L`; and
3. a separate `lrat-check` replay against the exact formula.

The normalized proof has 45,281 additions total: 45,280 nonempty additions
followed by one unique empty addition.  It contains no deletion, uses
variables at most 9,802, and has zero RAT lemmas in the forward core.  Its
SHA-256 is
`af216ef2d7698db2b1d1c55411bc05025bfe25f10c16f2e85c5301f7a88bdd5f`.
The 8,546,664-byte LRAT file has SHA-256
`f6ef614f2acee4cf43aa3b75372b354912c50248a13c3f863479cdc49b061805`.

## Claim boundary

Even successful replay of these proof files certifies only UNSAT of the exact
DIMACS formula.  Excluding the mathematical `hole9` branch additionally
requires the accepted graph-to-CNF theorem, exact constructor bindings, and a
coverage audit.  Until a separately written verifier and hostile review bind
and replay all of those dependencies, this directory makes no template
exclusion, order-13 exclusion, or universal conjecture claim.

The original nonclaim run remains unmodified in
`results/order13_k3_hole9_production/attempts/attempt-000001`.  Its raw proof
is frozen here byte-for-byte for provenance, but the additions-only proof and
LRAT file are the candidate certificates.

## Primary artifacts

- `candidate-manifest.json`: exact hashes, sizes, commands, tool hashes,
  source bindings, and the nonclaim provenance boundary.
- `instance.cnf`: exact `hole9` formula, 9,802 variables and 32,108 clauses.
- `proof.normalized.bdrat`: additions-only, unique-final-empty binary RUP
  proof.
- `proof.lrat`: LRAT certificate replayed by the separately compiled
  `lrat-check`.
- `normalization-report.json`: strict transformation census.
- `rup-forward.*`, `lrat-convert.*`, and `lrat-check.*`: retained diagnostic
  transcripts.
- `proof.raw.bdrat` and `raw-hardwarning.*`: original solver proof and the
  precise reason the accepted runner refused to promote attempt 1.

The final publication command will be supplied only after the independent
verifier and hostile review have frozen their own accepted artifacts.

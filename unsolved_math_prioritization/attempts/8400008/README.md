# O7b: restricted squarefree-oracle findings

Problem identifiers: O7b / 8400008 / AMR-083-0008.

**Current disposition: the reconstructed restricted results from turns 1 and 2 have passed a fresh independent AI mathematical audit. The original full-factorization reduction remains unresolved after two approaches (2/5 turns).** This proof-only edition restores those same two approaches; it introduces no new research turn.

## Read the complete argument

1. [Model and target](reports/MODEL_AND_STATUS.md): the parity squarefree-decomposition oracle C7, the complete-factorization task, zero-error output, and worst-case polynomial bit, query, and random-tape requirements.
2. [Full turn-1 derivations](reports/TURN1_RECONSTRUCTED.md): gcd-layer support projection, tape-by-tape coprime-query simulation, recoverable valuation blocks, the stated-operation invariant, and the fresh-polynomial bound with its exact adaptive event interpretation.
3. [Full turn-2 derivations](reports/TURN2_CANDIDATE.md): sign-blind square-relation success, the complete fixed-batch dependency kernel, and the equal-norm transporter theorem with arbitrary prime valuations.
4. [Full fresh mathematical audit](AUDIT.md): review of every argument, hypothesis, complexity bound, counterexample, and remaining obligation.
5. [Current acceptance and interpretive conventions](ACCEPTANCE.md), [chronology and editorial provenance](PROVENANCE.md), [historical source verification](reports/SOURCE_VERIFICATION.md), and [subsequent source-inspection metadata](SOURCE_PROVENANCE.json).

The four report files are preserved exactly as first reconstructed. Their “preliminary,” “unaccepted,” and “no independent acceptance” statements describe their pre-audit creation state. ACCEPTANCE.md and AUDIT.md record the later fresh acceptance of these exact bytes. The historical Dixon retrieval failure likewise precedes the successful audit-stage text inspection recorded in SOURCE_PROVENANCE.json. None of the preserved statements should be silently read as a current status update.

## Two essential conventions

For the transporter, under all hypotheses in turn 2, the identity is

    gcd(c,n) = n/gcd(B,n),    B = x*r' - x'*r.

It is never an identity asserting c = n/gcd(B,n). The reduced denominator c may contain higher prime powers and primes outside n. The supplied example has n=15 and c=105.

The subset relation theorem uses only exponents 0 and 1. Its brief extension to general integer exponents requires a well-defined rational-unit square relation when exponents are negative: all denominators must be invertible modulo n. At least one exponent must be odd for the fresh-sign argument. ACCEPTANCE.md spells out this convention.

## What this edition does not establish

- A polynomial-bounded way to acquire a useful relation or a suitable second equal-norm representation.
- A complete, zero-error factorization reduction for all positive inputs with at least half of bounded tapes successful.
- A lower bound for unrestricted classical bit algorithms, a general removal of C7, or a claim that coprime oracle answers are useless.
- Novelty for Dixon's congruence-of-squares method, gcd-free bases, valuation techniques, or elementary polynomial root bounds.

The review is AI mathematical auditing, not human peer review, journal acceptance, or formal proof-assistant verification. The unresolved status records the outcome of these two approaches, not an exhaustive certification of the current literature.

## Contents and integrity

MANIFEST.json lists all eleven edition files and hashes the other ten without a circular self-hash. This edition is readable without executing software. Audit descriptions of finite checks are retained as supplementary history; checking programs, standalone fixtures, separate results, and logs are not distributed. No third-party source document, dataset, private source, or private coordination material is included. No queue or unrelated repository file is changed.

# Hostile review of the order-12, parameter-four DoubleLex LRAT package

## Verdict

**ACCEPT EXACT DOUBLELEX CNF UNSAT ONLY.**

The exact DIMACS formula

```text
instances/order12_k4_connected_doublelex/instance.cnf
SHA-256 14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7
4,030,657 bytes
18,381 variables
115,507 clauses
1,190,774 literal occurrences
```

is unsatisfiable.

This verdict is intentionally narrow. This review does not itself establish
the transfer from the strengthened DoubleLex formula to the anchored parent,
does not by itself exclude the `(n,k)=(12,4)` graph slice, and does not resolve
the universal γ–θ conjecture. That transfer is a separate mathematical audit.

No blocking gap was found within the exact-formula UNSAT scope.

## Frozen target

The reviewed author package is:

```text
certificates/order12_k4_doublelex_seed0_lrat/
35 regular single-link files
260,029,326 total bytes
canonical inventory SHA-256
0814a4f435f9a50784eb12dcd99116f5b4529587a78723bff328dcec86ec7113
```

The decisive author records are:

```text
certificate.json
a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991

artifact-manifest.json
846a646ba951569f50a76b562fdc8ec005dcf0f06ff57e48b4e3d4d330fbd607
```

The complete review evidence is:

```text
hostile-evidence.json
2651f9d286582c068fb872acf862b82c4d4ab8e5fc07f6b99825b9335dd40b63

hostile_audit.py
950a7f787b8d3b1e5d6637c2bfded821925865b14d1615f1808b97ebcc0b6826

private-replay/prepare-evidence.json
df7390ff6fa7b7205ba954c444e2e723fc716581a0ad0a7c8caec83162026338
```

The author package, formula, source, tests, theorem, prior reviews, raw proof,
and checker binaries were rehashed before every long replay phase and again
at finalization. Their hashes remained unchanged.

## Static certificate and provenance audit

The exact certificate and artifact-manifest schemas, key sets, pending-review
statuses, proof-pipeline identifier, and claim boundaries were checked
fail-closed. Every source and output binding was compared with the actual
regular single-link file, including path, SHA-256, and byte size. The
certificate's embedded phase-resource objects equal their separately stored
resource JSON objects.

The following exact identities were confirmed:

```text
drat-trim
31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb

lrat-check
5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2

strict normalizer source
07229fce9293a05fed3fa6ef3f96415eb48ea4b0cdd8e9a329620017d2bced99

normalizer Python
b502cb4c5b46b8d4192ec6bcb600ce8922f1afc396fcf646e8765c6eba74a0bf
```

The bound DoubleLex theorem, generator, four generator tests, prior hostile
review, prior hostile probe, and prior probe evidence all match the hashes
recorded in the certificate. The four tests passed afresh. The accepted
hostile probe reran and reproduced its recorded JSON byte for byte. These
checks establish correct binding; the mathematical implication to the parent
remains separately scoped.

## Independent formula reconstruction

The exact parent

```text
SHA-256 adbe0c01614bae6cd3aed4ccdcd45a757ca56e7ef9c4f2f280f2d8ef200e40ac
```

was combined with a clean-room generation of all three adjacent eight-bit
column comparators. The independent suffix has 765 clauses, 10,758 literals,
37,710 bytes, and SHA-256

```text
328eeeaadc688bbce63fd3ffd952f86a4eb9209e6d0abf5542979fe54ebdbbe0
```

The resulting private formula is byte-identical to the reviewed formula and
has SHA-256 `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`.
An independent strict DIMACS parser confirmed the full census above.

## Independent binary-proof audit

The preserved raw binary DRAT stream is:

```text
SHA-256 ed3975c5f0cfbe9475c607e440c0ddc012722d0fe68b797e693149fd6f7d5c51
32,987,136 bytes
```

A reviewer-written parser consumed the complete stream, required canonical
unsigned varints, enforced the variable bound, rejected negative zero and
empty deletions, and recorded:

- 1,378,975 total records;
- 640,854 additions;
- 738,121 deletions;
- 22,445,080 literal occurrences across all records;
- 10,668,019 literals in addition records;
- maximum variable 18,381;
- one empty addition, at final record 1,378,975;
- no deletion or addition after that empty record.

The normalized stream was independently parsed as:

- 640,854 addition records and no deletions;
- 10,668,019 literal occurrences;
- maximum variable 18,381;
- one empty addition, at final record 640,854.

The pinned strict normalizer was then rerun on a private copy of the raw
stream. It deterministically reproduced the retained addition-only proof byte
for byte:

```text
SHA-256 2741335a5ed9af769f0db4bd0c03a70e414d0568681d5b8261a5667ed30b6686
15,783,377 bytes
```

The normalizer report independently reproduced the same record census and
retained its explicit `TRANSFORMATION_ONLY_NO_PROOF_CLAIM` boundary.

## Independent proof replay

All replay children used private formula and proof paths under the
campaign-wide single-heavy-job lock. No SAT solver was invoked.

### Forward RUP replay

The exact proof options were:

```text
-i -f -W -U -t 3600
```

The child exited 0 after 437.236 seconds, used 124.547 MiB maximum RSS, wrote
empty stderr, reported `s VERIFIED`, and reported `0 RAT lemmas`.

### Backward RUP conversion

The exact proof options were:

```text
-i -W -U -L <fresh-private-LRAT> -t 3600
```

The child exited 0 after 225.372 seconds, used 244.641 MiB maximum RSS, wrote
empty stderr, reported `s VERIFIED`, and reported `0 RAT lemmas`.

The freshly converted LRAT file is byte-identical to the retained LRAT:

```text
SHA-256 0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263
228,381,671 bytes
```

### Fresh LRAT checking

Pinned `lrat-check` was run separately against:

1. a private copy of the author's retained LRAT; and
2. the independently converted fresh LRAT.

Both children exited 0, wrote empty stderr, and reported `c VERIFIED`. They
each parsed 18,381 variables and 115,507 clauses and recorded identical proof
censuses:

```text
Added clauses = 471552
Deleted clauses = 471427
Max live clauses = 115507
```

## Failed-attempt separation

Both preserved failed-attempt directories are fully hash-bound by the
artifact manifest and excluded from the decisive output map.

In particular, the deletion-bearing raw-stream forward diagnostic in
`failed-attempt-000001` has `passed=false`, exit code 80, no verification
marker, and no entry in the certificate's decisive phase-resource map. No
decisive command or output path points into a failed-attempt directory.

The exit-80 raw-forward attempt is therefore provenance for a rejected
nonclaim, not evidence for UNSAT. The decisive forward check is the successful
warning-fatal RUP-only replay of the strictly normalized addition-only stream.

## Mutation probes

The hostile harness confirmed fail-closed rejection of:

- a one-byte formula mutation;
- a one-byte normalized-proof mutation;
- a truncated LRAT;
- a one-byte certificate mutation;
- a symlink substituted for a bound file; and
- a multiply linked bound file.

## Final scope

This hostile review accepts only:

> The exact DoubleLex-strengthened DIMACS formula with SHA-256
> `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`
> is unsatisfiable.

Any statement about the anchored parent or the `(12,4)` graph slice must cite
and survive the separate DoubleLex implication/coverage audit. No universal
conjecture claim follows from this review alone.

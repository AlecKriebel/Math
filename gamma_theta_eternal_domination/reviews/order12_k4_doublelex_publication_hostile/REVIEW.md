# Hostile review of the compact DoubleLex LRAT publication package

## Verdict

**ACCEPT THE EXACT-CNF UNSAT PUBLICATION PAYLOAD, WITH A METADATA-INTEGRITY
LIMITATION.**

The frozen four-file package

```text
certificates/order12_k4_doublelex_seed0_lrat_publication/
```

faithfully carries the already accepted LRAT certificate for the exact
DoubleLex CNF:

```text
instances/order12_k4_connected_doublelex/instance.cnf
SHA-256 14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7
4,030,657 bytes
18,381 variables
115,507 clauses
1,190,774 literal occurrences
```

The exact formula is unsatisfiable.  No blocking defect was found in the
compressed-proof recovery or exact-CNF proof-checking chain.

This verdict is deliberately narrow.  It does not establish the
graph-to-CNF transfer, does not by itself exclude the connected
`(n,k)=(12,4)` graph slice, does not establish an order-12 frontier, and does
not resolve the universal γ–θ conjecture.  Those statements require their
separate mathematical and coverage audits.

## Frozen target

The target remained unchanged from the opening snapshot through the final
rehash:

```text
4 regular single-link files
64,301,640 total bytes
canonical inventory SHA-256
3ac2f8b4107f737d175b0521ed121e465a9229dba6f119e0e8d9a431c1787be3
```

The individual bindings are:

```text
README.md
2,676 bytes
8878154c2529a0a28c25fd7203df8a5c5389c1074b246acb104fb1b8c003da43

proof.converted.lrat.zst
64,288,636 bytes
edc0f6b76bc96b2b26677f399566ae437cc47a6fc0cc921eaff81d77b72a50da

publication-manifest.json
2,679 bytes
2a93c99671d872bcd9f4284929614a4c3e6216f38f04dc6b81399694d48e5ac5

verify_publication.py
7,649 bytes
0313029ca93ee372178ed72bfb139887438355eaa66cf36537fdfdbad0b1c22f
```

The reviewer-written evidence is:

```text
hostile_publication_audit.py
39,986 bytes
d05aa5847db10cdaca2d8452a83062b533bdc77b107a7d8d4d21250afa474994

hostile-evidence.json
17,094 bytes
3c40bdac300d3d3a1aafefdfdc4dbade9351b2aff7dff1f66e0f0d9223782454
```

## Manifest and provenance audit

The manifest was parsed with duplicate-key and non-finite-number rejection.
Its exact root schema, nested key sets, value types, status, claim boundary,
paths, sizes, hashes, compression record, proof census, checker binding,
author-package binding, hostile-review binding, and verification record all
match the frozen target.  No extra package file, symlink, or multiply linked
file was present.

An independent strict DIMACS parser reproduced:

```text
18,381 variables
115,507 declared and parsed clauses
1,190,774 literal occurrences
maximum variable 18,381
```

The following external bindings used by the package verifier were rehashed
against the live files:

```text
exact formula
14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7

lrat-check
5d7d77a57457db82e57f2505ea9d0267ff0bceff197235b6edfc8fda1f26c7a2

author certificate
a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991

author artifact manifest
846a646ba951569f50a76b562fdc8ec005dcf0f06ff57e48b4e3d4d330fbd607

accepted hostile review
fb95934b5d5acd75c9f6deb9142be3b903900f5abd02a5cc21d9884788f38395

accepted hostile evidence
2651f9d286582c068fb872acf862b82c4d4ab8e5fc07f6b99825b9335dd40b63
```

The complete 35-file author package was also resnapshotted.  Its
260,029,326-byte inventory is entry-identical to the previously accepted
snapshot and retains canonical inventory SHA-256
`0814a4f435f9a50784eb12dcd99116f5b4529587a78723bff328dcec86ec7113`.
The accepted hostile evidence still has the exact verdict
`ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY` and binds both its fresh and retained
LRATs to the publication package's recovered-proof hash.

## Independent compression and recovery audit

Zstandard CLI 1.5.7 reported one frame, no dictionary, decompressed size
228,381,671 bytes, and an XXH64 frame checksum.  Its independent integrity
test passed.

Private decompression produced:

```text
proof.recovered.lrat
228,381,671 bytes
0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263
```

The recovered file was compared block-for-block with the retained author
LRAT and was byte-identical.  Recompressing that recovered file with the
manifested command parameters, `zstd -9 -T1 --check`, reproduced the
publication stream byte-for-byte, including its exact size and SHA-256.

Thus compression has not substituted, truncated, or logically changed the
accepted LRAT artifact.

## Fresh private one-command replay

The reviewer created a private campaign mirror containing only the ten files
needed by the publication verifier.  No package path or proof path was shared
with the target except as a copy source.  From that private campaign root the
documented verifier was run afresh:

```text
python3 certificates/order12_k4_doublelex_seed0_lrat_publication/verify_publication.py
```

The child exited 0 after 3.977 seconds, wrote empty stderr, recovered the exact
LRAT hash above, and invoked the hash-pinned `lrat-check`.  The checker
reported exactly one verification marker and the required census:

```text
c parsed a formula with 18381 variables and 115507 clauses
c VERIFIED
c Added clauses = 471552.  Deleted clauses = 471427.  Max live clauses = 115507
```

The verifier's exact JSON payload carried the verdict field:

```text
VERIFIED_EXACT_DOUBLELEX_CNF_UNSAT_ONLY
```

with its explicit boundary that transfer to graphs uses the separately
reviewed C-037/C-045 implication.  No SAT solver was invoked during this
audit.

## Fail-closed mutation probes

All eleven decisive-input probes were rejected with exit code 1, empty
stdout, and a `REJECTED:` diagnostic:

1. one-byte formula mutation;
2. one-byte compressed-LRAT mutation;
3. one-byte checker mutation;
4. one-byte author-certificate mutation;
5. one-byte author-manifest mutation;
6. one-byte accepted-review mutation;
7. one-byte accepted-review-evidence mutation;
8. formula symlink substitution;
9. formula multiple-hard-link substitution;
10. one-byte compressed-LRAT truncation; and
11. absence of `zstd` from the executable path.

These probes cover every logical or provenance input hardcoded by
`verify_publication.py`.

## Metadata-integrity limitation

The target verifier does not parse `publication-manifest.json` and does not
bind `README.md`.  Empirically:

- changing the manifest's schema version from 1 to 2 still returned the
  exact-CNF success verdict; and
- a one-byte README mutation still returned that verdict.

This means the command is a fail-closed verifier of the mathematical core,
not a complete integrity checker for all four package files.  The limitation
does **not** invalidate the exact-CNF UNSAT result: the formula, compressed
proof, recovered proof, checker, author certificate, author manifest, and
accepted hostile review are all hardcoded by size and SHA-256, and the
emitted verdict remains explicitly narrow.  The present frozen metadata is
independently validated and bound by this review.

For stronger one-command packaging, a later revision should parse the exact
manifest schema and validate its README and verifier entries.  Any such
revision changes the frozen package hashes and requires a new package review.

## Final accepted scope

This review accepts exactly:

> The compact zstd package faithfully represents the already accepted LRAT
> certificate proving that the DoubleLex DIMACS formula with SHA-256
> `14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7`
> is unsatisfiable.

No broader graph-theoretic or universal claim follows from this package
review alone.

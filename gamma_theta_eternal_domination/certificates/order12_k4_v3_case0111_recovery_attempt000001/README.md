# Order-12, parameter-4, v3 case `0111` recovery package

## Status

This is an **author-side recovery package pending separate hostile review**.
Its exact claim label is:

```text
NO_LEAF_OR_AGGREGATE_CLAIM_PENDING_SEPARATE_HOSTILE_REVIEW
```

It does not change the immutable production run. It does not yet promote case
`0111` to a certified-finite leaf. It makes no claim about the other 15 leaves,
the complete `(n,k)=(12,4)` slice, or the γ–θ conjecture.

## Recovered proof chain

The preserved production attempt ended as
`RAW_FORWARD_REJECTED_NONCLAIM` because the raw forward invocation exited
`80`. The source attempt is copied byte-for-byte under `source/attempt/`.

The recovery replay:

1. binds the frozen parent, partition, attempt, normalizer, `drat-trim`, and
   `lrat-check` by exact SHA-256 and size;
2. reconstructs the leaf CNF independently as the frozen parent with the cube
   clauses `-4`, `14`, `23`, `31`;
3. requires byte identity with the retained leaf
   `c9c187a8a83485da527910c7bc24b666d43248077d6d690c04bf0485f9f90e99`;
4. parses the complete raw binary DRAT stream
   `64ffb7bf3a6a25d1839a234298b3e7bbebdbd491303821dcb613ff5d515b1ce7`;
5. reproduces the historical raw-forward exit `80`;
6. invokes the frozen strict normalizer, producing the deterministic
   addition-only stream
   `b1bc9b3a26fe26acddf2c49c4202ebf82adba8298d5e3c0b386af35ec2c663e3`;
7. requires warning-fatal, RUP-only forward checking with
   `drat-trim -i -f -W -U`;
8. requires warning-fatal, RUP-only backward checking and LRAT emission with
   `drat-trim -i -W -U -L`; and
9. runs a fresh `lrat-check`, producing and accepting the deterministic LRAT
   artifact
   `5300c54b1e22492cbcae83a47898549c38ee799a33eba23fbe5d11123233dd54`.

The raw stream has 391,069 records: 158,688 additions and 232,381 deletions.
Its unique empty addition is record 391,069, the final record. After deletion
stripping, the stream has 158,688 addition records and its unique empty
addition is again final.

## One-command fresh audit

From this directory on the frozen Apple-arm64 runtime:

```sh
./verify_recovery.py
```

The command creates a private temporary replay, reconstructs the CNF, derives
both proof artifacts afresh, runs all three proof checks, compares exact
hashes, audits the retained author replay, prints one JSON summary, and removes
only its temporary directory. It never invokes CaDiCaL or another SAT solver.

To retain a new replay outside this package:

```sh
./verify_recovery.py --replay-dir /new/empty/path/that/does/not/exist
```

The verifier refuses to overwrite or reuse a replay directory.

## Retained artifacts

`author-replay/` contains the reconstructed CNF, normalized binary proof,
converted LRAT proof, checker stdout/stderr, phase resource records, the
normalization report, and `replay-report.json`. The latter is explicitly bound
to the exact `verify_recovery.py` bytes that created it.

`source/` contains frozen byte copies of every preserved production-attempt
file plus the parent, partition, run manifest, parent-generator manifest, and
normalizer. `tools/` contains the exact two checker executables used by the
frozen run. `package-manifest.json` inventories every package file except
itself.

See `CLAIM_BOUNDARY.md` before citing any artifact as a mathematical result.

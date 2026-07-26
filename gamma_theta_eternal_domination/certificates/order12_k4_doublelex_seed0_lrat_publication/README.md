# Publication package for the order-12 parameter-four DoubleLex refutation

## Exact claim

The DIMACS formula

```text
instances/order12_k4_connected_doublelex/instance.cnf
SHA-256 14284db1f0b9cfb37b91d834fbabac1d0ca06d36e0d2782683e35cbd04a976e7
18,381 variables
115,507 clauses
1,190,774 literal occurrences
```

is unsatisfiable.

The accepted LRAT file has SHA-256
`0e04eb639a3f7f7d335126d56040abb4ef11e8548770262c316a608390659263`
and 228,381,671 bytes.  It is stored here as
`proof.converted.lrat.zst`, because the uncompressed file exceeds GitHub's
100 MB per-file limit.  Zstandard 1.5.7 at compression level 9 produced the
64,288,636-byte stream with SHA-256
`edc0f6b76bc96b2b26677f399566ae437cc47a6fc0cc921eaff81d77b72a50da`.
Compression changes no logical artifact: the verifier checks the exact
uncompressed byte hash before invoking `lrat-check`.

This package alone does not encode the graph-to-CNF theorem.  The transfer
from exact formula UNSAT to the connected `(n,k)=(12,4)` exclusion uses the
separately accepted C-037 and C-045 proofs and the independent implication
audit.

## One-command verification

From the campaign directory:

```text
python3 certificates/order12_k4_doublelex_seed0_lrat_publication/verify_publication.py
```

The command:

1. verifies the exact package manifest and README bytes, plus the formula,
   compressed LRAT, checker, author-certificate, and hostile-review hashes;
2. decompresses the proof into a private temporary directory;
3. requires the recovered 228,381,671 bytes to have the accepted LRAT hash;
4. invokes the independently developed, hash-pinned `lrat-check`; and
5. requires a unique `c VERIFIED` marker and the accepted proof census.

Run `./tools/bootstrap_sat.sh` first if the pinned checker is not installed.
The verifier also requires the `zstd` command.  It uses approximately
230 MB of temporary disk and under 100 MB of memory during the decisive
LRAT replay.

## Source and independent review

The original frozen 35-file author package remains at
`certificates/order12_k4_doublelex_seed0_lrat/`, with inventory SHA-256
`0814a4f435f9a50784eb12dcd99116f5b4529587a78723bff328dcec86ec7113`.
Its certificate is SHA-256
`a21bd3db71fb271965859237d7665c5d0c38d32d061fdf3eda285c014e366991`.

The independent hostile review is
`reviews/order12_k4_doublelex_lrat_hostile_0814a4f4/REVIEW.md`, SHA-256
`fb95934b5d5acd75c9f6deb9142be3b903900f5abd02a5cc21d9884788f38395`.
It independently reconstructed the formula, reparsed and renormalized the
raw binary proof, reran warning-fatal forward and backward RUP checks,
created a byte-identical fresh LRAT, and replayed both retained and fresh
LRATs.  Its exact verdict is
`ACCEPT_EXACT_DOUBLELEX_CNF_UNSAT_ONLY`.

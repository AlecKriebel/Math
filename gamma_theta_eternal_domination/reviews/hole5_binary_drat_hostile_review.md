# Hostile review: binary-DRAT intake for the `hole5` run

## Verdict

**ACCEPT the independent binary-proof plumbing, subject to the production
gates below.**

The clean-room parser and deletion stripper in
`reviews/hole5_binary_drat_hostile_probe.py` can be trusted to transform a
canonical, bounded binary DRAT proof into its exact addition-only byte
subsequence.  It does not itself prove RUP.  Mathematical acceptance still
requires complete replay of that addition-only proof by the pinned checker
with explicit binary, forward, warning-fatal, RUP-only options.

This review launched no production solve, changes no package, and makes no
UNSAT claim for `hole5`.

Review date: 2026-07-25 PDT.

## Bound artifacts

| artifact | SHA-256 |
|---|---|
| `reviews/hole5_binary_drat_hostile_probe.py` | `02c3c00faf7afb91a3217f5b738d0dacf7699875928162d01ce2df97e600007d` |
| `reviews/hole5_binary_drat_hostile_probe_log.json` | `2674cf53eecd881535c6bc4bc2732d669562d7a86816e7bc9057222aadeb3ca8` |
| pinned `drat-trim` | `31df522b8b2b71acd357723b0e826cf488826ed78ad9e3a7bcad241271812beb` |
| pinned `drat-trim.c` | `f7619bdc338bc8151b2f6bb87488052795c926b048d5040cf165742eb1ba9a26` |
| pinned binary-format `README.md` | `fa0b7c5b81b332aad990a1980c5d7a5fda41b153159cf331982bf36d87483054` |
| pinned `compress.c` | `548ba9cbac8f4521b57464b4ea7682d8bbb384f7dd6412b9938de938003956a1` |
| pinned `decompress.c` | `c63af2530f6ebf4cf6ce470488f8fc5db0f8593241ec947e5098aa01363d13c3` |

The log is canonical JSON, binds the exact probe bytes, and is byte-stable
across repeated executions.  Its generation command was:

```text
python3 reviews/hole5_binary_drat_hostile_probe.py self-test \
  --output reviews/hole5_binary_drat_hostile_probe_log.json
```

## Exact binary grammar

A record begins with exactly one byte:

- `61` hexadecimal (`a`) for an addition; or
- `64` hexadecimal (`d`) for a deletion.

Each literal \(l\ne0\) is first mapped to

\[
u(l)=2|l|+\mathbf 1_{l<0}.
\]

Thus positive and negative literals have even and odd codes, respectively.
The literal-code zero is reserved for the record terminator.  Code one is
the otherwise ambiguous “negative zero” and is rejected.

An unsigned code is encoded in little-endian base 128.  Each nonfinal byte
has its high bit set; the final byte has it clear.  The parser requires the
unique shortest encoding.  In particular, `80 00` is not an alternative
encoding of zero and `82 00` is not an alternative encoding of two.

The probe independently reproduced every published boundary:

| unsigned value | canonical hexadecimal |
|---:|---|
| 0 | `00` |
| 1 | `01` |
| 127 | `7f` |
| 128 | `80 01` |
| 258 | `82 02` |
| 16,383 | `ff 7f` |
| 16,387 | `83 80 01` |

It also decoded the README's complete fixture exactly:

```text
64 7f 83 80 01 00       d -63 -8193 0
61 82 02 ff 7f 00       a 129 -8191 0
61 00                    a 0
```

For the intended 6,886-variable formula, literals \(6886\) and \(-6886\)
encode as `cc 6b` and `cd 6b`.  A variable above 6,886 is rejected before
checker invocation.

## Parser and deletion-strip audit

The probe uses only the Python standard library.  It imports no synthesis
encoder, symmetry breaker, solver wrapper, proof recovery, or author
parser.  It streams the proof in bounded blocks and:

1. requires exact `a`/`d` record prefixes;
2. detects EOF both at record boundaries and inside varints;
3. rejects varints beyond nine bytes or \(2^{63}-1\);
4. rejects redundant varint encodings and negative zero;
5. bounds every variable by the caller-supplied CNF variable count;
6. rejects duplicate or complementary literals;
7. rejects an empty deletion;
8. requires exactly one empty addition and requires it to be the final
   record;
9. hashes the original, addition, and deletion byte streams independently;
10. emits only complete validated addition records, byte-for-byte and in
    original order;
11. reparses the output with deletion records forbidden; and
12. rehashes the source before and after parsing and installs only to a new
    path.

The deterministic strip fixture contained five records: three additions and
two deletions.  Its exact 16-byte stream

`61020064040061030600640906006100`

was reduced to the exact nine-byte addition subsequence

`610200610306006100`.

The source addition-stream hash and complete output hash both equal

`d3d175eb7a18bc2cf3c1b49db6c957bbe3bceb112bd63fcc7342fc2d8c8c9d19`.

No literal is decoded and re-encoded during stripping; validated addition
record bytes are copied directly.

## Mutation results

All 20 hostile mutations were rejected with the intended failure class:

- empty proof;
- unknown record prefix;
- EOF immediately after a prefix;
- EOF inside a continuation varint;
- EOF after a nonzero literal without a terminator;
- truncation after a complete earlier record;
- redundant encoding of zero;
- redundant encoding of a nonzero literal;
- negative-zero code;
- varint overflow;
- variable outside the supplied range;
- duplicate literal;
- complementary literals;
- empty deletion;
- a record after the empty addition;
- two empty additions;
- no final empty addition;
- deletion-only input;
- any deletion in an alleged addition-only proof; and
- a raw literal byte where a new record prefix is required.

Valid EOF immediately after the one final `a 00` record was accepted.

## Why the independent parser is mandatory

Pinned DRAT-trim's binary reader is suitable as a proof checker after strict
intake, but it is not a hostile binary-file validator:

- `read_lit` at source lines 983--994 recognizes EOF only before the first
  varint byte.  EOF after a continuation byte is folded into the decoded
  integer rather than classified as truncation.
- The same loop has no canonical-encoding check and no explicit shift or
  integer-overflow bound.
- Proof literals are not subjected to the input formula's range check at
  lines 1148--1151.
- A wrong binary prefix reaches a warning-and-stop path at lines 1106--1114;
  strict acceptance must therefore inspect the entire input independently
  and also reject every checker warning.

These observations do not make a successfully checked proof unsound.  They
mean that DRAT-trim alone is not the correct boundary for malformed binary
artifacts.  The new parser must run first and fail closed.

## Strict pinned-checker smoke

The tiny smoke formula contains all four clauses on two variables:

```text
p cnf 2 4
1 2 0
-1 2 0
1 -2 0
-1 -2 0
```

The source binary proof contains additions \(1\), \(-1\), and the empty
clause, plus one deletion.  The parser stripped the deletion and produced

`6102006103006100`

with SHA-256

`01e30eecffa40b9b4e4fbe9f7dea1efb89f730337b02ec87901f2cf2f92fb7bf`.

The exact normalized command was:

```text
$CHECKER $CNF $ADDITION_ONLY_BINARY_PROOF -i -f -W -U -t 10
```

It exited zero, emitted exactly one warning-free `s VERIFIED`, and reported
zero RAT lemmas in the core.  Stderr was empty.  Normalizing only the
elapsed-time number gives stable stdout SHA-256

`28feef3747c341713589315e32b3cfeecb70b6ef3ce020121465fe6be7dc45d9`.

This verifies all important option directions:

- lowercase `-i` forces binary input;
- `-f` performs forward verification;
- `-W` makes checker warnings fatal where supported;
- `-U` forbids fallback from RUP to RAT.

Autodetection and uppercase `-I` are not acceptable for a binary production
certificate.

## Exact production gates

A forthcoming symmetry-broken `hole5` run may be promoted only if all of the
following pass.

1. **Symmetry coverage.**  The six-vertex signature theorem, exact 315
   comparator clauses, full variable covariance, and equisatisfiability
   argument receive a separate accepted hostile review.  The current author
   files are not accepted merely because this binary audit passed.
2. **Committed source binding.**  Freeze and commit every generator,
   symmetry-breaker, runner, parser, mathematical note, and test used by the
   run.  The manifest must bind their exact Git bytes and report no runtime
   mismatch.
3. **Exact formula binding.**  Independently reconstruct the symmetry-broken
   CNF.  It should have 6,886 variables, 23,968 clauses, and 192,169 literals
   only if the separate symmetry audit confirms the claimed 315-clause,
   3,210-literal suffix and exact original-CNF prefix.
4. **Immutable run input.**  Bind the CNF, package manifest, CaDiCaL binary
   and source, seed, binary-proof command, limits, and all output paths before
   launch.  Retain the first solver proof byte-for-byte.
5. **Solver terminal.**  Require solver exit 20 and an explicit UNSAT result.
   Timeout, signal, file ceiling, memory ceiling, malformed output, or any
   unexpected exit is `NO_MATHEMATICAL_CLAIM`.
6. **Strict binary intake.**  Invoke this independent parser with
   `--max-var 6886` on the immutable proof.  Require canonical grammar, one
   final empty addition, and source stability.  Any rejection is a nonclaim,
   not permission to weaken the parser.
7. **New addition-only artifact.**  Strip only deletion records into a new
   certificate path; never rewrite the source run.  Reparse it with
   deletions forbidden and require its file hash to equal the recorded
   source addition-stream hash.
8. **Strict proof replay.**  Run the pinned checker on the exact CNF and
   addition-only proof with `-i -f -W -U` and a recorded time limit.  Require
   exit zero, exactly one `s VERIFIED`, no warning in either stream, zero RAT
   lemmas, and unchanged checker/CNF/proof hashes before and after.
9. **Independent certificate package.**  Retain parser statistics, every
   source and derived hash, exact commands, stdout/stderr, tool hashes, and a
   one-command replay.  A separate reviewer must check the package without
   importing the search or generator core.
10. **Claim boundary.**  Only after gates 1--9 may UNSAT be combined with
    the already accepted `hole7` and `hole9` exclusions to claim the complete
    finite \((n,k)=(12,3)\) slice.  It would still not resolve the universal
    gamma--theta conjecture.

Within those gates, binary proof recovery is independently trustworthy.
Before them, it is plumbing rather than a mathematical result.

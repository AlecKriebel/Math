# Offline package verification

From an extracted source archive, run:

```sh
python3 -B verification/verify_all.py
python3 -B -O verification/verify_all.py
```

Both commands are read-only and need only Python's standard library. They
authenticate every frozen authored audit member, the full source manifest when
present, and the source/PDF QA pins. They execute `verify_finite_signs.py`
ordinarily and with optimization, compare the entire positive stdout byte for
byte with `EXPECTED_FINITE_SIGNS.stdout.json`, and require four genuine
construction mutations to fail the specified computed property in each mode.
All verification conditions use explicit exceptions and remain active under
`-O`. A PASS field or a matching subset of counts is insufficient.

The two successful processes and eight failing mutation processes are finite
diagnostic support. They do not prove the transfinite or proper-class claims.
Historical family programs using `assert` remain historical evidence; their
optimized executions are not counted as substantive checks.

Private third-party source bodies are intentionally absent. Repeating historic
source-body custody checks requires independently acquiring those bodies and
is optional, separate from this offline verifier. Every released authored
audit member is checked without them. No network request, external message,
deposit creation or publication is performed by these scripts.

To rebuild the two archives without recompiling the frozen PDF:

```sh
python3 -B build_package.py
```

The builder requires a frozen `AUDIT_MEMBERS.json`, complete byte-exact
`REPLAY_RECEIPT.json`, root PDF QA receipt, final source/PDF, README, license and
matching metadata/deposit files. Its three generated destinations (source ZIP,
kit ZIP, package receipt), their existing types and every ancestor are checked
before any output write. Existing regular output files can be atomically
replaced. Symlink members and ancestors anywhere from the filesystem root,
noncanonical/absolute/parent archive paths and case-colliding members are
rejected. ZIP membership is explicit; subsequent operational logs and final
review files do not enter the frozen source archive. Kit payload names are
flat. It contains the exact PDF/source ZIP/metadata and a deposit manifest whose
only difference is portable relative payload paths.

On a platform where a parent directory is a symlink (for example `/tmp` on some
systems), extract under a physical directory path. The guards deliberately
reject symlink ancestry. They do not provide protection against an adversary
concurrently changing filesystem components.

To exercise the packaging controls using small disposable synthetic fixtures:

```sh
python3 -B verification/self_test.py
python3 -B -O verification/self_test.py
```

The fixtures copy the real finite diagnostic but use deliberately synthetic
paper/PDF/metadata inputs. They test deterministic builds, arbitrary-directory
extraction, positive-output tampering, masked mutations, member tampering,
unsafe allowlist paths, output types, and symlink members/ancestors in both
ordinary and optimized processes. They never write to the actual released
inputs or existing outputs. Fixture folders are created beneath the audit's
`families/package_tooling_01/private/` directory and removed on completion;
source integrity verification itself is read-only.

Deterministic ZIP rebuilding assumes the same Python/zlib implementation.
The fixed member bytes and manifest remain independently verifiable across
implementations. An external archive checksum or immutable DOI authenticates
the manifest; a self-contained unsigned archive cannot detect wholesale
reauthoring of its own manifest and payloads.

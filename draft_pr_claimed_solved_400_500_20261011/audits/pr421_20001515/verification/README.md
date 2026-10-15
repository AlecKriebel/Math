# PR421 / 20001515 verification delivery

This standard-library-only packet reproduces the finite certificate for

```
G = <a,b,c,t | tat^-1=a, tbt^-1=ab, tct^-1=bcb>.
```

The written construction in `packet/ATTEMPT_1.md` is primary. Its finite quotient
has cells `(1,7,8,2)` and link f-vector `(14,32,16)`. The written reversible
presentation calculation and cubical local-to-global theorems establish the
group identification and geometric action. Executable checks corroborate the
finite data; a PASS is not a formal proof-assistant certificate, a substitute
for the global written proof, or a guarantee of source identity or priority.
Read the current dated `PUBLICATION_ADDENDUM.md` together with the frozen notes.

From this directory, using an installed Python 3.9 or later:

```sh
python3 verify_bundle.py
python3 -O verify_bundle.py
```

Each command checks the positive file inventory and SHA-256 pins, then directly
launches all three accepted scripts in both normal and optimized modes. It uses
fresh copies in temporary directories containing spaces, with a working directory
outside each packet. It deletes all three saved results before every launch.
The full check also runs three SHA tampering controls, seven mathematical/proof
corruptions in both modes, and a relocated complete bundle with its driver under
`-O`. The default commands leave the delivered files unchanged and remove their
temporary copies. No network, packages, virtual environment, compiler, or
system configuration changes are used.

To select a different installed interpreter or run just integrity and six clean
baselines:

```sh
python3 verify_bundle.py --python /absolute/path/to/python3
python3 verify_bundle.py --baseline-only
```

Success prints one JSON report with `status: "PASS"`, six `baseline_runs`, three
`negative_controls.sha_tampering` records, fourteen
`negative_controls.mathematical_data` records, and a successful `relocated_bundle`
record. The reduced `--baseline-only` command sets the last two fields to null.
Failure exits nonzero and writes `VERIFICATION FAILED: ...` to stderr. The driver
has no bare `assert` gates, so its checks remain active under `-O`. Reports print
to stdout; to save a report, redirect it to a file outside this delivery directory.

Expected output handling is specific to each script:

| Accepted program | Fresh output checked | Pinned historical baseline |
| --- | --- | --- |
| `packet/verify.py` | Full stdout JSON; does **not** generate `checks.json` | `packet/checks.json` |
| `packet/audit/independent_audit.py` | Newly written full `audit/independent_results.json`, plus its six-key stdout projection | `packet/audit/independent_results.json` |
| `packet/audit/independent_algebra.py` | Newly written full `audit/independent_algebra_results.json`, plus the identical full stdout JSON | `packet/audit/independent_algebra_results.json` |

All canonical fresh outputs must match the corresponding pinned baselines and
normal must agree with `-O`. Both newly written full files also match the saved
baseline bytes exactly. The geometric summary is never substituted for the full
geometric result. The author and geometric programs each report seventeen
internal finite controls; the algebra output has nine identity relation checks
for the exact positive-final-b automorphism. The driver additionally falsifies
actual cube data, a cube corner, a cube side, inverse monodromy, and proof bytes.
Controls run only on disposable copies and must raise `AssertionError` before
any successful stdout or result file.

`packet/` preserves the exact thirteen-file source layout at PR head
`d5bf8b5a25cabb177433338fae60af52ebfecf1c`, replacing only these paths with the
accepted optimization-safe programs:

| Program path | SHA-256 |
| --- | --- |
| `verify.py` | `e3357a9af58d68c2f450d2901ab71c58ed955112017fe0ec758d1adc3b36ca42` |
| `audit/independent_audit.py` | `281ebf97900d047447a2a3865f233cfba1c41df6dd6c4e8aaae66150250b1903` |
| `audit/independent_algebra.py` | `3fda0f889aa454390c6f30c54c842a0a49a5f5a3d1bdea0bce5819711e3dbc96` |

The unchanged proof pin is
`c022afdfe003d0692a032cee48855ddf712de22953b358b895c485215875d8a6`.
The three saved output files in `packet/` are explicitly historical baselines;
they are not evidence that a current launch succeeded. Frozen source notes and
old WIP hashes retain their historical dates and limitations. Original unsafe
scripts are omitted; their exact historical hashes are provenance only.
No peer reviewer scripts are included or covered by the three-program repair.

The accepted scripts require ordinary standalone execution with the standard,
unshadowed builtin `AssertionError`. The driver uses isolated Python launches
with `-I -S -B` and optional `-O`. It does not promise equivalence under foreign
embedding, injected globals, or altered builtins. The geometric program needs
the pinned proof in its source-relative parent and a writable `audit/` directory;
copying the whole packet supplies this layout.

`SOURCE_RECEIPT.json` binds the historical source and accepted overlays to the
controlling acceptance evidence. `MANIFEST.json` hashes every delivery file
except itself and `PUBLIC_OUTPUT_WHITELIST.json`, avoiding a hash cycle. The
positive whitelist hashes the same files plus `MANIFEST.json`; it explicitly
omits its own self-hash. The driver rejects unlisted files/directories, symlinks,
inventory disagreement, or incorrect hashes, and independently hard-pins all
thirteen packet files. These unsigned integrity records detect accidental
changes; authentication against coordinated replacement requires a separately
trusted digest of the delivery, manifest, or whitelist.

`BUNDLE_REPORT.md`, `EXECUTION_EVIDENCE.json`, and `RESEARCH_LOG.md` record the
delivery checks and limits. Verification used an OS-installed Homebrew Python
3.14.6 without dependencies. The macOS `/usr/bin/python3` launcher could not run
because this host has an unaccepted Xcode license; no claim is made for that
launcher, and no host license/setup was changed. Both full-package adversarial
reviews required before publication remain outside this preparation task.

Copyright 2026 Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X.
The included original materials are licensed under CC BY 4.0; see `LICENSE`.
This is unrefereed research developed and checked with extensive AI assistance.
Original author budget remains `1/5`; this delivery adds zero proof-search turns.

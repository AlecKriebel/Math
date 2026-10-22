# Target-specific portable verification tool

This tool authenticates only PR888 / PID30005079 at head
`a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7`. The original21files total98055bytes;
the original claimed effort is1/5. Mathematical acceptance, historical priority,
novelty, human peer review and publication approval are separate questions.

Authenticate the launcher and the independently supplied manifest SHA256 before
executing it. A program cannot establish the trustworthiness of its own startup
bytes. The package index deliberately excludes itself. Its SHA256 must come
from an independent record. The current publication manifest has the same
external-pin requirement and self-exclusion rule.

## Dependencies and execution

Use CPython3.11 or later with `-I -S -B`. Actual tests used CPython3.14.6 and
zlib recorded in the build receipt. Obtain the two official wheel files named
in [dependencies.json](dependencies.json) from its exact URLs, place only those
two files in a dedicated directory, and independently check their whole-file
byte counts and SHA256 values. Do not unpack or install them for this workflow.
The verifier performs no network request, package installation or implicit
environment change. The wheels are not publication payloads.

The verifier authenticates complete wheel bytes, excludes wheel bytecode,
site hooks and native extensions, copies those bytes to private temporary
storage, and imports SymPy1.14.0 and mpmath1.3.0 directly as ZIPs. It checks
versions and actual import locations. `-I -S` excludes ordinary site processing,
the current directory and PYTHONPATH. CPython, its standard library, native
standard-library extensions and any standard-library bytecode remain trusted,
unhashed runtime inputs. This is not an operating-system sandbox.

Portable package commands, with an independent package-index digest `PIN`:

```text
python3 -I -S -B portable.py verify PIN --verify-only
python3 -I -S -B portable.py verify PIN --dependency-dir WHEEL_DIRECTORY
python3 -I -S -B portable.py build PIN OUTPUT_DIRECTORY/rank-two-fano-verification.zip --dependency-dir WHEEL_DIRECTORY
```

`--verify-only` performs package authentication and executes zero archival
code. The build command does not accept `--verify-only`; every build requires
the complete replay. Its output must be fresh, outside every indexed input
directory and any dependency/primary-source directory, with no symbolic-link
traversal in the output parent. Directory identity checks include every input
directory derived from the closed inventory, including physical APFS aliases.
The final file is linked atomically without replacing an existing file.

Current outer publication checks use the independent current-manifest digest:

```text
python3 -I -S -B portable.py current CURRENT_PIN --dependency-dir WHEEL_DIRECTORY
python3 -I -S -B -O portable.py current CURRENT_PIN --dependency-dir WHEEL_DIRECTORY
```

The outer layout requires the exact two deposit asset names
`rank-two-fano-note.pdf` and `rank-two-fano-verification.zip`, a `verification/`
portable tree, and equal outer/inner copies of the launcher, actual TeX source,
metadata and deposit declaration. It validates the closed inventories,
metadata identity, sole author/ORCID, exact two deposit entries and ZIP bytes.
It authenticates the PDF under the external current manifest and checks its
PDF header; it does not validate PDF rendering, TeX-to-PDF correspondence or
mathematical content. Those require the independent paper review/rendering.

## Original replay and optimization contract

All original files stay byte-for-byte unchanged. Their SHA256, Git-blob SHA1,
file counts and total size are checked against the independently frozen source
manifest before any original code executes. JSON rejects duplicate keys,
NaN and nonfinite numeric overflow. Inventories reject untyped sizes, unsafe
or non-ASCII paths, aliases, symbolic links and unlisted files or directories.

The original root explicitly rejects actual optimized Python. Therefore the
wrapper always launches that unchanged root with **actual optimization0**,
even when the current verifier itself runs with actual `-O`. The receipt
separately records the actual outer, root and checker modes; no `sys.flags`
value is spoofed. The root and checkers compile with explicit `optimize=0`.
The two original root subprocess requests are narrowly checked and routed to
isolated checker bootstraps. Actual checker optimization follows the actual
outer mode, so the optimized-current run really executes optimized checker
processes while retaining original assertions through explicit compilation.

Each complete replay starts one actual original-root process and six actual
checker subprocesses: two positives, two negative controls that make original
assertions fail, and two damaged-code hash rejections before original checker
execution. The author negative changes SymPy integration inside that child;
the independent negative changes only its private candidate input. Positive
original stdout and generated JSON must match exact original bytes. Root output
must match its exact semantic contract and current Python version. The original
four-edition, three-transition chain runs, followed by three in-process damaged
patch-context rejections. These last three controls are not subprocesses.

The archived root's output includes historical statements about its AI audit
reports. Reproducing that output does not endorse those statements or promote
them to a present mathematical or publication verdict.

## Source-only authentication

```text
python3 -I -S -B portable.py source-only --catalog CATALOG --problems PROBLEMS --reports REPORTS --primary-dir PRIMARY_DIRECTORY
```

All three **complete** native corpora must pass their fixed whole-file pins
before any target extraction. The exact native catalog/problem pair is
serialized with insertion order, indent2, `ensure_ascii=False` and a final
newline:5415bytes, SHA256
`6bbb2826e583f9ccbbb38411ce780e865c0b9564b74bf9f6eca5250f4b06e083`.
The target report is absent; none is invented. The whole statement is separately
bound. This command does not read or execute archival candidate code, and it
does not copy corpora or primary-source bodies into publication artifacts.
The optional primary directory is a closed seven-file inventory, including
the precise BLXZv2 body. Hash authentication does not verify a paper's theorem.

## Archive and audit scope

Generated ZIPs use ASCII-sorted regular0644members, DEFLATE9 and fixed
2026-10-16T00:00:00Z timestamps. Verification checks every local record, central
record, terminal EOCD, field agreement, exact raw-DEFLATE consumption, payload,
CRC and absence of gaps, trailers, comments and extras. An independent second
ZipFile construction must reproduce exact ZIP bytes. Compressed-byte
reproducibility is limited to the same Python ZIP implementation and zlib;
cross-runtime compressed-byte equality is not promised.

The separate `independent_zip_rebuild.py` audit helper additionally rebuilt
the private fixture archive through manually authored local/central/EOCD
records and direct zlib compression. It imports neither this launcher nor the
ZipFile writer. Its actual bytes exactly matched the default build, as recorded
in INDEPENDENT_ZIP_REBUILD_RECEIPT.json. This remains a same-runtime check.

The engineering fixtures are private and contain a clearly labeled placeholder
PDF header. They are neither a paper PDF nor a publication package. The current
normal/optimized and outside-build receipts establish real wrapper execution,
not final parent-artifact clearance. Independent adversarial review of this
specific tool version is recorded separately by the parent.

Public audit payloads are explicitly listed in SAFE_PAYLOAD_MANIFEST.json.
That manifest excludes itself and needs an external SHA256. Private corpora,
primary PDFs, wheel bodies, runtimes, fixtures, failed raw traces and scratch
files are excluded. No external individual was contacted and no Git, remote,
PR, queue, DOI or deposit state was changed by this engineering effort.

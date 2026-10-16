# KP-4.84 / problem 2960: audited partial results

**Unsolved; five mathematical approaches completed (5/5).** The original report is
accepted without mathematical changes. This packet separately integrates the
independent audit's checker hardening. It does not claim a full solution or novelty.

## Read first

- [Acceptance and limitations](ACCEPTANCE.md)
- [Unchanged mathematical report](original/REPORT.md)
- [Unchanged independent audit](audit/AUDIT.md)
- [Actual hardening patch](audit/exact_checks_hardening.patch)
- [Separate corrected checker slice](corrected/README.md)

The target asks for one closed oriented smooth four-manifold on which every
prescribed finite subgroup of its smooth mapping class group has an exact
orientation-preserving diffeomorphism action in those prescribed components.
The strongest positive result here realizes all finite subgroups of the standard
product-and-factor-swap subgroup on products of closed surfaces. It does not
control the entire smooth mapping class group or its homotopically trivial kernel.

The 7 original and 10 audit files are byte-preserved. The corrected slice has its
own manifest and records actual zero-fuzz patch application. No third-party source
text, copied paper, image, dataset contents, or private coordination file is included.

## Authentication and reproduction

Obtain the SHA-256 of `BOOTSTRAP.py` from a trusted external publication record
(such as the reviewed draft PR body), independently hash the file, and compare
before running it. A freshly computed hash alone is not authentication. The pinned
bootstrap binds the publication manifest and exact verifier bytes before execution.
The verifier pins every accepted original, audit, and corrected member separately.

Use Python 3.12 with actual real/effective UID 1000 and `/usr/bin/patch` available:

```
python -I -S -B BOOTSTRAP.py /absolute/path/to/this/packet
python -I -S -B -O BOOTSTRAP.py /absolute/path/to/this/packet
python -I -S -B -OO BOOTSTRAP.py /absolute/path/to/this/packet
```

The complete corrected and independent results must equal their frozen JSON bytes.
The wrapper replays the unchanged audit's 36-run harness, applies the actual patch,
and executes eight additional read-only semantic controls at its current optimization
level. The corrected checker and independent six-point-permutation wreath calculation
run from genuinely read-only copies; attempted writes must fail as UID 1000.
The caller needs writable temporary space; the packet and working directory need
not be writable. The wrapper emits the full exact mathematical results in its JSON.

For publication-boundary controls, first authenticate both the bootstrap and
`mutation_tests.py` through the externally anchored publication manifest, then run:

```
python -I -S -B mutation_tests.py --root /absolute/path/to/this/packet --bootstrap-sha256 TRUSTED_EXTERNAL_BOOTSTRAP_SHA256
```

Repeat with `-O` and `-OO` before the script path. The controls test exact inventory,
schema, path safety, symlinks, linked ancestors, special files, altered/re-pinned
accepted evidence, external bootstrap rejection of a substituted verifier, and
relocation into read-only directories under hostile Python environment variables.

## Important limits

The unchanged original checker contains 17 optimization-removable assertions.
Its four corrupted variants each falsely emit PASS under both `-O` and `-OO`
(eight false passes), and it fails when its adjacent output path is read-only.
Those failures are deliberately reproduced and disclosed. Use the corrected checker
for direct finite checks, or the anchored bootstrap for complete packet acceptance.

A PASS concerns only explicitly executed integrity and finite algebra checks.
Fresh source and dataset verification are `NOT_RUN` in this source-free replay.
The historical audit's seven PDF bindings and two public dataset bindings are retained
as historical evidence. Illman's original full text remains uninspected; the
external equivariant-triangulation input is identified rather than machine-certified.
The literature search was bounded, and novelty is not established.

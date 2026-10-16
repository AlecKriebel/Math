# PR #872 verification-engine templates

These are engineering templates for a later reviewed package. They are not a
manuscript, mathematical acceptance, priority acceptance, final verification
archive, or permission to publish. Keep all 15 frozen originals and all 26 ZIP
members unchanged. The original proof effort remains 1/5.

## Portable assembly contract

Place `check_originals.py`, `verify_package.py` and, optionally,
`build_verification.py` at the portable root. Place the 15 unchanged original
files in `source/`, and the unchanged externally frozen `SOURCE_MANIFEST.json`
in `root_evidence/`. The source-manifest SHA256 is
`4589f9b70e9a65ae67356544b5ad59644290902bb9b3df80406710a22559e3f8`.
The parent may add its separately reviewed note, source, metadata, README and
public evidence. These templates never create or accept that material.

Create `package_index.json` with exactly the following keys:

```json
{
  "schema": "random-property-t-verification-v1",
  "problem_id": "30006628",
  "files": [
    {"path": "README.md", "bytes": 123, "sha256": "actual-lowercase-sha256"}
  ]
}
```

Every regular file except the index itself must have one exact row. Include
the startup verifier and original checker. The example row is illustrative,
not a usable pin. Paths must be canonical relative POSIX paths; no empty,
dot, parent, absolute, colon, backslash or control-character components. The
package must have exactly these files and their necessary parent directories;
extra files and even extra empty directories are rejected. Member counts are
derived from the external index, not a future hardcoded package size. The
index permits at most 10,000 rows, 256 MiB per file, 512 MiB total payload and
4 MiB for the index.

Obtain the index SHA256 and startup-code hashes from an independently trusted
acceptance record before running downloaded code. A script cannot establish
its own startup trust. A mutable index beside mutable code is not an
independent trust anchor. Likewise, authenticate the builder or this probe
harness before executing it. The builder requires both the index and verifier
digests as arguments and rejects mismatches before executing copied verifier
bytes. `verify_package.py` verifies the complete index and every payload
before executing a copied checker.

## Commands

Use a trusted Python 3.10 or newer, its standard library and zlib. For an
authenticated portable root, from any working directory:

```text
python3 -I -S -B /path/to/verify_package.py INDEX_SHA256 --root /portable/root
python3 -I -S -B /path/to/verify_package.py INDEX_SHA256 --root /portable/root --full
python3 -I -S -B /path/to/check_originals.py --root /portable/root --verify-only
python3 -I -S -B /path/to/check_originals.py --root /portable/root
```

The full replay authenticates all 15 originals, the historical 14-entry outer
inventory, all three archive manifests and 26 members, and the three readable
duplicates. It runs the three distinct finite diagnostic programs in both
normal and optimized child modes: six positive and eight intended-negative
receipts, 14 total. It compares positive stdout byte-for-byte with frozen
outputs and negative stdout with the exact intended reason. It does not run
the historical wrapper, whose originals and limitations remain preserved.

To add the fourth archived program's provenance replay, supply all four
arguments `--catalog FILE --problems FILE --reports FILE --pdf-dir DIRECTORY`.
For `verify_package.py`, this requires `--full`. All three complete corpus
files and six historical PDF versions must match their frozen byte and hash
pins. Every supplied leaf is screened as regular and exact-sized before any
source payload is read; actual bounded reads repeat leaf and open-descriptor
checks. All corpora also undergo duplicate-key/nonfinite JSON rejection. Raw
sources remain temporary and are never emitted. This adds two positive and
four intended-negative receipts across the modes, for 20 total. The original
source program checks the complete exact-ID record pair and catalog binding;
this is provenance reproduction, not fresh retrieval or source-proof review.

To build from a complete independently reviewed assembly:

```text
python3 -I -S -B /trusted/build_verification.py /assembly INDEX_SHA256 VERIFIER_SHA256 /fresh/output
```

The output must be outside the input tree and fresh or empty. Existing output
files are preserved by rejection. The builder authenticates the index and
all payloads, executes authenticated copies with a full finite replay, and
only then writes `verification.zip`. Entries are sorted, regular 100644,
deflated at level 9 and dated 2026-10-15 00:00:00 UTC. Byte reproducibility is
claimed only for identical inputs and the same Python ZIP implementation and
zlib; a different compressor is not promised to emit identical bytes.

Add `-O` to any invocation to exercise the same explicit guards under optimized
Python. No correctness guard relies on `assert`. Every authored subprocess
uses `-I -S -B`; the diagnostic children are deliberately run in both modes.
These switches harden runtime startup and import behavior; they are not an
operating-system sandbox.

## Path and trust boundaries

The selected root is resolved, so aliases in its ancestors or for that root
are allowed. Symlinks and other nonregular entries *inside* a portable tree
are rejected. Supplied corpus leaves and PDF leaves reject aliases; aliases
of their chosen ancestor directories, including the selected PDF directory,
are allowed. Pre-read `lstat`, `O_NOFOLLOW` where available, nonblocking opens,
and descriptor `fstat` reject FIFOs/devices/leaf aliases. Reads are bounded by
pinned sizes. This assumes a trusted local filesystem/runtime and no hostile
concurrent replacement of ancestor directories. It does not claim to defend
against a compromised Python, kernel, filesystem or trusted acceptance record.

ZIP members must have safe paths, unique inventories, expected bounded sizes,
unencrypted supported compression, no executable permissions and regular
type metadata. The historical first-review archive omits the Unix file-type
bits (mode 0600); type bits zero are treated as implicit regular files. FIFO,
device, symlink, directory and other explicit types are rejected. Members are
read as authenticated bytes, never extracted by a ZIP extraction API.

Finite enumerations and mutation guards cannot certify an all-length
asymptotic theorem, spectral or concentration arguments, published-source
validity, novelty, human peer review or formal proof checking. Those require
the separate mathematical and priority review and final package adversaries.

## Reproduce engineering probes

After authenticating the harness and three templates:

```text
python3 -I -S -B /path/to/adversarial_probes.py --original-base /audit/pr872_30006628 --templates /templates --output /new/PROBES.json
```

Repeat with `-O`. Add `--full-sources --repo /repository` when the three pinned
corpora and six PDFs under the audit's private source directory are available.
Only temporary engineering fixtures are built; no final paper or deposit is
created. Results classify ordinary rejections, startup rejections with marker
code unexecuted, positive controls, and artificially resealed parser branches
separately. The latter deliberately replace trusted pins to reach semantic
guards and are not successful attacks against fixed external digests.

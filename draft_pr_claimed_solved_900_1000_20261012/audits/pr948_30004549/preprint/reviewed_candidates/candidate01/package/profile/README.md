# Strict finite publication verification profile for PR948

This is a new engineering entry point. It preserves the historical original24 and the sealed computation-family audit unchanged. It adds zero author proof responses. The PR declares4/5 author turns; native per-turn history and the historical total remain unknown. No scientific promotion, priority, publication acceptance, or independent review of this profile is implied by development tests.

## Invocation and trust boundary

Use the externally authenticated driver and an independently obtained manifest hash:

```text
TRUSTED_PYTHON -I -S -B verify_package.py --root /absolute/package --manifest-sha256 EXTERNALLY_OBTAINED_64_LOWERCASE_HEX
TRUSTED_PYTHON -I -S -B verify_package.py --root /absolute/package --manifest-sha256 EXTERNALLY_OBTAINED_64_LOWERCASE_HEX --run-checkers
```

The outer process fails closed unless isolated mode, no-site startup, and no-bytecode mode are already active. The check also applies when importing the driver as a module. A guard cannot undo effects of an unsafe interpreter startup; use the flags from launch. The driver must itself be trusted independently, such as through the release freeze. A self-rebound manifest/sidecar is not an independent anchor. No optional unlisted checksum sidecar belongs inside the closed package.

Default verification uses only Python's standard library. The optional replay needs SymPy1.14.0 installed in the trusted interpreter environment. Actual development execution used only CPython3.14.6 and SymPy1.14.0 on this host; other Python/OS versions are untested.

The checker children use the same interpreter with explicit `-I -B`, a minimal sanitized environment, fresh empty temporary working directories, and compilation with optimize0 regardless of outer optimization. Children intentionally allow **trusted installed site packages** so SymPy is available. User-site and ambient PYTHONPATH/sitecustomize poisoning are excluded by startup/environment isolation, but installed dependencies and system site customization are trusted. This does not make the host, dependencies, files, or arbitrary programs safe.

## Exact envelope schema

The sole envelope is PACKAGE_MANIFEST.json. It has exactly these keys:

```json
{
  "schema": "pr948-sourcefree-package-v1",
  "version": 1,
  "problem_id": 30004549,
  "original_head": "be4313efafa1af5962394e07d8a4debff2e94d92",
  "files": {
    "verify_package.py": {
      "bytes": 123,
      "sha256": "64 lowercase hexadecimal characters",
      "mode": "100644"
    }
  }
}
```

The displayed entry is a schema illustration, not an actual record. Values for version/problem_id/bytes must be exact Python JSON integers, excluding booleans and floats. All entry objects have exactly bytes/sha256/mode. The manifest omits itself and includes every other regular file, including the driver and any selected public tests/docs. Its exact UTF-8 bytes are anchored by the supplied SHA256; duplicate keys, nonfinite numbers, malformed structures, unknown schema keys, and incoherent metadata reject.

Git mode100644 means a regular Git blob. Every actual payload file and the envelope must instead have disk permission0644 and one hard link. These distinct representations are checked explicitly. Directories are real directories and must be exactly those implied by the file paths, so extra empty directories reject. Root and ancestor symlinks, payload symlinks/hardlinks/FIFOs/devices/sockets, extra/missing files, and noncanonical paths reject. Paths use a portable ASCII subset, at most512 characters, no Windows device names, case aliases, traversal, repeated separators, or trailing dots. Do not put this profile's private development fixtures/log scratch into the assembled release.

Case aliases are checked across the combined file-and-directory namespace, including implied ancestors. Thus A/one with a/two, a file A with a directory a, and a file also used as an ancestor all reject. ZIP members receive the same combined-namespace check before decompression. Filesystem-neutral namespace regressions cover collisions a case-insensitive host cannot represent; a real-tree wiring check verifies that actual directory names reach the check, and concrete ZIP regressions exercise the full archive helper.

## Fixed limits

The tree is scanned for object type, mode and bounds before any payload file is read:

- At most512 files including the envelope,128 subdirectories, and12 path components.
- At most8MiB per file and32MiB total; the manifest is additionally capped at128KiB.
- Exactly24 immutable original files below original/unsolved_math_prioritization/attempts/30004549/. Their byte counts, SHA256, Git blob IDs, and100644 modes are constants generated from independently authenticated immutable Git records.
- ZIP metadata is checked before decompression: at most512 members,8MiB/member/archive bytes,32MiB cumulative expanded bytes, compression ratio at most200, stored/deflate only, no encryption, regular Unix0644 or100644 attributes, canonical unique names, no raw-name truncation. There is no extraction. The historical ZIP additionally requires its exact7 expected member paths and contents plus the fixed whole-archive SHA256.
- Each fixed checker child is limited to60 seconds wall time,64KiB captured stdout and16KiB captured stderr; source is at most16KiB. Output readers enforce the caps while the process runs. A false-assertion guard must fail. Child runtime flags/versions, canonical stdout hashes, and environment key names are reported.

A generic `inspect_archive(data, expected=None)` helper exposes the same archive profile for an outer release archive; checking an outer archive is separate from checking its extracted package tree. The root must separately construct and authenticate the outer archive.

## Development test invocation

The test runner takes explicit source and output directories so it can be included in a closed release without writing into that release:

```text
TRUSTED_PYTHON -I -S -B test_profile.py --driver /absolute/verify_package.py --originals /absolute/authenticated/original24 --output-dir /absolute/owned-development-output
```

Keep --output-dir outside a closed package tree. It holds small receipts, append-only progress events, and an owned private_fixtures directory whose temporary contents are cleaned. The suite replays the3 genuine frozen checkers under standard/optimized/poisoned outer environments and tests startup guards, malformed scalar/schema/path/hash cases, coherent rebinds without the external anchor, immutable-original changes, file/directory/count/size bounds, FIFOs/links/socket objects, pre-decompression ZIP attacks, and actual child wall/output caps. The socket test uses a short relative bind inside its owned fixture directory. Platform skips are reported as skips, never passes.

An unisolated positive control must execute the owned import poison before the hardened run is accepted as ignoring it. This distinguishes a valid poison fixture from one that simply was not reachable.

## Explicit remaining limitations

This verifies an externally anchored finite package and replays trusted, fixed local checks. It is not a signature, an OS or hostile-dependency sandbox, a proof assistant, a global mathematical argument, human peer review, a priority/novelty determination, or journal acceptance. Concurrent hostile filesystem mutation is outside the trust model; final-component no-follow/nonblocking opens, stat identity checks and in-memory authenticated checker sources reduce ordinary races but do not establish hostile-OS security. Wall/output limits do not cap child memory, CPU, filesystem writes, or descendants. Only pinned reviewed checker sources are executed.

Historical audit A/B assertions remain disabled when users run those old scripts directly with -O; this new entry point always forces assertions. The old wrapper remains historical and unmodified. Its limitations are retained in the sealed family report; this new profile is a separate implementation requiring fresh review of the entire eventual package.

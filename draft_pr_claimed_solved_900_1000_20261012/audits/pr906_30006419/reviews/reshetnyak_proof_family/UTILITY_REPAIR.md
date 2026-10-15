# Utility repair without a mathematical revision

The active review utilities were repaired after the enclosing audit identified
that Python `assert` validation disappears under `-O` and `-OO`, and that the
initial verifier assumed a workspace-only original-packet layout. All ten
initial sealed public files, including the initial manifest, are preserved
byte-for-byte in `history/initial_revision/`. These historical utilities are
evidence of the initial revision; the active utilities are the supported
verification entry points.

`independent_controls.py` now uses explicit exception guards and binds its
serialized result to the original control-result SHA-256. It also permits an
explicit `--output` for disposable checks. Its mathematical inputs and result
remain byte-identical to the initial revision.

`verify_manifest.py` now discovers an ancestor `ORIGINAL_SNAPSHOT.json` or
accepts `--audit-root`. It supports both `original/<full snapshot path>` and
standalone `original_packet/<suffix after the attempt prefix>`. It binds the
head, original proof, entire snapshot, canonical packet hash map, original
control result, and initial history manifest to fixed pins. A fixed set of
public file names closes the review allowlist. Directory scanning rejects
unlisted files and directories, symlinks, and special entries; `lstat` and
regular-file guards precede content opens, including when the manifest itself
is replaced by a FIFO. Only fixed ignored private directories are excluded.

The manifest does not hash itself. The active manifest hashes the historical
initial manifest as a regular, already-fixed history artifact; that history
manifest hashes only its nine initial files. This is an acyclic integrity
relationship. A distributor must externally seal the active manifest.

`utility_repair_checks.py` creates fresh workspace and standalone packages
using only allowlisted public files and unchanged original packet files. It
runs the active verifier and controls under normal Python, `-O`, and `-OO`.
Mutation controls cover altered public files, missing or extra files, extra
directories, manifest expansion, symlinks, listed/unlisted/manifest/original
FIFOs, original proof and self-consistent snapshot tampering, history and
history-manifest tampering, rewritten control results, a false scalar control
guard, and a wrong control-result pin. Fixtures are automatically removed
from ignored `private_tmp/`. No source PDF/text is copied into fixtures or
history. The exact receipts are in `UTILITY_REPAIR_RESULTS.json`.

All **126 receipts passed**: 18 valid package/control runs and 108 expected
mutation rejections across both layouts and all three Python modes. The three
active utilities contain zero `Assert` syntax nodes. Normal and optimized
control runs reproduce the exact original result hash
`e022ef5834ae41f135a308818af975d612c59af0fc4e836ee397a4e451b02783`.

These repairs change verification and distribution utilities only. The
analytic theorem, proof reconstruction, six analytic control families, source
scope limits, and absence of a central mathematical gap remain unchanged.

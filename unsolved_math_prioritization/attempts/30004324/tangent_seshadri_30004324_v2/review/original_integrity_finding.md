# Original verifier extra-file bypass

Status: REVISE_REQUIRED for the original verifier's advertised exact-file-set guarantee. This is not a mathematical proof gap, and the actual 13-file author freeze contains no unexpected file.

The frozen `verify_manifest.py` scans all descendants but excludes every file whose basename is `MANIFEST.json`. Thus it excludes both the intended root manifest and an unexpected file such as `extra/MANIFEST.json`.

In an isolated temporary copy, adding `extra/MANIFEST.json` with arbitrary text and leaving every original byte unchanged resulted in exit code 0 and a reported pass with twelve payload files verified. The freeze itself was never edited. The author's ten negative controls do not cover this case.

The accompanying independent verifier excludes only the exact root-relative path `MANIFEST.json`. It also validates canonical relative paths, duplicate entries, nonnegative integer sizes, SHA-256 format, regular file types, symlinks, exact file sets, and optional external binding of the root manifest.

The accompanying adversarial test accepts a clean generated fixture and rejects fourteen mutations, including the demonstrated nested-manifest case. It runs only in temporary fixtures. The independently authored audit packet and the original exact author directory both pass the strict verifier.

Before presenting the original verifier as fail-closed, replace it in a separately versioned derivative packet or clearly supersede it with the strict verifier. Preserve the old freeze and its audit binding. Any derivative packet needs a new manifest and external archive hash. No change to the proof is required by this finding.

# Corrections and observations

## Blocking corrections

None. The frozen mathematical claims, proof scope, source limitations, and unsolved 5/5 disposition are accepted as written. Do not edit or refreeze the package for this audit.

## Nonblocking observation: strict manifest allowlist

The frozen README describes a full public-file allowlist. The supplied verify_manifest.py excludes every file named SHA256SUMS.json, including nested files, and all files below a directory named __pycache__. In a disposable copy of the package, adding nested/SHA256SUMS.json and __pycache__/ignored.txt did not make that verifier fail.

This does not invalidate the actual package. The independent audit enumerates all files without these exclusions and verifies exactly the nine manifest entries plus the root manifest, with no symlinks or extra files.

For a future general-purpose verifier, exclude only the exact root manifest path and either forbid generated cache files or document the cache exception instead of calling the allowlist exhaustive. This optional hardening is not requested as a frozen-package change.

## Component quantifier clarification

Proposition 2's phrase “every connected component” is read in its stated modulus-one context. Its proof supports every connected component of {|F|=1}. No claim about every modulus is needed or used. Adding “of this modulus-one level” would be optional editorial clarification, not a mathematical correction.

## Publication-label clarification

Older saved repository guidance uses a different label for a fifth unfinished attempt. The current campaign coordinator explicitly confirmed unsolved 5/5 for this publication. No queue or repository write was performed by the auditor.

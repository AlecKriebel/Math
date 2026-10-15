# Fresh PR195 whole-package adversary 01

Read REPORT.md for the scoped CLEANPASS and limits. REVIEWED_INPUT_PINS.json binds all fourteen reviewed inputs; ARCHIVE_INSPECTION.json binds all fifty-five ZIP entries. SOURCE_CHECKS.json records primary source pins without redistributing them. COVERAGE.json records review methods. REPLAY_STDOUT.json preserves the fresh standalone package replay result.

Run the newly authored independent corroboration with Python 3.11 or later:

```text
python3 -E -S -B -P independent_controls.py
```

Its JSON must match INDEPENDENT_CONTROLS.json. It imports no package implementation. Genericity remains a proof obligation met by the open-set argument; coordinate checks alone do not certify a gin.

Private extraction, downloaded publications, text and page renders are excluded. SAFE_ALLOWLIST.json is the exact public-safe output set. HASH_MANIFEST.json authenticates all ordinary safe files including the allowlist and excludes itself. Safe files were frozen 0444. No reviewed input, remote state, publication or Git state was changed.

# Independent audit: problem 30002495

**Verdict:** accept the stated partial mathematics and source scope; retain **unsolved, 5/5**. No mathematical proof patch is needed. A narrow correction is required for optimization-safe finite-control replay.

The frozen original manifest is pinned by SHA-256:

`6c41bb59af46e93ffdc169484847271bbec0a6fc178673d491cf8ec9e41244ea`

## Contents

- INDEPENDENT_AUDIT.md: complete proposition-by-proposition audit, exact target/source review, endpoint diagnosis, gaps, and verification findings
- ACCEPTANCE.json: machine-readable disposition
- SOURCE_REVIEW.json: public citations, inspection scope, PDF hashes and byte counts; no source copies
- OPTIMIZATION_SAFETY.patch: minimal correction to the original checker
- check_controls_hardened.py: corrected checker; same arithmetic and same positive output
- audit_controls.py and AUDIT_CONTROL_RESULTS.json: externally pinned input verification, complete replays, every check-site mutation, inventory mutations, and corrected-wrapper integration
- independent_math_controls.py and INDEPENDENT_MATH_RESULTS.json: 2,068 independently implemented exact finite control groups
- MANIFEST.json and verify_audit.py: this audit's complete flat inventory and an externally pinned verifier

The originals were preserved. Nothing was published by the auditor. The audit contains authored mathematics/code and verification metadata only; no source PDFs, screenshots, extracted text, dataset contents or private coordination material.

## Reproduce

Supply the trusted audit-manifest digest delivered separately from the manifest itself:

```
python3 verify_audit.py --expected-manifest-sha256 <trusted-audit-digest> --selftest
python3 verify_audit.py --expected-manifest-sha256 <trusted-audit-digest> --replay --packet /path/to/original/public
```

Direct control replay:

```
python3 audit_controls.py --packet /path/to/original/public
python3 -O audit_controls.py --packet /path/to/original/public
python3 independent_math_controls.py
python3 -OO check_controls_hardened.py
```

The full audit replay takes a few minutes. It writes only temporary mutation copies, and never changes the input packet. It uses Python's standard library. The integrity tests include a POSIX FIFO and symlinks, so the complete control harness requires a POSIX filesystem. Python runtime version is recorded as metadata and excluded from cross-runtime JSON equality.

## Applying the correction

Apply OPTIMIZATION_SAFETY.patch to check_controls.py in a separate derived copy, or replace that derived copy's checker with check_controls_hardened.py. Regenerate that copy's manifest and publish its new external digest if distributing it. Preserve the original frozen packet and its original manifest digest.

The correction changes all 16 removable assertions to explicit checks. Optimized positive replay remains byte-identical to the original 23,767-group output, while deliberately false conditions fail. The original inventory logic remains unchanged.

This is AI-assisted independent review, not human refereeing or a formal proof certificate. All controls are finite. The methodological equivalence remains unproved in both directions here, and RH research is outside this audit's scope.

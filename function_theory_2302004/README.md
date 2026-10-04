# Function Theory Problem 2.4: a known affirmative answer

**2302004 / AMR-022-2004, rank 565.** Different Julia rays of one entire
function can have different finite exceptional values. This is a known
affirmative result, credited in the source update to Toppila (1970) and
corroborated by Hwang (1977), who also cites Barth–Schneider (1972).

`PROOF.md` gives a complete direct verification with the classical error
function: the finite exceptional values at angles pi/4 and 3pi/4 are
respectively 1 and -1. A nondegenerate affine change gives any prescribed
distinct pair. The argument proves actual eventual omission in a sector
and infinite occurrence of every other value in every angular
neighborhood. It does not confuse asymptotic and exceptional values.

This is a verification of a known existence statement, without a
novelty claim. The historical original constructions were not recovered;
that limitation is explicit in `SOURCE_GATE.md`. The independent witness
proof does not depend on those unretrieved texts. No full classification
is asserted, and Problem 2.5 / PR 491 is a different target.

## Contents and replay

- `PROOF.md`: mathematical proof and precise scope
- `SOURCE_GATE.md`: source identity, historical credit, limits, and
  actual prior-work checks
- `ATTEMPT_LOG.md`: one substantive completed investigation
- `STATUS.json`: scoped machine-readable conclusion
- `SOURCE_MANIFEST.json`: links and hashes of source inputs, without
  redistribution
- `verify.py` and `CHECKS.json`: 42 supplementary finite controls
- `verify_manifest.py` and `SHA256SUMS.json`: exact frozen file inventory

Run from this directory with Python 3 and mpmath 1.3.0:

```
python verify.py > /tmp/2302004-checks.json
cmp CHECKS.json /tmp/2302004-checks.json
python verify_manifest.py
```

Finite controls and hash checks are not analytic proofs. Preparation is
AI-assisted, not human peer review or formal proof-assistant certification.
No paper PDFs, OCR, source-page images, corpus copies, or private context
are included. An independent audit must be recorded separately before
publication; this packet does not self-certify that audit.

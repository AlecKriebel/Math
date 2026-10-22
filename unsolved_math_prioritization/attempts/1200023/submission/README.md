# AMR-011-0023: boundary-distance inequality

Status: **unsolved**, after five substantive approach families.

`REPORT.md` contains the exact intended scope, primary-source checks, reconstructed known unimodular proof, a spanning-tree sufficient condition, failed-inference controls, and the remaining nonunimodular gap.

Reproduce with Python 3, standard library only:

```
python3 verify.py > replay.json
cmp replay.json CONTROL_RESULTS.json
python3 verify_manifest.py
```

The integer-flow checks certify every subset of each stated finite support. They are not a general theorem. No connected transitive counterexample or full prior resolution was established. The disconnected literal-wording counterexample is explicitly excluded from the intended-resolution claim.

This packet contains authored mathematical analysis, verification code/results and public verification metadata. It does not redistribute scholarly PDFs or dataset contents. Results are AI-assisted and unreviewed; passing code is not peer review.

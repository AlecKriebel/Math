# 10300016: self-splitting branched surfaces

**Unsolved in this attempt.** The package preserves the exact source question,
two unsuccessful approaches, and the geometric statements still needed.
The invariant-measure observation is already in Calegari's original remarks;
no new theorem or general classification is claimed.

- [OBSTRUCTION.md](OBSTRUCTION.md): precise source scope, a full proof of the
  standard cone lemma, algebraic boundary cases, and the unresolved realization
  and splitting-radius gaps
- [SOURCES.md](SOURCES.md): primary references and retrieval scope
- [cone_verification.json](cone_verification.json): small exact controls
- [RESEARCH_LOG.md](RESEARCH_LOG.md): dated approach outcomes and completion
- `readiness.json`, `status.json`, `turns.jsonl`: problem-local research record

Reproduce the algebraic checks with Python 3's standard library:

```sh
python3 unsolved_math_prioritization/attempts/10300016/verify_cone_controls.py
```

[Independent adversarial review](review/REVIEW.md) passes this explicitly unresolved package, with 191 author and 1,141 independent algebraic controls. Both receipts replay byte-for-byte. This is AI review, not human peer review. The code does not recognize
self-splitting branched surfaces, and its examples are not claimed to have
geometric realizations. No public source PDFs are redistributed.

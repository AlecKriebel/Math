# Fractional SDE temporal integrability: source-scoped negative prior-result

Problem **30005030** (OWR-9790360-001), queue rank 946. Inspection date: **7 October 2026**.

**Disposition: `already_solved`, `0/5`, at the prior-result gate.** This classification refers only to the dimension-uniform scaling criterion for strong/pathwise uniqueness. An existing **preprint** theorem of Hess-Childs and Rowan, [arXiv:2604.23883v1](https://arxiv.org/abs/2604.23883v1), refutes that criterion for d >= 2, H in (1/2,1), even with an L-infinity time bound. This is not a new counterexample construction. The full multiscale proof has not been independently verified, and peer-reviewed publication has not been verified.

## Read the complete accepted scope

1. [Combined report and required addendum](COMBINED_REPORT.md)
2. [Full independent acceptance and limitations](INDEPENDENT_ACCEPTANCE.md)
3. Frozen originals: [report](REPORT.md), [required scope addendum](SCOPE_ADDENDUM.md)
4. [Audit manifest](AUDIT_MANIFEST.json), [source manifest](SOURCE_MANIFEST.json), and [retrieval clarification](PROVENANCE_ADDENDUM.json)

The exact witness is H=3/4, q=4, alpha=1/6: the scaling boundary is 0, the old boundary is 1/3, and the scaling exponent is 1/8. The drift is supplied existentially by the cited preprint theorem.

The negative result does not settle d=1 in general, autonomous drifts in general, H<1/2, integrated H>1 noise, the endpoint alpha=A(H), or every solution notion. Restricted autonomous positive results remain important: Butkovsky–Mytnik give weak uniqueness in V((1+H)/2) for 0<H<=1/2 under their hypotheses, and one-dimensional strong/pathwise uniqueness in that class under their additional product condition or nonnegative-measure hypothesis. No absence-of-all-strong-solutions conclusion is inferred from pathwise nonuniqueness.

## Run the strict checker

Python 3, standard library only. From this directory:

```sh
python3 audit_verify.py
python3 audit_checker_tests.py
```

Portable success is exactly `PASS_ARITHMETIC_AND_PAYLOAD_ONLY`: six frozen public-file identities, 6,960 exact rational parameter tests, the explicit witness, and the restricted BM arithmetic example. All eight external source checks are explicitly skipped. Six regression cases check portable skips, missing required sources, report/addendum tampering, missing report, and source tampering.

The source-backed mode requires separately supplied inputs:

```sh
python3 audit_verify.py --mode source-backed --source-dir SOURCE_DIRECTORY --corpus-dir CORPUS_DIRECTORY
```

It requires all three pinned PDFs, two pinned historical web captures, and three pinned corpus files. Missing inputs return exit 2 (`INCOMPLETE_REQUIRED_SOURCES`); mismatches return exit 1. Complete success is `PASS_ARITHMETIC_PAYLOAD_AND_SUPPLIED_SOURCE_HASHES`. Public source URLs and expected byte counts/hashes are in the metadata, but matching historical captures cannot be assumed obtainable today. No source documents or corpus contents are included here.

The historical [verify.py](verify.py) and [CHECK_RESULTS.json](CHECK_RESULTS.json) are preserved byte-for-byte. That original checker silently skips absent PDFs, and its `PASS` does not establish complete provenance or report/addendum identity. The later strict checker supersedes the frozen report's checker instructions. The frozen original wording is retained for auditability.

[Portable results](AUDIT_PORTABLE_CHECK_RESULTS.json), [source-backed results](AUDIT_SOURCE_CHECK_RESULTS.json), and [regression results](AUDIT_CHECKER_TEST_RESULTS.json) are frozen audit records. Publication preparation replayed them successfully. Hash checks establish supplied byte identity, not a full mathematical proof, exhaustive novelty search, peer review, or independent authentication of historical retrieval.

[PUBLIC_MANIFEST.json](PUBLIC_MANIFEST.json) pins every other file in this package. The full queue update changes only this problem's Status and Findings; Turns remains 0/5. All unrelated queue content is preserved.

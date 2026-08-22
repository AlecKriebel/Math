# Research log

## 2026-08-22T19:26:12Z - audit opened

- Goal: independently determine whether the manuscript and computer-assisted
  proof package warrant one of the four requested referee verdicts.
- Success criterion: complete package-integrity audit; full manuscript and
  source review; theorem-by-theorem mathematical checks; pre-execution source
  audit; replay under the specified interpreter where available; independent
  cross-checks; and a finding-indexed final report.
- Boundaries: package contents and prior audit language are claims, not
  evidence. No outside person will be contacted and nothing will be uploaded.
- Initial state: repository is on `main` with unrelated pre-existing modified
  and untracked files. They will not be altered or included in audit commits.
- Completion estimate: 2%.

## Checkpoint template

Each later checkpoint records the strongest verified result, the exact open
gap, and a best-guess completion percentage. The estimate may decrease when a
new issue enlarges the remaining work.

## 2026-08-22T19:30:15Z - identity and scope checkpoint

- Strongest verified result: the delivered package is internally
  byte-consistent. All package and archive digests match, a fresh archive
  extraction is byte-identical to the convenience extraction, and both PDF
  copies are identical.
- Manuscript coverage: all 30 compiled pages were rendered and visually
  inspected; the complete LaTeX source, appendices, and references were read.
  A theorem/quantifier ledger was reconstructed independently of Appendix C.
- Exact open gap: no theorem is yet promoted as validated. Independent
  mathematical derivations, the static software audit, complete replay, and
  cross-checks remain in progress.
- Completion estimate: 18%.

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

## 2026-08-22T19:45:00Z - source audit and exact replay checkpoint

- Strongest verified result: a pre-execution inspection traced the mandatory
  launcher to the unit suite and all 17 named verifier programs.  After an
  explicit clean-environment gate confirmed Python 3.14.6 with
  `sys.flags.optimize == 0` and no inherited `PYTHONOPTIMIZE`, `PYTHONPATH`, or
  `MAKEFLAGS`, the exact one-command referee replay completed with exit status
  0.  All mathematical stages passed and the rebuilt 30-page PDF had the same
  SHA-256 (`a6bda621...53bd2d`) as the delivered PDF.
- New source-audit finding: most scientific checks and the bootstrap version
  checks use bare Python assertions.  An optimized interpreter can erase those
  checks while leaving unconditional PASS messages, and the launcher does not
  prohibit optimization.  This did not affect the sanitized replay, but it is
  a genuine robustness/reproducibility defect in the delivered command.
- Exact open gap: the independent strong-selection/low-order reconstruction,
  alternative checker, and final adversarial proof/code-alignment pass are
  still in progress.  No overall verdict is assigned at this checkpoint.
- Completion estimate: 72%.

## 2026-08-22T20:01:30Z - final mathematical and adversarial checkpoint

- Strongest verified result: for every fixed `n>=3`, the independently audited
  sector decomposition covers the full directed tangent space and every sector
  scalar is strictly positive on its complete stated order range.  Hence the
  complete kernel has zero first variation and a strictly negative fixation
  Hessian at fitness two.  The directed strong-selection coefficient,
  fixed-graph support closure, triangle theorem, and both stated symmetric
  weighted-`K_4` families were also independently reconstructed without a
  mismatch or counterexample.
- Independent implementation: a new pure-`Fraction` checker, importing no
  delivered module, passed four nonsymmetric collision identities, all eight
  displayed `n=3,4,5` sector values, four exact strong-selection derivatives,
  and low-order equality/strictness/boundary examples.  Final exit status: 0.
- Adversarial result: no phase-order, sign, normalization, range, equality,
  boundary, quantifier, citation, or proof/code contradiction was found.
- Final adverse finding: the optimized-mode replay can print PASS and exit 0
  with theorem-bearing assertions erased.  The failure was reproduced both on
  an explicit false assertion and on the complete delivered launcher.  Its
  remediation is local, so the final verdict is **valid after minor
  corrections**, not a mathematical major correction.
- Exact remaining limitations: ordinary trust in CPython/SymPy/python-flint;
  no second independently authored solver for all 37 small symmetric systems;
  and version-pinned rather than artifact-hash-pinned dependencies.  The
  stronger global questions listed by the paper remain nonclaims.
- Completion estimate: 100% of the requested referee audit.

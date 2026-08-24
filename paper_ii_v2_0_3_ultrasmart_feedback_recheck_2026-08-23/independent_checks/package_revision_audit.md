# Independent Paper II v2.0.3 package and revision audit

Date: 2026-08-23 (America/Los_Angeles)  
Auditor task: independent package/software and v2.0.2-to-v2.0.3 revision check  
Completion: **100% of the assigned package/revision scope**

## Outcome

**PASS — no actionable submission blocker in the audited package/software scope.**

The v2.0.3 manuscript already incorporates every supported actionable point in
`FEEDBACK_CLAIMS.md`. Suggestions that would assert an unproved quantitative
rate or finite-size threshold were correctly handled by narrowing the stated
scope rather than inventing a bound. The remaining MSC and algebraic-display
suggestions are optional cosmetics, not correctness defects.

The frozen package is internally consistent, safe to unpack under the checked
member rules, reproducible with the pinned environment, and bound exactly to
the v2.0.3 annotated tag and 21 Git source blobs. Both an ordinary canonical
run and an explicitly network-denied canonical run reproduced the source
archive and PDF byte for byte. The supplied and independent checks do **not**
certify the analytic theorem; they certify only the stated finite symbolic,
transition-aggregation, packaging, and reproducibility properties.

## Frozen identities independently observed

- Scientific commit: `bd66a3bbf1c530ef67a4b7be5ee69a6825678457`
- Annotated unsigned tag: `simultaneous-amplification-beyond-three-halves-v2.0.3`
- Annotated tag object: `755969d69cdd7f86ad8eceddb4df52a4fe2b23ee`
- PDF SHA-256: `1e73984abfd64a45797b8ad6dc8b473d82a8d5eb8061efe470a1e603c2d10ad9`
- Source archive SHA-256: `e5b61e79d065a9abec0908e28db7e79366b5fccedeb6efbf22eadd7af3cc57ae`
- Referee-folder archive SHA-256:
  `f4baf76a66a12e4942f13bd7c73bbead0ff31555df5b69a489b914064c597bdf`
- Wrapper/handoff commit in the local checkout at audit time:
  `9345dc1ae3aa66530f01d9a4e4c36a21f13e7e06`

These agree with `VERSION.md:8-18` and the manifest/hash sidecars. The v2.0.3
tag is intentionally unsigned, and `VERSION.md:20-28` correctly states both
that authentication limitation and the boundary between exact programs and
analytic proofs.

Local and remote tag observations agreed exactly: the tag ref resolved to tag
object `755969...`, and its peeled commit resolved to `bd66a3...`. A live
remote-main lookup earlier in this audit returned
`8a3cfca8f09058ae00f082c31d54a1b39bb55ca6`, later than the local wrapper
checkout. This is **not** a frozen-package defect: the package identity is the
annotated tag, not a moving `main` branch. Submission materials should cite the
tag/commit above rather than describe a branch head as the scientific identity.

## Cross-check of the feedback against v2.0.3

1. **Finite-size numerical thresholds — addressed without overclaim.**
   `main.tex:1508-1516` now says the proof gives eventual positivity for each
   fixed fitness but no useful finite-size bound on `t_0(r)` and makes no
   finite-population optimality claim. The suggested values near 1.50 and 1.502
   were not established by the cited asymptotic argument, so omitting them is
   the mathematically responsible resolution.

2. **Floor-induced non-monotonicity — addressed.**
   `main.tex:1512-1515` explicitly records the `O(t^{-1})` oscillations from
   `m_t=floor(lambda_* t)` and warns that positivity need not appear
   monotonically before the eventual regime. Replacing the floor by nearest
   integer would define a different frozen family and is unnecessary.

3. **Mechanism at the `3/2` boundary — addressed.**
   `main.tex:1482-1484` states `F_r(0)=r(2r-3)` at the singular
   `sigma downarrow 0` boundary and explains that optimization over positive
   `sigma` moves the tangency to `R_hyb`.

4. **Early ordinary-core error scale — repaired.**
   `main.tex:501-515` states the `O(K/C)` result. The proof at
   `main.tex:526-545` derives an `O(C^{-1})` hazard ratio per ordinary-count
   change, `E N=O(K)`, and then the product-odds perturbation
   `exp{O(k/C)}`, yielding `O(K/C)+O(r^{-K})`. There is no residual
   `O(K^2/C)` step.

5. **Hidden-coordinate uniformity in the deficit argument — already explicit.**
   `main.tex:598-604` places “uniformly in the hub and pendant coordinates”
   immediately before the deficit-odds display, while `main.tex:614-625`
   explicitly conditions on the entire hidden history and states the final
   bound is uniform in all such histories.

6. **Gate union-bound direction — clarified.**
   `main.tex:1264-1269` says failure requires a reversal even though reversal
   need not imply failure, hence a union bound on reversals is an upper bound
   on failure. The direction is now unambiguous.

7. **Reciprocal estimate — not overstrengthened.**
   The theorem-relevant statements remain `o(C^{-1})` at
   `main.tex:1041-1045`, `1149-1158`, and `1206-1207`. The feedback's proposed
   exponential strengthening was numerical rather than proved, so no such
   claim was added.

8. **Weak-cut quantitative scale — appropriately not claimed.**
   `main.tex:296-323` proves existence and exact computability of the dyadic
   diagonal using uniform convergence and exact real-algebraic decisions. It
   does not promise a polynomial weak-edge scale. Adding one would be a new
   theorem obligation, not an editorial repair.

9. **Figure — repaired.**
   `main.tex:245-252` explicitly draws all ten edges of the five-vertex clique,
   including the two previously ambiguous chords. `main.tex:261` offsets the
   heavy-edge label, and `main.tex:272-274` explains that dashed edges are
   representative and every satellite vertex is adjacent to every clique
   vertex.

10. **Abstract definition — repaired.**
    `main.tex:45-50` now defines `R_sim` as the supremum of `R` for which one
    fitness-independent family eventually amplifies under both rules for every
    fixed `r in (1,R)`.

11. **Optional rational-expression simplification — no action needed.**
    `main.tex:1436-1454` retains
    `(5069+12 sqrt(147001))/6439`, aligned with the displayed defining
    quadratic `6439 r^2-10138 r+703=0`. Although the rational part alone can
    be reduced from `5069/6439` to `37/47`, that does not simplify the full
    algebraic root or expose an error.

12. **MSC suggestion — optional, no blocker.**
    `main.tex:79-80` and `submission/BIORXIV_METADATA.md:203` consistently use
    `92D15, 60J10, 05C81`. `HOSTILE_AUDIT.md:156` records the reason for not
    adding `60J27`: the model and exact absorbing/embedded chains are already
    appropriately covered by `60J10`, with continuous clocks auxiliary. An MSC
    addition would be cosmetic and would require refreezing the paper.

13. **Python 3.14.6 pin — confirmed, not a typo.**
    `VERSION.md:14`, `run_all_referee_checks.sh:16-24`, and
    `bootstrap_replay.sh:9-17,28-47` all require exactly Python 3.14.6. The
    selected executable `/opt/homebrew/bin/python3` reported 3.14.6 and passed;
    deliberately selecting `/usr/bin/python3` (3.9.6) failed closed before
    replay.

## v2.0.2 to v2.0.3 revision/package state

The appropriate v2.0.2 handoff baseline is wrapper commit
`0dcb450a1081e98d2ae1029d513c8343e5fd4328`; its scientific tag points to
commit `03e94e877ce10d9d459fd284bd652934cde08bb3` through tag object
`be3946c051c7f7e2073d6adf81bca31ae750251a`.

The package-side executable diff is narrow and coherent:

- `verify_referee_package.py:25-27` and `verify_git_binding.py:18-20` change
  only the frozen commit/tag-object/tag constants from v2.0.2 to v2.0.3.
- The archived `verify_paper_claims.py` changes only its required release
  marker from v2.0.2 to v2.0.3.
- `run_all_referee_checks.sh`, `all.sh`, `bootstrap_replay.sh`, `build.sh`,
  `release_bundle.sh`, `replay.sh`, `bundle_manifest.py`, the three scientific
  certificate programs, tests, requirements, and vendored wheels are
  byte-unchanged from the already-audited v2.0.2 machinery.
- The scientific changes are in the manuscript plus matching release/research
  records, rebuilt PDF/archive, and refreshed manifests and version constants.
  The source release notes state that theorem, threshold, construction, and
  certificates are unchanged.

The source/package paths in scope were clean relative to local `HEAD` after all
checks (`agent-pkg-053`). No delivered or source file was modified by this
audit; all replay occurred in a disposable copy or a temporary directory.

## Package, archive, dependency, and mode results

Independent standard-library audit (`agent-pkg-027`, repeated after dynamic
tests as `agent-pkg-039`) found:

- **PASS:** 34 payload files exactly match `PACKAGE_MANIFEST.sha256`.
- **PASS:** package paths are relative/canonical, with no symlinks or
  non-regular payload nodes; executable/non-executable modes are exact.
- **PASS:** source archive has exactly 23 sorted, unique, canonical regular
  members, root ownership metadata, fixed epoch, and exact internal manifest.
- **PASS:** extracted source tree is byte-for-byte and mode-for-mode identical
  to the source archive.
- **PASS:** convenience PDF equals the archived source PDF exactly and has the
  frozen PDF digest above.
- **PASS:** outer referee archive has exactly 35 safe deterministic regular
  members and is byte/mode-identical to the referee folder, including the outer
  manifest.
- **PASS:** both vendored wheels have the pinned outer SHA-256, safe/unique
  members, correct package/version metadata, and exact internal wheel `RECORD`
  digests and sizes.
- **PASS:** an AST scan of all eight Python programs found no bare `assert`
  statements in verification-critical code.

`requirements.txt:1-9` uses `--no-index`, the local `vendor` directory,
binary-only packages, exact versions, and `--require-hashes` with the two
verified wheel hashes.

The supplied package verifier also passed independently (`agent-pkg-028`), and
the Git-binding verifier passed (`agent-pkg-029`): the unsigned annotated tag,
21 archived Git blobs, and all associated modes match the supplied checkout.
Its authentication limitation is correctly printed rather than hidden.

## Replay and regression results

- **PASS canonical full replay** (`agent-pkg-030`): exact symbolic/lumping and
  integration verifiers, fail-closed tests, optimized-mode tests, mutation
  tests, failure propagation, deterministic PDF build, deterministic source
  bundle, and final byte comparisons all passed.
- **PASS explicitly network-denied full replay** (`agent-pkg-031`), using the
  macOS sandbox rule `(deny network*)`: dependencies installed exclusively from
  the two vendored wheels, and all canonical results still passed.
- **PASS deterministic identities:** both full runs rebuilt the source archive
  as `e5b61e...57ae` and the PDF as `1e7398...0ad9`, exactly matching the
  frozen deliverables.
- **PASS selected-interpreter plumbing:** Python 3.14.6 succeeded; explicitly
  selecting Python 3.9.6 was rejected with the required-version error
  (`agent-pkg-033`).
- **PASS optimized-mode fail-closed behavior:** package verification
  (`agent-pkg-034`), Git binding (`agent-pkg-036`), and submission-material
  verification (`agent-pkg-038`) all rejected `python -O`.
- **PASS submission-material verifier** in ordinary mode (`agent-pkg-037`).

Two logged audit-invocation mistakes were immediately corrected and did not
touch source or results: `agent-pkg-020` supplied an incomplete logger
invocation, and `agent-pkg-035` used the wrong audit-date directory. Earlier
`agent-pkg-004` likewise temporarily shadowed the shell `PATH`, and
`agent-pkg-041` guessed a nonexistent `rg` path. Each failure is retained in
the transcript for completeness; the corrected commands are
`agent-pkg-021`, `agent-pkg-036`, `agent-pkg-005`, and `agent-pkg-043`.

## Consequence of any further edit

No further manuscript/package edit is recommended for this feedback cycle.
Any byte change to `main.tex` or another archived source file would immediately
break the 21-blob Git/tag binding, the internal source manifest, the source
archive digest, the outer package manifest, and the outer archive digest. A
render-affecting edit would additionally break the frozen PDF digest and the
deterministic byte comparison. Even optional edits such as changing MSC codes,
rounding `m_t`, or restyling the rational root should therefore **not** be made
in-place.

If a genuinely necessary scientific edit is later discovered, the minimal
safe process is a new scientific commit and annotated release tag (for example
v2.0.4), followed by a PDF/source-archive rebuild, refresh of all submission
hashes/version markers/manifests, reconstruction of the outer archive, and a
fresh full replay. None of the current feedback justifies that identity churn.

## Limitations

- The tag is annotated but unsigned; equality is not authorship
  authentication.
- Python itself, Tectonic, Poppler, and the Tectonic resource cache remain
  externally provisioned, as `VERSION.md:20-23` discloses.
- Passing exact programs does not prove the manuscript's weak-cut limit,
  asymptotic cleanup, reciprocal-invasion analysis, or global sweep. Those
  analytic arguments require mathematical refereeing outside this package
  audit.

**Final package/software status: PASS. Actionable blockers: none.**

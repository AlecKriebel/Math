# R3 mathematical-source and PDF regression audit

## Verdict

**PASS.** Relative to the frozen R2 package, R3 changes **no mathematical or
scientific predicate**. Every theorem, hypothesis, order of quantification,
displayed formula, equality case, range endpoint, exact margin, sample
eigenvalue, limitation, and open-problem/nonclaim is preserved. Every one of
the 20 Python files in the scientific-check inventory is byte-identical to R2.

R3 does materially change the *operational* predicate attached to replay: the
package-root `run_all_referee_checks.sh` is now the sole certified route and
adds exact-tree, interpreter-path, private-cache, safe-extraction, and hostile
node controls. That wording accurately describes the changed sources. After
the parent referee cleared the pre-execution static gate, the certified R3
replay completed with exit status 0, rejected every advertised negative
control, ran the unit suite and all seventeen direct verifier/cross-check
programs, kept its controlled cache empty, and rebuilt the delivered PDF
byte-for-byte.

The strongest verified regression result is therefore:

> R3 preserves the complete R2 scientific statement and certificate payload,
> while its changed replay claim is both statically consistent with the
> delivered launcher and dynamically realized by the sole certified route.

No R2/R3 regression gap remains. This is a regression result, not a fresh
from-first-principles proof of every theorem; the broader mathematical
correctness question remains governed by the independent proof audits.

## Scope and gate discipline

- Frozen baseline:
  `/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/work/package`
- R3 candidate:
  `/Users/alec/Documents/Math/complete_graph_extremality_r3_rereview_2026-08-22/work/package`
- Report and command log were written only under the R3 audit `records/`
  directory. No package file was modified.
- Until explicit gate clearance from the parent referee, I only inventoried,
  diffed, hashed, parsed as inert data, extracted PDF text, and rendered PDFs
  with system tools. I did **not** execute or import any delivered source.
- After clearance, I ran exactly `./run_all_referee_checks.sh` from the R3
  package root. Its extraction, runtime, caches, logs, negative-control trees,
  and TeX build were disposable; it ended with exit status 0.

## Timestamped sub-log

- **2026-08-22 22:44 PDT — 10%:** opened the R3 static regression audit;
  counted 82 R2 files and 84 R3 files; began exhaustive inventory and recursive
  byte comparison.
- **2026-08-22 22:48 PDT — 45%:** isolated the only LaTeX change to Section 7
  replay/data-availability prose; confirmed Sections 1--6, all appendices,
  `main.tex`, and `references.tex` were byte-identical.
- **2026-08-22 22:52 PDT — 75%:** confirmed all 20 scientific-check programs
  and their 406-check inventory were preserved; verified the package/source
  manifests, archive/extracted-tree identity, PDF hashes, certificate binding,
  and exact page-delta set; visually inspected all 30 R3 pages and the changed
  R2 pages.
- **2026-08-22 22:53 PDT — 82%:** sent the parent an early static-readiness
  finding: no scientific change and no PDF defect; dynamic efficacy remained
  deliberately untested.
- **2026-08-22 22:54 PDT — 88%:** parent cleared the static gate; launched the
  sole certified R3 replay from the package root.
- **2026-08-22 22:58 PDT — 100%:** certified replay exited 0 after all hostile
  controls and exact theorem checks; rebuilt PDF SHA-256 matched the delivered
  R3 PDF exactly; completed this report.

## Exhaustive file-level regression matrix

The recursive comparison found 33 file deltas: 31 changed files and two R3
additions. No R2 file was removed. All unlisted common files are byte-identical.

| File class | Exact R2 -> R3 result | Scientific effect |
|---|---|---|
| Manuscript inputs (12 `.tex` files) | `main.tex`, `references.tex`, Sections 01--06, and Appendices A--C are byte-identical. Only `sections/07_implications_reproducibility.tex` changed. | None; Section 7 changes replay and data-availability prose only. |
| Compiled paper | Both top-level and nested PDFs changed from R2 hash `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4` to R3 hash `5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd`. Within each version, the top and nested copies are byte-identical. | No scientific text change; pages 17--26 reflow because Section 7 is longer. |
| Scientific programs | All 20 entries in `EXPECTED_SCIENTIFIC_CHECKS` are byte-identical. More broadly, 24 of the 27 common Python files are byte-identical. | Zero predicate drift; exact formulae, ranges, checks, and outputs are preserved. |
| Changed Python infrastructure | `paper_db_extremality/bundle_manifest.py`, `submission/verify_execution_safety.py`, and package-root `verify_referee_package.py`. | Packaging/safety only: exact node set, manifest parsing, safe extraction, links/special nodes, `.pyc`/`.pyo`/`__pycache__`, and cache-prefix enforcement. The existing 20-file/406-check scientific inventory is unchanged. |
| New R3 controls | `submission/create_tree_negative_control.py` and `submission/fake_python_public_token.sh`. | No theorem computation. They create disposable hostile-tree cases and a token-printing fake interpreter for negative controls. |
| Launcher/build scripts | `run_all_referee_checks.sh`, `submission/bootstrap_replay.sh`, `replay.sh`, `all.sh`, and `release_bundle.sh` changed. | Operational hardening. The internal replay retains the same direct unit suite and seventeen-program theorem/cross-check sequence. `all.sh`/release now select explicit development mode. |
| Proof/classification notes | Changed: `phase2_n4/README.md`, `phase2_n4/n4_symmetric_classification.md`, `phase2_triangle/README.md`, `phase2_triangle/triangle_classification.md`, `r2_determinant/TRUE_INVERSE_RANK_SYMMETRIC_PHASE_CONTRACTION.md`, `r2_standard_physical_phase/PHYSICAL_STANDARD_PHASE_THEOREM.md`, and `r2_standard_physical_phase/README.md`. | Only stale `.venv`/individual invocation prose changed. The omitted `search_exact_k4.py` is now accurately labeled development-only and non-theorem-bearing. No proof line, identity, bound, equality, or quantifier changed. |
| Paper-package documentation | Changed: paper `README.md`, `submission/BUNDLE_REPRODUCTION.md`, `submission/DECLARATIONS.md`, `submission/ENVIRONMENT.md`. `submission/PROVENANCE_AND_RELATED_RELEASES.md` is byte-identical. | Certified/development route clarification only. |
| Enclosing-package documentation | Changed: `CLAIM_CODE_MAP.md`, `README_FIRST.md`, `REFEREE_PROMPT.md`, `VERSION.md`, `BUNDLE_METADATA.txt`. `REFEREE_REPORT_TEMPLATE.md` is byte-identical. | Replay identity, exact-tree audit criteria, and new hashes/counts only. The claim map still distinguishes all-order proofs from finite checks and now accurately states that 17 programs run directly while three open-route modules have only limited import reach. |
| Identity artifacts | `PACKAGE_MANIFEST.sha256`, internal `MANIFEST.sha256`, the tarball, and detached tarball checksum changed consistently. | Expected because two files and operational prose/code were added or changed; no broken binding. |

### Exact Section 7 manuscript delta

R3 Section 7 lines 98--114 replace the old paper-directory `./replay.sh`
instruction with package-root `./run_all_referee_checks.sh` and state the
exact-tree/hash, safe-extraction, pinned-environment, empty-private-cache,
internal-stage, PDF-rebuild, and lower-stage noncertification properties. Lines
119--131 change “standalone archive supplied with the manuscript” to an
enclosing package whose verified payload is that archive, and identify the
package-root launcher as the certified entry point.

No text before line 98 changed. In particular, Section 7's mathematical
content at lines 1--96 is byte-identical: fitness monotonicity, Proposition 13,
the support-degree condition, the fixed-order/local-versus-asymptotic
distinction, the open global fitness-two statement, and every stated finite or
analytic Hessian range.

### Proof-note deltas

The seven changed mathematical notes have narrowly localized command blocks:

- triangle notes: the certified launcher runs all three unchanged programs;
  individual development examples use `PAPER1_DEV_PYTHON`;
- symmetric `K_4` notes: the launcher runs the two unchanged theorem programs;
  the absent search helper is explicitly development-only and has no theorem
  quantifier;
- standard and symmetric Hessian notes: individual invocation prose changes
  from a stale relative `.venv` path to `PAPER1_DEV_PYTHON`.

The surrounding derivations and certificate statements compare
byte-for-byte.

## Theorem-level predicate matrix

“Identical source” below means exact byte identity, not an interpretive
similarity judgment.

| Claim / controlling material | R2 -> R3 pages | Regression result |
|---|---:|---|
| Theorem 1, fitness-two strict local optimality; `sections/02_model_results.tex:46--74`, equations (2.6)--(2.8) | 5 -> 5 | Identical source. Preserves `n>=3`, every tangent direction, sufficiently small admissible epsilon, positive-definite inverse-mean curvature, negative fixation Hessian, full-polytope local maximality, and the `n=2` tie. |
| Theorem 2, complete-support strong-selection correction; lines 100--111, equation (2.10) | 6 -> 6 | Identical source. Preserves fixed `W`, positive complete directed support, `r -> infinity`, exact `1/r` coefficient, equality gauge, and full-chain equality. |
| Corollary 3 and Proposition 4; lines 113--136, equations (2.11)--(2.12) | 6 -> 6 | Identical source. Fixed finite universal-amplifier nonexistence and undirected support limit/deficit unchanged. |
| Theorem 5, positive weighted triangles; lines 141--151, equation (2.13) | 6 -> 6 | Identical source. Preserves every `r>1`, positivity, complete-graph upper bound, and equality iff all three edge weights agree. |
| Lemma 6, Proposition 7, Lemma 8: fair-geometric OR union dual, finite-union coverage, rectangular marked/active phase spaces, ordering, stationary laws, `rho=m/n`, and collision identity; Section 3 | 7--9 -> 7--9 | Entire Section 3 identical, including every map, phase order, normalization, and proof. The linked exact programs are also identical and passed replay. |
| Perturbation expansion, vanishing first variation, tangent decomposition/dimensions/orthogonality and norm normalization; Section 4 equations (4.1)--(4.10b) | 10--11 -> 10--11 | Entire source identical. No sign, tangent-space, dimension, or normalization drift. |
| Theorem 9, all three Hessian-sector positivity statements; `sections/04_local_hessian.tex:107--144`, equations (4.11)--(4.12) | 11--12 -> 11--12 | Identical source. Preserves standard `n>=3`, symmetric-balanced `n>=4`, antisymmetric-balanced `n>=3`; split ranges `3<=N<=39`, `40<=N<=287`, `N>=288`; sample eigenvalues; and the warning that finite values are checks, not extrapolation. |
| Uniform-neighborhood argument and nonclaim; lines 146--168, equation (4.13) | 12 -> 12 | Identical source. Preserves compact-ball remainder control and explicit statement that the radius depends on `n`. |
| Lemma 11 and fixed-structure strong-selection proof, Section 5 | 12--14 -> 12--14 | Entire source identical; analyticity assumptions, support cases, incoming-column identity, equality conditions, and asymptotic order unchanged. |
| Global low-order identities and signs, Section 6 | 15 -> 15 | Entire source identical, including the triangle determinant/SOS derivation and the fact that the symmetric `K_4` families are not a classification. |
| Lemma 12, Proposition 13, and open/nonclaim text; Section 7 lines 1--74 | 16 -> 16 | Identical source. No interchange of `n,r`, no uniform local radius, no global concavity/path claim, and global undirected fitness-two maximality remains open. |
| Appendix A analytic and exact Hessian certificates, equations (A.1)--(A.36) | 18--26 -> 18--26 (reflowed) | Appendix source byte-identical. Every recurrence, sector normalization, endpoint, inequality, coefficient list, discriminant, phase bound, and exact value is unchanged. |
| Lemma 15 finite exact symmetric certificate; Appendix A lines 529--560, equation (A.33) | lemma begins 25; program/hash on 26 -> all on 26 | Preserves `3<=N<=39`, all 248 orders `40<=N<=287`, minimum at `N=40`, exact margin `639304267467075678841 / 115369588296792467144716`, and the verifier hash. |
| Theorem 16, two symmetric weighted `K_4` families and nonclassification, Appendix B | 27--28 -> 27--28 | Appendix B and both pages are byte/pixel-identical. |
| Quantifier and scope ledger, Appendix C | 29 -> 29 | Source and page are byte/pixel-identical. The fixed-`n` local radius, full-tangent curvature, fixed-graph threshold, triangle quantifier, two open statements, and nonimplication warning are preserved verbatim. |
| References | 29--30 -> 29--30 | Source and pages are byte/pixel-identical. |

## Certificate and package binding

The identity values changed coherently because the operational source changed:

| Binding | R2 | R3 | Result |
|---|---|---|---|
| Scientific/source commit recorded by package | `e63cc44748e4084ade67c5ff7dc5d1bf2a872f7c` | `b9a415f763e82d9cc45c83de96c895b109e158a4` | Updated consistently in R3 metadata. |
| Source archive SHA-256 | `1754bee519537105f192a40d98f83a4b2fd5097897e0632d88ace1e9892d59ed` | `12a8c89b77aa898e9c16a1efdf93e77f35ea3cee3eed93ad34c7f497eaad3eb0` | R3 detached digest, README, VERSION, manifest, verifier output, and actual tarball agree. |
| PDF SHA-256 | `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4` | `5d2bc6cfa9d02b21e816d3dd30252d067e23b51ecd0c58bb8c3cfb116ab937bd` | R3 top copy, nested copy, package manifest, metadata, and rebuilt PDF agree. |
| Internal archive files | 71 | 73 | Exactly the two new hostile-control helpers account for the increase. Static archive scan found 73/73 regular members byte-identical to the delivered extracted tree. |
| Symmetric-certificate verifier SHA-256 displayed in Appendix A | `7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512` | Same | Actual `verify_true_inverse_rank_symmetric_phase.py` digest, `verify_paper_claims.py`, and Appendix A all agree. |

Independent system checksum checks passed every entry of
`PACKAGE_MANIFEST.sha256`, every entry of the internal `MANIFEST.sha256`, and
the detached tarball checksum. The certified replay independently reported 83
package payload files and 73 archive members matching their manifests.

## PDF regression and exact page deltas

### Structural comparison

Both PDFs have:

- 30 pages;
- US-letter media box, 612 x 792 points;
- zero rotation;
- PDF 1.5, unencrypted, no forms, no JavaScript;
- the same 22 embedded font entries and encodings;
- the same fixed creation timestamp metadata.

R3 is 235,301 bytes versus R2's 234,169 bytes. That increase is accounted for
by the longer reproducibility text.

At 120 dpi, independent Poppler renders and per-page byte comparisons give the
exact changed-page set:

- **pixel- and extracted-text-identical:** pages 1--16 and 27--30;
- **changed/reflowed:** pages 17--26 only.

### Page-by-page delta map

| Page | Exact R2/R3 delta |
|---:|---|
| 1--16 | Identical render and text. All main mathematical sections through Section 7.2 are unchanged. |
| 17 | Substantive expository delta: new sole-certified replay and data-availability wording. Longer text moves Author contributions, Ethics, and AI disclosure to page 18. Funding and Competing interests remain on page 17. |
| 18 | R2 begins Appendix A and reaches the start of A.1. R3 first carries the three displaced declarations, then begins Appendix A and ends after the proof following (A.3b). Appendix text itself is unchanged. |
| 19 | R2 continues A.1 from the operator blocks; R3 begins A.1. Pagination only. |
| 20 | R2 begins the positivity proof for `Phi_N`; R3 begins with the tail following (A.11s). Pagination only. |
| 21 | R2 starts at (A.20s), reaches A.2 and the start of Lemma 14's proof; R3 starts after (A.17s), completes the standard sector, and begins A.2. Pagination only. |
| 22 | R2 continues Lemma 14 and begins A.3; R3 begins Lemma 14. Pagination only. |
| 23 | R2 continues A.3 at the two-channel operator; R3 begins A.3. Pagination only. |
| 24 | R2 starts at the cross-term normalization and reaches (A.24); R3 starts at the preceding labelled-current normalization and reaches (A.23). Pagination only. |
| 25 | R2 covers (A.25)--(A.33), including the beginning of Lemma 15. R3 covers (A.24)--(A.32). Pagination only. |
| 26 | R2 begins Lemma 15's computer-assisted proof; R3 begins Lemma 15 itself. Both end with the proof of Theorem 9. The displayed exact margin and SHA-256 are unchanged. |
| 27--30 | Identical render and text; Appendices B--C and references are unaffected once Appendix B starts on its forced new page. |

### Visual inspection

I rendered all 30 R3 pages and inspected every page. I also inspected the R2
versions of all ten changed pages and then viewed R3 pages 17, 18, and 26 at
full individual-page resolution. No clipped line, margin overflow, equation or
caption collision, orphaned heading, blank page, missing glyph, broken
monospace path, or unreadable URL was found. The R3 reflow is clean. The long
archive names wrap inside the text block on page 17; the Appendix A heading
and declarations fit cleanly on page 18; Lemma 15 and its long hash fit cleanly
on page 26.

## Static-to-dynamic validation of remediation wording

The changed wording is accurate at both levels checked here:

1. Static source inspection shows that the public launcher rejects inherited
   `PYTHON`, requires exact tool versions, creates a fresh certified-run root,
   verifies and safely extracts the archive, runs five hostile-tree controls,
   invokes bootstrap with an internal certified-stage token, rebuilds the PDF,
   compares it with `cmp`, and re-verifies the original package.
2. `bootstrap_replay.sh` distinguishes certified and development modes,
   provisions a fresh exact Python 3.14.6 virtual environment from hash-locked
   requirements, and hands a fresh runtime/cache path to internal replay.
3. `replay.sh` rejects standalone invocation and `PYTHON` overrides, uses the
   fresh interpreter with `-B` and a private cache prefix, performs source and
   dependency preflights, directly runs the unit suite and all seventeen
   advertised programs, checks the cache again, and does not claim that its
   lower-stage status alone certifies the package.
4. Dynamic replay confirmed every advertised rejection: intentional false
   check, explicit false under `-O`, inherited `PYTHONOPTIMIZE`, fake public
   `PYTHON`, hostile bytecode/cache, extra file, extra directory, symlink, and
   FIFO. It also confirmed 73 regular source files, 25 implied directories,
   406 scientific and 436 total `require` calls, exact dependency versions,
   empty cache boundaries, all exact verifier successes, and byte-identical
   PDF reproduction.

## Remaining gaps

- **R2/R3 scientific regression:** none found.
- **Certified replay efficacy:** no remaining gap; the authorized run passed
  with exit status 0.
- **Package identity/binding:** no remaining gap in the delivered copy; all
  independent and certified checks agree.
- **PDF content/layout:** no remaining gap; all pages were inspected and the
  exact page-delta set is explained by the sole Section 7 source change.
- **Absolute theorem correctness:** not re-proved wholesale in this regression
  audit. Byte identity and replay establish preservation, not by themselves a
  new independent derivation of all R2 mathematics.

See `MATH_PDF_REGRESSION_COMMANDS.log` for the command/status record.

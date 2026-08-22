# R2 mathematical-source and PDF regression audit

## Scope and gate

This audit compares the R2 referee package

`/Users/alec/Documents/Math/complete_graph_extremality_r2_rereview_2026-08-22/work/package`

against the previously audited R1 package

`/Users/alec/Documents/Math/complete_graph_extremality_referee_audit_2026-08-22/work/package`.

The scope is mathematical and expository regression: every LaTeX manuscript source, every supplied proof note, the mathematical bodies of the verifier sources, all hypotheses/quantifiers/equality cases/range endpoints/nonclaims, the symmetric certificate binding, and both copies of the compiled PDF. Package prose about the remediation was treated as a claim and checked against the source.

In accordance with the static-review gate, **no delivered verifier, replay, bootstrap, build, Makefile, package Python program, or package shell program was executed in this audit**. Operations were limited to read-only inventory, `cmp`/`diff`, hashing and manifest checking with the system `shasum`, parsing source as inert text/AST, PDF metadata/text/font extraction, and PDF rendering. The only modified file is this report; temporary renders were written under `/tmp`.

## Timestamped sub-log

- **2026-08-22 15:18 PDT — 15%:** began the R2 regression audit; inventoried both package trees (R1: 81 files; R2: 82 files), identified the file-set delta and every byte-level difference, and confirmed that only two manuscript `.tex` files differ.
- **2026-08-22 15:20 PDT — 45%:** read the complete two-TeX diff, all changed verifier-source diffs, all replay/build/safety diffs, and all revised explanatory documents. A read-only AST comparison established that all 406 R1 scientific assertion conditions occur unchanged as the 406 R2 explicit `require` conditions.
- **2026-08-22 15:23 PDT — 75%:** checked the revised symmetric-verifier digest against the actual file, both manifests, the paper integration source, and the appendix; checked the new replay's 17 direct calls against the removed Makefile targets and traced the three imported-helper paths.
- **2026-08-22 15:26 PDT — 100%:** extracted and compared PDF text page by page, compared metadata and fonts, rendered all 30 pages of both PDFs, visually inspected R2 in five six-page sheets and the two changed R1/R2 page pairs at full-page resolution, and completed this report.

## Executive verdict

**PASS — no mathematical, theorem-scope, certificate-binding, or PDF-layout regression.**

R2 preserves the mathematical manuscript and proof package. Of the twelve LaTeX manuscript files, ten are byte-identical. The only two changes are:

1. `sections/07_implications_reproducibility.tex:93-96` adds an accurate clarification that the universal directed strong-selection result and the all-order antisymmetric-sector result are manuscript proofs, while their literal-chain executable checks are finite consistency tests.
2. `appendices/A_sector_certificates.tex:551` replaces the old SHA-256 with the exact new digest of the mechanically remediated symmetric verifier.

Every theorem statement, hypothesis, quantifier, formula, equality case, finite/analytic range, exact margin, displayed eigenvalue, and nonclaim is otherwise byte-identical to R1. All scientific verifier conditions are preserved exactly; R2 changes their failure mechanism from optimization-elidable Python `assert` statements to explicit exceptions. Several console/docstring literals in three verifier files are narrowed so finite checks are no longer described as universal proofs. No computational formula or mathematical branch changed.

The R2 PDF remains 30 US-letter pages. Pages 1-16, 18-25, and 27-30 render byte-for-byte identically to R1 at 96 dpi. Page 17 contains only the added proof-status paragraph and consequent local line reflow; page 18 is again identical, so there is no pagination cascade. Page 26 differs only in the 64-character verifier digest. Both changed pages are clean, within margins, and free of clipping, collision, missing glyphs, or footer/header displacement.

There are no remaining mathematical or PDF-regression gaps. Dynamic fail-closed behavior, dependency installation, and deterministic rebuilding were intentionally not exercised here because of the static gate; those are execution-audit questions, not unresolved source/PDF regressions.

## Exact content delta

### Manuscript source

The complete unified LaTeX delta is exactly:

```diff
--- R1/appendices/A_sector_certificates.tex
+++ R2/appendices/A_sector_certificates.tex
@@ -548,7 +548,7 @@
 arithmetic.  Its SHA-256 is
 \begin{center}
-\small\nolinkurl{b4d45a83ce5f21a1fd3e09403b376e071330290a01affff64711574b69e024bc}.
+\small\nolinkurl{7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512}.
 \end{center}
```

```diff
--- R1/sections/07_implications_reproducibility.tex
+++ R2/sections/07_implications_reproducibility.tex
@@ -90,6 +90,10 @@
 finite ranges is rational.  The verifiers discharge the finite
 computer-assisted portions; sampled numerical values are never used to
 extend a quantifier.
+The universal directed strong-selection conclusion and the all-order
+antisymmetric-sector conclusion are proved analytically in Section~5 and
+Appendix~A, respectively; their literal-chain executable checks are finite
+consistency tests.
```

No theorem environment, equation, label, proof step, bibliography entry, title/abstract text, declaration, or quantifier-ledger row changed.

### Verifier source

Twenty common scientific Python files changed. Across those files R1 contains 406 `assert` nodes and R2 contains 406 corresponding `require` calls. Parsing both versions without importing or executing them, deleting only the newly added `CertificateFailure`/`require` definitions, and normalizing each `require(condition[, message])` back to `assert condition[, message]` produced identical ASTs except for the following deliberate nonmathematical literals:

| File | Non-`assert` delta | Regression assessment |
|---|---|---|
| `phase4.../r2_marked_lift_v2/verify_marked_lift.py` | Final message changed from “exact universal two-step ... identity” to “finite exact examples match the stated ... identity.” | Accurate narrowing; formulas/checks unchanged. |
| `phase5.../verify_antisymmetric_hessian.py` | Docstring and two final messages now say “finite exact checks” and point to the all-\(n\) analytic Appendix A proof. | Accurate narrowing; recurrence checks remain \(n=3,\ldots,40\), literal active chains \(n=3,\ldots,7\). |
| `phase5.../verify_hessian_sectors.py` | “PROVED SEPARATELY” becomes “CONTEXT: ... established in Appendix A.” | Accurate; finite orbit table remains \(3\le n\le12\). |
| `paper_db_extremality/verify_paper_claims.py` | Symmetric-verifier hash literal updated from `b4d45...24bc` to `7a1fa...512`. | Required and exact; all 42 scientific conditions unchanged. |

The other sixteen scientific Python diffs are exactly the explicit-failure migration plus the common helper definition. `bundle_manifest.py` has packaging-only changes: remove the project Makefile from the archive list, add `verify_execution_safety.py`, add lock/bundle metadata, and detect the paper root by `main.tex` instead of the removed Makefile.

### Replay and explanatory material

The file-set delta is:

- R1 only: `source_and_certificates/universal_simultaneous_amplification/Makefile`.
- R2 only: `paper_db_extremality/requirements-lock.txt` and `paper_db_extremality/submission/verify_execution_safety.py`.

R2 `replay.sh` directly invokes the same unit suite and the same seventeen verifier/cross-check programs formerly reached through the Makefile plus direct calls. The removed Makefile contributed only the unit suite and the phase 1/2/3 commands now listed explicitly; no scientific invocation was dropped.

`CLAIM_CODE_MAP.md` now accurately distinguishes import from execution:

- `verify_resolvent_identities.solve()` is called by `verify_marked_lift.py`, but its guarded `main()` is not run;
- only `verify_direct_flow_screen.matrix_from_edges()` is called, not that module's guarded screen; and
- `verify_fisher_route.py` is imported transitively by `verify_direct_flow_screen.py`, but none of its functions or its guarded witness suite is called on the Paper I path.

Static inspection confirms all three statements. The first two helpers' called functions are visible at `verify_marked_lift.py:34-39,502,531,561`; `verify_direct_flow_screen.py:17-35` imports the Fisher functions but `matrix_from_edges()` does not use them. The uncalled guarded suites concern exploratory/global routes and are not cited as the proof of a Paper I theorem.

The revised `README_FIRST.md`, `REFEREE_PROMPT.md`, `BUNDLE_REPRODUCTION.md`, and `ENVIRONMENT.md` accurately describe the new direct replay, explicit failures, finite-check/proof boundary, hashed dependency lock, and Tectonic bundle check as implemented in the scripts. Their runtime efficacy and the provenance/completeness of external wheel hashes are reserved for the execution/supply-chain audit; no source-language contradiction was found.

## File-level diff matrix

| File or exhaustive group | R1→R2 status | Mathematical/expository effect |
|---|---|---|
| `main.tex`, `references.tex` | Byte-identical | None. |
| `sections/01_introduction.tex` through `06_low_order.tex` | All six byte-identical | All definitions, main theorems, proofs, equations, and equality cases preserved. |
| `sections/07_implications_reproducibility.tex` | Four prose lines added at 93-96 | Accurate proof-status clarification only; no theorem/nonclaim changed. |
| `appendices/B_k4_certificate.tex`, `C_quantifier_ledger.tex` | Byte-identical | K4 formulas/equality cases and every quantifier/nonclaim preserved. |
| `appendices/A_sector_certificates.tex` | One 64-hex digest replaced at line 551 | Mathematical appendix, all ranges/margins/formulas unchanged; certificate binding updated correctly. |
| Scientific proof notes: `non_strong_support_closure.md`; both phase-2 classification notes; `phase3_asymptotic/REPORT.md`; `MARKED_ONE_SAMPLE_REDUCTION.md`; all four `r2_determinant/*.md`; `LOCAL_COMPLETE_HESSIAN_THEOREM.md`; `PHYSICAL_STANDARD_PHASE_THEOREM.md` | All byte-identical | No proof-note regression. |
| Other scientific READMEs and `requirements.txt` files | Byte-identical | No claim change. |
| 20 scientific verifier `.py` files | 406 conditions mechanically migrated from `assert` to `require`; only the four literal changes listed above | Mathematical predicates, loops, formulas, constants, branches, and expected values preserved. |
| `src/*.py`, `tests/*.py`, top-level `verify_referee_package.py` | Byte-identical | Core chain implementation and tests unchanged. |
| New `submission/verify_execution_safety.py` and `requirements-lock.txt` | Added | Reproducibility/safety only; no theorem content. |
| `replay.sh`, `bootstrap_replay.sh`, `run_all_referee_checks.sh`, `build.sh`, `release_bundle.sh` | Revised | Fail-closed/direct replay and pinned-build plumbing; scientific call coverage preserved. |
| Project `Makefile` | Removed | Its exact scientific targets are now direct calls in `replay.sh`. |
| `CLAIM_CODE_MAP.md` | Revised | Corrects finite-vs-universal and import-vs-call descriptions. |
| `README_FIRST.md`, `REFEREE_PROMPT.md`, `VERSION.md`, `BUNDLE_METADATA.txt`, submission reproduction/environment docs | Revised | Package identity and remediation explanation; no mathematical claim weakened or enlarged. |
| `PACKAGE_MANIFEST.sha256`, internal `MANIFEST.sha256`, archive, detached digest, `VERSION.md` hashes | Regenerated | All system checksum checks passed; identities consistently describe R2. |
| Top-level and nested manuscript PDFs | Both regenerated and mutually byte-identical | Only pages 17 and 26 differ from R1 as described below. |

For completeness, the scientific prose inventory contained 34 R1 files and 35 R2 files: 30 common files are byte-identical, two manuscript TeX files and two submission-environment documents differ, and the hashed lock is new. This inventory includes every `.tex`, `.md`, and `.txt` file below `universal_simultaneous_amplification`.

## Theorem- and claim-level regression matrix

| Claim | Exact R2 source / PDF | Preserved content | Verdict |
|---|---|---|---|
| Theorem 1, fitness-two local optimality | `sections/02_model_results.tex:46-74`; PDF p. 5, (2.6)-(2.8) | \(n\ge3\); every tangent direction; nonnegative feasible perturbations; inverse-mean expansion; \(m_n\); positive-definite quadratic form; zero first and strictly negative second variation; full positive loopless row-stochastic space; \(n=2\) tie. | Byte-identical, preserved. |
| Local-radius and global nonclaims | `sections/04_local_hessian.tex:154-167`; `sections/07...tex:62-73`; Appendix C:7-18,31-44; PDF pp. 12,16-17,29 | Radius may depend on \(n\); no global concavity/path monotonicity; no control near singular faces/far from \(J_n\); global undirected \(r=2\) statement and growing-family statement remain open. | Byte-identical, preserved. |
| Theorem 2 and Corollary 3, strong selection | `sections/02_model_results.tex:100-120`; proof `sections/05_strong_selection.tex:44-149`; PDF pp. 6,13-14, (2.10), (5.4)-(5.17) | Fixed \(n\ge3\), complete positive directed support for the expansion; coefficient \(\mathcal E_{\rm dir}/[n^2(n-2)]\); equality iff each incoming target column is constant, giving the complete chain at every fitness; noncomplete/reducible closure and fixed-structure quantifier retained. | Byte-identical. New p. 17 sentence correctly says the universal algebra is in Section 5 and finite chains are consistency checks. |
| Proposition 4, undirected support limit | `sections/02_model_results.tex:125-136`; PDF p. 6, (2.11)-(2.12) | Every finite connected undirected weighted graph; exact support-degree limit and positive incomplete-support deficit. | Byte-identical, preserved. |
| Theorem 5, weighted triangles | `sections/02_model_results.tex:141-147`; proof `sections/06_low_order.tex`; PDF pp. 6,15, (2.13), (6.1)-(6.8) | Positive undirected triangle, every \(r>1\), complete-graph upper bound, equality iff all three weights agree. | Byte-identical, preserved. |
| Lemma 6 / Proposition 7, fair-geometric union dual and coverage | `sections/03_duality_collision.tex:3-106`; PDF p. 7, (3.1)-(3.9) | Positive loopless row-stochastic \(P\), no reversibility; OR law; proper-nonempty dual; irreducibility/aperiodicity; coverage formula; \(\rho=m(P)/n\); all mixed-difference signs. | Byte-identical, preserved. |
| Lemma 8, rectangular active-chain collision identity | `sections/03_duality_collision.tex:108-203`; PDF pp. 8-9, (3.10)-(3.18) | Distinct \(\mathcal Z_n/\mathcal Y_n\) phase spaces including empty cache; row-law ordering \(K=RA\), \(M=AR\); stationary phase laws and uniqueness; \(\nu H=1/m(P)=1/[n\rho]\); linearity. | Byte-identical, preserved. |
| Perturbation and tangent decomposition | `sections/04_local_hessian.tex:1-105`; PDF pp. 10-11, (4.1)-(4.10b) | Stationary expansion/sign; standard embedding; Frobenius-orthogonal dimensions \(n-1,n(n-3)/2,(n-1)(n-2)/2\); sum \(n(n-2)\); symmetric sector absent at \(n=3\); multiplicity-free physical decomposition. | Byte-identical, preserved. |
| Theorem 9, sector positivity and displayed eigenvalues | `sections/04_local_hessian.tex:107-161`; PDF pp. 11-12, (4.11)-(4.13) | Standard \(n\ge3\), symmetric-balanced \(n\ge4\), antisymmetric-balanced \(n\ge3\); eigenvalue table \(n=3,4,5\) remains \(1/11,\text{--},1/9;\ 87/640,3/208,57/640;\ 8585/57314,359/26660,143/2100\). | Byte-identical, preserved. |
| Standard-sector range | `appendices/A_sector_certificates.tex:216-245`; PDF pp. 19-21, (A.22s)-(A.23s) | Exact rational \(2\le N\le9\); analytic \(N\ge10\), bound \(2N(N-9)/(N-1)>0\); all eight exact table values unchanged. No endpoint gap. | Byte-identical, preserved. |
| Antisymmetric-sector range | Appendix A §A.2, lines 247-328; PDF pp. 21-22, (A.4)-(A.10) | Analytic positivity for every \(N\ge2\); strict Poisson-gradient recurrence, physical normalization, sampling-without-replacement expansion, and strictness unchanged. | Byte-identical, preserved. |
| Symmetric-sector finite and analytic ranges | Appendix A §A.3, especially lines 330-606; PDF pp. 22-26, (A.11)-(A.36) | Exact \(3\le N\le39\); all 248 orders \(40\le N\le287\); analytic \(N\ge288\); the auxiliary \(N=24\) exact minimum and \(N\ge25\) discriminant step; exact smallest margin at \(N=40\), \(639304267467075678841/115369588296792467144716>0\); \(\beta_N<19/20\), \(\varepsilon_N<1/20\), and first values \(3/208,359/26660\) unchanged. No endpoint gap. | Mathematical text byte-identical; only the bound file's digest changes. |
| Lemma 11, finite-state perturbation | `sections/05_strong_selection.tex:26-40`; PDF p. 13 | Analytic finite absorbing system and bounded-fundamental-matrix leakage statement. | Byte-identical, preserved. |
| Lemma 12 / Proposition 13, monotonicity and diverging support degree | `sections/07_implications_reproducibility.tex:8-60`; PDF p. 16, (7.1)-(7.2) | Every loopless row-stochastic kernel, every initial set, \(r>0\); fixed-\(r\) eventually-amplifying sequence implies reciprocal-degree average tends to zero and degree diverges in probability. | Byte-identical, preserved. |
| Theorem 16, two symmetric weighted-\(K_4\) families | `appendices/B_k4_certificate.tex:147-156`; PDF p. 28 | Every \(r>1\); both family inequalities; equality only at \(x=1\) or \(x=y=1\); expressly not a six-edge classification. | Byte-identical, preserved. |

## Hessian endpoint and normalization regression checks

The portions most susceptible to an accidental off-by-one or normalization regression are all on PDF pages that are pixel-identical to R1:

- The tangent dimensions and Frobenius orthogonality, p. 11, (4.9)-(4.10b).
- The displayed Frobenius-normalized eigenvalues, p. 12, (4.12).
- The standard physical normalization and exact \(N=2,\ldots,9\) table, pp. 19-21, (A.12s)-(A.23s).
- The antisymmetric physical normalization and strict recurrence, pp. 21-22, (A.4)-(A.10).
- The symmetric physical normalization, phase bounds, and finite-margin definition, pp. 23-25, (A.17b), (A.20)-(A.33).
- The \(N\ge288\) coefficient/discriminant tail and \(\beta/\varepsilon\) endpoint bounds, p. 26, (A.34)-(A.36); on this page only the earlier verifier hash differs.

Thus the splits

\[
\begin{array}{c|c|c}
\text{sector}&\text{finite/exact range}&\text{analytic range}\\ \hline
\text{standard}&2\le N\le9&N\ge10\\
\text{antisymmetric}&\text{none needed for the quantifier}&N\ge2\\
\text{symmetric}&3\le N\le39;\ 40\le N\le287&N\ge288
\end{array}
\]

still cover every physical order without a missing or duplicated boundary that changes the proof. The finite anti checks in code are now correctly described as checks rather than the source of the all-order quantifier.

## Certificate binding

The literal digest is intentionally not preserved because the bound verifier file changed mechanically. The **binding is preserved and internally exact**:

| Item | R1 | R2 |
|---|---|---|
| Actual `verify_true_inverse_rank_symmetric_phase.py` SHA-256 | `b4d45a83ce5f21a1fd3e09403b376e071330290a01affff64711574b69e024bc` | `7a1fa1f579c090cc32668392e67b9eb88e696b51ad602a90d069541e402aa512` |
| Appendix A printed digest | Matches R1 actual | Matches R2 actual at line 551 / PDF p. 26 |
| `verify_paper_claims.py` digest literal | Matches R1 actual | Matches R2 actual at line 30 |
| Internal and package manifest entries | Match | Both record the R2 actual digest (`MANIFEST.sha256:58`, `PACKAGE_MANIFEST.sha256:68`) |

The R2 verifier's normalized AST is mathematically identical to R1 after changing its 26 `assert` nodes to the corresponding 26 `require` calls. Therefore the new digest reflects the intended safety edit, not a changed symmetric-sector certificate.

## PDF content and layout audit

### Identity and metadata

| Property | R1 | R2 | Assessment |
|---|---:|---:|---|
| SHA-256 | `a6bda621b764ca8ee86658f6b68de0245790b84315eb77a6cc7ca45f7953bd2d` | `22142ee518e75c00d1948b19c210818ec797946df86a5e3272c9d1017800b0f4` | Expected content revision; R2 value matches package prose. |
| File size | 234,023 bytes | 234,169 bytes | +146 bytes. |
| Pages | 30 | 30 | Preserved. |
| Page geometry | 612×792 pt, rotation 0 | Same | Preserved. |
| Creator/producer | LaTeX with hyperref / xdvipdfmx (0.1) | Same | Preserved. |
| Creation date | 2026-08-20 17:00 PDT | Same | Preserved. |
| PDF version/encryption/forms/JavaScript | 1.5 / no / none / no | Same | Preserved. |
| Font inventory (`pdffonts`) | 22 font rows | Identical 22 rows | No font substitution/regression. |
| Convenience PDF vs nested source-tree PDF | Byte-identical | Byte-identical | Both R2 copies have the advertised digest. |

### Page-by-page result

Both layout-preserving and ordinary `pdftotext` comparisons identify only pages 17 and 26. Rendering both PDFs with Poppler at 96 dpi and comparing the resulting PNGs gives:

| Pages | Render result | Visual/content result |
|---|---|---|
| 1-16 | R1/R2 PNGs byte-identical | No content or layout change. |
| 17 | Different | Added four-line proof-status paragraph; preceding paragraph reflows by one line. “Statements and Declarations” moves down modestly but all text and the page footer remain comfortably within the page. No widow/orphan, clipping, overlap, or spill to p. 18. |
| 18-25 | R1/R2 PNGs byte-identical | No content or layout change. |
| 26 | Different | Only the centered 64-character SHA-256 changes. It fits on one line within the same measure. All equations, proof text, square end marker, and footer retain their positions. |
| 27-30 | R1/R2 PNGs byte-identical | No content or layout change. |

All 30 R2 pages were inspected in five six-page sheets. Because 28 R1 pages are byte-identical renders, those comparisons also inspect the corresponding R1 layouts; the two nonidentical R1/R2 page pairs were separately inspected at full-page resolution. Figures, tables, equation tags, hyperlinks as visibly styled, page numbers, headings, footnotes/declarations, and bibliography entries show no visual regression.

## Remediation-wording audit

| Revised wording | Source evidence | Assessment |
|---|---|---|
| Universal directed strong-selection algebra belongs to Section 5; executable chains are finite consistency tests. | Section 5 assumes symbolic \(n\ge3\) at line 44 and derives (5.4)-(5.16) without a finite-size extrapolation. The literal-chain program uses only the displayed \(n=3,4\) examples. | Accurate. |
| All-order antisymmetric positivity belongs to Appendix A; executable literal chains are finite. | Appendix A gives the recurrence/strict analytic proof for every \(N\ge2\). The code loops over recurrence values through \(n=40\) and full active chains through \(n=7\). | Accurate. |
| `verify_hessian_sectors.py` is a finite orbit check through \(n=12\), not the all-order proof. | Its `known` dictionary is exactly \(n=3,\ldots,12\); the final message now points to Appendix A. | Accurate. |
| All seventeen verifier/cross-check programs are invoked directly and the Makefile is not load-bearing. | Static call-by-call comparison of old Makefile targets with new `replay.sh` shows exact scientific coverage. | Accurate. |
| Imported-helper functions, module imports, and guarded mains are distinct. | Static import/call trace described above. | Accurate. |
| Scientific conditions remain active under optimized Python. | Each of the 406 R1 predicates is now the same operand of an explicit `require`; no mathematical condition was dropped or weakened. | Accurate as source wording; hostile runtime behavior was not executed in this gated subaudit. |
| Dependency wheels and Tectonic bundle are hash-bound. | `bootstrap_replay.sh` uses `--require-hashes --only-binary=:all: --no-deps` with the new lock; `build.sh` selects the v33 endpoint and checks the recorded content digest. | Accurate description of the scripts; external artifact provenance remains an execution/supply-chain audit item. |

No remediation statement was found that enlarges a theorem, converts a finite check into an infinite proof, or misstates actual replay reach. The Appendix A phrase “asserts every sign” is ordinary mathematical English (“checks every sign”); the program now uses explicit `require` calls, so it is not evidence of an optimization-elidable Python assertion.

## Exact command/status ledger

The following are the substantive reproducible commands. Here `R1` and `R2` denote the two absolute package paths stated under Scope. Commands returned status 0 unless explicitly noted.

| Command | Status/result |
|---|---|
| `find "$R1" -type f ...`; `find "$R2" -type f ...`; `comm -3` | 0; 81 R1 files, 82 R2 files; one removed and two added. |
| `diff -qr "$R1" "$R2"` | 1, expected because revisions exist; its complete changed-file list was classified above. |
| `find ... -name '*.tex' -o -name '*.bib'`; per-file `cmp -s` | 0; 10/12 identical, only Appendix A and Section 7 differ. |
| `diff -u` on the two changed TeX files | Underlying `diff` status 1, expected; the `|| true` inspection wrapper returned 0. Complete diff reproduced above. |
| Per-file `diff -u` on all 21 changed common Python files | Underlying `diff` status 1 per changed file, expected; the inspection wrapper returned 0. All diffs were read completely. |
| Read-only `python3` AST parse/normalization of all common changed `.py` files | 0; 20 scientific files, 406 R1 asserts, 406 R2 requires; normalized mathematical ASTs identical, subject only to the listed messages/hash. No package module was imported or executed. |
| `shasum -a 256` on both symmetric verifiers and both PDFs | 0; values reported above. |
| `shasum -a 256 -c PACKAGE_MANIFEST.sha256` from R2 package root | 0; every listed package member `OK`. |
| `shasum -a 256 -c complete_graph_extremality_db_source_and_certificates.tar.gz.sha256` | 0; archive `OK`. |
| `shasum -a 256 -c MANIFEST.sha256` from `R2/source_and_certificates` | 0; every internal member `OK`. An initial invocation from the package root returned 1 solely because `MANIFEST.sha256` is one directory lower; it was immediately rerun from the correct directory. |
| `cmp -s` for top-level vs nested PDF in each release | 0 for R1 and 0 for R2. |
| `pdfinfo` on both PDFs | 0; metadata table above. |
| `pdffonts` on both PDFs followed by `diff -u` | 0; no diff. |
| `pdftotext -layout` and ordinary `pdftotext` on both PDFs, split on form-feed, per-page unified comparison | 0; only pages 17 and 26 changed. |
| `pdftoppm -png -r 96` on both 30-page PDFs | 0; 60 page PNGs produced under `/tmp`. |
| Per-page `cmp -s` on the 30 render pairs | 0 for 28 pairs; 1 for pages 17 and 26, exactly matching the text/source diff. |
| `ffmpeg ... tile=2x3` to make five contact sheets per PDF; image inspection of all R2 sheets and changed page pairs | 0; no layout defect found. |

Two harmless audit-driver mistakes are recorded for completeness: the first zsh status loop attempted to assign the reserved variable name `status` and stopped before producing results; it was rerun unchanged with `result_label` and returned 0. The initial internal-manifest check used the package root rather than `source_and_certificates`, as noted in the table. Neither command wrote to or executed package content.

## Strongest verified result and remaining gaps

**Strongest verified result.** R2 is a mathematical-content-preserving remediation of R1. Every theorem-bearing formula and proof predicate is unchanged; every critical quantifier/range/equality/nonclaim is unchanged; the symmetric certificate is rebound to the exact remediated file; and the compiled document faithfully renders exactly the two intended prose/hash changes with no page-level regression.

**Exact remaining gaps.**

- None for mathematical-source regression, theorem-scope regression, certificate binding, or PDF content/layout.
- This subaudit did not execute the delivered safety preflight, replay, dependency bootstrap, verifier suite, or PDF rebuild because the parent imposed a pre-execution static gate. Therefore it makes no independent dynamic claim about failure propagation, wheel availability, toolchain behavior, or rebuilt-PDF identity. Those checks can be combined with this report after the gate is cleared.
- This regression audit does not re-prove the unchanged strong-selection, triangle, K4, and support-limit mathematics from first principles; it establishes that R2 did not alter those already audited R1 arguments. The fitness-two dual/local mathematics had been independently audited against R1 and is inherited verbatim except for the accurate proof-status sentence and digest.

**Regression verdict: fully preserved; no correction required.**

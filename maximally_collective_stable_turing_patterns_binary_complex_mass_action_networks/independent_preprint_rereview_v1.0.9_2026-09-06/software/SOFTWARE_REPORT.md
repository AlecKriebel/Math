# Independent software and release rereview — v1.0.9

Target: `94d5177485b9680be8b77f13448abf1f923963e8`, inspected on 2026-09-06. No manuscript or release source was changed. Commands ran against copies of the preserved archive. All paths below are relative to this audit's `source_snapshot`, unless explicitly identified as audit evidence.

## Verdict

The currently shipped numerical and exact-certificate data pass the release checks. The previously incomplete fresh build campaign is now complete. One additional **minor but substantive verifier representation defect** should be repaired: the `variables` field can change the printed mathematical meaning while escaping both direct and aggregate verification. This does not make the shipped coefficients or theorems false; it prevents the verification package from certifying all of the representation that it prints.

The parent reviewer independently raised a literature CSV column-shift error; I confirmed it in both canonical and portable copies. Mathematical and visual review beyond the software mechanisms is covered by the other referee reports.

## New finding: variable labels are not verified

**Affected locations.** `independent_verifier/verify_mode_isolation.py:21–51`, its duplicate `dd_verify_mode_isolation.py`, `frontier_verify_mode_certificates.py:189–239`, and `frontier_verify_exposition_identities.py:376–459` compare exponent tuples under hard-coded variable orders but do not check the JSON `variables` list. `computation/generate_tables.py:45–47,86–90` then uses that unverified list to generate the mathematical degree-column headings.

**Concrete witness.** Change only the homogeneous section's `variables` in `improved_modulus_certificate.json` from `["x","z"]` to `["z","x"]`, keeping every numeric coefficient, row count, and exponent tuple unchanged. The declared polynomial changes from `E(x,z)` to `E(z,x)`. Reconstructing

\[
E(x,y^2)=(1+\lambda)(1+\bar\lambda)P(\lambda)P(\bar\lambda)-R(\lambda)R(\bar\lambda),
\quad \lambda=x+iy,
\]

where `P(v)=v⁴+12v³+42v²+47v+16` and `R(v)=5v²+33v+16`, gives `E(1,2)=238914`. The altered variable-labelled JSON gives `2004282` at the same point: a difference of `1765368`.

The direct `verify_mode_isolation.py` command returns success. With the original generated TeX left unchanged, `frontier_verify_exposition_identities.py` correctly rejects the stale table. After `generate_tables.py` regenerates the table from the changed labels, the **complete `verify_symbolic_certificates.py` aggregate returns `ALL_SYMBOLIC_CERTIFICATES_PASS`**, including its printed-table freshness check. The printed heading is then `deg_z, deg_x` while the theorem's coefficient identity requires `deg_x, deg_z`.

This is a semantic input, not an unknown descriptive field: the production generator explicitly consumes it in the displayed polynomial. The documented exemption for unknown descriptive metadata therefore does not resolve this mismatch. Arbitrary ordering of distinct *rows* is harmless and should remain accepted; ordering of the *variables associated with each exponent vector* is a different matter.

**Containment and scope.** The original release SHA-256 manifest rejects the altered certificate and generated table, so this does not demonstrate a bypass of an untouched downloaded release's hash gate. It is a false acceptance in mathematical/generator validation during editing or regeneration. The shipped variable lists are correct. The full symbolic aggregate also contains wrappers and duplicate implementations; aggregate success is not separate proof evidence.

**Required repair.** Require each known table's exact variable tuple (`["x","z"]` or `["x","z","s"]`) in every reader and in the table generator, or make the generator use a trusted fixed variable tuple. Add a test that swaps labels, regenerates the printed table, and still requires the mathematical aggregate to reject it. For the scaled tables, also preserve the existing distinction between coefficient parameters `U` and `A`. Do not reject harmless unknown descriptive fields merely to satisfy this finding.

Evidence: audit `check_variable_order.py`, `VARIABLE_ORDER_WITNESS.json`, and `logs/variable_order_*.log`. The witness rebuilds the polynomial independently from the displayed modulus expression; no production helper is used for that comparison.

## Confirmed literature-table regression

`literature/theorem_comparison.csv:15` and `public/repository/literature/theorem_comparison.csv:15` parse as:

| Field | Actual value |
|---|---|
| Exact diffusion law | numerical continuation |
| Nonlinear branch | numerically stable segments |
| Stable branch | no |

The intended values belong one field later, with `no` in the exact-law field. This contradicts the revised main-text acknowledgement of numerical continuation and stable segments. `audit_manuscript.py:404–405` checks the main-text phrases, not this field mapping; its success does not close this defect. The parent reviewer is assessing the primary literature and exact editorial correction. Audit evidence: `CSV_COLUMN_WITNESS.json`.

## Closed findings and fresh execution results

| Check | Fresh result and evidentiary boundary |
|---|---|
| Immutable commit archive | 1,372 project files; all match the preserved source snapshot. |
| Tracked source manifest | All 1,371 entries verify and equal the archived file set excluding the manifest itself. |
| Portable manifest | All 212 entries verify before generators run. |
| Regression suite | **32 passed, zero failed, zero skipped.** |
| Direct verifier entrypoints | All **39** pass under the pinned Python package versions. |
| Optimized Python controls | All **39** reject with assertions-disabled diagnostic. |
| Minimal replay | `MINIMAL_VERIFIER_PASS`. |
| Full clean portable replay | `PUBLIC_REPLAY_PASS`, including current symbolic suite, all 15 numerical cases, figures, TeX, and PDF audits. |
| Exact regenerated baseline | All 13 selected JSON/TeX artifacts match the shipped baseline bytes; the baseline manifest remains unchanged. |
| Numerical illustration audit | Pass; maximum refinement relative difference `1.4095038570570294e-08`. These are illustrations, not proof substitutes. |
| Seven package ZIPs | CRC/path checks pass; independently regenerated archives match every original SHA-256 byte for byte. |
| Detached source builds | bioRxiv, arXiv, and SIADS sources each compile from clean extraction. All three supplement auxiliary/TOC states stabilize. |
| Detached PDF comparisons | Six extracted layout-preserving text streams exactly match their intended shipped manuscript/supplement PDFs. No PDF byte-equivalence claim is made. |
| Shipped PDF audits | Full and journal profiles pass. Root reviewer separately inspects the pages visually. |
| Actual release assets | All **nine** downloaded GitHub release assets byte-match the target snapshot and GitHub's published SHA-256 digests. |
| Remote tag | Annotated tag peels to precisely `94d5177485b9680be8b77f13448abf1f923963e8`. |

The original extra/missing/duplicate support defect is repaired: raw length, declared count, regenerated count, unique exponent tuples, complete support, and exact coefficients are enforced. Fresh regression tests exercise extra rows, missing rows, and identical/conflicting duplicates placed before and after legitimate rows. The new variable-label finding is a separate semantic gap.

## PDF overlap gate

Read the entire new `audit_modulus_table_spacing` implementation. It isolates the four modulus tables, detects degree-column row baselines, associates coefficient word boxes, counts all 218 rows, checks a broad horizontal page margin, and enforces at least one point of vertical clearance for adjacent coefficient boxes whose horizontal extents overlap. It is a targeted table-spacing regression check, not a general proof that every piece of ink in every document is legible or semantically unambiguous.

Both current supplements have **218 detected rows** and minimum adjacent coefficient clearance **3.108212 points**. As a negative control, I passed the older overlapping supplement to the current function **while keeping the current single-line-fraction TeX source**; this avoids merely testing the source-string ban on `\frac`. The geometry check rejected it with `−1.513` points of clearance. Thus the gate detects the originally observed physical collision. Whether the new slash notation has an ambiguous adjacent variable is a separate mathematical typography question handled in the root report; this geometry gate does not claim to settle that question.

Audit evidence: `check_pdf_gate.py`, `PDF_GATE_RESULTS.json`, and `logs/pdf_geometry_gate.log`.

## Environment, reproducibility, and unexecuted scope

The existing TinyTeX 2022.04 installation and Biber 2.17 were reused; nothing was downloaded to install a toolchain. The pinned stack is recorded in `PINNED_PYTHON_ENVIRONMENT.json`. A first portable launch used the workspace virtual environment, which lacks `matplotlib`; it failed at preflight before mutation. Switching to the existing system CPython 3.9.6 user-site packages and the already available pypdf 6.10.0 resolved it. Initial exploratory verifier runs with the workspace package versions also passed, but every one of the 39 normal and optimized commands was repeated under the pinned stack for the reported qualification result.

The top-level historical-lineage preflight was actually exercised and exited 2 because all five external archival inputs were absent in `/mnt/data`; its archived replay log was preserved. Source inspection confirms those five files are used only in the initial checksum loop, with no later extraction or proof/build dependency. The complete current portable replay, source builds, and fresh packaging all succeeded independently of them. No claim is made that the optional historical-lineage campaign ran successfully.

This audit read the changed certificate readers, printed-table checks, table generator, PDF gate, test additions, and release/replay/package orchestration. All 39 executable entrypoints were executed; that count is **execution coverage**, not a claim that 39 mutually independent proofs were reviewed line by line. Independent theorem verification belongs to the mathematics reports. No external message, submission, new tag, or release mutation was performed.

Machine-readable evidence: `VALIDATION_SUMMARY.json`, `COMMAND_RESULTS.jsonl`, `RELEASE_METADATA.json`, `RELEASE_ASSET_INTEGRITY.json`, and `portable_replay_evidence/`. Reproduction scripts use disposable `scratch/` directories, which are excluded from publication.

To reproduce locally, use the release's tested Python environment and TeX distribution, then run `python audit_driver.py setup`, followed by its `tests`, `verifiers`, `portable`, `packages`, and `detached` actions. `REFEREE_PATH`, `REFEREE_PYTHONPATH`, and `REFEREE_REPO` can override the recorded machine-specific defaults. The two focused defect/gate scripts use that same driver environment. The historical PDF negative control additionally requires the prior `6f68ad3e` supplement, as its script explains. The source snapshot is never mutated by these scripts.

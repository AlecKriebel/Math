# Independent referee audit research log

## 2026-08-22T21:59:04-07:00 — Evidence freeze

- Scope: independent audit of release packet `full_referee_validation_packet_v1.0.7` for *Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*.
- Source packet preserved at `source_snapshot/`; all executions are confined to `working_packet/` or further disposable copies.
- Supplied outer manifest verified before execution: 263/263 entries matched, exit status 0.
- Supplied inner repository manifest verified before execution: 198/198 entries matched, exit status 0.
- Original git state: branch `main`, one commit ahead of `origin/main`, with unrelated pre-existing modified/untracked paths outside this audit folder. Those paths will not be altered.
- Three independent review families started: core algebraic claims, nonlinear/PDE claims, and software/reproducibility semantics.
- Best-guess completion: **5%**. The evidence is preserved, but no mathematical conclusion or replay outcome has yet been accepted.

## 2026-08-22T22:07:00-07:00 — Full document read and independent dependency reconstruction

- Read all 1,217 lines of `main.tex` and all 971 lines of `supplement.tex`, rather than relying on the author-provided review maps.
- Rendered and visually inspected all 18 manuscript pages and all 18 supplement pages. Fonts are embedded; no clipping, overlap, missing page, or unreadable figure/table defect was apparent in the six full-document contact sheets. The dense supplement coefficient tables remain legible at page resolution.
- Confirmed that the packet reading PDFs and repository manuscript PDFs are byte-identical.
- Constructed `THEOREM_DEPENDENCY_MAP.md`, recording exact domains, conclusion types, direct dependencies, evidence types, and source-line locations.
- Static wrapper inspection found two host preflight gaps before execution: no `pdflatex` command, and the default `python` lacks required `pypdf`. The exact advertised wrapper will therefore be run and recorded as a non-pass; non-document stages will be pursued separately if the full environment cannot be made available transparently.
- No central contradiction has been found at this checkpoint. This is not a validity finding: certificate identities, verifier semantics, nonlinear reductions, boundary cases, and replays are still under audit.
- Best-guess completion: **24%**.

## 2026-08-22T22:14:00-07:00 — Independent exact checks and first publication checkpoint

- Reconstructed the reaction matrices, SCCs, omission minors, critical vectors, harmonic corrections, and representative cubic contractions without importing any submitted helper.
- Independently expanded all four load-bearing modulus polynomials and verified their exact term counts, coefficient signs, and equality loci.
- An independent symbolic recurrence reduction established the all-dimensional cubic bridge that the short submitted verifier itself checks only at six finite dimensions.
- Numerical falsification covered 76,560 smaller-block cases and both scaled endpoints through `m=149`; no contradiction was found, but near-machine-precision margins are recorded as numerical evidence only.
- Committed checkpoint `d37eb493` on `main` and pushed it successfully to `origin/main`.
- Best-guess completion: **45%**. Mathematical evidence is increasingly favorable; full software semantics, exact replay coverage, mutations, cited functional analysis, and final adversarial synthesis remain open.

## 2026-08-22T22:38:00-07:00 — Independent review families and execution campaign

- Core and nonlinear review families independently reconstructed the load-bearing algebra, spectra, endpoint/equality cases, normal-form contractions, conservation gauges, and high-dimensional checks. No in-domain counterexample or transferred central gap was found.
- Read every load-bearing verifier, shared helper, generator, audit, test, simulation, and orchestration source before assigning evidentiary weight to its output. The 38 entrypoints were classified as exact, finite, numerical, aggregate, or provenance checks; duplicate and common-source layers were identified.
- The minimal replay, all 38 entrypoints, all 22 tests/mutations, exact generators/exporters, manuscript/stale/numerical audits, 15 full simulations, and three figure generators completed. Separate independent mutations were rejected and a forced child failure propagated.
- The first literal all-in-one run was unavailable past preflight because the base host lacked `pdflatex`; this was recorded as not checked, not passed.
- Best-guess completion: **82%**. The remaining work was exact document-route coverage, final adversarial synthesis, and report publication.

## 2026-08-22T22:54:00-07:00 — Historical TeX route, exact defect, and final verdict

- Ran the pristine wrapper using disposable TinyTeX 2026.08, full TinyTeX 2022.08/Biber 2.18, and full TinyTeX 2022.04/Biber 2.17. Both 2022 environments built all figures and both 18-page manuscripts and reached the final PDF audit.
- The unmodified wrapper still exits 1: `pypdf==6.10.0` extracts the correct supplement wording as `withu the Latin letter`, while the audit requires literal `with u the Latin letter`. A one-condition whitespace-normalized regex repair in the disposable work root passes. The pristine source snapshot still passes all 263 outer hashes, and the submitted `audit_pdfs.py` remains byte-identical in the source snapshot and execution copy.
- The modern TeX build also changes supplement pagination and two extraction/layout probes, confirming that the TeX stack needs pinning. The supplied PDFs use an `xdvipdfmx` producer while the scripted route is pdfLaTeX.
- Final technical category: **VALID AFTER MINOR CORRECTIONS**. Recommendation: **minor revision**. No mathematical hypothesis, conclusion, endpoint, dimension range, or headline claim requires alteration; required fixes are local reproducibility/software/expository corrections.
- Best-guess completion: **100%**. Every failed or incomplete stage is disclosed in `REFEREE_REPORT.md`; the full unmodified wrapper completion box remains deliberately unchecked.

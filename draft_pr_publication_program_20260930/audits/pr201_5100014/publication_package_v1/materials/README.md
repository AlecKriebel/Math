# A flag-curve proof of an outer-pedal area invariant
Alec Kriebel, 16 October2026. Unrefereed, extensive AI assistance.

This is an attributed alternative proof presentation of k303,a under an explicit primitive least-period convention. Ferudun DOI10.5281/zenodo.23087221 v1.0 already gives the exact theorem, radial dependence, general hexagon constant and repeated-triangle caveat; v1.1 DOI10.5281/zenodo.23088516 preserves it. No theorem/method novelty, first-publication priority or certified independence is claimed. The analytic proof in outer_pedal_flag.tex establishes the universal result; finite controls do not.

Scope: a>b>0,0<lambda<b^2, strictly nested confocal ellipses, exact least N=2mod4>=6, every fixed finite real M, signed shoelace areas in orbit order including primitive stars, reversal and zero/negative pedal areas. Feet are on boundary tangents. No unrestricted repeated-odd-list, hyperbolic, degenerate, nonconfocal or unsigned filled-face extension follows.

## Reproduce
Use Python3.11 or newer with the pinned SymPy1.14.0 and mpmath1.3.0 from requirements.txt. Validation used Python3.14.6. No dependency implementation is distributed. In an environment containing those packages, from this extracted directory run:
python -B verification/run_checks.py
python -B -O verification/run_checks.py
python -B verification/run_checks.py --full-physical
python -B verification/run_checks.py --guard-false
python -B -O verification/run_checks.py --guard-false
The final two commands must fail with DELIBERATE FALSE CONDITION. The full physical sweep takes several minutes. Results are printed; no package inputs are mutated. Text is byte-compared; JSON comparison removes only UTC, optimization and elapsed_seconds. The runner verifies every manifest entry before checks. A hash is integrity evidence, not a mathematical proof or independent signature. SymPy reductions and noninterval high-precision numerics are disclosed limitations.

The exact source-family script checks the displayed M=(1,0) repeated-triangle products and154 conditions. Other exact controls verify general-semiaxis two-axis hexagon identities, physical reflection for fixed exact examples, a distinct repeated triangle at M=(1,2), nonconfocal failure and classical signed radiality. The physical checker rebuilds tangency/contact and second ellipse intersections directly, without importing the candidate's flag proof or Jacobi parametrization. It checks56 primitive cases over N6,10,14,18,22/all tested coprime windings/four aspect ratios plus repetition and negative/zero controls. It is finite noninterval evidence.

PORTABILITY_PROVENANCE.json pins each original and portable script: the only code edits remove local research-runtime path insertion. All mathematical operations/checks are unchanged. Original programs and historical receipts are separately preserved under audit; original assertion-based reviewer outputs under -O enforce zero assertions and must not be mistaken for validation. Deliberately false fixtures under audit are clearly labeled enforcement countercontrols, not claimed identities.

## Audit and provenance
audit/ preserves the explicit authored mathematical and priority gate allowlists with immutable original24 submission files and custody. These are historical stage artifacts, including pre-publication pending status and deliberately retained initial failed control hypotheses. They do not describe the final package's review/publication status. The current manuscript/metadata and ROOT_SOURCE_SCOPE_CORRECTION_01.md supersede the original SOURCE_AUDIT literal claim that the table prints primitive: it does not. Original files remain unchanged for accountability. The two gate files authenticate their listed inputs; each gate excludes itself from its own safe_files map.

Full third-party PDFs, scans, OCR, archives, raw API payloads, browser state, credentials and dependency software are excluded. Authored receipts contain bibliographic URLs and file hashes so inspected editions can be identified without redistributing full texts. Search is bounded; unread sources/access limits remain documented. The general family's unread-book gap was partially supplemented by exact-history cached contents/pedal-context inspection, not a comprehensive book theorem audit.

Observed PR201 creation2026-10-01T05:18:49Z at original HEAD90bdb85235979f2ffa7496b9b689036654e55200 precedes the current Zenodo v1.0 creation16:56:14.316216Z and registry16:56:15Z on that date. Those heterogeneous witnesses do not establish first public visibility or independence. October16 audit additions are not backdated. Author effort was one original substantive turn, QUEUE1/5; exact model/reasoning effort unverified. Three later mathematical families, three priority families and subsequent publication-package adversaries are distinct stages; the partial Euclidean reduction is not a separate full proof. Automated review is not conventional human refereeing or proof-assistant certification.

The three intended Zenodo uploads are the PDF, identical standalone LaTeX source, and verification-package.zip. materials/metadata.json is the exact intended metadata, also in the deposit manifest. This ZIP omits its own final PDF/ZIP and external publication-operation state to avoid circularity. MANIFEST.json excludes itself. License: CC BY4.0 for the authored materials; no license to third-party full texts is asserted.

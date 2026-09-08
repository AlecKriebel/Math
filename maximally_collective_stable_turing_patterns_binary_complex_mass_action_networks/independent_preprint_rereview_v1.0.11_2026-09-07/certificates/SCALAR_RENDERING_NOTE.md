# Separate bounded note: noncanonical scalar rendering

**Assessment: low-priority software hardening for noncanonical or malformed external certificate inputs. This does not alter the C1 closure or the correctness of the shipped preprint.**

Target: `137ffa9f1a340f621651395ad0236cf1bdadb51c`. Evidence completed 2026-09-08T04:28:59Z (September 7 local).

The scalar readers convert supplied coefficients with `sp.Rational` (`independent_verifier/verify_mode_isolation.py:32`, its duplicate, and the unit section of the exposition reader). The TeX generator instead converts the supplied object directly to a string (`computation/generate_tables.py:18–23`, used at `:88–90`). Those operations differ for some values outside the canonical integer/fraction strings used by every shipped coefficient.

## Minimal witness and observed acceptance

In `improved_modulus_certificate.json`, change only `homogeneous.terms[0].coefficient` from string `"1"` to JSON boolean `true`. This row has powers `[10,0]`. All three relevant reader calls accept it because the exact parser maps the Boolean to rational 1. Actual regeneration writes `10 & 0 & $True$` at line 9 of `data/certificate_tables.tex`.

In an isolated scratch copy, the following all return zero:

1. Ordinary table regeneration.
2. The complete `verify_symbolic_certificates.py` aggregate, ending in `ALL_SYMBOLIC_CERTIFICATES_PASS`.
3. The manuscript source audit with `release/` and `submission/` present, including their conditional wiring and source checks, ending in `MANUSCRIPT_AUDIT_PASS`.
4. A three-pass supplement build with the pinned TeX toolchain.
5. The canonical `--profile full` PDF audit, ending in `PDF_SEMANTIC_AUDIT_PASS`; only the supplement PDF was rebuilt, and the other audited PDFs were copied unchanged from the frozen target.

The final selected TeX-warning set is empty. The scratch supplement remains 19 pages and its PDF evidence reports 218 table rows and 3.108-point minimum clearance. Visual inspection of the complete page 11 confirms that the coefficient is actually displayed as the italic letters `True`; the PDF's extracted text separates this as `T rue`. The existing PDF audit does not reject that nonnumeric coefficient.

The alternative scalar string `"1e0"` also maps to rational 1 in all three direct readers, but the generator writes `$1e0$` instead of canonical rational notation. That alternative was verified through the direct readers and generator only; the full aggregate/PDF experiment was performed on the Boolean witness.

## Meaning and containment

The true x^10 coefficient of the stated homogeneous polynomial is 1, as independently reconstructed by the algebra reviewer. The accepted Boolean does not change the numeric polynomial used by the proof checks. It changes the generated display into letters that are not a defined rational coefficient. This is a rendering/validation inconsistency, not a counterexample to the proved polynomial identity.

All actual shipped coefficients are canonical integer/fraction strings, and independent parsing confirms all 218 displayed rows exactly. The outer `certificate_schema.json` does not define an enforced lexical schema for individual coefficient values; canonical scalar spelling is a producer convention. The witness therefore examines a broader accepted-input boundary than the actual release data.

The immutable published manifest detects the changed JSON, generated TeX table and PDF, with all three original hashes confirmed against the untouched target. This experiment does not replace a release asset or bypass its hash checks. No reader or generator program was changed, and all experiments are confined to scratch copies.

The unchanged-table freshness check also rejects the altered JSON against the shipped table with `STALE_GENERATED_MODULUS_TABLE`. The successful path includes ordinary table regeneration. The full package-refresh/release workflow was not run on the scalar mutant, and no claim is made that every later packaging step would accept it. The observed acceptance scope is precisely the direct readers, regeneration, symbolic aggregate, source audit, canonical supplement build and canonical full-profile PDF audit listed above.

## Proportionate repair

For future package hardening, render from the parsed exact rational value rather than the original object or spelling. Reject Booleans explicitly if the input contract requires numeric coefficient data. Alternatively, enforce and document canonical integer/fraction strings in both the readers and generator. The Boolean and scientific-string examples form two bounded regression cases; no broad parser redesign or mathematical revision is needed.

I do not recommend delaying submission of the correctly rendered frozen preprint solely for this noncanonical-input edge. The package should not claim a stronger input-format guarantee than its checks provide. The root referee may distinguish this optional software maintenance from any required publication corrections.

Evidence: `probe_scalar_rendering.py`, `SCALAR_RENDERING_RESULTS.json`, `boolean_true_certificate.json`, `scientific_string_certificate.json`, `scalar_full_symbolic_suite.log`, `scalar_source_audit.log`, `scalar_full_pdf_audit.log`, `scalar_mutant_pdf_evidence.txt`. The complete scratch build is ignored as disposable evidence; the retained script recreates it. Independent mathematical scope review: `../algebra/SCALAR_REPRESENTATION_CROSSREVIEW.md` and its companion exact-check script/results.

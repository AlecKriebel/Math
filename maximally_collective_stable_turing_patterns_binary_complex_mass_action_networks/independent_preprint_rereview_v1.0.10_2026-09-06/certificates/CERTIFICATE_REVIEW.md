# Certificate referee review of v1.0.10

Reviewed commit: `953c836a12b9d9d474521feb4a96e218c1155203`.

The prior ordered-variable and fraction-rendering findings are closed. One distinct, bounded defect remains in the connection between validated coefficients and their generated TeX table. The currently published coefficients are correct; this is a false-acceptance path in the supporting verification package, not a counterexample to the paper's theorems.

## C1. A conflicting known coefficient field overrides the validated coefficient

**Recommended disposition: correct before the next preprint/package update.**

In `computation/generate_tables.py:69–72`, a Pareto row containing `coefficient_in_U_ascending` is always rendered from that field, even when the row belongs to the spatial table whose coefficients must be read from `coefficient_in_A_ascending`. The exact readers do the latter correctly (`independent_verifier/frontier_verify_mode_certificates.py:229–236` and `frontier_verify_exposition_identities.py:447–460`). They do not reject the conflicting extra known field. Consequently the producer and readers can interpret the same row differently.

The witness changes only one JSON row in `pareto_all_m_certificate.json`, within `modulus.spatial.terms`. It retains powers `[6,1,0]` and the correct `coefficient_in_A_ascending: ["8281/24300"]`, then adds `coefficient_in_U_ascending: ["1"]`. This is a recognized coefficient field, not unknown descriptive metadata: the table generator actively selects it.

The two direct mathematical readers accept this file. Regenerating the TeX table changes its line 177 from `6 & 1 & 0 & $8281/24300$` to `6 & 1 & 0 & $1$`. The complete symbolic suite then prints `ALL_SYMBOLIC_CERTIFICATES_PASS`; the manuscript source audit prints `MANUSCRIPT_AUDIT_PASS`. The printed-table freshness check accepts because it compares the table with the same producer that selected the wrong field.

The displayed spatial polynomial differs from its claimed source identity by

\[
\widetilde E_{84}-E_{84}=\frac{16019}{24300}x^6z.
\]

At the allowed positive test point `x=z=s=1`, with `A=4` (for example, the scaled family with `nu=3, L=2/3`), this difference is `16019/24300`, not zero. The algebra reviewer independently reconstructed the boundary polynomial and all 84 displayed terms without importing the project implementation, confirming the identity failure. The unchanged original table equals that independently reconstructed polynomial exactly.

### Containment and limits

- The source snapshot itself has no conflicting fields, and all of its displayed coefficients are correct.
- A scratch supplement built in three passes with the pinned TeX toolchain retains 19 pages and has no final-pass TeX warnings. Visual inspection of its complete page 14 confirms that the altered row actually prints `1`.
- The full PDF audit also prints `PDF_SEMANTIC_AUDIT_PASS`, reporting 218 rows and 3.108-point minimum adjacent-row clearance. This is consistent with its geometric purpose; it does not supply an independent coefficient identity check.
- The published SHA-256 manifest detects all three changed files: JSON, generated table and rebuilt PDF. Therefore this does not silently alter an immutable downloaded release or defeat its integrity check. The gap occurs when validating and packaging newly generated artifacts with refreshed hashes.
- Before regeneration, the table freshness check rejects the changed JSON against the unchanged shipped table with `STALE_GENERATED_MODULUS_TABLE`. The successful attack includes ordinary table regeneration; it does not claim to bypass this stale-artifact check.
- No script was changed in the experiment. The result does not depend on replacing a verifier with a malicious program.

### Bounded repair

Select the coefficient key and parameter explicitly from the known table being generated: the 22-term table uses `coefficient_in_U_ascending` and `U`; the 84-term table uses `coefficient_in_A_ascending` and `A`. Reject a conflicting alternate coefficient field, or ensure it is never consumed. Retain harmless descriptive metadata only when it cannot change rendering.

Add a negative control with both known coefficient fields in one spatial row, including the regenerate-then-check path. An independent parse of all generated table coefficients into exact rational polynomials provides a stronger check that the final display equals the regenerated source polynomial; the audit's independent parser demonstrates that this is feasible for all 218 rows. The correction need not change any published coefficient or mathematical result.

Reproduction: run `probe_conflicting_fields.py` with a SymPy-capable Python. This builds only a scratch copy, runs both direct readers, runs the complete symbolic suite and the source audit, and writes the mutant and results. `check_mutant_pdf_gate.py` rebuilds only the scratch supplement using the recorded pinned toolchain and exercises the full PDF audit. It also records published-hash containment. Exact tools and paths are explicit in the scripts.

Evidence: `CONFLICTING_FIELDS_RESULT.json`, `conflicting_coefficient_fields.json`, `conflicting_coefficient_fields_table.tex`, `full_symbolic_suite_conflicting_fields.log`, `manuscript_source_audit_conflicting_fields.log`, `MUTANT_PDF_GATE_RESULT.json`, `mutant_supplement_pdf_evidence.txt`; independent mathematical cross-check in `../algebra/check_conflicting_field_mathematics.py`. The separate parser review in `render_equivalence/CROSSREVIEW.md` also reran both direct readers, reproduced the generated bad row, rejected it with independent exact-rational parsing, and separately reconstructed the boundary-polynomial discrepancy.

## Closure of the previous findings

**N2, ordered variables: closed.** Four certificate sections reject swapped variable declarations in 14 direct reader/generator calls. All 26 relevant current unpacked copies and all 12 reader copies in the seven current ZIP bundles match the corrected canonical implementations. The named historical v1.0.7 packet is not among the current seven bundles or nine release assets and is not a stale current reader. Evidence: `check_ordered_variables.py` and `ORDERED_VARIABLE_RESULTS.json`.

**N4, rational parameter notation: closed.** An independent restricted-grammar parser using exact rational arithmetic checked every one of the 218 rows in both releases against the unchanged exact JSON. Exactly 50 expressions changed and every coefficient polynomial is preserved. All five current table copies are identical; no residual `a/bA` notation or malformed shipped expression was found. Three negative controls confirmed that this independent checker rejects restored ambiguity, a changed numerator, and the wrong coefficient parameter. Evidence: `render_equivalence/REVIEW.md`, script and results.

No additional certificate finding is supported by this review. Standard full-suite release replay is handled independently by the release reviewer rather than being counted again here as separate mathematical evidence.

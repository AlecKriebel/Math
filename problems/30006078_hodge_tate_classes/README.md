# 30006078: reviewed higher-class partial results

**Original Hodge–Tate characteristic-class question remains unsolved after five substantive author turns.** The independent source/proof audit passes the scoped packet without a mandatory mathematical correction. No local-system counterexample, unrestricted formula, degree-one normalization theorem or historical novelty is claimed.

Start with FINAL_RESULT.md for the exact partial scopes, then SOURCE_GATE.md and TURN_1.md through TURN_5.md. The retained results include potentially arithmetic/scalar-geometric classes, proper-base tensor identities, exact failures of cup-product cancellation, and divisor-detected cases over Q_p. Properness, field, rational splitting and normalization qualifications are essential. Turn5 is a consequence of the report's credited top-degree theorem with compatible trace normalization; its underlying comparison theorem has not been independently reconstructed here.

The independent report is review/REVIEW.md. All38 frozen author artifacts and all4 frozen review artifacts are preserved byte-for-byte. Historical files which say review pending or1/5 are historical checkpoints; REVIEWED_STATUS.json gives the final reviewed status. Publication adds only this wrapper, the reviewed status, a portable runner and the publication manifest.

## Reproduce

- Run python3 verify_turn1.py through python3 verify_turn5.py from this directory. Python3 and SymPy are required. Compare output to the respective TURN_n_CHECKS.json.
- Author total:225,891 exact finite assertions. Independent total:1,680, including integrity checks. These supplement the analytic arguments and do not replace the credited p-adic theory.
- The unchanged independent checker contains its original local paths. Use `python3 review/run_portable.py --source-dir /path/to/downloaded/source_pdfs` to adapt only those locations. The seven required PDFs are named and linked in SOURCE_MANIFEST.json and SOURCE_ADDITION_T3.json. The runner performs every original mathematical and source-integrity assertion; compare its output to review/INDEPENDENT_CHECKS.json.
- Raw source PDFs, renders and imported data are not distributed. Their hashes and primary URLs are bound in the source manifests.

This is a draft research record, not human peer review or a merge/release request.

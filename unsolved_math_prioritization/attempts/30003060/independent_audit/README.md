# Independent audit: positive-characteristic higher Koszul obstruction

Read MATHEMATICAL_AUDIT.md and SOURCE_SCOPE_AUDIT.md for the actual verdict. The unrestricted written equivalence is false. The characteristic-zero converse remains unresolved in this investigation. One substantive approach is recorded; this is AI-assisted review, not external human refereeing.

ORIGINAL_ACCEPTANCE.json distinguishes acceptance of the original mathematics from the required source/execution corrections. CORRECTED_ACCEPTANCE.json binds the separately frozen corrected derivative and its actual replay. CORRECTED_DERIVATIVE_BINDINGS.json and the three patch files record exact changes. EXECUTION_AUDIT.md states which runs passed, which intentionally rejected optimized mode, and which original bootstrap path was not run.

The independently implemented mathematical controls are in independent_math.py and INDEPENDENT_MATH_RESULTS.json. Use python -I -S -B, optionally adding -O; both modes are supported by this independent checker. The audit's separately pinned external bootstrap validates this whole audit archive before running that checker. It does not redo textual review or source downloads.

To rerun the hostile/negative controls after verifying the archive, run test_replay_controls.py with python -I -S -B and pass the directory containing the separately supplied corrected ZIP, manifest and bootstrap. The program independently pins all three and refuses changed bootstrap bytes before launch. The saved REPLAY_CONTROL_RESULTS.json records all eighteen controls; normal and optimized control-harness outputs were identical.

CORPUS_SOURCE_VERIFICATION.json records complete original corpus and six-PDF hashes. CORRECTED_PROVENANCE_RESULT.json adds the v1 PDF to a separate actual provenance replay. No source texts, PDFs, raw records, dataset contents, private source material or private coordination files are distributed. Only authored mathematical prose/programs, public bibliographic metadata, byte counts/hashes, match results, patches and acceptance/audit reports are included. No publication or queue mutation was performed.

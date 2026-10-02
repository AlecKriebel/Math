# Preserved failures and their meaning

- The fresh web extraction of the literal archive URL returned an access error. The literal HTTP retrieval independently succeeded; hashes and retrieval timing are in sources/recovered_author_notes_metadata.json.
- The direct current author URL returned HTTP404. This is recorded by fresh_fetch.py in FRESH_RETRIEVALS.json; cached search text is not evidence of current direct availability.
- The first control_audit.py run used ROOT.parents[4] and selected /Users/alec/Documents instead of /Users/alec/Documents/Math. Readonly git cat-file failed with “not a git repository,” exit128. No outputs or shared files were changed by that failure. It was corrected to ROOT.parents[3] and the entire control program completed successfully. This was an audit-program routing mistake, not a source-package defect.
- The deliberately undersized reservoir code failed. Its full exception is retained in undersized_reservoir_stderr.txt. This demonstrates detection of an actual finite coupling mutation.
- Empty-proof and false-universal-claim mutations did NOT fail raw finite checkers. These are expected negative results about the reach of those checkers; changed note hashes and frozen binding rejected them. Their stdout/stderr are retained in the corresponding files and CONTROL_RESULTS.json.

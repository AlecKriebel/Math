# Independent audit of Function Theory 3.21

Read `ACCEPTANCE.md` for the decision and `MATHEMATICAL_AUDIT.md` for the full mathematical scope check. This audit accepts the unchanged author freeze as a credited prior-result verification, with `already_solved` and authored effort `1/5` recommended.

The packet contains authored reports, checker code, and public verification metadata only. Original articles, PDF images, extracted source text, dataset rows, and private coordination material are excluded.

## Reproduction

First validate this packet with its independently pinned external audit bootstrap, using Python `-I -S -B`. `verify_audit.py` is an internal consistency checker, not a mathematical proof verifier or its own authenticated entrypoint.

After validation, `replay_author.py AUTHOR_ARTIFACT_DIRECTORY ORIGINAL_PACKET_DIRECTORY` verifies the pinned original author inputs and runs the 46-case author-bootstrap matrix. Run with Python `-I -S -B`, and repeat with `-O`.

`verify_corpus.py CATALOG_JSON PROBLEMS_JSON RESEARCH_RESULTS_JSON` can reproduce complete corpus and complete-pair checks when the authorized local inputs are available. It prints metadata only. Public reproduction does not require redistribution of those inputs.

`independent_math.py` runs finite diagnostic checks of the elementary identities. Its success does not prove the general harmonic-measure theorem. The actual reasoning, source inputs, and limits are explicit in the mathematical audit.

Retain the original author artifacts and this audit as distinct immutable records. No corrected freeze is necessary and no publication was performed by this audit.

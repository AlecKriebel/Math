# Reproducing the five-turn packet

The original question remains unsolved. Start with RESULT.md, SOURCE_SCOPE.md and FINAL_REVIEW_REQUEST.md. The final authoritative state is CURRENT_STATE_T5.json; earlier CURRENT_STATE files are immutable historical snapshots.

Using Python 3 with only the standard library, run from this directory:

    python replay_author.py

It runs all five verify_turnN.py files and compares stdout byte-for-byte with TURN_N_CHECKS.json, then validates all historical checkpoint entries. The output matches AUTHOR_REPLAY.json. This works after relocating the directory.

To check the final packet binding separately:

    python -c "import json,hashlib,pathlib; p=pathlib.Path('.'); m=json.loads((p/'FINAL_AUTHOR_MANIFEST.json').read_text()); [(_ for _ in ()).throw(AssertionError(x['path'])) for x in m['files'] if len((p/x['path']).read_bytes())!=x['bytes'] or hashlib.sha256((p/x['path']).read_bytes()).hexdigest()!=x['sha256']]; print(len(m['files']), 'files verified')"

The final manifest excludes itself and includes every other public file. No raw problem import, source PDF, private coordination record or receipt for a remote operation is part of the public author packet. Source URLs, edition dates and locally checked PDF hashes are in SOURCE_SCOPE.md, SOURCE_MANIFEST.json and SOURCE_ADDITION_T3.json. Finite controls are supporting evidence; the analytic and representation-theoretic claims require the full written proofs and credited inputs.

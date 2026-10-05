# Independent audit supplement

Read `AUDIT.md` for the verdict and `CORRECTIONS.md` for downstream wording constraints.
`AUDIT_BINDING.json` identifies the unchanged frozen packet.

Python 3.10 or later, standard library only:

    python verify_binding.py /path/to/rank666-30001138-authored-packet.zip
    python independent_verify.py /path/to/extracted/packet > new_results.json

Compare parsed `new_results.json` with `independent_results.json`.
`author_replay.json` is the separately replayed author-verifier result.
`SOURCE_AUDIT.json` contains fresh public-source hashes, sizes, status, and inspection history.
`AUDIT_MANIFEST.json` covers every other file in this supplement.

The frozen author packet is required as input but is not duplicated here. This archive includes no source PDFs, source text, datasets, downloaded webpages, or coordination files. It certifies the listed exclusions and audit checks, not a full solution or global open status.

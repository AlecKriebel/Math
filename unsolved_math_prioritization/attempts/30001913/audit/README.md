# Independent acceptance of problem 30001913

Accepted as a scoped partial-results packet. The full conjecture is unresolved by these five approaches. No author correction was required; no novelty or formal-verification claim is made. AI-assisted and unrefereed.

- AUDIT.md: complete mathematical and source-scope review.
- ACCEPTANCE.json: machine-readable audit decision.
- SOURCE_VERIFICATION.json: public hashes, byte counts, citations, inspection history and limitations only.
- REPLAY.json: 54 independent isolated normal/optimized acceptance and mutation tests.
- INDEPENDENT_MATH.json: 13,617 supplementary exact controls, normal/optimized identical.
- replay_audit.py and independent_math.py: independently authored replay code.
- author/: byte-identical copies of the original safe archive, external manifest and freeze receipt.

After independently validating this audit archive and its external manifest, use Python 3.11+:

    python -I -S replay_audit.py author/HODGE_EXTREMALITY_30001913_AUTHOR_SAFE_FREEZE.zip author/HODGE_EXTREMALITY_30001913_AUTHOR_EXTERNAL_MANIFEST.json author/HODGE_EXTREMALITY_30001913_AUTHOR_FREEZE_RECEIPT.json
    python -I -S independent_math.py

Repeat each command with -O. The replay script creates only disposable temporary trees; it does not rewrite the author inputs. Do not treat editable manifests or an unpinned script as their own trust authority.

No source PDF/text, corpus contents, private research records, private coordination, or publication credentials are included. This packet has not been published by the auditor.

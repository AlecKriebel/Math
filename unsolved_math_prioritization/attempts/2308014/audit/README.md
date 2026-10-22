# Independent acceptance packet: positive Hankel symbols

Read `ACCEPTANCE.md` for the decision and `MATHEMATICAL_AUDIT.md` for its analytic basis.

The original author files in `author/` are preserved exactly. `provenance/` contains the exact safe author ZIP and its external manifest, so the independent replay is self-contained. The original author's pending-review status is historical; the later audited disposition is in `audit/STATUS.json`.

After safely extracting this audit ZIP, from its root run:

    python3 -I -B audit/verify_author_freeze.py provenance/POSITIVE_HANKEL_2308014_AUTHOR_SAFE_FREEZE.zip provenance/POSITIVE_HANKEL_2308014_AUTHOR_EXTERNAL_MANIFEST.json

This validates the author's external trust anchors before extracting and executing it, then reruns normal/relocated finite checks and adversarial controls. The audit ZIP itself must first be checked against its separate external manifest or the supplied pinned bootstrap. An edited checker certifying itself is not a trust anchor.

Expected outcome: 1,948 finite exact sanity checks pass; optimized author execution is explicitly rejected under -O and -OO; envelope/member tampering is rejected; isolated shadow-import and no-bytecode controls pass. No automated proof of the infinite theorem is claimed.

Only authored proof/audit files and public verification metadata are packaged. Raw datasets, inherited reports, source PDFs, source extracts, source images, and private coordination are excluded. No publication, queue edit, or external outreach was performed.

# RBM(4,3): credited prior obstruction

Problem 20002559 / AIM-PROBABILITY-0001, rank 763. Disposition: **already_solved**,
one substantive approach out of five. The prior negative closure result was
independently reconstructed and audited. No new mathematical discovery is claimed.

Credit: **Anonymous, An eight-point obstruction to universality of RBM(4,3),
v0.2.0-candidate, 6 September 2026**. The source remains an **unrefereed,
AI-assisted candidate**. Ian Pitchford / Evidence Press is the public operator
and publisher, with OpenAI Codex assistance disclosed. No journal acceptance,
human specialist endorsement, formal verification or historical priority is claimed.

The [public GitHub release](https://github.com/ipitchford/rbm43-eight-point-obstruction/releases/tag/v0.2.0-candidate)
and pinned commit fac57cd9a497a509d443f34f9b9843f6c7a7042f were verified.
The source lists DOI 10.5281/zenodo.22550044; the DOI landing/deposit was not
independently opened. Main proof inspection used the verified Markdown, not a PDF.

## Result and limits

The classical real binary RBM with four visible and three hidden units does not
approximate every law on the sixteen visible states. An exact product-identity
leakage inequality extends by continuity to the entire Euclidean visible closure,
including arbitrary escaping parameter sequences. A strictly positive target
also violates it. All 16,777,216 unrestricted selectors are covered. The fresh
audit uses independent Shannon-complement and interleaved truth-matrix algorithms.
The existing six-hidden-unit upper bound gives 4 <= m_min <= 6. The exact minimum
and sharp approximation radius remain unsettled here.

Read author/REPORT.md for the reconstruction and audit/AUDIT_REPORT.md for the
independent mathematical challenge. Both frozen packets are unchanged. Historical
author wording that says the audit is pending describes the pre-audit freeze;
audit/VERDICT.json records the subsequently completed PASS. The review was by a
fresh assistant worker, not an unaffiliated human or a formal proof assistant.

## Reproduction: two distinct levels

Python 3.10+ and the standard library suffice. Obtain the expected SHA-256 of
PUBLICATION_MANIFEST.json from the PR description or another trusted channel;
do not derive your trust anchor from an untrusted copy of the package itself.

Portable integrity and exact positive-target/local-chart checks:

    python3 -I -B verify_publication.py . EXPECTED_MANIFEST_SHA256
    python3 -I -B -O verify_publication.py . EXPECTED_MANIFEST_SHA256

This checks every packaged byte, the frozen inner manifests, scope, and a few
source-free calculations. It explicitly reports full certificate replay NOT_RUN.
It does not establish the full mathematical result without external input.

Full finite-certificate replay requires external appendix.md and certificate.json
from the pinned public commit. Keep those files outside this directory:

    python3 -I -B verify_publication.py . EXPECTED_MANIFEST_SHA256 --full --sources /path/to/external-source-directory
    python3 -I -B -O verify_publication.py . EXPECTED_MANIFEST_SHA256 --full --sources /path/to/external-source-directory

Both external files are hash- and size-checked before any checker executes. The
author reconstruction, eight adversarial controls, and fresh independent audit
are replayed and compared to the saved receipts. Missing inputs return NOT_RUN
with exit status 2; changed inputs fail. No producer code is executed or imported.

The separate audit/README.md gives auxiliary parity-control and complete corpus
correspondence commands. These need additional external public files and the
original author freeze; those extra checks are not silently folded into the
portable or finite-certificate replay status. Their saved receipts are frozen.

For package-integrity negative controls, including omitted/tampered manifests,
changed prose/code, unexpected source data, symlinks, changed queue fields and
missing/tampered external input:

    python3 -I -B test_publication.py . EXPECTED_MANIFEST_SHA256
    python3 -I -B -O test_publication.py . EXPECTED_MANIFEST_SHA256

An optional --queue /path/to/QUEUE.md verifies the exact three-cell patch,
restoring the old row in memory to prove that all other bytes, including Chat,
DOI and the stale header, are unchanged. No queue regeneration is performed.

## Publication boundary

This folder contains original reconstruction/audit prose and code, verification
receipts and public verification metadata. It excludes original proof/appendix
text, certificate contents, source PDFs, raw datasets and private coordination.
PUBLICATION_MANIFEST.json inventories the complete folder except itself.
No GitHub release, merge or external outreach is part of this draft publication.

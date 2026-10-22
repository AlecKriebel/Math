# Attributed interior contact-arc proof note

This package proves an interior second-order Taylor defect for the particular smooth strictly positive Ross–Witt Nyström contact-arc example. The five-page note states all imported construction/duality contracts and supplies the Green slope/curvature/Legendre deduction. No numerical PDE solve or closed-form potential is claimed.

The earlier OWR2021 joint-work contribution already announces/sketches an interior construction. All prior machinery is credited. Historical priority, first discovery, independent discovery and current worldwide openness are unestablished. The current note is a proof/application contribution. The supplement records18 source/list entries and64 discovery queries with explicit full/partial inspection scope, versions, hashes and gaps. Search absence is not proof of literature absence.

## Reproduce the scalar checks

Extract verification-package.zip into a fresh directory, then run Python3.11 or later from that directory:

    python3 -E -S -B -P verify_package.py

Only the Python standard library is required. The verifier checks every archive file against ARCHIVE_INVENTORY.json and replays the independent exact rational scalar certificate both normally and under optimization, plus the legacy81-case/486-assertion control normally. It writes only to stdout. Explicit exceptions protect the wrapper and new scalar checker under optimization. The legacy checker uses assertions, so it is deliberately launched without -O; its printed count alone under -O is not evidence of executed checks.

Computation verifies scalar normal-form algebra/support signs, not the Hele-Shaw geometry, elliptic dependence or weak PDE. Read the analytic proof and dependency reports for those inputs. Independent AI checks do not constitute human peer review.

## Contents and provenance

The archive includes the paper, source, authored source/geometry/Legendre/priority audits, Root mathematical and qualified-priority gates, original19 submitted artifacts and their custody record, scalar scripts/certificates, metadata and inventory. Historical original artifacts are immutable records: their imported open-status language is corrected by the current note, CLAIM_SCOPE.json and priority gate. Original effort remains4 recovered substantive author turns plus unknown/nonzero interrupted history; audits are separate work.

Copyrighted third-party PDFs, extracted texts, screenshots, raw web outputs, credentials, caches and upload state are excluded. SOURCE_REFERENCES.json and audit source-access records identify the inspected copies; relative private-copy paths are historical inspection locations, not promised archive members. Whole-package publication reviews and actual later deposit/integration receipts are recorded separately in the repository, avoiding circular inclusion of reviews that bind this archive.

The top-level zenodo-deposit.json is the exact intended metadata and three-file upload manifest for the repository kit. It does not assert that uploading has occurred. All authored materials are supplied under CC BY4.0. AI tools were used extensively. This is an unrefereed preprint without conventional human peer review.

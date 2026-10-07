# Exact production payload and review record

The production manifest is ../zenodo-deposit.json. The intended four downloadable files are zenodo-upload-kit/paper.pdf, height-repair.pdf, source.zip, and verification.zip. The outer directory is an upload kit, not a single archive to substitute for those payload files.

The archives contain only owned source, derivations, verification code, metadata and references. No secrets, caches or third-party manuscript bodies are included. Extract both archives into one fresh directory; standalone TeX sources need no bibliography file. See reproducibility/README.md for clean build and finite checks.

CANDIDATE_INVENTORY.json identifies the exact payload bytes and archive-member hashes. Complete-package review reports and operational receipts are retained outside the archives. Gate completion and the eventual public DOI/tracker range are recorded in ../PUBLICATION_STATUS.json. Historical scoped reports preserve their original audit checkpoints; the completed integration audit and candidate ledger distinguish resolved interfaces from earlier open assessments.

Do not create a GitHub release or a second deposit to repair a resolver delay or tracker failure. Use the documented repository Zenodo tool and reconcile the same deposit state after an ambiguous response.

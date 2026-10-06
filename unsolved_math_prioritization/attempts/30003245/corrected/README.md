# Corrected author-safe review package: 30003245

Read MATHEMATICAL_REPORT.md first, followed by STATUS.json and APPROACH_LEDGER.json. The full problem remains unresolved by this work. Partial proofs use classical methods; no novelty is claimed.

SOURCE_METADATA.json records primary-source access, public status, locators, and limits. PRIOR_ATTEMPT_GATE.json binds the complete inherited inputs by hashes without including their contents.

verify_arithmetic.py is an import-free supplementary checker. Review it as text before running. Its author execution used `python -I -S verify_arithmetic.py`; ARITHMETIC_RESULT.json records that run. It checks finite integer identities and conductor-bound samples, not the entire proof. No dependencies or source documents are required to run it.

The corrected verifier uses explicit fail-closed checks, preserved under Python -O. Independent replay and negative controls are recorded in the separately pinned audit package. This derivative preserves the original mathematical conclusion.

An external manifest binds every archived member and the ZIP itself. The archive contains authored report/status/audit material only: no copied source texts, PDFs, images, raw datasets, secrets, or private coordination. No publication was performed.

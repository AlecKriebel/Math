# Reproducibility and scope

The original author scripts and the independent replay used Python assert statements. Packaging replaces each assert with an explicit require(condition, reason) that raises RuntimeError, preserving the mathematical condition and surrounding calculations. GUARD_NORMALIZATION.patch records all script changes, and PROVENANCE.json records original and packaged hashes. This ensures checks survive python -O. No certificate or mathematical claim was changed by this normalization.

Authored reports were sanitized to remove local workspace references, internal coordination language, and an uninspected search hit. Remaining source access statements distinguish preview inspection from full-PDF access. Audited original report hashes remain in AUDIT.md as historical evidence, not as packaged-file hashes. PROVENANCE.json links the versions.

The three replay transcripts record complete stdout. replay.json is the earlier certificate-only structured audit output; replay.txt and current replay.py additionally cover all-k samples. Fresh package replay compares complete output for all scripts under normal Python and python -O. Mutation controls deliberately alter the dual matrix, author separating matrix, positive factor coefficients, and all-k family parameter. Each must fail in the mathematical certificate validator, not merely the integrity gate. Separate controls detect missing, unexpected and altered files, corrupted manifest hash/total, duplicate entries, and path traversal.

No source or dataset download is required for replay. Public corpus hashes describe local recovered copies, not a new upstream fetch. Exact rational finite computations complement, but do not prove alone, the uniform family, full-spark and rank-two classification theorems.

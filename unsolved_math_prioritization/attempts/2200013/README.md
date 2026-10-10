# Binomial-weighted tropical corners: a literature-derived negative resolution

Rank 1031; problem 2200013 / AMR-021-0013; Shapiro's Conjecture 8.

The explicit rational polynomial has actual degree **200000000000000000100**, strictly positive coefficients at every index, at least **four distinct negative roots**, and exactly **three distinct corners** of `max_i(log(a_i binom(N,i)) + i t)`. Each corner has two maximizing terms. The conventional slope-jump multiplicities are K, 100, K and sum to N; they are not the target count.

Start with [the accepted, unchanged proof](audit_reproducibility/corrected/public/PROOF.md), then [the scope audit](audit_scope/AUDIT.md) and [the independent mathematical/reproducibility audit](audit_reproducibility/AUDIT.md). [ACCEPTANCE.md](ACCEPTANCE.md) states the release decision and limits.

This is a reconstruction of the small-curvature obstruction in Forsgård–Novikov–Shapiro, [arXiv:1510.03257v1, Theorem 11](https://arxiv.org/abs/1510.03257v1), specialized to the binomial weights. The explicit finite witness removes the unspecified constant and establishes full support. The target is [Shapiro 2015, Section VII](https://arxiv.org/abs/1503.05295v1). [Katkova–Shapiro–Vishnyakova 2024, Section 5](https://arxiv.org/abs/2403.12200v1) repeats the target as Conjecture 1 and disproves its Conjectures 2 and 3. That later status discrepancy is disclosed but its historical cause is not explained. No novelty, priority, minimum degree, or exact total root-count claim is made.

## Layout and historical status

- `audit_reproducibility/corrected/` is the authoritative release slice.
- `audit_scope/` preserves the full first audit and its manifest. It was mathematical/source review; it did not run packet tests.
- `audit_reproducibility/` preserves all 21 allowlisted second-audit files, including 687 passing independent controls, 229 per mode and 78 overflow rejections.
- `original/` contains exactly nine original replay files for the old/new parser contrast. The original certificate is mathematically valid; the original standalone parser is intentionally retained as historical test input, not as the recommended interface.
- `historical/ORIGINAL_CONTROL_REPORT.json` preserves the author's earlier 93-control receipt, separate from the independent audit.
- [PARSER_HARDENING.patch](audit_reproducibility/PARSER_HARDENING.patch) is the actual code difference. Only verify_math.py changes in the seven-file public slice. Proof and certificate bytes are unchanged.
- Frozen RESULT.json still says the independent audit was pending at authoring time. The later full audits and acceptance supersede that historical status without rewriting it.

## Pinned source-free replay

Python 3.12+, standard library, and UID/EUID 1000. Obtain **both** the wrapper SHA-256 and PUBLIC_MANIFEST.json SHA-256 independently from the exact-commit PR receipt. Verify the wrapper bytes before executing any packet code. A packet and digest supplied together by an untrusted party do not authenticate one another.

    python -I -B verify_publication.py --root PACKET_DIRECTORY --manifest-sha256 INDEPENDENTLY_OBTAINED_MANIFEST_SHA256

Repeat with `-O` and `-OO`. The wrapper checks exact files and directories, byte sizes, SHA-256 values, duplicate keys, finite JSON numbers including overflow, exact integer count fields, both nested manifests, both audits' external pins, proof preservation, and the actual pure-code patch. It runs both frozen bootstraps and the independent integer reconstruction. It reruns all 687 adversarial audit controls and reseals only disposable copies. Real nonroot write-denial, read-only hostile relocation, corrupted arithmetic, integrity tampering, and old/new parser controls are part of those runs. The packet remains read-only.

The mathematical controls use exact finite integers and fractions with symbolic enormous-degree bounds. They never expand the degree-N polynomial or form the denominator of delta. These tests are not a proof-assistant kernel. They assume a trusted interpreter/standard library and stable files, not a concurrently malicious filesystem administrator.

Fresh source retrieval, corpus retrieval, proof-assistant certification, and CI are `NOT_RUN` in default replay. Frozen source metadata describes prior inspection and local byte checks; it is not a fresh network retrieval claim. No source PDFs/text, dataset contents, private sources, personal data, or private coordination files are in this packet.

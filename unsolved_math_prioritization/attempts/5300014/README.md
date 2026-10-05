# Blaschke compactification comparison: audited scoped partial results

Problem **5300014 / AMR-052-0014**, queue rank 794. **UNSOLVED after 5/5 approach families.** No genuinely nonmonomial base in degree greater than two has a proved boundary nonextension witness in this packet. The target is the extension of the common-interior identification between geometric mating closures, not an arbitrary abstract boundary homeomorphism.

## Read the governing corrections first

[CORRECTIONS.md](CORRECTIONS.md) and the [complete independent audit](independent_audit/AUDIT_REPORT.md) govern interpretation of the immutable author snapshot. [ATTEMPTS_AUDITED.json](independent_audit/ATTEMPTS_AUDITED.json) is the operative, percentage-free status record.

- **C1:** The historical completion estimates in the frozen author record are withdrawn. They are unsupported subjective heuristics and must not be treated as proof progress, probability of success, or literature status. No completion percentage is endorsed or summarized here.
- **C2:** The double-hole family's free zeros are n−3 copies of 0, −r, and −s. The leading factor z is separate. The displayed derivative and radial-rate identity were already correct.
- **C3:** The quadratic statement uses an explicit coefficient gauge and basin labels. The third fixed-point marking is allowed to collide with 0 when beta=1; it is not a three-distinct-marked-points chart.
- **C4:** Cao–Wang–Yin's theorem is imported from the inspected arXiv v1. The journal PDF was not retrieved or compared. The closed-graph equivalence is conditional on its compact metrizable Hausdorff hypotheses and compatible normalization; no universal compactness or quotient-descent theorem is supplied.

## Accepted scope and remaining gap

The packet provides the quadratic coefficient-chart extension, all-base Fourier/Newton witnesses, inverse-circle-conjugacy absolute-continuity rigidity, an exact algebraic double-hole rate, and a simultaneous-graph criterion. The polynomial-side nonsingleton impression uses an explicitly attributed external theorem.

Inverse-circle-conjugacy rigidity is dynamical information and does not establish parameter-boundary nonextension. The double-hole limit is a coefficient pair with holes, not a genuine degree-n geometric rational limit. The explicit radial paths are not proved to realize distinct polynomial impressions. There is no simultaneous boundary obstruction for any required higher-degree nonmonomial base, much less every such base. The original target remains unsolved. Finite controls do not certify the analytic proofs or imported theorem. No novelty, conventional human peer review, or machine-proof certification is claimed.

## Immutable inputs and layout

- `independent_audit/`: exact extraction of the accepted audit archive, including the original author files and nested author ZIP
- `archives/`: both original author and audit ZIPs, byte-for-byte preserved
- `CORRECTIONS.md`: prominent exact copy of the audit's governing clarifications
- `PUBLICATION_STATUS.json`: disposition and archive/manifest identities
- `PUBLICATION_MANIFEST.json`: complete publication payload allowlist, byte counts, and SHA-256 hashes
- `verify_publication.py`: externally pinned recursive integrity and replay verifier
- `test_publication_integrity.py`: disposable negative controls and relocated positive checks

The archived audit and author statements about publication being pending or no remote writes describe their frozen historical checkpoints. This wrapper records their subsequent draft-PR publication; it does not silently alter those checkpoints.

Author ZIP: 21,759 bytes; SHA-256 `3652ecfb4a18b4acabb62df193d7f84f556eecf53cc6fb0d03534be704a30d6e`.

Audit ZIP: 64,421 bytes; SHA-256 `16578dd5087fd61a7c2d39d0df597b02553031a779a6e18e52e0a788bfb0fd17`.

Audit manifest SHA-256: `b5eb408734800ba3040933c7f9576d00dc0bdddd56b96557c9480daab1ce2c1c`.

## Reproduce

Python 3.10 or newer; standard library only. From any working directory:

    python -B /path/to/verify_publication.py --expected-manifest EXTERNALLY_SUPPLIED_PUBLICATION_MANIFEST_SHA256
    python -B /path/to/test_publication_integrity.py --expected-manifest EXTERNALLY_SUPPLIED_PUBLICATION_MANIFEST_SHA256

Use the publication manifest hash recorded separately in the draft PR. Hashing an untrusted manifest itself does not establish a trust anchor. The verifier checks the exact file and directory inventory, all file bytes, both ZIPs, their exact extracted payloads, immutable author copies, operative unsolved status, and author/independent exact mathematical controls under normal Python, -O, and -OO. All integrity conditions use explicit exceptions and remain active when Python assertions are disabled.

Optional source replay requires separately obtained public corpora and PDFs as described in the author README. Only public verification metadata is included here. Scholarly PDFs, extracted source text, images, raw datasets, and private coordination files are excluded.

The sole existing-repository edit changes this target's queue Status to `unsolved` and Turns to `5/5`. All other queue bytes, including its pre-existing header, remain unchanged. This is one draft PR; no merge, release, DOI, or external outreach is part of the publication.

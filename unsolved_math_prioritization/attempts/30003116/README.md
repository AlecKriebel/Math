# Rational multiplicative orbit entropy: audited partial progress

**30003116 / OWR-14603-015, rank 993. Status: unsolved, 5/5.**

The intended sufficiently-large-denominator entropy question remains unresolved. Accepted partial results include uniform logarithmic-time covering at least c sqrt(log log s) at scale (log s)^(-4), and covering at least c(log p)^(3/2) at scale (log p)^(-6) for all but at most (p-1)/sqrt(log p) nonzero numerators when p is prime. The former has a weaker scale of entropy growth; the latter does not control every numerator or composite denominators. Power-small forward seeds, power-close pairs and coarse empirical entropy remain unproved universal hypotheses. The a=4,b=7,s=3 fixed point refutes only an unqualified all-denominators reading.

Read the five proof files in `corrected/`, the complete independent review in `independent_audit/FULL_AUDIT.md`, and `PUBLICATION_ACCEPTANCE.md`. The untouched original and untouched audit each retain their original externally pinned manifest. The corrected slice applies exactly the required nonempty-U clarification and, separately, optional schema/diagnostic hardening, with a new manifest. No other original content changes. Historical README statements about publication and review describe their original snapshot, not this later package.

## Credits and limits

The source is Elon Lindenstrauss, *Around Furstenberg's ×2 ×3 theorem*, Question 2, [OWR 21/2016](https://doi.org/10.4171/OWR/2016/21), printed pp.1127–1128. The fixed-base logarithmic-form input is credited to Baker–Wüstholz through [BLMV, Theorem 4.3](https://math.huji.ac.il/~elon/Publications/Effective_Furst.pdf). BLMV's Theorem 1.10 already establishes logarithmic-time rational-orbit density at a triple-log scale. This prior work is not claimed as new. The source's printed Baker-case inequality is anomalous under changes of numerator representative; no unstated repair of the author's intent is assumed.

This is extensively AI-assisted, unrefereed work with an independent AI audit. No human peer review, formal proof verification, novelty, exhaustive search, or current global openness certification is claimed. Written mathematical arguments carry the universal claims; finite diagnostics cannot establish them. No PDFs, source extracts, page images, corpus contents, private coordination files, or private personal data are redistributed. Public titles, URLs, sizes, hashes and historical inspection metadata are preserved. Source bytes are absent, so source-free replay does not freshly inspect or authenticate them.

## Two separate external trust anchors

Obtain both the SHA-256 of `VERIFY_PUBLICATION.py` and the SHA-256 of `PUBLICATION_MANIFEST.json` from an independently trusted record such as the reviewed commit/PR. First authenticate the wrapper using a trusted external hashing tool; do not execute a replacement wrapper simply because its own manifest was rewritten. Then run:

    python -I -B VERIFY_PUBLICATION.py --expected-manifest TRUSTED_MANIFEST_SHA256
    python -I -B -O VERIFY_PUBLICATION.py --expected-manifest TRUSTED_MANIFEST_SHA256
    python -I -B -OO VERIFY_PUBLICATION.py --expected-manifest TRUSTED_MANIFEST_SHA256

Each invocation runs full baseline and independently re-pinned read-only finite replays in all three optimization modes. The wrapper enforces exact regular-file and directory sets, strict schemas and integer types, no duplicate JSON keys/nonfinite JSON, no symlinks/special files, baseline modes, exact sizes/hashes and both preserved patches with exact hunk context/offsets. The original mathematical checker produces 86,778 finite checks; the independent checker produces 38,715. Full replay compares complete historical negative-control results, including 174 independent packet cases.

For actual outer-packet mutations and authenticated-bootstrap rejection tests:

    python -I -B TEST_MUTATIONS.py --packet . --expected-manifest TRUSTED_MANIFEST_SHA256 --expected-wrapper TRUSTED_WRAPPER_SHA256

## File modes and read-only relocation

Original and audit manifests bind baseline files to 0644. Those manifests and their pins are preserved, with 0755 directories. A physically read-only relocation uses 0444 files and 0555 directories without changing any bytes; explicitly select `--filesystem-profile readonly` for the publication wrapper. The outer validator recognizes this declared projection rather than silently dropping mode checks.

The historical native verifiers cannot accept 0444 files under their original 0644 manifests. Full replay therefore stages exact disposable baseline copies at 0644, and additionally creates separate 0444 native-verifier fixtures whose manifests rebind only member modes and receive new external pins. Receipts explicitly identify those fixture pins, prove attempted writes fail, and check pre/post identities. A read-only fixture pin must never be described as the unchanged original anchor.

# Independent audit package

Read AUDIT.md for the verdict and reasoning. The result is PASS for the stated partial results and honest unresolved status; it is not a solution of the general odd-characteristic problem or human peer review.

BINDING.json identifies the exact 13-file author archive. CORRECTIONS.json records that no required correction was found. SOURCE_VERIFICATION.json contains public source retrieval and inspection metadata only. REPLAY_RESULTS.json records the frozen author replay.

Reproduce with Python 3.12 and SymPy 1.14.0. Supply the separately preserved author's EXACT_RESULTS.json:

    python independent_checks.py --author-results ../author/packet/EXACT_RESULTS.json > independent-replay.json
    cmp INDEPENDENT_RESULTS.json independent-replay.json
    python certificate_checks.py ../author/packet/EXACT_RESULTS.json > certificate-replay.json
    cmp CERTIFICATE_RESULTS.json certificate-replay.json

The first script uses full unpruned iterates and shares SymPy as a factorization dependency with the author. The second is pure Python and imports no author code or algebra library. It uses independently implemented descending-coefficient arithmetic to check all saved stable-factor certificates.

The package contains authored audit material, generated verification results and public-source metadata. It contains no source PDFs, extracted primary-source text, original catalogue contents, private coordination material or remote-write receipts.

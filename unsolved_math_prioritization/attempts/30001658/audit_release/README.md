# Independent audit of problem 30001658

Verdict: **PASS WITH A NONBLOCKING DOMAIN CLARIFICATION**, scoped to an unresolved five-approach research packet. The unrestricted all-dimension inequality remains unproved here. No historical-novelty or global-open-status claim is made.

- `AUDIT.md`: full source, analytic, computation and scope review
- `VERDICT.json`: machine-readable verdict and controlling endpoint qualification
- `INPUT_BINDING.json`: independent nine-file author-input binding
- `SOURCE_AUDIT.json`: public source hashes, retrieval/inspection history and limits
- `independent_checks.py` / `INDEPENDENT_RESULTS.json`: independent exact certificate
- `audit_replay.py` / `REPLAY_RESULTS.json`: normal and optimized replays, with filesystem rejection tests
- `verify_audit.py` / `MANIFEST.json`: strict audit inventory and reproducible verification

Run from any directory:

`python3 -B verify_audit.py --source-dir PATH_TO_FROZEN_AUTHOR_RELEASE --expected-audit-manifest-sha256 EXTERNALLY_SUPPLIED_HASH`

The author packet's manifest is pinned internally to `68a1fa6b5900a7cc03cd2d991e1a135afb2366a169b680ad5ac9db335203ed68`. The audit manifest should also be externally pinned. Source PDFs are not required for replay and are not included.

The recommended wording clarification restricts the largest-coefficient quotient in author PROOF.md §3 to proper coordinate subcubes, k>=1. All retained inequalities and source-case distinctions pass; the frozen author files remain unchanged.

The independent certificate uses matrix inversion, Gray-code traversal, antichain enumeration and integer-power logarithm bounds. It passes 1,282,085 exact checks. These computations supplement the written review; they do not solve the unrestricted conjecture or constitute human peer review.

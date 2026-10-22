# Strong quantization for the fourth-order Navier equation

Problem 30000801 / OWR-1591-003. Research date: 2026-10-06 (UTC).

**Verdict: PARTIAL ONLY; the full problem is not solved.**

This package contains an authored local Pohozaev identity and a conditional
single-bubble criterion. The additional weighted-tightness, positive finite
height-ratio, and exterior-profile assumptions are not consequences established
here of the original hypotheses. No novelty claim is made for these standard
identities or their conditional consequence.

Read `PROOF.md` for the analytic proof and exact remaining gap, `SOURCE_AUDIT.md`
for the scope of the primary literature, and `APPROACHES.md` for five bounded
mathematical approaches. The code verifies exact identities and finite controls;
it is not a PDE existence argument or a proof of strong quantization.

## Reproduce

Python 3 with SymPy 1.14.0 is required. From this directory:

    python verify.py
    python -O verify.py
    python test_fail_closed.py

The verifier is location-independent. All ordinary assertions use explicit
exceptions, including under optimized Python. Missing, modified, extra, or
symlinked payload files fail integrity validation. The manifest is an integrity
inventory, not a cryptographic signature; the enclosing ZIP hash supplies the
external freeze identity. The tests also reseal mathematical metadata mutations
to check semantic rejection independently of file hashes.

`PUBLIC_METADATA.json` contains only public citation/retrieval metadata and
source/corpus hashes, sizes, and match results. No third-party PDF, extracted
source text, dataset row, dataset contents, or private coordination is included.

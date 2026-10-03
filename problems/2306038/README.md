# Function Theory 6.38: reviewed historical resolution

The affirmative weighted-square-summability result is due to V. I. Milin (1981), Theorem 2 and Corollary 1. It holds for every positive exponent. This package makes no new-resolution or priority claim.

The [proof and source gate](artifacts/README.md) are preserved exactly as reviewed. The [independent AI-assisted audit](audit/INDEPENDENT_AUDIT.md) passed without mathematical corrections. The audit supersedes the frozen artifacts' pending-review status; their bytes and checksum manifest remain unchanged. This does not constitute human peer review or formal verification.

Reproduce from this directory:

```
(cd artifacts && sha256sum -c SHA256SUMS && python3 verify.py | cmp - verification.json)
(cd audit && sha256sum -c SHA256SUMS && python3 replay.py | cmp - replay.json)
```

The 2018 collection's citation to I. M. Milin (1968) is distinguished from the unrestricted 1981 result. Complete relevant primary proofs were read; source PDFs, scans and full extracted texts are excluded from this repository package.

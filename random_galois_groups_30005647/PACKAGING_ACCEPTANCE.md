# Packaging acceptance report

Status: UNSOLVED; five approaches; no novelty claim. This is a packaging check, not an additional proof audit.

Accepted mathematical inputs were checked against their frozen SHA-256 hashes before copying. The research, source-priority audit, independent audit and expected exact output were copied unchanged. The source gate header omits its recovery-corpus key. Public source metadata includes only downloaded public PDF hashes, sizes and public URLs, with inspection history; copied sources and local-extraction fingerprints are excluded.

The exact checker was converted from three Python assert statements to explicit failure guards. Reverse-transforming those guards restored the entire original AST, including condition expressions and control-flow placement. AssertionError remains the failure type, but the message is now explicit; optimized Python intentionally retains checks.

The test suite passed byte-for-byte output replay in normal and -O modes, and rejected three real mathematical mutations in both modes: erroneous square-count denominator, reversed parity equality, and omitted composition sign. The manifest suite passed its valid baseline and rejected missing, same-size changed, extra, nested-manifest, symlink, manifest-symlink, empty-directory, duplicate-record and unsafe-path changes in both modes. Only the root MANIFEST.json is exempt from the exact file inventory. These checks do not prove general mathematics or the unresolved asymptotic.

The existing independent audit explicitly retains the limitation that exact Wiley acceptance/publication dates were not independently reproduced. Its acceptance is a scoped mathematical audit, not exhaustive source verification.

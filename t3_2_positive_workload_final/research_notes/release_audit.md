# Release audit of the inherited candidate

## Reproduction

- Available outer archive SHA-256:
  `1414312696f80850557676e53d5dfc1b59be26bf0f0906ff87b51e0a7633f568`.
- Internal manifest: pass.
- Python 3.11 replay: all 12 supplied tests and all three atlas paths pass.
- Generated JSON reports are byte-stable under that replay.
- The existing 11-page PDF has embedded fonts and no observed clipping,
  overlap, or broken glyphs.

## Blocking defects

1. The finite verifier itself identifies terminal localization, source-layer
   induction, one-active closure, and global return as noncomputational
   load-bearing claims, while the public status surfaces label the full
   theorem certified.
2. The clean-extraction report contains stale hashes for both generated JSON
   reports. The actual hashes agree with the manifest and gate JSON, not the
   clean-extraction prose.
3. The available outer archive hash differs from the previously reported
   hash and has no commit/tag provenance.
4. The scripts are non-hermetic and mutating: an ambiguous Python executable,
   undocumented Python/TeX/compiler requirements, fixed shared temporary
   names, certificate/PDF rewrites, optional input skips, assertions used as
   verification, and no subprocess timeouts.
5. Historical material dominates the proposed release and includes mutually
   inconsistent certification statements.
6. License, citation metadata, repository/version locator, code-availability
   statement, precise classwise scope definitions, and PDF metadata are
   missing.

The top-level read-only verifier deliberately covers only the new generic
regressions and the finite algebra supporting the exact-seam repair. A theorem
release must be rebuilt as separate minimal arXiv and code archives after the
mathematics closes.

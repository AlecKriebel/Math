# Changes after independent review

The frozen original is preserved byte for byte in frozen_original/, with author-manifest SHA-256 9e0722156cc50db5ed6e178b424c270c644ad3d898e182da7c548ee478054529. The full independent report and status are retained in audit/. Its report SHA-256 is df0db89b77353ac68fa5cbaa7bdfe1597d934cff3037cd6a8de6aa3b5f25a9f7.

## Mathematical wording correction

In turn_03.md, the sentence saying that a finite abelian H has limit 1 now specifies nontrivial H; H=1 has limit 0. The nonzero-kernel G formula remains max_i |H/K_i|, giving 1 when H=1. This is precisely the minor issue noted in the audit, with no new author attempt or claim.

## Presentation and verification

README.md now reports the completed scoped review and explains the release layout. status.json records that review and the minor correction. The standalone verification script checks every release hash, every original author hash, the exact one-sentence proof change, unchanged other proofs, and both exact computations. The original root author manifest is retained only at frozen_original/AUTHOR_MANIFEST.json to avoid presenting it as a hash manifest for corrected release files.

All other original proof and check files are unchanged. Source PDFs, extracted primary texts, screenshots, catalogue imports, and private preparation records are excluded. The universal problem remains **unsolved, 5/5**.

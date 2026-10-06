# Independent acceptance packet for fractional infinity eigenfunctions

The representation counterexample is accepted. The general finite-p selection
question remains unresolved by this work, so problem 30002288 remains PARTIAL.
Read MATHEMATICAL_AUDIT.md for the complete independent reasoning and
ACCEPTANCE.md for the accepted artifact pins and scope.

The exact patch only clarifies the source's admissible C_0^1 viscosity tests.
PATCH_METADATA.json records the original and corrected proof hashes.
VISCOSITY_TEST_CLASS.patch was applied with zero fuzz to a fresh original copy.
No source documents, excerpts, corpus contents or private coordination material
are contained in this packet. SOURCE_VERIFICATION.json and
CORPUS_VERIFICATION.json contain public verification metadata only.

## Replay the independent diagnostic

Read the code before execution. With the separately supplied pinned bootstrap,
external manifest and audit archive, run:

    python -I -S FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_BOOTSTRAP.py \
      EXTRACTED_AUDIT_DIRECTORY \
      FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_SAFE.zip \
      FRACTIONAL_INFINITY_30002288_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json

Append --optimized to run the diagnostic with -O. The bootstrap validates the
external manifest, archive and complete flat inventory before launching code.
Extra files, caches, altered entry points, symlinks and nonregular files fail
before the diagnostic. The expected output is
INDEPENDENT_DIAGNOSTICS_RESULTS.json. All finite checks are corroboration only.

## Replay the author and corrected artifacts

The two public scripts perform 36 isolated replay/mutation controls apiece.
Their inputs remain unchanged; only disposable temporary copies are modified.

    python -I -S replay_author.py \
      FRACTIONAL_INFINITY_30002288_AUTHOR_SAFE_FREEZE.zip \
      FRACTIONAL_INFINITY_30002288_AUTHOR_EXTERNAL_MANIFEST.json \
      FRACTIONAL_INFINITY_30002288_AUTHOR_BOOTSTRAP.py

    python -I -S replay_corrected.py \
      FRACTIONAL_INFINITY_30002288_CORRECTED_SAFE.zip \
      FRACTIONAL_INFINITY_30002288_CORRECTED_EXTERNAL_MANIFEST.json \
      FRACTIONAL_INFINITY_30002288_CORRECTED_BOOTSTRAP.py

Expected outputs are AUTHOR_REPLAY_RESULTS.json and
CORRECTED_REPLAY_RESULTS.json respectively. These scripts pin all three inputs
before invoking the independently reviewed bootstrap. The source inventories
must not be modified in place. The original historical status fields are
preserved in the corrected derivative; this independent acceptance report
supplies the later review decision.

No external specialist acceptance, journal endorsement, worldwide literature
completeness or novelty claim is made. No publication was performed by this
reviewer. The environment trust assumptions are stated in the full audit.

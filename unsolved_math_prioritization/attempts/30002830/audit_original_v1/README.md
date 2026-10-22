# Independent audit: Ueno method question 30002830

**SCOPED PASS. NO RATIONALITY RESOLUTION.** Five retained partial routes pass mathematical audit. The strongest is a rational cover of exact degree three, with descent unresolved. No mandatory correction to the frozen author packet was found.

Read AUDIT.md and CONTROLLING_SCOPE.md for the proof review and required limitations. The live target returned HTTP 403, and the full imported statement/report remain uninspected.

Run independent exact checks:

    python independent_verifier.py
    python -O independent_verifier.py

Replay all safe-tree and frozen-input bindings, symbolic outputs, and the author ZIP:

    python replay_audit.py --author-safe PATH/TO/author/safe --author-zip PATH/TO/UENO_METHODS_30002830_SAFE_V1.zip

Re-run corruption controls in temporary copies:

    python -O run_negative_controls.py --author-safe PATH/TO/author/safe

Use --integrity-only on replay_audit.py to check bytes without representing a symbolic replay as completed. Geometric theorem dependencies are stated and human-audited, not machine-formalized. No remote changes were made. This safe folder contains authored audit material, exact verification code/results, and public-source verification metadata only.

# Intrinsic rough viscosity: restricted positive result

Row 1838 · ID 30002169 · status UNSOLVED · turns 5 (UNSOLVED5).

This package records a source-bounded mathematical result, not a proof that the original question is still open today. No full-scope resolution was certified, and no novelty is claimed.

## Claim ledger

- **Accepted restricted proposition:** For a geometric step-two alpha-Hölder path, 1/3 < alpha <= 1/2, C_b-infinity transport fields, compact metric controls, the bounded/Lipschitz drift and cost assumptions stated in RESEARCH.md, and BUC terminal data, rough-flow pullback gives intrinsic controlled-test well-posedness and equivalence to smooth-driver/value-function approximation. The transformed-drift Lipschitz estimate and comparison growth estimates are explicit.
- **Existing GTT result:** Its intrinsic tests and flow equivalence are genuine; the explicit level-two smooth-field theorem assumes bounded Lipschitz F. Control Hamiltonians generally have gradient growth, so that theorem cannot be applied verbatim without the separately proved comparison bridge.
- **Existing CFO framework:** General p-variation with strong Lip^(gamma+2), gamma > p, transport regularity and invariant deterministic comparison; this is not a proved all-p controlled-expansion theorem at the low-regularity threshold.
- **Not established here:** Original low-regularity/general-p scope, richness of formal low-regularity jets, or an unchecked clock-change extension. The original transport question must not be conflated with arbitrary nonlinear-gradient noise.
- **Exact example convention:** Z^{ij} = integral Z^i dZ^j; pure area Z^{12}=a(t-s), Z^{21}=-a(t-s) gives displacement +a t in coordinate two and terminal shift +a(T-t), not twice that amount. The affine example is outside the bounded-field theorem; pure-area geometric approximation requires p>2.

## Files and evidence

RESEARCH.md contains the authored arguments; INDEPENDENT_AUDIT.md contains the independent mathematical acceptance and limitations. PUBLIC_SOURCE_METADATA.json and CORPUS_VERIFICATION.json contain public provenance only. PROVENANCE.json records input and sanitized-output hashes. No source PDFs, extracted source text, images, dataset records, or private coordination files are redistributed.

## Verification

Run from this directory:

    python3 -B verify_manifest.py
    python3 -B -O verify_manifest.py
    python3 -B test_integrity.py
    python3 -B -O test_integrity.py

The manifest verifier checks the exact file inventory, byte counts, SHA-256 digests, and copied-file provenance. The corruption suite tests normal and optimized Python against changed bytes, same-size changed bytes, deletion, extra files, symlinks, duplicate manifest paths, traversal paths and incorrect totals. These are integrity checks, not authentication and not mathematical proof verification. No theorem is certified by a computation in this package. A manifest cannot authenticate itself; retain its externally reported hash.

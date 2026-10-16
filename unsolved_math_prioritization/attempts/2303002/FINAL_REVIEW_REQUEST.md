# Independent full source/proof review request

Problem2303002 / AMR-022-3002. Proposed credited disposition: already_solved0/5. Please verify the exact original question, its immediately following Update3.2 and the full proof exposition before approving that disposition.

Primary sources are hash-bound in SOURCE_MANIFEST.json. The Hayman–Lingham target and update are printed p.60, PDF p.61. Carleson's theorem is on p.35, with its continuous-case discussion on pp.35–36. The full five-page paper was read, but its discontinuous-subharmonic extension is not a dependency of this packet's argument.

Audit-sensitive steps in SOURCE_PROOF.md:

- Correct normalization and uniform large-radius bounds for the ball Poisson kernel
- Spherical averages tending to the supremum for bounded nonnegative continuous subharmonic functions, without incorrectly claiming those functions are constant
- Zero-pasting on an arbitrary superlevel component without assuming regular boundary
- At most one bounded-above superlevel component, and why this supplies an unbounded-above child at every higher level even with infinitely many components
- Entire-tail lower bounds on polygonal pieces and compact-tail properness, rather than merely an escaping sequence
- One-sided harmonic Liouville via nonnegative harmonic functions, including the h(0)=0 case

The component proof is an explicit verification of the known continuous-case result, with no novelty claim. It avoids reliance on the printed thinness/Phragmén–Lindelöf criterion and does not assert that the entire discontinuous-case proof has been independently recertified.

Replay the standard-library arithmetic controls:

    python verify_source_alignment.py > /tmp/source-checks.json
    cmp SOURCE_CHECKS.json /tmp/source-checks.json

The3,675 controls are only sanity checks, not an analytic proof. Verify both PDF hashes and all final packet hashes. No raw PDFs, imported report or private material is included in the public-ready packet. No final queue change or PR before independent review.

# 3419 / OPG-37237: five attempts, unresolved

The question asks whether some smooth or locally flat PL 2-sphere in standard S⁴ has a complement group with an undecidable word problem. **This packet does not settle that question.**

- [Frozen research and proofs](public/PROOF.md): five substantive attempts, precise gaps, decidable special cases and excluded candidate groups.
- [Independent adversarial audit](audit/AUDIT.md): accepts the original packet as unresolved with valid partial results.
- [Exact-homology supplement](audit/HOMOLOGY_SUPPLEMENT.md): the September 2026 small undecidable group Γ₆ has dim H₂(Γ₆;Q)=7, so cannot be a sphere-knot group.
- [Separate check of the supplement](SUPPLEMENT_CHECK.md): verifies the additional argument independently of its author.
- [Source gate](public/SOURCE_GATE.md) and [attempt log](public/ATTEMPT_LOG.md).

The original public packet and audit are preserved byte-for-byte, including their historical pending-review headers. This overview records their completed review status. All conclusions remain AI-assisted research requiring expert checking; novelty, human peer review and a solution of the target are not claimed.

Five planned approaches are complete (100% of this investigation's attempt budget); the full target remains unproved. The exact homology calculation is a partial obstruction, not a percentage estimate of progress toward a solution.

## Reproduce

From this directory, using Python 3 with its standard library:

    python public/verify.py > /tmp/3419-author.json
    cmp public/verification.json /tmp/3419-author.json
    python audit/audit_verify.py > /tmp/3419-audit.json
    cmp audit/audit_verification.json /tmp/3419-audit.json
    (cd public && sha256sum -c SHA256SUMS)
    (cd audit && sha256sum -c SHA256SUMS)

The author verifier runs 35,453 finite consistency assertions. These checks do not prove undecidability, all subgroup embeddings, or a geometric realization. The written proofs and identified mathematical source theorems carry those arguments.

No source PDFs or extracted source text are redistributed. This submission proposes only this problem's artifacts and the queue row's status/attempt-count change to unsolved, 5/5. It is a review draft.

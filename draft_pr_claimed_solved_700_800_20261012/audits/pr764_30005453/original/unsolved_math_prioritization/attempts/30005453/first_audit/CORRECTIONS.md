# Required corrections to the frozen author description

These corrections do not change the theorem's hypotheses, conclusion, or analytic
proof in Sections 2–8. The mathematical verdict in AUDIT.md concerns the original
frozen proof. The proposed replacement files are not accepted by their editor;
they require a separate bounded delta review.

## C1 Source intent must be identified as inference

The report's equilibrium definition permits the alternating boundary examples,
and Conjecture 1 does not explicitly restrict uniqueness to positive arrays.
Consequently, phrases asserting an “intended” positive-equilibrium statement
must not be presented as a source-verified convention. Use:

“The theorem here addresses an explicitly corrected positive-equilibrium
formulation. Interpreting this as the source's intended non-vanishing
homogenization problem is an inference, not an explicit restriction in the report.”

Apply that distinction consistently in PROOF.md, README.md, SOURCE_REVIEW.md,
and the RESULT.json outcome label. Preserve the full warning that literal
nonnegative-equilibrium uniqueness is false. The source correction does not
invalidate convergence from unit initial counts or positive uniqueness.

## C2 Nonunit-count extension must reference the compensated identity

The positive-integer extension points to equation (12), although the needed
initial-condition change is in equation (9). The correct identity is

    H(N_e(t)) - H(N_e(0)) = Q_e(t) + M_e(t).

The fixed edgewise initial constant vanishes after division by t^(1-alpha).
The original extension is analytically valid. Correcting this reference makes
its justification unambiguous.

## Proposed delta boundary

PROPOSED_V2.diff gives the exact content edits. PROPOSED_V2_DELTA.json binds
the old and new hashes of the four changed content files. The proposed v2
manifest additionally updates generated size/hash records, its version label,
and the status to pending separate delta review. The other six content files
are byte-identical. No new analytic lemma or mathematical extension is added.

The historical v1 SOURCE_METADATA.json's absent review-hash assertion is not
retroactively changed. The independent reconstruction of that hash belongs to
this audit's results/provenance.json.

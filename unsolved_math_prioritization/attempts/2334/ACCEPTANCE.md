# Acceptance of the corrected EP-839 / 2334 note

## Decision

ACCEPT_WITH_MINOR_BOUNDARY_WORDING_CORRECTION. The correction has been incorporated into PROOF.md. Both original density questions remain unresolved for arbitrary admissible sequences. Novelty and priority are not asserted.

The independent audit accepts the complete general mass theorem with coefficient log(C)/log(2), the admissible width-two sharpness construction and full-x asymptotic, Freud's finite count and sum polynomials, the general symbolic printed-rule defect, the universal repair for T>=3, and the repaired sequence's exact upper density 19/36 and reciprocal coefficient gamma=[log 2+(19/12)log(9/8)]/log 4.

## Minor correction to our note

The original sentence asserted that both surviving C-bridge terms were strictly inside C for T>=4 divisible by 4. At T=4 the left term equals C's first term. Both terms still belong to C and are consecutive; all theorem statements, constants and substantive conclusions remain unchanged. The accepted wording states the boundary explicitly.

Original authored note: 17,633 bytes; SHA-256 84569672464364bd298fafad242a5de76acfbe4ed4bce67ba9ea1b5856b458fb.

Accepted corrected note before publication editing: 17,715 bytes; SHA-256 77ed2a28eb062dcce26b2eab3d6c5509e218f4af73c415307cf3cd30b06866c2.

CORRECTION.patch replays that exact one-paragraph change from the original note to the accepted corrected note. Its zero-context presentation omits nearby coordination references and optional examples. The publication proof has subsequent documented editorial changes, so this patch is historical evidence of the minor correction, not an instruction to patch PROOF.md a second time.

## Substantive repair of the printed extension

This is separate from the wording change. Freud's printed final deletion interval begins at 4L+3T+1. For T>=4 divisible by 4, the newly adjacent C terms have sum 4L+3T, which survives the printed deletions. The proof checks membership, adjacency, residue classes and every deletion family symbolically. The original finite-block sum polynomial gives T=6100 for F_1, showing that the witness applies to the source's own valid seed.

Replacing that endpoint by 4L+3T gives a sufficient repair for every admissible prefix of total T>=3. The proof exhausts entirely new-block sums and sums crossing the old/new boundary. The finite construction and the existence of the upper-density-19/36 sequence remain valid. The excluded T=1 boundary is not covered by the repair theorem.

## Preservation, evidence and limits

The original candidate inventory has 13 members and manifest SHA-256 b36ac515383501830bfe77f06956da84b5bef309d4f9c0534a0abe6fc960a414. The independent audit has 20 members and manifest SHA-256 df60ca0b91a5190966b10abf984c50c91f8b52e502b992afc9636caca212a584. Both sealed originals remain unchanged.

Edition editing removes optional explicit large witness numbers, small finite seed examples and private checker references, and updates status and historical-evidence framing. It preserves the complete general symbolic proofs, exact finite formulas, all-x asymptotic arguments, and all qualifications. The mathematical results rest on those proofs; historical finite checks only corroborate them. Hashes certify byte identity and recorded matches, not mathematical truth.

Historical audit tests passed in normal Python, -O and -OO with the same certificate digest; counts and identities are in VERIFICATION.json. No mathematical programs or third-party code were run during edition preparation, and no fresh scholarly-source inspection is claimed. Source documents and computational evidence contents are not reproduced. These files alone do not reproduce the historical program runs.

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit, not external human peer review, journal acceptance or formal proof-assistant certification.

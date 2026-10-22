## Accepted partial result and correction

Both original EP-839 questions remain unresolved for arbitrary admissible
sequences: lower natural density zero, and H_A(x)/log x tending to zero.
No novelty or priority is asserted.

The complete proof and independent audit establish the general mass bound
H_A(x) <= (log C/log 2) log log x+O_C(1) for prefix-sum-separated blocks
contained in [m_r,Cm_r], without needing an avoidance assumption. An explicit
admissible width-two construction attains H_A(x)=log log x+O(1), with lower
density zero and upper density 1/2. These asymptotics hold for all x.
The avoidance property has not been shown to force this block architecture.

## Two separate corrections

The substantive correction concerns Freud's printed infinite-extension rule.
For every T>=4 divisible by 4, the retained consecutive C terms
(2L+T-2) and (2L+2T+2) have retained sum 4L+3T. The complete symbolic proof
checks membership, adjacency, residue classes and all deletion families.
The finite count 76y-7 and total 7436y²-1406y+70 show that the source's own
valid F_1 seed has T=6100, so the objection applies to that seed.

Lowering the final deletion interval's left endpoint from 4L+3T+1 to 4L+3T
is proved sufficient for every admissible prefix of total T>=3. All internal
new-block sums and old/new boundary sums are exhausted. Freud's finite
construction and the existence of the upper-density-19/36 example remain
intact. For the repaired sequence,
H_A(x)=gamma log log x+O(1), where
gamma=[log 2+(19/12)log(9/8)]/log 4, for all x.

The independent audit separately corrected one sentence in our note:
at T=4 the left C-bridge term equals C's first element rather than being
strictly interior. Membership and consecutiveness hold. The accepted proof
already incorporates this wording correction. CORRECTION.patch records only
that original-note correction, with zero adjacent context; it is not to be
applied again to the publication proof. Its original and accepted target
identities are stated in ACCEPTANCE.md.

## Evidence, citations and review limits

[Freud, Adding Numbers (1993)](https://webhomes.maths.ed.ac.uk/cook/iss_no60.PDF)
was historically inspected throughout printed pages 6199-6202, including the
image of the printed endpoint on page 6202.
[Erdős, Some forgotten problems (1992)](https://hrj.episciences.org/125/pdf)
was historically inspected at printed pages 42-43 for the original questions
and the separate upper-density speculation. The known log-log growth and
finite density construction receive prior credit. The later
Coppersmith-Phillips full paper was not inspected. No new source inspection
or comprehensive novelty search is claimed for edition preparation.

The original candidate's 13 members and independent audit's 20 members remain
unchanged, as do all 100 pinned source-handoff members. Their bytes and sizes
were revalidated. Historical independent tests passed in normal Python, -O
and -OO with identical certificate hashes, covering 83 finite parameters,
162 corrected extensions, symbolic C-bridge cases, six width-two stages
ending with 40,191 terms, and 21 negative or boundary controls. Those
mathematical programs were not rerun for this edition. The historical runs
are not reproducible from this prose-and-metadata edition alone. Universal
and asymptotic claims rest on the written proofs. Hashes certify byte identity
and recorded matches, not mathematical truth.

This AI-assisted work is unrefereed. Acceptance means an independent internal
AI mathematical audit, not external human peer review, journal acceptance or
proof-assistant certification.

## Narrow addition-only boundary

Exactly eight files of authored mathematical prose, a minimal correction patch,
and public verification/source metadata are added under
unsolved_math_prioritization/attempts/2334. Complete symbolic proofs, finite
formulas and the source-specific T=6100 derivation are retained. Optional large
explicit witness numbers, small finite seed examples, source text/documents,
scans, OCR, programs, raw datasets, detailed certificates, private sources,
personal data and private coordination records are excluded.
QUEUE.md and every existing repository path remain unchanged. Draft only;
no merge, release, DOI or CI-pass claim.

Base commit: `4b27092a448d53b61408355ce44ec38d103a1ce4`.

## Exact public-file identities

- `ACCEPTANCE.md`: 3,929 bytes; SHA-256 `e15d9a89eb1c8fb9e9d4dfd21c3039891b72ef575c4b8370a660391bb5db7c91`.
- `AUDIT.md`: 17,729 bytes; SHA-256 `748df3a14b7abaf3975b50123086c6881a2b7d0cc02eee46200be81544c65615`.
- `CORRECTION.patch`: 1,350 bytes; SHA-256 `cb661007da3ad98028c76b87ca0fe5cc69cf12c5cec980b5b9efab0381a8d880`.
- `MANIFEST.json`: 1,694 bytes; SHA-256 `176d87981c567e367aed4cc262fb7a4950f0901c4c4fad5ccb93221936c327fc`.
- `PROOF.md`: 17,397 bytes; SHA-256 `a132d64654e56a9858276c0e00a1a54f5b2cdf639feb1a125fb8768b2e806479`.
- `README.md`: 3,570 bytes; SHA-256 `db0109d8cb582c4f0aa2a40c6bc5def4375707ccfed801c0a82203c5dc3156cd`.
- `SOURCES.json`: 1,628 bytes; SHA-256 `add411fff0580febf923e3a95c58e6bfed63a3fbc5350872fd10f5fb46cbfa11`.
- `VERIFICATION.json`: 3,859 bytes; SHA-256 `b6ccd0fa6f113d40aa34771a0c21e01102710be8e4ec27eef15e7ec4662f6850`.

MANIFEST.json lists eight members and hashes the other seven; this body independently pins its digest.


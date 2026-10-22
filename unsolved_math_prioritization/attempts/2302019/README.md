# Asymmetric exponential-type bounds: reconstructed partial results

Problem 2302019 / AMR-022-2019, queue rank 674. **Unsolved, historical
five-turn budget 5/5.** This draft preserves a fresh 2026-10-05 reconstruction
and its fresh independent audit. The original sharp modulus at a general
nonreal point remains unresolved.

The historical research record reports five substantive approaches ending
unsolved. Their original files were unavailable; these are newly authored
proofs, not recovered original bytes or five newly claimed historical turns.
No earlier acceptance is inherited. The author reconstruction's subjective
progress estimate toward the sharp target is 10%; packaging and successful
finite replay do not increase that mathematical estimate.

## Read the result and its limitations

- `author/PROOFS.md`: compact extremal attainment, a strict step-Poisson
  gap, an explicit Bernstein-ramp improvement, an integrated-sinc witness,
  and the finite real-frequency approximation obstruction.
- `audit/AUDIT.md`: the complete fresh independent mathematical audit,
  PASS for the stated partial results only.
- `audit/CORRECTIONS.md`: no mandatory corrections; three optional
  explanatory clarifications are preserved separately from the author freeze.
- The obstruction excludes local-uniform approximation on any nonempty
  complex open set **only for globally admissible finite real-frequency
  sums with a common type bound**. Sampled caps or unbounded types are
  not covered. No sharp general complex-point bound or extremizer formula
  is proved; ramp optimality is not asserted.
- Classical results and the historical real-axis solution are credited.
  No novelty, exhaustive current-literature finding, or identification with
  the exact Gol'dberg--Levin envelope is claimed.

Both frozen directories are byte-preserved. Public source provenance and
inspection limits accompany the authored work; source PDFs, extracted
source text, images, dataset contents and private coordination are excluded.
AI-assisted authorship and audit are unrefereed and are not human peer review.

## Reproduce

Use unoptimized Python 3 with mpmath 1.3.0 available, then run from this
folder or pass the script's path:

    python3 -B replay.py

The wrapper rejects `-O`, `-OO`, and optimization inherited through
`PYTHONOPTIMIZE`. It verifies strict file inventories and both independently
recorded manifest digests, runs the original scripts in normal Python mode,
and compares every saved audit result except the interpreter-version
provenance string. Extra files, missing files, symbolic links, changed bytes,
and manifest inconsistencies are rejected. Keep outputs outside this folder.

Expected finite controls are 832 exact rational checks and 2,413 author
floating-point smoke checks, plus 859 independent non-certified smoke checks,
six integrity mutation controls, two author optimization guards, and a
coherent-rewrite/external-binding control. Numerical quadrature is not
certified; these counts are not numbers of proved theorems.

Trust anchors:

- Author manifest SHA-256:
  `6584a3d052edae771b709241b7ee909e7684efe318c0045e7ad36118f6008f12`
- Audit manifest SHA-256:
  `13356d28cf40480b72aafdd1a69a97074522d2bc6c9da2cadb6b17b518db9710`

`PUBLICATION_MANIFEST.json` inventories this complete delivery apart from
itself. Authenticate its digest from the draft PR or a separately retained
receipt; a self-consistent manifest alone cannot authenticate a packet.

The only queue changes in this draft are this problem's Status=`unsolved`
and Turns=`5/5`. The existing queue header and every other byte are preserved.
No queue regeneration, merge, GitHub release, DOI deposit, or outreach is
part of this draft.

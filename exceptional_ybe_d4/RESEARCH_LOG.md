# Research log: exceptional \(d=4\) Hecke Yang--Baxter operator

All times are America/Los_Angeles (PDT, UTC-07:00).

## 2026-07-27

- **19:33:15** -- Opened an independent audit of the proposed \(16\times16\)
  witness for the exceptional class
  \([e^{i\pi/3},\tfrac12,4]\).
- Preserved the supplied verifier as `verify_supplied.py`.  The retained file
  checks the final witness but is not evidence about how the witness was
  discovered.
- Audit scope fixed before publication: exact matrix and tensor-word checks;
  tensor ordering; Hecke normalization; spectrum and partial traces; the
  Markov-trace/localization claim; amplification to larger dimensions;
  minimum local dimension; generalized-Yang--Baxter interpretations; and a
  primary-source priority search.
- Independent-research rule recorded: no author, expert, or other outside
  individual will be contacted.  Potentially useful outside review will be
  listed as a limitation only.
- Repository state: work is being carried out on `main` in a dedicated folder.
  Unrelated untracked files from parallel research programs are excluded from
  every stage and commit.
- **19:42:53** -- Core verification checkpoint completed.
  - The supplied SymPy verifier passed using SymPy 1.14.0.
  - A new standard-library checker independently implemented exact arithmetic
    in \(\mathbb Q(\sqrt2,\sqrt3,i)\).  It directly checked the \(16\times16\)
    Hecke and unitarity identities, the \(64\times64\) Yang--Baxter equation,
    both partial traces of the spectral projection, and the \(32\times32\)
    \((3,2)\)-generalized Yang--Baxter equation after the required coordinate
    permutation.
  - A second new checker worked only in the abstract tensor-word algebra.  It
    found exactly 18 words in the generic cubic residual and matched every
    rational polynomial coefficient against a hard-coded certificate.
  - The involution circle \(H(\alpha,\beta)^2=I\) is exact.  On that circle all
    18 residual coefficients vanish exactly when
    \(\beta^2=1/3\), hence \(\alpha^2=2/3\).
  - Both unnormalized partial traces of
    \(P=(I-H)/2\) equal \(2I_4\).  This supplies the Markov parameter
    \(\eta=1/2\) needed for the full localization argument, rather than merely
    the two-site spectrum.
- Corrected the provenance copy of the supplied verifier to be byte-for-byte
  identical to the download.  SHA-256:
  `df5ccbc8807c20a2f782762681100e3ad06cb95a750b7e052839584006fe3677`.

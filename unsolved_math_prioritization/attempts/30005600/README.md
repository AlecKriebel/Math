# 30005600: corrected scoped partials; full conjecture unresolved

**Disposition: unsolved, 5/5 substantive approaches.** Start with the [corrected proof](review/reading_copy/PROOF.md), then the [full independent AI mathematical audit](review/AUDIT.md) and [acceptance report](ACCEPTANCE.md). No full solution, novelty, human peer-review, or formal-proof claim is made.

For the trivial spin structure on a fixed skew torus, a smooth positive b-periodic conformal factor f(y) satisfying max f <= integral_0^b f has full first strictly positive Dirac eigenvalue 2*pi/integral_0^b f. Every horizontal Fourier sector, including its quasiperiodic boundary condition, is controlled. The normalized value is at least the flat value. The weighted kernel-corrected Rayleigh formula and exact Ritz matrices are also accepted scoped results.

The b>2*pi theorem belongs to Karpukhin, Métras and Polterovich; b=2*pi follows from their published comparison and the flat value. The full pi-threshold conjecture, including b=pi, remains unresolved here.

## Required mathematical scope corrections

- Covering estimates bound the energy of the pulled-back harmonic map and its associated eigenpair. Additional lower eigenmodes of the pullback metric are uncontrolled. The direct metric-cover counterexample route is not closed.
- At b=2 the search misses a known spherical-bubbling comparison below flat. This does not establish that concentration is necessary or that a smooth minimizer does not exist.
- The floating-point search is uncertified and supplies no spectral lower bound.

These are substantive scope corrections, not typography. The exact [patch](review/SCOPE_CORRECTIONS.patch) produces the corrected proof and research log from the preserved author files. The historical `author/` material and `AUTHOR_30005600.zip` retain the superseded wording for auditability; read them with the correction patch and audit. Their pending-review/publication statements describe the freeze, not the present packet.

## Reproduce without source files

Run `python verify_packet.py` from this directory or use its path from elsewhere. This checks the full packet manifest, frozen author/review manifests, all archive members, the exact correction patch, and normal plus optimized exact-control outputs. It requires Python 3.10+ and the standard `patch` command. It does not fetch or require scholarly-source files or datasets, and it does not prove the analytic arguments.

`python verify_packet.py --numerical` additionally replays the complete frozen numerical search in a temporary directory and requires byte-identical JSON. It requires NumPy and SciPy; the independently audited replay used Python 3.12.14, NumPy 2.3.5 and SciPy 1.17.0 with single-thread BLAS. Other numerical libraries/platforms can change last digits or optimizer paths. A mismatch fails the replay rather than silently relaxing the comparison. The auditor's already completed numerical replay is recorded in the full audit and its frozen replay file.

No source PDFs, extracted third-party text, screenshots, dataset contents, private sources, private personal data, or private coordination files are included. [Public source metadata](author/SOURCES.json) records source identities, public URLs, sizes, hashes and inspection history; it is not source content or proof of exhaustive literature coverage.

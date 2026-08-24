# Replay status for the v1.0.8 pre-submission release candidate

This file distinguishes the unqualified current release candidate from
historical v1.0.7 evidence and from historical-lineage verification.

## v1.0.8 current source: passed current-release qualification

The active metadata and reproducibility infrastructure target version 1.0.8.
The pinned TinyTeX 2022.04/pdfTeX 1.40.24/Biber 2.17 preflight and exact Python
lock pass.  The current campaign also passes:

- all 25 mutation/regression tests, including all 39 direct entrypoints under
  optimized Python, where every one fails closed;
- every direct verifier entrypoint under normal Python, the complete symbolic
  aggregate, and the standalone all-dimensional cubic-recurrence bridge;
- the current-profile exact generators, provenance checks, all 15 numerical
  illustrations, and the refinement gate;
- exact integrated designs through the current stress dimensions 149 and 200;
- the 19-page manuscript, 19-page supplement, 3-page theorem summary, 6-page
  proof skeleton, and four standalone figures under semantic, producer,
  embedded-font, clean-log, and page-by-page visual checks;
- all seven deterministic bundle hashes and clean detached builds of the three
  submission source ZIPs; and
- a full replay from a detached copy of the portable public package through
  `PUBLIC_REPLAY_PASS`.

The portable replay preserves its downloaded manifest, verifies deterministic
exact artifacts against that baseline, and writes a distinct regenerated-tree
self-consistency manifest.  A detached mutation control confirmed that an
exact-profile edit is rejected by both.  The exact preceding v1.0.7 release
remains archived at `10.5281/zenodo.22062080`.

## Historical v1.0.7 round-7 source status: passed

The branch-positivity closure, exact within-family contrast-minimum statement,
positive-diagonal diffusion quantifier, and SCC terminology cleanup target
immutable version 1.0.7.  The documents, seven bundles, submission packages, portable
repository, and manifests have now been regenerated from those exact sources.
All 22 mutation/regression tests, the complete symbolic aggregate, the source
and PDF semantic audits, three isolated submission-source builds, and the
detached full portable replay pass.

## Historical v1.0.7 source: passed checks

The following were rerun after the high-dimensional endpoint repair and final
source edits:

- 22 mutation/regression tests;
- the complete symbolic aggregate, including the determinant-identity bridge,
  the 22-term homogeneous certificate, the 84-term spatial certificate, the
  exceptional `m=3` cubic, and the exact legacy-endpoint counterexample;
- current-profile and detached numerical provenance;
- finite integrated designs at `m=3,4,5,6,8,10`, with the repaired Pareto
  family also checked at `m=149` and `m=200`;
- full current-profile cosine-Galerkin simulations and the strengthened
  refinement audit (maximum recorded relative discrepancy
  `1.6246526173879546e-08`, below the `2e-8` gate);
- all eight principal PDFs: 18-page manuscript, 18-page supplement, 3-page
  theorem summary, 6-page proof skeleton, and four one-page figures;
- all seven ZIP integrity checks and all three detached submission-source
  builds; and
- a full portable replay in a detached copy of `public/repository`, including
  a replay-generated self-verifying manifest. The shipped pre-replay public
  tree has its own complete manifest; the replay regenerates numerical outputs
  and verification records for the downloader's local toolchain while
  retaining the canonical public file set.

This round additionally verifies the corrected maximal stoichiometric minor
$4(-1)^m$, the explicit $m=3$ SCC base case, the reflection-induced odd
center-manifold normal form, the parameterized equilibrium-scaled PDE, and the
printed four-variable second-harmonic boundary system.
The final exposition pass also reconstructs the generic near-threshold affine
critical vector and all induced diffusion entries from
$(A_m-D)r^{\rm aff}=0$, prints the scaled transversality numerator, and
restricts the localization minimum explicitly to nonempty principal sets.
The 21 August precision pass additionally verifies the explicit
$a,b$-dependence of $s_*(a,b,H,D)$, the all-dimensional identity
$\Pi_m'(0)=-(163/45)\ell^Tr>0$, the
generalized-vector exclusion after
positive row scaling, the final order-$(n-1)$ coefficient hypothesis in the
network application, and the fixed-mass Fredholm/transversality interface.
The final 22 August closure proves componentwise branch positivity from
$H_N^2\hookrightarrow C^0$ for each fixed parameter choice, verifies exactly
that $\chi_D(L)>\chi_H(L)$ throughout the certified scaling interval and that
the within-family maximum is uniquely minimized at $L_0$, and makes the
positive diagonal $D$ explicit in the exact network diffusion theorem.  It
also separates negative singleton SCCs from the non-singleton classification.
The stable Zenodo concept DOI remains `10.5281/zenodo.21753404`; the exact
preceding v1.0.6 snapshot is `10.5281/zenodo.22058969`, and is not
misidentified as the new v1.0.7 source.

The portable replay used Python 3.9.6, Matplotlib 3.7.1, NumPy 1.24.3,
Pandas 2.3.3, pypdf 6.10.0, pytest 8.4.2, SciPy 1.10.1, and SymPy 1.14.0.
Because pdfTeX was unavailable in the repair environment, its `pdflatex`
invocations were routed through a local Tectonic 0.16.9 compatibility shim.
The canonical build retained the already verified Biber 2.17 bibliography
output because the bibliography did not change. Each submission source ZIP
was then extracted into a fresh temporary directory and built independently
with Tectonic and Biber 2.17, producing the expected 18-page main and 18-page
supplement. The detached public replay used the same compatible pair and ended
in `PUBLIC_REPLAY_PASS`. Numerical outputs are certified to the recorded
tolerances, not asserted to be byte-identical across BLAS/SciPy toolchains.

## Historical-lineage stage: not rerun for v1.0.8

The top-level command additionally requires five frozen source archives listed
in `release/reproducibility.md`. They were unavailable in the final repair
environment. Its preflight was exercised against an empty `FROZEN_BASE`: it
reported all five missing archives, exited with status 2, and did not create or
truncate `release/replay.log`.

Accordingly, v1.0.8 claims a current portable replay and direct verification of
the substantive stages above. It does **not** claim that this tree completed
the optional historical-lineage replay. The lineage
archives are not consumed by any current proof, data, document, or package
stage.

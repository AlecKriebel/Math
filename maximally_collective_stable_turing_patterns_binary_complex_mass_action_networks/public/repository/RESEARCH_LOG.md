# Research log

## 2026-08-15 21:37:07 PDT

- Imported the final flagship paper and reproducibility package into a dedicated top-level research folder.
- Confirmed the title from `manuscript/main.pdf`: *Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*.
- Verified the supplied immutable manifest and embedded archive integrity before import.
- Preserved the package without initiating any submission, outreach, or other external communication.
- Excluded macOS `.DS_Store` metadata files from version control.

## 2026-08-16 21:30:49 PDT

- Replaced the original flagship package in place with the revised final release.
- Confirmed the revised title from `manuscript/main.pdf`: *Exact Diffusion Design for Maximally Collective Stable Turing Patterns in Binary-Complex Mass-Action Networks*.
- Matched renamed verifier files by content and purpose, including `verify_one_bad_minor.py` to `verify_network_one_bad_minor.py` and `verify_primary_crossing.py` to `verify_principal_minor_diffusion_ray.py`.
- Removed superseded certificates, legacy simulation parameterizations, redundant figure aliases, and obsolete audit fragments that are absent from the revised release.
- Excluded `.DS_Store`, test caches, Python bytecode, and transient LaTeX build products while retaining intentional release logs and verification outputs.
- Preserved the existing folder and log so the revision remains a direct, reviewable Git history rather than a second independent import.
- Verified 9 live tests, the manuscript and stale-claim audits, both numerical-provenance checks, the generalized diffusion-ray theorem interface, the network-specific one-bad-minor corollary, all symbolic certificates, 710 immutable manifest hashes, and 7 embedded archives.
- Visually reviewed all 15 manuscript pages and all 12 supplement pages; the replicated manuscript and supplement PDFs agree byte-for-byte across the public and submission packages, and all fonts are embedded.

## 2026-08-16 22:20:21 PDT

- Began a clean-main pre-submission adversarial replay and review in an isolated
  checkout, preserving unrelated dirty worktrees.
- Replayed the nine mutation/regression tests, numerical-provenance audits,
  principal-minor theorem verifier, all-dimensional symbolic verifiers, exact
  integrated designs, and full current-profile simulations.
- Confirmed the supplied local algebraic-simplicity objection and reference,
  caption, replay-prerequisite, and terminology defects.
- Found an additional exact transcription error in the printed boundary-triad
  Routh--Hurwitz gap and a missing `m=3` homogeneous-stability base case.
- Found a release-blocking high-dimensional counterexample missed by the prior
  review: at `m=149`, `nu=147`, and the old rational endpoint `L=1/21`, the
  equilibrium-scaled homogeneous Jacobian has an unstable complex pair.
- Traced the failure to a 34-term polynomial certificate not connected to the
  actual characteristic determinant.  Derived and independently checked a
  repaired piecewise endpoint and exact 22-term determinant-linked certificate
  that preserve both `Theta(sqrt(m))` contrasts.
- Rechecked the close literature boundary and added Haas--Goldstein (2021), a
  relevant statistical study of many-species diffusion thresholds and
  lower-dimensional reduction failure.

## 2026-08-16 23:16:52 PDT

- Completed the endpoint repair with a direct `QF-R` homogeneous certificate,
  a separate exact `m=3` Routh--Hurwitz proof, and an exact rational Rouché
  regression for the unstable superseded `m=149`, `L=1/21` endpoint.
- Strengthened the release gates: 13 mutation tests now alter endpoint,
  certificate, and Fourier data; the determinant-identity verifier is in the
  canonical aggregate; optimized Python mode is rejected; and the numerical
  refinement threshold is the claimed `2e-8`.
- Rebuilt and visually inspected all 39 pages across the eight principal PDFs.
  The three numerical figures now use embedded TrueType fonts, and all document
  fonts are self-contained.
- Refreshed and integrity-tested all seven public, submission, and specialist
  ZIPs. Each of the three submission source bundles compiled independently to
  16 manuscript pages and 12 supplement pages.
- Completed a full portable replay in a detached public-package copy. The exact
  source and certificate tables reproduced byte-for-byte; numerical
  illustrations satisfied their structural and tolerance audits.
- Confirmed that the top-level historical-lineage preflight fails safely and
  leaves no misleading replay log when the five external frozen archives are
  unavailable. No post-repair historical-lineage replay is claimed.
- Kept the later SIADS directory explicitly provisional. Funding, competing
  interests, exclusivity, final AI disclosure, keywords/MSC, and portal fields
  remain author-controlled decisions; no external communication or submission
  was initiated.

## 2026-08-16 23:34:00 PDT

- Completed independent final mathematical, manuscript/PDF, and release audits;
  all three found no remaining substantive blocker after the repaired endpoint
  and determinant-linked certificate were propagated through every mirror.
- Made the portable replay preserve its strict canonical file set, preflight
  all required external tools before mutation, and regenerate and verify the
  seven-bundle checksum record on every package refresh.
- Reconfirmed 13 adversarial tests, the complete symbolic aggregate, the
  tightened numerical-provenance gate, all PDF and ZIP checks, and exact
  public/package mirror integrity on the final sources.
- Recorded the SIADS materials as synchronized but provisional pending the
  author's required metadata and journal-format decisions. No submission,
  outreach, or other external communication was initiated.

## 2026-08-17 17:04:25 PDT

- Completed the final pre-submission proof-exposition pass without changing
  the reaction topology, repaired piecewise endpoint, current-profile data, or
  theorem content.
- Scoped every lower bound and optimality statement to stationary crossings of
  the indexed topology; framed equilibrium contrast as concentration-scale
  separation; and made the fixed contrast-product identity prominent.
- Printed the complete $R_m$, $C_m$, $L_m$, $N_m^{\rm ref}$, gauge-tail, and
  clearing-factor bridges, together with explicit source polynomials, sign
  conventions, term counts, and equality cases for all four modulus tables.
- Separated the supplement's coefficientwise-nonnegative and signed
  certificates; removed the remaining notation collisions; and restricted the
  robustness statement to the positive-equilibrium realization manifold.
- Verified the subsystem-endpoint comparison against the published general-$n$
  terminology of Satnoianu--Menzinger--Maini and the complementary
  three-component analysis of Anma--Sakamoto--Yoneda. No external contact was
  initiated.
- Added exact freshness gates for the printed modulus, triad, and signed-scalar
  tables. All 18 mutation/regression tests and the complete symbolic aggregate
  pass, including the direct $m=149$ Pareto check.
- Rebuilt and visually inspected all 45 pages across the eight principal PDFs;
  independently compiled all three submission source archives to 16 main and
  17 supplement pages; refreshed and hash-checked all seven deterministic ZIPs;
  and completed a full detached portable replay of the final public package.

## 2026-08-19 21:27:06 PDT

- Completed a fresh adversarial pre-submission revision without changing the
  reaction topology, repaired piecewise endpoint, numerical data, or theorem
  conclusions.
- Distinguished the dynamical one-dimensional center-manifold normal form from
  the associated stationary Lyapunov--Schmidt zero equation, excluded the empty
  principal set from the spectral-max statements, and made the selected-
  realization quantifier in the subsystem-endpoint corollary explicit.
- Replaced floating-point ordering in the exact Pareto verifier and mutation
  test with symbolic pairwise certificates, including the repaired `m=149`
  endpoint regression.
- Consolidated the crowded `R_3,\ldots,R_{m-2}` labels in the topology figure
  and fixed the numerical-figure float so it no longer interrupts the open-
  problem list.
- Rebuilt and visually inspected all 46 pages across the eight principal PDFs;
  the main manuscript is now 17 pages, the supplement 17, the theorem summary
  2, and the proof skeleton 6. No external communication was initiated.

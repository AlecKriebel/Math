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

## 2026-08-20 21:30:43 PDT — round-4 source checkpoint

- Independently rejected the alleged S9 $\nu/u$ typo: the current source,
  immutable v1.0.3 source, and rendered supplement all already use Latin $u$.
- Verified the reviewer-supplied affine-vector and diffusion formulas directly
  from $(A_m-D)r^{\rm aff}=0$ for $m=3,\ldots,10$, then printed them in S9.
- Printed the exact transformed transversality numerator and restricted the
  localization minimum to nonempty principal sets.  No theorem, endpoint,
  topology, or numerical profile changed.
- Added exact source and symbolic regressions and corrected archive metadata:
  v1.0.3 has version DOI `10.5281/zenodo.22032277`, while all versions share
  concept DOI `10.5281/zenodo.21753404`.
- Best-guess completion toward the pre-submission v1.0.4 release: **70%**.
  Remaining work is document rebuilding, visual inspection, package replay,
  independent final audits, manifests, and immutable publication.

## 2026-08-20 09:11:57 PDT

- Independently confirmed and corrected a false, unused dimension-dependent
  value for a maximal stoichiometric minor.  The balance
  equations give the exact two-dimensional kernel and rank $m$ by
  rank--nullity; an explicit maximal minor has determinant $4(-1)^m$.
- Added the direct $m=3$ SCC base case and the Neumann reflection argument that
  makes the one-dimensional center-manifold vector field odd, exchanges the
  two patterned branches, and justifies the stated odd remainder.
- Restored the bifurcation factor $(1-\mu)$ in the equilibrium-scaled PDE,
  removed three local notation collisions, and printed the exact four-variable
  second-harmonic boundary system with determinant
  $64\mathcal Q_m/[6615(91m-183)(91m-181)(91m-180)]$.
- Corrected Figure 1's outline description and reinspected the centered
  $R_3,\ldots,R_{m-2}$ label.  Added the adjacent 2025
  reaction--cross-diffusion design paper and assigned distinct roles to the
  functional-analytic references without guessing theorem numbers.
- Added exact stoichiometric-minor and second-harmonic regressions plus source
  and PDF semantic gates.  All 19 tests and the complete symbolic aggregate
  pass, including the exact Pareto check through $m=149$.
- Rebuilt and visually inspected all 46 pages across the eight principal PDFs,
  refreshed and hash-checked all seven deterministic bundles, and completed a
  full portable replay.  Prepared immutable release version 1.0.3; no archival
  DOI is claimed and no external communication or submission was initiated.

## 2026-08-20 21:52:11 PDT — round-4 final verification checkpoint

- Confirmed that the reported S9 Greek-$\nu$ typo was absent from both v1.0.3
  and the current source; retained Latin $u$ and added a defensive regression.
  Made S9 self-contained by printing the affine critical vector and every
  induced diffusion entry, all verified exactly from
  $(A_m-D)r^{\rm aff}=0$.
- Printed the equilibrium-scaled transversality numerator and restricted the
  localization minimum explicitly to nonempty principal sets.  No topology,
  endpoint, current-profile datum, numerical table, or theorem conclusion
  changed.
- The full symbolic aggregate, all 20 mutation/regression tests, manuscript
  audit, stale-claim audit, numerical-provenance audit, and PDF semantic audit
  pass.  Exact finite checks include the repaired Pareto family at $m=149$ and
  the generic near-threshold ansatz through representative dimensions.
- Rebuilt and inspected all 48 pages across the eight principal PDFs: 17-page
  main manuscript, 18-page supplement, 3-page theorem summary, 6-page proof
  skeleton, and four one-page figures.  No clipping, overlap, unresolved
  reference, or font defect remains.
- Refreshed and hash-checked all seven deterministic bundles, independently
  rebuilt all three submission archives, and completed an isolated full public
  replay ending in `PUBLIC_REPLAY_PASS`.  Three independent final audits found
  no mathematical, manuscript, or release blocker.
- Prepared v1.0.4 metadata with ORCID `0009-0001-9320-500X` and stable Zenodo
  concept DOI `10.5281/zenodo.21753404`.  No external communication or
  submission was initiated.
- Best-guess completion toward the round-4 pre-submission revision and
  verification goal: **100%**.

## 2026-08-21 13:34:07 PDT — round-5 mathematical-precision checkpoint

- Independently reproduced the reviewer’s $m=3$ threshold polynomial and
  confirmed that the threshold location depends on the steady-flux parameters
  $a,b$, although the exact crossing criterion does not.
- Derived the all-dimensional selected-mode identity
  $\Pi_m'(0)=-(163/45)\ell^Tr>0$
  directly from the sparse determinant,
  closing algebraic simplicity at the unique equality point of the 77-term
  certificate.
- Verified that invertible positive row scaling preserves the selected kernel
  and that the transformed left-right pairing excludes every generalized
  zero eigenvector.  No theorem conclusion, topology, endpoint, or numerical
  profile changed.
- Confirmed publicly that the v1.0.4 GitHub release and Zenodo concept/version
  DOIs resolve; the review’s broken-metadata concern was stale.
- Best-guess completion toward the round-5 pre-submission revision and
  verification goal: **55%**.

## 2026-08-21 13:59:07 PDT — round-5 rebuilt-release checkpoint

- Propagated the flux-dependent threshold notation, selected-zero derivative,
  network-to-matrix coefficient bridge, row-scaled generalized-vector
  exclusion, and fixed-mass Fredholm/transversality interface through the
  manuscript, supplement, theorem summary, proof skeleton, and exact audits.
- The full symbolic aggregate and all 21 mutation/regression tests pass.  The
  rebuilt PDFs contain 49 pages in total (18-page main, 18-page supplement,
  3-page theorem summary, 6-page proof skeleton, and four one-page figures),
  all visually inspected without clipping or overlap.
- Regenerated and hash-checked all seven deterministic packages; all three
  submission source bundles independently rebuild to 18-page main and
  18-page supplement PDFs.
- Completed a full detached portable replay through `PUBLIC_REPLAY_PASS`,
  including current-profile simulations, exact certificates, regenerated
  figures, documents, and a self-verifying manifest.
- Best-guess completion toward the round-5 pre-submission revision and
  verification goal: **90%**.  Remaining work is independent final audit,
  manifest closure, immutable publication, and final remote-access sync.

## 2026-08-21 14:10:06 PDT — round-5 final verification checkpoint

- Corrected the final S9 punctuation defect found during adversarial page
  inspection and rebuilt the affected supplement and every derived package.
- Three independent audits found no mathematical, manuscript, PDF, or release
  blocker.  The exact symbolic aggregate, all 21 mutation/regression tests,
  manuscript and stale-claim audits, numerical provenance checks, and PDF
  semantic checks pass.
- Visually inspected all 49 pages across the eight principal PDFs and verified
  the seven deterministic bundles, all submission and specialist mirrors, and
  the full detached public replay ending in `PUBLIC_REPLAY_PASS`.
- Prepared the v1.0.5 immutable snapshot and synchronized the final main TeX
  and bibliography to the local Google Drive mobile-access folder.  No
  external communication or submission was initiated.
- Best-guess completion toward the round-5 pre-submission revision and
  verification goal: **100%**.

## 2026-08-22 07:55:16 PDT — round-6 notation and release-lineage checkpoint

- Accepted the reviewer’s notation objection: component symbols $r_m$ and
  $\ell_m$ are now reserved for the $X_m$ entries, while the complete right
  and left critical vectors are explicitly $r=(r_1,\ldots,r_m,r_Z)^T$ and
  $\ell=(\ell_1,\ldots,\ell_m,\ell_Z)^T$.  The self-contained scaled PDE
  statement, fixed-mass covector terminology, local S9 parameter $\omega$, and explicit scaled cubic
  quotient are also being propagated.
- Independently verified that the existing v1.0.5 annotated tag and release
  are public, that all nine attached release assets match the local hashes,
  and that both the stable concept DOI `10.5281/zenodo.21753404` and the
  version DOI `10.5281/zenodo.22050742` are open and DataCite-Findable.  The
  review’s archival concern is stale.
- Prepared release-facing metadata for a new immutable v1.0.6 snapshot dated
  22 August 2026.  The stable concept DOI remains unchanged; no unminted
  v1.0.6 version DOI is asserted.
- Best-guess completion toward the round-6 pre-submission revision and
  verification goal: **60%**.  Remaining work is exact regression, document
  rebuild and page inspection, package refresh, portable replay, final audits,
  manifest closure, and immutable publication.

## 2026-08-22 08:13:04 PDT — round-6 rebuilt-document checkpoint

- Propagated the full-vector/component distinction through the manuscript,
  supplement, theorem summary, proof skeleton, proof audits, exact verifier,
  and semantic regression gates.  The scaled-family theorem now states the
  physical PDE and Neumann domain directly, and the supplement uses $\omega$
  for its local near-threshold design parameter to avoid both the spatial-mode
  and gauge symbols.
- Rebuilt the 18-page manuscript, 18-page supplement, 3-page theorem summary,
  and 6-page proof skeleton.  Contact-sheet inspection of every page and
  full-resolution inspection of every changed page found no clipping,
  overlap, broken glyph, or ambiguous mathematical line wrap; all fonts are
  embedded.
- All 21 mutation/regression tests, the complete symbolic aggregate,
  manuscript audit, numerical-provenance audits, principal-minor verifier, and
  full PDF semantic audit pass from the exact round-6 sources.  The additional
  review warning about archival metadata was rejected as stale after checking
  the live v1.0.5 release and both existing Zenodo records.
- Best-guess completion toward the round-6 pre-submission revision and
  verification goal: **90%**.  Remaining work is package refresh, detached
  portable replay, independent final audits, manifest closure, mobile sync,
  and immutable v1.0.6 publication.

## 2026-08-22 08:31:13 PDT — round-6 final verification checkpoint

- Three independent final audits found no mathematical, manuscript, PDF, or
  release blocker.  Their residual notation findings were applied: the
  machine-readable certificate now distinguishes the full vector $r$, the
  dimension offset $\nu$, the harmonic scalar `hfrak`, and the scaling matrix
  `Hmat`; the proof skeleton uses one effective-diffusion symbol consistently.
- Rebuilt and hash-checked all seven deterministic bundles, independently
  rebuilt all three submission source ZIPs to 18-page main and 18-page
  supplement PDFs, and completed the final detached public replay through
  `PUBLIC_REPLAY_PASS` using recorded Tectonic 0.16.9, Biber 2.17, and Python
  package versions.
- The complete symbolic aggregate, all 21 mutation/regression tests,
  manuscript and 439-file stale-claim audits, numerical provenance checks,
  embedded-font checks, and full PDF semantic audit pass.  No reaction,
  theorem, endpoint, numerical datum, or nonlinear conclusion changed.
- Best-guess completion toward the round-6 pre-submission revision and
  verification goal: **100%**.  The source is ready for immutable v1.0.6
  publication and author-controlled external audit/submission.

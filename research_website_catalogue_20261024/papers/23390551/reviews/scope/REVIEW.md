# Static source and scope intake — Zenodo 23390551

This is a source-custody and claim-boundary report, not a mathematical PASS, priority certification, publication authorization, or acceptance of archived reviews. The selected scientific claims remain hypotheses for later independent analytic and adversarial review. No submitted executable was imported, built, or run.

## Identity and acquired edition

Frozen queue row 76, work Z-23390550, selects **Off-interval spectral convergence for geometrically consistent discrete dipoles**, Alec Kriebel, DOI **10.5281/zenodo.23390551**, version **1.0**, publication date **15 October 2026**. The manuscript title page independently states that date/version and “Unrefereed preprint.” Author ORCID is https://orcid.org/0009-0001-9320-500X. This is a preprint deposit, not a journal publication.

Fresh public [Zenodo API metadata](https://zenodo.org/api/records/23390551) was retrieved beginning 2026-10-25T03:47:18Z (24 October locally). Its published/done/submitted state, title, creator, version, date, concept record 23390550, and two-file inventory agree with the queue. Record creation is **2026-10-15T09:25:22.728191+00:00** and modification **2026-10-15T09:25:23.405142+00:00**; these administrative timestamps do not replace the manuscript publication date.

Both public assets were freshly downloaded from the API file-content endpoints, with no local fallback used:

| Asset | Bytes | MD5 | SHA-256 |
| --- | ---: | --- | --- |
| dipole_spectrum.pdf | 113063 | 7f55e5f7ac34192211d0e5767935ca7c | 7fc583c50f2d75e08fc008d0b7891a81135fa8c2109af9f33472f2a492784d46 |
| dipole_spectrum_verification.zip | 764472 | af31c1542d5af7fdce96e7424c62048f | 5cbd35e7c4b30d3d7e90a953cffb689b03bc957e60c4aa6905b0a60e38c069d7 |

The selected PDF is 11 pages. Acquisition receipts retain origin/final URL, UTC time, HTTP headers, bytes, MD5 and SHA-256. Queue identity is copied with the frozen queue file's hash in `sources/queue_identity.json`.

## Reader and archive coverage

All 11 pages of the actual published PDF, including proofs and references, were read using its layout-preserving extraction. The actual 34975-byte main TeX was read in full. Rendered published pages 2 and 6 were inspected, including the conjugation in the adjoint-resolvent identity that text extraction can obscure. The complete original abstract is preserved in `ABSTRACT.source.tex` and `ABSTRACT.txt`; the latter changes only TeX typography/math rendering and whitespace, not wording or scope.

The support ZIP was recursively inventoried and safely extracted within the owned ignored source cache. Across both archive layers there are **323 entries**, **170 unique member SHA-256 values**, **one nested ZIP** and **16 hidden entries**. Every member has a name, container, size, CRC, original timestamp, mode, MD5 and SHA-256 in `sources/archive_inventory.json`. Absolute/traversal paths, duplicates and symlinks were checked before extraction; no such unsafe member was found. Every member's permissions are 0644 and were preserved. Binary signature inspection found no extra disguised PDF/archive beyond the listed historical PDF and nested ZIP. The nested archive is 262286 bytes, SHA-256 `dfc0a9c0775af5b205494e56e561cbd27c1519af734b3cb387ad7e06a4b7760d`.

One additional unique actual reader is archived: `history/review01_frozen/output/pdf/dipole_spectrum.pdf`, 112956 bytes, SHA-256 `5368254f4192d7a617bb27b6bbc6454c89e5ddd62ed2fa9c5d617f95442507af`, also 11 pages. It was read completely. Its corresponding historical TeX is repeated byte-identically inside the nested ZIP. Comparing the two unique TeX bodies finds only two changes: the current source explicitly equips full-lattice sequences with the weighted norm making the embedding isometric, and it adds the Anselone–Treuden reference page range. The mathematical statements/proof text otherwise agree. No extra unique PDF appendix, HTML, office document or notebook reader was found.

`reader_map.json` binds these readers and sources. `support_member_map.json` classifies every entry. Historical audit reports, priority reports, verdicts, acceptance documents, narrative conclusions, and expected-result files were kept opaque: their names and hashes are inventory evidence only. Necessary executable support was inspected as source, including the four current verification programs and the four original programs referenced by the replay driver. This permission to inspect program text did not include reading historical judgment documents or accepting program-reported PASS strings. The current verification README was read for its declared limitations.

## Exact claim interface

The principal claim (Theorem 1, published pp. 2–3) uses the intrinsic space H_Ω=L²(Ω;C³) for a **bounded measurable** set Ω and a **fixed κ∈C** during the mesh limit. With g_κ(x)=exp(iκ|x|)/(4π|x|), A_κ is the distributionally differentiated Maxwell volume operator written in the manuscript. The compared operator is **S_κ=A_κ−I/3**. This shift is essential: results for S_κ are not unshifted A_κ eigenvalue claims or material-permittivity claims.

Centers are x_m=a_h+hm with arbitrary translations a_h; cells are x_m+h[−1/2,1/2)³; membership is exactly x_m∈Ω. The matrix uses h³K_κ(x_m−x_n) for distinct occupied centers and **zero 3×3 diagonal blocks**. It is not an integrated-cell kernel, an adjusted polarizability scheme, an anisotropic lattice, or a self-interaction corrected matrix. The representative of Ω matters for center membership even though the continuum volume operator only sees Ω modulo null sets.

The sufficient geometric premise is **|Ω_h Δ Ω|→0**, where Ω_h is precisely that center-selected voxel union. Bounded sets with boundary measure zero, including bounded Lipschitz particles with either boundary-membership convention, are asserted to satisfy it for arbitrary translations. The theorem does not say that every bounded measurable/compact set satisfies it or that it is necessary.

The comparison interval is the **exact closed numerical range J_lat=[Λ_−,Λ_+] of the bounded selfadjoint full static cubic lattice operator**, containing [−1/3,2/3]. No decimal endpoint estimate is substituted. The cited primary source labels the particular 3D endpoint-extremizer locations as numerically suggested; the theorem uses the exact interval definition and form bound instead.

| Claim part | Actual quantifier/topology | Boundary of what is asserted |
| --- | --- | --- |
| Resolvent stability/no pollution | Every compact L⊂(C\J_lat)∩ρ(S_κ); all z∈L and all sufficiently small h; inverse norms bounded uniformly over z and h | No compact set touching J_lat; no h-dependent κ regime; no assertion of full norm-resolvent convergence |
| Spectral points and clusters | Every continuum spectral point outside J_lat is isolated of finite algebraic multiplicity; a disk with closure missing J_lat isolates it | Includes real points outside J_lat as well as nonreal ones; not inside-interval spectral correctness |
| Riesz projections | Embedded in common L²(R³;C³), extended by zero; convergence in operator norm on an isolating contour | No projection comparison between unspecified Hilbert spaces; no promise to preserve individual Jordan block sizes |
| Multiplicity/subspaces | Eventual equal rank, total algebraic multiplicity of the enclosed cluster, both subspace gap directions | Not semisimplicity, individual eigenvector convergence, diagonalizability or a convergence rate |
| Norm bounds | Matrix operator norms uniformly bounded as h→0, using scalar-equivalent h³-weighted norms | Not a computed uniform constant for varying frequency or unbounded particle diameter |

The stated empty occupied set convention is a zero-dimensional matrix. Zero-measure Ω, changing representatives on null sets, empty masks, zero frequency, complex frequencies, and contours approaching J_lat are boundary cases that later scientific reviewers should test against the exact quantifiers. This intake records their interfaces; it does not certify those cases.

## Proof and support mechanisms to be reviewed

The manuscript's proof route is explicitly split into three parts. Lemma 2 establishes strong convergence of the static full-lattice embedding using smooth compactly supported test fields, radial cubic cancellation, a near-cutoff O(δ) estimate, translated Riemann sums away from the cutoff, and a whole-space tail estimate. This smoothness is a dense proof core, not an extra smoothness assumption on every L² eigenfield. Multiplication masks then converge strongly under (G).

Lemma 3 identifies the **actual sampled dynamic correction** with an integral kernel on cell products, omitted on same-cell blocks. R_κ=K_κ−K_0 is O(1/r) on a bounded physical difference set for fixed κ. The claimed near-diagonal squared-kernel mass is O(δ+h), and the far part uses bounded uniform continuity and changing-mask volume control. The order is first h→0, then δ→0; no rate coupling between these parameters is asserted. The desired limit is Hilbert–Schmidt, hence operator-norm, convergence of the dynamic correction.

Lemma 4 supplies a self-contained compact-factor resolvent/Riesz argument for strong selfadjoint static convergence and norm convergence of compact corrections with spectra in a common real interval. It uses strong convergence of **adjoint** resolvents for the compact factor on the left, not strong convergence alone. Infinite zero extensions are kept outside the contours because 0∈J_lat. Independent scientific reviewers must assess these mechanisms, including the lattice-bound interface, the tail/near-diagonal estimates, analytic Fredholm continuation and the finite-rank projection arguments.

The supplementary Theorem 5 (pp. 7–9) is different in scope. It claims a compact positive-volume empty-interior support, at fixed real κ=1/10000 in unit-ball-scaled coordinates, with an isolated nonreal continuum eigenvalue, while **all rational meshes h=1/n, a_h=0** see only one isolated null anchor and give 3×3 zero matrices. Its proof first works intrinsically on the ball, with a rank-three static constant-field mode, spectral gap 1/15 and a trace-imaginary-part perturbation estimate. It then removes rational points in an explicit nested small-volume sequence and uses continuum mask spectral persistence to select a sufficiently large **existential finite index**. No effective support index or numerical eigenvalue location is supplied. The example fails (G), and is not a regular-particle counterexample or necessity theorem.

Finite support programs contain symbolic/rational algebra, finite cubic-shell checks, ball perturbation constants, and floating diagnostic matrix/refinement/Riesz calculations. Their static content is mapped to the proof components above. Finite algebra cannot certify infinite-dimensional completeness, mask limits, Fredholm continuation, or the existential index. No code/data reproduction result is produced by this assignment, and no archived finite count or PASS is treated as new evidence.

## Primary source scope and access

Actual full source PDFs were acquired for ten primary references; receipts and specific body coverage are in `sources/primary_acquisition_receipts.json` and `sources/primary_read_ledger.json`. Full source acquisition does not imply every unrelated page was read.

- **Original problem:** Costabel's complete OWR contribution, printed pp. 2580–2582, was read from the actual [publisher report](https://ems.press/content/serial-article-files/46980). It uses the same A_κ/K_κ/shifted matrix and records prior static/dynamic stability and the observed nonreal off-interval spectral behavior. The 2026 condition (G) is an explicit additional sufficient scope, not the text of the 2022 question. Neither this report nor a 2026 bounded search licenses a current worldwide-openness statement.
- **Imported lattice input:** The actual [CDN arXiv v3](https://arxiv.org/pdf/2302.13159v3) theorem/hypothesis/proof chain was read, including quadratic homogeneous cancellation, the Ewald bounded-symbol result, matrix-valued extension, Proposition 3.15 and the 3D numerical qualification. The d=3 kernel and shift match the manuscript's conventions. This is the central imported mathematical interface.
- **Classical spectral credit:** Actual bodies of relevant statements in [Anselone–Palmer](https://msp.org/pjm/1968/25-3/pjm-v25-n3-p02-p.pdf), [Anselone–Treuden](https://msp.org/pjm/1985/120-2/pjm-v120-n2-p01-p.pdf), and [Descloux–Nassif–Rappaz](https://www.numdam.org/article/M2AN_1978__12_2_97_0.pdf) were read with their convergence/compactness hypotheses. Their abstract results do not by themselves establish consistency of the raw singular sampled matrix. The paper gives its own factorization argument and credits them as classical machinery.
- **Earlier DDA consistency/continuity:** Actual YMH smoothness/cubic-cancellation and inverse-assumption passages, its full 2015 erratum, and YM §IX/footnote 22 were read from author-hosted PDFs. The comparison retains their hypotheses and point-value sensitivity, and does not rebrand consistency or geometry sensitivity as first discoveries.
- **Announced dynamic work:** The complete primary IMU report and Hilbert manuscript reference 3 were read. They document the named 2022/2023 time-harmonic work in preparation. Its full theorem/proof body was not acquired in this bounded intake, so overlap/priority cannot be certified. No conclusion about its existence, publication or coverage follows from this gap.
- **Rahola:** A fresh official full-PDF request returned HTTP 403. No full theorem body was acquired or relied upon. The paper's historical sphere-spectrum credit must remain; this intake cannot narrow that work's coverage from an abstract.
- **Other contextual bibliography:** Budko–Samokhin, Zhou, Ammari–Li–Zou, Ammari–Millien and Tzarouchis et al. are cited as prior continuum/sphere context by the manuscript. Their theorem bodies were not separately acquired/read here, and none is being used by this intake to replace the manuscript's own ball proof or certify novelty. The unnamed forward-citing thesis mentioned in the paper is not identified in the published references; its full contents are an explicit uncovered interface, not negative prior-art evidence.

There is no unresolved full-body access gap at the imported CDN static-lattice theorem interface. The gaps above prohibit priority/exhaustiveness claims; independent proof assessment remains entirely pending.

## Conditional public copy and disposition boundary

`PUBLIC_CANDIDATE.md` and `public_candidate.json` provide restrained copy for a possible later page. They preserve the original abstract and date/version, exact off-interval/fixed-frequency/geometric qualification, prior credit, unrefereed status, extensive AI-use disclosure, direct DOI/PDF/support links and passive professional collaboration invitation. `follow_up` is **null**: no sufficiently supported research question is proposed. There is no firstness, journal-acceptance, current-openness, necessity or universal-compact-support claim.

The strongest verified result of this assignment is a fresh checksum-bound identity/custody record, complete actual-reader intake, and a checkable mapping of the published scope and source interfaces. Scientific analytic/adversarial validation and the root publication/defer disposition are later work. No manuscript repair, spreadsheet/site/UI action, outreach, Git action or release was performed.

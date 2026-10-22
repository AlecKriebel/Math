# Source and dependency audit

Checked 2026-10-10 UTC. No novelty or exhaustive worldwide-status claim is made.

## Accepted scope and historical inspection

Problem 30004486 / OWR-1703869-006 remains OPEN. The independent [mathematical audit](MATHEMATICAL_AUDIT.md) accepts only the bounded theorem in [PROOF.md](PROOF.md), with no substantive correction. The complete mathematical proof is unchanged. This source review distinguishes imported results from deductions. [SOURCE_METADATA.json](SOURCE_METADATA.json) records exact public source identities and historical inspection coverage.

Edition preparation rechecked frozen input bytes and publication integrity without new scholarly-source retrieval, source-text inspection, literature search or mathematical-computation reruns. Manuscript and audit are AI-assisted and unrefereed; acceptance is not external human peer review, journal acceptance or formal proof-assistant certification.

## Primary model source

Christof Melcher and Zisis N. Sakellaris, *Curvature stabilized skyrmions with angular momentum*, arXiv:1902.04881v2, 1 May 2019; Letters in Mathematical Physics 109 (2019), 2291–2304.

- https://arxiv.org/abs/1902.04881
- https://arxiv.org/pdf/1902.04881
- https://doi.org/10.1007/s11005-019-01188-6
- PDF SHA256: `02b8f5bc70cc57fe3a585a111a42cb28dd60681b13c162eb93c4b88ecf6701cd`
- Bytes: 196,034

Read model, target, first variations, equivariance, elliptical-distortion calculation, competitor construction and attainment text on PDF pp.1–9, plus bibliography. The historical author inspection covered pp.2,4,5,6,7,8,9 visually. The independent mathematical audit read the full paper and bibliography and visually inspected every PDF page 1-9, independently rendering pp.1 and 3. The standard existence theorem, strict competitor bound, and smooth minimizing representative are credited inputs. The cited harmonic-map regularity literature was not independently re-proved, and the packet does not silently promote non-equivariance to nonzero frequency.

The source PDF, extracted text and rendered images are not distributed. During the historical author work, arXiv metadata was opened again and identified v2 as the current revision. This is a source-version check, not a certificate that no other paper solves the problem.

## Original report

Christof Melcher, joint work with Zisis N. Sakellaris, *Emergent spin-orbit coupling in a spherical magnet*, Oberwolfach Report 22/2020, printed pp.1168–1171.

- https://ems.press/content/serial-article-files/46860
- https://doi.org/10.4171/OWR/2020/22
- PDF SHA256: `7b625ed2fd74f0d0dd3c5ad1c37090012ebdfd91ed9e5c86c06b87f7622fd5bc`
- Bytes: 795,156

The historical author work read the full contribution as extracted text, including the exact target paragraph and bibliography. The independent audit read the complete contribution and bibliography and independently rendered and visually inspected PDF pp.31–33. The report's Poisson-bracket presentation uses a different paired sign convention from [MS]; the proof explicitly fixes the physical equation and positive rotation direction from [MS].

## Quantization dependency and exact inspection boundary

H. Brezis, J.-M. Coron, and E. H. Lieb, *Harmonic Maps with Defects*, Communications in Mathematical Physics 107 (1986), 649–705, DOI 10.1007/BF01205490.

- Author-hosted PDF: https://sites.math.rutgers.edu/~brezis/PUBlications/112-Journal.pdf
- PDF SHA256: `495fc13f3c13c95ff3463d150887642ad2a30c2af13d5f3b81142b29eb247858`
- Bytes: 5,308,470

During the historical author work, the full 58-page PDF was downloaded. The author and independent auditor each read and visually inspected PDF pp.51–54 (printed pp.699–702): Theorem E.1, its three lemmas and proof, and **Corollary E.5** for maps from SN to SN. The theorem applies to arbitrary bounded W1,N sequences with almost-everywhere convergence, not only harmonic or Palais–Smale sequences. Its Jacobian defects are finitely many integer-weighted atoms. The separately numbered Theorem E.5 later on the same printed p.702 is not the dependency. No full audit of the rest of the 58-page paper is claimed.

The energy cost of each atom is derived from |Jac m|≤|grad m|²/2 and weak lower semicontinuity. Therefore the proof does not require an uninspected extra energy-quantization statement or the Lions lemma cited by [MS]. Degree integrality and strong-H1 continuity remain standard background conventions; the proof states them explicitly.

An earlier ICTP mirror returned HTTP 502 to the local retrieval. A Project Euclid request returned 1,158 bytes of HTML rather than a PDF. Both outcomes are preserved as public historical retrieval metadata in [SOURCE_METADATA.json](SOURCE_METADATA.json); neither counts as a successfully inspected source. The author-hosted PDF subsequently succeeded. The HTML response is not distributed.

## What is derived here

The proof derives the H1 momentum-rank lemma, including weak transport equivariance and endpoint quantization; finite-dimensional exact momentum corrections using smooth pointwise rotations; unique weak variational multipliers and axial alignment; constraint continuity and strong compactness of minimizing families below 8π; uniform upper supports; local semiconcavity; and the exact one-sided extremal-multiplier formulas. It then states precisely why none supplies the missing nonzero slope.

## Bounded current checking

Searches included the exact article and the spherical energy/frequency question. The recorded historical checking covered the exact target and primary model. A 2025 paper on symmetry-governed dynamics under field pulses appeared as a neighboring source, but its planar, driven model does not replace this spherical constrained problem. Search snippets and catalogs were not used as proof. Initial supplementary discovery lookups are not all independently saved; the source and retrieval ledger does not claim a complete global search log.

No exact later replacement theorem was identified in this bounded check. This is a limited research finding, not a theorem that the problem remains open throughout the literature.

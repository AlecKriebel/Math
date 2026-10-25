# Source snapshot and provenance

Snapshot opened on 27 July 2026, re-audited on 16 August 2026, and extended
for the concurrent-work revision on 18 August 2026
(America/Los_Angeles).

## Supplied exact verifier

- Original supplied filename: `verify_exceptional_ybe_d4.py`.
- Size: 1,552 bytes
- Local modification time: 2026-07-27 17:53:50 PDT
- SHA-256:
  `df5ccbc8807c20a2f782762681100e3ad06cb95a750b7e052839584006fe3677`
- Repository copy: `verify_supplied_original.py`, retained byte for byte.

`verify_supplied.py` is the supported hardened adaptation. It rejects
optimized Python and uses explicit scientific checks; it is intentionally not
byte-identical to the supplied file.

The supplied file verifies only the final witness.  It does not contain or
reconstruct the numerical search that reportedly discovered the five-word
support.

## 2026 classification preprint

- Gandalf Lechner, *The classification problem for unitary R-Matrices with two
  eigenvalues*, arXiv:2603.20158v1 [math.QA].
- Submitted 20 March 2026 at 17:34:47 UTC.
- <https://arxiv.org/abs/2603.20158v1>
- <https://arxiv.org/html/2603.20158v1>

The audit uses version 1 because that is the version specified in the research
question.

## 2012/2013 localization paper

- César Galindo, Seung-Moon Hong, and Eric C. Rowell, *Generalized and
  Quasi-Localizations of Braid Group Representations*, International
  Mathematics Research Notices 2013(3), 693--731.
- Advance access publication: 14 February 2012.
- DOI: <https://doi.org/10.1093/imrn/rnr269>
- Author-supplied local PDF used during the audit; not redistributed.
- Size: 335,860 bytes.
- SHA-256:
  `ce68f021303048dffb4badd498291865e56c860a309901d6463a18b5d938cdf7`.

The local PDF is used for research but is not redistributed in this repository.

## Rowell--Wang localization paper

- Eric C. Rowell and Zhenghan Wang, *Localization of Unitary Braid Group
  Representations*, Communications in Mathematical Physics **311** (2012),
  595--615.
- DOI: <https://doi.org/10.1007/s00220-011-1386-7>
- arXiv source: <https://arxiv.org/abs/1009.0241v2>
- Author-hosted journal PDF checked during the audit; not redistributed.
- SHA-256 of the checked journal PDF:
  `4049ea09174d55596278dc7694b0955f887a07b94cb34f88d7f170e97516adef`.

The published and arXiv texts were checked to bind the foundational
localization framework: the statement is published Conjecture 3.1 (p. 601)
and arXiv-v2 Conjecture 4.1. No local copy is redistributed.

## Final consolidated review input

On 16 August 2026 the author supplied a 24,165-byte consolidated text containing
two additional model reviews. Its SHA-256 is
`9670856928cee77362e804df048b6f4eaba5539b599ca9b4b02fdbca09a94697`.
The input is not redistributed; the itemized, source-checked disposition is
recorded in `REVIEW_ADJUDICATION_v1.1.2.md`.

## Version 1.1.3 correction review

On 16 August 2026 the author supplied a further review directly in the task
conversation. It was not provided as a standalone file, so no artificial file
hash is claimed. Its source-checked disposition is recorded in
`CORRECTION_AUDIT_v1.1.3.md`.

## Galindo--Rowell concurrent preprint

- C. Galindo and E. C. Rowell, *Unitary Yang--Baxter Operators: Towards a
  Classification*, arXiv:2608.16865v1 [math.QA].
- Official record: <https://arxiv.org/abs/2608.16865v1>.
- Submitted: 2026-08-17 17:47:15 UTC.
- Supplied source archive: `arXiv-2608.16865v1.tar.gz`, 62,866 bytes.
- SHA-256:
  `b7bc3fb2d1906140247e7643d82fda2bb02ee6cc53e6367956a087fa96d814ab`.
- The archive contains only regular, safe paths. Its `main.tex` is SHA-256
  `069fd53e0be504c6e5369b8646e63e42992971ac187b4571c6432c0111534aff`.

Section 13 was read literally for the independent encoding of `P_Z`, `P_X`,
`U`, `V`, and `R_GR`. The source does not state the reported earlier private
circulation; that fact is attributed as a report and supported by separately
preserved private records, not by the arXiv text. Neither the supplied archive
nor any private correspondence is redistributed in the public source package.

## Quaternionic braid source

- Eric C. Rowell, *A quaternionic braid representation (after Goldschmidt and
  Jones)*, Quantum Topology **2** (2011), 173--182.
- DOI: <https://doi.org/10.4171/QT/18>.
- The published article was inspected directly for Theorem 3.1 (finite image),
  Lemma 3.2 (the `H_n(3,6)` braid-generated subalgebra), Lemma 3.3 (finiteness
  of the generated group), and the normal basis on p. 176.

The audit corrects a locator in Galindo--Rowell v1: its reference to Rowell
“Lemma 3.4” corresponds to published Lemma 3.2. The source PDF is not
redistributed.

## Enhanced-Yang--Baxter and topological sources

- V. G. Turaev, *The Yang--Baxter equation and invariants of links*, Invent.
  Math. **92** (1988), 527--553,
  <https://doi.org/10.1007/BF01393746>. The audited original typeset scan had
  SHA-256
  `d59c4f4de43d62a21a7ce07c261e1bd3ab9ed2c1cad7af74a5ae2bf5e0c148d8`.
- W. B. R. Lickorish and K. C. Millett, *Some evaluations of link
  polynomials*, Comment. Math. Helv. **61** (1986), 349--359,
  <https://doi.org/10.1007/BF02621920>. The audited original typeset scan had
  SHA-256
  `a5acc50000f17616a1af076eac16769505272ab41ab4eec40a959c74e9cdb437`.

The exact convention and sign crosswalk is recorded in
`TOPOLOGICAL_NORMALIZATION_AUDIT_v1.2.0.md`. The PDFs are research inputs and
are not redistributed.

## Final global-strengthening program

On 18 August 2026 the author supplied a 35,753-byte final strengthening
program. Its SHA-256 is
`d5ceba1b691b9da802b2efa1d0d2e69e10950afda3f6cf9d8508bd68ac441010`.
The input is not redistributed. Its source-checked disposition is recorded in
`GLOBAL_STRENGTHENING_ADJUDICATION_v1.2.0.md`.

## Discovery provenance

The formula was supplied with the explanation that a structured numerical
search in a real Pauli--Clifford basis found the five words, after which the
coefficients were recognized exactly.  The original search program, random
seeds, and raw numerical trace were not retained.  No claim of exhaustive
search, uniqueness, or reproducible discovery is made.

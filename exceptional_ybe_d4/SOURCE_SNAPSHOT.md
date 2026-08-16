# Source snapshot and provenance

Snapshot opened on 27 July 2026 and re-audited on 16 August 2026
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

## Final consolidated review input

On 16 August 2026 the author supplied a 24,165-byte consolidated text containing
two additional model reviews. Its SHA-256 is
`9670856928cee77362e804df048b6f4eaba5539b599ca9b4b02fdbca09a94697`.
The input is not redistributed; the itemized, source-checked disposition is
recorded in `REVIEW_ADJUDICATION_v1.1.2.md`.

## Discovery provenance

The formula was supplied with the explanation that a structured numerical
search in a real Pauli--Clifford basis found the five words, after which the
coefficients were recognized exactly.  The original search program, random
seeds, and raw numerical trace were not retained.  No claim of exhaustive
search, uniqueness, or reproducible discovery is made.

# A note on Γ-supercyclicity of dissipative composition operators

**Alec Kriebel · version 1.0.0 · 23 September 2026 · attributed, unrefereed research note**

- [Read the five-page note](output/pdf/note.pdf) or visit the [paper website](https://aleckriebel.github.io/Math/papers/gamma-supercyclicity/).
- [LaTeX source archive](output/note-source.zip).
- [Zenodo upload kit](output/zenodo-upload-kit.zip), including the PDF, source archive, structured metadata, copy-and-paste fields, and [upload instructions](zenodo/UPLOAD.md). No deposition or DOI has been created.

The note gives an affirmative answer in the original separable setting. Its contribution is to make an application of earlier theorems explicit; neither the scalar criterion nor the amplification mechanism is claimed as new. The user authorized this narrower publication scope after the original priority audit.

This effort checks the candidate associated by the user with [OWR-14298367-006](https://www.unsolvedmath.com/problems/OWR-14298367-006). The exact question was recovered independently in Emma D'Aniello's contribution (joint work with Martina Maiuriello), printed p.1083 of [Oberwolfach Report 19/2024](https://doi.org/10.4171/OWR/2024/19). The catalog page itself was inaccessible during this audit.

For every fixed subset Gamma of C, the bounded-distortion dissipative composition operator and its associated bilateral weighted shift have the same Gamma-supercyclicity. The theorem needs the report's standing assumption of a separable complex Lp space, with 1 <= p < infinity. It does not assert that every such operator is supercyclic.

The scalar criterion was already known. Moreover, the Banach-valued amplification follows by a short specialization and dense-range factor argument from Abbar and Kuznetsova's [2020 preprint, published in 2021](https://arxiv.org/abs/2005.11230). This is a concrete antecedent, not merely a keyword match. We did not locate a publication explicitly spelling out the answer to the 2024 question, so this audit does not assert that the question had already been explicitly answered.

## Read first

- [Manuscript](manuscript/note.tex): a self-contained direct proof and a deduction from the prior translation theorem.
- [Manuscript proof review](audit/note-proof-review.md) and [attribution review](audit/note-attribution-review.md).
- [Verification report](audit/VERIFICATION_REPORT.md): verdict, scope, corrections, and the historical publication decision.
- [Independent proof](audit/independent-derivation.md): self-contained finite-tail and Baire argument.
- [Priority audit](audit/priority-audit.md) and [independently checked prior-theorem deduction](audit/priority-derivation-independent.md).
- [Candidate proof audit](audit/proof-adversary.md) and [original-source/conjugacy check](audit/source-match.md).
- [Finite exact checks](verification/README.md), with a standard-library Python script. These do not constitute formal verification of the infinite-dimensional theorem.
- [Research log](RESEARCH_LOG.md) and [source inventory](sources/README.md).

## Reproduce the materials

From this directory, run `python3 build_package.py --compile --deploy-site`. This requires Python 3 and Tectonic. The script compiles the manuscript, creates archives with fixed member timestamps, checks their contents, and copies the paper page to the repository's Pages directory. It performs no network upload or git operation. The self-contained source archive can also be compiled separately; see [its README](manuscript/README.md).

The paper's proof is analytic. The optional finite checks can be run with `python3 verification/verify.py`; they check identities and examples, not the universal theorem. No supplemental paper is required to follow the argument.

`SHA256SUMS` covers the note, package, sources, metadata, and audit records in this effort, excluding itself and local raw source downloads. The downloadable website has a separate manifest. Licensing: [CC BY 4.0 for the note and accompanying text; MIT for Python code](LICENSES.md).

Original audit date: 22 September 2026, America/Los_Angeles (23 September UTC). Publication package: 23 September 2026. This is AI-assisted work, not external peer review or a proof-assistant certificate. No individual was contacted. Author: Alec Kriebel, [ORCID 0009-0001-9320-500X](https://orcid.org/0009-0001-9320-500X).

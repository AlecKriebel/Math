# Zenodo copy-and-paste upload guide

This is a prepared manual upload package. No deposit or DOI has been created. No GitHub release is needed.

1. Extract `zenodo-upload-kit.zip`.
2. Create a new upload at [Zenodo](https://zenodo.org/uploads/new).
3. Upload `paper.pdf` and `source-and-verification.zip` as the two research files. Optionally also upload `metadata.json` and `SHA256SUMS`. The outer upload-kit ZIP is only a convenience envelope; the PDF should be visible as its own file.
4. Use the fields below. Review the record before publishing. If depositing on a later date, use the actual first-publication date of this version as appropriate. Zenodo can assign the DOI; do not mark the source report's DOI as this paper's DOI.
5. After publication, record the assigned DOI in `CITATION.cff`, the website, and any later version's metadata. No DOI placeholder has been inserted into the present paper.

## Resource type

Publication → Preprint

## Title

The odd-part ratio under slow variation: a note on the printed Hilberdink problem

## Creator

- Family name: Kriebel
- Given name: Alec
- ORCID: 0009-0001-9320-500X
- Affiliation: Independent researcher

## Publication date and version

2026-09-23; version 1.0.0

## Description — paste the following

For every nonzero nonnegative multiplicative function f whose summatory function F is slowly varying, the odd-part ratio F2(x)/F(x) converges to the reciprocal of the unweighted local sum sum(k>=0) f(2^k), with reciprocal infinity interpreted as zero. A short monotonicity proof covers finite and infinite local sums and bounded summatory functions.

This answers the existence question under the slow-variation hypothesis printed in Hilberdink's Problem 3 in Oberwolfach Report 51/2017 and catalogued as OWR-15956-012. The source's accompanying weighted numerical prediction is incompatible with that hypothesis: f(n)=1/n gives actual limit 1/2, whereas that prediction gives 3/4. The possible intended index-one regular-variation problem is not resolved here.

The deposit includes a three-page paper, editable LaTeX, exact finite-check Python code, independent AI proof audits, a source audit, and a bounded priority-search record. No exact earlier resolution was found in the searched literature; originality is not certified, and limitations in full-text access are recorded. Finite computation supplements the analytic proof and is not formal proof-assistant verification.

## License and access

Open access. Creative Commons Attribution 4.0 International (CC BY 4.0) for text. The included Python and website code is MIT-licensed; this exception is documented in LICENSES.md.

## Keywords

multiplicative functions; slow variation; odd-part ratio; Euler factor; Hilberdink problem; OWR-15956-012

## Notes

Unrefereed preprint. Prepared from an AI-generated candidate supplied by the author, with OpenAI Codex assistance and separate AI audit agents. No external human referee was consulted. This record does not claim a resolution of the possible intended index-one formulation or certified originality.

## Related works

- References: https://doi.org/10.4171/OWR/2017/51
- References: https://doi.org/10.4153/CMB-2003-046-5
- References: https://www.unsolvedmath.com/problems/OWR-15956-012
- Described by: https://aleckriebel.github.io/Math/papers/odd-part-slow-variation/
- Supplemented by: https://github.com/AlecKriebel/Math/tree/main/owr_15956_012_slow_variation

`metadata.json` contains the same description and bibliographic references in Zenodo deposition metadata format. It is a field reference, not a claim that the website supports JSON import. For the deposition API it belongs under the top-level `metadata` key. Metadata fields were checked against [Zenodo's official API documentation](https://developers.zenodo.org/) on 23 September 2026.

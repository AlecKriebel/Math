# arXiv submission metadata

Use the arXiv source archive generated in `submission/`. It contains only the
self-contained `main.tex`; do not upload the locally generated PDF. Verify it
first with `(cd submission && shasum -a 256 -c ARXIV_SHA256SUMS)`.

- Title: `An exceptional four-dimensional unitary Hecke Yang-Baxter operator`
- Authors: `Alec Kriebel`
- Primary category: `math.QA`
- Cross-list: `math.RT`
- Optional cross-list: request `quant-ph` only if the interface permits it and
  its endorsement/moderation requirements are met; the present paper makes no
  physical-implementation claim, so acceptance of this cross-list is uncertain
- MSC class: `20C08 (Primary); 20F36, 16T25, 81R50 (Secondary)`
- License: choose the arXiv license deliberately; CC BY 4.0 matches the
  manuscript license in this package
- Journal reference: leave blank until journal publication
- DOI: leave blank; the Zenodo supporting-record DOI does not belong here
- ORCID: link `0009-0001-9320-500X` in the author's arXiv account

Comments (fill from the reserved DOI before Zenodo publication, then use after
the record is published):

```text
12 pages. Exact verification package: https://doi.org/[ZENODO VERSION DOI].
```

Replace the bracketed field with the actual fresh reserved version DOI. The abstract
in `main.tex` is within arXiv's 1,920-character limit. Copy it as plain ASCII
metadata and inspect arXiv's generated PDF page by page before submission.

Significant generative-AI use is disclosed in the manuscript. The author must
personally complete any category endorsement workflow. No endorsement request
or external contact was made while preparing this package.

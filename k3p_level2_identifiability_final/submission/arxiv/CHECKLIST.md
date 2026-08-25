# arXiv source-staging checklist

Official instructions:

- <https://info.arxiv.org/help/submit_tex.html>
- <https://info.arxiv.org/help/00README.html>

Rules re-checked 2026-08-25.

- [x] The preprint wrapper is compact and does not use referee/double spacing.
- [x] The wrapper has a fixed date rather than `\today`.
- [x] The source allowlist includes the toplevel TeX file, every included
  canonical section, shared macros/abstract, and the BibTeX database.
- [x] `00README.json` selects `pdflatex`, TeX Live 2025, and one toplevel file.
- [x] The source manifest excludes generated PDFs, auxiliary files, hidden
  files, cover letters, journal wrappers/templates, and unrelated material.
- [x] The package relies only on standard TeX Live packages and carries its
  custom macros.
- [ ] Resolve every `@@TOKEN@@` from author-confirmed information.
- [ ] Choose and confirm the primary category and any cross-list categories.
- [ ] Choose the arXiv license in the author-controlled submission flow; no
  license is inferred here.
- [ ] Deposit the exact archive in Zenodo, verify its DOI, and replace the DOI
  token in source and metadata.
- [ ] Decide whether the reader supplement is represented only by the Zenodo
  record or should be added as a clean ancillary file; do not add a generated
  PDF to the TeX source bundle by accident.
- [ ] Materialize the allowlisted staging directory and verify there are no
  unused files, hidden paths, build products, journal templates, or referee
  correspondence.
- [ ] Compile with the arXiv-supported TeX Live version, inspect the generated
  PDF, and verify bibliography processing.
- [ ] Confirm author approval for public posting and review all live metadata
  before the human author submits.

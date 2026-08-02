# Version 2 specialist audit packet

Start with the concise [problem/answer and theorem statement](ONE_PAGE_STATEMENT.md).
The rendered one-page handout is `specialist_audit_one_page.pdf`.
The fully explicit audit-ready statements, including all twenty family
formulas, are in [THEOREMS.md](THEOREMS.md).

For an adversarial review, use [AUDIT_CHECKLIST.md](AUDIT_CHECKLIST.md), which
maps likely failure modes to exact certificates and explicitly lists claims
that are out of scope.

Complete source pointers:

- Version 2 manuscript: [`../manuscript_v2_draft/MANUSCRIPT_V2.md`](../manuscript_v2_draft/MANUSCRIPT_V2.md)
- Complete directed rate table: [`../manuscript_v2_draft/rates.csv`](../manuscript_v2_draft/rates.csv)
- Exact family theorem and matrix: [`../family/README.md`](../family/README.md)
- Independent audit: [`../audit_v2/AUDIT.md`](../audit_v2/AUDIT.md)

One-command exact replay from the repository root:

```sh
.venv/bin/python weakly_reversible_continuum_no_common_factor/manuscript_v2_draft/verify_v2_claims.py
```

The optional PDF rebuild script is `build_one_page_pdf.py`; it requires the
local Python packages `reportlab` and `pypdf` and writes only the handout in
this directory.

Repository-wide Zenodo concept DOI: **10.5281/zenodo.21753404**. It groups
unrelated releases from the `AlecKriebel/Math` monorepo and is **not** an
all-versions DOI specific to this paper. Citations to Version 2 should use its
version-specific DOI, which remains pending until the GitHub Version 2
release triggers the automatic Zenodo archive. This packet neither publishes
anything nor prepares or initiates external communication.

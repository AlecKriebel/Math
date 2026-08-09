# Research log: archive visibility and priority refresh

## 2026-08-09 10:59 PDT

- Started from commit `8a6039ad` on the fetched `origin/main` history in the
  existing dedicated clean site-maintenance worktree.
- Identified the three Discovery entries in the public Archive and provenance
  section as Discoveries 03, 05, and 06.
- Identified four sitemap-listed HTML archive destinations:
  `unipotent-three-point`, `symmetric-keller-and-vanishing`,
  `full-symmetric-monodromy`, and `explicit-vanishing-counterexample`.
  Discovery 05 is a source-only archive and has no separate Pages route.
- Confirmed that the gamma-theta research workstream and all four archive
  destinations are present in `docs/sitemap.xml`.

## 2026-08-09 11:01 PDT

- Rechecked the Cassidy, Thompson, and Mikhail Szh primary commit timestamps
  and conclusions recorded in the Discovery 03 audit.
- Re-ran exact and variant searches over arXiv, Zenodo, GitHub, and the open
  web for the residual 22/44-variable certificate, `SIC(21)`, `SIC(14)`, and
  the exact 14-variable unipotent map.
- Found no earlier source changing the original priority conclusions.
- Located Roy van Rijn's 28 July 2026 archival `SIC(3)` publication. Recorded
  it as later external supersession of the Discovery 05 and 06 dimension
  headlines, not as earlier priority.
- Removed the homepage Research and Archive sections and all cross-page links
  to the gamma-theta workstream and the four archive destinations while
  preserving their canonical metadata and sitemap entries.
- Updated the individual audit records, source READMEs, and the two applicable
  archive landing pages with explicit supersession language.

## 2026-08-09 11:04 PDT

- Verified across every HTML file that no anchor targets the gamma-theta
  workstream or any of the four archive page routes.
- Verified that each hidden route occurs exactly once in the sitemap, retains
  a canonical URL, and has no `noindex` directive.
- Validated the sitemap XML, all JSON-LD blocks, route files, and patch
  whitespace.

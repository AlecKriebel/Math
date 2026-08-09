# Research log: credibility and publication-portfolio cleanup

## 2026-08-09 — inventory and scope lock

- Started from fetched `origin/main` commit `cdbf1252` in the dedicated clean
  site-maintenance worktree. The primary checkout contains unrelated work and
  was left untouched.
- Inventoried 107 tracked files under `docs/`, including 28 paper landing
  routes, six research routes, 38 PDFs, redirects, images, checksums, and
  downloadable archives.
- Classified the three cyclic Bell compatibility pages as pure redirect
  stubs with `noindex,follow`; all other paper and research pages are
  substantive and must remain live and indexable.
- Confirmed that the sitemap contains the homepage, 21 paper routes, and six
  research routes. Four substantive unlisted paper routes were missing and
  require restoration: `bimolecular-positive-recurrence`,
  `k3p-theta-trinet-collision`, `lgt-jc69-identifiability`, and
  `s-tc-jc-sharp-boundary`.
- Identified the eight promoted landing pages and their existing PDFs,
  releases, source packages, and review materials. No public route or
  substantive artifact will be deleted or converted into a redirect.
- Verified the author-supplied ORCID `0009-0001-9320-500X` from the committed
  Version 0.3 `CITATION.cff` for the positive-recurrence package. The same
  repository records the research contact `me@aleckriebel.com` and the role
  `Independent Researcher`.
- Confirmed that the current positive-recurrence source package is Version
  0.3 dated 9 August 2026, while its website still presents Version 0.2. The
  website will preserve the Version 0.2 URLs and PDFs while adding distinct
  Version 0.3 PDF URLs and current metadata.
- Confirmed that this repository is a lightweight static GitHub Pages site
  with no `.openai/hosting.json`; no framework, build system, or additional
  hosting target will be introduced.
- Recorded the pre-task workflow count (two tracked workflow files). This
  task will not add or modify CI.

## 2026-08-09 — implementation

- Replaced the homepage with the requested one-page architecture: hero,
  compact research-status notice, six selected papers in two research
  programs, two additional completed papers, specialist review and
  collaboration, AI-assisted methodology, contact, and footer.
- Removed category codes, active-research promotion, manual revision dates,
  dense release controls, and self-disqualifying homepage language.
- Updated the shared stylesheet without adding a framework or build system.
  The design uses flat color, restrained borders, responsive grids, visible
  keyboard focus, and horizontally accessible mobile navigation.
- Standardized the eight promoted landing pages around the Alec Kriebel /
  Independent Researcher identity, research email, verified ORCID, compact
  unrefereed status, professional AI disclosure, canonical citation metadata,
  and a contact section.
- Added Version 0.3 positive-recurrence PDFs at distinct URLs and recorded
  their hashes. The two Version 0.2 PDFs remain byte-for-byte unchanged at
  their original URLs.
- Applied only the shared site-name replacement to the remaining 26 hidden,
  archived, research, and redirect pages; their substantive wording, status,
  links, and artifacts were not changed.
- Restored the four omitted substantive unlisted papers to the sitemap and
  retained the three pure redirect stubs as `noindex,follow` outside it.

## 2026-08-09 14:28 PDT — validation checkpoint

- Parsed all promoted-page and homepage JSON-LD and validated sitemap XML.
- Verified exactly six selected cards and two additional cards, with no
  hidden, archived, or active project advertised on the homepage.
- Resolved local assets and internal anchors across all 35 HTML files.
- Verified every homepage review entry point against its repository object or
  archival release asset and confirmed the ORCID record resolves.
- Served `docs/` locally and received HTTP 200 for all 32 sitemap routes, the
  three cyclic Bell redirect pages, all three historical Bell PDFs, both
  historical recurrence PDFs, and both new Version 0.3 recurrence PDFs.
- Inspected the homepage at 1440px and 390px widths. The six MathJax formulas
  rendered, the selected cards collapsed to one column, navigation remained
  accessible, and no horizontal page overflow occurred.
- Loaded all eight promoted pages at desktop width. Each showed its canonical
  URL, status, contact, ORCID, MathJax output, and no horizontal overflow.
- Confirmed that no public document or artifact was deleted, historical PDF
  hashes remain unchanged, and no CI file was added or modified.

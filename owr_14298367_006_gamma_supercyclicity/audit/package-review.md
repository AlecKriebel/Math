# Independent publication-package review

Reviewed 2026-09-23, approximately 13:56–14:03 UTC. This is an independent AI
package and consistency review, not external peer review or a new priority
finding. No manuscript, package, build script, or website file was edited.

## Final verdict

**PASS for the publication package.** The paper, regenerated archives,
package-specific hashes, local Pages copies, and manual-upload instructions
passed the checks below. No unresolved package blocker remains.

The first inspection found that `CITATION.cff` declared top-level
`type: article`, whereas the
[official CFF 1.2.0 schema](https://raw.githubusercontent.com/citation-file-format/citation-file-format/1.2.0/schema.json)
allows only `dataset` or `software` at that position. The primary agent
replaced it with an appropriate `CITATION.bib` research-note entry and rebuilt
the archives and site copies. I independently verified that the old CFF is
absent from the source folder, expanded kit, both archives, and nested source
ZIP. The BibTeX entry was successfully processed in an isolated test document
using Tectonic and BibTeX. Its title, author, year, version, URL, and attribution
are consistent with the note.

Public availability is pending, separately from package QA: read-only requests for the live page,
PDF, source ZIP, upload-kit ZIP, and checksums all returned HTTP 404 during
this review. The local `docs/papers/gamma-supercyclicity` publication directory
is internally consistent. A successful later deployment must be checked
separately before claiming the site is live.

## Checks performed

- Opened and extracted text from the five-page PDF; independently rendered
  and visually inspected all five pages. No clipped equations, overlapping
  text, missing glyphs, broken references, or other material layout defect
  was found. PDF title and author match the note; it contains no JavaScript,
  encryption, or form fields.
- Tested every member's CRC in both ZIPs and the nested source ZIP; checked
  unique member names and absence of absolute or parent-traversal paths.
  All archive members equal the corresponding current files byte for byte.
- The source ZIP contains exactly `CITATION.bib`, `LICENSES.md`, `README.md`,
  and `note.tex`. The outer kit contains those two ancillary files plus
  `COPYPASTE.md`, `SHA256SUMS.txt`, `UPLOAD.md`, `metadata-for-api.json`,
  `metadata.json`, `note-source.zip`, and `paper.pdf`. No third-party full
  text, downloaded paper, internal audit transcript, or numerical verifier
  is included. The self-contained TeX has an embedded bibliography and no
  external figure or data dependency.
- Recomputed every listed SHA-256 value in the regenerated upload payload
  manifest (2 entries), generated site manifest (5), and local Pages manifest
  (5). All passed. The original folder manifest's 15 entries passed the first
  inspection; subsequent README editing made that old checkpoint manifest
  stale. Refreshing the root manifest after this review is written, and checking
  it before commit, are explicitly assigned to the primary agent. The final
  root-manifest check is excluded from this package verdict.
- All six generated site files equal the corresponding local Pages files.
  Source HTML and CSS equal their generated copies; downloadable files
  equal their originals. Every relative file link and local fragment in
  the HTML resolves within the local publication directory.
- Parsed both Zenodo JSON files. `metadata-for-api.json` is exactly the
  `{ "metadata": ... }` wrapper of `metadata.json`; `.zenodo.json` agrees.
  The copy/paste description equals the JSON description. Author, ORCID,
  title, version, date, license, and URLs agree across the publication
  materials. There is no assigned or reserved DOI field for this note.
  All six related identifiers have relation `cites`, so bibliography DOIs
  are not represented as this note's DOI.
- The PDF, source README, website, and Zenodo description consistently
  retain the separable complex finite-p setting and attribute the older
  scalar criterion and amplification mechanism to Abbar and
  Abbar–Kuznetsova. They describe an explicit application to the reported
  question, not a new criterion or an established priority claim. AI
  assistance and unrefereed status remain visible.
- `UPLOAD.md` clearly identifies the two intended deposit files, keeps
  the readable PDF separate from the outer convenience kit, supplies
  copy/paste fields, explains that no DOI exists yet, and warns against
  an unintended duplicate deposit through a GitHub release. Its DOI
  reservation/publication directions agree with the current official
  [upload guide](https://help.zenodo.org/docs/deposit/create-new-upload/)
  and [DOI guide](https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/).
  The optional API JSON was inspected as data; no deposit or API
  submission was made, and server acceptance was not tested.
- Reran `verification/verify.py --json`: all four exact finite check
  groups passed. Their documented limitations remain explicit; they are
  not presented as a formal verification of the infinite-dimensional
  theorem.

## Inspected artifact hashes

These identify the final inspected package after the citation-file correction.
The PDF and TeX are unchanged from the initial visual/text review. Future
changes require rechecking the affected artifacts.

| File | SHA-256 |
|---|---|
| `output/pdf/note.pdf` | `cbc84a37bc7735675d833236c68c8194c99389b1398b21175f43998b9926e171` |
| `manuscript/note.tex` | `5950e74b23cb2be12626cb0c8d266cf3e3d6040c0dcfe8908a1fb49741796c94` |
| `output/note-source.zip` | `eb002c284e3bf15a10dbdee81a77aee22ba0d3d9ddd31274ab24e6673c792aae` |
| `output/zenodo-upload-kit.zip` | `f09d518062cfcff985afb9ac4240995a72d35a2d40a917c1853bf00f7c11c980` |
| `zenodo/metadata.json` | `6c400e1409c578a25bb58b5a22b8c236c6bb672395d58f00e0ee9aeee240b7f2` |
| `CITATION.bib` | `13218155696c86eecffe501728db32aa521ad898d456edc2aef1cac619bf6ac9` |
| `site/index.html` | `47d211384fa4170f7bd89cbbf7b2c74dc899b45ab2a2ed3b85ebc662bce4f6a2` |

No individual was contacted and no external state was changed. Best-guess
completion of this bounded package audit at this checkpoint: **100%**.
The root-manifest refresh and live-deployment verification are separate
publication steps still pending with the primary agent.

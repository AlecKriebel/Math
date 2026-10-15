# Standalone source for Local Ricci-pinching maxima on an almost-abelian group

Author: Alec Kriebel. ORCID: https://orcid.org/0009-0001-9320-500X.

This research-note source package contains the exact final standalone
[TeX source](local_ricci_pinching_maxima.tex) and a positive
[source manifest](SOURCE_MANIFEST.json). The manifest lists all payloads
except itself; the separate assembly/delivery record pins its actual hash.

Build with Tectonic:

    tectonic local_ricci_pinching_maxima.tex

Alternatively run pdflatex twice on that file. It uses article, geometry,
amsmath, amssymb, amsthm, and hyperref, with no external inputs or bibliography
files. A first Tectonic build may download its TeX support bundle. The root
compiled and visually checked all six PDF pages. Rebuilding renders the note;
different compiler versions or PDF metadata can change the PDF's byte hash.
The accompanying production PDF is copied exactly from the root's checked
90558-byte PDF, SHA-256
13d6fcdb924ea1461a6c44d4bb4e6aec1f278598218f8a34f26252d52ca0d37b.

The claim is a non-strict local maximum for every 0<u<1/2 among all nearby
left-invariant metrics on the specified fixed five-dimensional group, with
F=1/3, failure of that group's algebraic solvsoliton equation, and a same-group
metric with F=9/17. The metric is a Ricci soliton on another transitive
presentation. The family and value are Lauret–Will's prior work, and Lauret's
23 July 2018 slides already announced the negative existence statement.
Only the actually inspected arXiv versions are described; the full final
journal text was unavailable. No new family, first assertion, first proof,
novelty, or present community-open status is claimed.

This is an unrefereed, extensively AI-assisted account. AI tools were used
in solving, symbolic computation, source review, writing, and adversarial
verification. Machine agents are not independent human referees; no external
human peer review is certified, and the author retains responsibility.
The author proof-search record remains 2/5 with zero added assembly turns.
Whole-package acceptance and release status are tracked separately from
these source and historical component records.
No third-party full sources, raw searches, private state, or runtime are included.

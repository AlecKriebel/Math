# Version 1.2.1 frontier-feedback audit

**Audit date:** 16 August 2026
**Target:** two independent frontier-model reviews of Version 1.2
**Outcome:** valid corrections incorporated; no theorem blocker found after a
fresh post-edit reconstruction

## Adjudication

Each review item was treated as a hypothesis and checked against the current
source, rendered PDFs, proof dependencies, or live primary record.

Accepted and applied:

- defined the divergent species represented in top complexes as
  \(\mathcal J=\{i\in I:y_i\ge1\text{ for some }y\in\mathcal T\}\);
- displayed the exhaustive three-case bimolecular trichotomy inside the proof
  of the top-complex lemma;
- reduced the main notation collisions by using \(\rho\) for residuals,
  \(\delta\) for one-jump drift, \(\mathcal T\) for the top set,
  \(h_\star\) for maximal weight, and distinct path/trace/bound symbols;
- stated explicitly that removing self-channels leaves the population
  generator and minimal CTMC unchanged, that the population projection is
  autonomous, and that residual coordinates are bounded by population
  coordinates in the supermartingale integrability check;
- spelled out Anderson--Cappelletti--Kim in reader-facing prose;
- removed repository release numbering from preprint/supplement title pages
  and made the preprint-status wording durable after posting; and
- retained the supplementary note for optional bioRxiv and archival use while
  removing it from the planned JAP upload unless an editor requests it.

One additional defect was found while checking the reviews: active materials
cited the published 2020 JAP article with internal numbers from arXiv Version
2. The published article renumbered those items. The manuscript, cover letter,
expert note, reviewer checklist, and audit topics now use stable references to
published Section 6 and Section 6.1. The historical Version 1.1 literature
audit carries an explicit locator corrigendum.

Rejected or already satisfied:

- the JAP abstract already renders in seven nontechnical lines, within the
  current 4--10-line rule;
- the AI note already has the requested title, three paragraphs, tool/use
  description, and the statement that Codex did not expose its exact backend;
- the live official arXiv Version 2 title is *On the Regulary of Reaction
  Systems*; the proposed replacement was stale metadata, although the
  editorial `[sic]` note was removed;
- the Geneva program already supplies an earlier June 2022 public conference
  record than the proposed Cornell addition;
- the proposed sharper multiple-linkage conclusion is false for this proof
  method because terminal availability does not supply a directed path from a
  carried target in another linkage class; and
- folding the two-page note into the self-contained paper would duplicate
  material and add late-stage churn. Current APT guidance permits beneficial,
  nonessential supplementary material, although the note is not planned for
  the JAP upload.

## Fresh adversarial reconstruction

After the edits, the proof was reconstructed through lifted state returns,
marked-target irreducibility, the exact factorial and entropy identities,
episode recursion and scalar envelope, normalized-log extraction, every
bimolecular top-complex branch, terminal rarity, exceptional-set compactness,
the stopped Foster argument, trace return, autonomous population projection,
physical-time nonexplosion, and regenerative occupation. No circularity,
missing branch, invalid quantifier, or new notation defect was found.

All 57 verifier tests passed with the unchanged Version 1.2.0 verifier and the
canonical report remained byte-identical. The release replay, manifest,
archive, deterministic rebuilds, and final rendered-page inspection are
recorded by the Version 1.2.1 validation materials. These finite checks are
falsification and reproducibility aids, not the universal proof.

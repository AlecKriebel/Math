# Priority search log

**Run date:** 2026-08-08 (America/Los_Angeles)

**Policy:** primary sources support substantive conclusions; index services
were used only for discovery and citation/update checks.

## Primary records opened

- `https://arxiv.org/abs/2606.21362` and raw source archives for v1, v2, v3.
- `https://arxiv.org/abs/2606.21369v2`.
- `https://arxiv.org/abs/2606.21371v2`.
- `https://arxiv.org/abs/2606.21626v1`.
- `https://arxiv.org/abs/2604.03700v1`.
- `https://arxiv.org/abs/2308.08601v2` and the published Quantum article.
- `https://arxiv.org/abs/1909.12722v2` and the published npj Quantum
  Information article.
- DOI landing pages for the complete-statistics randomness papers, SATWAP,
  MUB self-testing, and the binary calibration cited in `main.tex`.

## Originating-version inspection

Each arXiv source archive for 2606.21362 was unpacked and searched for:

- the reduced and augmented operator definitions;
- every occurrence of `Conjecture`, `randomness`, `guessing`, `unique`,
  `self-test`, `sum of squares`, and `supplement`;
- (B_y) versus (B_y^\dagger);
- the first value (2\csc(\pi/(2d)));
- the second-family coefficient and SOS normalization;
- public code or supplementary archives.

Result: v3 is the latest version found. Its substantive change relevant here
is the corrected (1/(2d)) second-family SOS and added fixed-full-behavior
numerics. The first exact upper proof and phase-permutation construction are
absent from all three inspected versions.

## Discovery queries repeated after claim freeze

Searches used combinations of the following strings in arXiv/web scholarly
indexes (with title/author and 2026 date filters where supported):

- `"Bell inequalities tailored to optimal global randomness certification"`
- `2606.21362 cyclic Bell`
- `Perito D'Avino Jung Mironowicz Acin Augusiak cyclic Bell`
- `"2 csc(pi/(2d))" Bell`
- `"exact Tsirelson bound" cyclic modular Bell`
- `cyclic Bell commuting operator value`
- `weighted shift phase permutation Bell maximizer`
- `permutation blind Bell score randomness`
- `maximum Bell value nonuniform joint outputs`
- `global randomness complete behavior scalar Bell value`
- `augmented cyclic Bell family SOS`
- `site:arxiv.org cyclic Bell randomness 2026`
- cited-by and related-work records for arXiv:2606.21362.

Author/date searches were also run for Perito, D'Avino, Mironowicz, Acin,
and Augusiak for records dated after 21 July 2026.

## Negative-result boundary

No later originating version, public correction, source-author note, citing
paper, or independent paper containing the same family-specific theorem was
located. OpenAlex reported zero citations and Semantic Scholar returned only
the contemporaneous June papers at the cutoff. Index lag and unpublished
work remain possible, so the audit uses `PLAUSIBLY NEW` and `to our
knowledge`, never definitive priority language.

## Repository and historical searches

All three source packages were searched for prior audits, claim ledgers,
failed approaches, certificates, release records, and copied literature
notes. Git history and `PUBLICATION.md` were used to identify initial and
revised PDF hashes. No Git tag, GitHub release, or DOI specific to these Bell
papers was found. Historical records were evidence about internal chronology,
not substitutes for the fresh external search.

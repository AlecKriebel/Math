# Source and duplicate gate

Checked 2026-10-04 UTC.

## Primary-source chain

1. [Hayman and Lingham, arXiv:1809.07200v2](https://arxiv.org/pdf/1809.07200v2), printed p. 109, PDF page 110: Problem 5.66 and its immediately following Update. The page was read as text and visually inspected. The update records the negative answer and the shift argument, although its publication label is stale.
2. [Stephenson, 1988, DOI](https://doi.org/10.1090/S0002-9947-1988-0951624-3), *Construction of an Inner Function in the Little Bloch Space*, Trans. Amer. Math. Soc. 308(2), 713–720. [Complete article text inspected here](https://www.academia.edu/60898917/Construction_of_an_Inner_Function_in_the_Little_Bloch_Space). Section 2, pp. 714–716, identifies finite fibers; Section 3, pp. 716–717, establishes innerness; Section 4, pp. 717–718, records infinitely many zeros and the Frostman-shift conclusion. The journal's PDF endpoint was inaccessible and the alternative download encountered a challenge; no publisher PDF or visual inspection of this article is claimed. Readable full text, including the proof and page markers, was available.
3. [Bishop, 1993](https://www.math.stonybrook.edu/~bishop/papers/Indestructible.pdf), *An Indestructible Blaschke Product in the Little Bloch Space*, Publicacions Matematiques 37, 95–109: p. 96 states the relevant shift theorem; pp. 101–102 give a directly Blaschke variant of Stephenson's example before the subsequent indestructibility modification. Those two pages were also inspected visually. This is corroboration, not a claim that the paper's ultimate indestructible example has finite fibers.

### Construction checks

The 1988 proof was checked for three properties: infinitely many sheets retain zero; each designated exceptional value occurs only on finitely many earlier sheets; the generation lengths can be chosen to make the boundary-circle exit probability arbitrarily close to one. The resulting function supplies precisely the input theorem in `PROOF.md`.

No correction invalidating the result was located in title/author/problem-specific searches. This is a targeted check, not an exhaustive bibliographic certificate. The 1993 paper provides later primary corroboration.

## Catalogue and prior report

[Catalogue request](https://www.unsolvedmath.com/problems/2305066) returned HTTP 403. The recovered selected upstream record has the exact infinite-Blaschke formulation and directs readers to the 2018 source. Its prior report says open/no resolution found; that assessment is obsolete.

The inspected research-results corpus exactly matches the repository manifest's SHA-256. The available problems corpus does **not** match that manifest's recorded bytes/hash; its separate observed hash is retained in `SOURCE_MANIFEST.json`. Accordingly no claim is made that this selected metadata comes from the manifest's exact immutable problems snapshot. The mathematical statement is independently confirmed in the primary source.

## Live repository duplicate check

Repository: [AlecKriebel/Math](https://github.com/AlecKriebel/Math).

Observed main commit: `bd5c59ad2b9f2c57c82aa1fe7b0466fe3ea92e1b`.

The live queue row was rank 579, queued, 0/5. The attempts directory listing contained no 2305066 directory; state.json had no corresponding entry. Target-ID and problem-number PR searches and the ID-specific branch search returned no matches. The related-target groups file did not list this ID. These are point-in-time searches, not guarantees against unindexed or concurrent work. Adjacent Problem 5.65 is a different claim.

## Publication scope

This package reports a historical resolution and a corrected classification. It does not claim a novel counterexample, formal verification, explicit computable zeros, or exhaustive literature coverage. Its source dependencies and access limits are stated above. Source files and dataset corpora are not part of the public package.

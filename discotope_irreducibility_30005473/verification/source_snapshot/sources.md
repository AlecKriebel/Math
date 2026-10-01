# Source and novelty audit

Checked 30 September 2026. This is a dated, bounded literature search, not a certification of historical novelty.

## Exact source

- Requested upstream page: https://www.unsolvedmath.com/problems/30005473. Tried first. The web tool could not retrieve it, and the cloud browser displayed a 403 request-blocked page. No workaround around that page's block was attempted.
- The repository pins the UnsolvedMath dataset to revision `37e53eabe540fb458758e198be61634bd02ee008`. The full record at numeric ID `30005473` has code `OWR-12697711-006`, and its clean statement asks for irreducibility of the Zariski closure **E of exposed points**, for a generic discotope with all summand dimensions at least two. No entry for this code exists in the pinned `research_results.json`; there is no prior upstream AI proof report to audit.
- Official source: Chiara Meroni, *Two convex conjectures for different flavours*, in *New Directions in Real Algebraic Geometry*, Oberwolfach Reports 15/2023, pp. 829–832. The target is Conjecture 1 on printed p. 830 (PDF page 18). The report's Definition 1 on that same page defines the discs as linear images of unit balls and defines E from exposed points. The report's following rank-one-convexity conjecture is a different problem.
  - DOI: https://doi.org/10.4171/OWR/2023/15
  - Official PDF: https://publications.mfo.de/bitstream/handle/mfo/4031/OWR_2023_15.pdf?sequence=4
  - Downloaded PDF SHA-256: `32c4fbd8b25f445613300ed0a00ba2082d653a154a3b2f64734f19c678d351ff`

## Earlier paper and scope distinction

Fulvio Gesmundo and Chiara Meroni, *The Geometry of Discotopes*, Le Matematiche 77(1) (2022), 143–171.

- DOI: https://doi.org/10.4418/2022.77.1.8
- arXiv: https://arxiv.org/abs/2111.01241
- Publisher PDF: https://lematematiche.dmi.unict.it/index.php/lematematiche/article/download/2338/1156/6734
- Downloaded PDF SHA-256: `76d7033365db98c4cc4ce166aaa5bda2b1aaa25d5ba3386d3d66651a849c9adb`

Relevant exact locations: Section 2, pp. 145–147, defines generalized discs, the generic-bases convention, and reduction to a full-dimensional span. Section 3, pp. 147–149, describes normal directions and introduces S. Definition 3.3, p. 149, takes S to be the complex Zariski closure of the boundary points which are sums of relative summand-boundary points. Section 5, especially pp. 155–156, uses the support gradient and explicitly notes that S might have additional components. Conjecture 8.2, p. 167, asks for S to be irreducible. Its neighboring remarks discuss different critical-locus, birationality, and degree questions.

The 2023 report calls its E conjecture the earlier Conjecture 8.2, but the written formulations concern different algebraic sets. The candidate addresses this rather than assuming equality: Sections 1–4 prove the exact E claim, and Section 5 separately proves S=E under explicit general position. Section 6 gives a nongeneric example where E and S differ, so the distinction is meaningful.

## Current literature checks

- The arXiv record for 2111.01241 still identifies version 2, dated 28 July 2022, as its latest version. Its abstract describes the two-dimensional-disc theorem; the original paper retains its general conjecture.
- Meroni's current research bibliography, including entries through July 2026, was inspected: https://merochia.wixsite.com/chiara-meroni/research. It lists the 2022 discotope paper, the 2023 fiber-body paper, and the 2023 Oberwolfach report. No later listed item was identified as a general discotope irreducibility resolution.
- The related primary paper *Fiber Convex Bodies* is available at https://arxiv.org/abs/2105.12406 and https://doi.org/10.1007/s00454-022-00451-3. The relevant discotope discussion concerns discs in three-space and fiber-body geometry; it does not supply a general higher-dimensional-disc resolution.
- Focused public searches included the mathematical term with “irreducibility,” “real analytic,” “Conjecture 8.2,” “exposed points,” and “2026.” The retrieved mathematical results led back to the original paper, report, thesis, and related fiber-body work. Most other results use the unrelated biological term DiscoTope and were excluded.

- The public IMProofBench paper, linked by the author and revised July 2026, was checked for the mathematical terms at https://arxiv.org/html/2509.26076v2. It contains no discotope or irreducibility occurrence and supplies no relevant resolution. No private benchmark access was attempted.

**Conclusion:** No prior full resolution was identified in the sources inspected. This supports further review of the candidate; it does not establish that the proof or theorem is historically new. No researchers were contacted.

## Repository and related-record checks

Repository base inspected: `01358d66fc67d1c462bddf31c0d4ee5b120e6737` on main.

- QUEUE.md rank 27 shows ID 30005473 as queued, 0/5, with no historical note. The empty state.json is not used to override queue history.
- Exact ID and discotope code searches found only queue and desk-review metadata, not a prior attempt. All-state PR searches for `30005473` and `discotope`, and branch search for `30005473`, found none.
- `review_v2/related_target_groups.json` has no group containing this ID. The desk-review note suggests a quadratic-radical route; it is not a prior proof attempt.
- Adjacent record 30005472 asks algorithmic zonoid recognition; it is not settled by the candidate. Adjacent record 30005474 is an orphaned conjecture-label extraction; it should not be promoted or counted as a second discovery from this work without separately repairing its exact source statement.

## Reproducible source binding

The record hash is computed exactly as queue.py's score function: SHA-256 of `json.dumps([problem_record, {}], sort_keys=True)` encoded as UTF-8. The missing report is represented by `{}`. See source_record.json and readiness.json for the resulting hash. No queue regeneration or state mutation was performed.

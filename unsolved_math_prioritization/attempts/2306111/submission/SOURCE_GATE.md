# Source and repository gate

Checked 2026-10-04 UTC.

## Exact source authority

The requested starting URL was https://www.unsolvedmath.com/problems/2306111. A direct request returned HTTP 403, and the web reader could not access it. The current catalogue presentation and status are therefore not verified.

The statement was recovered from Walter K. Hayman and Eleanor F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2, printed page 156 / PDF page 157, Problem 6.111 and its update. The full PDF, extracted text and rendered target page were inspected. The update reports no known progress to the authors at that edition's date. It is not evidence that no later work exists.

- Primary source: https://arxiv.org/abs/1809.07200
- Fixed PDF: https://arxiv.org/pdf/1809.07200v2
- Original cited paper: T. Sheil-Small and E. M. Silvia, *Neighborhoods of analytic functions*, Journal d'Analyse Mathématique 52 (1989), 210–240, https://doi.org/10.1007/BF02820479

The publisher confirms the original paper's bibliographic identity. Its full text was not obtained: the nominal PDF request yielded HTML. Accordingly, the restricted-range theorem is used as explicitly recorded by Hayman–Lingham, not as an independently audited original-paper proof.

## Pinned corpus and prior work

The repository manifest names dataset revision 37e53eabe540fb458758e198be61634bd02ee008. Both source files were downloaded from that fixed revision and matched its size and SHA-256:

- problems.json: 68,931,837 bytes; 04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf
- research_results.json: 80,334,822 bytes; 8da848d31c20eb4eecaa07702eced4724aa4a89f877c2a0774d9f3138389aa6b

The selected record is numeric ID 2306111, code AMR-022-6111. Its exact statement agrees with the primary source. The prior report's classification is OPEN-TRIAGE; it records reading the statement and an unsuccessful web search, and supplies no mathematical proof or counterexample. The statement and report were read in full. A pre-existing shared corpus with a different hash was used only for initial discovery, not accepted as pinned evidence.

The adjoining records 2306112 and 2306113 concern different Sigma-neighbourhood/dual-class assertions. They share context but are not duplicates of this coefficient-neighbourhood problem.

## Live repository / duplicate checks

Repository: https://github.com/AlecKriebel/Math
Observed main commit: 6a112842592930803e459f013484062787ce7772.
Observed QUEUE.md Git blob: c1009ab2e12b93cffb15cb17c0ac893979ce5a44.

The root AGENTS.md, queue AGENTS.md and queue README were read. The rank-590 row was `queued`, 0/5. The state file had no exact target entry. Exact-ID code search, PR search and branch search returned no matches. Both unsolved_math_prioritization/attempts/2306111 and function_theory_2306111 returned 404. Additional Janowski code and neighbourhood/Janowski PR searches returned no matches. The related_target_groups.json file contains no 2306111 group.

These are scoped, live negative checks, not proof against every possible differently named or unindexed duplicate. No remote content was changed.

## Current-literature check and limits

Searches used the exact problem number, proposer names, title, Janowski convex/neighbourhood terms, and the original DOI. Primary publisher pages were preferred for bibliographic facts.

A directly relevant later paper is Richard Fournier, *One More Note on Neighborhoods of Univalent Functions*, Computational Methods and Function Theory 20 (2020), 693–699, https://doi.org/10.1007/s40315-020-00347-4. Its publisher page and abstract were inspected; the full text was not obtained. The available abstract does not establish whether it settles the exact Janowski question. This is a material literature limitation. No `already_solved` finding is justified, and no comprehensive still-open or novelty assertion is made.

Nihat Yagmur's 2015 paper, *On neighborhoods of functions associated with conic domains*, was retrieved from the journal site and its relevant definitions and Theorems 2.1–2.3 inspected. Theorem 2.3 displays the radius (A-B)t/[8(t+1)], which is at most (A-B)/8<=1/4; this does not provide the requested sharp delta(A,B). Indeed, in the missing region B=-b and 0<beta=(A+b)/b<2, the target is (1+b)^(-beta)>1/4. Its proof was not independently audited and is not used in our partial results. Searches also found work on generalized weighted or meromorphic neighbourhoods; those altered classes and constants are not silently identified with this target. See SOURCE_MANIFEST.json.

The primary 2018 source, ordinary analytic convexity/starlikeness criteria, and Herglotz's representation are the mathematical inputs to this package. Propositions 1 and 2 are fully argued in FULL_PROOF.md. Proposition 3 clearly declares its dependence on the recorded restricted-range result.

## Rights and publication scope

Source PDFs, full corpora, extracted source text, source screenshots, retrieval response bodies and private coordination stay outside the candidate publication set. The publication set consists only of original research notes, mathematical deductions, source metadata, code, finite computation results and checksum controls. Downloading a source for private research does not grant redistribution rights.

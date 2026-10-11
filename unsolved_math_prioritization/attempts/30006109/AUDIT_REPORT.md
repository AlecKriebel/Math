# Independent audit of bounded congestion and the fare zone model

## Verdict

PASS as a correctly scoped partial result and model correction. No combinatorial gap was found in the frozen candidate's exchange proof, congestion-at-most-two reduction, or two-edge separation example. The original open problem must remain open in any sense that would require sharp approximability or a general classification.

Audited identifier: row 1688, problem 30006109. The frozen candidate was 4,751 bytes with SHA-256 adac9eda645c63fbe5e76a9db8c65a0ba1eb3f62a8c971d82cb9cfe6981c4b20. Its bytes were checked before and after the audit. This identifier records the supplied audit target; it is not a fresh audit of the full source dataset or queue.

The full independently checked argument is in PROOF_AND_MODEL_CORRECTION.md. This report should travel with that explicit scope, rather than being summarized as a solution of the original problem.

## Mathematical checks

- Original objective: confirmed as the sum of selected-edge profits, each edge profit being the sum of weights of all commodities containing that edge. This equals the sum of each commodity weight times its number of selected path edges.
- Hard capacities: confirmed in the actual displayed OWR program. Every commodity's path count must stay below its capacity. A zero-weight commodity still imposes a constraint.
- Nonnegativity: explicitly assumed by the candidate and the expanded theorem. The short OWR statement does not itself specify the number domains or signs. For the stated finite-time guarantees, the expanded proof uses nonnegative rational weights and capacities with finite binary encodings.
- Integral capacities: nonnegative rational capacities can be floored and clipped to path size. This is exact because all path counts are integral. Clipping also prevents a numerically large binary capacity from creating too many matching slots.
- Congestion: the maximum number of listed commodity paths containing an edge. The exchange bound depends on this incidence count, not path length. Empty paths, duplicate paths, zero capacities, zero profits, and congestion zero are handled explicitly.
- Exchange lemma: adding an edge violates at most k unit-coefficient constraints, and one removable edge outside the protected greedy prefix can be chosen for each. Simultaneous removals cannot create new violations.
- Greedy bound: the exchange loss is at most (k-1) times the accepted edge profit. A removed edge cannot have been previously rejected, so its profit is no larger than the current accepted edge's. The final comparison set equals the greedy set; telescoping yields OPT <= k times the greedy value. This is not a sharp-ratio claim.
- Congestion at most two: the constructed multigraph's commodity degrees are exactly the original cut counts. Private capacity-one vertices cover singleton incidences. Distinct original choices require parallel edges to remain distinct and each graph edge to have upper capacity one. The graph need not be bipartite.
- Exact polynomial algorithm: the expanded proof supplies a slot-and-edge gadget reduction to ordinary general-graph maximum-weight matching. It has at most four times as many vertices as retained edges and quadratically many edges after capacity clipping. Exact rational weights preserve finite bit complexity.
- Two-edge witness: exhaustive enumeration gives hard-feasible revenues 0,3,3 and dropout revenues 0,3,3,4. The last choice is infeasible under hard capacities.

## Primary source inspection and attribution

The OWR paragraph at printed page 2992 / PDF page 44 and the later manuscript's Definition 1 at PDF page 2 were both read as extracted text and visually inspected as rendered pages. The later manuscript's surrounding model text on pages 2-3, congestion terminology on page 4, and Theorem 3 on page 7 were read as well. Its cut-budget violation changes revenue to zero rather than excluding the cut set. This directly establishes the claimed model difference; the conclusion does not rest on an abstract-only comparison.

Mestre's official publisher preview, printed pages 528-529, confirms prior general k-extendible-system and greedy attribution. Only the two-page preview was available and inspected, not the complete chapter. The proof used here is supplied directly, so this access limitation creates no missing combinatorial step.

Gabow's primary manuscript, arXiv:1611.07541v1, Section 1, pages 1-2, confirms ordinary weighted matching as a classical polynomial-time problem and discusses generalized matchings. Its perfect, uncapacitated b-matching convention differs from the unit-capacitated degree-upper-bound formulation needed here. The explicit reduction to ordinary matching avoids treating those conventions as identical. This audit does not reproduce or independently verify the full blossom algorithm.

All four inspected PDF versions have byte counts and SHA-256 pins in PUBLIC_SOURCE_METADATA.json. The original OWR and later FZA PDFs were reused from already retrieved primary-source files, with their hashes recomputed and relevant pages independently reinspected. The Mestre preview and Gabow manuscript were freshly retrieved from their official public locations. The source log distinguishes retrieval from inspection; no full-source read or lifetime retrieval count is claimed.

## Finite verification

The locally retained authored finite-check program has no external dependencies, network access, or source-author code. It checks finite examples in addition to the mathematical proof. It does not turn a finite enumeration into a proof of the general result. The executable program is not included in this public packet; only its identity and aggregate results are published.

- 234,946 greedy instances: all set systems on up to three elements with up to three listed constraints, capacities from zero to the corresponding subset size, and commodity weights in {0,1,2}.
- 9,050 unweighted systems with 55,975 eligible exchange triples.
- 4,600 congestion-at-most-two systems with 35,132 subset checks of feasibility and objective preservation.
- 260 independently optimized ordinary-matching gadgets, including rational weights, odd-cycle, parallel-edge, zero-capacity, and enormous-capacity cases.
- Exact rational flooring checks and all four choices in the model-separation witness.

The normal, Python -O, and Python -OO runs produce identical PASS JSON. The checker uses explicit failures rather than relying on assert statements. Detailed deterministic counts and the witness are in MATHEMATICAL_CHECKS.json.

## Accepted use and limits

The accepted statement is a nonnegative, finitely encoded hard-capacity bounded-congestion baseline, with exact polynomial solvability for congestion at most two, plus a verified distinction from the later dropout model. The general exchange idea and polynomial matching algorithms have prior literature attribution. There is no novelty certification, no best-possible ratio, no new hardness result, and no claim that all remaining tree instances are solved.

This is an AI-assisted mathematical audit, not human expert peer review, journal acceptance, or a formally machine-checked proof. The finite checker is a supplementary consistency test. The cited primary literature remains responsible for the imported general weighted-matching theorem.

No inference is made that the later paper is incorrect in its own model, or that a future reduction between the models is impossible. Its approximation guarantees simply cannot be imported automatically as hard-feasible guarantees. No complete mathematical audit of that manuscript's approximation proofs is claimed.

The audit itself made no publication, repository, queue, source-author-code, or outreach changes. This prepared packet is governed by PUBLICATION_MANIFEST.json. Copied third-party PDFs, source text, images, executable programs, raw finite-instance data, and private coordination files are excluded.

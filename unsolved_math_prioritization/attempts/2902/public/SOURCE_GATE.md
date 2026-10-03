# Source and prior-work gate

Checked 2026-10-03. Exact-question identification: **verified**. Universal resolution: **not established**. External proof access is itemized rather than inferred from abstracts.

## Exact problem

- Catalogue locator: https://www.unsolvedmath.com/problems/2902 ; a direct retrieval returned HTTP 403. Catalogue identification was only a pointer, not mathematical evidence.
- Primary problem source: *K3: A New Problem List in Low-Dimensional Topology*, preliminary 2026 version, Problem 4.26, printed pp. 211–212, proposed and scribed by C. Livingston. The question and surrounding remarks were read in text and checked against page images. The exact wording is transcribed once in PROOF.md.
- Verified public PDF: https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf
- The frequently supplied https://aimath.org/pastworkshops/kirbylistrep.pdf is a four-page workshop report, not the full problem-list text. It was not used as a substitute.

The target is the compact puncture of an arbitrary integral homology 3-sphere in standard smooth S⁴. Neither a topological embedding, a closed-sphere obstruction, nor an embedding in a homology/homotopy 4-sphere settles that target.

## Established results and proof access

1. E. C. Zeeman, *Twisting spun knots*, Transactions of the AMS 115 (1965), 471–495, DOI https://doi.org/10.1090/S0002-9947-1965-0195085-8 . Full article obtained from the London Mathematical Society: https://www.lms.ac.uk/sites/default/files/1965%20Twisting%20spun%20knots.pdf . Inspected §§5–7, including the branched-cover definition, Lemma 3, the Main Theorem, and Lemmas 4–6 with their proofs. Main Theorem part 2 and Corollary 4 supply the compact punctured embedding used here. Corollary 2 instead states the ±1-twist unknot conclusion. Pages 486–487 were visually checked.
2. J. A. Hillman, *Locally flat embeddings of 3-manifolds in S⁴*, §2.9, pp. 25–26, author manuscript https://www.maths.usyd.edu.au/u/jonh/embkDec24.pdf . Confirms the standard doubling and connected-sum reductions; both are proved in the present note rather than treated as new results.
3. K. Larson, *Surgery on tori in the 4-sphere*, arXiv https://arxiv.org/abs/1502.06834 ; full PDF https://arxiv.org/pdf/1502.06834 . Published Math. Proc. Cambridge Philos. Soc. 164 (2018), 109–124, DOI https://doi.org/10.1017/S0305004116000876 . Inspected the statements and arguments of §5.1 for scope comparison. This article is not used to prove the stronger arbitrary-knot punctured S⁴ assertion. Its proof dependencies are not being certified wholesale.
4. K. Larson, *Some Constructions Involving Surgery on Surfaces in 4-manifolds*, University of Texas at Austin PhD thesis (2015). K3 credits an arbitrary-knot 1/n-surgery punctured embedding to this thesis. The linked file https://repositories.lib.utexas.edu/server/api/core/bitstreams/32f94088-e19b-4b49-8dd8-7b2320ef72e3/content returned HTTP 403. The proof is **not inspected** and the assertion is **not used as a premise** in any proposition.

The source's unqualified ordinary-spinning sentence is not promoted to a universal smooth embedding of closed Y in a smooth homology 4-sphere. The explicit surgery here preserves the punctured slice; the smooth closed interpretation would conflict with the homology-ball and Rokhlin obstruction. No claim is made about what an unqualified topological reading intended.

## Prior attempt and update checks

Repository: https://github.com/AlecKriebel/Math . Read the live unsolved_math_prioritization/QUEUE.md: rank 533 / ID 2902 / KP-4.26 was queued, 0/5. Independently searched all PR states for `2902`, `Kirby` with `4.26`, and `KP-4.26`, and searched repository code for `2902`, `Kirby Problem 4.26`, and `punctured homology sphere`; no exact-target result was returned. The exact attempts/2902 directory returned 404. A broader `punctured` PR search found unrelated targets, including KP-3.71, not a prior KP-4.26 attempt. A recursive-tree request failed in transport and is not counted as evidence. These checks are bounded retrieval evidence, not a proof that no differently named prior artifact exists. The queued row alone was not accepted as sufficient clearance.

Targeted public searches for the exact number, punctured homology spheres, smooth embeddings, and recent updates located the current problem list and established special cases, but no verified universal proof or counterexample. Search absence is not a mathematical proof of openness or a historical-priority claim.

## Reuse and attribution

The note is an unrefereed research attempt. Its reductions and elementary surgery calculations are standard reasoning, and known positive examples are attributed. No novelty claim is made. Source PDFs and extracted source texts are retained only for local inspection and are not part of the public package. Public source fingerprints are in SOURCE_HASHES.json; the mathematical and verification files are frozen by SHA256SUMS.

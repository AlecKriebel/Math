# Acceptance report: restricted outerplanar divergence

The independent mathematical audit accepts the complete theorem for interval-complete positive-integer weighted trees with w(v)>=deg(v)-2: along every sequence with total weight W tending to infinity, W/2^q tends to zero. The centroid/matching bound, bounded nonleaf core, finite-coordinate subsequence extraction, fixed choice of M, and small-weight collision argument are retained with their endpoints and quantifiers.

Through the polygon-dissection model, this proves h_out(n)-log_2 n->infinity. The face-weight identities, cycle-to-connected-face direction, existence of a pancyclic fan for every n>=3, and passage to minimizers are included. The result concerns the restricted outerplanar extremal function, not the unrestricted h(n).

For every integer k>=3, a pancyclic graph with star weak dual obeys n<=4k^2-19k+34, while the explicit central-k-gon construction realizes n=4k^2-19k+31 with excess k. Its leaf weights, contiguous subset-sum intervals, simple cycles, and k=3 empty-list endpoint are fully proved. These conclusions establish the leading coefficient 4 in this subclass, not its exact finite extremum.

The internal unpublished candidate's intermediate c=k substitution was corrected from k^2+6 to k^2+4. The corrected successive differences and endpoint values 13,13,13,12 at k=3 prove the maximum bound for every integer k>=3. The repair is explained completely in AUDIT.md. A bibliographic omission of “Some” from the Erdős title was also repaired. Neither correction is a claim about an error in published literature.

ACCEPTANCE.json binds this edition's proof, audit, and acceptance report to their exact bytes and identifies the separately accepted corrected input. Editorial removal of internal bookkeeping and replacement of supporting raw evidence by aggregate metadata do not remove any mathematical proof or construction. The corrected input and the publication edition are not claimed to be byte-identical.

## Publication and review boundary

This AI-assisted work is unrefereed. Acceptance means an independent internal AI audit of the authored candidate, corrected proof, and separate exact controls. No external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The arithmetic correction concerns an unpublished internal candidate, not a claimed error in published literature.

The complete mathematical proofs and algebraic construction are included. The universal statements rest on those proofs, not on finite enumeration. Raw code, certificates, copied source documents, and private coordination material are not distributed. The omitted finite controls are supporting validation and are not unproved premises of the mathematical results. This edition is a self-contained mathematical proof of the stated restricted results, but is not a computational reproduction package. No novelty, priority, or exhaustive literature-status claim is made. The unrestricted crossing-chord divergence question and the stronger coefficient-one log-star lower bound remain unresolved by this work.

## Sources and historical inspection

- P. Erdős, *Some Unsolved Problems in Graph Theory and Combinatorial Analysis* (1971), Problem 10, printed page 101 / PDF page 5. [Original PDF](https://www.renyi.hu/~p_erdos/1971-25.pdf). The retained source was inspected in text and visually for the title and Problem 10; unrelated problems were not reviewed. It supplies the original unrestricted question whether h(n)-log_2 n tends to infinity, not an explicit statement of the stronger modern log-star lower bound.
- Sean Griffin, *Minimal Pancyclicity*, arXiv:1312.0274v1 (2013). [Abstract](https://arxiv.org/abs/1312.0274), [PDF](https://arxiv.org/pdf/1312.0274). Historical inspection covered the relevant introduction, Claim 1 and its complete lower-bound proof, the binary log-star stopping convention, sections 1.1 and 1.2, and references; PDF page 2 was visually checked. Claim 1 gives the standard lower bound h(n)>=log_2(n-1)-1. The upper construction's full derivation was not used.

These sources provide problem and literature context. They are not external proof dependencies for the weighted-tree lemmas, restricted divergence, star bound, or algebraic construction, all of which are proved here. A bounded earlier search did not establish whether these restricted results were already known. No theorem from an uninspected related paper is invoked. Edition preparation performed no new scholarly-source retrieval, visual inspection, mathematical experiment, or literature search. SOURCES.json records the retained public source identities and the earlier reading scope; historical inspection is not presented as a new inspection.

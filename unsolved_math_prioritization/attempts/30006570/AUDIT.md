# Independent audit: threefold Feige baseline values

Problem 30006570 / OWR-14299906-007. Audit date: 11 October 2026.

## Review and edition status

This is an AI-assisted, unrefereed mathematical proof and audit edition. Its acceptance records an internal AI mathematical audit; it is not external human peer review or formal proof-assistant certification. No novelty is claimed. The exact classical and nonsignalling baseline values were already stated in the cited primary literature. The original quantum-comparison problem remains unresolved by this work.

This is a prose proof/audit edition, not a computational reproduction package. The complete elementary arguments and compact symbolic strategies are provided here. Executable programs, raw outputs, expanded event lists, copied source documents and private coordination material are not distributed. Historical computational checks are described with their scope and limits; they are not represented as new executions during edition preparation. The hand proofs do not depend on those omitted materials.

## Verdict and scope

**ACCEPTED:** the authored proof establishes the exact classical value 5/16 and exact nonsignalling value 1/3 for the threefold parallel repetition specified in the original question. Both values have explicit attaining witnesses. This yields 5/16 <= omega_q <= 1/3.

**UNRESOLVED:** this audit does not establish whether the quantum value is strictly greater than 5/16. It does not certify a quantum optimum or a quantum-realizable 1/3 strategy. The original problem must not be marked solved on the strength of these results.

The primary literature already states both baseline values. This work supplies a self-contained upper-bound argument and exact computational cross-checks rather than a novelty claim.

## Conventions checked against the original sources

- Two parties receive independent uniform three-bit vectors, giving 64 input pairs.
- Each party returns a vector from {0,1,bottom}^3. Every coordinate must satisfy either (a_i,b_i)=(bottom,x_i) or (y_i,bottom).
- Local answers may depend on all three local bits. No product, sequential, synchronous, fixed-pattern, or restricted-orbit assumption is imposed.
- The classical set includes arbitrary private and shared randomization. Since all inputs and outputs are finite, sampling all local response-table entries in advance expresses any such strategy as a convex combination of deterministic table pairs. Linear optimization therefore reduces to all 27^16 deterministic pairs.
- The intended quantum value is the supremum over finite-dimensional tensor-product states and unrestricted local POVMs on full input/output vectors. There is no fixed-dimension conclusion here.
- Nonsignalling means independence of each complete output-vector marginal from the remote input vector. No additional coordinatewise independence is imposed.

The original Oberwolfach question appears on printed p. 241, PDF p. 25. Its preceding definition and the manuscript's Definitions 2.1-2.5 and 6.1-6.2 fix these conventions.

## Classical upper-bound proof audit

For every deterministic pair, partition Alice's eight rows by bottom count k and Bob's eight columns by bottom count 3-k. All winning edges stay within matching classes because bottom positions must be complementary. The number e_k of winning pairs in each class satisfies

e_k <= 2^k r_k and e_k <= 2^(3-k) c_k.

This holds for every response table: fixing a row answer specifies 3-k bits of Bob's input, leaving at most 2^k candidates. The column argument is symmetric. Complementarity of the counts is necessary, not sufficient; relaxing sufficiency enlarges the feasible set and cannot invalidate the upper bound.

The ceiling argument is valid. For k=1,2 the cost is ceil(e/2)+ceil(e/4). For k=0,3 the cost is e+ceil(e/8), which is at least that quantity: e=0,1 are direct, and for e>=2, floor(e/2)>=ceil(e/4). Summing costs and using ceiling subadditivity gives

16 >= ceil(E/2)+ceil(E/4).

E>=21 would require at least 17 vertices. Thus E<=20 for every deterministic pair and for every classical mixture. This proof does not transfer integer rounding to fractional quantum or nonsignalling masses.

The attributed Boolean strategy is transcribed correctly. Its five winning assignments of (x1,x3,y2,y3), with four independent choices of unused (x2,y1), give exactly 20/64=5/16. All 64 input pairs were independently checked, not sampled.

## Nonsignalling upper and lower bounds

For general nonsignalling p, let R_k and C_k be total full-vector marginal masses in the matching bottom-count classes, and let S_k be total unnormalized winning mass there. The same input-compatibility count, together with nonsignalling, proves S_k<=2^k R_k and S_k<=2^(3-k) C_k. The exact convex weights (8/9,2/3,1/3,1/9) give coefficients (8/9,4/3,4/3,8/9), each at most 4/3. Since sum R_k=sum C_k=8, total winning probability is at most (4/3)*16/64=1/3.

No hidden integrality assumption appears in this argument. Positivity, normalization, and the two block-marginal equalities are sufficient. Quantum correlations satisfy those equalities by POVM normalization, so the bound holds for the entire intended quantum class.

The explicit lower witness assigns mass 1/3 to each of three distinct events for every question pair, giving 192 positive events. Its first-coordinate marginal is uniform on the three symbols, and its other outputs depend only on the relevant local vector. The exact rational audit checks normalization at all 64 pairs and every marginal equality. Its score is exactly 1/3. Therefore the nonsignalling claim is an achieved exact optimum, not merely an upper bound.

## Source exposition issue: exact scope

The manuscript's pp. 21-22 announce a conditional event order involving W2 given W1 and W3, while the subsequent displayed hypotheses prove that W1 and W2 imply W3. The complete event counts for its actual strategy are:

- (W1,W2,W3)=(0,0,0): 20 input pairs
- (0,1,0): 12 pairs
- (1,0,0): 12 pairs
- (1,1,1): 20 pairs

Consequently W1 intersect W2 equals W1 intersect W3, both of mass 5/16, and both relevant conditional probabilities equal 1. Equation (21) and the final numerical value are correct. The authored direct-count presentation is an exposition clarification; it must not be described as exposing a false probability or disproving the source's strategy.

## Authored-proof correction during audit

One preliminary sentence incorrectly suggested that arbitrary shared-randomness correlations are quantum-realizable in dimension one. It was corrected before acceptance: deterministic strategies are realizable in dimension one, which suffices for the value inequality; general finite shared-randomness correlations have finite-dimensional quantum realizations. No upper bound or witness required alteration.

## Independent verification and actual controls

The proof's two authored verification implementations were read before execution. No source-author program was run. A third independent verifier imports neither candidate implementation and reconstructs the game event predicate, all witnesses, the capacity relaxation, and rational marginal checks.

The third route checks 512 universal winning input/output events, all 432 local question/answer degree cases, the entire edge-count range 0 through 64 for the vertex inequality, all 27,225 composition pairs, all 20 classical winners, and all 192 NS support events.

All three implementations pass under normal Python, -O, and -OO. Sixteen actual malformed-certificate cases yield 41 scoped verifier rejections in each mode. Mutations include wrong model, bottom encoding, input order, witness score or answer, deleted winner, corrupt relaxation witness, negative or incorrect NS mass, missing/duplicate NS events, corrupt NS output, bad dual weight, and malformed schema/duplicate JSON keys. The first two routes are mathematical checkers, not complete schema validators; route B intentionally does not consume the relaxation-maximizer list, and the third route supplies full schema and corresponding metadata checks. This is recorded as test scope, not hidden.

All failures are enforced by explicit exceptions, not removable Python assertions. A closed exact-file manifest and independent external hash anchor protect the final audit packet. Actual post-seal controls cover missing, extra, modified, same-size-corrupted, re-manifested, and symlinked members under all three interpreter modes. Validation receipts are separately hash-pinned after their creation to avoid a circular manifest dependency.

## Dependencies and literature boundary

The mathematical proof uses only the original finite game definition, elementary convexity/counting, exact rational arithmetic, and explicitly given strategies. The finite verifiers use Python's standard library only. Neither the source's reported exhaustive search nor a numerical optimization is a proof dependency.

Restricted quantum searches and their numerical calibrations are outside this acceptance. Failure to find a better strategy gives no dimension-specific or dimension-independent upper bound. The audit does not certify the implementation or performance of those searches.

Primary sources checked:

1. Schmidt, Storgaard, Walter, Zhao, *Guess your neighbor's input: Quantum advantage in Feige's game*, [arXiv:2510.08484v3](https://arxiv.org/abs/2510.08484v3), 25 February 2026. Relevant text read on PDF pp. 1, 4-7, 18, 21-22; pp. 21-22 also visually checked. Retained PDF: 628,332 bytes, SHA-256 fd843d15b5d5cd409aa5abb0811e4f7dec47f439d1cf2d471db5b27d36acae43.
2. *Noncommutative Harmonic Analysis and Quantum Information*, [Oberwolfach Report 4/2026](https://ems.press/journals/owr/articles/14299906), DOI 10.4171/OWR/2026/4, published 21 July 2026. Relevant text read on PDF pp. 23-25. Retained PDF: 553,570 bytes, SHA-256 aa32c629a15785ed194a5ff8f625d0fecf20db43953c47065b4931a909890f76.

Primary metadata pages were independently opened on 11 October 2026. This is a bounded version and source check, not a proof of global current literature status. Neither complete source document was audited in full.

## Public-edition boundary

This edition publishes the authored proof, mathematical audit and scoped acceptance, together with public source and verification metadata. The prose above preserves the complete audit of the accepted baseline claims, including the corrected shared-randomness sentence, source-event clarification, computational coverage limits and unresolved quantum target. It does not distribute executable checkers, solver files, raw outputs, expanded event or capacity lists, copied third-party source text, private sources, personal data or coordination material. The exact formulas and compact case analysis in PROOF.md suffice to follow every mathematical claim accepted here. Integrity hashes authenticate bytes; they are not proofs of mathematical truth or grants of redistribution rights.

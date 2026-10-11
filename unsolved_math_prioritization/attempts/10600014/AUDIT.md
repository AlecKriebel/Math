# Audit of the virtual Brauer projector component

This AI-assisted, unrefereed edition records an internal AI mathematical audit. Acceptance is limited to the expressly stated projector component and parameter criterion; it is not external human peer review or formal proof-assistant certification. The full original recoupling problem remains PARTIAL. This is a written proof/correction/audit edition, not a computational reproduction package. Source inspection and exact mathematical checks described below occurred in the preceding audit on 11 October 2026. Editorial preparation authenticates the retained records without claiming a fresh scholarly-source inspection or a new mathematical-program run.

## Decision

ACCEPT the specific symmetric annihilating projector theorem, recurrence, and coefficient formula in the free diagram algebra B_n(d)=VTL_n(d), over C(d) and every complex specialization admitted by the source's recurrence. The accompanying general proof is independent of the printed inductive argument. Its direct coefficient equations also establish the exact fixed-rank exceptional set.

The original problem remains PARTIAL. No full recoupling theory and no classification of all primitive idempotents is accepted by this audit. Two separately checked statements in the inspected preprint's Section 6 are false as printed and are explicitly excluded from the accepted component.

## Primary source identity and inspection

Primary source: Qingying Deng, Xian'an Jin, and Louis H. Kauffman, Projectors in the Virtual Temperley-Lieb Algebra, arXiv:2103.11355v1, https://arxiv.org/abs/2103.11355v1 . The arXiv record states submission on 21 March 2021; the retained PDF is 24 pages and bears that v1 identifier. Its 23 March 2021 typesetting footer is a separate date.

Retained PDF: 271,213 bytes; SHA-256 1755b463ec0926b652366eea413a7c5a7127fd0a94895e1f4a35e724b8cbcd6d.

Retained extracted text: 68,642 bytes; SHA-256 d4f8b4c1d5962d41b18ea358482fa675cc736dc4aa4cdc7245d8d0921cd9983c.

The entire extracted text, pages 1-24, was read in bounded batches. Pages 1 and 3-22 were visually inspected in rendered form, including every page of the relevant proof chain. Page 2 and the reference-list pages 23-24 were read as text, not visually certified. Complete PDF retrieval is not being equated with full visual inspection.

Original problem source: Roger Fenn, Denis P. Ilyutko, Louis H. Kauffman, and Vassily O. Manturov, Unsolved Problems in Virtual Knot Theory and Combinatorial Knot Theory, arXiv:1409.2823v1, https://arxiv.org/abs/1409.2823v1 . Problem 14 is on retained PDF page 27. That complete page was read and visually inspected. The first-page text was also read to establish title, authors, and version.

Original PDF: 774,711 bytes; SHA-256 ad59ace54d3ad6fb630eee8376c87a34af0340fe5a469daba97d53080ba3fa53.

This audit uses the retained preprint. The preceding retrieval record reports HTTP 403 at the publisher page; no journal PDF was inspected or compared. The arXiv abstract record was separately opened during this audit to verify the versioned citation and submission date. No old placeholder identifier is treated as a citation. These findings make no claim about corrections in an uninspected journal edition.

## Source claim map

- Pages 3-4 specify C(d), the pairing model, dimension (2n-1)!!, and the e_i and v_i generators.
- Page 6, Definition 2.5, supplies the three-term recurrence and its finite exclusion set {0,-2,...,-2n+4}.
- Pages 7-11, Lemma 2.6, give the simultaneous inductive identities. These pages were read fully, including the virtual-invariance calculation.
- Pages 11-12, Proposition 2.8, characterize the unique nonzero idempotent using BOTH-sided e_i annihilation and BOTH-sided v_i invariance.
- Pages 12-13, Lemma 3.1, simplify the recurrence using a restricted collection of diagrams.
- Pages 14-16 identify the equal-coefficient orbits by through-strand count and compute the first non-permutation coefficient.
- Pages 16-20, Lemmas 5.1-5.2, Proposition 5.3, and Corollary 5.5, derive the coefficient recurrence and explicit orbit-sum formula. The full proofs and figures were inspected.
- Pages 21-22 define the closure trace and state the two later results discussed separately below. They are not imported into the accepted proof.

The proof in PROOF.md reconstructs the accepted statements from diagram factorization, an augmentation character, a complete four-case contraction-preimage count, and a three-dimensional corner argument. The ring and specialization arguments are explicit. No printed auxiliary lemma is left as an unverified imported mathematical dependency.

## Corrections and qualifications in the printed target proof

These are statements about the exact inspected v1, not a journal-version comparison.

1. In the calculation for Lemma 2.6(6_{i+1}) on page 11, two consecutive lines print an extra y_i multiplying the term whose coefficient comes from z_i. Direct expansion of the preceding parenthesis gives z_i, not z_i y_i. The final asserted identity uses z_i. This is a local display error; the independent corner proof bypasses it entirely.

2. The auxiliary identities in Lemma 2.6 involving e_i or v_i require i<n when written in B_n. For i=n they must be interpreted in a larger ambient algebra after adding a strand. The target characterization itself uses only i<n and is well-defined.

3. On page 17, a diagram in U^i is in B_{n+1} and has one upper and one lower pair, so its through-strand count is n-1. The printed count n-2 is an index slip. A permutation diagram there has n+1 through strands. These slips do not occur in the accepted formula after consistent indexing.

4. Equation (5.2) on page 19 must sum over the k-dependent sites i in {k+1,k+3,...,n}, as the preceding text states. The printed lower index does not specify that set. The subsequent conclusion counts (n+1-k)/2 sites, which is the intended set's size. The direct contraction count in PROOF.md avoids relying on that display.

5. The coefficient functions and auxiliary alpha expression are rational functions. At i=1, apparent d-2 factors in unsimplified auxiliary displays are removable; the source explicitly supplies x_0=1,y_0=z_0=0,alpha_0=d. They do not justify excluding d=2. The accepted proof has no such artificial division.

6. Generic identities do not authorize substitution at a true denominator zero. The source's recurrence excludes E_n={-2j:0<=j<=n-2}. The fixed-rank formula has poles only at P_n={-2n+2l+2:1<=l<=floor(n/2)}. The audit proves the distinction rather than asserting that all recurrence-excluded parameters are solved by formal substitution. At P_n it proves nonexistence of this exact idempotent; at E_n minus P_n it proves the formula directly in the specialized free diagram algebra.

The source's uniqueness argument uses the permutation coefficient 1/n!, not the identity coefficient 1 familiar from the planar Jones-Wenzl convention. Virtual invariance cannot be removed from the accepted characterization. The sign idempotent (1-v_1)/2 in B_2 already demonstrates why.

## Separate checks on Section 6 of the inspected v1

These checks limit source acceptance. They are not prerequisites for the projector proof and do not assert anything about an uninspected later version.

### Lemma 6.1 trace normalization

Pages 21-22 define trace by connecting corresponding external vertices and explicitly give tr(1_n)=d^n. Thus it is the unnormalized diagram closure trace. In rank 2, closing the identity produces two loops, while closing e_1 or v_1 produces one. Therefore

    tr(1_2)=d^2,    tr(e_1)=d,    tr(v_1)=d.

Using the source's own rank-2 projector,

    tr(F_2)=d^2/2 - 1 + d/2 = (d+2)(d-1)/2.

The printed Lemma 6.1 gives d(d+2)(d-1)/2 at n=2. At the admissible parameter d=3 these are 5 and 15. This is a counterexample using exactly the stated closure convention and normalization, not a competing normalized trace convention.

The extra factor is d^(n-1). Multiplying the source's preceding alpha factors, with alpha_r=(d+r-2)(d+2r)/((r+1)(d+2r-2)) for r>=1 and tr(F_1)=d, instead gives

    tr(F_n) = (d+2n-2) product_{j=1}^{n-1}(d+j-2)/n!.

The telescoping is a rational-function computation. It agrees with direct exact diagram closures for n=1,...,6. Only the rank-2 calculation is needed to reject the printed formula.

### Proposition 6.2 reduced words

Page 22 defines a reduced word as a generator word not equal to a scalar multiple of any shorter word. In B_3, take

    w=v_2 v_1 v_2.

This is the permutation reversing three positions, with three through strands. A word containing any e_i has at most one through strand in rank 3 and cannot represent w, even up to nonzero scalar. Among words in v_1,v_2, lengths at most 2 give only the identity, the adjacent transpositions, and the two 3-cycles. None is the reversal. Equivalently its inversion number is 3. Thus w is reduced under the stated definition and contains v_2 twice, contrary to the assertion that every reduced word contains at most one occurrence from {e_2,v_2}.

There is another reduced expression v_1 v_2 v_1 with a single v_2. That illustrates a weaker possible statement about choosing representatives; it does not prove the printed assertion about an arbitrary reduced word. The countercheck exhaustively examines the 31 words of length at most 2 in {1,e_1,v_1,e_2,v_2}.

## Exact computation and limits

The independently authored code executes no source-author code. It uses perfect matchings and diagram stacking. Two separate composition implementations, disjoint-set components and adjacency traversal, agree on all products through n=4 (11,260 pairs in total). Associativity is exhaustively checked through n=3 (3,403 triples). Two hundred elementary generator-relation checks cover n=2,...,6.

The complete contraction-preimage coefficient count is checked on both sides, for every adjacent generator and every output diagram, through n=6; the rank-6 algebra has 10,395 basis diagrams. Symbolic idempotence and permutation invariance are checked through n=5, including all 893,025 input products at rank 5. The exact recurrence is checked coefficient by coefficient through n=5. There are 331 selected exact parameter checks through n=20, including source-admissible values, removable tower obstructions, and genuine fixed-rank obstructions.

Negative controls detect a sign error in the first contraction coefficient and expose the antisymmetrizer when virtual invariance is omitted. A separate executable checks the two Section 6 counterexamples. Normal, -O, and -OO runs pass; checks use explicit exceptions rather than removable Python assertions.

These computations corroborate the general proof. The generic theorem and every admissible specialization are justified by the all-n arguments and ring maps in PROOF.md, not by a finite sample. The exact source model is the free diagram algebra, not a quotient obtained from a particular tensor representation.

## Remaining acceptance boundary

Accepted: the particular symmetric annihilating projector, its exact coefficients, uniqueness under all three conditions, the stated recurrence, the source-admissible complex parameters, and the separately proved sharp fixed-rank parameter criterion.

Not accepted as solved: the full original problem, a useful recoupling construction, all primitive idempotents, all blocks of singular Brauer algebras, positive-characteristic analogues, or the two defective printed Section 6 statements. No journal-version identity or correction is inferred.

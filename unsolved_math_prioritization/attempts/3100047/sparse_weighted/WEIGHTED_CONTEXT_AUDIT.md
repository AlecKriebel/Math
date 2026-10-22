# Independent audit of the four-letter weighted pressing identity

Problem 3100047, campaign row 1747. Audit date: 12 October 2026 UTC.

## Decision

**Accepted, after a terminology correction.** The exact local classification, its weaker support consequence, the Schur-complement substitution identity with the exact integer factor F(S)G(S ∪ Q), the fixed-quadruple coverage criterion, and the five-letter abstract countermodel are mathematically valid. Acceptance applies only to the final report and accompanying original files identified by the weighted-proof, weighted-input-manifest and weighted-authored-evidence records in ORIGINAL_INPUT_PINS.json, not to a moving directory or subsequent revision.

These are partial results. They do not prove the general pressing 1/3–2/3 conjecture, a universal coverage bound, or a classification of all pressing families of any given small cardinality. No claim of novelty was assessed. No repository changes or publication were performed during this independent audit.

## Correction made during review

The initial frozen report said that the abstract language contains “every maximal chain” of its union prefix system. Taken literally in the inclusion poset, this is false. For example,

∅ ⊂ {3} ⊂ {1,2,3} ⊂ {1,2,3,4} ⊂ {1,2,3,4,5}

is a maximal inclusion chain that skips the two-element level. That poset has seven maximal inclusion chains, of which four are complete singleton-addition chains. The required and proved property is precisely completeness for **singleton-addition chains from ∅ to the full set**. The writer corrected the unqualified maximal-chain language and re-froze the report. This changes neither the prefix-splicing counterexample nor any matrix theorem.

No substantive mathematical correction was required.

## 1. Local algebra and exact enumeration

Assume the four distinct labels are a,b,c,d and abcd is a successful full-length pressing order for a symmetric matrix B over F2. Each successful pivot has value one. Recording its current column as the corresponding instructional row gives the unique unit upper-triangular factor B=UᵀU in that order. Write its upper entries as p,q,r,s,t,u in positions ab,ac,ad,bc,bd,cd.

For consecutive pivots with residual 2×2 block [[1,e],[e,f]], success in the original order gives f+e=1. The reversed order is legal exactly when f=1, equivalently e=0. When e=0, the two full residual columns are orthogonal at those coordinates and the rank-one updates commute, including every outside coordinate. Thus the two forbidden swaps bacd and acbd force p=s=1, whereas the permitted swap abdc forces u=0.

Because cdab is successful, its initial c pivot has diagonal one. The Gram formula gives B_cc=q+s+1=q, so q=1. Its third prefix {c,d,a} has determinant one. Since det B=1, the complementary cofactor formula gives det B[{a,c,d}]=(B⁻¹)_bb. The b row of U⁻¹ is (0,1,s,t+su), whose F2 self-product is 1+s+t+su=t when s=1 and u=0. Hence t=1. Only r remains free.

The resulting two matrices agree exactly with the displayed B_0 and B_1 in the report. Direct pressing gives:

- r=0: abcd, abdc, cdab, cdba;
- r=1: abcd, abdc, cdab, dcab.

The report's branch-by-branch proof exhausts the legal initial pivots and every subsequent pivot choice. Its instructional-class counts are also correct. In the first pair, c and d commute; in the other pair, either a and b commute after c,d or c and d commute initially. The first class has a nonzero a-to-c instruction while the other class presses c before a and consequently has zero in that position. The two classes are therefore distinct and both have size two.

Every cross-pair in {a,b}×{c,d} is forward in exactly the first two words and backward in the other two. Its local probability is exactly 1/2. Removing the two forbidden-word hypotheses gives the stated support implication by a valid case split: either one forbidden word is present, or the exact classification forces cdba or dcab.

Independent finite verification covers **all 1,024 symmetric 4×4 matrices**, rather than only the writer's 64 upper-triangular roots. Of these, 448 are nonsingular and 402 admit a successful full-length order. The support antecedent holds in six matrices; none violates its conclusion. Exactly two matrices satisfy all five hypotheses, and their complete families and root-class counts are exactly as claimed. These counts are verification results for the local identity, not evidence of an unproved general balance theorem.

## 2. Prefix and suffix counts, with accessibility kept separate

For a subset S, a prescribed order is a legal pressing prefix exactly when each of its leading principal determinants is one. Indeed, scalar Schur elimination identifies each pivot with the ratio of successive determinants; over F2 every nonzero ratio equals one. Consequently the F recurrence counts reachable determinant flags. Nonsingularity of A[S] alone is not sufficient for F(S)>0.

For a nonsingular principal set T, let R_T be the full Schur complement on the remaining vertices. For every remaining set X,

 det R_T[X] = det A[T ∪ X] / det A[T].

This is the ordinary block determinant identity, valid even if T has no legal ordering. Since the denominator is one, the G recurrence counts the complete determinant flags in R_T. A nonsingular R_T may have no successful ordering, so G(T)=0 remains possible. Extending G by zero at singular T gives exactly the reported recurrence; no accessibility axiom is introduced.

The empty-set and full-set conventions are consistent: the empty determinant is one, F(∅)=1, G(E)=1, and F(E)=G(∅)=Z. The ambient hypotheses include successful pressability, so Z>0 whenever probabilities are discussed.

The writer's explicit three-vertex boundary examples were independently checked by dense direct pressing:

- Packed rows (3,5,2), S={1,2} in zero-based labels: D(S)=1, F(S)=0, G(S)=1. Its selected principal matrix is alternating and inaccessible.
- Packed rows (7,3,5), S={0}: D(S)=1, F(S)=1, G(S)=0. Pressing its first vertex leaves a nonzero alternating residual.

Both complete ambient matrices nevertheless have successful full-length orders. The independent ambient cases additionally exhibit 376 occurrences of inaccessible nonsingular subsets and 310 occurrences of reachable but uncompletable subsets. Those are occurrences across the test cases, not counts of distinct mathematical isomorphism classes.

## 3. Full residual substitution and common multiplicity

Fix the same ordered quadruple (a,b,c,d) throughout, with Q its underlying set. Let S be disjoint from Q and satisfy F(S)>0. Eliminating any legal prefix with set S gives the full residual R_S, independent of the prefix order. This follows directly from the Schur-complement formula for symmetric elimination, not from an assertion that all feasible sets are accessible.

While pressing vertices only in Q, each diagonal and off-diagonal entry within Q is updated using only entries within Q. Thus a four-letter order is legal in the full residual exactly when it is legal in the principal restriction B_S=R_S[Q]. Vertices outside Q do not alter these internal pivot tests. For any successful order of B_S, eliminating all four vertices produces the same full residual on E\(S∪Q). The Schur-complement quotient identity identifies it with R_(S∪Q), including all entries among outside vertices.

It follows that concatenation is a genuine bijection:

legal orders of S × successful full orders of B_S × successful full orders of R_(S∪Q)

with full successful words whose prefix set is S and whose next four positions consist of Q. The reverse map reads the three pieces of a full word. Therefore every individual local word has exactly F(S)G(S∪Q) extensions, including interactions with every outside vertex. The formula does not assume that suffix feasibility follows from nonsingularity; G explicitly imposes it.

For a qualifying S, the local theorem supplies exactly four words and two occurrences of each direction of every fixed cross-pair. Hence this context contributes four times its weight overall and twice its weight to each cross-pair direction.

## 4. Disjointness and the coverage boundary

The context subfamilies are disjoint as S varies because a permutation containing the fixed set Q consecutively has a unique Q block and a unique set of labels preceding that block. This argument relies on Q being fixed. One must not sum the same formula indiscriminately over differently chosen quadruples or allow the target pair to change between contexts.

Summing over qualifying S gives |H|=4W and counts 2W in each direction of every pair in the same fixed set {a,b}×{c,d}. If c is its total forward count, the remaining Z−4W words can contribute anywhere between zero and Z−4W, so

 2W ≤ c ≤ Z−2W.

Thus 6W≥Z implies Z/3≤c≤2Z/3 for each of the four fixed cross-pairs. Since |H|=4W, this is exactly the sufficient coverage condition |H|/Z≥2/3. Equality is included correctly. The result is not a necessity claim and supplies no unconditional lower bound on W.

The report's explicit five-vertex example was checked independently. Its packed rows are (19,13,2,10,1), its complete successful family is exactly

12345, 12354, 14523, 15423, 41523, 42315,

and Q=(2,3,4,5) in one-based labels has the sole qualifying prefix set {1}. Here F=G=W=1, Z=6, |H|=4, and exactly two words put 2 before 4. Therefore the claimed coverage and probability attain 2/3 and 1/3 respectively. The first four listed words are precisely H.

## 5. Abstract countermodel and non-realizability

For L={12345,12354,12435,34125}, independent enumeration finds exactly the eleven reported prefix sets. The complete singleton-addition chains from ∅ to the full set yield exactly these four words. Relative to 12345 the inversion sets are ∅, {45}, {34}, and {13,14,23,24}. They are pairwise disjoint. Every pair therefore has minority count zero or one; no count is two, the only balanced count for a four-word family. The majority order 12345 belongs to L.

For non-realizability, use Q={1,2,3,4}. The three successful ambient words 12345,12435,34125 have the common remaining suffix 5 and supply precisely the required local successes. If 2134 or 1324 were successful locally, the substitution identity would append the same suffix 5, contradicting the exact proposed language. The local theorem therefore forces 3421 or 4312, and appending 5 gives an additional full successful word. This is a valid contradiction.

The same reasoning survives any fixed common outside prefix and suffix: first eliminate that legal prefix, then substitute the local Q block, then append the unchanged successful remaining suffix. Arbitrary interactions with outside vertices are already covered by the full Schur identity. This is an exclusion of the exact stated language with that padding, not a classification of every possible four-word family.

## 6. Reproducibility and acceptance boundary

The independent verifier uses dense 0/1 matrices and ordinary permutation-based principal-determinant flags, and compares those families to an independently implemented rank-one pressing recursion. It does not import the writer's verifier. It checks:

- all 1,024 symmetric four-vertex matrices and all their full permutations;
- all 120 permutations for the abstract five-letter system;
- all 90 authored ambient examples, matching Z, W, |H|, context support, common local-word multiplicities, and fixed cross-pair bounds;
- 30 additional relabelled or reordered-quadruple examples, including 20 zero-weight cases;
- every nonsingular principal set against direct prefix and residual suffix pressing for 51 of the original ambient examples, ten extra relabelled examples, and the explicit endpoint example;
- the two explicit zero-weight boundaries and the exact endpoint example.

The writer's frozen verifier was rerun independently under normal Python, -O, and -OO. All three outputs exactly match the frozen output bytes. The independent verifier was likewise run in all three modes, with identical outputs and fail-closed RuntimeError checks rather than optimization-sensitive assertions.

The authored mathematical proofs, rather than finite ambient samples, establish the general conditional identities. The original acceptance binds the accepted final inputs by byte count and SHA-256; the original audit manifest binds the audit artifact set, and its external seal pins that manifest. ORIGINAL_INPUT_PINS.json identifies these originals, and ACCEPTANCE.json records their accepted scope for this separate public edition. Any substantive edit to the accepted inputs requires a new audit decision.

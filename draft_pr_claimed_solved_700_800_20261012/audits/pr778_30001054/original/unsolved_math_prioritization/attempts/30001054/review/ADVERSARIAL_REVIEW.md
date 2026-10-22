# Adversarial review of the double permutation scope correction

Problem 30001054, rank 818. Review date: 2026-10-06.

## Verdict

**ACCEPT THE WEAK-AXIOM COUNTEREXAMPLE, WITH THE SCOPE ADDENDUM BELOW.**

The word in the rebuilt packet satisfies the four conditions printed in Goodman--Pollack Corollary 11 and adopted by Definition 12. It cannot be the tangent encoding specified in that paper, including its connected-set and pseudoline version. I found no additional abstract-input condition in the inspected definition or surrounding material that excludes it.

Preserve the historical affirmative attribution for the intended, properly constrained allowable-interval/fibration problem. Do not classify that established topological representation theorem as false. Also do not describe this witness as a counterexample to the separate polygonal problem when its fully separated starting-term clause is imposed.

## Independent mathematical verification

Let A=(1,2,1',2'), B=(1,2,2',1'), and C=(2,1,2',1'). Let P be the doubly infinite repetition of

A, B, A, B, C, B, C, B.

Each term is an endpoint-respecting permutation. Each consecutive pair, including the last-to-first transition, differs by one adjacent swap of endpoints belonging to different bodies. Let R reverse a term and interchange primed and unprimed symbols. Since R(A)=C, R(C)=A, and R(B)=B, P[k+4]=R(P[k]) for every integer k. The least period is eight: it divides eight, and periods one, two, and four would all imply P[0]=P[4], contrary to A≠C. Finally, eight is the required value 8·C(2,2).

The post-switch ordered pairs are

(2',1'), (1',2'), (2',1'), (2,1), (1,2), (2,1), (1,2), (1',2').

The supporting types (1,2), (2,1), (1',2'), and (2',1') each occur twice. The separating types (1,2'), (2,1'), (1',2), and (2',1) never occur.

The obstruction is already part of the topological target's specification. Each pair of connected sets must have two internal and two external tangent pseudolines, together with a strict separator. Encoding the two directions of an internal tangent gives mixed primed/unprimed switch events. The required internal tangents therefore cannot produce a word having no mixed events. This reasoning does not assume straight tangents, Euclidean convexity, or global stretchability. Goodman--Pollack's stronger necessary condition in Proposition 10 is consistent with this direct contradiction. [Goodman--Pollack, pp. 3--9](https://math.nyu.edu/~pollack/pubs/dblperm11-26-06.pdf).

Changing the starting phase, traversal direction, or body names cannot change the absence of separating events. The witness has no stationary or simultaneous transitions. Its repeated nonconsecutive terms do not violate simplicity, which concerns a single switch at each step. Requiring all eight terms to differ would also exclude every genuine n=2 eight-event encoding: only six endpoint-respecting permutations exist. No n≥3 restriction or reduced-word/minimum-path condition appears in the inspected four-axiom definition.

## Definition and theorem checks

The Goodman--Pollack manuscript separates its necessary switch conditions in Proposition 10 from the four term-sequence conditions in Corollary 11. Definition 12 explicitly chooses the latter. The surrounding general-position assumptions govern the geometric families and their tangent events; they do not insert an unprinted switch-once condition into that standalone definition. [Author manuscript, pp. 3--9](https://math.nyu.edu/~pollack/pubs/dblperm11-26-06.pdf).

Dhandapani--Goodman--Holmsen--Pollack distinguish cyclic interval sequences from allowable interval sequences. The latter require each directed separating and supporting type once per period. Simplicity alone requires a single ordered-pair switch per step. The witness is simple and cyclic but fails allowability in this stronger sense. Their pre-switch convention reverses the ordered pairs relative to the reviewed packet; it does not alter the multiplicity obstruction. [Author manuscript, Section 2, pp. 4--6](https://math.nyu.edu/~pollack/pubs/interval.pdf).

Habert--Pocchiola Theorem 49 has a fibration of an arrangement of pseudocircles as its input. The surrounding definitions impose specified two-curve arrangement types, and the fibration preserves the relevant pencil/direction ordering. Page 76 identifies the intended allowable encodings with those fibrations. This is a representation result for that constrained input, not a theorem that an arbitrary weak four-axiom word determines such a fibration. The inspected theorem and its stated application support retaining the affirmative attribution. This review does not independently reprove the representation theorem. [Accepted manuscript, Section 6, pp. 74--76](https://arxiv.org/pdf/1101.1022).

## Required distinction between the two OWR questions

The relevant topological question is Question 1 on printed p. 2492, following Definition 2. Its answer is immediately credited to Habert and Pocchiola, with the discussion continuing on p. 2493. The separately numbered problem-session item 12 on p. 2551 repeats the four weak conditions and requests a polygonal construction. These are distinct passages. [OWR 44/2008, pp. 2491--2493 and 2551](https://ems.press/content/serial-article-files/46191?nt=1).

The last paragraph of item 12 additionally refers to the term (1,1',2,2',...,n,n'). If this is interpreted as a required starting term, the present witness is inadmissible for that restricted request. More generally, that extra condition repairs the multiplicity defect:

**Fully separated start lemma.** Suppose a word satisfies the four weak conditions and contains E=(1,1',2,2',...,n,n'). Shift its phase so that P[0]=E. The term half a period later is R(E)=(n,n',...,2,2',1,1'). Every endpoint of body i must reverse order with every endpoint of body j for each i<j. There are four such unordered endpoint pairs per body pair, hence 4·C(n,2) required pair crossings. A single adjacent swap changes the relative order of exactly one pair. The stipulated half-period has exactly 4·C(n,2) swaps. It therefore crosses every required pair exactly once and has no spare steps for backtracking. The second half restores every endpoint pair, giving each directed cross-body switch once per full period. Thus a weak word containing E is switch-once.

This lemma is an additional scope check, not a solution or a claimed construction for the polygonal request. The four-axiom definition remains insufficient without that extra starting-term hypothesis. The lemma does not weaken the counterexample to the unrestricted abstract definition.

## Independent finite checks and packet replay

The new checker imports no code from the reviewed packet. It enumerates all 6^4=1296 possible first halves, derives the second halves by reverse-toggle, and independently tests every transition and all potential shorter periods. It obtains:

- 48 rooted primitive eight-term weak words
- 16 switch-once words
- 32 non-switch-once words, all with zero separating events
- 16 words containing a fully separated term; all 16 are switch-once

These are rooted words, not isomorphism-class counts. Thirty-two phase/reversal/relabeling checks preserve the witness. A genuine switch-once example and two invalid controls behave as expected. Normal and optimized Python runs agree, and a relocated optimized run agrees.

The rebuilt packet's own 44 CLI controls, 24 integrity controls, witness check, and package verifier pass. All four supplied primary PDFs were rehashed against the declared identities, and the package verifier passes with those external PDF bytes. These checks certify finite claims and pinned artifacts; they do not prove the imported topological theorem.

The input archive is 20,762 bytes, SHA-256 ad0e79032522c72ee0015336e11f53f2a58c66fa1b5be17478d72f0f4416edba. Its 14 members match the receipt and the supplied extracted copies. It was preserved unchanged. No unavailable original author archive or dataset corpus was replayed or recertified. The source-definition finding concerns the inspected author manuscripts and OWR passages; this review does not claim to have inspected the inaccessible final Goodman--Pollack journal PDF.

## Recommended disposition text

The intended topological realization problem for properly constrained allowable interval sequences has an affirmative solution due to Habert and Pocchiola. The four conditions printed in the inspected Goodman--Pollack/OWR definition do not by themselves characterize that input: the explicit period A,B,A,B,C,B,C,B satisfies them but cannot encode the required internal tangents. Treat the literal four-axiom universal statement as false and retain a scope warning on an otherwise affirmative literature classification. The separate polygonal request, if restricted to a fully separated starting term, is outside this counterexample's scope.

No novelty claim, Euclidean realization claim, polygonal construction, or independent proof of the representation theorem is made.

# Mandatory scope correction: problem 30001054

Audit date: 2026-10-06. This is a source and definition audit, with no novelty claim.

## Corrected disposition

- **Literal four-axiom formulation: false.** The finite witness below satisfies the four printed axioms and cannot have the specified tangent/separator realization.
- **Switch-once allowable-interval/fibration formulation: affirmative in the literature**, credited to Luc Habert and Michel Pocchiola.
- **Unqualified catalog or author-package acceptance: NEEDS_SCOPE_CORRECTION.** Do not describe the literal four-axiom statement as covered by the representation theorem without changing or clarifying its input definition.

The historical attribution and the definition gap must both be retained. This audit neither refutes the representation theorem nor independently reproves it.

## Explicit witness and elementary verification

Write a prime for the right endpoint. Set

- A = (1, 2, 1', 2')
- B = (1, 2, 2', 1')
- C = (2, 1, 2', 1')

Repeat the eight terms A, B, A, B, C, B, C, B in both directions.

Every term contains each of 1, 1', 2, 2' once, with i before i'. Every transition, including the final B to the next A, swaps one adjacent pair from different bodies. There are no stationary transitions, simultaneous swaps, same-body swaps, or nonadjacent swaps.

Let R reverse a term and toggle every prime. Then R(A)=C, R(C)=A, and R(B)=B. Consequently P[k+4]=R(P[k]) at every phase. The sequence has period eight. Its least period is eight: a smaller least period would divide eight, whereas P[0]=A differs from P[4]=C, ruling out periods 1, 2, and 4. Its length is exactly 8 binomial(2,2), as required by the fourth printed axiom.

Under the post-switch convention used in the OWR contribution, the eight ordered switches are

(2',1'), (1',2'), (2',1'), (2,1), (1,2), (2,1), (1,2), (1',2').

Thus each of the four supporting switch types occurs twice; none of the four mixed primed/unprimed separating switch types occurs. A valid tangent encoding has two internal and two external undirected tangents for each pair of bodies. Over a full directed turn, each internal tangent contributes separating events. In particular the four mixed ordered switch types for this pair cannot all be absent. This necessary condition is also stated in Goodman--Pollack Proposition 10. The witness therefore has no realization of the required kind.

This obstruction is invariant under renaming the bodies, reversing the traversal, or changing the starting event. It is not caused by repeated equal consecutive terms or a smaller fundamental period. Calling the sequence simple in the interval-sequence sense does not exclude it: every step already consists of a single pair swap. Requiring all terms to be distinct would be a different condition and is not printed; for n=2 there are only six endpoint-respecting permutations, fewer than the stipulated eight event terms.

## Where the stronger hypothesis enters

Goodman--Pollack's author manuscript, Proposition 10 and Corollary 11 on p. 8, separates a strong necessary switch condition from four weaker properties of the term sequence. Definition 12 on p. 9 refers only to the latter four properties. OWR problem-session item 12, printed p. 2551, reproduces those four properties. The weakness is therefore present in the source definition itself, independently of that item's additional polygonal-construction request.

Dhandapani--Goodman--Holmsen--Pollack's *Interval sequences and the combinatorial encoding of planar families of pairwise disjoint convex sets*, manuscript pp. 4--5, explicitly requires each directed supporting and separating switch for distinct labels to occur once per period. It also defines simplicity as a single ordered-pair switch per step. Its switch convention is before the move, while OWR's is after; reversing each ordered pair does not change the omitted-type or multiplicity obstruction.

Habert--Pocchiola Theorem 49, manuscript p. 75, assumes a specified fibration of an arrangement of pseudocircles in a Moebius strip and realizes that fibration. The discussion on p. 76 identifies the intended allowable-interval/double-permutation encodings with fibration classes. A word satisfying only the four weak axioms need not encode such a fibration: the witness fails the required two-body event pattern. The theorem's fibration hypothesis cannot be discarded by citing that discussion.

## Replacement wording

A defensible status statement is:

“The intended realization problem for properly constrained allowable interval sequences, in particular the simple switch-once double-permutation setting, has an affirmative topological solution due to Habert and Pocchiola. However, the four-axiom definition printed in the earlier source is insufficient as written: the period A,B,A,B,C,B,C,B above satisfies those axioms but omits every internal-tangent switch. The literal four-axiom universal statement is false; an unqualified affirmative classification requires a scope correction.”

No Euclidean stretchability claim, explicit polygonal construction, independent proof of the imported theorem, or novelty claim is made.

## Primary sources

1. [OWR 44/2008, printed pp. 2491--2493 and 2551](https://ems.press/content/serial-article-files/46191?nt=1).
2. [Goodman--Pollack author manuscript, pp. 8--9](https://math.nyu.edu/~pollack/pubs/dblperm11-26-06.pdf).
3. [Dhandapani--Goodman--Holmsen--Pollack author manuscript, pp. 4--5](https://math.nyu.edu/~pollack/pubs/interval.pdf).
4. [Habert--Pocchiola accepted manuscript, Section 6, pp. 74--76](https://arxiv.org/pdf/1101.1022).

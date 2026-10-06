# Turn 4: the thirty-letter case and the complete convention-qualified classification

Four substantive author turns. Complete candidate for the original fixed-generator positive-word problem, pending full independent source/proof/computational review. Author search stops here; a fifth turn is not spent merely to reach a quota. No novelty certification.

## 1. The remaining finite braid theorem

**Six-strand theorem.** Every positive braid word on six strands in which every pair of labelled strands crosses exactly twice represents the full twist z=(a1a2a3a4a5)^6 in B6.

This theorem is established by the exhaustive exact certificate below. We do not claim it for an arbitrary number of strands or infer it from experiments with fewer strands.

Turn2 proves that a positive thirty-letter word representing c² in G has every pairwise pure linking number1. Positivity means every labelled pair therefore crosses exactly twice, so the six-strand theorem applies. Thus every such word equals z already in B6. The classical positive braid monoid embedding and the Hurwitz implementation of braid relations from turn2 imply that its factor tuple is strictly Hurwitz equivalent to the standard thirty-term tuple z. No faithfulness of G→Mod or G→Aut(F4) is needed for this step.

## 2. A finite directed acyclic graph covers every candidate word

Index the fifteen unordered pairs of labels{0,...,5} in lexicographic order. A crossing state has counts c_ij in{0,1,2}, encoded as

    code(c)=sum_(i<j) c_ij*3^index(i,j).

Retain also the ordered list p of strand labels at the six horizontal positions. Initially all counts are0 and p=(0,1,2,3,4,5). At position i, a positive generator interchanges the two currently adjacent labels a=p_i and b=p_(i+1). It increases c_ab by1 and leaves the other counts unchanged. The transition is allowed if and only if c_ab<2.

This is a finite graph with at most3^15 count vectors. Along every edge the sum of the counts increases by1, so it is acyclic and has depth at most30. There is no imposed search-depth or state cap beyond these exact defining bounds.

The permutation is determined by the parities of the pair counts: the relative order of two labels reverses precisely when their mutual crossing count is odd. Whenever a count vector is reachable, those relative comparisons determine its actual ordering uniquely. The implementation checks that any second path to a count vector gives the same permutation. Merging by the count vector therefore loses no available continuation.

Let R be the set of all states reachable from the empty state. Breadth-first expansion explores every allowed edge from every discovered state until the queue is exhausted. It obtains234368 states and711342 outgoing edges. In particular the full vector f, whose fifteen counts are2, is reachable; its permutation is the identity. Every word in the six-strand theorem is a path from0 to f, and conversely every such path is a word of the required kind.

## 3. Which reachable states can lead to the full state?

A state c in R can continue to f if and only if f−c belongs to R.

To prove necessity, take a suffix from the permutation at c to the final identity. Reverse its sequence of adjacent transpositions, keeping all generators positive. This starts at the identity and ends at the permutation at c; its labelled pair counts are2−c_ij. Thus f−c is reachable.

Conversely, a path from the identity to the count vector f−c ends at the same permutation as c, because2−c has the same pair parities. Reverse its sequence of generators. Starting at that common permutation, it ends at the identity, crossing each labelled pair2−c_ij times. It is a permissible continuation after c, and no intermediate count exceeds2 because all added counts are nonnegative and their final values are exactly2−c_ij.

Reversal here is reversal of the positive word, not its group inverse; it reverses the combinatorial trajectory of the adjacent swaps. The positive crossing counts and label pairs remain the required ones. This argument only identifies possible suffixes, not equalities of braid elements.

Let S={c in R:f−c in R}. Every complete path lies in S, and every state in S is on some complete path. The exact computation obtains90921 states in S and261810 edges with both endpoints in S.

## 4. An exact certificate of path-independent Artin action

Let F6 have free generators x1,...,x6. Use the classical faithful Artin action, in the inverse-generator right-action convention

    A_i(x_i)=x_i x_(i+1) x_i^−1,
    A_i(x_(i+1))=x_i,
    A_i(x_j)=x_j otherwise.

For a word, substitute these automorphisms successively and freely reduce after each step. González-Meneses, *Basic results on braid groups*, §1.6, printed22–24, records the opposite generator convention and faithfulness. Inverting all braid generators and reversing the composition convention are bijections (an automorphism and an anti-automorphism of the braid group), so this convention still detects equality faithfully. The programs implement exactly the tuple action displayed above, including inverse letters inside free words. They do not use numerical matrices or hashes to decide equality.

The breadth-first search records one canonical parent edge for each nonempty reachable state. For every state c in S its canonical parent is also in S: a prefix of a path reaching c can be followed by a completion from c. Define A(c) to be the exact six-tuple of reduced free words obtained along this canonical path.

The certificate checks, for **every** edge c --i--> c' with endpoints in S,

    apply_generator(A(c),i)=A(c')                              (1)

as literal equality of all six freely reduced integer words. All261810 equalities hold. Starting with the identity at0, induction on path length now proves that every path in S from0 to c has action A(c), not just its canonical path. In particular all complete paths have action A(f).

A separate direct computation of the standard positive word z=(a1a2a3a4a5)^6 gives exactly A(f). Faithfulness of the Artin action proves that every complete-path word equals z in B6. This proves the six-strand theorem and the thirty-letter classification.

The argument does not assert that all reachable prefixes have the same braid for a given crossing vector. Only the coaccessible subgraph is used, and every edge in that subgraph is checked. No multiplicity of paths or unknown word equality is collapsed without the explicit comparisons(1).

## 5. Reproduction and certificate identity

Two separately implemented exact programs are supplied:

- check_turn_4.py uses Python's standard library, explicit permutation tuples, dictionaries, free-word reduction and a complete reachable-state queue
- check_turn_4.cpp uses packed permutations, dense parent arrays, a vector queue and exact C++ integer-word reduction

Both construct all reachable states and all coaccessible edges; neither has a cap. Both perform the exact action comparisons before any hashing. The C++ wrapper compiles with an installed C++17 compiler, streams all90921 coaccessible action records sorted by count code, and compares their SHA256 with the Python result:

    af2b8ec569d613e4f3d8ba3b72d18e85e8c612f4265057b7f4c485d544d159bf.

A record contains the count code, packed permutation and all six full reduced words. The full stream is regenerable with the C++ --stream option but is not retained as a large artifact. The digest is an integrity cross-check, not a replacement for exact free-word comparisons. The Python and C++ receipts record the same census and final result.

## 6. Assemble all four turns and state both conventions

The quantified objects are **positive words in the five fixed standard Artin generators a1,...,a5 of the source's quotient**. This is not a classification of arbitrary quasipositive factorizations into conjugates, arbitrary positive Dehn twists, or unframed Lefschetz fibrations without that restriction. Hurwitz moves may introduce conjugate factors as intermediate tuples; the initial word restriction is exactly what permits the crossing arguments.

Turn1 proves the exact possible lengths20,30,40, using the credited topological maximum40 plus the linking obstruction to0/10. Turn3 gives one strict Hurwitz class at length20, represented by h². The present turn gives one strict class at length30, represented by z. Turn2 gives exactly two strict classes at length40, represented by c² and (a2a3a4a5)^10. Their different generated S5 subgroups in the permutation quotient prove they cannot be strictly Hurwitz equivalent. Simultaneous conjugation by a1a2a3a4a5 identifies the two forty-term classes.

Therefore the complete classification is:

- under strict Hurwitz moves alone: **four classes**, one at20, one at30 and two at40; the source's single40-class clause is false under this convention
- under Hurwitz moves plus simultaneous conjugation: **exactly three classes**, represented by h²,z,c²; the proposed list is affirmative under this convention

The source's own brief use of Hurwitz equivalence is not treated as an unequivocal choice between those conventions. Instead both are resolved, avoiding a purely terminological promotion. The remaining unrestricted geometric classifications are outside the stated fixed-generator result.

All classical ingredients are credited. The finite certificate and the full source interpretation require separate independent review before publication or a complete-result announcement. No fifth author search is undertaken after this freeze.

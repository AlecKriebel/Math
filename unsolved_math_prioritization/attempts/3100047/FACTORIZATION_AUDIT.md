# Independent audit: variable-order block factorization

Date: 12 October 2026 UTC. Problem: row 1747 / 3100047 / AMR-030-0047.

Disposition: **ACCEPTED AS A STRUCTURAL REDUCTION.** This is a separately frozen supplement. The previously accepted pressing-balance audit, its input pins, and its reports are unchanged. No unrestricted balance theorem, counterexample, or novelty claim is made.

## Exact statement audited

A is a symmetric nonsingular matrix over F2 with a nonempty family Sigma(A) of successful full-length pressing permutations. The measure is uniform on that family. Join two labels when their order varies among the successful permutations. The connected components of this variable-order graph are fixed-order contiguous blocks in every successful word.

At each block boundary, form the Schur complement after eliminating the earlier blocks, and restrict it to the current block. The resulting matrices B_i are symmetric, nonsingular, and successfully pressable. Concatenation is a bijection from the Cartesian product of their full successful-word families to Sigma(A). There is no shuffle factor. The component words are independent and uniform; internal pair probabilities are unchanged and cross-component comparisons are fixed.

The final authored proof, FACTORIZATION.md, is accepted at SHA256 da725b56d2b250e81845a6b81bdc8fbdb5d93a5442e02730da45baee5e8cb3ef, 6,842 bytes. Its author freeze is separately pinned. No correction to that proof was needed.

## 1. Fixed order and contiguity

The first lemma is valid for any nonempty permutation family. Let uv be a variable edge, and let z lie outside its connected component. Neither uz nor vz can vary. Their fixed comparisons cannot place z between u and v: that would fix the order of u and v in every word, contradicting variability. Thus z is always before both or always after both.

A path of variable edges propagates this common side throughout the component. Applying the same observation along the second component shows that two distinct components have a fixed uniform order between all of their vertices. One actual word certifies consistency and yields the unique total order of components. Every component must therefore occupy a contiguous interval in every word. Isolated vertices, which are singleton components, are covered by the same argument.

The nonempty-family assumption is essential. An invertible alternating matrix can have no legal initial press, so nonsingularity alone does not define these probabilities or provide a reference word.

## 2. Full residual state and the row convention

For a legal prefix with vertex set S, place S first in its pressing order and write

    A = [[P,Q],[Q^T,R]].

The current press columns, transposed into rows, form a rectangular matrix U=[U_S,U_T]. The square block U_S is unit upper triangular. Summing the rank-one updates clears the first rows and columns, giving

    P = U_S^T U_S,
    Q = U_S^T U_T.

Consequently P is nonsingular,

    U_T = U_S^(-T) Q,
    U_T^T U_T = Q^T P^(-1) Q,

and the full surviving state is R+Q^T P^(-1)Q. This uses the same instruction-row convention A=U^T U as the original accepted report. No transposition is missing. It determines every remaining entry, including off-block incidences, from the prefix set alone.

The empty-prefix convention is harmless: no elimination occurs and the residual is A. The author states its main result for a nonempty ground set; the auditor additionally checked the empty matrix as an implementation boundary without extending the balance assertion to it.

## 3. Every local word is substitutable

At a block boundary S_i, both S_i and S_i union C_i are prefix sets of an existing complete successful word. Their principal matrices are nonsingular. The determinant quotient shows that B_i is nonsingular; symmetry follows from the Schur formula. An observed global block word establishes its successful pressability.

Choose any successful full word of B_i, including one not initially selected from a global reference word. Its internal updates are precisely the restriction of the full-state rank-one updates to C_i. Outside entries never enter those internal pivot calculations, because no outside vertex is pressed during the block. Thus every pivot of this replacement is legal in the full residual matrix.

After the whole block is pressed, its cleared coordinates and all remaining entries are determined by the prefix set S_i union C_i. The later residual is therefore identical to the reference residual. The unchanged suffix remains successful. This replacement can be repeated for every coordinate of the block tuple, establishing surjectivity of the product map. The fixed block order makes concatenation injective. Conversely, every global successful word restricts to local successful words. These facts prove exact equality with the Cartesian product.

This is stronger than merely matching observed local restrictions: it explicitly proves realization of every combination of local words.

## 4. Probability and singleton conventions

Uniform measure on a finite Cartesian product gives independent uniform marginals, since each fixed local word has exactly the product of the other factor sizes as completions. In particular, an internal pair's global count is its local numerator multiplied by that product. There is no weighting by block length or by a multinomial shuffle count.

For a singleton block, nonsingularity forces B_i=[1]. Its successful family consists of one word. It changes neither the count nor other pair probabilities. Defining its balance statistic delta to be zero makes

    delta(A) = max_i delta(B_i)

correct, including uniquely pressable matrices whose variable-order components are all singletons. A singleton is not a nonunique counterexample and is not required to supply a balanced pair.

A nonsingleton connected variable-order component contains a variable edge, so its corresponding B_i has at least two successful words. Its local variability graph is precisely the same component because every internal probability is preserved. Hence any nonunique counterexample has a nonsingleton factor which is itself a nonunique counterexample. A vertex-minimal counterexample must have connected variable-order graph.

## 5. Independently checked implementation evidence

The auditor wrote a separate verifier, using the already frozen direct rank-one and Gaussian-elimination primitives as read-only dependencies. It enumerates every labelled symmetric matrix through order five, plus the empty implementation boundary. Every nonempty successful full-length family is checked for:

- Fixed block order and contiguity in every full successful word
- Nonsingularity and successful pressability of each local matrix
- Realization of every local word, including identical full residual after every alternative local word
- Agreement of that residual with an independently computed explicit Schur complement
- Exact equality between the full word set and the Cartesian product of local word sets
- Product counts, exact uniform pair marginals, fixed cross-block orders, connected local variability graphs, and the exact delta identity
- Singleton conventions

At order five this covers all 32,768 symmetric matrices, including 13,498 full-length pressable matrices and 12,778 nonunique families. It checks 21,318 local factors and 122,880 complete substituted words. The checks pass in normal, -O, and -OO modes with byte-identical result files. They use explicit runtime checks rather than removable Python assertions.

These exhaustive checks are bounded validation of the supplied arbitrary-order proof. The author's 128 deterministic examples are not described as an exhaustive scan.

Two important negative controls separate the valid argument from stronger false claims. The abstract family {(0,1,2,3),(1,0,3,2)} has contiguous variability blocks {0,1} and {2,3}, but contains only two of the four tuples in the product of its local restrictions. Thus the product property does not follow from contiguity alone; the pressing-state argument is indispensable. In the pressing fixture with row masks (7,5,3), the fixed first singleton and the remaining two-vertex block give exactly two words, whereas inserting an erroneous shuffle factor would give six.

## 6. Combined consequence with the accepted finite verification

Combining this proved factorization with the independently accepted exhaustive verification through order eight yields:

**Every nonsingular successfully pressable symmetric F2 matrix with more than one full-length successful word has a balanced pair if all components of its variable-order graph have size at most eight.**

Indeed, nonuniqueness gives a nonsingleton component; its B_i is a nonunique full-rank pressable matrix of order at most eight. The accepted finite result supplies a balanced pair there, and exact uniform marginals preserve it globally. Other singleton factors have no effect.

Consequently a vertex-minimal counterexample, if one exists, has a connected variable-order graph and at least nine vertices. This is an unbounded-size subclass consequence, not a claim that every pressing matrix has small variable-order components or that the unrestricted conjecture is solved.

## Boundaries

The original computational and structural acceptances remain intact and separately pinned. The new supplement requires no external classification theorem: its factorization proof is elementary. The combined numerical corollary uses only the already accepted finite result. No queue edits, repository changes, source-text publication, or external publication were performed. Code and raw outputs remain private.

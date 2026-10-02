# Turn 5: a Sperner bound and random-oracle infinite antichains

This final author turn proves a quantitative measure obstruction for positive reductions between differently signed copies of one oracle. It gives no new finite positive-degree cardinality. The original corrected question remains unresolved after five turns. Sperner's theorem and effective-null-set methods are classical; novelty of this application has not been established.

## 1. Finite-coordinate probability estimate

Let S,T be computable binary masks and let I be any k-element set of coordinates where they differ. Let Φ be a total positive truth-table functional. Under independent fair bits for A, put Y=A XOR T and X=A XOR S. Then

    Pr[ Φ(Y)(i)=X(i) for every i in I ] ≤ binom(k,floor(k/2))/2^k.       (1)

Fix all source bits Y outside I. On I, X(i)=1−Y(i). The assignments z in {0,1}^I satisfying the k equations form an antichain: if z<w, choose a changed coordinate i. Positivity gives Φ(z)(i)≤Φ(w)(i), but the required target values are respectively 1 and 0. Thus two comparable assignments cannot both satisfy the equations.

Sperner's bound gives at most binom(k,floor(k/2)) assignments. Averaging over the outside bits proves (1). Although we described fixing infinitely many outside bits, each of the finitely many truth tables uses only finitely many of them, so ordinary finite conditioning already suffices.

For completeness, the classical chain-counting proof of the bound is short. A uniformly random permutation of k coordinates generates a maximal chain. It passes through a fixed r-element subset with probability 1/binom(k,r). A chain meets an antichain at most once, so the sum of these probabilities over an antichain is at most 1. Since binom(k,r) is at most the middle binomial coefficient, the asserted size bound follows. Credit: E. Sperner, Mathematische Zeitschrift 27 (1928), 544–548, DOI 10.1007/BF01171114; primary archival record https://gdz.sub.uni-goettingen.de/dms/resolveppn/?PPN=GDZPPN002369915 .

## 2. Nullity for infinitely differing masks

If S XOR T is infinite, choose arbitrarily large finite I inside it. The event Φ(A XOR T)=A XOR S is contained in each finite-coordinate event, so it has measure zero by (1), because the central binomial ratio tends to zero. Taking the countable union over all total positive functionals proves that almost every A has no such reduction.

This argument alone is a measure statement. The next paragraph supplies the effective uniformity needed for Martin-Löf randomness; it does not assume an effective enumeration of all total functionals.

## 3. Effective test, including partial-program enumeration

Enumerate all programs e that, on input n, may halt with a finite query list and a Boolean truth table. Verify that the table is well formed and monotone; an invalid table is treated as undefined. This enumerates partial positive truth-table descriptions and includes every total positive truth-table functional. No decision of totality is attempted.

For a finite I, let E(e,I) be the event that the programs halt with valid monotone tables on every i in I and those tables give the required signed target values. It is uniformly c.e. open: wait for the finitely many computations, and if they all succeed enumerate exactly the finitely many satisfying oracle cylinders. If any fails to terminate or produces an invalid table, nothing need be enumerated. Its measure still satisfies (1), since either it is empty or the same finite monotonicity proof applies.

Let b(k)=binom(k,floor(k/2))/2^k. There is a computable search for an even k with b(k)<2^(−v), using exact rational arithmetic. Termination can be seen from

    b(2m)=product over j=1,...,m of (1−1/(2j)) → 0,

since log of the product is at most minus one half the divergent harmonic sum. Alternatively b(2m)^2≤1/(m+1), proved by induction from b(2m+2)/b(2m)=(2m+1)/(2m+2), gives an explicit bound.

For r≥1 and e≥0 choose such a k with v=r+e+1, and let I(r,e) be the first k disagreements of S,T. This set is computable because the masks are computable and the disagreement set is infinite. Define

    U_r = union over e≥0 of E(e,I(r,e)).

The sequence is uniformly c.e. open and has measure at most sum_e 2^(−r−e−1)=2^(−r). Any oracle for which a total positive reduction exists lies in every U_r, using the index of that reduction. Hence this set is covered by a Martin-Löf test.

## 4. Consequences and exact scope

For every Martin-Löf random A and every two computable masks S,T,

    A XOR S ≤p A XOR T  iff  S XOR T is finite.

The finite case uses the hardcoded reduction from Turn 3. For the infinite case, the preceding effective test applies to this fixed pair of computable masks. Quantification over all such pairs is legitimate because a Martin-Löf random sequence avoids every effective null test; no uniform total enumeration of computable masks is required.

Using the valuation masks S_k from Turn 3 gives an infinite antichain in the truth-table degree of every Martin-Löf random oracle. Therefore any truth-table degree containing either a 1-generic oracle or a Martin-Löf random oracle has infinitely many positive degrees. This does not say every nonrecursive truth-table degree contains such an oracle, nor does it contradict Stephan's known finite examples. No additional odd finite cardinality is realized or excluded here.

## 5. Verification and stop

The checker exhausts antichains on Boolean cubes through dimension four and all three-coordinate monotone vector maps, verifies the conditional antichain bound with an extra outside bit, and checks exact central-binomial inequalities. These are finite controls of the estimate and its degeneracies, not tests of an infinite oracle's randomness. Five substantive author turns are now complete; the full packet is frozen for separate review, with no sixth author search.

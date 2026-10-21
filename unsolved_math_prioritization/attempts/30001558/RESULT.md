# Row 1880 / ID 30001558: partial result, not a solution of existence

## Exact result

The specific candidate proposed in Problem 39 is not fragile. This does not answer whether any infinite ternary squarefree word is fragile under arbitrary nonempty finite changes.

Write t for the binary Thue–Morse word beginning 01101001, g for its word of numbers of ones between successive zeros, and w for g with its initial symbol removed. Then

- g = 21020121012021020120…;
- w = 1020121012021020120…;
- v = 2120121012021020120… = 21g[3:].

Here all indices are zero-based. The words v and w differ only at indices 0 and 1, but v is squarefree.

### Proof

Define E(a)=0 1^a for a in {0,1,2}. The classical overlapfreeness of t implies squarefreeness of g: a square AA in g would give the binary overlap E(A)E(A)0 = 0u0u0 in t, where E(A)=0u.

The gap morphism induced by the binary Thue–Morse morphism is

h(0)=1, h(1)=20, h(2)=210.

Indeed, the gaps in the images of E(0), E(1), and E(2), closed by the next initial zero, are respectively 1, 20, and 210. Therefore g=h(g).

Every h-image avoids 010 and 212. An occurrence of 1 is either the internal 1 in 210, where its neighbors are 2 and 0, or a singleton h(0). In the latter case a preceding image ends in 0 or 1, and a following image starts in 1 or 2. Neither possibility permits either forbidden triple.

Also, g avoids 1201. Any occurrence of 1201 in h(g) must parse as h(0)h(1)h(0): its first 1 is not internal to 210; its following 20 is h(1), not a prefix of h(2); and its final 1 is at an image boundary. This would require 010 in g, a contradiction.

Put x=1g[3:]=120121…. Every square in x must start at its initial position because its remaining suffix is a suffix of g. A square of period at least 4 would repeat 1201 later, within g. Periods 1, 2, and 3 fail by direct comparison in 120121. Thus x is squarefree.

Finally v=2x begins 2120…. Again any square must start at its initial position. For period at least 3, it would repeat 212 later. There is no such later occurrence: at position 1 the triple is 120; at every position at least 2 it is in g. Periods 1 and 2 fail directly. Thus v is squarefree, proving the claim.

## Five substantive approaches and their outcomes

1. **Binary gap transfer.** A finite modification changes the binary tail offset by the sum of its gap changes. Even zero offset would not suffice: squarefree ternary 212 encodes to E(212)0=011010110, which contains binary overlap 10101. Thus ternary squarefreeness does not imply binary overlapfreeness under this encoding. The direct binary fragility transfer fails for two independent reasons.

2. **Backward-prefix uniqueness.** Exhaustive backward extension of fixed 512-symbol tails of w retained two admissible prefixes at cut 2, four at cut 5, ten at cut 8, and 35 at cut 12. The alternatives included 10→21 and 10201→02010 or12010. These finite results were treated only as candidates, not infinite certificates. Linear-time Z-function testing of each potentially affected square start checked the 10→21 alternative through a word of length524286 without finding a square.

3. **Morphic synchronization and forbidden markers.** Desubstitution established the extra forbidden marker1201. This upgraded the 10→21 experimental survivor to the exact proof above. This is an obstruction to the suggested construction, not an existence proof or impossibility theorem for all words.

4. **Compactness and finite-certificate formulation.** For an infinite squarefree w and fixed n, uniqueness of its length-n predecessor is equivalent to existence of some finite L≥n such that w[:n] is the only length-n prefix p for which p+w[n:L] is squarefree. The forward direction holds because there are only3^n candidate prefixes, and each excluded candidate has a finite square witness; take the maximum witness endpoint. The reverse direction is immediate. Fragility is equivalent to this condition for every n. Delicacy alone does not control these joint prefixes. A construction would require compatible certificates for unbounded n and an infinite squarefree continuation, neither obtained here.

5. **Exhaustive finite forcing and extendibility.** Generate all ternary squarefree words through length32 by appending a letter only when it creates no suffix square. At length32 there are58446 words. Grouping by suffix after the first6 positions gives exactly6 singleton groups; they are the alphabet permutations of01021012102012101202101210201210. That representative has exactly one squarefree extension to length33 and none to length34. Thus all six finite6-prefix-rigid witnesses at this length are dead ends. This rules out this particular finite search level as an infinite construction and demonstrates the necessity of checking continuation, but says nothing about longer levels.

Selected exact counts of singleton groups, for cut positions1 through6:

- L=24, total7032: 3372,1500,282,96,12,0.
- L=28, total20220: 9696,4260,816,306,54,0.
- L=32, total58446: 28074,12492,2424,906,144,6.

## Adversarial review

An independent worker checked the gap encoding, found the encoding-overlap obstruction, and independently supplied the forbidden-marker proof. The parent researcher verified the morphism parsing and the short-period cases, checked the forbidden factors computationally, and checked all potentially affected square starts with exact Z arrays. Infinite correctness rests on the symbolic proof, not the finite search.

No proof of existence or nonexistence for the original fragile-word question was obtained. Robustness and single-letter delicacy were not represented as new results. No repository publication or queue changes were made.

## Sources

- Jeffrey Shallit, contribution to Mini-Workshop: Combinatorics on Words, Oberwolfach Reports7 (2010), printed pp.2232–2233, Problem39. DOI https://doi.org/10.4171/OWR/2010/37 ; primary PDF https://ems.press/content/serial-article-files/46296 . Used for the exact question, suggested candidate, and stated binary Thue–Morse overlapfreeness.
- Private primary-source inspection and prior-art boundaries are recorded separately in SOURCE_GATE.md. No copied source text is included here.

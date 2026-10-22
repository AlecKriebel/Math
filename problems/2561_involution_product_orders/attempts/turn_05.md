# Attempt 5: larger alternating involution classes and the unbounded-rank obstruction

Date: 2026-10-03. Fifth substantive attempt. Goal: extend the double-transposition support method to every alternating involution class and, if that fails, isolate exactly what remains. The full Notebook problem is not resolved after this attempt.

## General fixed-cycle-type reduction

Let k>=2 be even and D_{n,k} the involution class of k disjoint transpositions in A_n, n>=2k. Fix a in D. The two-point signature criterion of Attempt4 remains applicable. If it holds at degree6k, it holds for every n>=6k: the supports of a and a proposed indistinguishable pair x,z have total size at most6k, and the signature equality restricts to the full class in any6k-letter subset containing them. The same proof as for k=2 is exact.

This gives a finite certificate scheme for each fixed k, but not a finite verification for all even k. Its degree6k grows with k, and the matching class size grows rapidly. We do not assert the criterion at degree6k for untested k.

## A padding-probe lemma with a proof

There is, however, a uniform restriction on possible signature collisions. Assume n>=8k and that x,z in D_{n,k} have equal signatures against every member of D_{n,k} commuting with a. Write A=support(a) and R=the remaining letters. Then:

1. x and z move exactly the same letters of R.
2. Their transposition edges entirely inside R are identical.

Proof of1. Fix i in R. Choose a fresh letter r outside the supports of a,x,z and different from i. Let t=(i r). Choose k-1 disjoint padding transpositions on fresh letters outside those supports and outside {i,r}. There are enough: the union of the three supports has size at most6k, and n>=8k provides2k fresh letters; removing i if it was fresh and r still leaves2k-2. The product y of t and the padding transpositions belongs to D_{n,k} and commutes with a because it is supported in R.

If x fixes i, then x and y are disjoint involutions, so xy has order2. If x moves i, the component containing i is a3-cycle in xy, while the k-1>=1 padding transpositions guarantee an order2 component. Thus xy has order6. Equality of the signatures says order(xy)=order(zy), proving that i is moved by x exactly when it is moved by z.

Proof of2. Let i,j in R be moved. Use t=(i j) and k-1 padding transpositions fresh from a,x,z. If x(i)=j, the common transposition cancels and the remaining disjoint involutions give order2. If x(i)!=j, t joins two different x-transpositions; their product is a4-cycle, and all remaining factors have order at most2. Therefore xy has order4. The same holds for z, and equal signatures imply x(i)=j exactly when z(i)=j. QED.

Consequently all outside-to-outside edges are already reconstructed. After those common edges are removed, a signature collision can differ only in a matching on A together with the outside letters attached to A. There are at most2k such outside legs, so the unresolved matching occupies at most4k labeled letters. This is a structural reduction; it does not identify those remaining attachments or their internal edges.

## Why the existing criterion cannot simply be asserted

For k=4, exact raw signature computations already give:

- n=9: class945, commuting set25, outside fibers68 of size2 and196 of size4.
- n=10: class4725, commuting set53, outside fibers272 of size2 and1032 of size4.

These are complete raw-signature computations only. They show failure of that sufficient criterion at these degrees; they do not produce graph automorphisms, and are not counterexamples to21.52. Unlike the A7 double-transposition case, no full equitable refinement or full automorphism enumeration of these two larger graphs was undertaken. No unsupported jump from a local size4 ambiguity to a global color symmetry is made.

One possible further approach is to probe an a-transposition together with a transposition from an outside leg to a fresh point, then compare probes swapping two a-pairs. Such probes distinguish some attachment patterns through different alternating-path lengths. But recovering all attachments uniformly would require a proof that the only surviving ambiguity is simultaneous conjugation by a. I have not proved that statement; local color information can fuse different product structures through equal least common multiples.

## Final mathematical outcome after five attempts

Established partial results:

- exact extension criterion via preservation of the conjugation operation;
- elementary A5 reconstruction;
- all characteristic-two symplectic transvection classes (including all even-q PSL2 involutions);
- all alternating double-transposition classes, via a proved support reduction and small exact certificates;
- exact full-class certificates for A6, A7, PSL2(7), PSL2(11), and A8 fixed-point-free involutions;
- general local two-point sufficient criterion, and a uniform padding-probe reduction for larger alternating classes.

Unresolved: arbitrary involution classes of arbitrary finite nonabelian simple groups. No counterexample to21.52 was found. None of these arguments proves that all other alternating classes, higher-rank classical involutions, exceptional groups, or sporadic classes satisfy the claim. No new discovery, first-priority claim, publishable full solution, or DOI is warranted. The proper queue outcome is unsolved with partial results and5/5 substantive attempts, subject to independent audit of those partial results.

Retrieval, source correction, exact replays, independent review, packaging and future gate repair are not additional substantive attempts.

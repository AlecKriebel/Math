# Attempt 3/5: direct-product kernels and odd wreath-product counterexamples

Date: 2026-10-03 UTC. Objective: construct a counterexample by odd permutations of simple factors, or reduce that construction to an almost-simple obstruction. Outcome: a proved localization theorem; pure odd wreath permutations cannot create the needed failure when the factor outer automorphism groups are pi'-groups.

Let N=S_1×...×S_t be a direct product of nonabelian finite simple groups, normal in G=NH. Let H be pi-maximal in G, pi consisting of odd primes, and A=H∩N. Conjugation by H permutes the factors S_i (automorphisms permute the minimal normal subgroups of N).

## 1. Maximality forces the intersection to split

Let A_i be the projection of A to S_i. Each A_i is a pi-subgroup. Because A is normal in H, conjugation by H permutes these projections compatibly with its permutation of the factors. Thus D=∏A_i is H-invariant and contains A.

The product DH is a group, D is normal in it, and D and H are pi-groups. Hence DH is a pi-group. Maximality forces DH=H, giving D≤H∩N=A. Therefore

A=A_1×...×A_t.

This rules out a diagonal-intersection counterexample: even if one starts with a diagonal pi-subgroup across several factors, its direct product of projections is an H-invariant pi-enlargement unless it already equals the whole intersection.

## 2. A transport lemma

Fix i and let H_i={h∈H:S_i^h=S_i}. Suppose B_i≤S_i is a pi-subgroup containing A_i and normalized by the conjugation image of H_i. For each factor S_j in the H-orbit of S_i, choose h_j∈H with S_i^{h_j}=S_j and put B_j=B_i^{h_j}. This does not depend on the choices: two choices differ by an element stabilizing S_i, which normalizes B_i. On other H-orbits keep the original A_j.

The product B of these B_j is H-invariant, is a pi-group, and contains A. Again BH is a pi-group, so maximality forces B=A. Consequently B_i=A_i.

Thus A_i has no proper H_i-invariant pi-overgroup inside S_i. This conclusion alone is weaker than pi-maximality; the rest of the turn identifies the precise almost-simple configuration that measures the difference.

## 3. The induced almost-simple configuration

Let K_i be the image of H_i under conjugation on S_i, viewed as a pi-subgroup of Aut(S_i), and identify S_i with Inn(S_i). Since A_i≤H_i, we have A_i≤K_i∩S_i. The subgroup C_i=K_i∩S_i is a pi-group normalized by K_i. The transport lemma forces

K_i∩S_i=A_i.

Set L_i=S_iK_i≤Aut(S_i). We claim K_i is pi-maximal in L_i. Let K_i≤U≤L_i be a pi-subgroup. Put B_i=U∩S_i. This is a pi-subgroup containing A_i, normal in U and hence normalized by K_i. The transport lemma gives B_i=A_i.

The image of K_i in L_i/S_i is all of L_i/S_i by definition. Since U contains K_i and is contained in L_i, it has the same quotient image. Consequently

|U|=|U∩S_i|·|L_i/S_i|=|A_i|·|L_i/S_i|=|K_i|.

So U=K_i, as claimed.

We have recovered an exact normal-intersection instance

S_i normal L_i,  K_i pi-maximal in L_i,  K_i∩S_i=A_i.

## 4. Counterexamples over direct products localize

If every A_i is pi-maximal in S_i, then A=∏A_i is pi-maximal in N: any pi-overgroup of A projects into a pi-overgroup of each A_i and is therefore contained in ∏A_i=A.

Hence if A is not pi-maximal in N, some A_i is not pi-maximal in S_i. The configuration (L_i,S_i,K_i) constructed above is then a counterexample whose normal subgroup is simple. Thus counterexamples with a semisimple direct-product kernel cannot arise solely from factor permutations; they require an almost-simple counterexample already on one factor.

No assertion is made here that every radical-free N is a direct product of simple groups. In particular, this does not finish the general reduction from turn 2.

## 5. A positive criterion that eliminates pure odd wreath attempts

If the outer automorphism group Out(S_i)=Aut(S_i)/S_i has pi'-order, the pi-group K_i has trivial outer image. Hence K_i≤S_i, L_i=S_i, and the proved pi-maximality of K_i in L_i says A_i=K_i is pi-maximal in S_i.

Therefore the original intersection assertion holds whenever N is a direct product of nonabelian simple factors with pi'-outer automorphism groups. This includes the case in which those outer automorphism groups are 2-groups, since pi is odd.

This statement permits arbitrary odd pi-subgroups permuting the factors. In particular, adjoining a cyclic odd permutation of identical factors with no odd outer automorphisms cannot produce a counterexample. The projection-and-transport enlargement defeats that proposed construction.

## 6. Remaining obstruction

For a simple S with odd primes in Out(S), one still has to decide whether a pi-maximal K in SK≤Aut(S) can have nonmaximal K∩S. An inner automorphism action is covered above; a genuinely odd outer action is not. Separately, a general radical-free normal subgroup may contain nontrivial layers above its socle, so solving only the direct-product case would not by itself settle every N.

No universal proof or counterexample obtained. Budget used: 3/5 substantive attempts.

# Turn 1: exact length spectrum, with the Hurwitz part left open

One substantive author turn. Original question remains unresolved1/5. The maximal-length input is a credited published theorem; no novelty claim is made for this corollary or its elementary ingredients.

## Theorem

In the exact group

    G = B6 / << c h^−1 >>,
    c = (a1 a2 a3 a4)^5,
    h = a5 a4 a3 a2 a1² a2 a3 a4 a5,

the set of lengths of positive words representing c² is exactly {20,30,40}.

This proves the first clause of Wajnryb's question. It does not classify the corresponding ordered factorizations up to Hurwitz moves in G.

## 1. Realization and the geometric upper bound

Let z=(a1a2a3a4a5)^6. The classical full-twist decomposition in B6 is

    z = c h.                                                   (1)

Here c is the full twist of the first five strands and h is the pure braid that takes the sixth strand once positively around all five. The decomposition follows by separating that strand from the full twist; it also follows by the Artin braid relations. The supplied exact free-group-action check verifies this particular identity independently, using the faithful classical Artin action.

In G, c=h, so c²=z=h². These positive representatives have lengths40,30,20 respectively.

For the upper bound, take the usual five-curve chain on a genus2 surface with two boundary components and cap one of those boundary components with a disk. Denote the surviving boundary by delta. Each chain curve remains nonseparating, adjacent twists satisfy the braid relation, and distant twists commute. The chain identities give

    image(z)=t_delta,
    image(c²)=t_delta.                                        (2)

The four-curve chain has a genus2 one-boundary neighborhood; its boundary is parallel to the surviving boundary after the other disk is capped. The five-chain identity before capping is the product of the two boundary twists. These are precisely the familiar chain relations described in Wajnryb's source, printed125, cases(2) and(3).

By (1) and (2), image(c) image(h)=image(c)², so image(h)=image(c). Thus the geometric homomorphism B6→Mod(Sigma_2^1) factors through G. Every positive word of length m representing c² maps to a factorization of t_delta into exactly m positive twists along nonseparating curves. No injectivity assertion is required.

Baykur–Monden–Van Horn-Morris, *Positive factorizations of mapping classes*, AGT17(2017), TheoremA, gives L(t_delta)=40 for genus2 and one boundary component. All its hypotheses hold here. Consequently

    m ≤ 40.                                                   (3)

This upper bound, including its geometric input, is credited. It does not follow just from abelianizing G.

## 2. The quotient's exponent sum

In the abelianization of B6 all five generators have the same class. The new relation has exponent sums20 and10, so it imposes10 times that class equal to zero. Conversely sending every a_i to1 modulo10 respects all relations. Therefore

    G_ab = Z/10Z.

Since c² has exponent sum40, every representing positive word has length divisible by10. Together with (3), only0,10,20,30,40 need be considered.

## 3. Pure-braid linking obstruction to lengths0 and10

Let P6 be the kernel of the standard permutation map B6→S6. Both c and h are pure, so the added relation is pure and the permutation map descends to G. A word w equal to c² in G is therefore a pure braid when regarded as a word in B6.

For a pure braid define ell_ij to be half the algebraic crossing count of the two labelled strands i,j, for1≤i<j≤6. These are integer homomorphisms P6→Z. On a positive word all ell_ij are nonnegative, and the exponent sum is2 sum ell_ij. Conjugation by a braid permutes these coordinates according to its strand permutation. These elementary facts can be seen directly by following labelled strands; no faithful linear representation is assumed.

The linking vector beta of c² has entries

    beta_ij=2 if i,j≤5, and beta_i6=0.

The relator r=c h^−1 has linking vector r_6 with entry+1 on edges among the first five vertices and−1 on edges incident to6. Its braid conjugates have vectors r_k, k=1,...,6, where

    (r_k)_ij = 1−2*indicator(k in {i,j}).

If w=c² in G, then w(c²)^−1 is a finite product of conjugates of r and r^−1 in B6. All factors are pure. Applying the linking homomorphism yields integers t1,...,t6 such that

    ell_ij(w) = beta_ij + T − 2(t_i+t_j),
    T = t1+...+t6.                                            (4)

No bound or sign is placed on the integers t_i; they record a necessary normal-closure condition only. Summing (4) over the fifteen pairs gives

    m/2 = 20 + 5T,
    T = m/10 − 4.                                            (5)

Suppose m=0 or10. Then T is−4 or−3. For i,j≤5, positivity in (4) and integrality give t_i+t_j≤−1 in either case. Writing s=t1+...+t5 and summing the ten inequalities gives4s≤−10, hence

    s ≤ −3.                                                  (6)

For the five pairs i,6, positivity gives t_i+t6≤−2. Summing yields

    s+5t6≤−10,
    5T−4s≤−10,
    s≥ceil((5T+10)/4).                                       (7)

When T=−4 the last lower bound is−2, and when T=−3 it is−1. Both contradict (6). Thus lengths0 and10 are impossible. This argument also directly shows that the target element is nontrivial; it does not rely on declaring a nonempty word nontrivial by positivity alone.

Together with the upper bound, congruence and three realizations, this proves the length theorem.

## 4. Exact verification and remaining problem

The standard-library checker verifies the full-twist identity via freely reduced Artin automorphisms, all pure linking vectors, the six conjugation patterns, summed inequalities, three representative lengths and bounded stress instances. The finite controls are supplementary: equations(6)–(7) are a proof for all integers t_i, not an extrapolation from the bounded test. The cited topological upper bound remains an external theorem, not a finite computation.

What remains is the original second clause: for each of the three lengths, must every positive word representing c² in G be Hurwitz equivalent to the corresponding standard word? Equality in G is weaker than equality in B6; closed-surface equivalence is also weaker than the requested boundary setting. Neither the linking obstruction nor the maximal-length theorem supplies these equivalences. The next turn will study the normal-closure/linking data at the allowed lengths and what it can and cannot detect under Hurwitz moves.

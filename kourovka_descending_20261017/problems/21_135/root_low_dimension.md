# Low-dimensional quotient counts for two simple families

Checkpoint24October2026. This is a candidate restricted recognition deduction under fresh independent audit, not a solution of21.135. No originality claim. The input classification is a published theorem rather than a new lemma.

## The proposed restricted theorem

For all integers r,s>=0, any finite group H with the same multiset of irreducible complex character degrees as

    G=A5^r × PSL2(7)^s

is isomorphic to G. In particular H has trivial solvable radical. The empty product is allowed.

The proposed argument uses only the order, the unique linear character, the number of degree-three characters, and absence of degree ten. The elementary Itô/lcm criterion independently proves radical-freeness for these products; the stronger isomorphism conclusion here is a distinct low-dimensional-quotient mechanism.

## External classification input and character data

Bácskai–Flannery–O'Brien, *Classifying finite monomial linear groups of prime degree in characteristic zero*, IJAC31(8)(2021),1547–1585, DOI10.1142/S0218196721500569, arXiv2107.12252v2, Theorems11.9–11.10, classify finite nonsoluble primitive subgroups of GL3(C). Their possible scalar extensions have central quotients A5, PSL2(7), or A6; the A6 type contains3.A6. Taking the derived subgroup of each scalar extension shows that its perfect members are precisely A5, PSL2(7), and3.A6.

An irreducible imprimitive subgroup in dimension three is monomial. The permutation action on its three one-dimensional blocks has image in S3 and abelian diagonal kernel, making the entire monomial subgroup soluble. A nontrivial finite perfect subgroup therefore cannot be of this kind. A finite soluble perfect group is trivial, and cannot act irreducibly in dimension three. Hence every finite perfect irreducible three-dimensional image belongs to the preceding three-type list. Perfectness also makes determinant trivial; no extra scalar factor survives the derived subgroup.

The ordinary irreducible degrees of A5 are1,3,3,4,5; those of PSL2(7) are1,3,3,6,7,8. The degrees of A6 include10, and that degree inflates to3.A6. Thus a group having3.A6 as a quotient has an irreducible character of degree10. These are ordinary complex character claims; modular matrix dimensions and reducible permutation dimensions must not be substituted. The primary ATLAS representation pages are source leads, while an explicit ordinary-table certificate is to be checked independently.

## Proof assuming the stated external inputs

Write D for the common multiset. The sum of squares gives |H|=60^r168^s. Exactly one member of D is1, so |H/H'|=1 and H is perfect. Every irreducible degree of G is a product of degrees from its factors. It follows that degree10 never occurs: the only nontrivial member of either factor-degree list dividing10 is5, and5 alone cannot produce10. Exactly2(r+s) irreducible characters have degree3, because exactly one factor must contribute a degree-three character and all other factors contribute their unique degree-one character.

Let chi be any degree-three irreducible character of H. Its representation image H/ker(chi) is finite and perfect and acts faithfully irreducibly on C^3. The classification input gives A5, PSL2(7), or3.A6. The last type would inflate its degree-ten irreducible character to H, contradicting10 not in D. Thus every such image is A5 or PSL2(7).

Each distinct normal subgroup K with H/K isomorphic to either simple group is the kernel of exactly two degree-three irreducible characters: inflate the two faithful degree-three irreducibles of that simple quotient. Conversely every degree-three irreducible has precisely such a kernel. Inflation gives a bijection for each fixed kernel; different kernels give disjoint sets of characters. Let a be the number of A5 kernels and b the number of PSL2(7) kernels. We obtain

    a+b=r+s.

The homomorphism from H to the product of all these distinct simple quotients is surjective. Here is the needed subdirect-product argument. Induct on the number of quotient factors. After the first k maps have full image P=S1×...×Sk, a proper subdirect image in P×S_(k+1) would, by Goursat, identify a nontrivial simple quotient of P with S_(k+1). Every epimorphism from a direct product of nonabelian simple groups to a nonabelian simple group kills all but one factor: the commuting normal images of the factors cannot both be the entire nonabelian target. Thus the new coordinate map would differ from one earlier coordinate by an automorphism of its simple target, forcing equal kernels. This contradicts the choice of distinct kernels. The subdirect image is full, proving the induction.

Consequently H has a quotient A5^a×PSL2(7)^b and 60^a168^b divides60^r168^s. Its5-adic valuation gives a<=r, while its7-adic valuation gives b<=s. Together with a+b=r+s these inequalities give a=r and b=s. The quotient has the entire order of H, so its kernel is trivial and H is isomorphic to G.

If r=s=0, the sum of squared degrees immediately gives |H|=1 and the conclusion is direct. If just one exponent vanishes, the same divisibility proof excludes quotients of the other type. No finite bound on either exponent is used. QED conditional only on the identified classification and ordinary-table data.

## General quantitative variant and limits

For a finite perfect H with10 absent among its irreducible degrees, all degree-three images are A5 or PSL2(7). If their distinct quotient-kernel counts are a,b, then m_H(3)=2(a+b), and H has a quotient A5^a×PSL2(7)^b. Thus a<=v5(|H|), b<=v7(|H|), and

    m_H(3) <= 2(v5(|H|)+v7(|H|)).

This is a checkable restricted statement, not a classification of arbitrary perfect groups or arbitrary radical-free groups. Most source groups do not supply degree-three characters, and general radical-free groups need not be perfect. Even if the above theorem and its novelty survive review, it is a partial answer to21.135 and does not qualify for the user-authorized solved-problem publication pipeline.

The 2020 Azad–Khosravi paper located during preliminary screening establishes selected bounded direct powers under other numerical recognition hypotheses. That does not certify novelty of the present stronger-count input or argument. Fresh literature searches must check arbitrary powers and mixed products, equivalent low-dimensional formulations, and subsequent work. Until then priority remains unestablished.

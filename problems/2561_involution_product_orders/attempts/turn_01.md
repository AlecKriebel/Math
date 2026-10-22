# Attempt 1: reconstructing the inner action, and the smallest simple group

Date: 2026-10-03. First substantive new proof attempt. Exact target: every color-preserving permutation of one involution class D in a finite nonabelian simple group L must extend to an automorphism of L. This attempt does not resolve that universal claim.

## Faithful embedding and the actual missing step

Since D is a nontrivial conjugacy class, its generated subgroup is a nontrivial normal subgroup of L, hence equals L. The conjugation action rho:L -> Sym(D) is faithful: its kernel centralizes every generator and is Z(L)=1. Likewise restriction of Aut(L)_D is faithful, since D generates L. Every such automorphism preserves orders of products. Therefore

    rho(L) <= Aut(L)_D <= H := Aut(Gamma).

Here the second inclusion means the faithful restrictions to D. The question is exactly whether equality holds on the right.

For each a in D, let c_a:D -> D send x to axa. These permutations generate rho(L). If a color-preserving tau satisfies

    tau(c_a(x)) = c_{tau(a)}(tau(x))  for every a,x in D,

then conjugation by tau sends c_a to c_{tau(a)}, normalizes rho(L), and defines an automorphism alpha of L with alpha(a)=tau(a). Conversely an extending automorphism satisfies this relation. Thus the missing reconstruction datum is the ternary operation (a,x) -> axa, not only the binary order data.

A Coxeter presentation does not fill that gap. Let W have involutory generators s_a indexed by D and relations (s_a s_b)^{|ab|}=1. There is a surjection W -> L, s_a -> a, and every color permutation acts on W. Descent to L requires invariance of the kernel. The pair-order presentation by itself gives no proof of this kernel invariance. Adding relations s_a s_b s_a=s_{aba} would suffice, but this assumes the very reconstruction we seek.

## Complete elementary result for L=A5

Identify D with the 15 double transpositions on five letters. Each vertex a fixes exactly one letter f(a). Distinct vertices commute if and only if they fix the same letter: the centralizer of a=(12)(34) in A5 is the four-group {1,(12)(34),(13)(24),(14)(23)} fixing 5. Thus color 2 has exactly five connected components B_i of size 3, indexed by the fixed letters. Every colored automorphism permutes these five blocks. Conjugation by S5 realizes every permutation of the blocks.

It remains to prove that a colored automorphism fixing all five blocks is identity. For a in B_i and j != i, exactly one b in B_j has |ab|=3. Moreover these four matchings of B_i with B_j determine a uniquely once one block permutation is fixed consistently around all triangles. Here is a shorter intrinsic identification using an order-3 triangle: for fixed i, identify B_i with the three partitions of the other four letters into two pairs. For a in B_i and j,k distinct from i, choose the unique order-3 neighbors b in B_j and c in B_k. Direct multiplication shows |bc|=3 precisely when j,k form a pair in the partition a. This reconstructs the partition a solely from the colored graph and the already reconstructed five blocks. Hence any automorphism fixing all blocks fixes every a, and H is exactly S5=Aut(A5).

To verify the two local multiplication assertions without a table of 15 vertices: take i=5, a=(12)(34). The order-3 neighbor in B_1 is b=(25)(34), and in B_2 it is c=(15)(34); their product is a 3-cycle. In B_3 the order-3 neighbor is d=(12)(45); b*d is a 5-cycle. The centralizer of a in S5 permutes each of the pairs {1,2}, {3,4} and interchanges them, so these representatives cover every j and every unordered pair {j,k}. The assertions follow. (An exact independent permutation check is included in the final verifier.)

## Why commuting information alone is inadequate

For A5, the commuting graph is 5 disjoint triangles. Its automorphism group is S3 wr S5, order 6^5*120=933120, vastly larger than Aut(A5), order120. Thus one cannot replace the full coloring by color2 in a general proof.

Source-version correction during verification (no new attempt): the initially consulted v1 HTML of Bryden-Rowley, arXiv:2509.25901, displayed Theorem1(ii) for odd q>3 and therefore missed q=5. The current v2 PDF already corrects the hypothesis to odd q>=7. It is not a current-paper defect. We cite v2 and retain the A5 commuting-graph calculation as an independent warning against extending the commuting-only statement to q=5. Current v2 Theorem1(ii) gives the odd-q>=7 cases of21.52 as a credited immediate corollary: every full-color automorphism preserves commuting adjacency, whose full automorphism group is already Aut(PSL2(q)). No independent reproof of the entire cited theorem is claimed.

## Outcome and next route

Proved the exact extension criterion and A5 case. Universal proof obstructed by reconstruction of aba from product-order colors. Next attempt will exploit characteristic-two transvections: their color3 neighborhoods are affine hyperplanes, which may reconstruct the missing linear structure for an infinite family.

# Independent mathematical and implication review

This is a fresh deduction audit of the frozen note and original proof. Earlier acceptance verdicts were not premises. The claim is existence of one finite, nontrivial, simple **left** brace with metabelian multiplicative group, every multiplicative Sylow abelian, and no isomorphic asymmetric-product presentation with both factors trivial. All five restrictions remain in force. No minimal-order or classification claim is needed.

## 1. Universal obstruction, including nonsplit additive primary groups

The left-brace formulation in [2001.08905v1, Theorem 2.2](https://arxiv.org/abs/2001.08905v1) and [1705.08493v1, Theorem 3.1](https://arxiv.org/abs/1705.08493v1) has exactly the coordinate laws used in the note. The definition starts with a normalized symmetric cocycle, not a bilinear form. The paper proves a necessary condition for the larger class of all cocycles for which these laws form a brace, so replacing source admissibility by that necessary condition does not discard any source presentation.

For a general normalized cocycle, solving c+(u,v)=(t,s) gives c=(t-u,s-v-b(t-u,u)). This yields lambda_(t,s)(w,Z)=(alpha_s(w),Z-b(alpha_s(w),t)). Setting both first arguments' S coordinates to zero, lambda composition forces

    b(w,t+u)=b(w,t)+b(w,u).

This step uses the fact that the factors are trivial: (t,0) circle (u,0)=(t+u,0). Symmetry gives the other additivity. It is not an assumption imported from a selected bilinear family.

For arbitrary finite abelian T,S and arbitrary prime p, mixed-primary values vanish because a bilinear value is killed by both input orders. The set T_p x S_p is consequently an additive subgroup of p-power cardinality equal to the entire p-part of |T||S|. This identifies the unique additive Sylow by cardinality, without asserting that its additive law splits. In characteristic two, an element of coordinate order two can indeed have additive order four. The same set is a multiplicative Sylow since alpha preserves T_p. Its abelianness forces alpha_s(t)=t for all s in S_p,t in T_p.

Twisted subtraction, not componentwise subtraction, gives a*b=(0,-b(u,t)) on this primary subbrace. Each such result has identity lambda action on that subbrace. Therefore (a*b)*c=0 for **every** triple from it. Zero factors, primes absent from one factor, noncyclic factors, arbitrary prime powers, and p=2 are all covered. Finiteness of the whole product forces finiteness of each factor. Brace isomorphisms preserve the unique additive Sylows and star products. Thus the lemma excludes all factors and all coordinate presentations; it does not merely exclude the displayed construction family. Metabelianity and simplicity are not needed for this lemma.

The packaged C4-addition control, mixed-prime control, nonbilinear cocycle rejected by brace admissibility, nonzero-square/zero-triple control, and nonabelian-Sylow control exercise the places where a weaker proof might fail. Their computed outcomes agree with the abstraction. They cannot replace its universal quantifiers.

## 2. Construction and group law

Work inside the ideal R=x F5[x]/(x^5) of the unital truncated polynomial ring. Every product of five ideal elements vanishes. The degree-four formal log/exponential identities have only denominators invertible modulo five; no degree-five denominator is introduced by truncation. Hence the polynomial identities are valid after substitution of arbitrary r,u in R. In particular, L is a bijective circle-to-additive homomorphism, sigma commutes with it, and eta=[x^4]L is sigma-invariant. The symbolic checker establishes the two-variable identity before evaluation on the 625-element ring; finite pair enumeration is additional evidence.

On the even-weight subspace V of F2^5, the integer weight formula gives the stated polarization, and V-perp in F2^5 is the constant subspace. The nonzero constant vector has odd weight, so the restricted form has zero radical. A five-cycle fixes only constant vectors; M-id therefore has no kernel on V and is invertible. Both beta and Q are preserved by M.

Psi is a bijection because its first and last logarithm coordinates reconstruct r using E and e reconstructs z using Q. For completely arbitrary a,b, the first output logarithm is L(r)+sigma^e L(u). Its first three coefficients have the tau action and its fourth coefficient adds without a sign. Polarization cancels the binary beta term and gives output e+f. Thus the displayed law is precisely the direct product of the two stated semidirect products on every pair. Associativity and inverses follow from this all-pair identity, not from a basis-pair extrapolation.

For fixed a, the displayed lambda formula is linear on each additive primary block. Multiplication by 1+r is invertible and the binary block is triangular with invertible M action. Thus every lambda is an additive automorphism; together with the proved circle group law this proves the left-brace law. No lambda homomorphism property is assumed to prove the group law. The order is 625*16*2=20,000.

The tau-id image is two-dimensional over F5; the M-id image is all V. Therefore the derived subgroup is C5^2 x C2^4 of order 400 and is abelian. The 5-Sylow C5^3 x C5 and the 2-Sylow C2 x V have the full respective p-parts of the group order and are abelian. Conjugacy covers every Sylow. Neither Sylow is assumed normal.

## 3. Simplicity for every ideal

For an ideal I, lambda_g(i)-i belongs to I by additive closure and lambda invariance. The separate inference i*g in I uses the quotient brace B/I and thus multiplicative normality. It is valid for ideals; it is not being granted to arbitrary lambda-stable subgroups.

If an arbitrary nonzero i=(r,v,z) has r nonzero, 6i=(r,0,0) isolates it. If r=0 it is already binary. This treats every mixed element; no coordinate-subspace assumption about I is made. For a pure ring element with lowest term c x^j, multiplication by x^(4-j) when j<4 isolates exactly c x^4; j=4 is handled directly. Scaling gives a=x^4. For a binary element with v nonzero, nondegeneracy supplies w and the lambda difference gives b=(0,0,1); when v=0 it is already b.

The b-to-ring step is b*x=3x, with 3 nonzero modulo five. The a-to-V step uses eta(x^4)=1, yields (M-id)w with zero scalar coordinate, and reaches every V vector. A binary lambda difference then supplies b. Scaling 3x gives x; repeated ring lambda differences give x^2,x^3,x^4. Thus either initial case reaches all nine additive generators. This proves I=B for every nonzero ideal. Both cross-actions are essential, as the omitted-sigma and omitted-M controls produce actual proper homomorphism kernels.

On the 5-primary subbrace the star law is ordinary ring multiplication, so (x*x)*x=x^3 is nonzero. This is the contradiction with Section 1 and simultaneously proves nontriviality. The full theorem and the original question are therefore established by the note's own arguments.

## 4. Retained original center, fixed-set and derived witnesses

The original full proof's redundant claims were also checked. Global lambda-fixedness first forces u in Ann(R)=F5 x^4, then w=0 by M-id invertibility; all scalar z remain fixed. Thus Fix has order 10. The displayed semidirect product gives Z(G)={(E(c x^2),0,0)}, order five. E(x^2)=x^2+3x^4. The derived group has order 400 and abelianization order 50.

The comparator claims about simple nontrivial two-trivial-factor products hold independently. The radical of b, embedded in T, is a proper ideal, hence zero. If W=sum Im(alpha_s-id), then W x S is a nonzero ideal, so simplicity gives W=T. Consequently G'=T and Fix={0} x S is a complement. The kernel of alpha in S is also a proper ideal, hence alpha is faithful. A multiplicatively central (t,s) must have s=0 and t fixed by all alpha. Invariance of b then makes b(t,alpha_u(v)-v)=0; those differences generate T, so t is in the zero radical. The multiplicative center is therefore trivial in that comparator class. No general centerlessness claim about arbitrary simple braces is used.

For k=(0,0,1) and h=(E(2x),0,0), conjugation by k reflects the ring, so [k,h]=E(x). Direct expansion gives E(x)=x+3x^2+x^3+4x^4, d*x=x^2+3x^3+x^4, and x*(d*x)=x^3+3x^4 nonzero. The packaged exact checks reproduce these orientations and coefficients.

## 5. Independent review of the new implication bridges

The following are audit deductions, **not prior theorems attributed to their source authors**. I rederived them from the inspected formulas, after separately checking the source hypotheses.

### Group-action lemma

For finite G=N semidirect S with N abelian, metabelianity implies that a in S' centralizes [a,N]. On additive N, writing alpha_a=1+D gives D^2=0. It suffices to consider p-elements of the finite abelian S'. On N_p, the subgroup N_p semidirect <a> is a p-subgroup, so the abelian-Sylow hypothesis gives D=0 there. On N_q for q different from p, (1+D)^(p^e)=1 gives p^e D=0, hence D=0 since p^e acts invertibly on N_q. Thus S' acts trivially on N. The proof handles arbitrary finite abelian primary N, not only vector spaces.

### The 2401.12904v2 nontrivial-factor route

The actual §4 setup requires t-id invertible and has A1=A semidirect <t>. Thus A=[<t>,A] lies in A1'. Applying the group lemma to N semidirect A1 under the target group restrictions forces alpha(A)=1. In A1, lambda_(a,id) is identity. The asymmetric-product lambda formula then makes every (0,(a,id)) a socle element. Because A is nonzero and <t> is nontrivial, this is a nonzero proper socle and contradicts simplicity. Theorem 4.5's hypotheses and its generally nontrivial A1 factor were retained. The 2025 final journal body remains uninspected; this argument is pinned to arXiv v2.

### The 1705.08493v1 extension route

For a simple two-trivial-factor S=U asymmetric V, the arguments in Section 4 give S'=U and zero radical. For a finite N asymmetric S with target group properties, the group lemma gives alpha(U)=1. The general cocycle is forced biadditive by lambda composition. Its compatibility with lambda_u implies its values are fixed by all lambda_u, hence lie in {0} x V. Alpha factors through V, and the coordinate laws now exhibit the output as (N direct-sum U) asymmetric V with both factors trivial. Quotients preserve metabelianity and the abelian-Sylow property, so the reasoning applies successively to iterations from such seeds. Requiring an already outside-class seed transfers the original target difficulty to an unsupported input.

The matched-product existence theorem does recover this submitted law: cross-actions sigma^e and M^eta are brace automorphisms, invariant under the opposing action. Its available cited simplicity theorem assumes simple factors, while R and H have proper nonzero ideals. Thus it supplies construction formalism, not the missing all-ideal propagation result. The explicit nested Example 4.3 in 1610.00477v1 has f_i=id and Q-preserving actions depending only on scalar q_i; coordinate permutations preserve their sum forms. The q_i coordinates give the claimed flattening for that example. This does not classify arbitrary nested matched products.

### The 2609.20401v1 kernel-wreath route, arbitrary seeds

Use the actual group G=ker epsilon inside R^T semidirect T. A Sylow p-subgroup P of R maps onto T_p. For |T|>2 choose order-p u in T, r in P with chi(r)=u^-1, and form a kernel element g with top u and base r in one coordinate. Choose nonidentity a in P and a compensated base element h supported at two coordinates with entries a,a^-1. Choose that support not invariant under u; such a pair exists even when p=2 because |T|>2. Then both elements lie in a common p-group and fail to commute: conjugation shifts h's support, and base conjugation cannot erase nonidentity entries. Thus some Sylow is nonabelian.

For T=C2 and |P|>2, use instead a nonidentity element of ker(chi|P) at one coordinate. Its support is moved by the top lift, giving the same failure. The sole remaining possibility has |P|=2 and K=ker chi odd. Then K^2 is normal Hall odd in G. In any finite classical left brace a normal multiplicative Hall subgroup is an ideal: the unique additive Hall subgroup is lambda invariant, therefore multiplicative Hall, and its image in the complementary quotient has coprime order and is trivial. If K is nontrivial this is a proper ideal. If K is trivial, the order-four output has nonzero diagonal socle. Therefore no arbitrary-seed output can meet the full simple-classical-brace/abelian-Sylow target. Metabelianity was not even needed for this elimination.

### Other recent candidates

[2608.01884v2](https://arxiv.org/abs/2608.01884v2), Theorem 1.1 and Proposition 7.2, has nonabelian multiplicative p-group and a proper three-dimensional ideal. Its Proposition 2.1 is primary-algebra construction machinery, not a mixed-prime simplicity theorem. It is relevant established methodology and is credited.

For [2609.24640v1](https://arxiv.org/abs/2609.24640v1), nonzero kappa gives nonabelian addition by the actual commutator formula; zero kappa returns its input. The displayed asymmetric-product seed has a required order-p nonidentity action on a p-vector space, making its same-prime multiplicative subgroup nonabelian. Neither operation yields this target. These exclusions do not establish the absence of other, uninspected consequences or sources.

## Conclusion

No mathematical counterexample or missing proof obligation was found in the full original proof or self-contained note. The strongest verified result is the full negative answer to the original question. Historical-first status is a separate bounded literature issue; inaccessible bodies and uninspected final revisions remain explicitly open.

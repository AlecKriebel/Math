# Independent mathematical audit: Kourovka 21.6

## Disposition

**PASS. No fatal gap found. No mathematical revision is required for the negative answer as stated.**

This conclusion concerns the supplied construction and the literal October 2026 formulation. It is an independent mathematical audit, not human-specialist certification, formal proof-assistant verification, editorial acceptance, or a novelty/priority determination. The finite calculations corroborate, rather than replace, the infinite argument below.

## 1. Scope of the controlling question

The editor-hosted October 2026 Kourovka Notebook, printed page 177, attributes Problem 21.6 to A. O. Asar. The quantifiers are over a prime p, a transitive finitary permutation group G, and its transitive Sylow p-subgroups S. The requested subgroup of S is transitive, totally imprimitive, and has every individual cycle support as a block for that subgroup. The ambient G need not be the entire finitary symmetric group. No perfectness, maximality in FSym, or preassigned block system is imposed.

The proof produces p = 2, a countably infinite domain, and a transitive locally finite 2-group G with S = G. It excludes the cycle-support condition for every transitive H <= G. This is sufficient even before total imprimitivity of H is considered.

Source: [October 2026 primary PDF](https://kourovkanotebookorg.wordpress.com/wp-content/uploads/2026/10/21tkt.pdf), printed p. 177. The page was read in both its displayed rendering and text. Detailed retrieval limits are in SOURCE_AUDIT.json.

## 2. Finite algebra: independent line-by-line check

Use the author's eight labels, with V = F_2^2 and D = V x F_2. Write e_1 = (1,0), e_2 = (0,1), tau_t f(v) = f(v+t), and sigma(f) for the sum of all four values. Let E be the additive group of four-bit functions and E_0 = ker sigma.

The action of (f,t) sends (v,epsilon) to (v+t, epsilon+f(v+t)). With ordinary function composition, applying the right-hand map first gives

    (f,t)(g,u) = (f + tau_t g, t+u).

There is no source/destination indexing error: the second added term at the final point w = v+t+u is g(w+t), exactly tau_t g(w). The kernel of the surjective homomorphism (f,t) -> sigma(f)+t_1 is therefore

    P = { (f,t) : sigma(f)=t_1 },

of order 32. The action is faithful, because a trivial permutation forces t = 0 and then f = 0. Its quotient on the four two-point fibres is the regular translation group V. Its even base E_0 flips either point of any selected fibre while possibly flipping one other fibre. Hence P is transitive.

### Minimal transitivity: verify the author's direct proof

Let Q <= P be transitive. Its image on the four fibres is a transitive subgroup of the regular group V, so is V itself. Thus Q has elements q_1=(f,e_1), q_2=(g,e_2) with sigma(f)=1 and sigma(g)=0. Put D_i=1+tau_{e_i}.

1. q_1 squared is (D_1 f,0). The function h=D_1 f has one value on each e_1-pair. The sum of these two values is sigma(f)=1, so h is the indicator of exactly one pair.
2. Conjugating a base function by q_2 translates it by e_2. The base part g cancels because the base is abelian. Thus h and tau_{e_2}h are both in Q and span the two-dimensional space L=ker D_1.
3. Direct multiplication, including inverses, gives the base function of q_1 q_2 q_1^{-1} q_2^{-1} as c=D_2 f+D_1 g. There is no omitted translation term.
4. D_1 c = D_1 D_2 f = 1_V, since D_1 squared vanishes and the double difference sums f on all four points. Thus c is even but not in L.
5. The three independent even vectors generate all of E_0. Therefore Q contains the full kernel E_0 and maps onto V, whence Q=P.

No finite enumeration or classification theorem is needed here. The independent verifier additionally recovered the functions from the cycle-generated permutations and checked all 64 possible lift pairs.

### Separate Frattini proof of minimal transitivity

This gives an independent mathematical route. Put a=(delta_0,e_1) and b=(0,e_2). The square a^2 is the base indicator of {0,e_1}; its b-conjugate is the indicator of {e_2,e_1+e_2}; and [a,b] is the indicator of {0,e_2}. These three functions span E_0.

In a finite 2-group, every maximal subgroup has index 2, so contains all squares and commutators and is normal. Consequently every maximal subgroup of P contains E_0. Conversely, inverse images of the three index-2 subgroups of P/E_0 = V are maximal; their intersection is E_0. Hence Phi(P)=E_0.

The stabilizer K of (0,0) consists of (f,0) with f(0)=0 and sigma(f)=0, and has order 4. In particular K <= Phi(P). If a subgroup Q were transitive, every p in P could be written qk with q in Q, k in K, so P=QK. If Q were proper, it would lie in a maximal subgroup M, which also contains K. Then P=QK <= M, a contradiction.

The independent finite program obtains Phi(P) as the intersection of all maximal subgroups, not by the author's square-and-commutator closure computation.

### Exact obstruction

The permutations

    b = (1 5)(2 6)(3 7)(4 8),
    z = (3 4)(5 6)

belong to P. The set C={1,5} is an entire cycle of b. Its image under z is {1,6}, and the intersection is exactly {1}. Therefore C fails the block test. This is an individual-cycle obstruction; it does not confuse the support of b as a whole with the support of a single cycle.

All 32 elements and all their cyclic orbits, including singleton orbits for robustness, were checked independently. There are 22 distinct cyclic subgroups. Exactly 12 elements have every cyclic orbit a P-block, and 20 have a crossing orbit. Among all 255 nonempty subsets, the 19 P-blocks comprise 8 singletons, 4 pairs, 6 four-point blocks and the whole set. The witness pair {1,5} is not one of them.

## 3. Universal obstruction transfer: the essential quantifier

The following argument is valid in arbitrary permutation groups; finitarity is not needed for the transfer itself.

Assume B is a G-block and the image of its setwise stabilizer on B is P in the eight-point action above. Take an arbitrary transitive H <= G.

- B is automatically an H-block, because H has fewer translates than G.
- For arbitrary x,y in B, choose h in H with h(x)=y. Then h(B) meets B; the G-block property forces h(B)=B. Thus the setwise stabilizer H_B acts transitively on B.
- The restriction map H_B -> Sym(B) is a homomorphism with image Q <= P. The preceding transitivity makes Q transitive; finite minimal transitivity forces Q=P.
- Surjectivity supplies h_b,h_z in H_B restricting to b,z. No claim is made that H contains the base copy P, that either lift is supported on B, or that the restriction map is injective.
- Because h_b stabilizes B, its powers cannot leave B when started there. Starting at 1, the orbit is exactly 1 -> 5 -> 1. Thus C is a complete cycle of the full permutation h_b on the infinite domain, regardless of the order or cycles of h_b outside B.
- The actual element h_z belongs to H and sends C to {1,6}. Therefore C is not an H-block. A single such element and cycle contradict the required universal cycle condition.

This proves the conclusion for every transitive H. It is not an inference from the action on the set of blocks, nor a statement only about the stabilizer's own block system. The crossing translate is provided by an element of H itself.

### General inheritance formulation

If a permutation group H has the cycle-support block property and B is any H-block, then H_B^B also has that property on B. Indeed, lift an arbitrary element of H_B^B to H_B. Each of its cycles in B is a full cycle of the lift, so is an H-block and, upon restriction, a block for H_B^B. This argument proves the contrapositive used above. One must restrict the setwise stabilizer, not an arbitrary element which moves B; the manuscript uses exactly the correct restriction.

The independent finite check tested all 32 choices of h_b and all 32 choices of h_z in the first wreath-stage block stabilizer, covering 1,024 ordered lift pairs. This is an implementation stress test, not the justification of the unrestricted statement.

## 4. The infinite tower: every hypothesis checked

Let Omega = D x N_0 and Omega_n = D x {0,...,2^n-1}. Define G_0=P, and G_{n+1}=G_n wr C_2 in its imprimitive action on two adjacent copies of Omega_n. The inclusion of G_n is its action on the first copy with identity on the second. Every finite-stage element is then extended by identity on the rest of Omega. Put G=union G_n.

### A. Actual inclusions, not abstract identifications

The first-copy inclusion agrees with the previous action on Omega_n and fixes the new points. These are injective permutation-group homomorphisms. Hence for g,h in the union, some common G_n contains both, their product and their inverses. The union is a group of actual permutations of one fixed domain.

### B. Finitary and locally finite

Every g lies in some finite-stage G_n and fixes Omega outside the finite set Omega_n. Thus every element has finite support. Every finite set of group elements is contained in one G_n, so its generated subgroup is finite. The orders satisfy

    |G_0|=2^5,  |G_{n+1}|=2|G_n|^2,
    |G_n|=2^(6*2^n-1).

Every finite-stage group is a 2-group, so every element and every finite subgroup of G has 2-power order. This also directly verifies local finiteness rather than merely appealing to FSym being locally finite.

The domain is countably infinite. The group is countable as a countable union of finite groups, and infinite since the stage orders strictly increase. Infinite elements of a Cartesian or profinite completion are not included.

### C. Transitivity

G_0 is transitive on Omega_0. At stage n+1 the two factors act transitively inside their own copies, and the top involution exchanges the copies pointwise. Thus G_{n+1} is transitive on Omega_{n+1}. Any two points of Omega belong to a common Omega_n, giving transitivity of the union.

No global shift of N_0 or infinite-support permutation has been introduced: each top exchange moves only the finite set Omega_{n+1}.

### D. A compatible family of genuine G-blocks

For fixed n, partition Omega into intervals D x {j*2^n,...,(j+1)*2^n-1}, j>=0. At every stage m>=n, each of the two subactions preserves the appropriate subpartition, and the coordinatewise top swap interchanges corresponding partition members. Outside Omega_m everything is fixed. A stage m<n acts inside Omega_n and fixes the other members. Thus the entire G preserves this partition. In particular Omega_n is a G-block.

The partitions are compatible with the fixed inclusions. The argument does not mistakenly promote an arbitrary block of G_n to a block of every later group; it establishes this for the explicitly aligned dyadic partitions.

### E. Total imprimitivity

Every proper block A in a transitive finitary action on an infinite set is finite. Otherwise choose a in A and y outside A, and g with g(a)=y. Then g(A) intersects the complement of A, so the block axiom forces g(A) to be disjoint from A. Every point of A would be moved, contradicting finite support.

The displayed Omega_n are finite, proper, strictly increasing blocks whose union is Omega. Every proper block A is finite, so lies inside some Omega_n as a set, and hence is strictly contained in Omega_{n+1}. Therefore there is no maximal proper block. This is precisely the standard finitary meaning of totally imprimitive. There is no missing cofinality assumption. In fact the same block chain also makes any transitive subgroup H <= G totally imprimitive.

### F. Bottom stabilizer action remains exactly P

Use a slightly stronger induction invariant. Every finite-stage element permutes the eight-point fibres D x {i}, and on each fibre its map to the target fibre has D-coordinate equal to an element of P. This is true for G_0. Independent products preserve it, and the top swap acts as the identity on the D-coordinate. It therefore holds for every stage and every element of G.

Consequently an element of G stabilizing B=Omega_0 restricts to an element of P. Conversely, the original copy G_0 realizes every element of P on B. Hence G_B^B=P exactly. It is not merely a containing group or a group with P as a quotient.

## 5. Sylow condition and final logical closure

Take p=2 and S=G. G is itself a 2-subgroup of G and there can be no larger 2-subgroup inside G. Thus it is a Sylow 2-subgroup of G in the maximal-p-subgroup sense. For this locally finite p-group the same conclusion holds under the usual equivalent Sylow formulations: a Sylow subgroup of a group that is already a p-group is the group itself. Transitivity was proved above.

The primary problem concerns Sylow subgroups of arbitrary G. It does not require S to be maximal in FSym(Omega), and the construction does not claim that stronger property. Imposing that different condition would change the question and invalidate this particular use of S=G; it is absent from the controlling statement.

Now B is a G-block with G_B^B=P. Section 3 therefore rules out the cycle-support block condition for every transitive H <= S. In particular S has no subgroup satisfying the requested conclusion. This is a genuine infinite finitary counterexample for p=2, and a single prime suffices to refute the universal assertion.

## 6. Adversarial checks and resolved concerns

1. **Could a smaller local image avoid z?** No. H_B^B is transitive, and P has no proper transitive subgroup.
2. **Could a lift's longer order enlarge C outside B?** No. B is invariant under the lift, and the orbit through 1 returns after two steps inside B.
3. **Could the relevant block notion be for G rather than H?** The failure is exhibited by h_z in H, so it is an H-block failure directly.
4. **Could a different H block system hide the failure?** The definition tests whether the actual cycle support is a block, not whether a chosen system contains it. The crossing set certifies failure under the definition itself.
5. **Could a diagonal embedding be required?** No. The stated first-factor embeddings are explicit and are exactly what provides finite support. A diagonal direct limit would be a different construction.
6. **Could local finiteness fail at the union?** Any finite generating set is contained in a single finite stage.
7. **Could a nontrivial element have infinite support?** Every union element belongs to a finite stage; no completion is taken.
8. **Could the domain be finite, or total imprimitivity depend on an unintended convention?** The domain is explicitly countably infinite, and no maximal proper block is proved directly.
9. **Could the theorem only handle selected generators?** The argument exhibits an element of every transitive H with a bad cycle. The verifier also exhausts all finite elements, and its dihedral diagnostic catches the generator-only fallacy.
10. **Could the finite computation alone be mistaken for an infinite proof?** The infinite result follows from the inductive invariants and the unrestricted lifting argument, not from a bound on n.
11. **Could literature hypotheses such as perfectness, homogeneous generators or a centralizer condition be silently assumed?** None is invoked in this proof or imposed by Problem 21.6. Those conditions occur in separate results about minimal non-FC groups.
12. **Could “cycle” require the isolated cycle permutation to belong to H?** The question concerns cycles in the decomposition of an element. It does not require each isolated cycle to be an element. Both the manuscript and this audit use that definition.

## 7. Remaining limits

- The original 2011 full text was unavailable; publisher metadata and abstract were checked. The 2017 definition and relevant construction were inspected in a publicly indexed reproduction, with publisher metadata separately confirmed. No result from either paper is required for the proof.
- No novelty or priority claim follows from a bounded search or from the primary problem's present unsolved marking.
- No claim about all finite transitive p-groups, a classification of minimally transitive groups, or transitive Sylow subgroups of the entire finitary symmetric group is established.
- This audit does not certify unrelated articles about minimal non-FC groups or their corrigenda.
- The executable verification is exact finite arithmetic but is not a formalization of the infinite proof.

These are scope limits, not gaps in the submitted counterexample.

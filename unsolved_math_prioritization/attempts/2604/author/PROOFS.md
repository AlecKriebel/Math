# Rigorous exclusions for Kourovka 21.95

All groups here are finite. Write Γ(G) for the labelled prime graph: its vertices are the prime divisors of |G|, with an edge r–s exactly when an element of order rs exists. Forgetting the vertex labels gives the abstract prime graph. A counterexample to recognisability may be any finite group, not necessarily almost simple. These are partial exclusion results, not a solution of the existence problem. No novelty is claimed.

## 1. Two elementary obstructions

**Proposition 1.** If r is a universal vertex of Γ(G), then Γ(G × C_r^k) = Γ(G) for every positive integer k. Thus G has infinitely many pairwise nonisomorphic groups with the same labelled graph.

**Proof.** The prime sets agree. The old group embeds, so old edges remain. For an element of the product, its order is the least common multiple of the component orders. A new edge can therefore only involve r. All such edges already exist by hypothesis. Product orders |G|r^k are distinct. ∎

**Proposition 2.** If S is a proper subgroup of G and Γ(S) = Γ(G), then G is not recognisable, even with vertex labels retained.

**Proof.** The groups have different orders and identical labelled graphs. ∎

These implications are one-way obstructions. Neither absence of a universal vertex nor a change from the socle graph establishes recognisability.

## 2. The affine-extension lemma

Let p divide |G|, and let V be a nonzero finite-dimensional F_p G-module, written additively. Write H = V ⋊ G with multiplication (v,g)(w,h) = (v+g(w),gh).

**Lemma 3.** Γ(H) has the same vertex set as Γ(G). Edges not incident to p are unchanged. For a prime r ≠ p, the edge p–r occurs in Γ(H) if and only if it already occurs in Γ(G), or some element of order r in G fixes a nonzero vector of V.


**Proof.** Since |H|=|V||G| and p divides |G|, the prime sets agree. The copy of G inside H preserves every old edge. If x in H has order rs with r,s ≠ p, its cyclic subgroup intersects the p-group V trivially, so its image in G has order rs. This proves the claim about edges away from p.

Suppose p–r is absent in Γ(G) but x in H has order pr. Its image in G has order dividing pr; the kernel of the map on ⟨x⟩ is a p-group. The only possibility is that the image g has order r. The nonidentity vector x^r in V is centralised by x, and hence is fixed by g. Conversely, if g has order r and fixes nonzero v, then (v,1) and (0,g) commute and have coprime orders p and r. Their product has order pr. ∎

**Corollary 4.** If every order-r element with a nonzero fixed vector satisfies p–r ∈ Γ(G), then Γ(V^k ⋊ G)=Γ(G) for all k ≥ 1, where the action is diagonal. This gives infinitely many distinct group orders and excludes recognisability.

**Proof.** A nonzero fixed vector in V^k has a nonzero fixed coordinate in V. Apply Lemma 3; group orders grow by powers of |V|. ∎

## 3. All symmetric groups S_n, n ≥ 5

Let M=F_2^n with S_n permuting coordinates. Let W={v: Σ_i v_i=0}. When n is odd put D=W; when n is even put D=W/⟨(1,…,1)⟩. Thus dim D=n−1 for odd n and n−2 for even n. In either case D is nonzero.

**Theorem 5.** For every n ≥ 5 and k ≥ 1,

Γ(D^k ⋊ S_n)=Γ(S_n).

Consequently no S_n with n ≥ 5 answers Kourovka 21.95.

**Proof.** For distinct primes r,s ≤ n, the condition for adjacency in S_n is r+s ≤ n. Sufficiency follows from disjoint r- and s-cycles. For necessity, a permutation of order rs needs either distinct cycles whose lengths are divisible by r and s, consuming at least r+s points, or a cycle divisible by rs, consuming at least rs ≥ r+s points.

We use Corollary 4 with p=2. The only odd primes r ≤ n for which 2–r is absent are r=n (when n is odd) or r=n−1 (when n is even). In either case every order-r permutation is a single r-cycle, with at most one remaining fixed point.

If n=r is odd, the fixed subspace M^g is the line of constant vectors. Its nonzero vector has coordinate sum 1, so W^g=0.

If n=r+1 is even, a g-fixed vector has value a on the r-cycle and value b on the fixed point. Its coordinate sum is a+b. Therefore W^g is exactly the constant-vector line T. Fixed vectors commute with taking the quotient by T because the cyclic group ⟨g⟩ has odd order in characteristic 2: averaging a lift over ⟨g⟩ provides an invariant lift of any invariant quotient vector. Hence (W/T)^g=W^g/T=0.

Thus no previously absent edge 2–r is added. All other potential new edges already belong to Γ(S_n), so Corollary 4 proves the claim. ∎

### Exact checks and failure controls

The verifier enumerates all elements (v,g) for n=5,6,7, using the specified quotient representatives. The respective group orders are 1,920; 11,520; 322,560. All labelled graphs agree with Γ(S_n).

For any odd prime r and an order-r permutation with k disjoint r-cycles, the fixed dimension in D is n−k(r−1)−1−ε, where ε=1 for even n and 0 otherwise. This follows by counting the permutation orbits, imposing the augmentation equation, and, for even n, quotienting the invariant line; averaging justifies exactness. The program checks this formula's nonnegativity and its zero value for the nonadjacent primes for 5 ≤ n ≤ 100.

The quotient in even degree is essential: the augmentation module W for S_6 has a fixed constant vector and adds the absent edge 2–5. The full permutation module for S_5 also adds 2–5. Both failed constructions are verified as negative controls.

## 4. Characteristic-two semilinear symplectic groups

Let F=F_{2^f}, let V be a nonzero even-dimensional F-vector space with nondegenerate alternating form B, and let Sp(V,B) ≤ G ≤ Sp(V,B) ⋊ Gal(F/F_2), using field automorphisms in a symplectic basis. Regard V as an F_2-space.

**Theorem 6.** For every k ≥ 1,

Γ(V^k ⋊ G)=Γ(G).

Thus none of these groups is recognisable by its labelled or unlabelled prime graph. In particular this excludes the nonsimple field-automorphism extensions of PSL_2(2^f), f ≥ 2, in its usual SL_2(2^f) model.

**Proof.** The group Sp(V,B) contains a nontrivial involution, so 2 divides |G|. Let x in G have odd prime order r and fix v ≠ 0. Define the transvection

t_v(w)=w+B(w,v)v.

The alternating identity B(v,v)=0 gives t_v²=1; nondegeneracy of B makes t_v nonidentity. Expanding B(t_v(w),t_v(z)) shows that the cross terms cancel in characteristic 2, so t_v belongs to Sp(V,B).

If x has field component σ, then B(xw,xv)=σ(B(w,v)). Since xv=v, semilinearity gives x t_v(w)=t_v x(w). Therefore x commutes with the involution t_v, and x t_v has order 2r. The edge 2–r already belongs to Γ(G). Corollary 4 completes the proof. ∎

For dimension two, Sp_2(q)=SL_2(q), and in characteristic two its scalar centre is trivial, so it is PSL_2(q). The usual field-semilinear description supplies the stated field-automorphism extensions. The theorem is deliberately stated for this concrete semilinear subgroup; it does not assert that exceptional graph automorphisms in every higher-rank case act on this natural module.

### Exact checks

The program constructs F_4 and F_8 by the irreducible polynomials x²+x+1 and x³+x+1. It enumerates all determinant-one 2×2 matrices and all field automorphisms, obtaining base orders 120 and 1,512. It enumerates all affine elements, obtaining orders 1,920 and 96,768, and verifies the graph equality by their exact orders. For every odd-prime-order base element and every nonzero fixed vector, it explicitly constructs the transvection, checks its determinant, involution order, and commutation relation.

## 5. PGL_2(q) in odd characteristic: abstract graph collisions

**Lemma 7.** Let q=p^f be odd. The element orders of PGL_2(q) are precisely the divisors of q−1, the divisors of q+1, and p. Its graph consists of the clique on π(q−1), the clique on π(q+1), sharing exactly the vertex 2, and the isolated vertex p.

**Proof.** A projective 2×2 matrix is represented by a scalar matrix, a nontrivial Jordan block, or a semisimple matrix. A nontrivial Jordan block has projective order p. A split semisimple matrix has eigenvalue ratio in F_q^*, so its projective order divides q−1; all these orders are realised by diagonal matrices. For a nonsplit semisimple matrix the eigenvalues lie in F_{q²} and are conjugate under z↦z^q. Its projective order divides q+1. Multiplication by elements of F_{q²} on its two-dimensional F_q-space gives a cyclic subgroup F_{q²}^*/F_q^* of order q+1, realising all divisors. This exhausts the Jordan forms. Since gcd(q−1,q+1)=2 and p divides neither, the graph description follows. ∎

Let a(q)=|π(q−1)\{2}| and b(q)=|π(q+1)\{2}|. Whenever the unordered pairs {a(q),b(q)} and {a(r),b(r)} agree for q ≠ r, Lemma 7 gives an explicit graph isomorphism: map p to the characteristic prime for r, map 2 to 2, and biject the two odd-prime branches, swapping branches if necessary. The orders q(q²−1) and r(r²−1) are different, so the groups are nonisomorphic.

Three examples illustrate why a theorem about labelled recognisability does not solve the question:

- PGL_2(27) and PGL_2(11): both have two edges meeting at one vertex, plus an isolated vertex. One map is 2↦2, 3↦11, 7↦3, 13↦5.
- PGL_2(169) and PGL_2(181): two triangles sharing the vertex 2, plus an isolated vertex. One map is 2↦2, 3↦3, 7↦5, 5↦7, 17↦13, 13↦181.
- PGL_2(289) and PGL_2(29): a triangle and an edge sharing vertex 2, plus an isolated vertex. One map is 2↦2, 3↦7, 5↦3, 29↦5, 17↦29.

**Finite census.** For all 183 odd prime powers q with 5 ≤ q ≤ 1,000, the verifier finds another odd prime power r ≤ 10,000 and verifies the vertex bijection and every edge. Thus every PGL_2(q) in that stated range is excluded. The full list of authored certificates is in CHECK_RESULTS.json. This is a finite statement, not a number-theoretic assertion that such an r always exists for arbitrary q.

As an independent check on the formula, all projective matrix classes are enumerated for q=5,7,11,13, producing group orders 120,336,1,320,2,184. Exact element-order multiplicities agree with Lemma 7. A deliberately corrupted cross-branch vertex map is rejected.

## 6. Remaining logical gap

No theorem above excludes every nonsimple almost simple group. In particular, the PGL_2(q) finite collision census has no proved all-q extension; other odd-characteristic Lie-type groups and non-field outer actions remain; sporadic outer extensions beyond the explicitly literature-certified obstructions have not been settled here.

A positive answer requires one concrete nonsimple almost simple G plus a proof that every finite H with abstract Γ(H)≅Γ(G) is isomorphic to G. A negative answer requires a competitor or another obstruction for every such G. A finite search without a match proves neither direction. Nor can one assume an arbitrary competitor H is almost simple merely because the candidate G is almost simple: controlling solvable radicals is part of a recognisability proof, and our affine competitors explicitly have nontrivial radicals.

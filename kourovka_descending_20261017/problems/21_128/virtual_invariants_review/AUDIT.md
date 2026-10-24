# Independent adversarial audit: virtual free retracts, outer torsion, Euler indices

Checkpoint: 2026-10-24, 20:35 UTC. Assigned review completion estimate: 100%. Discovery of a complete solution to 21.128 remains unproved.

**Verdict: the partial theorems PASS after the sole boundary qualification was repaired. The inner-adjusted nonrealization paragraph now explicitly requires m>1, including its intended m=5 application.** No full solution, priority certificate, or publication approval follows.

## Evidence and scope

I read the actual `virtual_invariants/FINAL_REPORT.md`, `FREE_RETRACT_FILTER.md`, `OUTER_TORSION_FILTER.md`, `OTHER_ROUTES.md`, `check_schreier.py`, and `schreier_checks.json`, together with `root_invariants/EULER_INDEX_RIGIDITY.md`. I inspected the cached Soroko Proposition 3, Theorem 7 and Table 1, and Bestvina's Question 2 discussion. I independently downloaded the original [Marin 2007 paper](https://doi.org/10.5802/aif.2317) and read Theorem 3 and its proof/corollary in the actual PDF. The theorem is on printed p.1889, PDF p.8; its all-spherical pure-group scope is explicit. Its source receipt is `SOURCE_MANIFEST.json`. Frozen authored inputs are hashed in `REVIEW_MANIFEST.json`.

All assertions reviewed are filters on unsuccessful methods or conditional reductions. The review does not infer that F4 and H4 are or are not commensurable.

## 1. Epimorphism, normal cyclic kernels, and cofinal retracts

An A2 standard parabolic contributes exactly the required three-hyperplane subarrangement of rank two. Its complement is C* times a twice-punctured affine line times C². A based smooth loop in this complement can be perturbed relative to its basepoint to avoid each additional complex hyperplane: the loop has real dimension one, each excluded hyperplane real codimension two, and there are finitely many. The perturbation stays in the larger complement, so it represents the same fundamental-group element. Therefore deletion gives an epimorphism of fundamental groups, not an embedding.

Composing P→Z×F2 with the free projection is surjective. Surjectivity is essential when claiming that the image of Z(P) lies in the target center. Since Z(F2)=1, the map descends to Q=P/Z(P). This step is valid for both F4 and H4.

For K_m=ker(F2→C_m), the m-vertex rose cover has 2m positive edges, rank 2m−m+1=m+1, and spanning-tree basis a^m, a^j b a^(−j), 0≤j<m. Thus V_m=π^(−1)(K_m) is **normal of exactly index m in Q**, and the epimorphism V_m→K_m splits because K_m is free. Normality in the original Artin group is not supplied and is correctly not asserted. Every d-generated abstract group is a quotient whenever m+1≥d. The boundary cases d=0 and m=1 work.

For any finite-index H≤Q, π(H) is finite index e in F2. The coset map Q/H→F2/π(H) is well-defined and surjective even when H is not normal; no quotient-group argument is needed. Thus π(H) is free of rank e+1. A cyclic kernel of index m inside it has rank 1+me, and its full preimage in H is normal of exactly index m in H. It retracts onto that free group by the same splitting argument. This proves the claimed cofinal unbounded free ranks. It does not assert every rank occurs at a prescribed index for an arbitrary H.

For an arbitrary finite-index subgroup of the full Artin group, intersecting the pure subgroup and projecting to Q leaves finite-index images. Pulling back the construction produces further finite-index subgroups with free quotients (indeed the free epimorphisms can again be split). There is no hidden need for the intersection to be normal in the original overgroup.

## 2. Virtual cohomological and quotient consequences

A free retraction gives a split integral H¹ injection. Its image is a primitive direct summand of H¹(W;Z), and cup products of its classes vanish by naturality and H²(F_r;Z)=0. The field-coefficient statement follows separately by the same naturality, without a formality assumption.

For rank-one local systems, the induced character torus is a closed embedded r-dimensional subtorus. Inflation on H¹ is injective: a pulled-back cocycle which is a principal cocycle already descends to that principal cocycle because the quotient map is onto. The rose complex has H¹ dimension r−1 at every nontrivial character and r at the identity. Therefore the whole subtorus belongs to V¹_(r−1)(W). Since the jump locus for the finitely presented cover is algebraic and the torus is irreducible, some component has dimension at least r. Both component dimensions and the attained depths are unbounded virtually. No tangent-cone or resonance equality for arbitrary covers is used.

Every finitely generated abstract group is countable, and the asserted discrete quotient existence is consistent with this. The pro-p assertion is specifically an epimorphism **of pro-p completions** W^p→F_r^p. It is not an assertion that the countable discrete W maps surjectively as a set onto the uncountable free pro-p group. The image of the completion map is compact and hence closed, and contains the dense image of the surjective discrete map, so it is all of F_r^p. This reasoning is valid for every prime, including p=2. The nilpotent quotient assertion concerns ordinary finitely generated discrete free nilpotent groups and also follows directly.

The consequences do not identify full profinite completions, open subgroups, numbers or costs of quotient maps, faithful representation images, or finite generation of their kernels. Those are correctly left outside the theorem.

## 3. Outer torsion versus commensurator torsion

The original Soroko Proposition 3 explicitly gives bi-orderability for P and for its embedded central quotient Q; the independent Marin Theorem 3 check confirms the needed pure-group input. Bi-orderability passes to subgroups and implies unique roots: if a<b, two-sided order preservation yields a^n<b^n. The relevant Q are torsion-free and center-free.

In any center-free unique-root group, an element centralizing a finite-index subgroup centralizes the whole group: every g has some positive power in that subgroup, and equality of conjugate powers invokes unique roots. Consequently C_G(V)=1 in the cyclic-kernel construction.

Conjugation by x, where q(x)=1 and V=q^(−1)(mZ), has outer order exactly m. Its m-th power is inner by x^m∈V; an inner k-th power would imply v^(−1)x^k∈C_G(V), hence x^k=v∈V and m divides k. The chosen representative itself has infinite order in Comm(G), because any identity power on a further finite-index subgroup would force x^k∈Z(G)=1, contradicting q(x^k)=k. This includes m=1: the outer order is one while this chosen inner automorphism is still an infinite-order commensuration.

**Boundary qualification:** the further statement that *no inner-adjusted representative in this outer coset has finite order* needs m>1. For m=1, V=G and choosing v=x^(−1) gives c_v c_x=id. The report's paragraph begins with m=5, for which the deduction is correct, but retains the variable m without explicitly restricting the general nonrealization statement. Add “for m>1” to remove this ambiguity. The q(vx)∈mZ+1 nonvanishing argument works precisely in that range. This does not change the main lemma or its order-five application.

The finite-order realization claim for **actual commensurations** is valid. If [f] has order k, choose a finite-index W inside the domains of all iterates through k and the subgroup where f^k=id. Then f^k(W)=W. Every f^i(W) is a finite-index subgroup and H=∩_(0≤i<k)f^i(W) is contained in the domain of f. Applying f permutes these intersected subgroups cyclically, so f(H)=H. The restriction is an actual order-k automorphism: a smaller order would lower [f]'s order. Conversely, an actual finite-order automorphism of a finite-index subgroup cannot become the identity only on a further finite-index subgroup in a unique-root group unless it was already the identity. Thus no geometric Nielsen realization assumption is hidden here; this is a finite-domain intersection argument.

The torsion lists are correctly those of the **full central quotients**, not Q. Table 1 gives H4 order15 and F4 no order5, but does not determine Comm(Q_F). A hypothetical commensurability forces order5 in Comm(Q_F). Excluding it requires a uniform theorem about actual automorphisms of every finite-index subgroup; an outer torsion list does not supply that theorem.

## 4. Euler index rigidity and the center

For finite K(Q,1) and χ(Q)≠0, multiplicativity under finite covers and invariance under group isomorphism give [Q:U]=[Q:V] whenever U≅V have finite index. This applies to every self-commensuration, including those with domains not normal in Q. It excludes a proper finite-index self-image and makes no statement about infinite-index embeddings.

The signed values −240 and −5040 yield −240a=−5040b, so the F4 index is exactly 21 times the H4 index. This orientation is correct. The free-group comparison F241 and F5041 is a genuine index21 inclusion by 1+21·(241−1)=5041; it correctly demonstrates why this rational Euler constraint alone gives no noncommensurability certificate.

For P=Q×Z and finite-index U, an element of Z(U) projects into the centralizer of its finite-index image in Q. That centralizer is trivial by the same unique-root argument. Hence Z(U)=U∩Z(P), and U/Z(U) identifies with the projection Ubar. The elementary index formula is

[P:U]=[P:UZ(P)]·[UZ(P):U]=[Q:Ubar]·[Z(P):U∩Z(P)].

An isomorphism preserves the intrinsic centers and the quotient groups, so it controls the Q-index but need not control the central index. Q×rZ and Q×sZ are isomorphic and have indices r and s. Therefore all positive rational self-index ratios occur for P; invoking Euler index rigidity on P itself would indeed be incorrect because χ(P)=0.

## 5. Independent word-certificate reproduction

`independent_schreier.py` uses full integer a-exponent carrying. At a b-letter at exponent s=qm+r, it writes the contribution as u^q v_r^(±1) u^(−q), then finishes with a terminal power of u and a residue path. This is different from the author's mod-m edge-state rewrite. It independently checked all 13,121 reduced words through length eight at all 64 indices, giving **839,744** checks, all basis elements and inverses, and every recorded closed-word count. All checks passed, including negative a-exponents and m=1. Output: `independent_schreier.json`.

The all-index/all-word theorem still rests on the covering-tree proof; the finite reproduction is not presented as exhaustive mathematics beyond its recorded range.

## Remaining substantive gap

None of these filters constructs isomorphic finite-index subgroups of Q_F and Q_H or exhibits a genuinely virtual invariant that differs. Bestvina's primary discussion supports the F4 poly-free input, while subgroup inheritance proves its stated conditional virtual consequence. It does not provide an obstruction to virtual poly-freeness for H4. Every blocked route remains blocked at the exact structural assertion described in the authored family report.

No complete Kourovka resolution is verified or claimed by this review.

## Repair acceptance

The author applied the sole m=1 boundary qualification at 20:34:27 UTC. I re-read and accepted the repaired note; see `DELTA_ACCEPTANCE.md` for its exact current hash and the historical author-manifest distinction. No substantive objection remains.

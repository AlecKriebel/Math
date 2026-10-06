# Minimum positive factorization lengths and failed relaxations

This is a partial mathematical audit of K3 Problem 2.21 (problem ID 2769). It does not determine the minimum for general genus and boundary count. The results below are standard deductions, written out to identify exactly what a proposed computation would have to certify. No novelty is claimed.

## Conventions

Let S_g^b be the compact connected oriented surface with genus g and b boundary circles. Mapping classes fix the boundary pointwise. Write Delta for the product of one right-handed twist about each boundary circle. A permissible factor is a right-handed twist about a simple closed curve that is neither null-homotopic nor boundary-parallel. Separating curves are permitted. These conditions must not be replaced by the stronger requirement that every curve be nonseparating or homologically nonzero.

The intended range in the source's discussion is g >= 1 and b >= 0. For b = 0, interpret the minimum over nonempty positive identity factorizations, corresponding to fibrations with a singular fiber. Otherwise the empty word would give the vacuous minimum zero. We do not extend the question to g = 0. For b > 0 with no permissible factorization, the minimum does not exist; writing +infinity for it would be a separate bookkeeping convention.

The source and its discussion are [K3], Problem 2.21, printed pages 102–103. The target concerns a minimum and a realizing word. A supremum of lengths answers a different optimization problem.

## 1 A complete familiar subcase

**Proposition 1.** Every permissible positive factorization of Delta on S_1^1 has exactly 12 factors. Such a factorization exists.

**Proof.** A separating simple closed curve in S_1^1 bounds a disk or is boundary-parallel: the genus-zero side has either no original boundary circle or the unique original boundary circle. Thus every permissible curve is nonseparating. The abelianization homomorphism Mod(S_1^1) -> Z sends every right-handed nonseparating twist to 1 and the boundary twist to 12; see [BMVHM], Proposition 1. Applying this homomorphism to any factorization gives its length as 12. If a and d intersect once and their regular neighborhood is S_1^1, the two-chain relation gives (T_a T_d)^6 = Delta. This supplies 12 permissible factors and proves the claim. QED.

The chain relation is also used explicitly in [BK], Section 3.1. This recovers a known subcase; it does not extrapolate to higher genus.

## 2 The genus two integer obstruction

For a nontrivial relatively minimal genus-two fibration over S^2, let n and s count nonseparating and separating vanishing cycles. The established constraints in [BK], Lemma 5, are

n + 2s = 0 modulo 10,   2n - s >= 3,   n + 7s >= 20.

**Proposition 2.** These constraints imply n+s >= 7. Equality forces (n,s) = (4,3).

**Proof.** Put l=n+s. The last constraint excludes n=s=0. If l<=6, then 0<n+2s<=12, so the congruence forces n+2s=10. Consequently s=10-l and n=2l-10. The second constraint becomes 5l-30>=3, impossible for l<=6. If l=7, then 0<n+2s<=14, and the same congruence gives n+2s=10. Solving yields n=4 and s=3. QED.

[BK], Theorem 7, constructs a seven-factor boundary-twist factorization in Mod(S_2^1). Capping its boundary also gives an identity factorization. Conversely, capping a permissible curve of S_2^1 preserves essentiality: a curve becoming null-homotopic would previously have bounded a disk or an annulus with the sole boundary. Thus the established construction and obstruction settle m_2,1=7 and the nonempty closed case m_2,0=7. We do not infer a general formula from these genus-specific constraints.

## 3 Euler characteristic is the exact numerical objective

**Proposition 3.** If a genus-g pencil on a closed connected oriented four-manifold X has b base points and l nodes, then

l = e(X) + 4g - 4 + b
  = b_2(X) - 2b_1(X) + 4g - 2 + b.

For its blown-up fibration Y -> S^2, the corresponding equations are

e(Y) = 4 - 4g + l,   b_2(Y) = l - 4g + 2 + 2b_1(Y).

**Proof.** A smooth genus-g bundle over S^2 has Euler characteristic 2(2-2g). Each nodal singularity contributes one additional unit, as seen either by replacing the singular fiber by a regular fiber or by its Lefschetz two-handle. Blowing up each of the b base points adds one to Euler characteristic, so e(Y)=e(X)+b. Finally Poincare duality for a closed connected oriented four-manifold gives e(X)=2-2b_1(X)+b_2(X). Substitution proves every identity. QED.

For fixed g,b, minimizing length is therefore exactly minimizing e(X), equivalently b_2(X)-2b_1(X). Minimization of b_2 alone is equivalent when b_1 is fixed, but does not follow formally without that restriction or an additional theorem about the admissible family. This qualifies the second-Betti-number motivation; it does not establish that two actual minima differ.

## 4 A rigorous false positive for symplectic word tests

**Proposition 4.** For every g>=2 and b>=0, there is a positive word of 12 permissible nonseparating twists whose action on H_1(S_g;Z), after capping the boundary, agrees with Delta, but whose mapping class is not Delta.

**Proof.** Embed a one-holed torus in the interior with boundary gamma, choosing its complement to have genus g-1. Then gamma is essential and nonperipheral. Choose a,d in this torus with one intersection. The two-chain relation gives

W = (T_a T_d)^6 = T_gamma.

The curves a,d are nonseparating in the ambient surface. On their symplectic homology summand, choose matrices

A = [[1,1],[0,1]],   B = [[1,0],[-1,1]].

Then AB=[[0,1],[-1,1]], (AB)^3=-I, and (AB)^6=I. The action on the complementary homology summand is the identity. Equivalently, gamma is separating, so T_gamma has trivial closed-surface homology action. The same is true for every boundary twist, hence for Delta.

Choose an essential closed curve x meeting gamma essentially. Such a curve exists because both sides of gamma have positive genus. A twist about gamma moves x: the standard geometric intersection calculation is i(T_gamma(x),x)=i(gamma,x)^2>0. Boundary twists fix every closed-curve isotopy class, since it has a representative outside boundary collars. Thus W(x) differs from Delta(x), and W != Delta. This also covers b=0, when Delta is the identity. QED.

A homology-only search can reject a word whose matrix product is wrong. It cannot accept a word as a factorization of Delta from matrix equality. A finite search in bounded curve coordinates also cannot prove minimality without a theorem that every shorter factorization has a representative in its search domain. Neither missing theorem is provided here.

## 5 Restricted optimization cannot certify the unrestricted minimum

Let F be the full set of permissible factorizations and H a restricted class, such as those whose capped monodromy is hyperelliptic. If H is a subset of F, then min(F) <= min(H), provided the minima exist. Hence a lower bound proved only on H is not a lower bound on F.

For example, [Alt], Introduction, records the sharp value 12 for nontrivial genus-three hyperelliptic fibrations over S^2. It does not assert this minimum for every genus-three fibration. Additional conditions such as holomorphicity, simple connectivity, fixed Betti numbers, or extension over a handlebody similarly change the admissible set. A successful construction in a subclass supplies an upper bound for the general problem, but subclass minimality does not supply the opposite inequality.

## Exact unresolved obligation

No argument here excludes every shorter permissible word for the still-unsettled general pairs, nor constructs matching minimizers for them. Already the unrestricted genus-three one-boundary minimum is not established by these arguments. To finish the original task, one must verify the equality in Mod(S_g^b), prove a lower bound against all allowed curves, and match it with a word for every admitting pair. The report stops as partial with these obligations unproved.

## Public references

- [K3] R. Inanc Baykur, Robion C. Kirby, Daniel Ruberman, K3 – A New Problem List in Low-Dimensional Topology, author's preliminary version, Problem 2.21. https://math.berkeley.edu/sites/default/files/surv-295-ruberman-watermarked-author-pdf.pdf
- [BMVHM] R. Inanc Baykur, Naoyuki Monden, Jeremy Van Horn-Morris, Positive factorizations of mapping classes, Algebraic & Geometric Topology 17 (2017), 1527–1555. https://msp.org/agt/2017/17-3/agt-v17-n3-p06-p.pdf
- [BK] R. Inanc Baykur, Mustafa Korkmaz, Small Lefschetz fibrations and exotic 4-manifolds, Mathematische Annalen 367 (2017), 1333–1361. https://arxiv.org/abs/1510.00089
- [Alt] Tulin Altunoz, The number of singular fibers in hyperelliptic Lefschetz fibrations, Journal of the Mathematical Society of Japan 72 (2020), 1309–1325. https://www.jstage.jst.go.jp/article/jmath/72/4/72_1309/_pdf

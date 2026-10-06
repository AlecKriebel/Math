# Generic points for the two exceptional surface groups

**Problem 30006162 / OWR-14299082-004. Unresolved after five approaches.**

This report gives structural necessary conditions, a restriction lemma for continuous quasimorphisms, and a hypothesis audit. It does not prove or disprove the generic point property for either exceptional surface. The deductions below are elementary consequences of credited results, with no novelty claim. They were prepared with substantial AI assistance and have not received human peer review.

## 1. Exact target and conventions

For each of the two closed surfaces \(X=S^2\) and \(X=\mathbb{RP}^2\), let
\(G=\operatorname{Homeo}_0(X)\), with the compact-open topology. The question is whether every minimal compact Hausdorff \(G\)-flow has a comeagre orbit. This is Question 5 on printed p. 91 of Andrea Vaccaro's contribution, jointly with Gianluca Basso and Alessandro Codenotti, to [Oberwolfach Report 2/2025](https://ems.press/content/serial-article-files/51347), DOI [10.4171/owr/2025/2](https://doi.org/10.4171/owr/2025/2).

A flow is a jointly continuous action on a compact Hausdorff space. Minimal means every orbit is dense. Comeagre means its complement is meagre. We abbreviate the generic point property by GPP and write \(M(G)\) for the universal minimal flow. For Polish groups, GPP is equivalent to the existence of a comeagre orbit in \(M(G)\). Neither a generic conjugacy class nor ample generics is the property being asked for. In particular, no statement about conjugation on \(G\) is substituted for a statement about all minimal compact flows.

These groups are Polish. On a compact metric surface the topology may equivalently be described by uniform convergence of maps and inverses. Homeomorphism groups of compact manifolds are locally contractible; thus their identity components agree with their identity path components and are open and closed. See [Dirbák, Section 2.11](https://link.springer.com/article/10.1007/s00209-025-03918-0). In this setting the subscript 0 agrees with being isotopic to the identity.

On the sphere, \(\operatorname{Homeo}_0(S^2)=\operatorname{Homeo}_+(S^2)\), of index two in the full group. The orientation-isotopy assertion is recorded in [Bhat–Vlamis, Theorem 2.3](https://arxiv.org/abs/2311.00229v2). For the projective plane the mapping class group is trivial, so \(\operatorname{Homeo}_0(\mathbb{RP}^2)=\operatorname{Homeo}(\mathbb{RP}^2)\); see [Szepietowski, p. 1056](https://www.numdam.org/item/CRMATH_2002__335_12_1053_0.pdf). We do not assign an orientation-preserving subgroup to the nonorientable projective plane.

## 2. Credited structure theorems, with the quantifiers intact

Let \(H\) be a closed subgroup of a topological group \(G\). For identity neighbourhoods \(U\), the two conditions are different:

- **Presyndetic:** for every \(U\) there is a finite \(F\subset G\) such that \(G=FUH\).
- **Co-precompact:** for every \(U\) there is a finite \(F\subset G\) such that \(G=UFH\).

The order of the factors matters. We use the left-coset/right-uniformity conventions of [Basso–Zucker, arXiv:2412.05659v2](https://arxiv.org/abs/2412.05659v2), abbreviated BZ. Their Corollary 7.11 says that a Polish group is GPP exactly when it has a closed, presyndetic, extremely amenable subgroup. Their Theorem 7.12 says that its UMF is metrizable exactly when it has a closed, co-precompact, extremely amenable subgroup. Their Proposition 7.15 says that a closed presyndetic subgroup has GPP exactly when its ambient Polish group does.

The relevant nonmetrizability input is [Gutman–Tsankov–Zucker, Theorem 1.1](https://arxiv.org/abs/1910.12220), abbreviated GTZ: a locally transitive subgroup of the homeomorphism group of any closed manifold of dimension at least two has nonmetrizable UMF. Identity components of the two surface groups are locally transitive: small disk-supported isotopies move any point to nearby points. Thus **both target groups already have nonmetrizable UMF**. This does not answer the present question; BZ describe Polish GPP groups whose UMF is nonmetrizable.

There is a source-level sign hazard. BZ v2's abstract says “no points of first countability,” whereas the introduction, Theorem 7.7(2)–(3), and the proof give the opposite equivalence: for a minimal \(G\)-extremally disconnected flow, a comeagre orbit is equivalent to having a point of first countability. Applied to the UMF this says **GPP iff \(M(G)\) has a point of first countability**. We use the theorem and proof. The \(G\)-extremal-disconnectedness hypothesis cannot be dropped for an arbitrary minimal flow, and ordinary nonmetrizability does not imply absence of first-countability points.

## 3. A point-stabilizer reduction and finite-configuration obstruction

All claims in this section hold for any closed connected surface. Fix \(p\in X\) and set \(K=G_p\).

### Proposition 1

The closed subgroup \(K\) is both presyndetic and co-precompact. It has GPP if and only if \(G\) has GPP. Its UMF is nonmetrizable, and \(K\) is not extremely amenable.

**Proof.** The evaluation map \(G\to X\), \(g\mapsto gp\), is onto and open, and has continuous local sections. The latter can be made by disk-supported isotopies; [Dirbák, Lemma 5.29](https://link.springer.com/article/10.1007/s00209-025-03918-0) gives an explicit construction. Hence \(G/K\cong X\).

For any open identity neighbourhood \(U\), \(Up\) is open. The sets \(fUp\), \(f\in G\), cover the compact space \(X\), so finitely many suffice. This gives \(G=FUK\). Also \(Uy\) is open for every \(y\in X\), and the family \(\{Uy:y\in X\}\) covers \(X\); choose finitely many \(y_i=f_ip\) to get \(G=UF'K\). These two arguments establish the two properties separately, without interchanging factors.

BZ Proposition 7.15 gives the equivalence of GPP. If \(K\) had metrizable UMF, BZ Proposition 7.16 and co-precompactness would give metrizable UMF for \(G\), contradicting GTZ. In particular, \(K\) is not extremely amenable. Alternatively, its extreme amenability and co-precompactness would directly contradict BZ Theorem 7.12 and GTZ. \(\square\)

### Proposition 2

If a subgroup \(H\leq G\) preserves a finite subset \(A\subset X\) with \(|A|\geq2\) setwise, then \(H\) is not presyndetic. Closedness is not needed for this statement.

**Proof.** Fix a compatible metric \(d\) on \(X\), and let
\(\delta=\min\{d(a,b):a,b\in A,\ a\neq b\}>0\).
Take the open identity neighbourhood
\[
U=\{u\in G:\sup_{z\in X}d(uz,z)<\delta/4\}.
\]
For every \(u\in U\), distinct points of \(uA\) are separated by more than \(\delta/2\). Fix any nonempty finite \(F\subset G\). For each \(f\in F\), compactness and injectivity give
\[
\eta_f=\min_{d(x,y)\geq\delta/2}d(fx,fy)>0,
\qquad \eta=\min_{f\in F}\eta_f>0.
\]
Consequently, for every \(g\in FUH\), the set \(gA=f(uA)\) has pairwise separation at least \(\eta\), because \(hA=A\).

The identity component of the homeomorphism group of a connected surface is transitive on ordered pairs of distinct points. One can move a point along a path by successive disk-supported isotopies; after fixing that point, one moves the second along a path in its connected punctured complement. Therefore some \(g_0\in G\) sends a chosen pair from \(A\) to two distinct points at distance less than \(\eta\). This contradicts \(g_0\in FUH\). The same fixed \(U\) defeats every finite \(F\), which is exactly the negation of presyndeticity. \(\square\)

### Corollary 3: what an affirmative certificate would have to look like

If either target group is GPP, it contains a closed, presyndetic, extremely amenable subgroup \(H\) satisfying all of the following:

1. \(H\) fixes exactly one point \(p\in X\). This singleton is its only finite orbit on \(X\).
2. \(H\subsetneq G_p\), and \(H\) is presyndetic in \(G_p\).
3. \(H\) is not co-precompact in \(G\), nor in \(G_p\).
4. \(H\) is not normal in \(G_p\), hence also is not normal in \(G\).

**Proof.** Extreme amenability supplies a common fixed point in the compact \(H\)-space \(X\). Proposition 2 excludes two fixed points, any other finite orbit, and any finite invariant set of size at least two. Proposition 1 excludes \(H=G_p\). Presyndeticity passes to the intermediate closed subgroup \(G_p\) by BZ Proposition 7.2. Co-precompactness in \(G\) is ruled out by GTZ and BZ Theorem 7.12. Co-precompactness in \(G_p\), combined with that of \(G_p\) in \(G\), would imply it in \(G\), by BZ Proposition 7.4.

If \(H\) were normal in \(G_p\), the presyndetic condition would make the quotient group \(G_p/H\) precompact: every identity neighbourhood in that quotient would have finitely many left translates covering it. In a topological group, inversion turns this into the analogous finite right-translate condition. Pulling it back gives co-precompactness of \(H\) in \(G_p\), a contradiction. If \(H\) were normal in \(G\), it would also be normal in \(G_p\). \(\square\)

These restrictions do not prove that no such \(H\) exists. In particular, failure of all the finite-point stabilizer models does not exhaust the closed extremely amenable subgroups.

## 4. Full groups, the antipodal cover, and the missing transfer

The sphere's index-two identity component is presyndetic in the full homeomorphism group: choose representatives \(F\) of its two cosets, and \(F H=G\subseteq FUH\) for every identity neighbourhood \(U\). Thus BZ Proposition 7.15 makes GPP for the full sphere group equivalent to the exact identity-component question. For \(\mathbb{RP}^2\) the two groups are equal. This reconciles the full-group wording in BCV Question 1.4 with OWR Question 5.

Let \(a(x)=-x\) on \(S^2\). Covering-space lifting gives an isomorphism
\[
\operatorname{Homeo}(\mathbb{RP}^2)
\cong C_{\operatorname{Homeo}_+(S^2)}(a).
\]
Indeed each projective-plane homeomorphism has exactly two sphere lifts, differing by \(a\); these commute with \(a\). The antipodal map has degree \(-1\), so exactly one lift is orientation preserving. Uniqueness makes the choice multiplicative. Conversely, an orientation-preserving map commuting with \(a\) descends, and the kernel is trivial. The descent homomorphism is continuous between Polish groups, hence its bijectivity makes it a topological isomorphism by the open-mapping theorem for Polish groups.

This identifies a closed centralizer subgroup, **not a quotient of the whole sphere homeomorphism group**. An arbitrary sphere homeomorphism need not preserve antipodal pairs. GPP has no unrestricted closed-subgroup inheritance theorem. To use BZ Proposition 7.15 here one would have to establish presyndeticity of this particular centralizer, which is not established in this report. Consequently neither answer transfers between the two surfaces by the double cover alone.

## 5. Chain methods: credited restrictions are still insufficient

Let \(\Phi(X)\) be the compact metrizable double-Vietoris space of maximal chains of nonempty subcontinua of \(X\). This is the connected-chain space, not the larger space of all maximal chains of arbitrary closed sets. The \(G\)-action on \(\Phi(X)\) is minimal for the two targets, by the locally transitive case of Gutman's theorem as recorded in GTZ and BCV. Therefore GPP would force a comeagre orbit here; proving that no such orbit exists would give a negative answer. A comeagre chain orbit alone would not verify all minimal flows or identify the nonmetrizable UMF with this metrizable chain space.

[BCV Theorem 1.2](https://arxiv.org/abs/2403.08667v3) rules out generic chains when a Peano continuum without locally separating points has one of three additional features: a locally nonplanar open set, a planar open set containing a non-locally-separating simple closed curve, or a circular covering. Neither exceptional surface satisfies these sufficient hypotheses. The one-sided essential curve in \(\mathbb{RP}^2\) does not lie in a planar open neighbourhood, so it does not satisfy the second alternative. The circular-cover exception is explicit in BCV Proposition 6.13. Missing these sufficient hypotheses proves neither existence nor nonexistence of generic chains.

The earlier authored [thin-chain report for problem 30006161](https://github.com/AlecKriebel/Math/blob/91ddfb046912817229202f5478487cf91fcb3e36/unsolved_math_prioritization/attempts/30006161/PARTIAL_RESULT.md), with its separate review, proves that comeagrely many chains have empty interior in every proper member. Its disk-containing chain orbits are meagre despite being dense. It also gives the standard nerve argument that a circular cover forces a fundamental-group quotient \(\pi_1(X)\twoheadrightarrow\mathbb Z\), impossible for either exceptional surface. These are credited prior partial results, not new results of this report and not a resolution of the present ID.

For the minimal Polish chain action, the unresolved Rosendal condition has the form
\[
\forall U\ni 1_G\ \forall A\neq\varnothing\text{ open}\
\exists B\neq\varnothing\text{ open},\ B\subset A\
\forall C,D\neq\varnothing\text{ open},\ C,D\subset B:\ UC\cap D\neq\varnothing.
\]
To disprove it, one fixed \(U,A\) must defeat every nonempty open refinement \(B\). Excluding a named disk chain, checking finitely many walks, or showing local turbulent points does not discharge these quantifiers. The BCV off-by-one weak-amalgamation condition is necessary; it was not shown sufficient in the source.

## 6. Newer cocycle and quasimorphism routes

### 6.1 The homotopical construction cannot simply be specialized

[Dirbák, Theorem 1.3 and Lemma 5.28](https://link.springer.com/article/10.1007/s00209-025-03918-0) construct a minimal circle extension of the evaluation action with meagre orbits for closed surfaces with \(\chi(X)<0\). The proof starts with a non-nullhomotopic map \(X\to\mathbb T\) and uses simple connectedness of \(\operatorname{Homeo}_0(X)\) in that regime. Here \(\chi(S^2)=2\) and \(\chi(\mathbb{RP}^2)=1\). In addition,
\[
H^1(S^2;\mathbb Z)=H^1(\mathbb{RP}^2;\mathbb Z)=0.
\]
For \(\mathbb{RP}^2\), this follows from \(H_1\cong\mathbb Z/2\) and \(\operatorname{Hom}(\mathbb Z/2,\mathbb Z)=0\); its torsion in integral homology must not be mistaken for nonzero integral first cohomology. Thus the initial circle map of that proof is unavailable. This rules out that specialization, not all possible circle cocycles.

### 6.2 A rigorous restriction lemma for the September 2026 result

A real homogeneous quasimorphism is a function \(q\) with \(q(g^n)=nq(g)\) for integers \(n\), and finite defect
\(D(q)=\sup_{g,h}|q(gh)-q(g)-q(h)|\).

**Proposition 4.** Let \(q:G\to\mathbb R\) be a continuous homogeneous quasimorphism on a topological group, and let \(H\leq G\) be presyndetic. If \(q|_H\) is bounded then \(q=0\). Consequently restriction is injective on the vector space of continuous homogeneous quasimorphisms.

**Proof.** Choose an identity neighbourhood \(U\) with \(|q(u)|\leq1\) for \(u\in U\), and a finite \(F\) with \(G=FUH\). Let \(B\) bound \(|q|\) on \(H\). Twice applying the defect inequality to \(g=fuh\) gives
\[
|q(g)|\leq\max_{f\in F}|q(f)|+1+B+2D(q)=:C.
\]
Thus \(|nq(g)|=|q(g^n)|\leq C\) for every positive integer \(n\), forcing \(q(g)=0\). For injectivity, apply the result to a difference of two continuous homogeneous quasimorphisms whose restrictions coincide. \(\square\)

[Böke, arXiv:2602.10707v2](https://arxiv.org/abs/2602.10707v2), revised September 29, 2026, Theorem 1.1, gives an infinite-dimensional space of nontrivial homogeneous quasimorphisms on \(\operatorname{Homeo}_0(\mathbb{RP}^2)\). Remark 4.12 invokes their continuity for the compact-open topology, referring to the appendix of Bowden–Hensel–Webb. This is current preprint evidence, not a published solution of the GPP question.

Combining that credited continuity input with Proposition 4 yields an additional necessary condition: **every presyndetic subgroup of the projective-plane group has an infinite-dimensional space of continuous homogeneous quasimorphisms, by injective restriction.** In particular, any extremely amenable certificate in Corollary 3 would have to carry such restrictions.

The missing step in turning this observation into a negative GPP answer is a vanishing theorem applicable to these possibly non-locally-compact, topologically extremely amenable subgroups. This report does not establish one. Discrete-group amenability results about quasimorphisms cannot simply be applied to a subgroup that is only extremely amenable in its inherited Polish topology. Nor has continuity of the relevant translation action on a compact space of functions been established by pointwise boundedness alone. Accordingly, positive stable commutator length is not promoted here to a GPP obstruction. Proposition 4 remains valid independently of that missing step, and the conditional consequence precisely identifies what another argument would have to resolve.

## 7. Outcome and verification limits

The five approaches were: metrizability/first-countability certificates; point and finite-configuration stabilizers; finite-index and double-cover transfer; maximal-chain amalgamation; and newer cocycle/quasimorphism obstructions. None produced a complete positive or negative answer. No current checked source proves either target case; absence of a found source is not a proof of global literature completeness.

The established partial results are Propositions 1, 2 and 4 and Corollary 3, with the indicated credited inputs. The exact remaining certificate problem is existence of a closed extremely amenable presyndetic subgroup satisfying those restrictions, or, equivalently, a minimal compact counterflow without a comeagre orbit. The finite program checks elementary arithmetic, product-order examples, and finite diagnostic instances of the estimates. It does not certify a theorem about infinite-dimensional Polish dynamics, Baire category, the cited source proofs, or the existence of the required subgroup.

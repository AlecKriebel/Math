# Relatively isolated infinite-order conjugacy classes

Research checkpoint: 2026-10-24, begun after the independent Lie attempt. Full-problem outcome: **unsolved**, with a new local structural reduction. No originality or publication claim is made. Completion estimate remains **10%** until additional structural input handles arbitrary profinite groups.

## 1. Exact local question

An infinite-order element x of a profinite group G has a **relatively isolated infinite-order conjugacy class** if some open neighborhood U of x satisfies

\[
U\cap\{y\in G:y\text{ has infinite order}\}\subseteq x^G.
\tag{LI}
\]

This does not say x^G is open in G. Torsion elements may occupy most of U. A class satisfying (LI) may coexist with continuum many infinite-order classes elsewhere in G. Thus proving the nonexistence of such a class is a stronger local assertion than the original small-class problem, and it must not be assumed.

The parent's class-space argument shows that a countably based counterexample to 21.136 would have a class satisfying (LI): the infinite-order class space is a nonempty countable Polish space and hence has an isolated point. That argument is kept separately in root_class_space.md and its independent review.

All arguments below use ambient conjugacy. No inheritance of the class bound or torsion density by arbitrary closed subgroups is used.

## 2. Isolation survives quotienting by an abelian normal subgroup

**Theorem.** Let A be a closed abelian normal subgroup of a profinite group G. If x has infinite order and satisfies (LI), then its image b in B=G/A has infinite order and itself satisfies (LI) in B.

**Proof.** Let π:G→B be the quotient map and choose U as in (LI). The set π(U) is an open neighborhood of b, because a topological group quotient map is open.

Suppose first, toward a contradiction, that b has finite order q. Then every element of π(U) is torsion. Indeed, an infinite-order element c∈π(U) has a lift y∈U, necessarily of infinite order. By (LI), y is conjugate to x, so c is conjugate to b, contradicting the finite order of b.

It follows that C_B(b) is torsion. To see this, choose an open subgroup K of C_B(b), small enough that bK⊆π(U). For every k∈K, the elements b and k commute, b has finite order, and bk has finite order. Thus k=(b^{-1})(bk) has finite order. Hence K is torsion. Since K has finite index in C_B(b), every element c of that centralizer has a positive power in K, and therefore has finite order itself. No uniform exponent or normality of K is needed.

Now choose an integer n>1 with n≡1 modulo q and x^n∈U. Such integers exist: choose an open normal subgroup N with xN⊆U, let d be the finite order of xN in G/N, and take n=1+lcm(d,q). The element x^n still has infinite order, so (LI) supplies g∈G with

\[
x^g=x^n.
\]

Modulo A, the congruence n≡1 mod q gives b^{π(g)}=b. Thus π(g) belongs to the torsion group C_B(b). For some m≥1 we have g^m∈A.

Put a=x^q∈A. This element has infinite order. Conjugating the displayed power relation q times and iterating conjugation by g gives

\[
a^{g^m}=a^{n^m}.
\]

But g^m and a belong to abelian A, so the left side is a. Thus a^{n^m-1}=1, impossible since n^m−1>0 and a has infinite order. This contradiction proves b has infinite order.

Finally, every infinite-order c∈π(U) has a lift y∈U of infinite order. Such y is conjugate to x, hence c is conjugate to b. Therefore π(U) witnesses (LI) for b. □

**Scope of the key repair.** It is not asserted that B itself is torsion. Only C_B(b) is shown torsion under the temporary assumption that b is finite. The generalized dihedral group shows why an open torsion coset in a nonabelian quotient cannot be replaced by an open torsion subgroup without an argument. Passing to the centralizer of b is what makes the torsion-subgroup argument valid.

## 3. Consequence: virtually soluble profinite groups have no such class

**Corollary.** No virtually soluble profinite group contains a relatively isolated conjugacy class of infinite-order elements.

**Proof.** Let N be an open normal soluble subgroup of G; obtain one by taking the core of an open soluble subgroup if necessary. Induct on the finite derived length of N. If N=1, G is finite and the conclusion is immediate. Otherwise its last nontrivial closed derived subgroup A is abelian, closed, and characteristic in N, hence normal in G. If x satisfied (LI), the theorem would produce an infinite-order element satisfying (LI) in G/A. But N/A is open, normal and of strictly smaller derived length there, contradicting induction. □

Thus the class-space reduction gives the original torsion conclusion for virtually soluble profinite groups without imposing finite generation or a countable basis on the original G: reduce a hypothetical counterexample to a countably based quotient, retain virtual solubility in that quotient, and obtain an isolated class. This is a restricted result, not a proof for arbitrary prosoluble groups of unbounded derived length.

The local quotient theorem was independently audited by the Lie adversary after its author first found the metabelian case through a different action-norm mechanism. The full local theorem still requires the root's fresh nonauthor audit before any stronger presentation claim. No first-priority assertion is made.

## 4. Small conjugators and the exact extra force of isolation

Suppose C=cl⟨x⟩≅Z_p. Isolation alone forces the normalizer action N_G(C)→Aut(C) to have open image: all generators x^u with u sufficiently close to 1 lie in U and hence are conjugate to x; their conjugators normalize C.

The compact normalizer action is a quotient map onto its image, so arbitrarily small normalizer neighborhoods have open images. One can find h_j→1 inducing nontrivial power automorphisms λ_j∈1+pZ_p (use 1+4Z_2 when p=2), with λ_j→1 and λ_j of infinite order. Each h_j has infinite order. The elements y_j=xh_j normalize C and act on C by λ_j; they consequently have infinite order and tend to x. Isolation gives y_j∈x^G.

Moreover, their conjugators can be chosen tending to 1. For an open normal subgroup M of G, the conjugacy class x^G splits into finitely many disjoint M-orbits, each compact and hence closed. Each orbit is therefore also relatively open in x^G. Thus y_j→x eventually lies in x^M; taking a shrinking sequence of M gives a subsequence with x^{g_j}=y_j and g_j→1. In a nonmetrizable group the corresponding statement is naturally a net; the parent's counterexample reduction supplies metrizability when needed.

The resulting relations include

\[
(x^{g_j})^{-1}x(x^{g_j})=x^{\lambda_j},
\qquad g_j\to1,\quad \lambda_j\to1.
\]

They are necessary local constraints, not a contradiction proved here. The closed subgroup generated by x and x^{g_j} is metabelian, but it need not be open and has not inherited P0. Applying the metabelian P0 theorem to it would therefore be invalid.

## 5. Why a fixed Baumslag/Higman relation does not settle the local question

For a finite group, if y has the same order d as x and x^y=x^k, then d divides k^d−1. At k=2 the least-prime-divisor argument forces d=1. At k=1+p^s, however, this numerical obstruction is compatible with arbitrarily large p-power d. For example, for odd p the lifting-the-exponent formula gives

\[
v_p\bigl((1+p^s)^{p^r}-1\bigr)=s+r,
\]

and for p=2 the same formula holds when s≥2. Hence p^r divides the displayed power difference for every r. No contradiction follows just from equality of orders.

A primary structural control is Glebsky, [*p-quotients of the G. Higman group*, arXiv:1604.06359](https://arxiv.org/abs/1604.06359), especially the introduction and Corollary 1. For p∣(k−1), its generalized Higman group

\[
H(k)=\langle a_0,a_1,a_2,a_3\mid a_i^{-1}a_{i+1}a_i=a_{i+1}^{k}\ (i\bmod4)\rangle
\]

has p-group images in which the orders of the generators are unbounded; its pro-p completion retains the infinite cyclic subgroups generated by the a_i. The order-four cyclic permutation of its generators acts continuously on that completion. For p=2 and odd k, adjoining this rotation gives a pro-2 group containing infinite-order x=a_0 and a conjugate y=a_3 with x^y=x^k. Thus a single relation involving conjugate power-conjugators is compatible with profiniteness. This use is a prior-theorem control; the source's entire proof has not been formally verified here.

This does **not** exhibit a relatively isolated infinite-order class, does not verify the required uniform family near 1, and is not a counterexample to 21.136. The rotation conjugator in this construction is fixed, so it cannot be substituted for the small-conjugator conclusion in Section 4.

## 6. Locally nilpotent kernels and finite normal series

The quotient theorem extends to a **closed normal abstract locally nilpotent** subgroup A. The temporary assumption that b=π(x) is finite again makes C_(G/A)(b) torsion, producing g and m with h=g^m∈A and a=x^q∈A of infinite order such that

\[
a^h=a^{n^m}.
\]

The abstract subgroup ⟨a,h⟩ is nilpotent by local nilpotence. Put r=n^m−1>0. With [u,v]=u^{-1}v^{-1}uv, induction gives

\[
[a,{}_j h]=a^{r^j}\quad(j\ge1),
\]

since h acts by the indicated power on the cyclic group generated by a. If ⟨a,h⟩ has nilpotency class c, its commutator of weight c+1 vanishes, giving a^{r^c}=1. This contradicts infinite order. Thus π(x) remains infinite and retains (LI).

A closed normal torsion kernel also preserves infinite order of the image directly: if x had a finite-order image, some positive power of x would belong to the torsion kernel, making x finite-order. Isolation passes to the quotient by the same open-map lifting argument.

Consequently no profinite group with a finite closed G-normal series whose factors are each torsion or abstract locally nilpotent has a class satisfying (LI). Repeatedly take these quotients; the image must remain infinite-order and isolated all the way to the trivial quotient, which is impossible. This includes virtually soluble profinite groups. It does **not** include an arbitrary pronilpotent group: being an inverse limit of finite nilpotent groups is not the assertion that its finitely generated abstract subgroups are nilpotent.

## 7. Further elementary constraints and a limiting control

Every neighborhood of an element satisfying (LI) contains torsion elements of unbounded finite orders. Otherwise some smaller neighborhood W of x would have all its torsion elements in a single closed set E_d={g:g^d=1}. Shrink around x to avoid E_d. This gives a nonempty open set consisting entirely of infinite-order elements conjugate to x, so x^G has interior. An infinite-order class cannot have interior: counting its images in finite quotients would bound the sizes of all images of C_G(x), forcing that centralizer finite despite its containing cl⟨x⟩. The contradiction proves the claim.

In particular no group with an open torsion-free subgroup has an (LI) class. Indeed torsion elements of such a group have uniformly bounded orders: after taking the normal core N of the open torsion-free subgroup, their orders divide the exponent of the finite quotient G/N.

The procyclic closure C=cl⟨x⟩ of an (LI) element has only finitely many prime divisors. If it had infinitely many nontrivial Sylow components, every neighborhood of x in C leaves some prime component unrestricted. Delete just that component, preserving infinitely many other nontrivial components and hence infinite order. This produces a nearby infinite-order element of different supernatural order, so it cannot be conjugate to x.

The normalizer N_G(C) must have infinite index in G. To prove this, first note that (LI) restricts to an open subgroup H containing x. The compact class x^G splits into finitely many compact H-orbits. Remove the finitely many orbits different from x^H from the original isolating neighborhood. In the resulting neighborhood, the (LI) conclusion is H-conjugacy. If N_G(C) were open, take H=N_G(C). Then C is abelian normal in H, but the quotient theorem would force the image xC=1 to have infinite order. This is impossible.

The abstract-local-nilpotence hypothesis in Section 6 cannot be replaced by pronilpotence. For an explicit control, let A=Z_3⋊Z_3 with multiplication

\[
(u,s)(v,t)=(u+4^{-s}v,s+t).
\]

This is pro-3. For a=(1,0) and h=(0,1) one has a^h=a^4 and

\[
[a,{}_j h]=a^{3^j}\ne1\qquad(j\ge1).
\]

The commutators tend to 1 but never vanish. Thus inverse limits of finite nilpotent groups do not supply the terminating commutator needed in Section 6. This control is itself metabelian and has no (LI) class; it only falsifies the attempted replacement of a kernel hypothesis.

## 8. Current exact gap

An arbitrary profinite group need not have a nontrivial kernel of one of these types with a quotient of lower complexity. Infinite prosoluble derived series, nonabelian pro-p factors, and infinite products of nonabelian simple sections remain outside this reduction. The required normal subgroup cannot be inferred from the mere existence of a relatively isolated infinite-order class using any argument established here.

No example satisfying (LI), no proof excluding it in all profinite groups, and no complete resolution of the original problem have been obtained. The general local assertion remains a precise unsupported step; it is not promoted to a lemma.

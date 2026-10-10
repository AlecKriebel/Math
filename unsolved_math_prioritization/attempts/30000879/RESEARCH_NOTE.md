# Trivial restrictions of nilpotent twists

## Partial results and the remaining question

Let G be torsion-free nilpotent with finite integral cohomological dimension cd_Z(G)=n, let α∈H²(G,C×), and put R=C^αG. Aljadeff asks whether a subgroup H≤G satisfies both α|_H=0 and gldim(CH)=gldim(R). The question appears as Problem 3 on printed page 3171 of *Mini-Workshop: Arithmetik von Gruppenringen*, Oberwolfach Report 55/2007 [1]. That source reports the case gldim(R)=n as already affirmative; this note neither supplies nor claims to have checked its unnamed proof.

The general remaining case gldim(R)<n is **not resolved here**. The results below provide two rigorous reductions and their limitations:

1. If G has nilpotency class c≥1, every class α vanishes on γ_m(G), where m=⌈(c+2)/2⌉ and γ_i is the lower central series. This statement requires neither torsion-freeness nor finite generation. The universal cutoff m cannot be decreased, even among finitely generated torsion-free nilpotent groups of finite cohomological dimension.
2. The original hypotheses imply that G is countable. If d is the supremum of gldim(C^αK) over its finitely generated subgroups K, then d≤gldim(R)≤d+1. If the upper alternative occurs, every subgroup witnessing Aljadeff's conclusion must be infinitely generated.

The countable direct-limit bound is a classical homological-algebra fact; see Osofsky's Proposition 2.1 [2]. A complete proof in the precise twisted-group-algebra setting is included below. No originality claim is made for that bound or the elementary boundary cases. The lower-central argument and explicit optimality examples are fully proved here; their novelty has not been certified by a comprehensive literature review.

Throughout the proofs, gldim means **left global dimension**. The same arguments with sides reversed establish the corresponding statements for right global dimension. No unproved left/right equality for arbitrary nonnoetherian rings is needed. Cohomological restriction α|_H=0 means that the class is a coboundary on H; it does not require a selected cocycle to equal 1 pointwise. No Gelfand–Kirillov or Krull dimension is substituted for global dimension.

## 1 Subgroup restriction and induction

Choose a normalized cocycle a representing α, and write u_g u_h=a(g,h)u_gh. For H≤G put B=C^{a|_H}H⊆R.

**Lemma 1.** The ring R is free as a left and as a right B-module, and

    gldim(B) ≤ gldim(R).

**Proof.** Representatives for the right cosets H\G give a decomposition R=⊕ B u_t as left B-modules; representatives for left cosets G/H give R=⊕u_t B as right B-modules. The cocycle scalars are nonzero, so each summand has the asserted free basis. In particular both induction and restriction have the projectivity properties used next: right-B freeness makes R⊗_B− exact, induction sends B-projectives to R-projectives, and left-B freeness makes restriction send R-projectives to B-projectives.

As B-bimodules, R=B⊕V, where V is the span of u_g with g∉H. Multiplication on either side by an element of H preserves G\H. Thus for every left B-module M,

    Res_B(R⊗_B M) ≅ M ⊕ (V⊗_B M).

If gldim(R)=r<∞, restrict a length-r R-projective resolution of R⊗_B M. It is still exact and consists of B-projectives. Its direct summand M therefore has projective dimension at most r. Taking the supremum over M proves the inequality. The infinite case is automatic. □

If α|_H=0, rescaling the homogeneous basis by a trivializing 1-cochain identifies B with CH. Consequently

    α|_H=0  ⇒  gldim(CH)≤gldim(C^αG).                 (1)

An arbitrary subring inclusion would not suffice for this conclusion; the freeness and bimodule splitting above are essential to this proof.

**Finite global dimension without a finiteness assumption on G.** For clarity, the upper bound gldim(C^αG)≤cd_Z(G) can also be justified directly. Extension of scalars sends a length-n projective ZG-resolution of Z to a projective CG-resolution of C: C is flat over Z. If P is a left CG-module and M a left R-module, equip P⊗_C M with the diagonal twisted action

    u_g(p⊗m)=(g·p)⊗(u_g·m).

This obeys the cocycle multiplication law. When P=CG, the map R⊗_C M→CG⊗_C M given by u_g⊗m↦g⊗u_g m is an R-module isomorphism from a free R-module onto this diagonal module; its inverse uses the invertible action of u_g. If P is CG-projective, split it off a free CG-module and tensor the equivariant splitting with M. Thus P⊗_C M is R-projective. Tensoring the projective CG-resolution of C with the vector space M now gives an exact length-n R-projective resolution of M. This proves the upper bound for every M. This argument only uses cd_C(G)≤cd_Z(G); it does not identify those two dimensions in general.

## 2 Countability under the exact original hypotheses

**Lemma 2.** A torsion-free nilpotent group of finite integral cohomological dimension is countable.

**Proof.** Set n=cd_Z(G). Integral cohomological dimension does not increase on passing to a subgroup: restricting a projective ZG-resolution of Z gives a projective ZH-resolution, because ZG is free over ZH. Also cd_Z(Z^k)=k, as follows from the usual length-k Koszul resolution over Z[t_1^{±1},…,t_k^{±1}] and its nonzero top cohomology with trivial Z coefficients. Hence G cannot contain Z^{n+1}.

Choose a maximal abelian normal subgroup A of G. It exists by Zorn's lemma, since the union of a chain of abelian normal subgroups is again abelian and normal. We claim C_G(A)=A. Write C=C_G(A). Normality of A makes C normal in G. If C/A is nontrivial, then it is a nontrivial normal subgroup of the nilpotent group G/A. Every nontrivial normal subgroup N of a nilpotent group P meets Z(P) nontrivially: take the last nontrivial term among N,[N,P],[[N,P],P],… . Thus some x∈C\A has xA∈Z(G/A). The subgroup ⟨A,x⟩ is abelian because x centralizes A; it is normal because every conjugate of x differs from x by an element of A. This contradicts maximality, proving the claim.

As a torsion-free abelian subgroup, A embeds in Q⊗_Z A. Its rational rank t is at most n: otherwise n+1 rationally independent elements of A generate Z^{n+1}. Therefore A embeds in Q^t and is countable. Every automorphism of A extends uniquely to a Q-linear automorphism of Q⊗A, so Aut(A) embeds in GL_t(Q) and is countable. Conjugation gives an injection G/A→Aut(A), its kernel being C_G(A)/A=1. Thus G is a countable union of cosets of the countable group A. □

For G=1 the conclusion is immediate, and the rank-zero cases in this argument cause no exception. This proof imports no finite-rank structure theorem and makes no finite-generation assumption about G.

## 3 The one-dimension obstruction to a finitely generated reduction

**Theorem 3.** Suppose G is countable, a is a normalized cocycle with values in C×, and

    d = sup { gldim(C^{a|_K}K) : K≤G finitely generated } <∞.

Then

    d ≤ gldim(C^aG) ≤ d+1.                          (2)

**Proof.** Enumerate G and let G_1≤G_2≤… be the subgroups generated by initial finite segments; their union is G. Put R_i=C^{a|_{G_i}}G_i and R=C^aG. Every finitely generated subgroup lies in some G_i. By Lemma 1,

    d=sup_i gldim(R_i)≤gldim(R).

Let M be an arbitrary left R-module, without a finite-generation assumption. Define N_i=R⊗_{R_i}Res_{R_i}M and let f_i:N_i→N_{i+1} send r⊗m to r⊗m. Since R is right-R_i free, inducing a projective resolution gives pd_R(N_i)≤d.

The multiplication maps N_i→M induce an isomorphism colim_i N_i→M. Surjectivity follows from m↦1⊗m. For injectivity, any element has a representative ∑_j r_j⊗m_j in one N_i. All the finitely many r_j lie in some R_k with k≥i, and its image in N_k is 1⊗∑_j r_jm_j. It vanishes if its image in M vanishes.

The countable telescope sequence is exact:

    0 → ⊕_i N_i --T--> ⊕_i N_i → M → 0,
    T(ι_i(x))=ι_i(x)−ι_{i+1}(f_i(x)).

To see that T is injective, the first coordinate of a finitely supported kernel vector is zero, then the second is zero, and so on. Its cokernel is precisely the direct limit by the defining relations. Direct sums of length-d projective resolutions give pd_R(⊕N_i)≤d. The short exact sequence, or its Ext long exact sequence, then gives pd_R(M)≤d+1. Since M was arbitrary, (2) follows. □

Applied to the original target, Lemma 2 supplies countability and Lemma 1 bounds d by the finite r=gldim(R). The finite integer supremum d is attained by some finitely generated K.

**Corollary 4.** In the original target:

- If r=d and the question is affirmative for one finitely generated K with gldim(C^{α|_K}K)=d, then it is affirmative for G.
- If r=d+1, no finitely generated subgroup H≤G can satisfy α|_H=0 and gldim(CH)=r.

**Proof.** In the first case a subgroup witnessing the conclusion inside K also lies in G. In the second, a finitely generated H with α|_H=0 has

    gldim(CH)=gldim(C^{α|_H}H)≤d<r,

by the definition of d. This uses equality of the two H-algebras up to the cochain rescaling, and does not assert that arbitrary untwisted subalgebras control the ambient dimension. □

This does not prove the finitely generated conjecture. Even a future proof of that case would leave the dimension-jump alternative to address.

## 4 A genuine dimension jump within the stated class

The extra 1 in (2) is real even for a trivial twist in the original class. Let G=(Q,+) and α=0. Every nontrivial finitely generated subgroup is infinite cyclic, so d=1. Nevertheless

    gldim(CQ)=2.

Here is a direct ring-theoretic proof. The upper bound is Theorem 3. Put R=CQ and let I be its augmentation ideal. R is a domain: the highest exponent in the product of two nonzero finitely supported sums is the sum of their highest exponents and has nonzero coefficient.

The ideal I is not finitely generated. Otherwise the finite union of supports of generators is contained in a cyclic subgroup H<Q. Those generators have augmentation zero in CH, so I⊆R I_H. But R/(R I_H)≅C[Q/H], whose augmentation ideal is nonzero because H≠Q; hence R I_H is strictly smaller than I, a contradiction.

Every nonzero projective ideal J of a commutative domain is finitely generated. Indeed, choose a split injection j:J→R^{(S)}. After tensoring with the fraction field F, F⊗J is one-dimensional, so all j(y) have support contained in the finite support of j(x) for one nonzero x∈J. If S_0 is that finite support, a retraction R^{(S)}→J restricts to a surjection R^{S_0}→J. Thus J is finitely generated.

It follows that I is not projective. The exact sequence 0→I→R→C→0 then implies pd_R(C)>1, giving the lower bound 2.

For completeness G also has finite integral cohomological dimension: the same telescope applied to the trivial ZQ-module and its cyclic subgroup restrictions gives cd_Z(Q)≤2. The augmentation-ideal argument over ZQ, using its fraction field, gives cd_Z(Q)>1. Thus cd_Z(Q)=2.

This example is **not a counterexample** to Aljadeff: H=G witnesses the desired conclusion. It shows why a realizing subgroup need not be finitely generated, and why replacing G by one finitely generated subgroup loses information.

## 5 Automatic splitting on a deep lower central subgroup

Write γ_1(G)=G and γ_{i+1}(G)=[γ_i(G),G]. The standard commutator inclusion

    [γ_i(E),γ_j(E)] ⊆ γ_{i+j}(E)                  (3)

holds for every group E. It follows by induction from the commutator identities and the three-subgroup identity; it involves the lower central series, not the derived series.

**Theorem 5.** Let G be nilpotent of class at most c≥1, and let α∈H²(G,C×), with trivial action on the coefficients. If 2m≥c+2, then

    α|_{γ_m(G)}=0.                                  (4)

In particular m=⌈(c+2)/2⌉ works. No finite-generation or torsion-freeness hypothesis is required.

**Proof.** Represent α by a central extension

    1→C×→E --π--> G→1.

It may be constructed explicitly as E=C××G with multiplication (s,g)(t,h)=(st a(g,h),gh). Since γ_{c+1}(G)=1, γ_{c+1}(E) lies in the central kernel, and therefore γ_{c+2}(E)=1.

Surjectivity of π implies π(γ_m(E))=γ_m(G): lift each iterated commutator and its products. Hence

    π^{-1}(γ_m(G))=C×·γ_m(E).

By (3) and 2m≥c+2, γ_m(E) is abelian. The other factor C× is central, so the entire preimage is abelian. Its extension of γ_m(G) by C× is now an extension in the category of abelian groups.

The multiplicative group C× is divisible and therefore injective as an abelian group. To recall the relevant elementary argument, a homomorphism from a subgroup B of an abelian group D into a divisible abelian group can be extended one element at a time. For x∈D\B, if no positive multiple of x lies in B, choose its image arbitrarily. Otherwise let k be the least positive integer with kx∈B and choose a k-th root of the already prescribed image of kx. This extends the map consistently to B+Zx. Zorn's lemma gives an extension to D.

Apply this extension property to the identity of the embedded C×. It yields a retraction π^{-1}(γ_m(G))→C×. The kernel of the retraction maps isomorphically onto γ_m(G), furnishing a group-homomorphic section. The restricted central extension splits, exactly asserting (4). □

**Corollary 6.** Under the original target hypotheses, put D=γ_⌈(c+2)/2⌉(G). Then

    gldim(CD)≤gldim(C^αG).

If equality holds, D is a subgroup witnessing Aljadeff's conclusion.

The inequality follows from Theorem 5 and Lemma 1. The equality condition is a sufficient condition, not a conclusion established for arbitrary α. For class 2, D=[G,G]. For class 1 the bound gives D=1 and provides no nontrivial abelian-case theorem.

## 6 Optimality of the universal lower central cutoff

**Theorem 7.** For every c≥1, set j=⌊(c+1)/2⌋, so that j+1=⌈(c+2)/2⌉. There exist a finitely generated torsion-free nilpotent group G of class exactly c and finite integral cohomological dimension, and a class α∈H²(G,C×), such that

    α|_{γ_j(G)}≠0.

Thus the cutoff of Theorem 5 cannot be reduced universally.

**Proof.** Put N=c+2 and U=UT_N(Z), the integer upper-unitriangular group. Let z=I+E_{1N}, and set G=U/⟨z⟩. The lower central series of U consists of matrices whose first i−1 superdiagonals vanish at stage γ_i. One can verify this directly: matrix multiplication gives the containment, and [I+aE_{pq},I+bE_{qr}]=I+abE_{pr} supplies all elementary matrices at the required distances. Thus U has class N−1=c+1, its last term is ⟨z⟩, and G has class c.

The quotient G is torsion-free. If a representative u is not in ⟨z⟩, let d≤N−2 be its first nonzero superdiagonal. For every positive integer k the d-th superdiagonal of u^k is k times that of u and so remains nonzero. Therefore u^k∉⟨z⟩. The usual superdiagonal filtration, refined by individual integer coordinates, is a finite central series with infinite cyclic factors for G. Repeated extensions by Z give a finite-length resolution of its trivial module, so cd_Z(G)<∞. U, and hence G, is finitely generated by the elementary matrices on the first superdiagonal.

There is a concrete cocycle. Represent each g∈G uniquely by s(g)∈U whose (1,N) entry is zero. Then

    s(g)s(h)=z^{ω(g,h)}s(gh),
    ω(g,h)=∑_{k=2}^{N−1} s(g)_{1k}s(h)_{kN}.

Because z is central, associativity gives

    ω(g,h)+ω(gh,l)=ω(h,l)+ω(g,hl).

Hence a(g,h)=2^{ω(g,h)} is a normalized C×-valued 2-cocycle.

Take x=I+E_{1,j+1} and y=I+E_{j+1,N}. Their superdiagonal distances are j and c+1−j≥j, respectively, so their images x̄,ȳ lie in γ_j(G). Their commutator in U is z, so their images commute in G. They generate a copy of Z²: the two indicated off-diagonal coordinates recover their exponents. For the cocycle above,

    a(x̄,ȳ)=2,    a(ȳ,x̄)=1.

A coboundary on an abelian group is symmetric, so its ratio on a commuting pair must be 1. The ratio here is 2, proving that α restricts nontrivially even to ⟨x̄,ȳ⟩≤γ_j(G). □

These examples establish **optimality of the automatic splitting depth**. They do not compute gldim(C^αG) and do not refute the original conjecture.

## 7 Why taking an isolator is not harmless

One also cannot silently replace the lower-central subgroup in Theorem 5 by its isolator. Let P have generators x,y,z, with z central and [x,y]=z²; use the integer-coordinate multiplication (a,b,t)(a',b',t')=(a+a',b+b',t+t'+2ab') to realize it as a torsion-free class-2 group. Let G=P×P, with central generators z_1,z_2. Then

    [G,G]=⟨z_1²,z_2²⟩,
    isol_G([G,G])=⟨z_1,z_2⟩≅Z².

There is a homomorphism φ:G→(Z/2)² sending z_1,z_2 to the two basis vectors and the four other generators to zero. The defining commutators map to zero, so φ is well-defined. Pull back the cocycle

    b((u_1,u_2),(v_1,v_2))=(−1)^{u_1v_2}.

Its restriction to [G,G] is pointwise 1, but its commutator ratio on z_1,z_2 is −1. Thus the class does not vanish on the isolator. This is compatible with Theorem 5 and rules out that tempting strengthening.

## 8 What remains unresolved

The boundary r=1 is elementary: in nontrivial torsion-free G, any nontrivial g generates H≅Z. Choose a lift of g in the central extension and take its integer powers to split the restriction; CH≅C[t,t^{-1}] has global dimension 1. Thus the genuinely unaddressed range, after also crediting the original source's r=n result, begins at 2≤r<n.

The present results do not prove that a subgroup with trivial restriction attains r in that range. They identify two concrete obligations for a further attack:

- Even for finitely generated G, show that some trivial-restriction subgroup attains the global dimension; the automatic lower-central witness need not be known to do so.
- In the infinitely generated case, handle r=d+1 by producing an infinitely generated witness, or prove that the jump cannot occur for the particular twist under study.

The unitriangular calculations and the Q example expose invalid shortcuts but leave both obligations open. The exact original target remains unsolved by this attempt.

## References and verification scope

[1] *Mini-Workshop: Arithmetik von Gruppenringen*, Oberwolfach Report 55/2007, problems section, E. Aljadeff's Problem 3, printed p. 3171, PDF p. 23. Publisher PDF: https://ems.press/content/serial-article-files/46141 . The complete PDF was authenticated, and the target page was visually inspected. Its r=n sentence is a prior-status statement without a proof reference on that page, not an imported proof dependency.

[2] B. L. Osofsky, *Upper bounds on homological dimensions*, Nagoya Mathematical Journal 32 (1968), 315–322, especially Proposition 2.1 on p. 320 and Theorem 2.3 on pp. 320–321. DOI: https://doi.org/10.1017/S002776300002674X . The complete publisher PDF was retrieved, relevant text read, and pp. 320–321 visually inspected. Proposition 2.1 refers its proof to Berstein; this note supplies its own telescope proof for the exact setting used, so that uninspected citation is not a proof dependency.

Only these two sources are cited for the problem statement and historical attribution. The proofs above are explicit and do not invoke a quantum-torus dimension theorem, a nilpotent Hirsch-length formula, or the unaudited proof of the r=n case. Finite exact computational checks supplement, and do not replace, the proofs.

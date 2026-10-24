# Independent adversarial audit of structural reductions for 21.138

Checkpoint: **2026-10-24 17:07 UTC**. Assigned reviewer did not author the structural approach. Review completion estimate: **100% of the four supplied claims**. This percentage measures this bounded audit; it is not a percentage proof of the Kourovka problem. The unrestricted problem remains unresolved here.

## Scope and verdict

Write **IF** for the property that every subgroup of infinite index is free, with no finite-generation restriction. The supplied structural deductions survive the checks below, with two necessary scope clarifications:

* The torus/Klein-bottle conclusion requires a finite-index copy of `Z^2` (or the Klein bottle group). An arbitrary torsion-free virtually surface group may instead be a negative-Euler-characteristic surface group.
* The central-extension construction is conditional. Neither the required finitely presented infinite torsion quotient nor a suitable torsion-free extension has been constructed here. The general extension mechanism has substantial prior literature under the name **Adian extension**, so no novelty is established by rediscovering it.

No claim below proves that every finitely presented IF group is free or surface.

## 1. Torsion, coherence, ends, and the flat exception

Let `G` be infinite and IF. A nontrivial finite cyclic subgroup has infinite index and is not free. Consequently `G` is torsion-free.

IF is hereditary: if `L <= H <= G` and `[H:L]` is infinite, then `[G:L]` is infinite. This remains true when `H` or `L` is infinitely generated.

If `G` is finitely presented, every finitely generated subgroup `H` is finitely presented. Indeed an infinite-index `H` is a finitely generated free group, and a finite-index `H` is finitely presented by Reidemeister--Schreier. Thus coherence is valid. Finite generation of `G` alone would not justify this finite-index step.

If a finitely generated torsion-free IF group has more than one end, Stallings' theorem gives a splitting over a finite, hence trivial, subgroup. A nontrivial free-product decomposition has infinite-index factors. Each factor is free by IF, so the whole group is free. The HNN splitting over the trivial subgroup has the form `A * Z` and gives the same conclusion; the degenerate two-ended case is torsion-free virtually cyclic and hence `Z`. Therefore a nonfree finitely generated IF group is one-ended. This invocation is for finitely generated groups only; ends of arbitrary infinitely generated free groups are not needed.

If `Z^2 <= G`, IF makes this subgroup finite index. The classification of torsion-free virtually `Z^2` groups gives `Z^2` or the Klein bottle group. Equivalently these are the two torsion-free two-dimensional crystallographic groups. In particular, a candidate outside the claimed classification contains no `Z^2`.

## 2. Finitely generated nonabelian normal free subgroup

Assume `N = F_r` is normal in `G`, where `2 <= r < infinity` and `[G:N]` is infinite.

### Centralizer calculation

Suppose `1 != c in C_G(N)`. Torsion-freeness makes `<c>` infinite cyclic. If `c^m in N`, that element centralizes `N`, and the center of the nonabelian free group `N` is trivial. Thus `<c> intersect N = 1`, and `<N,c> = N x <c>`.

For any `1 != n in N`, the subgroup `<n,c>` is `Z^2`. Its index in `N x <c>` is infinite because `<n>` has infinite index in the finite-rank nonabelian free group `N`. Its index in `G` is therefore infinite. This contradicts IF. Hence `C_G(N)=1`.

The induced map `G/N -> Out(N)` is injective: if conjugation by `g` is inner on `N`, choose `n in N` inducing the same automorphism; then `n^{-1}g in C_G(N)=1`.

### The quotient is virtually cyclic

Put `Q=G/N`. The standard virtual torsion-freeness of `Out(F_r)` implies that an infinite subgroup of `Out(F_r)` cannot be a torsion group: intersect it with a torsion-free finite-index subgroup. Thus the infinite group `Q` has an element `q` of infinite order.

Let `H` be the preimage of `<q>`. Then `H=N semidirect Z`, since a lift of `q` supplies a splitting. This `H` is finitely generated. It cannot be free. Otherwise the nontrivial finitely generated normal subgroup `N` of the finite-rank free group `H` would have infinite index, contradicting the standard normal-subgroup theorem for free groups. One direct proof of that theorem uses the normal Schreier cover: a nontrivial cyclically reduced word from `N` labels a reduced closed loop at every vertex; every vertex therefore lies in the finite core associated to a finitely generated subgroup. The cover has finitely many vertices, so the index is finite.

Since `H` is nonfree, IF forces `[G:H]` finite. Hence `[Q:<q>]` is finite: `Q` is virtually cyclic and `G` is virtually indicable. This verifies the advertised reduction. It does not independently audit the later GKL--Linton--Wilton classification chain; that is covered by the separately assigned review.

**Finite generation is essential.** An infinite-rank free normal subgroup does not yield a map to `Out(F_r)` for finite `r`, and may be normal with infinite index in a free group. Kernels of maps from closed negative-Euler-characteristic surface groups onto `Z` also give natural infinite-rank controls. The reduction must retain `r < infinity`.

Primary check for the external automorphism-group input: Culler--Vogtmann, *Moduli of graphs and automorphisms of free groups*, Invent. Math. **84** (1986), 91--119, printed p.93 explicitly records torsion-free subgroups of finite index in `Out(F_r)`: https://marc-culler.info/static/home/papers/OuterSpace.pdf . This establishes the property needed here, not a new assertion about all infinite subgroups.

## 3. Central elements and the exact conditional converse

Suppose now that `G` is an infinite finitely presented IF group outside the free/surface classification and that `1 != z in Z(G)`. Let `C=<z>`.

For every `g`, `<z,g>` is a torsion-free abelian group on at most two generators. If it were noncyclic, it would be `Z^2`, already forcing the flat surface exception. Thus `<z,g>` is cyclic. In particular every nontrivial `g` has a nonzero power in `C`.

It follows that `Q=G/C` is torsion. It is finitely presented, since it is obtained from a finite presentation of `G` by adding one relation killing `z`. It is infinite: otherwise `G` would be torsion-free virtually cyclic, and hence `Z`, contrary to the choice of `G`.

For an arbitrary infinite-index subgroup `U <= Q`, its full preimage `P` has infinite index in `G`. IF makes `P` free, while its center contains the nontrivial element `z`. A free group of any rank with nontrivial center is infinite cyclic. The nontrivial subgroup `C <= P = Z` has finite index in `P`; hence `U=P/C` is finite cyclic. This proof includes infinitely generated `U`, rather than merely checking finitely generated subgroups.

### Converse with all subgroup quantifiers checked

Assume, conditionally, that `Q` is an infinite finitely presented torsion group in which every infinite-index subgroup is finite cyclic, and that an extension

`1 -> C = Z -> E -> Q -> 1`

is central and torsion-free. Let `1 != H <= E` have infinite index. Choose `1 != h in H`. Since its image in `Q` has finite order, some positive power `h^m` lies in `C`; torsion-freeness makes this power nontrivial. Hence `H intersect C != 1`, and

`[HC:H] = [C:H intersect C] < infinity`.

As `[E:H]` is infinite, `[E:HC]` is infinite as well. Thus `U=HC/C` is an infinite-index subgroup of `Q`, so is finite cyclic. Consequently `HC` is torsion-free virtually cyclic, and hence infinite cyclic. Therefore `H` is cyclic. The trivial subgroup is free also. This proves full IF for `E`, including all infinitely generated subgroups; indeed all its infinite-index subgroups would be cyclic.

The finite-presentation claim is checkable directly. Choose a finite presentation `Q=<x_1,...,x_d | R_1,...,R_s>` and lifts `y_i` in `E`. The elements `y_i,z` generate `E`, and each lifted relator satisfies `R_j(y)=z^{k_j}` for some integer `k_j`. The finite presentation

`<y_1,...,y_d,z | [z,y_i]=1, R_j(y)=z^{k_j}>`

maps onto `E`. Any word in its kernel is trivial in `Q`, so is a finite product of conjugates of lifted relators and reduces to `z^k`. Since `z` has infinite order in `E`, `k=0`. The map is injective.

Finally `E` is neither free nor a closed aspherical surface group. It has nontrivial center and is noncyclic, which excludes all free groups and all negative-Euler-characteristic closed surface groups. Neither the torus nor the Klein bottle admits an infinite torsion quotient by an infinite cyclic central subgroup: in either case such a quotient still has an infinite-order element. Thus a concrete pair `(Q,E)` with these properties would be a counterexample. No such pair has been supplied, so this remains a precise conditional construction, not a counterexample.

### Priority and obstruction

The broad central-extension mechanism is established prior mathematics. Gardam--Kielak--Logan, *Algebraically hyperbolic groups*, https://arxiv.org/html/2112.01331v3 (28 April 2025), Definition 2.8 and Lemma 2.9 discuss finitely generated torsion-free cyclic extensions of infinite torsion groups as **Adian extensions**. Their Section 5 also rules such subgroups out in torsion-free residually finite groups and records stronger quotient constraints. These facts were checked in the primary paper and must be credited when interpreting this route.

In particular, neither finite presentation of `G` nor the IF condition has been shown here to exclude the required torsion quotient. Assuming that exclusion, or assuming that arbitrary finitely presented IF groups have cohomological dimension at most two, would transfer the central difficulty to an unsupported assertion.

## 4. Rank-one normal subgroup and inversion control

For a normal infinite cyclic subgroup `N=<z>`, the conjugation map `G -> Aut(N)={+1,-1}` has kernel of index at most two, on which `N` is central. IF passes to this kernel, so the advertised central-case reduction is valid. If the kernel is already free or surface, the standard torsion-free finite-extension conclusions supply the corresponding classification for `G`.

There is a sharper check. Suppose `gzg^{-1}=z^{-1}`. The homomorphism from the Klein bottle presentation `<z,g | gzg^{-1}=z^{-1}>` into `G` is injective. If `z^m g^n=1`, odd `n` contradicts the induced conjugation on `z`; if `n` is even, conjugating the equation by `g` gives `z^{-m}g^n=1`, so `z^{2m}=1`, whence `m=0` and then `n=0` by torsion-freeness. The normal forms are therefore distinct. IF makes this embedded nonfree Klein bottle group finite index. Then `G` is torsion-free virtually `Z^2`, hence torus or Klein; the inversion excludes the torus. Thus a genuinely unclassified IF group with a cyclic normal subgroup already has that subgroup central.

The finite-extension surface input is explicitly recorded in Gardam--Kielak--Logan, https://arxiv.org/html/2202.11093v2 , Theorem 3.4, with the Nielsen-realization and Eckmann--Müller references. It allows negative-Euler-characteristic surfaces too; it must not be compressed into a torus/Klein-only assertion without the flat hypothesis.

## Boundary controls and final audit status

* `Z^2` and the Klein bottle satisfy IF and are permitted surface groups. They are necessary exceptions to arguments prohibiting central elements, commuting pairs, or cyclic normal subgroups.
* Closed nonorientable surfaces of negative Euler characteristic are permitted too; nonorientability alone is not an obstruction.
* Infinite cyclic groups are in the free conclusion. Rank-zero or rank-one free kernels must be handled separately from the nonabelian centralizer argument.
* `BS(1,m)`, `|m|>=2`, fails full IF because its normal `Z[1/m]` subgroup is infinite-index, noncyclic, and not free. Tests restricted to finitely generated subgroups of that kernel miss the obstruction.
* No appeal in the accepted deductions assumes the unrestricted conclusion, virtual indicability, cubulation, finite cohomological dimension, or a surface subgroup for every IF group.

**Audit outcome:** the four supplied structural claims are valid with the stated scope corrections and the documented conditional/existence gap. They support restricted reductions and rejection criteria. They do not establish `solved_verified`, originality, or publication eligibility for 21.138.

## Addendum: power balance and the cyclic-CSA/central-Adian dichotomy

Fresh assigned audit, **2026-10-24 17:12 UTC**. The author supplied additional deductions after the first report. The following review is independent of authorship. Completion estimate: **100% of these added deductions**; the original problem remains unresolved.

### A. Direct power-balance argument

**Accepted, without a finite-generation assumption on the ambient group.** Let `G` be infinite and IF. Suppose

`t^{-1} a^m t = a^n`, with `a != 1`, `m,n != 0`, and `|m| != |n|`.

Torsion-freeness makes `a` infinite order. The commensurator `Comm_G(<a>)` is a subgroup. For an element `h` in it, define the modular character by

`delta(h)=v/u` whenever `h^{-1} a^u h=a^v`, with `u,v != 0`.

The ratio is well-defined: two such equations, raised to their respective common multiples, give equality of the corresponding powers of `a`, and thus equal ratios. Applying the equations successively proves that `delta` is a multiplicative homomorphism to `Q^times`; the order convention for conjugation makes no difference because the codomain is abelian.

Set `H=<a,t>`. Both generators commensurate `<a>`. The image of `delta|H` is the infinite cyclic group generated by `n/m`, since `delta(a)=1` and `|n/m| != 1`. Therefore its kernel `K` has infinite index in `H`, and hence in `G`. Full IF makes `K` a free group, possibly of infinite rank. It contains `a` and all its `H`-conjugates.

Each such conjugate is commensurable with `a`. In a free group, two nontrivial elements with a common nontrivial power belong to the same maximal cyclic subgroup, namely `C_K(a)`. Consequently the normal closure `N=<<a>>_H`, generated by all those conjugates, is a nontrivial subgroup of the cyclic group `C_K(a)`. Thus `N` is cyclic and normal in `H`. Conjugation by `t` acts on `N` as `+1` or `-1`. Since `a` is a nonzero power of a generator of `N`, the displayed relation forces `n=m` or `n=-m`, a contradiction.

This proof does not need to prove `K=N`, although that assertion is also true: `H/N` is cyclic on the image of `t`, and the induced modular character maps that generator to an infinite-order generator, so is injective. Nor does the proof use the separately reviewed virtually-indicable IF classification. Retaining that theorem as a dependency would be unnecessary.

If one of `m,n` is zero, torsion-freeness forces the other to be zero, so it gives no exception. The equal-absolute-value case is deliberately retained: the Klein bottle realizes inversion. Thus **every infinite IF group is power-balanced**, in precisely the absolute-value sense used in the definition of weak algebraic hyperbolicity.

### B. Every abelian subgroup of a hypothetical counterexample is cyclic

Let `G` now be a hypothetical finitely presented counterexample, as in the main review. If an abelian subgroup `B` were noncyclic, it would be nonfree and hence would have finite index by IF. Finite generation of `G` then makes `B` finitely generated. A finitely generated torsion-free noncyclic abelian group contains `Z^2`, contradicting the exclusion of the flat surface case. Therefore **every abelian subgroup is cyclic**, including abelian subgroups initially presented without a finite-generation assumption.

### C. The commutative-transitive branch is cyclic-CSA

Assume commutativity is transitive on nonidentity elements. For any `a != 1`, its centralizer is abelian by that property, and hence cyclic by B. It is the maximal cyclic subgroup containing `a`: any cyclic overgroup of that centralizer would still centralize `a`.

Unique roots also follow. If `x^r=y^r != 1`, the elements `x,y` lie in the abelian centralizer of the common power, and torsion-freeness yields `x=y`.

Let `A=<a>` be maximal cyclic and let `g` commensurate `A`. There are nonzero `m,n` with `g^{-1}a^m g=a^n`. By A, `n=+m` or `n=-m`. Unique roots give `g^{-1}ag=a` or `g^{-1}ag=a^{-1}`. The first alternative puts `g` in `C_G(a)=A`. The second produces an embedded Klein bottle group by the rank-one argument above, and hence a `Z^2`, impossible. Thus `Comm_G(A)=A`.

For infinite cyclic groups, nontrivial intersection with a conjugate is equivalent to commensurability. Hence each maximal cyclic subgroup is malnormal. All maximal abelian subgroups are cyclic and malnormal: this is the **cyclic-CSA** branch. Nothing here makes an arbitrary cyclic-CSA group hyperbolic, special, or a surface group.

### D. The non-commutative-transitive branch is a central Adian extension

If commutativity is not transitive, choose nontrivial `x,y,z` with `[x,z]=[y,z]=1` and `[x,y] != 1`. Then `K=<x,y,z>` is nonabelian with a nontrivial central element `z`, so it is nonfree and therefore has finite index in `G`. For every `k in K`, the group `<k,z>` is cyclic, since it is abelian and `G` contains no `Z^2`. Thus `K/<z>` is torsion. This quotient is infinite: otherwise `K` would be torsion-free virtually cyclic, hence cyclic, contrary to `[x,y] != 1`.

For each nontrivial `g in G`, some positive power belongs to `K` because `[G:K]` is finite, even though `K` need not be normal. A further positive power is a nonzero power of `z`. Choose finite nontrivial generators `g_1,...,g_d` of `G` and equations `g_i^{r_i}=z^{s_i}`, where `r_i>0` and `s_i != 0`. Each `g_i` commutes with `z^{s_i}`. For a common positive multiple `L` of the `|s_i|`, all generators commute with `z^L`; hence `C=<z^L>` is central in `G`.

Every element of `G` has a power in `C`, so `Q=G/C` is torsion. It is finitely presented by adding the single relation `z^L=1` to a finite presentation of `G`. It is infinite, since otherwise `G` would be virtually cyclic and hence cyclic. Finally every infinite-index subgroup of `Q` is finite cyclic by the preimage argument in Section 3. This verifies the author's upgrade from a finite-index Adian subgroup to a **central Adian description of `G` itself**. The common-power and centralization arguments require finite generation only when choosing a common `L` for the finite generating set.

Therefore the sharpened structural alternative survives review: a hypothetical counterexample is cyclic-CSA, or it is a torsion-free central extension of an infinite finitely presented torsion group with all infinite-index subgroups finite cyclic. Neither branch has been excluded, and the latter quotient/extension has not been produced.

### E. Source and boundary checks

The author's initial formulation through GKL's weak-AH/Adian theorem is consistent with the primary definitions and Theorem 5.2 of https://arxiv.org/html/2112.01331v3 . Sections A--D above give the elementary mechanisms and remove the unnecessary virtually-indicable dependency. The established AH and Adian literature must still be credited; this review does not establish priority for the IF specialization.

The corrected Klein bottle sentence in Proposition 5 of `../approach_structure.md` is valid. In the convention `<a,b | a^{-1}ba=b^{-1}>`, the center is `<a^2>`. Quotienting by `<a^{2k}>`, `k != 0`, leaves `b` of infinite order. One exact certificate is the quotient map to the infinite dihedral group sending `a` to a reflection and `b` to an infinite translation: both the Klein relation and `a^{2k}=1` hold. Thus the quotient cannot be torsion. The earlier, now withdrawn assertion that the central generator has zero image in the free part of the Klein bottle abelianization must not be used; its image is nonzero there.

**Addendum verdict:** accepted as a structural reduction, with no remaining substantive objection found in the stated deductions. This is not a complete solution, a new counterexample, formal verification, human peer review, or an originality certificate.

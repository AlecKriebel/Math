# Independent reconstruction, before candidate exposure

Prepared 2026-10-03 UTC. The claim under audit is that for every virtually type-FP group G, the direct sum of all H^q(G;ZG) is finitely generated as a right ZG-module. Here FP means a finite-length resolution of the trivial left module Z by finitely generated projective left ZG-modules. Coefficients use left multiplication; the commuting right multiplication gives the right module action. No candidate proof, code, old verdict, root report, or sibling artifact was read in preparing this document.

## 1. Finite index: the right action, not just abelian groups

Let H<G have finite index, R=ZG, S=ZH, and let pi:R->S discard coefficients outside H. The coinduced module is Hom_S(R,S), where R is a left S-module, with left G-action (a.f)(x)=f(xa) and commuting right H-action (f.h)(x)=f(x)h. Define

    Theta(r)(x)=pi(xr).

Theta is left G-equivariant and right H-equivariant: Theta(ar)(x)=Theta(r)(xa), and pi(xrh)=pi(xr)h for h in H. Choose left H-coset representatives t, so every S-linear f is determined by f(t). If f(t)=sum_h c(t,h)h, its inverse is r=sum_(t,h) c(t,h)t^(-1)h. This is a finite sum because H has finite index. The same construction fails for infinite index: arbitrary coinduced functions need not have finite support.

Shapiro's lemma, applied to this explicitly identified coinduced coefficient module, gives

    Res^G_H H^q(G;ZG) ~= H^q(H;ZH)

as RIGHT S-modules. Right-H equivariance follows already at the coefficient map and the natural Hom adjunction, rather than from an arbitrary abelian-group isomorphism.

For any right R-module M, M is finitely generated over R iff its restriction to S is finitely generated over S: the reverse direction uses the same S-generators; in the forward direction multiply a finite R-generating set by a finite right S-basis of R. Therefore finite generation of the total cohomology module is invariant under finite-index passage. No FP assumption is needed for this equivalence itself. If H is type FP, its cohomology vanishes above its finite resolution length; hence the same is true of G with these coefficients. This reduces the virtual question to the type-FP question.

Distinct induced module: if H is FP-infinity (in particular finite-length FP), Hom from its fg projective resolution commutes with extension from S to R, and R is free as a LEFT S-module. Then

    H^q(H;ZG) ~= H^q(H;ZH) tensor_S R

as right R-modules. This is NOT H^q(G;ZG). Example G=Z, H=2Z: H^1(G;ZG)=Z, while the induced right-G module H^1(H;ZH) tensor_ZH ZG is Z[G/H], of abelian rank two. The finite-index Shapiro isomorphism above instead identifies the restriction of Z with the subgroup module Z.

## 2. The finite-kernel obstruction and realizability gap

Dualizing a finite fg projective resolution P_* of Z gives a bounded complex of fg projective RIGHT modules P^*=Hom_R(P_*,R). Its top cohomology is a quotient of the fg last cochain module, so is fg. At an intermediate degree, H^q=ker(d^q)/im(d^(q-1)); the kernel need not be fg over a noncoherent ring. Noetherianity would suffice, but it is an extra ring hypothesis.

A precise logical falsifier for the inference "bounded fg projective complex => fg cohomology" is the square-zero ring A=Z direct-sum V, where V=direct-sum_(j>=0) Z e_j and V*V=0. The two-term finite free complex A --e_0--> A has kernel V. A acts on V through the augmentation A->Z, so a finite set of elements generates at most a finite-rank Z-subgroup. Consequently V is not fg over A. Its cokernel A/(e_0) is fg (cyclic). This is not a group-ring counterexample to the workshop question: A is not identified as a group ring, and the dual primal complex does not resolve the trivial augmentation module Z. Its augmentation kernel V is itself not fg. Realizing an analogous bad kernel inside the dual of an ACTUAL augmentation resolution remains the central gap.

For a right R-module M and a quotient ring S, cohomology need not commute with tensor unless the needed flatness/Tor conditions hold. Exact model: R=Z[a,a^-1], C=(R --(a-1)--> R). C has H^0=0 and H^1=Z. Under the augmentation R->Z, C tensor_R Z has zero differential and H^0=Z, H^1=Z. The new lower class is Tor_1^R(Z,Z)=Z, computed from the same two-term resolution. Thus killing a subgroup in a coefficient quotient cannot be called a flat specialization merely because extension ZH->ZG was free.

## 3. Ascending HNN extensions: what height proves

Let H be type FP, let phi:H->H be injective, and let

    G=<H,t | t^-1 h t = phi(h) for all h in H>.

The normal-form theorem embeds H. The Bass-Serre tree has one orbit each of vertices and edges, both stabilizers isomorphic to H; one edge inclusion is the identity and the other is phi. Inducing the finite projective resolution of H and taking the tree mapping cone gives a bounded fg projective G-resolution of Z, so G is type FP.

The height homomorphism G->Z, h|->0 and t|->1, decomposes ZG as a direct sum of homogeneous left ZH-submodules R_k. Each cochain of a fg projective H-resolution has finite height support, and its differential preserves height; hence the cohomology A_q=H^q(H;ZG) also decomposes as direct sum of its height pieces. The Bass-Serre cohomology sequence has right-ZG-linear maps

    ... -> H^q(G;ZG) -> A_q --(1-T_q)--> A_q -> H^(q+1)(G;ZG) -> ...

where the identity edge inclusion contributes the identity and the other, with the stable-letter coefficient transport, contributes a map T_q shifting height by exactly one (the sign of the shift depends on the chosen tree convention). Chain maps lifting phi have coefficients in ZH, so do not add other height shifts. The coefficient transport is left multiplication by a stable letter; it commutes with the RIGHT regular action. In particular this is a right-module LES, not an assertion about multiplication on the right by t.

The map 1-T_q is injective: if a nonzero vector has finite height support and T shifts height upward, its minimum-height component survives in (1-T)a; if T shifts downward use the maximum-height component. This works even when T_q is neither injective nor surjective on its homogeneous pieces.

Consequently

    H^(q+1)(G;ZG) ~= coker(1-T_q:A_q->A_q).

Since H is FP, A_q ~= H^q(H;ZH) tensor_ZH ZG as right ZG-modules. If the total base module H^*(H;ZH) is fg, every A_q is fg, and the cokernel formula proves the ascending HNN extension's total module is fg. There are only finitely many degrees. This is a valid closure theorem CONDITIONAL on the base property, not a solution for arbitrary FP bases. The case H=1 gives G=Z with cyclic H^1; H=Z and phi=id gives Z^2 with cyclic H^2. More generally abelian bases have the usual Koszul resolution and are covered.

The height argument cannot be transferred to periodic height, infinite product cochains, or finite cutoffs without checking the support condition. In Z[t,t^-1], 1-t is injective by lowest degree and has cokernel Z, with quotient map evaluation t=1. In Z[C_m], 1-t has nonzero kernel generated by the norm 1+...+t^(m-1). On a finite height window with the upward shift artificially discarded at the top, 1-T is invertible, so its cokernel is zero. That finite model misses the actual infinite Laurent cokernel. The exact computations here test these failure mechanisms, and are not extrapolated to a universal group-ring computation.

## 4. Free products and nonsplit extensions

Let G=A*B, where A and B are type FP and already have fg total group-ring cohomology. The one-edge Bass-Serre tree has trivial edge stabilizer. Its LES with R=ZG is

    0 -> H^0(G;R) -> R^A direct-sum R^B -> R
      -> H^1(G;R) -> H^1(A;R) direct-sum H^1(B;R) -> 0,

and for q>=2, H^q(G;R) ~= H^q(A;R) direct-sum H^q(B;R). Each subgroup coefficient module is induced from its group-ring cohomology because the factors are FP. H^1(G;R) is an extension of the cokernel of R^A+R^B->R (a quotient of cyclic R) by a fg module. An extension of two fg right modules is fg, by choosing lifts of generators. H^0(G;R)=0 when G is infinite, since a nonzero finite-support element cannot be fixed by every left translation; when G=1 it is cyclic Z. No splitting assumption is needed. Trivial factors are harmless; in this FP convention nontrivial finite factors are not themselves type FP, but their virtual extensions can be handled separately. Free products give more positive cases conditional on the factors, without resolving arbitrary FP groups.

## 5. Primary-source checks and their limits

EMS OWR43/2006 physical pages 10-12, printed2588-2590, establish the question and Coxeter result. EMS metadata article1381 records workshop/submission17 September2006, journalvolume3(2006), and publication30 September2007. The source should not be relabelled as a 2007 workshop.

The AGT6(2006),1289-1318 paper starts with left coefficient and inherited right-action conventions. Sections3-5 give an abelian splitting using the hat-A^T pieces, but those pieces are not right W-submodules. Sections4-5 give a finite filtration by right W-modules with graded pieces H^*(K,K^(S-T)) tensor (A^T/A^>T). Each quotient is cyclic as a right module, K finite, and extensions of fg modules give the Coxeter conclusion. Example5.2 disproves an equivariant splitting in general. The filtration proof is sufficient; dropping the filtration is not justified.

Davis pdgroup.pdf printedp4 (physical4) and IGAP physical233, printed229, define FP with finite length. The IGAP printed223 locator is incorrect for this definition. The printed229 locator is additive bibliographic correction, not a new mathematical hypothesis.

Davis-Okun2012 author copy, /papers/do3final-okun.pdf, Theorem4.5 requires every graph-product factor to be infinite; §2 Lemma2.2 distinguishes zero maps to each strict subspace (Z0) from the stronger map to their union (Z), and only (Z) gives collapse. The resulting formulas compute associated graded RIGHT modules. One vertex gives exactly the original factor's cohomology: the only contributing term has J={s}, K_J=point, boundary empty. Thus the graph-product formula cannot prove the arbitrary-group question. The introduction's broad sentence asserting fg right-hand sides cannot be applied to arbitrary factors without separately establishing finite generation of those factor-dependent coefficient modules. Likewise induced coefficient identities need an appropriate finiteness hypothesis (satisfied in the FP audit), and the paper does not license arbitrary Hom/direct-sum interchange by fiat. No present-day literature-completeness claim follows from these source checks.

## Status

Strongest verified result: the finite-index equivalence, conditional closure for ascending HNN extensions and free products, and the exact obstruction separating finite cochain matrices from fg middle cohomology. The universal virtually-FP question remains unproved here. Estimated completion: 55% of this scoped source/HNN audit before candidate comparison; 0% certified resolution of the universal question. No novelty or acceptance claim.

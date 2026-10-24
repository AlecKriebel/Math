# Cofinal free retracts and the failure of qualitative virtual quotient tests

Research checkpoint: 2026-10-24 UTC. This is a rigorously proved filter on candidate methods for Kourovka 21.128. It supplies no positive or negative answer and makes no novelty claim. Write P_T for the pure spherical Artin group and Q_T=P_T/Z(P_T), for T=F4,H4.

## 1. The starting epimorphism is elementary

Each diagram contains an A2 edge. The corresponding three reflecting hyperplanes form a rank-two subarrangement B of the reflection arrangement A_T. After a linear change of coordinates,

M(B) is isomorphic to C* × (C minus {0,1}) × C².

The inclusion M(A_T) → M(B) is surjective on fundamental groups: a smooth based loop can be perturbed, relative to the basepoint, to be transverse to the finitely many extra complex hyperplanes. A one-dimensional loop transverse to real-codimension-two submanifolds avoids them. The perturbation is a homotopy in M(B). The usual pure Artin group identification therefore gives P_T → Z × F2 → F2. The image of the center under an epimorphism is central in its target. Since the center of F2 is trivial, this descends to an epimorphism

π: Q_T → F2=⟨a,b⟩.

The pure/central arrangement identification and the passage between the original Artin commensurability problem and the Q_T comparison are established in [Cumplido–Paris, Proposition 3.1 and Corollary 3.2](https://doi.org/10.4171/RMI/1282). No arrangement-deletion map is asserted injective.

## 2. Explicit normal subgroups of every index

For each m≥1 let K_m be the kernel of F2 → C_m sending a to 1 and b to 0, and let V_m=π⁻¹(K_m). Then V_m is normal in Q_T and has index m. The m-sheeted cover of the two-petal rose has vertices 0,…,m−1, an a-edge j→j+1 modulo m and a b-loop at each vertex. Its spanning tree consists of the a-edges 0→1→…→m−1. Contracting this tree gives the following free basis of K_m:

u=a^m; v_j=a^j b a^(−j), 0≤j<m.

Thus K_m is free of rank m+1. The restriction V_m → K_m is an epimorphism. An epimorphism onto a free group splits: choose a preimage of each free generator and use the universal property. Hence K_m, not just a quotient isomorphic to it, is a retract of V_m.

For every d-generated group L and every integer m≥max(1,d−1), mapping d basis elements to a generating list of L and the others to the identity yields V_m → L. The trivial group is included by taking d=0. Normality here is in Q_T. There is no assertion that V_m is normal in the full Artin group or another finite overgroup.

## 3. The construction survives inside every finite-index subgroup

Let H≤Q_T have finite index. Then L₀=π(H) has finite index e in F2, since Q_T/H surjects as a coset set onto F2/L₀. Nielsen–Schreier gives rank(L₀)=e+1≥2. For any m≥1 choose a cyclic epimorphism L₀→C_m and write K for its kernel. Then

W=(π|_H)⁻¹(K) is normal of index m in H,

and W retracts onto K, a free group of rank 1+m e. Consequently every H has further finite-index subgroups with free retracts of unbounded rank. There is no claim that every prescribed rank appears by this particular cyclic construction when e>1; unbounded rank suffices to obtain every finitely generated quotient.

The property also passes from Q_T to P_T=Q_T×Z and then virtually to the original Artin group. For an arbitrary finite-index subgroup H of the original Artin group, intersect H with P_T and project to Q_T; the image has finite index. Pulling back the construction gives finite-index subgroups of H surjecting onto arbitrarily large free groups. Normality in H is not claimed after this intersection step.

## 4. Consequences for proposed virtual invariants

**All finitely generated quotient isomorphism types occur virtually.** For either group, and inside every finite-index subgroup, some further finite-index subgroup surjects onto any prescribed finitely generated group. In particular the union of finite quotient isomorphism types over all finite-index subgroups is the set of all finite groups. Merely finding a finite simple quotient, a finite p-group, an arithmetic image, or a particular finitely generated linear image somewhere virtually cannot distinguish F4 from H4.

This does not identify their profinite completions or open profinite subgroups. It does not equate the number, indices, or kernels of quotient maps. It makes no claim about faithful representations, subgroup embeddings of an arbitrary quotient L, or kernels with a prescribed finiteness property. Those stronger requirements can carry information that quotient existence loses.

**Unbounded primitive isotropic H¹ subspaces.** A retraction W→F_r induces a split injection H¹(F_r;Z)→H¹(W;Z), whose image has rank r. All products of two classes in this image vanish because H²(F_r;Z)=0. The same holds over any field. Thus the supremum, over finite-index subgroups of either target, of the dimension of a totally cup-isotropic H¹ subspace is infinite. This is a stronger statement than just infinite virtual first Betti number, but still does not separate the pair.

**Unbounded rank-one jump-locus dimensions.** Let T(W)=Hom(W,C*) and define V¹_k(W) by dim H¹(W;C_χ)≥k. The epimorphism W→F_r embeds the r-dimensional character torus T(F_r) into T(W) as a closed subtorus. For each character χ of F_r, inflation is injective on H¹: if an inflated cocycle is a coboundary, surjectivity makes the original cocycle a coboundary. The rose cochain complex C→C^r has rank zero at the trivial character and rank one otherwise, so H¹(F_r;C_χ) has dimension r at 1 and r−1 elsewhere. The entire r-dimensional subtorus is therefore contained in V¹_(r−1)(W), for r≥2. Both virtual supports have unbounded component dimension and unbounded depth.

No statement is made here that the degree-one resonance variety of an arbitrary cover equals its characteristic variety's tangent cone. That equality needs extra formality hypotheses. The cup-isotropic and rank-one local-system arguments above are separate and require no such hypothesis. Different finite arrangement pencil multiplicities do not by themselves yield a bounded dimension of all virtual cup-isotropic spaces or all virtual jump-locus components.

**Nilpotent and pro-p quotient ranks are unbounded.** For every r and every fixed nilpotence class c, an appropriate W maps onto the free nilpotent group F_r/γ_(c+1)(F_r). Their abelianization ranks already tend to infinity. For every prime p, the map W→F_r induces an epimorphism of pro-p completions onto the free pro-p group of rank r. Indeed the image of the compact pro-p completion contains the dense image of F_r, so it is all of its pro-p completion. Hence merely admitting high-rank free nilpotent or free pro-p quotients somewhere virtually gives the same answer for both targets.

Again, this does not classify the full pro-p completion, nor equate rational Malcev completions of finite-index subgroups. The latter are not generally invariant under finite index: F2 has an index-two subgroup F3, with different first rational Betti numbers and different rational abelianizations of their Malcev completions.

## 5. Exact remaining gap

A negative solution still needs a structure or numerical invariant that is preserved by every possible isomorphism between finite-index subgroups, and a proof that this invariant differs. This filter rules out several qualitative existence tests. It neither constructs a common finite-index subgroup nor constrains the full cohomology ring, the commensurator, or open profinite subgroup isomorphisms sufficiently to exclude one.

The accompanying standard-library program checks the explicit cyclic Schreier formulas on exhaustive bounded free words and checks covering ranks. The proof for all m and all words is the spanning-tree construction above; finite tests are reproducibility evidence rather than a replacement for that proof.

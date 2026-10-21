# The flex-point cover: an eight-domain section construction

**Problem:** 30003711 / OWR-15987-022.  
**Author claim:** complete resolution for ordinary Schwarz genus, pending independent review.  
**Date:** 2026-10-06. No novelty or priority claim is made.

## 1. Statement and conventions

Let X be the space of smooth homogeneous complex cubics in three variables modulo multiplication by a nonzero scalar. Thus X is the discriminant complement in CP^9, not the quotient by projective coordinate changes. Let Y consist of pairs (F,p), where p is one of the nine flexes of F. We use the ordinary, unnormalized Schwarz genus: the least number of open sets covering X on each of which Y → X has a continuous section. A section need choose only one flex. The open sets need not be connected, and need not trivialize all nine sheets. With the normalized sectional-category convention the answer below is one smaller.

**Theorem.** The ordinary Schwarz genus of Y → X is 8. Equivalently, its normalized sectional category is 7.

The lower bound 8 is Chen–Wan, Theorem 1.2 / Theorem 4.1 [CW]. This note proves the matching upper bound. It does not compute the minimum number of domains on which every sheet can be simultaneously labeled, and makes no algorithmic branching-complexity equality claim.

The original workshop wording [OWR, Question 5, pp. 114–115] describes trivial restrictions on connected open sets. Read literally, that wording asks a stronger invariant for a nonregular cover. The theorem here concerns the standard section-based genus explicitly defined in [CW], which is the invariant in the stated 8-versus-9 problem.

## 2. Classical input and the homogeneous cover

Use the following classical Hesse data [AD, §2 and Proposition 4.1]. Write ω = exp(2πi/3), P = PGL_3(C), and G = PU(3). The smooth members of the pencil

F_λ = x^3 + y^3 + z^3 − 3λxyz,   λ ∈ T := C \ {1,ω,ω²},

have the same nine flexes, denoted S. Its projective symmetry group Γ lies in G and acts on S as

Γ ≅ F_3² ⋊ SL_2(F_3).

For p₀ = [1:−1:0], the stabilizer Γ₀ is SL_2(F_3). The translation subgroup K is generated projectively by

A = [[0,0,1],[1,0,0],[0,1,0]],    B = diag(1,ω,ω²).

The element C = diag(1,1,ω) belongs to Γ₀. These data identify S with K via k ↦ kp₀; this is the affine action in the displayed semidirect product.

The Hesse parameterization gives X ≅ (P × T)/Γ and Y ≅ (P × T)/Γ₀ [CW, §3]. In these associated quotients, the action on the first coordinate is right multiplication, with the matching inverse action on the second. Consequently the cover Y → X is pulled back from P/Γ₀ → P/Γ. Polar retraction r:P → G is right-G-equivariant. For a representative matrix M, its unitary factor is M(M* M)^(−1/2); changing M by a nonzero scalar changes this factor only by a unit scalar, so it defines r on P. Also r(MU)=r(M)U for unitary U. Hence Y → X is pulled back from

p : E := G/Γ₀ → M := G/Γ

along [(g,λ)] ↦ r(g)Γ. Explicitly the map on total spaces sends [(g,λ)] to the point r(g)Γ₀ over that base point; on every fiber it is a bijection of nine points. It therefore suffices to prove g(p) ≤ 8. The manifold M is compact and has real dimension 8.

## 3. The Hessian spectral lemma

**Lemma 1.** If γ ∈ Γ fixes no point of S, then every matrix representing γ has three distinct eigenvalues.

**Proof.** In the affine description write γ(v)=Lv+t, with L ∈ SL_2(F_3). If L−I is invertible, then v=(I−L)^(−1)t is a fixed point. Thus a fixed-point-free γ has L−I singular. Since det L=1, both eigenvalues of L are then 1, and (L−I)²=0.

If L=I, γ is a nonidentity translation A^a B^b. For a=0, b≠0, its three diagonal eigenvalues 1,ω^b,ω^(2b) are distinct. For a≠0 its matrix is a weighted permutation matrix whose underlying permutation is a 3-cycle. For any such matrix, with nonzero weights d₁,d₂,d₃ around the cycle, the characteristic polynomial is z³−d₁d₂d₃. It has three distinct roots over C.

Suppose L≠I. Every nontrivial unipotent in SL_2(F_3) is conjugate within SL_2(F_3) to one of the two matrices

[[1,0],[1,1]] and [[1,0],[2,1]].

Indeed, choose a nonzero fixed vector u and then v so that (v,u) is a determinant-one basis. The map L−I sends v to cu for some c∈F_3^×={1,2} and sends u to zero. In this basis L has the displayed form.

Direct multiplication gives C A C^(−1)=AB and C B C^(−1)=B in PGL_3(C). Since C fixes p₀, its linear action on the translation coordinates (a,b) is (a,b) ↦ (a,b+a). Therefore, by conjugating γ with an element of Γ₀, we can arrange that

γ = A^a B^b C^c,   c∈{1,2}.

Projective conjugation preserves both the existence of a fixed flex and eigenvalue multiplicities. If a=0, the affine action is

(x,y) ↦ (x, y+cx+b).

It fixes the three points with x=−b/c. Hence a fixed-point-free γ must have a≠0. But then A^a B^b C^c is again a weighted 3-cycle, and the same characteristic-polynomial calculation gives three distinct eigenvalues. This proves the lemma. ∎

**Corollary 2.** Put H={diag(1,z,z): z∈U(1)}⊂G. For every g∈G, the finite cyclic group J_g := Γ ∩ g^(−1)Hg has a common fixed point in S.

**Proof.** J_g is conjugate to a finite subgroup of the circle H, so it is cyclic. If it is trivial, any point works. Otherwise choose a generator γ. It is conjugate in G to diag(1,z,z) with z≠1, and therefore has a repeated eigenvalue. Lemma 1 implies that γ fixes a point of S. That point is fixed by the whole cyclic group it generates. ∎

This is a common-fixed-point statement for the entire isotropy subgroup, not merely a separate fixed point for each of its elements. Cyclicity is essential to that implication.

## 4. Local sections around circle orbits

The circle H acts on M=G/Γ and E=G/Γ₀ by left multiplication; p is H-equivariant. Its stabilizer at m=gΓ is

L_m = H ∩ gΓg^(−1).

Conjugation by g identifies L_m with J_g. The fiber of p at m identifies with S, and under this identification its L_m-action is the J_g-action. By Corollary 2 it has a fixed point e∈p^(−1)(m).

The formula

s_m(hm) = he

defines a continuous section over the orbit O_m=Hm. It is well defined: any two h's representing the same point of O_m differ by an element of L_m, which fixes e. The formula covers every point of the orbit and p(s_m(hm))=hm.

Choose an H-invariant Riemannian metric on M. Each orbit is a compact embedded circle, since its stabilizer is finite. The equivariant tubular-neighborhood theorem supplies an H-invariant open neighborhood W_m of O_m and a deformation retraction onto O_m by radial contraction in the normal bundle. The section s_m extends to W_m by the homotopy lifting property of the covering p: lift the homotopy from the retraction to the identity, starting at s_m composed with the retraction. At its final time the lift is a section over W_m.

Let q:M → B:=H\M be the orbit projection. Since W_m is H-invariant, U_m=q(W_m) is open and q^(−1)(U_m)=W_m. Thus B has an open cover whose full inverse images under q admit sections of p.

## 5. Eight colors suffice

We provide the dimension-to-genus argument to avoid assuming that a branched quotient of E → M is itself a covering.

First, B is a compact metrizable space of covering dimension at most 7. One way to see this is to write B=(H\G)/Γ. The left homogeneous space H\G is a compact smooth 7-manifold, and Γ acts smoothly on it by right multiplication. A finite-group equivariant triangulation exists [I]. After subdivision the quotient is a polyhedron of dimension at most 7. In particular every finite open cover of B has a finite open refinement of order at most 8.

Choose a finite subcover {U_i} of the orbit neighborhoods constructed above, and an open refinement {V_j} of order at most 8. For each j choose i(j) with V_j⊂U_i(j). A subordinate partition of unity defines a map f:B → |N| to the nerve N of {V_j}. The order bound gives dim N≤7. Let sd N be the barycentric subdivision. Its vertices correspond to nonempty simplices σ of N; color the vertex b_σ by dim σ∈{0,…,7}.

For each σ, let W_σ=f^(−1)(star(b_σ)), using the open star in |sd N|. For distinct σ,τ of equal dimension these open stars are disjoint: a simplex of sd N is a strictly increasing chain, which cannot contain both σ and τ. The W_σ cover B.

Choose one vertex j(σ) of σ. Every point of star(b_σ) has positive original barycentric coordinate at j(σ): its barycentric coefficient at b_σ is positive, and b_σ has positive coordinate at every vertex of σ. Hence

W_σ ⊂ {b : f_j(σ)(b)>0} ⊂ V_j(σ) ⊂ U_i(j(σ)).

It follows that p has a section on q^(−1)(W_σ). For each color k, set

Z_k = ⋃_{dim σ=k} q^(−1)(W_σ).

These are eight open subsets covering M. Their pieces for fixed k are pairwise disjoint, so the chosen sections on those pieces combine into a continuous section on Z_k. Therefore g(p)≤8. Pullback now gives g(Y→X)≤8. The cited lower bound proves the theorem. ∎

## 6. Scope and relationship to the residual obstruction

The construction permits finite circle isotropy, provided each isotropy subgroup fixes one sheet. It neither asserts that H acts freely on G/Γ nor constructs a nine-sheeted covering of the coarse orbit space B. The only coverings used for extension and pullback are the genuine covers E→M and Y→X. This distinction is the reason a nonfree circle action can still lower the section-domain bound.

An eight-domain section cover produces a section of the eightfold fiberwise join by a subordinate partition of unity. Consequently its primary obstruction in H^8(X; \widetilde H_0(S;Z)^(⊗8)) vanishes. No direct calculation of this rank-8^8 coefficient system is needed, and no assertion about arbitrary choices of higher obstruction classes is used.

This is a mathematical manuscript, not a formal proof-assistant certificate. Its finite-dimensional geometric and topological arguments require mathematical review. No executable proof verifier is included. Literature checks are bounded and do not establish novelty or an exhaustive absence of earlier resolutions.

## References

[OWR] G. Denham, G. Gaiffi, R. Jiménez Rolland, A. Suciu (organizers), *Topology of Arrangements and Representation Stability*, Oberwolfach Reports 15 (2018), 43–123, Question 5, pp. 114–115. DOI https://doi.org/10.4171/OWR/2018/2 . Publisher PDF https://ems.press/content/serial-article-files/46724 .

[CW] W. Chen and Z. Wan, *Topological complexity of finding flex points on cubic plane curves*, arXiv:2306.17303v2 (2023); publication recorded as Proc. Amer. Math. Soc. 153 (2025), 2255–2267, DOI https://doi.org/10.1090/proc/17184 . Inspected preprint https://arxiv.org/pdf/2306.17303 . The published full text was not retrieved in this investigation.

[AD] M. Artebani and I. Dolgachev, *The Hesse pencil of plane cubic curves*, Enseign. Math. 55 (2009), 235–273, DOI https://doi.org/10.4171/LEM/55-3-3 . Inspected publisher PDF https://ems.press/content/serial-article-files/44190 .

[I] S. Illman, *Smooth equivariant triangulations of G-manifolds for G a finite group*, Math. Ann. 233 (1978), 199–220, DOI https://doi.org/10.1007/BF01405351 . This is the finite-group equivariant triangulation theorem used for the compact smooth Γ-manifold H\G.

# The missing-middle-face embedding obstruction

## Statement and status

Let S be a finite simplicial complex whose realization is homeomorphic to the sphere S^{2d}. Let T be a set of d+1 vertices such that T is not a face of S, while every proper subset of T is a face. Put

K = S^{(d)},    L = K ∪ {T}.

**Claim.** The realization of L has no topological embedding in S^{2d}.

This manuscript gives a complete argument, subject to fresh independent review. It combines published results with an explicit extension of the Nevo–Wagner argument in dimension four. It does not assert that the combination is new or that an independent human peer review has occurred.

The proof separates two genuinely different issues: the source triangulation may fail to be a PL sphere, and a putative embedding may be topological rather than PL. Neither issue is suppressed. For d≥3 we use face rings and the metastable embedding theorem. For d=2 we use the mod-2 van Kampen obstruction directly. For d=1 there is an elementary edge count.

## 1. A dimension jump after adding one missing face

We first prove a purely algebraic lemma over any field F. We will eventually choose F to be a rational-function field of characteristic zero.

A triangulation S of S^{2d} is an integral homology sphere in the local sense: the link of every face has the reduced integral homology of the sphere of the appropriate dimension. Consequently its Stanley–Reisner ring A=F[S] is Cohen–Macaulay of Krull dimension r=2d+1. For a generic linear system of parameters Θ=(θ_1,…,θ_r), the quotient A/(Θ) has Hilbert function h_i(S), and Dehn–Sommerville gives

h_d(S)=h_{d+1}(S).

Let C=F[K] and B=F[L]. All rings use the same vertex variables. A and C have identical graded pieces and multiplication through degree d+1, because the first faces removed by passing to the d-skeleton have d+2 vertices. The rings B and C agree through degree d. There is a surjection B→C whose kernel M has

M_j=0 for j≤d,    M_{d+1}=F x_T,

where x_T is the squarefree monomial on T. In particular the kernel has dimension exactly one in degree d+1.

A warning is essential: simply counting one extra monomial before quotienting does not prove a one-dimensional jump after quotienting. The required exactness is as follows.

The part of the Koszul complex computing H_1(Θ;C) in total degree d+1 is

C_{d-1} ⊗ ∧²F^r → C_d ⊗ F^r → C_{d+1}.

It is identical to the corresponding part for A. Since Θ is a regular sequence on A,

H_1(Θ;C)_{d+1}=H_1(Θ;A)_{d+1}=0.

Apply the long exact Koszul-homology sequence to 0→M→B→C→0. Since M_d=0, its relevant segment is

0 → M_{d+1} → (B/(Θ))_{d+1} → (C/(Θ))_{d+1} → 0.

The degree-d quotients for A,B,C coincide, and the degree-(d+1) quotients for A,C coincide. We obtain the exact identities

(1)  dim_F(B/(Θ))_d = h_d(S),

(2)  dim_F(B/(Θ))_{d+1} = h_{d+1}(S)+1 = h_d(S)+1.

Here Θ is regular on F[S]. It is not an l.s.o.p. for F[L], whose Krull dimension is only d+1. We are taking the quotient of F[L] by r restricted ambient parameters.

## 2. No PL embedding, in every dimension

Suppose L admits a PL embedding into the standard PL sphere S^{2d}. The extension theorem of Adiprasito–Patáková [AP, Theorem 2] produces a PL triangulation P of that sphere containing the original abstract complex L as a subcomplex. It is important that L is retained without subdivision, although the embedding map is allowed to change.

Let V(P)={1,…,N}. Work over

F=Q(a_{ij}: 1≤i≤r, 1≤j≤N),

with all a_{ij} algebraically independent. On F[P] set θ_i=Σ_j a_{ij}x_j, and set ℓ=Σ_j x_j. These are the generic parameters used in the cited anisotropy theorem. Their restrictions to the variables of S are still generic, and thus form a regular parameter sequence on F[S].

By Karu–Xiao [KX, Theorems 1.2–1.3], applied to the integral homology sphere P, the quadratic form

u ↦ ℓ u² ∈ (F[P]/(Θ))_{2d+1}

is anisotropic on degree d. Indeed the theorem's n is 2d+1, its m is d, and n−2m=1. Therefore ℓu=0 implies ℓu²=0 and hence u=0. Dehn–Sommerville equates the dimensions in degrees d and d+1. Multiplication consequently gives an isomorphism

ℓ : (F[P]/(Θ))_d → (F[P]/(Θ))_{d+1}.

The quotient map F[P]→F[L] sets variables outside L equal to zero and kills the additional nonfaces of L. It descends modulo Θ. Surjectivity of multiplication by ℓ passes through this graded quotient: lift any target class to F[P]/(Θ), take a preimage there, then project. We therefore obtain a surjection

ℓ : (F[L]/(Θ))_d → (F[L]/(Θ))_{d+1}.

Equations (1)–(2) make this impossible. A vector space of dimension h_d(S) cannot surject onto one of dimension h_d(S)+1.

Thus **L has no PL embedding into S^{2d}**, even when the original triangulation S is not a PL sphere. Only the prospective ambient triangulation P had to be PL.

## 3. Topological embeddings when d≥3

A d-dimensional finite polyhedron embedded in S^{2d}, for d≥1, does not fill the sphere: otherwise the embedding would be a homeomorphism onto S^{2d}, contradicting invariance of topological dimension. Delete a point outside its image to obtain an embedding into R^{2d}.

Such an embedding induces an equivariant map from the deleted product of L to S^{2d−1}, by normalized differences. The existence part of the Haefliger–Weber theorem [W; Sk, Theorem 8.1] converts this to a PL embedding whenever

2m ≥ 3n+3,

where n is the complex dimension and m the Euclidean ambient dimension. Here n=d and m=2d, so the condition is 4d≥3d+3, exactly d≥3. This contradicts Section 2.

We use only the existence theorem. We do not claim that the original embedding is tame, that it has a PL approximation, or that it is ambient isotopic to the new embedding. The injectivity/classification range has a different bound and is unnecessary.

## 4. Dimension four: extending the bistellar obstruction argument

The metastable inequality fails when d=2. We instead prove that L has nonzero mod-2 van Kampen obstruction o^4_2(L), which rules out even topological embeddings.

### 4.1. The source is a combinatorial manifold

Every triangulation of a topological 4-manifold is a combinatorial 4-manifold. Here is the relevant reason. Local homology identifies the links of positive-dimensional simplices as homology spheres of dimension at most two. Starting with the zero-dimensional links and working upwards, these are PL spheres. Vertex links are therefore closed 3-manifolds with spherical homology. A sufficiently small punctured coordinate neighborhood at a vertex, together with radial contraction in its conical star, shows that each vertex link is simply connected. The three-dimensional Poincaré theorem makes it a 3-sphere, and Moise's theorem makes its triangulation PL standard. This fact is also explicitly recorded in [DFL, p. 797].

This does **not** assert that S is PL homeomorphic to the standard 4-sphere. A potentially exotic PL structure is allowed throughout.

### 4.2. Complement lemma

Let Q be any combinatorial 4-manifold homeomorphic to S^4, and let B_0⊂Q be the closed 4-ball supporting a bistellar move. Its boundary is locally flat in Q. At a boundary vertex the link pair consists of a PL 2-sphere inside a PL 3-sphere, and three-dimensional PL Schoenflies gives the local flatness; the lower-dimensional strata are covered by the same local argument.

Consequently

C_0=closure(|Q|\int|B_0|)

is a compact PL 4-manifold with boundary S^3 and a collar. It is contractible. In fact, van Kampen applied with collars to Q=B_0∪C_0 shows π_1(C_0)=0. Excision and the homology sequence, or Mayer–Vietoris, show that C_0 is acyclic: the map H_4(Q;Z)→H_4(B_0,∂B_0;Z) is degree ±1. A simply connected acyclic CW complex is contractible by Hurewicz and Whitehead.

Only this contractibility, not PL standardness of C_0, will be needed. In particular there is no appeal to the four-dimensional PL Schoenflies conjecture or smooth Poincaré conjecture.

### 4.3. Transfer under a bistellar move

For a combinatorial 4-manifold Q homeomorphic to S^4 define property E(Q):

For every missing triangle M of Q, o^4_2(Q^{(2)}∪{M})≠0.

We claim that E(Q) implies E(Q′) whenever Q′ is obtained from Q by one bistellar move. Write the move as

B_0=α*∂β   replaced by   B_1=∂α*β,

dim α=p, dim β=q, p+q=4.

For clarity we specify the exact ingredients imported from [NW, Section 5]. Their Theorem 5.3 transfers the nonzero obstruction across a bistellar change in the augmented 2-complex when:

- intersection cochains can be chosen with all intersections outside the move's old and new supports;
- there is a vertex outside the support;
- the induced complements used in their homological coning construction have vanishing reduced H_0 and H_1.

This theorem is a statement about general-position maps and finite chain complexes; it assumes no PL-sphere condition beyond those listed hypotheses. Their Lemma 5.2 constructs the required homological cones.

Suppose first that a missing triangle M of Q′ was also missing in Q. Its boundary lies outside the interior of the move support. By the complement lemma, its boundary map extends continuously over a disk into C_0. Use a collar to push the disk's interior into int C_0, and relative PL general position to avoid the 1-skeleton of Q. An embedded disk is not required. Combining this map with the natural embedding of Q^{(2)}, and then with a homeomorphism Q\{x}→R^4 for x in the interior of B_0 off Q^{(2)}, gives the old general-position map. Transport across a homeomorphism B_1→B_0 fixed on the common boundary to get the new one. The forbidden disjoint-face intersections are absent; simultaneous small relative approximations preserve this and make the maps general-position representatives if needed.

The support is induced and not the whole sphere, so an outside vertex exists. For the homology condition, the forbidden vertex subsets W appearing in [NW, Observation 5.1] have Q[W] a cone. Alexander duality in the topological sphere and the standard deformation retraction onto the complementary induced complex give zero reduced homology. Passing to the 2-skeleton and adding a triangle cannot create H_0 or H_1. These checks establish precisely the hypotheses of [NW, Theorem 5.3]. Hence its transfer conclusion applies.

For newly missing triangles, [NW, Claim 2 in the proof of Theorem 1.2] is purely combinatorial and leaves two possibilities:

1. p=q=2 and M=α. The old missing triangle β gives exactly the same augmented 2-complex, so E(Q) applies.
2. q=1, p=3 and M=v*β for a vertex v outside the move support. The final local witness construction in [NW, proof of Theorem 1.2, pp. 13–14] applies. It uses the homological cones just verified and the linking number inside the explicit standard ball ∂α*β. The pairing of the witness with the intersection cochain is the linking of ∂M with ∂α, which is one modulo two. Its ambient input is only a homeomorphism Q′\{o}→R^4, not a PL homeomorphism.

Thus E(Q′) holds. This checks every occurrence of the global PL-sphere hypothesis in the cited induction: the transfer-map construction used the complement lemma instead of a PL complement-ball theorem; the homological and new-face arguments use only the topological sphere and the standard local bistellar ball.

### 4.4. A vacuous base in the correct PL class

The barycentric subdivision sd(S) is flag. Its vertices are faces of S, and a pairwise-comparable collection is a chain. Therefore any three pairwise adjacent vertices span a triangle. It has no missing triangles, so E(sd(S)) holds vacuously.

The complexes sd(S) and S triangulate the same closed PL 4-manifold. Pachner's theorem for closed combinatorial manifolds [L, Theorem 5.9] provides a finite bistellar sequence between them. Every intermediate complex remains a combinatorial 4-manifold homeomorphic to S^4. Apply the transfer result at each move. We conclude E(S), and hence o^4_2(L)≠0.

The nonzero van Kampen obstruction forbids topological embeddings. This finishes d=2 without asserting that every triangulated 4-sphere is PL standard.

## 5. Low dimensions and conclusion

For d=1, the 1-skeleton of a triangulated 2-sphere with n vertices has 3n−6 edges: each triangular face is incident to three edges and each edge to two faces, and Euler's formula applies. Adding a missing edge gives 3n−5 edges, exceeding the planar bound for simple graphs. Thus L cannot embed into S^2.

Under the usual convention that missing faces are subsets of the actual vertex set, d=0 is vacuous. If one instead permits an additional missing singleton outside that set, a triangulated S^0 consists of two points and adding the singleton gives three points, which cannot embed in S^0.

Sections 2–3 prove the claim for every d≥3, Section 4 proves d=2, and the preceding paragraph proves d=1. Therefore the claimed topological non-embeddability holds in every dimension.

## References and exact inputs

- [NW] E. Nevo and U. Wagner, *On the Embeddability of Skeleta of Spheres*, Israel J. Math. 174 (2009), 381–402. [Author preprint](https://pi.math.cornell.edu/~eranevo/homepage/NevoWagner-EmbeddabilitySkeletaSpheres-Rev2.pdf), dated 4 February 2008. Theorem 1.2 is the PL-source case; Conjecture 1.3 is the present question. Section 5, especially Observation 5.1, Lemma 5.2, Theorem 5.3 and the final proof, supplies the explicitly audited local transfer argument.
- [KX] K. Karu and E. Xiao, *On the anisotropy theorem of Papadakis and Petrotou*, Algebraic Combinatorics 6 (2023), 1313–1330. [Published paper](https://alco.centre-mersenne.org/articles/10.5802/alco.298/). Theorems 1.2–1.3 supply anisotropy for the generic reduction, including the characteristic-zero version for spheres that are homology spheres over F_2.
- [AP] K. Adiprasito and Z. Patáková, *A higher-dimensional version of Fáry's theorem*, Bull. London Math. Soc. 57 (2025), 1409–1414. [DOI](https://doi.org/10.1112/blms.70036), [author version](https://arxiv.org/abs/2404.12265). Theorem 2 extends a finite PL-embeddable complex, without subdividing it, to an ambient triangulation.
- [W] C. Weber, *Plongements de polyèdres dans le domaine métastable*, Comment. Math. Helv. 42 (1967), 1–27. [Original record](https://eudml.org/doc/139330).
- [Sk] A. Skopenkov, *Embedding and knotting of manifolds in Euclidean spaces*. [Author survey](https://arxiv.org/abs/math/0604045). Theorem 8.1 states the precise existence bound 2m≥3n+3 used here; this is a locator for [W].
- [L] W. B. R. Lickorish, *Simplicial moves on complexes and manifolds*, Geometry & Topology Monographs 2 (1999), 299–320. [Article](https://arxiv.org/abs/math/9911256). Theorem 5.9 proves the closed-manifold Pachner equivalence used here, without requiring either manifold to be PL standard.
- [DFL] M. W. Davis, J. Fowler and J.-F. Lafont, *Aspherical manifolds that cannot be triangulated*, Algebraic & Geometric Topology 14 (2014), 795–803. [Author paper](https://people.math.osu.edu/lafont.1/agt-DFL.pdf), p. 797, explicitly explains why all triangulations of topological 4-manifolds are PL triangulations.

The exact computations accompanying this manuscript are finite consistency checks. They do not replace the cited topological or algebraic theorems, the Koszul exactness argument, or the dimension-four transfer proof.

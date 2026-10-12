# Rational Hodge transfer to mixed K3 moduli products

Status: established reduction conditional on the base-product hypothesis below. It does not establish that hypothesis. This is research documentation, not an unconditional solution preprint.

## Precise conditional theorem

Let S_1,...,S_r be complex projective K3 surfaces, α_i∈Br(S_i), and M_i smooth projective moduli spaces as in Bülles, Theorem 0.1: moduli of Gieseker-stable α_i-twisted sheaves, or moduli of σ_i-stable objects in D^b(S_i,α_i) for a generic stability condition σ_i. Smoothness and projectivity are assumptions on the actual moduli spaces; this statement does not establish existence, nor enlarge the cited theorem to singular semistable moduli. Ordinary untwisted sheaves are obtained by α_i=0. For Gieseker stability a polarization and the relevant sheaf data are fixed as required by the moduli problem. The term “generic” for Bridgeland stability is relative to those fixed numerical data; every point of the stated moduli is stable. No additional universal-family or primitivity hypothesis is inserted into Bülles' theorem.

Assume rational Hodge in every codimension for every variety ∏_{i=1}^r S_i^{k_i} with nonnegative integers k_i needed in the finite Chow-motive decompositions. In particular, assuming it for all such k_i suffices. Then rational Hodge holds in every codimension for X=∏_{i=1}^r M_i. For positive-dimensional M_i it suffices to check 0≤k_i≤dim M_i. A zero-dimensional factor can be handled separately.

## Correspondence conventions

For smooth projective V,W with dim V=d_V and a rational cycle A∈CH^a(V×W)_Q, define

A_*z=(pr_W)_*((pr_V)^*z·A).

The same formula on cohomology sends H^{2p}(V,Q)∩H^{p,p} into H^{2(p+a-d_V)}(W,Q)∩H^{p+a-d_V,p+a-d_V}. Pullback, multiplication by an algebraic (a,a) class, and integration over the d_V-dimensional source give this degree and type shift. The cycle class map commutes with all three operations.

The composition of A∈CH^a(V×W)_Q and B∈CH^b(W×V)_Q has codimension a+b−dim W in V×V. Thus a+b=d_V+dim W makes B∘A a degree-preserving correspondence on V. This convention avoids ambiguity in the sign of a Tate twist.

## Proof

Bülles' direct-summand theorem provides a finite family of products K_{ij}=S_i^{k_{ij}} and complementary homogeneous algebraic correspondences

A_{ij}∈CH^{a_{ij}}(M_i×K_{ij})_Q,
B_{ij}∈CH^{b_{ij}}(K_{ij}×M_i)_Q,

a_{ij}+b_{ij}=dim M_i+dim K_{ij},
Σ_j B_{ij}∘A_{ij}=Δ_{M_i} in CH^{dim M_i}(M_i×M_i)_Q.

These identities mean a split summand in rational Chow motives; the projectors and Tate twists can be absorbed into the algebraic maps. The existence of these maps is the externally cited theorem, rather than a claim derived from a hypothetical honest universal family.

Take exterior products for a multi-index J=(j_1,...,j_r). Set K_J=∏_i K_{ij_i}, A_J=⊠_i A_{ij_i}, B_J=⊠_i B_{ij_i}, a_J=Σ_i a_{ij_i}, and b_J=Σ_i b_{ij_i}. Composition of exterior products is the exterior product of compositions. Every class involved is even, so no Koszul sign is introduced. Expanding the product of the diagonal identities gives

Σ_J B_J∘A_J=Δ_X,
a_J+b_J=dim X+dim K_J.

Let z∈H^{2p}(X,Q)∩H^{p,p}. Put q_J=p+a_J−dim X. The class A_{J*}z is a rational (q_J,q_J) class on K_J. If q_J is outside [0,dim K_J], this cohomology group is zero. Otherwise the assumed base-product Hodge conjecture gives Z_J∈CH^{q_J}(K_J)_Q with cl(Z_J)=A_{J*}z. In the zero case take Z_J=0. Then

Z=Σ_J B_{J*}Z_J∈CH^p(X)_Q,

because q_J+b_J−dim K_J=p. Compatibility with cycle classes and the diagonal identity give

cl(Z)=Σ_J B_{J*}A_{J*}z=z.

This proves the conditional claim in every codimension.

## Boundary cases

- An empty moduli factor makes the product empty and the surjectivity statement trivial.
- A smooth projective zero-dimensional factor over C is a finite disjoint union of points. Its cohomology and motive are sums of the unit; each point component reduces to the product of the other factors.
- r=0 and S^[0] are points; S^[1]=S. For n≥1, S^[n] is the smooth projective rank-one ideal-sheaf moduli with Mukai vector (1,0,1−n), covered by the untwisted case.
- Repeated and distinct bases are permitted; the proof explicitly uses HC for K_J, a mixed product, and never infers mixed HC from separate self-power statements.
- Codimension p<0 or p>dim X has zero target; these cases require no cycles.

## Logical strength

If the universal mixed-moduli target holds, choose M_i=S_i^[1]=S_i for every factor. Then rational Hodge holds for every mixed product of projective K3 surfaces. Conversely, the universal mixed-K3 statement plus Bülles proves the target by the preceding argument. Thus the two universal assertions are equivalent given the established motivic reduction. This is not a counterexample to the target, and it does not resolve the upstream universal input.

## Attribution and excluded conclusions

Bülles supplies the unconditional Chow-motive splitting. Arapura supplies older conditional consequences for Hilbert schemes and sheaf moduli. The upstream quadratic-locus companion explicitly records related moduli/self-power transfer; an all-base mixed corollary would be an assembled consequence, not a new reduction or an independent base-conjecture solution.

No inference here establishes HC for arbitrary deformations of K3^[n] type, singular moduli, moduli on arbitrary abelian surfaces, integral or generalized Hodge, or finite-dimensional Chow motives. No conventional human peer review has occurred. AI tools have been used extensively in this documentation and its audits.

## Primary source links

- Bülles: https://arxiv.org/abs/1806.08284v1, Theorem 0.1 and §2.1.
- Arapura: https://arxiv.org/abs/math/0102070, exact version and locators in agent_notes/bulles_transfer.md.
- Pinned upstream repository: https://github.com/openai/math/tree/adc7f1241b42e322a6451854ab7e4b4c146bf78a; source fingerprints in sources/UPSTREAM_MANIFEST.json.

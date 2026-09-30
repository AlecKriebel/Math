# KP-4.59: exact order-231 algebra and the unresolved topological gap

Status: **unsolved**. No topological cobordism or full obstruction has been constructed. All computations below concern necessary algebraic conditions, not a realization theorem. Independent review pending; no novelty claim.

## Target and primary sources

[K3 Problem 4.59, printed p.238](https://bpb-us-e2.wpmucdn.com/websites.umass.edu/dist/b/22144/files/2026/04/K3-problem-list-watermarked.pdf) asks whether topologically integral-homology-cobordant lens spaces must be homeomorphic. Its discussion identifies L(231,53) and L(231,86) as an unresolved test pair, credits Gilmer–Livingston for the prime-power case, and explains why higher-dimensional homology surgery does not directly solve the four-dimensional problem. It further reports that a hypothetical 231-fold cyclic cover of a cobordism for this pair must have nonzero first Betti number. This last restriction is retained as a cited source result, not independently rederived from signature formulas here.

[Doig–Wehrli, arXiv:1505.06970v1](https://arxiv.org/abs/1505.06970) proves the smooth classification via correction terms. Its proof uses smooth cobordism invariance, notwithstanding the combinatorial computation of the boundary invariants. That does not establish invariance across an arbitrary topological four-manifold. Their lens-space homeomorphism criterion supplies the arithmetic check below.

Homology means integral homology, not rational homology. For the forward implication one normally fixes oriented cobordisms and oriented homeomorphisms; the pair below is not even unoriented-homeomorphic, so it avoids this convention issue. The converse for a homeomorphic pair is the product cobordism, with orientations chosen consistently.

No prior dedicated attempt, campaign publication or exact imported research-result key was found at intake. Current queue rank87 was queued0/5. The complete-record scan found no other lens-space homology-cobordism target. Website retrieval failed; the pinned full record and primary sources were used.

## 1. The candidate passes linking-form tests but fails homeomorphism tests

Write p=231=3·7·11. In the generator convention λ_q(x,y)=qxy/p mod Z, an isometry from λ_53 to λ_86 has form x↦ux with u a unit modulo p, and requires

86u² ≡ 53 (mod 231).

This equation has exactly eight unit solutions:

10, 32, 67, 109, 122, 164, 199, 221.

For example, 86·10²−53=8547=37·231. Exhaustive modular enumeration independently checks the complete list. Using q^{-1}/p instead as the convention conjugates the description of generators and does not remove the existence of an isometry.

By the lens-space classification, the unoriented homeomorphism orbit of L(231,53) is described by q'∈{±53,±53^{-1}} modulo231. Since 53^{-1}≡170, this set is {53,178,170,61}. It does not contain86. Therefore these lens spaces are not homeomorphic, even after reversing orientation.

An equivalent boundary algebra check uses G=(Z/231)² with nonsingular pairing

λ((x,y),(x',y'))=(53xx'−86yy')/231 mod Z.

The graph M={(x,10x):x∈Z/231} is isotropic, by the congruence above. It has order231, the square root of |G|, so nonsingularity implies M=M^⊥: it is a metabolizer. Projection to either cyclic factor is an isomorphism. Thus this boundary linking data is consistent with the graph-type metabolizer expected from an integral homology cobordism. It does not construct such a cobordism.

The fact that linking forms are preserved by oriented integral homology cobordism can be expressed using the natural torsion-linking construction from the Bockstein and Poincaré duality; the two inclusions identify the pairings with the same cobordism data. The graph computation exhibits why this necessary test cannot distinguish this pair.

## 2. Elementary constraints on the cyclic cover

Let W be a hypothetical connected oriented topological integral homology cobordism between the two lens spaces of order p. The inclusions identify H₁(W;Z) with Z/p. Let V→W be the connected p-fold cover from the kernel of the abelianization map to Z/p.

Each boundary restriction is the universal cover of its lens space, since π₁(L)=H₁(L)=Z/p maps isomorphically to H₁(W). Hence ∂V=S³⊔S³. Also χ(W)=χ(L)=0 and χ(V)=pχ(W)=0.

Over Q, the long exact sequence of (V,∂V) gives a short exact sequence

0 → H₁(V;Q) → H₁(V,∂V;Q) → Q → 0,

because H₁(∂V;Q)=0 and the map H₀(∂V;Q)→H₀(V;Q) has one-dimensional kernel. Poincaré–Lefschetz duality therefore gives b₃(V)=b₁(V)+1. Since b₀(V)=1 and b₄(V)=0, Euler characteristic now yields

b₂(V)=2b₁(V).

These equalities hold for every such connected cover, without any smoothness assumption. Combining them with the additional source-reported nonvanishing restriction for the order231 pair would force b₂(V)≥2 and b₃(V)≥2. The nonvanishing input has not been independently proved in this package.

A further conditional fact is useful for testing a proposed construction. If π₁(W)=Z/p, then V is simply connected. In that case the equalities imply b₂(V)=0. Moreover H₂(V;Z) is torsion-free: since H₁(V;Z)=0, the universal coefficient theorem identifies H²(V;Z) with Hom(H₂(V;Z),Z); duality and H₂(∂V)=H₁(∂V)=0 identify H²(V;Z) with H₂(V,∂V;Z)≅H₂(V;Z). Thus H₂(V;Z)=0. The other groups are those of S³×I, with either boundary inclusion an integral homology equivalence. Since V and S³ are simply connected, the homology version of Whitehead's theorem gives homotopy equivalences. Consequently W would be an h-cobordism.

This conditional reduction is not a construction or a general homeomorphism classification of topological h-cobordisms. In particular, do not import a dimension≥5 surgery or h-cobordism theorem into dimension4. It is consistent with the source's warning that the unresolved pair requires a more complicated cyclic cover.

## 3. Blocked routes and exact gap

1. Linking forms and the first homology: explicit exact tests pass for the nonhomeomorphic order231 pair. These necessary algebraic constraints alone provide no obstruction.
2. Smooth correction terms: the boundary arithmetic is computable, but the needed topological cobordism invariance is not supplied. Declaring it invariant would silently replace the original category.
3. Cover/handle realization: the cover identities constrain any candidate. They do not build a group/action and a topological four-manifold with the required boundary and integral homology. Higher-dimensional homology surgery does not fill this gap.

What remains is an actual topological integral homology cobordism for a nonhomeomorphic pair, or a valid obstruction applying to all such cobordisms at composite order, including those with nontrivial cyclic-cover H₁. This note does neither. Proposed status: unsolved,3/5 approaches. Source and arithmetic diagnostic completion100%; full original classification completion0%.

The verifier exhausts every candidate unit and graph element, checks all graph-pair linking values exactly, and validates the displayed integer identities. No floating point signatures, new rho-invariant computation or topological realization is claimed. Runtime metadata: inherited runtime; exact model identifier not exposed to this worker; no model/reasoning switch made.

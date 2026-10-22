# Partial results for Agol's tree action and Thurston norm question

Target: 10900010 / AMR-108-0010, rank 672, Agol Question 3.2 in Delp--Hoffoss--Manning (2015).

Status: **NO RESOLUTION of the general question.** This note proves special cases and records precise obstructions to extending them. The deductions are not claimed to be new. In particular, a surface embedded in a covering space is not automatically embedded under its covering projection.

## 1. Source and conventions

The primary problem is §3.2 on printed/PDF page 2 of [DHM]. Its input is a fixed-point-free simplicial tree action of a 3-manifold group. It concerns the class selected by an edge in the associated edge-stabilizer cover, and asks whether that class has a Thurston-norm minimizer which embeds downstairs. The norm is therefore an upstairs norm; replacing it by the norm of the pushed-forward class changes the problem.

The short source does not explicitly specify closedness, orientability, irreducibility, coefficients, inversions, or boundary conventions. We do not use those omissions to claim a counterexample. The proofs below use closed, connected, oriented, smooth 3-manifolds and integral ordinary homology. Extra hypotheses are stated at the point of use. Compact manifolds with boundary would require proper surfaces and a relative homology formulation; that extension is not asserted here.

Write G=π1(M), let T be a simplicial tree, and suppose G acts without edge inversions. Choose an oriented edge e and an interior point m, and write H=Stab_G(e). Without inversions, H fixes e pointwise and preserves its chosen orientation. Let

q: M̃ → N=M̃/H,       p: N → M.

Thus N is the edge-stabilizer cover. It need not be regular. We interpret 'embeds in M' as: for an embedded representative S⊂N, the restriction p|S is an embedding. Merely asking whether the abstract surface type admits some unrelated embedding in M would discard the content of the question.

For a compact oriented surface S=⊔S_i, put

χ_-(S)=Σ_i max(0,-χ(S_i)).

For a representable α∈H_2(N;Z), define x_N(α) as the minimum of χ_-(S) over compact embedded oriented representatives. Noncompactness of N does not prevent this minimum from existing: the feasible set is nonempty and its complexities are nonnegative integers. It does not provide a finite algorithm or a canonical minimizer.

The two components of T\{m} should be regarded as sides, or as a partition of the relevant ends, rather than as a claim that each side has exactly one topological end. We use the action-defined class below instead of assuming H_2(N)=Z. If the action has inversions, subdivision changes the edge stabilizer relevant to a half-edge; that change must be tracked, rather than silently identifying the two covers.

## 2. A canonical class and a descending representative

**Lemma 1.** For the conventions above, a transverse, finite-type G-equivariant map F:M̃→T defines a class

α_e=[F^{-1}(m)/H]∈H_2(N;Z)

which is independent of F. The surface F^{-1}(m)/H is compact, and its projection to M is embedded. Reversing the edge orientation reverses α_e.

Here finite-type means that the construction is carried out over a finite triangulation of M, with only finitely many tree edges used over a compact fundamental set. Such maps exist: choose images of representatives of vertices of M̃, extend equivariantly over edges by the unique tree paths, and extend over higher cells because T is contractible. A piecewise smooth general-position adjustment near the orbit of m makes inverse images surfaces. This is the usual dual-surface construction; see also [C], Example 1.5.

**Proof.** Distinct points in the orbit Gm have disjoint inverse images. Their union is G-invariant, so its quotient gives an embedded surface D in M. Since e has no inversion, the chosen coorientation of e extends consistently over its G-orbit and hence orients D.

Put U=F^{-1}(m). If x,y∈U have the same image in M, then y=gx for some g∈G. Equivariance gives m=F(y)=gF(x)=gm. Thus g∈H, and x,y already have the same image in U/H. Consequently p restricts to a one-to-one local embedding U/H→M; it identifies U/H with D.

For compactness, take finitely many lifted closed simplices whose G-translates cover M̃. Their images meet only finitely many points in the orbit Gm. For a translate of one such simplex to meet F^{-1}(m), its translating element must carry one of those finitely many orbit points to m. For each such point the permitted translating elements form a single left H-coset. Modulo H, finitely many compact pieces therefore cover U/H.

Any two equivariant maps are equivariantly homotopic by the unique pointwise geodesics in T. Use a finite-type homotopy, transverse to m after a relative general-position adjustment. Its inverse image of m modulo H is a compact oriented 3-dimensional bordism in N×[0,1], by the same finite-orbit argument. Its boundary is the difference of the two representative surfaces. They have the same ordinary homology class. ∎

This argument does not claim that the dual surface is connected, incompressible, norm-minimizing, or that its dual tree is isomorphic to T. There is generally only an equivariant map from its dual tree to T; folding information may remain.

Define the descending minimum

μ_e = min{χ_-(S): S⊂N compact oriented embedded, [S]=α_e, p|S an embedding}.

Lemma 1 makes this set nonempty. Thus

0 ≤ x_N(α_e) ≤ μ_e < ∞.

The general question is exactly whether the nonnegative integer μ_e-x_N(α_e) is always zero, for the intended class of manifolds and actions. This reformulation does not establish that it is zero.

## 3. Compression alone is insufficient

A compression of a descending representative along a disk downstairs lifts to a compression upstairs, preserves its class, and does not increase χ_-. The lifted disk exists because it is simply connected and its boundary has the prescribed lift. Since the original disk interior misses the whole downstairs surface, its lift misses the chosen upstairs surface. Surgery therefore preserves the descent property as well. This gives a way to remove compressions; it does not compare all incompressible representatives of the class.

There is an explicit test against the inference 'essential dual surface implies norm-minimizing'. Let Σ_g be closed orientable of genus g≥2 and let M=Σ_g×(R/Z). The action is translation by the circle character, with N=Σ_g×R. On one period define the piecewise linear degree-one height map h by

h(0)=0, h(1/3)=1, h(2/3)=0, h(1)=1,

and extend by h(t+n)=h(t)+n. The level h=1/2 consists of three slices at t=1/6,1/2,5/6, with signs +,-,+. Each slice is π1-injective, and the three-slice surface descends to three disjoint essential surfaces in M. Its class is the generator α, but its complexity is 3(2g-2). The single slice has class α and complexity 2g-2, which is minimal by Proposition 4 below. The corners of h can be smoothed away from the three regular roots without changing this example.

Thus this action has both an essential non-minimizing dual surface and a minimizing dual surface. It is a negative control for a proof shortcut, not a counterexample to Agol's existence question. It also shows that the choice of equivariant map can matter greatly at the representative level even though α_e is unchanged.

## 4. A pushforward bound and a sufficient certificate

We use the following standard consequence of Gabai's singular/embedded norm theorem [G]: for a closed oriented irreducible 3-manifold M and a map f:R→M of a compact oriented surface,

x_M(f_*[R]) ≤ χ_-(R).                                             (1)

The use of this inequality for immersed surfaces is explicit in [CT], printed page 13. This packet does not reprove Gabai's theorem. Its original publisher endpoint did not yield a readable PDF in this retrieval; [CT] is a directly inspected primary research source for the exact inequality being used.

**Proposition 2.** Under the hypotheses of (1), every covering p:N→M and representable α∈H_2(N;Z) satisfy

x_M(p_*α) ≤ x_N(α).

If there is a compact embedded S⊂N representing α such that p|S embeds and χ_-(S)=x_M(p_*α), then S is minimizing in N and descends. In particular, this certifies a positive answer for a tree edge whenever such an S has class α_e.

**Proof.** Apply (1) to p|R for every embedded representative R of α and minimize. Under the certificate hypothesis, χ_-(S)=x_M(p_*α)≤x_N(α)≤χ_-(S), so equality holds. ∎

The certificate contains both the lift into the specified cover and the upstairs class identification. Computing only a taut surface in the class p_*α does not supply those facts. A component lifts to N with a chosen basepoint only if its fundamental-group image lies in H (up to the relevant conjugacy). Different components can require different lift choices, and their resulting sum must still be α, not merely have the same pushforward.

## 5. A positive answer for translation actions on a line

**Theorem 3.** Let M be closed, connected, oriented and irreducible. Let φ:G→Z be onto, and let G act on the simplicial line with vertices Z by g·t=t+φ(g). For every edge e, the class α_e in N=M_kerφ has a norm-minimizing representative whose projection to M is embedded. More precisely,

x_N(α_e)=x_M(PD(φ)).

The same conclusion holds when all translation lengths are multiplied by a positive integer, after choosing the primitive character defining the kernel and identifying the corresponding edge class. No fibering hypothesis is needed.

**Proof.** Choose a compact embedded oriented surface D⊂M representing PD(φ) and realizing x_M(PD(φ)). A cooriented surface determines a map f:M→R/Z whose regular fiber at an interior value is exactly D: use its cooriented product collar to traverse the circle once and map the complement to a point outside that regular value. For disconnected D perform this simultaneously on the disjoint collars. Its induced integral cohomology class counts oriented intersections with D, so it equals φ.

Lift f to f̂:N→R. The generator a of the infinite-cyclic deck group can be chosen so that f̂(ax)=f̂(x)+1. Choose a lift t_0 of the regular value, and put S=f̂^{-1}(t_0).

For each x∈D, its fiber in N is a Z-orbit, and the values of f̂ on that orbit are all translates by integers of one lift of f(x). Exactly one of them equals t_0. Thus p|S:S→D is bijective. It is locally a diffeomorphism, so it is a diffeomorphism and S is compact. Its fundamental class is α_e after choosing compatible orientations: the universal lift of f is a G-equivariant map to the same line, and Lemma 1 identifies its edge-level class with the action-defined one. Hence

x_N(α_e) ≤ χ_-(S)=χ_-(D)=x_M(PD(φ)).

Also p_*α_e=[D]=PD(φ). Proposition 2 gives the reverse inequality. ∎

This argument uses an essential special property: the edge stabilizer is the kernel of the entire circle character. For a general branching tree, the stabilizer of an edge is typically much smaller than the kernel of a character obtained by passing to the quotient graph. The lift argument then fails. If the quotient graph is a tree, there need not be any nonzero quotient-graph character at all. Orientation-reversing line actions are not included in this theorem.

## 6. An elementary surface retraction certificate

**Proposition 4.** Let p:N→M be a covering of oriented 3-manifolds. Suppose S_0⊂N is a closed connected oriented surface of genus g≥1, its projection embeds, and there is a continuous map r:N→S_0 such that

r_*α=[S_0],       [S_0]=α∈H_2(N;Z).

Then x_N(α)=max(0,2g-2), realized by S_0.

**Proof.** The case g=1 follows from nonnegativity and χ_-(S_0)=0. Suppose g≥2. Let R=⊔R_i be an arbitrary compact embedded oriented representative of α, and let d_i be the degree of r|R_i. The identity r_*[R]=[S_0] implies Σd_i=1, so at least one d_i is nonzero.

For any map u:R_i→S_0 of nonzero degree d, the map u^*:H^1(S_0;Q)→H^1(R_i;Q) is injective. Indeed, if a≠0, nondegeneracy of the cup-product pairing on S_0 supplies b with ⟨a∪b,[S_0]⟩≠0. Naturality gives

⟨u^*a∪u^*b,[R_i]⟩ = d⟨a∪b,[S_0]⟩ ≠0,

so u^*a cannot vanish. Consequently 2 genus(R_i)≥2g. Therefore χ_-(R)≥χ_-(R_i)≥2g-2. Since S_0 realizes that value, it is minimizing. ∎

Only the existence of one nonzero degree component is used. We have not invoked an unproved formula for the norm of every multiple kα, or assumed that a disconnected representative has a connected component of degree exactly one.

**Corollary 5.** Let M be closed, connected, oriented and aspherical, and let D⊂M be a closed, connected, oriented, two-sided, π1-injective surface of genus g≥1. Put H=i_*π1(D). In the cover N associated to H, the preferred lift S_0 of D is norm-minimizing in its own class. If the tree action is the Bass--Serre action obtained by cutting M along D, this answers the question positively for its edge class.

**Proof.** The lift S_0→N induces an isomorphism on π1. Both spaces are aspherical CW spaces, so it is a homotopy equivalence and has a homotopy inverse r. In particular r_*[S_0]=[S_0], in the respective domains. Proposition 4 applies. For the stated geometric tree action, collapse the complementary pieces to vertices and each product collar to its edge. The selected edge preimage in N is S_0, proving α_e=±[S_0]. ∎

The assumption that H is exactly the image of the surface group matters. Replacing H by a larger edge stabilizer can destroy the homotopy equivalence and the retraction certificate. The statement does not prove that every abstract tree splitting is realized by an embedded surface carrying all of H.

## 7. A separating example with a completely uninformative downstairs bound

Here is an explicit family where Proposition 2's lower bound is strictly smaller than the upstairs norm, even though the desired descending minimizer exists.

For g≥2, let Σ_g→B_{g+1} be the orientation double cover of the closed nonorientable surface of genus g+1. Its deck involution τ is free and orientation reversing. On Σ_g×(R/2Z), let

ι(x,[t])=(τ(x),[-t]),       M_g=(Σ_g×(R/2Z))/⟨ι⟩.

The involution is free and preserves the product orientation. Thus M_g is a closed oriented 3-manifold. It is aspherical because Σ_g×(R/2Z) is aspherical and is a finite cover of M_g.

There is a regular covering N=Σ_g×R→M_g with deck group generated by

a(x,t)=(x,t+2),       r(x,t)=(τ(x),-t).

These satisfy r²=1 and rar=a^{-1}; the deck group is infinite dihedral. Choose the edge e=(0,1). It acts on the line by the t-coordinate, with vertices the integers. No edge is inverted, and there is no global fixed point. Composing G=π1(M_g)→D_∞ with this action yields an action whose edge stabilizer is π1(Σ_g), the kernel of the covering quotient. Thus N is exactly its edge-stabilizer cover.

Let S_0=Σ_g×{1/2}. Its only images under the deck transformations have heights 2n+1/2 and 2n-1/2. The first equals 1/2 only for n=0, and the second never does. Hence S_0 projects injectively. The projection r_Σ:N→Σ_g supplies Proposition 4, giving

x_N([S_0])=2g-2.

The map ρ:M_g→[0,1] induced by the distance of t to 2Z has the image of S_0 as its level 1/2. That level is the boundary of the compact submanifold ρ^{-1}([0,1/2]); therefore p_*[S_0]=0. It follows that

x_M(p_*[S_0])=0 < 2g-2=x_N([S_0]).

This is not a negative answer to the target: the displayed surface itself is a descending minimizer. It is a counterexample to the stronger auxiliary identity x_N(α_e)=x_M(p_*α_e) for arbitrary tree actions. It shows why the argument for translation actions cannot be extended by simply dropping the character-kernel hypothesis.

## 8. The exact obstruction in the universal cover

**Lemma 6.** Let S⊂N be compact embedded and put U=q^{-1}(S)⊂M̃. Then p|S is an embedding if and only if

U∩gU=∅ for every g∈G\H.                                         (2)

**Proof.** If z∈U∩gU with g∉H, write z=gy with y∈U. The points q(z) and q(y) are distinct: equality would give z=hy for some h∈H, hence h=g by freeness of the deck action. But they have the same image in M. Conversely, two distinct points of S with the same image lift to points z,y∈U with z=gy; then g∉H and z∈U∩gU. Compactness converts the resulting injective immersion into an embedding. ∎

For a nonnormal H, (2) cannot be replaced by disjointness under the deck group of N→M. That deck group is only N_G(H)/H. Testing it can miss collisions caused by elements outside the normalizer. The finite-group control included with this note demonstrates the distinction at the coset level.

Thus a sufficient missing theorem is: one can choose an upstairs norm-minimizer for α_e satisfying every disjointness condition in (2). Neither the existence of an upstairs minimizer nor the existence of one descending non-minimizer provides that theorem.

## 9. Why the remaining methods did not close the gap

### Least area and intersection theory

One may compress a norm-minimizer and then try a least-area representative in its homotopy class. This does not change its domain's genus, but the main embedding theorem of Freedman--Hass--Scott [FHS, Theorem 5.1] assumes that the map is already homotopic to a two-sided embedding. The edge class identifies homology, not that homotopy class. Their disjointness theorem likewise requires maps that can be homotoped disjoint. We did not derive those hypotheses from α_e or establish (2).

At a formal level, exchange-and-roundoff preserves total Euler characteristic, whereas χ_- is a componentwise truncation. The numerical equality 0+0=2+(-2) permits χ_- totals 0 and 2; hence an Euler-characteristic identity alone is not a norm inequality. This numerical control is not asserted to be a realizable exchange of incompressible tori. A successful topological exchange argument must exclude or remove positive-Euler-characteristic components, preserve each required class, and respect all translates simultaneously. In a common cover associated to H∩gHg^{-1}, the cut pieces can also be noncompact; their Euler characteristics cannot be summed as if they were compact fundamental domains.

Scott--Swarup [SS] provides algebraic compatibility and intersection-number results. The geometric surface subgroups of components of an upstairs norm-minimizer may be proper subgroups of H. The zero-crossing fact attached to the original H-splitting does not, in this investigation, imply the requisite zero self-intersection statement for each such component. No new homotopy-to-embedding theorem is claimed.

### Normal surfaces, finite covers, and taut certificates

A finite triangulation of a suitable compact manifold permits normal-surface norm calculations [CT]. The prescribed cover N can be infinite and no general finite compact core containing every potential minimizing representative was supplied. Even if one computes x_N(α_e) inside a certified suitable compact region, the additional descent condition (2) still has to be enforced. An arbitrary truncation of the cover can establish neither a global lower bound nor descent.

A finite cover in which a surface embeds is also insufficient: the question asks it to embed in M. Averaging or taking a union of finite deck translates can create intersections and changes multiplicities and the target class. Finite-cover multiplicativity for a pulled-back cohomology class cannot be applied to an arbitrary ordinary homology class in an infinite edge cover.

Cigna's 2026 paper [Ci] makes extraction of Thurston-norm information from sutured hierarchies explicit. The hierarchies certify surfaces in a specified compact manifold; the theorem does not supply a hierarchy that simultaneously satisfies (2) for this infinite cover.

The August 2026 version of Jaikin-Zapirain--Kudlinska--Sánchez-Peralta [JKS, Corollary 1.5] establishes existence of an optimal admissible splitting dual to a nonzero character, with complexity measured by an L²-Betti number. Its quantifier allows the splitting and its edge group to vary. Agol's question keeps the tree action and edge cover fixed, and also includes quotient graphs with no nonzero character. We found no implication from that theorem to μ_e=x_N(α_e).

## 10. Final mathematical conclusion

The compact dual-surface construction, the pushforward certificate, the translation-line theorem, the surface-group retraction theorem, and the explicit separating family are proved above. The general minimizer-descent statement is neither proved nor disproved. The exact unclosed step is to produce an upstairs minimizer satisfying (2), or to exhibit an action for which every upstairs minimizer violates it.

The supplied controls verify exact finite arithmetic and coset identities used to detect faulty reductions. They do not mechanically verify the topological proofs or constitute a search over all 3-manifolds. A separate audit is required before any publication claim.

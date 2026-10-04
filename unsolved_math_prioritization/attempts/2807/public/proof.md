# Five proof routes for KP-3.9

## Pass 1. Abelian quotients and nonseparating surfaces

Write Ĝ for the profinite completion, and b₁(G) for dim_Q Hom(G,Q). All groups in the algebraic statements are finitely generated; isomorphisms of completions are topological.

### Lemma 1. Abelianization is detected

If Ĝ ≅ Ĥ, then G_ab ≅ H_ab.

**Proof.** Every homomorphism from G to a finite group extends uniquely to Ĝ. Thus the numbers of homomorphisms to C_(p^k) agree for G and H, for every prime p and k ≥ 1. Write the p-primary part of the torsion of G_ab as ⊕_i C_(p^e_i), and let r be its free rank. Then

log_p |Hom(G,C_(p^k))| = kr + Σ_i min(k,e_i).

Put the value at k=0 equal to zero. Its first difference at k is r + #{i:e_i ≥ k}. The eventual value of this nonincreasing difference sequence determines r; the difference between adjacent first differences determines the multiplicity of the exponent k. Doing this for every p determines all of the finite torsion group. The fundamental theorem of finitely generated abelian groups proves the claim. □

### Lemma 2. Finite-index Betti profiles are detected

An isomorphism Ĝ ≅ Ĥ matches finite-index subgroups with the same index, and corresponding subgroups have equal b₁.

**Proof.** Finite-index subgroups L ≤ G correspond to open subgroups L̄ ≤ Ĝ by closure and intersection. The topology induced on L is its full profinite topology: if K has finite index in L, then it has finite index in G, and the core of K in G is finite-index normal in G and contained in K. Therefore L̂ ≅ L̄. Apply the isomorphism of completions, intersect its image with H, and apply Lemma 1 to the corresponding subgroup. □

### Lemma 3. Positive b₁ gives Haken-ness in the closed irreducible case

Let M be a closed, connected, orientable, irreducible 3-manifold with b₁(M)>0. Then M is Haken.

**Proof.** A nonzero integral class in H¹(M;Z) has Poincaré dual represented by an oriented embedded surface: use a map M→S¹ representing the class and a regular level set. Compress that surface along compressing disks while preserving its homology class, and discard sphere components. Compression terminates: a nonseparating compression decreases total genus; a separating compression splits a positive genus into smaller positive genera (sphere components can be discarded), so a lexicographic complexity given first by total genus and then by the sum of squares of component genera decreases. Spheres bound balls by irreducibility and contribute zero to H₂. Thus some nonspherical component remains, since the original homology class was nonzero. At termination it has no compressing disk; the Loop Theorem gives injectivity of its fundamental group. Closed M has no boundary-parallel obstruction. This is the required two-sided incompressible surface. □

**Attempt and exact gap.** These lemmas detect nonseparating surfaces, but H₂(M;Z)=0 in the rational-homology-sphere case. Every connected, orientable embedded surface in that case separates. Hence the homology mechanism loses the very surfaces required by the residual problem. Positive Betti number in a finite cover does not supply an embedded surface downstairs.

## Pass 2. Dihedral quotients and signed double covers

Let D∞ = ⟨r,s | s²=1, srs⁻¹=r⁻¹⟩, with ⟨r⟩ ≅ Z.

### Theorem 4. An index-two Betti criterion

For a finitely generated group G, the following are equivalent:

(a) G admits an epimorphism to D∞.

(b) Some subgroup H of index two satisfies b₁(H)>b₁(G).

In particular, (a) is invariant under isomorphism of profinite completions.

**Proof.** Fix an index-two H, choose t∈G\H, and let T act on V=Hom(H,Q) by (Tψ)(h)=ψ(tht⁻¹). Since t²∈H and inner automorphisms act trivially on Hom(H,Q), T²=1. Over Q, V=V⁺⊕V⁻.

Restriction identifies Hom(G,Q) with V⁺. Injectivity follows because a homomorphism vanishing on H factors through finite G/H. For surjectivity, an invariant ψ∈V⁺ extends by sending t to ψ(t²)/2. The relations t h t⁻¹∈H and t²∈H are respected: invariance verifies the first, and the chosen value verifies the second. Equivalently, use the presentation of G as an extension of H with these conjugation and square relations. Thus dim V⁺=b₁(G), and b₁(H)>b₁(G) exactly when V⁻≠0.

Suppose (b). Because H is finitely generated, clear denominators in a nonzero element of V⁻ and divide by the positive generator of its image to obtain a surjection φ:H→Z with φ(tht⁻¹)=−φ(h). The element t² is fixed by conjugation by t, so φ(t²)=−φ(t²), and consequently φ(t²)=0. Define ρ(h)=r^φ(h) and ρ(t)=s. The conjugation and square relations are now exactly the defining relations of D∞; thus ρ is a homomorphism. It is onto because φ is onto and s lies in its image. This proves (a).

Conversely, given an epimorphism ρ:G→D∞, let H=ρ⁻¹(⟨r⟩). The exponent of r defines a nonzero element of V⁻. Hence dim V⁻>0 and (b) follows.

Finally, Lemma 2 preserves index-two subgroups and their first Betti numbers, while Lemma 1 preserves b₁(G). Therefore (b), and hence (a), is profinite. □

### Corollary 5. A special affirmative Haken criterion

Let M and N be closed, orientable, irreducible 3-manifolds with isomorphic profinite completions. If π₁(M) has a D∞ quotient, N is Haken.

**Proof.** Theorem 4 gives such a quotient of π₁(N). Pull back the usual action of D∞ on a subdivided line; it has no global fixed vertex and has no edge inversions. The classical splitting-to-surface theorem for 3-manifold groups gives a nonempty essential surface. Here we use Garden–Tillmann, Proposition 26, recording the Culler–Shalen/Epstein/Waldhausen result, rather than claiming to prove that topology theorem. Irreducibility excludes essential sphere components. □

### A topological control outside the hyperbolic residual case

Take two trefoil exteriors E₁,E₂ and glue their boundary tori by an orientation-reversing map exchanging meridian and longitude. Each exterior is irreducible with incompressible boundary (standard facts for a nontrivial knot exterior). Gluing along an incompressible torus preserves irreducibility, by the usual innermost-circle argument for spheres. The amalgam normal-form theorem preserves injectivity of the torus group, so the glued torus is essential. Thus the resulting closed manifold M is Haken.

But H₁(E_i;Z)=Z, generated by the meridian μ_i, while the preferred longitude λ_i is zero in H₁(E_i;Z). Under the meridian-longitude exchange, the Mayer–Vietoris map H₁(T²;Z)→H₁(E₁;Z)⊕H₁(E₂;Z) has matrix diag(1,−1) in suitable bases. It is onto. The subsequent H₀ map is injective because the pieces and torus are connected. Hence H₁(M;Z)=0. This Haken integral homology sphere has no D∞ quotient, since D∞_ab=C₂×C₂. Its essential gluing torus makes it nonhyperbolic; it is a counterexample to the proposed necessary dihedral criterion, not to KP-3.9.

**Attempt and exact gap.** This route converts signed-cover information into double-cover tests for a fixed presentation, and detects the quotient without a general discrete lift of a profinite map. The control just proved shows that Haken-ness does not in general imply the dihedral condition. No argument here forces an arbitrary separating quasi-Fuchsian surface in the hyperbolic residual case to produce a double-cover Betti jump.

## Pass 3. Finite-image representations and character curves

### Lemma 6. Characters over algebraic closures of finite fields

Fix p, let k=overline(F_p), and let G and H be finitely presented groups with Ĝ≅Ĥ. Then their sets of SL₂(k)-characters have the same cardinality. In particular, one character variety has positive dimension if and only if the other does.

**Proof.** Each representation ρ:G→SL₂(k) has finite image: finitely many matrix entries of finitely many generators all belong to one finite field F_(p^a). Hence ρ uniquely extends to a continuous map Ĝ→SL₂(F_(p^a)). Precomposition by a fixed isomorphism Ĥ→Ĝ and restriction to H transports ρ. The inverse isomorphism supplies the inverse construction. The image subgroup is unchanged, since the dense subgroup's image in a finite discrete group is the full image.

We must descend to characters rather than merely count representations. If ρ₁ and ρ₂ have the same trace on every element of G, their extended trace functions agree on dense G and hence on Ĝ; both take values in a common finite field, so continuity proves equality everywhere. Their transported restrictions have the same character. Applying the inverse isomorphism proves the converse. This gives a well-defined bijection on characters, not merely on raw representations or conjugacy classes.

The character variety of a finitely presented group is an affine variety of finite type over k. Its k-points are its characters. A zero-dimensional affine variety of finite type over an algebraically closed field has finitely many points, whereas a positive-dimensional one has infinitely many (for example by Noether normalization). Thus the set bijection detects whether the dimension is positive. It is not asserted to be an algebraic isomorphism or to preserve the actual dimension. □

**Field restriction.** A finitely generated subgroup of SL₂(F) need not be finite for an arbitrary algebraically closed field F of characteristic p: diag(t,t⁻¹) over overline(F_p(t)) has infinite order. The finite-image argument above intentionally uses overline(F_p). Existence of a curve after another algebraically closed extension of F_p can instead be handled using invariance of dimension under extension of the base field of the finite-type character variety. No false finite-image claim for transcendental fields is used.

**Topological application.** Garden–Tillmann Theorem 24 and Proposition 26 associate a nontrivial ordinary tree splitting and an essential surface to a character curve. Therefore Lemma 6 gives another sufficient Haken-transfer mechanism. We use those published theorems as external inputs.

**Attempt and exact gap.** Counting finite representations is profinite information; a character curve is enough for an essential surface. The missing converse would say that every relevant Haken manifold has such a curve in some characteristic, and that converse is not established here. The literature reports explicit failures. Nonintegral isolated characters require a different mechanism. A finite computation over F₂,F₃,F₅ cannot decide whether curves exist over every extension field or in every characteristic.

## Pass 4. Arithmetic traces and actions on valued trees

### Lemma 7. A trace obstruction to a fixed vertex

Let K be a discretely valued field with valuation ring O, and ρ:G→SL₂(K) a representation. If some trace tr(ρ(g)) has negative valuation, the action on the Bruhat–Tits tree has no global fixed vertex.

**Proof.** Vertices are homothety classes of O-lattices in K². A subgroup of SL₂(K) fixing one vertex preserves an actual representative lattice: if a determinant-one matrix carries a lattice to a scalar multiple, determinant valuation forces the scalar to have valuation zero, so that scalar multiple is the same lattice. In an O-basis of this lattice, each such matrix has entries in O, and its trace is in O. Trace is conjugation-invariant, contradicting the proposed negative valuation. □

In the 3-manifold setting, a nontrivial tree action leads to an essential surface by the splitting-to-surface input already cited. Transporting nonintegrality itself across profinite completions is subtler: a nonintegral p-adic representation does not have compact image and cannot simply be extended continuously to a profinite group. Cheetham-West–Lê handle a finite-character case with bounded-representation counting; this attempt does not replace that argument by the invalid direct extension.

### Exact arithmetic control

Let f(x)=2x⁴−17x³+46x²−40x+8. Its reduction modulo 7 is irreducible: `controls.py` verifies gcd(f,x⁴⁹−x)=1 and x²⁴⁰¹≡x mod f after normalizing the leading coefficient. The degree-four finite-field irreducibility criterion proves irreducibility over F₇ and hence over Q, since f is primitive and its leading coefficient remains nonzero modulo 7. The monic minimal polynomial over Q of any root is f/2, which has a nonintegral coefficient. An algebraic integer has an integral monic minimal polynomial. Therefore every root of f is nonintegral.

Cheetham-West–Lê Example 5.4 cites this polynomial for a squared trace. If x=t² is nonintegral then t is also nonintegral, since algebraic integers form a ring. The calculation above verifies this arithmetic implication only. It does not recover the manifold representation or verify the claimed trace identity from a triangulation.

**Attempt and exact gap.** This mechanism reaches some Haken manifolds with isolated characters, bypassing Pass 3's limitation. It does not show that every Haken hyperbolic rational homology sphere has a nonintegral SL₂ trace, nor does it transfer an arbitrary unbounded representation by completion. No full result follows.

## Pass 5. Surface subgroup separability and the discrete-lifting obstruction

Cutting a closed Haken rational homology sphere along a connected essential orientable surface gives a separating amalgamated splitting. For a quasi-Fuchsian surface, separability suggests finite quotient models of that splitting and maps to virtually free amalgams. The tempting step is to transfer the completed splitting to N̂ and simply intersect its edge or vertex groups with π₁(N). The following exact test shows why density alone cannot justify such a step.

### Lemma 8. A direct summand can miss the dense discrete lattice

Let A=Ẑ=∏_p Z_p. Define α∈A to have 2-adic coordinate 0 and p-adic coordinate 1 for every odd p. Let K={(x,αx):x∈A}≤A². Then K is a closed direct summand, isomorphic to Ẑ, but K∩Z²={(0,0)} under the ordinary diagonal embedding of Z² into A².

**Proof.** K is the graph of a continuous map between compact Hausdorff groups, so it is closed. Projection to the first coordinate is an isomorphism K→A, and K⊕({0}×A)=A². If an integer pair (m,n) lies in K, the 2-adic coordinate gives n=0 in Z₂. Since Z→Z₂ is injective, n=0 as an integer. Any odd p-adic coordinate then gives m=0 in Z_p, so m=0 as an integer. □

The automorphism (x,y)↦(x,y+αx) of A² carries the closure of Z×{0} to K. Thus even a profinite automorphism may carry the closure of a discrete subgroup to a closed subgroup whose intersection with the other dense discrete copy is trivial. This example is abelian. It is not a counterexample to KP-3.9, and it does not contradict the additional homology regularity known for hyperbolic 3-manifolds.

**Attempt and exact gap.** Transferred actions on profinite trees are not automatically actions on ordinary simplicial trees. The required extra statement must reconstruct enough discrete splitting data, or prove that the transported image in a suitable free profinite quotient is a discrete free/virtually free group. Cheetham-West–Lê Question 6.1 isolates one such unproved freeness assertion. Replacing the original question by that assertion without proving it is a blocked route, not a solution. General residually finite groups exhibit failures of property FA detection, so no unrestricted group-theoretic transfer theorem can be silently assumed.

## End-of-budget conclusion

Passes 1–4 rigorously establish limited detection mechanisms; Pass 5 proves a precise obstruction to an invalid general inference. None proves that every embedded separating incompressible surface can be detected or reconstructed profinitely. No concrete pair of hyperbolic 3-manifold groups with isomorphic profinite completions and different Haken behavior is found. The exact target remains unresolved in this attempt after five substantive passes.

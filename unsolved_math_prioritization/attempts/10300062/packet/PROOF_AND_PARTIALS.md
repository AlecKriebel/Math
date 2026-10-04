# Immersed objects: a coherent-approximation obstruction

Problem identifier: 10300062 / AMR-102-0062; queue rank 670.

## Status and exact scope

**NO UNQUALIFIED RESOLUTION OF CALEGARI QUESTION 14.2 IS CLAIMED.**

The source is Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, arXiv:math/0209081v1, Question 14.2, printed page 31. It asks whether each pointed leaf of a taut foliation is a compact-set limit of images of expanding intrinsic balls in compact immersed incompressible surfaces. The question itself does not require a hyperbolic ambient manifold. The immediately following doubling construction indicates that the approximating surfaces are closed in the closed-manifold setting. The source does not supply a formal topology for the stated convergence of images.

We prove a complete obstruction for **coherent compact-domain approximation**, defined below. In particular it disproves the version using ordinary marked pointed convergence of immersed surfaces. However, convergence of image sets alone does not imply this coherence, even for closed incompressible immersions. Section 5 supplies an exact control demonstrating that distinction. Consequently this packet does not promote the obstruction into an unconditional solution of the source's imprecisely specified convergence question. It also does not settle a version restricted to hyperbolic 3-manifolds.

All surfaces and manifolds in the construction are smooth. A closed immersed essential surface means a compact surface without boundary whose immersion induces an injection on fundamental groups. The main obstruction also allows nonorientable approximating surfaces with that property. We do not silently substitute disk-incompressibility for this convention.

## 1. Minimal coherence needed for the obstruction

Let j:L -> M be a leaf inclusion into a compact Riemannian manifold. Say that maps phi_i:S_i -> M coherently approximate j on compact domains if, for every compact connected subsurface K of L, eventually there are continuous maps u_i:K -> S_i with phi_i u_i converging uniformly to j|K. Requiring u_i to be embeddings, or requiring C^1 or smooth convergence, only strengthens this condition. In the expanding-ball version one further asks that the image of u_i lie in the specified expanding ball. Our obstruction does not need that additional requirement.

### Lemma 1: compact-domain group obstruction

Suppose j|K is pi_1-injective. If phi_i u_i converges uniformly to j|K, then for all sufficiently large i the map (u_i)_*:pi_1(K) -> pi_1(S_i) is injective.

**Proof.** Choose epsilon smaller than the injectivity radius of M. Once the two maps have pointwise distance less than epsilon, the unique short geodesics between their values give a continuous homotopy. Thus their induced homomorphisms agree up to the basepoint conjugation determined by this homotopy. The composition (phi_i)_*(u_i)_* is therefore injective. A composition can be injective only if its first-applied map (u_i)_* is injective. This proof does not require phi_i itself to be injective on pi_1. QED.

The same argument proves a uniform version: there exists epsilon_K>0 such that no map through a surface group lacking a copy of pi_1(K) can be epsilon_K-close to j|K.

## 2. Circle bundles with nonzero Euler number

### Lemma 2: no closed negative-Euler-characteristic surface subgroup

Let p:E -> B be an oriented circle bundle over a closed oriented surface B of genus g>=2. If its Euler number e is nonzero, then pi_1(E) contains no subgroup isomorphic to the fundamental group of a closed orientable surface of genus s>=2.

**Proof.** Since pi_2(B)=0, the homotopy sequence of the bundle gives

1 -> Z -> G=pi_1(E) -> Gamma_g=pi_1(B) -> 1.

The fiber subgroup Z is central because the circle bundle is oriented. Suppose H<=G were a closed orientable genus-s surface group, s>=2. Such a group has trivial center. For example, realize it as a cocompact torsion-free Fuchsian group: an element centralizing two hyperbolic elements with distinct endpoint pairs must be the identity. Consequently H intersects the central fiber subgroup trivially. Projection embeds H as a subgroup J of Gamma_g.

Let B_J -> B be the connected covering associated with J. This is an aspherical oriented surface, so its second integral homology equals the second group homology of J. Since J is a closed genus-s surface group, this group is Z. An infinite-sheeted cover B_J would be a noncompact connected surface and would have H_2(B_J;Z)=0. Therefore the covering is finite-sheeted, of some positive degree d.

Pull back E to B_J. Its Euler number is d e, which is nonzero. But projection H -> J is an isomorphism, so its inverse followed by H<=G is a splitting of the pulled-back central extension. A split oriented-circle extension over the aspherical surface B_J has zero Euler class, a contradiction.

For completeness, the last implication can be seen without assuming it as a slogan. A splitting represents loops in E_J over a generating set of pi_1(B_J), with the surface relator null-homotopic in E_J. Extending over the relator produces a map s:B_J -> E_J for which p_J s induces the identity on pi_1. As B_J is aspherical, p_J s is homotopic to the identity. The map s is a lift of p_J s, hence gives a section of the pullback of E_J by p_J s. That pullback has Euler class (p_J s)^*e(E_J)=e(E_J), but a bundle with a section has Euler class zero. QED.

### Corollary 3: the compact surface groups available in E

Every connected closed surface whose fundamental group injects into G has virtually abelian fundamental group.

**Proof.** An orientable surface of genus >=2 is excluded by Lemma 2. A nonorientable closed surface of genus k>=3 has an orientable double cover of genus k-1>=2, also excluded. The remaining closed surfaces are the sphere, projective plane, torus and Klein bottle, and their groups are virtually abelian. Some of these cannot inject into G, but including them does not weaken the conclusion. QED.

This proof automatically applies to every finite cover of E: its fundamental group is a subgroup of G. Passing to a finite ambient cover therefore cannot supply a missing closed negative-Euler-characteristic surface subgroup.

## 3. A smooth taut suspension with a free-group patch in every leaf

Let B_2 be a closed oriented hyperbolic surface of genus 2 and let Gamma_2 act on the ideal boundary circle of its universal hyperbolic plane. Denote this faithful Fuchsian boundary action by rho_0:Gamma_2 -> Diff^+(S^1).

The suspension bundle

E_0 = (universal_cover(B_2) x S^1)/Gamma_2

is the oriented unit tangent circle bundle of B_2. Indeed, send (x,xi) to the unit tangent vector at x directed toward the ideal endpoint xi; this is a smooth equivariant fiberwise diffeomorphism. Therefore the Euler number of E_0 is chi(B_2)=-2. Reversing the fiber orientation changes the sign but not the nonvanishing used below. The Fuchsian-boundary identification and Euler computation are also explicitly discussed in Banagl's *Isometric group actions and the cohomology of flat fiber bundles*, Section 6, printed pp.17–18.

Write the closed genus-3 surface B_3 as a once-punctured torus A attached along its boundary to a genus-2 surface with one boundary component. Let f:B_3 -> B_2 be a degree-one pinch map collapsing the handle A. In standard surface-group generators it induces

q:Gamma_3 -> Gamma_2,

q(a_1)=q(b_1)=1, q(a_2)=a'_1, q(b_2)=b'_1, q(a_3)=a'_2, q(b_3)=b'_2.

This respects the surface relator. Define rho=rho_0 q and form the smooth suspension

M = (universal_cover(B_3) x S^1)/Gamma_3.

The diagonal action is free and properly discontinuous because it is so on the first factor. Its quotient is a closed smooth oriented circle bundle p:M -> B_3. It has Euler number -2: the flat bundle is the pullback of E_0 by f, and the Euler number multiplies by deg(f)=1.

Horizontal slices define a smooth cooriented codimension-one foliation F. For t in S^1 let H_t be its stabilizer under rho. Its leaf is naturally universal_cover(B_3)/H_t, and projection to B_3 is the covering associated with H_t. In particular every leaf projects onto B_3. A single circle fiber is transverse to F and meets every leaf, so F is taut in exactly the source's definition.

Since rho kills pi_1(A), the restriction of each leaf-covering over A has a component mapping homeomorphically onto A. Thus every leaf contains a compact once-punctured-torus patch K with pi_1(K)=F_2. The map pi_1(K) -> pi_1(M) is injective, as its composition with p_* is the inclusion pi_1(A) -> Gamma_3.

One can verify the latter injection directly. In the presentation

Gamma_3 = <a_1,b_1,a_2,b_2,a_3,b_3 | [a_1,b_1][a_2,b_2][a_3,b_3]=1>,

send (a_1,b_1,a_2,b_2,a_3,b_3) to (x,y,y,x,1,1) in the free group F(x,y). The relator becomes [x,y][y,x]=1. This homomorphism is a retraction on the subgroup generated by a_1,b_1, proving that subgroup is free of rank 2. It also detects the two horizontal lifts in pi_1(M), since killing the central fiber gives the stated projection to Gamma_3.

The foliation has no compact leaves: a compact leaf would cover B_3 with finite degree and yield a closed genus>=2 surface subgroup, contradicting Lemma 2. Its leaves are complete for the induced metric, as is true of smooth leaves of a foliation of a compact Riemannian manifold; equivalently a bounded-speed leafwise path cannot terminate in finite time because it extends in a finite family of foliation charts. Only compactness of K, rather than completeness, is needed for the group obstruction.

## 4. Complete negative theorem for coherent approximation

### Theorem 4

There exists a closed smooth oriented 3-manifold M with a smooth cooriented taut foliation F such that no leaf can be coherently approximated on compact domains by closed pi_1-injective immersed surfaces. More strongly, each leaf contains a compact subsurface K and has an epsilon_K>0 for which no continuous map K -> S through any such closed essential surface S -> M is uniformly epsilon_K-close to the leaf inclusion.

**Proof.** Use the genus-3 circle bundle and suspension in Section 3. The leaf patch K has pi_1(K)=F_2 and includes injectively in pi_1(M). Corollary 3 says every closed pi_1-injective surface S -> M has virtually abelian fundamental group. Every subgroup of a virtually abelian group is virtually abelian, whereas F_2 is not. To check the last fact, any finite-index subgroup of F(x,y) contains positive powers of both x and y, and those powers do not commute by free-word reduction. Thus no homomorphism F_2 -> pi_1(S) can be injective. Lemma 1 now rules out the required uniformly close maps. QED.

The theorem is not vacuous because M does have compact essential surfaces: the preimage of an essential embedded base curve is a vertical torus. The restricted oriented circle bundle over that curve is trivial, and its group is the preimage of the corresponding infinite cyclic subgroup, namely Z^2. It injects into pi_1(M). Thus the obstruction is to approximating the specified leaf patches, not to the bare existence of immersed essential surfaces.

The example is Seifert-fibered, not hyperbolic. It does not answer a hyperbolic-only reformulation. No novelty claim is made: the individual ingredients are classical, and a bounded search did not establish priority for this combination.

## 5. Exact countercontrol: image convergence does not imply coherence

Work in the flat 3-torus with angular coordinates of period 2 pi. Let L be the compact horizontal leaf z=0 of the product taut foliation. For every integer n>=1 take the pi_1-injective immersion

phi_n:T^2 -> T^3, phi_n(x,y)=(n x,y,0),

with the pullback metric n^2 dx^2+dy^2 and basepoint (0,0). For any point of L choose its angular representatives X,Y in [-pi,pi]. The domain point (X/n,Y) maps to it and has distance at most pi sqrt(2) from the basepoint. Consequently, for r_n=n and n>=5, the image of the intrinsic r_n-ball is **exactly L**. These images converge to the target leaf in the strongest possible setwise sense.

Nevertheless there is no continuous u_n:L -> T^2 for which phi_n u_n is uniformly close enough to the identity inclusion to be homotopic to it when n>1. On fundamental groups the first two coordinates of such a homotopy would give

diag(n,1) U = I_2

for an integral 2x2 matrix U. The top-left entry would require n U_11=1, impossible. This remains an obstruction even without asking u_n to land in the ball.

This is a control for the logical inference, not a counterexample to the original approximation assertion: the compact leaf L itself is of course a valid constant approximating sequence. Its purpose is to show rigorously why Theorem 4 cannot automatically be applied to a formulation that specifies only convergence of images.

## 6. Positive special case: irrational linear planes in T^3

Let v=(1,sqrt(2),sqrt(3)), let P=v-perp, and foliate the flat unit 3-torus by translates of P. The three coordinates of v are linearly independent over Q, so P intersects Z^3 only in zero. Each leaf is an intrinsically Euclidean plane. A circle in any integer direction transverse to P meets every leaf, so this foliation is taut.

Choose m_i -> infinity and integral normals

w_i=(m_i, floor(sqrt(2) m_i), floor(sqrt(3) m_i)), P_i=w_i-perp.

The planes P_i descend to embedded essential flat tori T_i=P_i/(P_i intersect Z^3), translated to pass through the chosen basepoint p. Put ell_i=min{|z|:0!=z in P_i intersect Z^3}. Then ell_i -> infinity. Otherwise there would be a bounded sequence of nonzero integer vectors z_i perpendicular to w_i. After taking a subsequence z_i would be a fixed nonzero z, and division by m_i followed by passage to the limit would give v dot z=0, contrary to the rational independence.

Choose rotations R_i with R_i(P)=P_i and R_i -> identity. Let delta_i=||R_i-identity||, and choose

r_i=min(ell_i/4, delta_i^(-1/2), i),

omitting the middle bound when delta_i=0. All bounds tend to infinity, and delta_i r_i ->0. The intrinsic r_i-ball in T_i lifts isometrically to the Euclidean disk of radius r_i in P_i, since r_i<ell_i/2. The maps x -> p+R_i x (mod Z^3) identify those disks with disks in the leaf up to uniform ambient error at most delta_i r_i, with first derivatives also tending to the leaf derivatives. Hence the required coherent pointed approximation exists for these plane leaves.

This is a proof for one concrete class, not evidence for arbitrary taut foliations. The integer checks in verify.py illustrate the lattice escape used here; the finite checks are not the proof that ell_i tends to infinity.

## 7. Two further rigorous limitations on positive routes

### 7.1 Doubling a leaf patch creates a kernel

Let A be a once-punctured torus, and double it along the boundary to form a genus-2 surface D(A). The fold D(A) -> A maps both halves identically. With generators a_+,b_+,a_-,b_-, its group has the relation [a_+,b_+]=[a_-,b_-]. The word a_+ a_-^(-1) maps to 1 under the fold. It is nontrivial in pi_1(D(A)): its image in H_1(D(A);Z)=Z^4 is (1,0,-1,0), which is nonzero. Thus doubling alone cannot preserve incompressibility. Mapping the double into a product neighborhood of A by two nearby sheets and thin boundary annuli has the same folded homotopy class and the same defect. No argument here shows that compression can remove the defect while retaining the prescribed leaf patch.

### 7.2 A current estimate does not control a distant cap

Let omega be a closed 2-form on a compact oriented Riemannian M. Suppose omega is positive on an oriented plane field. By compactness there are a neighborhood of that plane field and a c>0 such that omega evaluates to at least c on every positively oriented unit tangent plane in the neighborhood. Let C>0 bound the comass of omega. For an oriented closed immersed surface S which is null-homologous over R, divide it into a good region whose tangent planes are in that neighborhood and the remaining bad region. Then

0=integral_S omega >= c Area(good) - C Area(bad),

so Area(bad) >= (c/C) Area(good).

This forbids a null-homologous surface from being globally tangent-close with negligible exceptional area. It does not prohibit approximation on expanding pointed balls: a closing region beyond the controlled balls may have arbitrarily large area. In particular a global-current obstruction cannot simply be transferred to the source's local pointed problem.

### 7.3 Rational branch weights require a missing transverse measure

For a finite branched surface, transverse weights satisfy homogeneous linear matching equations A w=0 with integer coefficients. If there is a strictly positive real solution, rational solutions sufficiently close to it remain positive: choose a rational basis of the nullspace by row reduction and approximate the basis coefficients by rationals. Clearing denominators then gives positive integral weights. This familiar mechanism by itself says nothing about whether the resulting closed carried surface is incompressible or approximates the chosen leaf with controlled topology.

More fundamentally, it cannot justify beginning with a transverse invariant measure on every taut foliation. The suspension in Section 3 has no nonzero locally finite transverse invariant measure. A complete circle fiber would restrict such a measure to a finite nonzero probability measure invariant under rho(Gamma_3)=rho_0(Gamma_2). For one hyperbolic boundary transformation, an invariant finite measure is supported on its two fixed points: each of the two complementary intervals decomposes into disjoint iterates of a half-open fundamental interval, whose mass must be zero by invariance and finiteness. Choose two hyperbolic elements with disjoint fixed-point pairs in the non-elementary cocompact Fuchsian group. An invariant probability would have to be supported on the empty intersection of those pairs, a contradiction.

Thus tautness does not supply the starting measure for global rational-weight approximation. This does not refute local patch approximation by surfaces whose uncontrolled parts depart from the foliation; such a relative closing construction remains an unproved extra step.

## 8. Remaining gap

The decisive unresolved bridge is a formal source-compatible convergence notion. If the intended convergence entails the compact-domain coherence in Section 1, Theorem 4 supplies a negative answer in the stated unrestricted ambient class. If it allows limits of images without coherent lifts of leaf loops, Section 5 shows that this proof does not apply. Neither a general construction nor a counterexample for that weaker interpretation has been proved here. Independently, no proof or counterexample is supplied for a hyperbolic-only version.

The source's global-angle remark, surface-subgroup existence in the hyperbolic case, separability, and the elementary doubling construction do not fill this bridge. This is why the recommended campaign disposition is an unresolved attempt with precisely scoped partial results, pending an independent audit rather than a solved claim.

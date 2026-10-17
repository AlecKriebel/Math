# Movability for finite-component one-dimensional isolated invariant compacta

Problem 30003527 / OWR-15575-006, queue row 1767. Authored 13 October 2026 during the fifth and final shared substantive pass. This is a restricted theorem, not a resolution of the unrestricted invariant-enlargement problem. No novelty claim is made. The proof is supplied for independent verification.

## Theorem and scope

**Theorem.** Let K be an isolated invariant compactum for a continuous full flow on R³. If K has finitely many connected components and covering dimension at most one, then K is movable.

There is no finite-rank assumption on its first Čech cohomology. In particular the theorem includes the isolated planar Hawaiian earring already constructed in pass 4. For this subclass, the original enlargement question has the answer B=K in every prescribed neighborhood.

The proof does not claim that arbitrary manifold blocks are handlebodies. It first proves an actual fundamental-group surjectivity statement for neighborhoods inside suitably refined blocks. It then constructs a finite-graph factorization of a neighborhood inclusion and lifts that graph into each target neighborhood. An epimorphism of fundamental groups is used only for the graph, where lifting finitely many loops supplies all the required data; it is not treated as a homotopy section of a three-manifold inclusion.

Two hypotheses remain real restrictions: infinitely many components are not covered, and the order-two cover argument uses dimension at most one. General nonisolated compact invariant sets are not reduced to isolated ones.

## 1. Accepted block input

The independently accepted pass-4 finite-cut theorem supplies arbitrarily small tame manifold isolating blocks N of K for which

Ȟ⁰(N,K;F₂)=Ȟ¹(N,K;F₂)=0.

The entry surface E=Nⁱ and its forward-stable trace L=n⁺ satisfy the same relative vanishing. This follows from the actual disk/strip shaving construction and the relative block–entry isomorphism. Neither vanishing is being inferred merely from a split map of absolute cohomology.

Because H⁰(N)→Ȟ⁰(K) is an isomorphism, each component of N contains exactly one connected component of K. It suffices to work with one such component, so from now on N and K are connected. At the end the finite number of components are treated in disjoint blocks. The empty compactum is harmless and can be omitted.

Write D=N⁺, the points whose forward orbit stays in N forever. Standard block coordinates give:

1. D is compact, positively invariant, and φ_t(D) decreases to K as t tends to infinity.
2. D∩∂N=L⊂Int E.
3. Near L there is a uniform initial flow collar: for a compact surface neighborhood P₀⊂Int E of L and sufficiently small a>0, (q,t)↦φ_t(q) is an embedding P₀×[0,2a]→N. Inside this collar, D is precisely the image of L×[0,2a].
4. Entry and exit times tⁱ:N→[-∞,0] and tᵒ:N→[0,∞] are continuous with their extended-real topologies.

These are continuous-flow block facts, not differentiability assertions. Their source is J. J. Sánchez-Gabites, *Using an invariant knot of a flow to find additional invariant structure*, arXiv:2403.18805v1, Definition 6, block-coordinate discussion, Proposition 5, and §5.4: https://arxiv.org/html/2403.18805v1 . The disk/strip refinement itself was proved separately in the preceding pass and audited there.

D is connected. Indeed, a separation D=D₀⊔D₁ into two nonempty compact open-and-closed pieces would be preserved by every forward orbit, since each orbit segment is connected. Every point of D has a nonempty omega-limit set in K, so K would meet both pieces. Their intersections would separate the connected K. The same argument also shows that each separated component of a small neighborhood of D which meets D must belong to its single connected neighborhood component.

## 2. Surface lemma: relative vanishing gives actual loop surjectivity

**Lemma 1.** Let E be a compact orientable surface and L⊂Int E compact. Suppose

Ȟ⁰(E,L;F₂)=Ȟ¹(E,L;F₂)=0.

Then each component Eα of E meets L in exactly one nonempty connected compactum. Moreover L has a cofinal family of compact surface neighborhoods P⊂Int E such that P∩Eα is connected and

π₁(P∩Eα)→π₁(Eα)

is surjective for every α. The same is true with Int P in place of P.

**Proof.** Degree-zero exactness shows that H⁰(E;F₂)→Ȟ⁰(L;F₂) is an isomorphism. Thus each Eα contains exactly one component of L. Here a compact Hausdorff space's components equal its quasicomponents, so two distinct components can be separated by a clopen partition; this identifies the asserted component information even for wild L.

Set M=E\L. Surface Alexander–Lefschetz duality gives

H₂(M,∂E;F₂)=H₁(M,∂E;F₂)=0.

Every component A of M is noncompact: a compact component, being both open and closed in the relevant Eα, would be all of Eα and disjoint from L. Its boundary is a union of components of ∂E, hence a finite union of circles.

If ∂A is empty, H₁(A;F₂)=0. A connected, noncompact orientable surface without boundary and with zero first mod-2 homology is an open disk. If ∂A is nonempty, the exact sequence of (A,∂A) shows that H₀(∂A)→H₀(A) is injective. Consequently ∂A has exactly one circle. The same sequence says H₁(∂A)→H₁(A) is onto. Capping this circle with a disk gives a connected noncompact boundaryless surface with H₁=0, hence an open disk again. Therefore A is a half-open annulus with its outer boundary retained, homeomorphic to S¹×[0,∞).

The elementary classification fact just used is the zero-genus, one-end case of classification of noncompact surfaces. For completeness, any positive genus gives a pair of nonzero first-homology classes, and two different ends can be separated by a compact subsurface whose boundary gives a nonzero mod-2 first-homology class. Zero H₁ therefore gives genus zero and exactly one end, yielding the plane. Equivalently one may use I. Richards, *On the classification of noncompact surfaces*, Transactions AMS 106 (1963), 259–269, Theorem 3 on p.268, DOI https://doi.org/10.1090/S0002-9947-1963-0143186-0 . The same capping argument appears in the proof of Theorem 16 of the block source, in its stronger relative-acyclic situation.

Now let Q be any neighborhood of L in E. The compact set E\Q is covered by components of M, so only finitely many of those components are needed to cover it. In every selected open-disk component choose a closed disk whose interior contains the relevant compact subset of E\Q. In every boundary-collar component choose a finite initial closed collar containing its part of E\Q; include a small initial collar in each remaining boundary component as well. Choose all these compact pieces disjoint from L. Removing the interiors of the disks and the initial boundary collars leaves a compact surface neighborhood P of L contained in Q and in Int E. Arbitrarily small enlargements of the removed pieces make the containment in Q strict if necessary.

Deleting finitely many disjoint interior disks and shaving boundary collars does not disconnect a connected surface. Conversely E is recovered from P by adding collars and filling boundary circles with disks. Seifert–van Kampen therefore gives the claimed epimorphism. Passing from P to Int P is a homotopy equivalence by its boundary collar. This proves cofinality and all component assertions. ∎

Only a finite number of holes is handled for each prescribed Q. There can be infinitely many open-disk components of E\L. No simultaneous infinite drilling in the three-dimensional block occurs in this proof.

## 3. A controlled neighborhood lemma at the entry boundary

**Lemma 2.** In the block setting of §1 and under the surface hypotheses of Lemma 1, let O_D be any relatively open neighborhood of D in N. There are relatively open sets V,A⊂N such that:

- D⊂V⊂O_D and V is path connected;
- E⊂A and A is a disjoint union of sets Aα, one for each component Eα, with Aα homotopy equivalent to Eα;
- Aα∩V is path connected and its inclusion into Aα is surjective on π₁;
- A∪V is a neighborhood of E∪D in N.

**Proof and construction.** Choose the uniform flow collar near L from §1, decreasing its thickness so that a neighborhood of L×[0,2a] in that collar lies in O_D. By Lemma 1 choose a compact surface neighborhood P of L, contained in Int P₀ and small enough that its full collar strip P×[0,2a] lies in O_D.

Use an inward collar of the tame boundary of N which agrees with the initial flow collar on a neighborhood of P. Such a collar is obtained by extending the already specified collar on this compact patch; this is the usual relative boundary-collar extension property. The entry surface has a boundary collar within ∂N as well. A small regular neighborhood A of E in N can consequently be chosen to deformation retract onto E and, over P₀, to be exactly the inward strip of height less than a/3. Outside a slightly larger patch of L it can be made disjoint from D. This last separation is possible because the rest of D, after removing its initial flow collar, is compact and disjoint from E.

More explicitly, let D_tail be D with the portion L×[0,a/2) of the initial collar removed. It is compact and disjoint from E. Take A thin enough that its closure misses D_tail. Choose a relatively open neighborhood V_tail of D_tail in O_D whose closure misses A. It may extend into the initial flow collar only at heights greater than a/3. Define

V₀ = V_tail ∪ φ(Int P×[0,a)).

The product is relatively open at height zero; its upper end is omitted. By choosing V_tail to contain the compact overlap L×[a/2,3a/4], V₀ is a relatively open neighborhood of D. Its intersection with A is exactly the product Int P×[0,a/3), component by component (or the same product with a positive varying upper height, which has the same deformation retraction). The collar and V_tail may be shrunk to achieve these descriptions, since the latter is separated from A.

Keep the path component V of V₀ containing D. The compact connected D lies in one component because N is locally path connected and V₀ is open. Every component of the product over P meets L and is connected, so none is lost by this restriction. Thus Aα∩V retracts to Int(P∩Eα), and Aα retracts to Eα. The induced map agrees with the surface inclusion up to these deformation retractions, hence is onto on π₁ by Lemma 1. All other assertions follow from construction. ∎

This lemma uses relative neighborhoods in N, so no point immediately outside an entry face is inadvertently included. It also separates off the stable tail instead of pretending that shaving the entry surface alone makes a neighborhood cofinal at K. Boundary collars and regular neighborhoods here are elementary for a tame three-manifold with the specified collared surface patch; no handlebody assumption is used.

## 4. The nonabelian bridge

**Proposition 3.** For the connected refined block N of §1, let W⊂Int N be any open neighborhood of K. Its component W₀ containing K satisfies

π₁(W₀,p)→π₁(N,p) is onto, for every p∈K.

**Proof.** First show that, for any relatively open O_D⊃D, the inclusion of its component containing D induces an epimorphism onto π₁(N). Apply Lemma 2. Adjoin the finitely many disjoint Aα to V one at a time. Each overlap is path connected and already surjects onto the fundamental group of the piece being added. Seifert–van Kampen says adjoining Aα adds no generators. Hence π₁(V)→π₁(A∪V) is onto.

The stopped backward flow is

F_t(x)=φ(max{-t,tⁱ(x)},x),  t≥0.

It is continuous, fixes E, starts at the identity, and stays in N. Its image is

F_t(N)=E∪{y∈N:φ([0,t],y)⊂N}.

For the equality, a point in the second set has precursor φ_t(y)∈N and is recovered by F_t; the reverse inclusion follows from the stopped trajectory segment. These are decreasing compact sets with intersection E∪D. Thus F_t(N)⊂A∪V for all sufficiently large t. Every based loop in N is homotopic, up to its basepoint track, into A∪V and then represented by a loop in V. If the original basepoint is p∈K, its track φ_{[-t,0]}(p) lies in K⊂V. Whiskering along this track makes the conclusion an epimorphism based at p, rather than merely a free-homotopy assertion. In particular π₁(O_D,p)→π₁(N,p) is onto in the component containing D.

Now choose T>0 so large that φ_T(D)⊂W₀. This is possible by compactness and the decreasing intersection K. Define a relatively open neighborhood of D in N by

O_D={x∈N:tᵒ(x)>T and φ_T(x)∈W₀}.

Exit-time continuity makes this set relatively open. Every x∈O_D stays in N for the entire interval [0,T], and φ_T(O_D)⊂W₀. Take a loop in O_D representing a prescribed element of π₁(N,p), which is possible by the previous paragraph. Apply the forward-flow homotopy φ_s, 0≤s≤T. It stays in N, and its endpoint is a loop in W₀ based at φ_T(p). The basepoint path φ_{[0,T]}(p) lies entirely in K⊂W₀, so whiskering yields a loop in W₀ based at p representing the original element in π₁(N,p). ∎

When E is empty, every point stays in N for all backward time, so N=N⁻, whereas D=N⁺=K. Take A empty and V to be the component containing K of any relatively open neighborhood of K in N. The stopped backward flow itself maps N into V for all sufficiently large times, and proves the same fundamental-group surjectivity without an entry collar or a van Kampen attachment. Thus Lemma 2 is unnecessary in this case. The construction of O_D in the nonempty-entry case explicitly addresses finite-time containment at entry boundary points.

Proposition 3 is stronger than a homological epimorphism and weaker than a homotopy section of W₀→N. The next step is precisely where dimension one is used to bridge that remaining difference.

## 5. Finite-graph approximation and the actual movability homotopy

**Lemma 4.** If a compact K⊂R³ has covering dimension at most one and N is a neighborhood of K, then some open neighborhood V of K has its inclusion V→N homotopic in N to a composite

V --f--> G --g--> N,

where G is a finite graph. When K and N are connected, G can be chosen connected and g(G) lies in that component of N.

**Proof.** Choose ε>0 such that the closed 4ε-neighborhood of K lies in Int N. Cover K by sufficiently small relatively open sets and refine to a finite cover of order at most two, using dim K≤1. Take a finite shrinking whose closures still cover K. Extend the shrunken sets to open subsets U_i of an ambient neighborhood of K, keeping diameter less than ε and arranging that no three meet there; the shrinking and compactness permit these properties to persist after a sufficiently small ambient extension. Discard sets not meeting K.

On their union V choose a partition of unity subordinate to {U_i}. It defines f:V→G into their finite nerve, which has dimension at most one. Pick x_i∈K in the corresponding original cover element and send the vertex i to x_i. Map every edge linearly between its endpoint choices. By choosing the cover and extensions with the stated small-diameter control, whenever x∈U_i the distance |x-x_i| is less than 2ε. Therefore g(f(x)) is within 2ε of x, and the straight-line homotopy from x to g(f(x)) stays within the 4ε-neighborhood of K, hence in N. Connected K gives a connected nerve after any irrelevant components are removed. ∎

This is a direct neighborhood construction; it does not replace ambient neighborhoods by imaginary embedded graph spines.

**Proof of the theorem.** First suppose K is connected. Given an arbitrary open O⊃K, choose a refined tame block N⊂O as in §1. Lemma 4 supplies an open V with K⊂V⊂Int N and an inclusion factorization up to homotopy through a finite connected graph G. Decrease V if necessary; the same factorization restricts.

Let W⊃K be any open neighborhood. Replace it by its component W₀ containing K inside W∩Int N. Proposition 3 gives an epimorphism π₁(W₀,p)→π₁(N,p). Consequently the map g:G→N is homotopic in N to a map g_W:G→W₀: choose a spanning tree of G, homotope it to the point p along paths in N, regard the remaining finitely many edges as based loops, choose a loop in W₀ representing each of their classes under the epimorphism, and use the corresponding based loop homotopies in N. The spanning-tree collapse and those homotopies give a genuine homotopy of the whole graph.

Compose with f and concatenate with the homotopy from Lemma 4. This is a homotopy H:V×[0,1]→N⊂O starting with inclusion and ending in W. The fixed V depends only on O, not on W. These are exactly the movability quantifiers.

For finitely many components K₁,…,K_c, use disjoint refined block components N_i⊂O. Apply the connected construction separately to obtain V_i. Their disjoint union V is an open neighborhood of K. For each W, the finitely many homotopies on V_i paste to a homotopy on V with image in O and endpoint in W. Thus K is movable. ∎

## 6. What has and has not been established

The new bridge is actual nonabelian loop surjectivity plus finite-graph factorization. The surface geometry matters: the abstract nonmovable collar/finite-quotient example from pass 3 has no reason to have the cofinal loop-surjective entry-surface neighborhoods used here.

No graph factorization is claimed for dimension two or three. No countably infinite pasting or uniform component argument is claimed for infinitely many components. No isolated enlargement of a general invariant A is constructed. In particular the identity flow still shows why an isolated-set theorem alone cannot settle the original target.

The unrestricted question therefore remains unresolved by this theorem. Its exact missing affirmative step remains an invariant movable enlargement in every prescribed neighborhood for arbitrary continuous flows and compact invariant sets; an opposing answer still needs one actual flow/A/U excluding every permitted B, with equality and disconnected B allowed.

## Sources and verification boundary

- Accepted finite-cut block refinement: preceding pass's authored theorem and independent acceptance. It supplies the actual block hypotheses; it is not a citation to an unproved infinite-rank extension of a published theorem.
- Sánchez-Gabites, *Using an invariant knot of a flow to find additional invariant structure*, arXiv:2403.18805v1: https://arxiv.org/html/2403.18805v1 . The relevant continuous block, coordinate, and stopped-flow arguments were inspected directly.
- Richards, *On the classification of noncompact surfaces*, Trans. AMS 106 (1963), 259–269, Theorem 3, p.268: https://doi.org/10.1090/S0002-9947-1963-0143186-0 . Public author-hosted scan: https://web.dm.unipi.it/benedett/Richards.pdf . The theorem is used only for the explicit open-disk and capped-collar classification in Lemma 1.
- Classical tools used in their ordinary forms: surface Alexander–Lefschetz duality, relative boundary-collar extension for tame manifolds, Seifert–van Kampen, and the defining order-two cover characterization of covering dimension at most one. The neighborhoods and homotopies to which they are applied are specified above.

No remote mutation, source-body publication, or external communication was made. This file is an authored proof candidate pending its independent acceptance; source retrievals do not constitute a sixth search pass.

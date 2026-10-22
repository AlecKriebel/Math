# Independent acceptance: one-dimensional isolated movability

Problem 30003527 / OWR-15575-006, queue row 1767. Audited 13 October 2026. This verifies the completed fifth-pass candidate and its one-paragraph correction; it is not an additional substantive problem-solving pass.

## Verdict and frozen inputs

**ACCEPTED for V2:** An isolated invariant compactum of a continuous full flow on R³ is movable if it has finitely many connected components and covering dimension at most one. No finite-rank assumption on first Čech cohomology is needed in this argument.

**The original version requires one local correction.** Its paragraph beginning “When E is empty” falsely identifies D with N and uses the wrong flow direction. The correct statement is N=N⁻ and D=K, with backward flow giving the required fundamental-group conclusion. V2 makes exactly this correction. No essential mathematical gap remains in V2; the detailed geometric checks below justify the potentially delicate steps rather than replacing them by a stronger unstated assumption.

This acceptance is restricted. It neither solves the general invariant-enlargement problem nor establishes movability for all isolated compacta. It makes no novelty claim.

Inputs, all checked byte-for-byte:

- Original candidate, `ONE_DIMENSIONAL_ISOLATED_MOVABILITY.md`: 19,249 bytes; SHA-256 `76e335e786c9a1f908bd671bd30110bfcb2cd991cc3352cccd9e1035207f5655`.
- Corrected candidate, `ONE_DIMENSIONAL_ISOLATED_MOVABILITY_V2.md`: 19,573 bytes; SHA-256 `5a325bc382d9094bd50e13b8a17fbdf8151b31e56dc58e3e32af9355f8a0ca1c`.
- Supplied correction, `EMPTY_ENTRY_CORRECTION.patch`: 1,593 bytes; SHA-256 `91ad5980bd093fccf4d0466e2a45963712308d2d9d39b64543cb6d49b1ded9b4`.
- Accepted preceding block audit, `AMBIENT_BLOCK_ACCEPTANCE.md`: 14,926 bytes; SHA-256 `b519ba9131089ad9732028d7e9e32cfa9e1a5a1bfd0ad3b9876a302aae56fe84`.

The two candidates were compared directly. Replacing the original exceptional-case paragraph by the supplied V2 paragraph reproduces the entire V2 file exactly. The original was not edited. No remote mutation was made.

## 1. Dependencies and block coordinates

The accepted finite-cut result is a genuine input, not a theorem reconstructed from absolute cohomological splitting. It supplies arbitrarily small tame manifold isolating blocks with relative degrees zero and one vanishing over F₂, and transfers those vanishing statements to the entry pair (E,L). This audit does not promote the published finite-cohomology handle theorem to an infinite-rank theorem.

The degree-zero relative exact sequence, together with degree-one relative vanishing, makes H⁰(N)→Ȟ⁰(K) an isomorphism. Because N has finitely many components and each compact component of K can be distinguished by clopen partitions, each component of N contains exactly one component of K. Components of K are invariant: every finite orbit segment is connected. Restricting to one component of N is therefore legitimate.

For D=N⁺, compactness follows by intersecting the closed conditions that an orbit remains in N for each bounded forward interval. Positive invariance gives the nesting of φ_t(D). Their intersection is K: a point in every φ_t(D) has a predecessor in D for every t, hence a full orbit in N; the converse follows from invariance of K.

The entry trace is L=D∩∂N and avoids the tangency and exit sets. Every point of L is a transverse entry point. The continuous-flow product chart gives an initial collar over a surface patch containing L. Compactness permits a uniform positive time and a slightly larger patch. Injectivity also follows directly: an equality φ_t(q)=φ_s(q′), with q,q′ on the entry patch and 0≤s<t in the permitted interval, would put q′ in the interior of N while q′ is on its boundary. This supplies an actual topological collar, not a differentiable assertion. A point φ_t(q) in this collar is forward trapped exactly when q is forward trapped, proving the claimed L×[0,2a] description of D there.

D is connected when K is connected. If D were the disjoint union of two nonempty compact clopen sets, every forward orbit would stay in its initial piece. Its nonempty omega-limit is contained in K and in that piece. K would consequently meet both pieces and be separated by them. This argument requires connectedness, not local connectedness, of K or D.

The relevant dynamical source was inspected directly: Sánchez-Gabites, [*Using an invariant knot of a flow to find additional invariant structure*, arXiv:2403.18805v1](https://arxiv.org/html/2403.18805v1), §2.3, Proposition 5, Definition 6, Proposition 7, and §5.4. These supply continuity of entry/exit times, the relative-pair comparison, transverse-entry charts, and the block neighborhood basis. The stopped-flow formula is also present in Proposition 5. The author's handle theorem has additional finite-cohomology hypotheses and is not the result being applied here.

## 2. Lemma 1: complement components and cofinal surface neighborhoods

The exact sequence gives an isomorphism H⁰(E;F₂)→Ȟ⁰(L;F₂). This proves both that every component Eα meets L and that its intersection with L is connected. For a compact Hausdorff space, a failure of this component assertion produces a finite nontrivial clopen partition and hence extra degree-zero classes. Local connectedness of L is unnecessary.

Surface duality gives H₂(E minus L,∂E;F₂)=H₁(E minus L,∂E;F₂)=0. The complement is a second-countable surface with boundary. Each of its components A is open in E and has manifold boundary consisting of whole components of ∂E. If A were compact, it would be closed as well as open in E, making it an entire component of E disjoint from L. Thus all such A are noncompact.

For an A without boundary, the displayed vanishing gives H₁(A;F₂)=0. A connected noncompact orientable boundaryless surface with this property is a plane: a handle gives nonzero first homology, and multiple ends give a nonzero separating-cycle class. For A with boundary, the pair exact sequence injects H₀(∂A) into H₀(A), so ∂A has one circle. It also makes H₁(∂A)→H₁(A) surjective. Capping that circle kills H₁ and leaves a noncompact boundaryless orientable surface, hence a plane. The original A is therefore a plane with an open disk removed, including its boundary circle, or equivalently a half-open annulus. The classification being used is precisely the genus-zero, one-end case, consistent with Richards, [*On the classification of noncompact surfaces*](https://web.dm.unipi.it/benedett/Richards.pdf), Theorem 3, p.268, inspected directly.

Let Q be an open neighborhood of L in E and F=E minus Q. Complementary components are open and cover the compact set F, so finitely many suffice. This really means only finitely many components meet F, since components are disjoint. For each selected A, F∩A is compact: its complement in F is a union of the other finitely many component intersections, hence open in F. This justifies the compact-subset argument inside each plane or annulus.

In a plane component, enclose F∩A in the interior of a single closed disk. In a half-open annulus, enclose it in an initial collar. Include a small initial collar at any otherwise unselected original boundary circle. There are finitely many such circles. The pieces are disjoint because different components are disjoint. Removing the interiors of the disks and relatively open initial collars leaves a compact surface P⊂Int E, contains L in its interior, and makes P⊂Q. More explicitly, in annular coordinates one removes S¹×[0,R), retaining the new circle at R; this is the compact interpretation of “shaving boundary collars” in the candidate.

Deleting finitely many disjoint interior disks and shaving boundary collars cannot disconnect a connected surface. The deleted disks and collars are disjoint from L. Reattaching collars preserves homotopy type, and filling boundary circles with disks only adds relations to fundamental groups. Hence π₁(P∩Eα)→π₁(Eα) is surjective. The inclusion Int P→P is a homotopy equivalence, obtained by pushing a boundary collar inward. This proves every part of Lemma 1, including its cofinality assertion.

No simultaneous infinite collection of cuts is needed. Infinitely many complementary disk components may exist; only the finitely many meeting a particular compact complement F are relevant.

## 3. Lemma 2: the relative collar construction in full

This is the main ambient-geometric point. The claimed construction is valid in the topological category.

First choose a flow collar over a surface neighborhood larger than the eventual P and with spare time length. It may be shortened so that a neighborhood of the initial segment L×[0,2a] lies in O_D. Compactness then permits choosing P by Lemma 1 so that its whole required product strip lies in O_D. One must retain a larger patch around P for the collar extension; the initial P₀ and permitted shrinking supply it.

The precise extension result is Armstrong, [*Collars and concordances of topological manifolds*](https://www.maths.gla.ac.uk/~mpowell/Armstrong1970_Article_CollarsAndConcordancesOfTopolo.pdf), Theorem 1, p.119, inspected directly together with its proof on pp.121–122. A collar of a compact boundary submanifold, given with twice the necessary length, extends after restriction to the full boundary. Armstrong assumes local flatness. Here this hypothesis holds because the flow product is defined on a larger boundary patch, and the compact patch can be chosen with collared surface boundary. Restricting the product produces ordinary local product and corner charts. No arbitrary wild closed collar is being extended.

Here is an explicit construction realizing all overlap claims. Denote the extended inward collar by c, agreeing with the flow collar on the specified larger patch. Take pairwise disjoint open regular neighborhoods Bα of Eα inside ∂N, by adding short outside collars to their boundary circles. Each Bα deformation retracts to Eα, fixing Eα pointwise. Their union B contains E.

The set

D_tail = D minus φ(L×[0,a/2))

is compact. Indeed the removed part is relatively open in D by the local product description and L⊂Int P. D_tail is disjoint from E, since D∩E=L. The compact strip over the larger patch at heights at most a/3 is likewise disjoint from D_tail. Choose the boundary thickening A in the form

A = {c(q,t): q∈B, 0≤t<h(q)},

where h is positive and continuous, equals a/3 on the patch needed over P, and is sufficiently small elsewhere that closure(A) misses D_tail. This is possible by compact separation and the available collar. Make B and its thickening small enough to keep different Aα disjoint. Each Aα retracts first down its interval fibers to Bα and then onto Eα. A is relatively open in N, including at t=0.

Now choose V_tail relatively open in O_D, containing D_tail, with its closure disjoint from closure(A). This is possible because D_tail is compact and disjoint from closure(A). Over the initial collar, it has no points at heights at most a/3. It automatically contains L×[a/2,3a/4], as this compact strip is part of D_tail. Consequently

V₀ = V_tail ∪ φ(Int P×[0,a))

is relatively open in N, is contained in O_D, and contains all of D. Its intersection with A is exactly φ(Int P×[0,a/3)). A positive varying upper height would give the same conclusion, but constant height is available on the required patch.

The relatively open set V₀ lies in a manifold with boundary and is locally path connected. Its path components are open. Connected D therefore lies in one such component V. For every Eα, P∩Eα is connected and meets L. Thus its entire path-connected product strip meets D and is retained in V. No overlap component is lost in passing from V₀ to V. It follows that

Aα∩V = φ(Int(P∩Eα)×[0,a/3)).

The two explicit retractions identify the inclusion of this overlap into Aα with Int(P∩Eα)→Eα. Its induced fundamental-group map is surjective by Lemma 1. This proves the required connected overlap, its exact component control, and its nonabelian surjectivity. A∪V contains the relatively open neighborhoods A of E and V of D, as required.

The construction concerns relative neighborhoods in N. It does not introduce outside points near an entry face, assume a handlebody, or assert that an entry-surface shaving alone shrinks all of D toward K.

## 4. Proposition 3: van Kampen and the stopped backward flow

There are only finitely many entry-surface components. Their thickenings Aα are pairwise disjoint. In adjoining them successively to V, the intersection of the next Aα with everything already adjoined is therefore exactly Aα∩V. It is path connected, and its fundamental group surjects onto that of Aα. Van Kampen then says that adjoining Aα supplies no new generators. Choose connecting paths in V from a fixed basepoint to an overlap basepoint when necessary. Thus π₁(V)→π₁(A∪V) is genuinely onto; disconnected overlaps are not being overlooked.

The map F_t(x)=φ_{max{-t,tⁱ(x)}}(x) is continuous jointly for finite t. The scalar maximum is finite and continuous even where tⁱ=-∞. It fixes E and stays in N by definition of the first entry time. Its image is exactly the union of E and the points whose forward orbit stays in N for time t:

- A trajectory stopped at its entry endpoint lands in E; one not stopped yields a point with a surviving forward segment of length t.
- Conversely, if y has that surviving segment, x=φ_t(y) lies in N and its entry time is at most -t, so F_t(x)=y.

These images are decreasing compacta with intersection E∪D. Given the relatively open neighborhood A∪V of that intersection, compactness puts a sufficiently late image inside A∪V. The resulting homotopy carries every loop into A∪V, where van Kampen represents its class by a loop in V.

Basedness is also correct. If p∈K, its track under F_t lies in K⊂V. Whiskering by that track identifies the transported loop class with the original element of π₁(N,p). Therefore the component of any O_D containing D surjects onto π₁(N,p). This is an assertion about actual loop classes, not merely their homology or free homotopy classes.

## 5. The safe forward-time neighborhood and the empty-entry correction

For open W⊂Int N containing connected K, its component W₀ containing K exists, is open, and is path connected. The nested compact sets φ_t(D) converge to K, so some T has φ_T(D)⊂W₀. The proposed set

O_D = {x∈N: tᵒ(x)>T and φ_T(x)∈W₀}

is relatively open by exit-time and flow continuity, and contains D. For every point in O_D the entire segment of times [0,T] lies in N. This extra survival condition is essential: the condition φ_T(x)∈W₀ alone would not rule out departure and reentry.

The established epimorphism supplies a loop in O_D representing any prescribed π₁(N,p) class. Flowing it forward for time T gives a loop in W₀ through a homotopy in N. Its basepoint track is inside invariant K⊂W₀, so the endpoint loop can be whiskered within W₀ to restore the original basepoint and class. Hence π₁(W₀,p)→π₁(N,p) is onto.

If E is empty, every finite first-entry endpoint would have to belong to E, so tⁱ=-∞ throughout N. Thus N=N⁻ and D=N⁺=K, not N. Backward images φ_{-t}(N) are decreasing compact neighborhoods in the relative sense and intersect in K. For any relatively open V containing K, sufficiently large backward time maps all of N into V; the basepoint track again stays in K. In particular one may take V=W₀ for the desired epimorphism. V2 states this correctly and bypasses the entry-collar lemma in this exceptional case.

This is a real error in the original text, as the outward radial flow on a closed ball already has empty entry and D equal to the center. It is nevertheless entirely local: the main stopped-flow identity already contains the correct argument, and no theorem hypothesis or quantifier is changed by the correction.

## 6. Lemma 4: an actual ambient graph factorization

The dimension argument can be made explicit without assuming embedded graph spines. Choose a finite open cover of K of sufficiently small mesh and order at most two, subordinate to a small-mesh initial cover. Take a finite closed shrinking F_i inside those sets, still covering K, and discard empty F_i. Every triple of F_i is empty. Since there are finitely many compact triples, sufficiently small ambient open neighborhoods U_i of F_i also have empty triple intersections. These may be chosen inside the prescribed small tubular neighborhood and with uniform diameter control. For example, small Euclidean metric neighborhoods of the F_i suffice. Choose x_i∈F_i⊂K.

On V=∪U_i a finite partition of unity gives a map f into the finite nerve G. The absence of triple intersections makes G a graph. Assign each vertex to x_i and each edge to the straight segment joining its assigned endpoints. If x lies in U_i, its distance to x_i is uniformly small. Therefore both every relevant edge and g(f(x)) lie in the same controlled Euclidean neighborhood of x. The straight homotopy from x to g(f(x)) lies in the chosen 4ε-neighborhood of K, hence in Int N. Shrinking V further, if desired, preserves this homotopy and factorization.

If K is connected, the nerve can be taken connected. Indeed the restrictions U_i∩K are a finite open cover of K and every U_i meets K. A disconnected intersection graph would partition K into two disjoint nonempty relatively open unions, contradicting connectedness. Any ambient intersections only add edges. This proves the connected-graph assertion and all ambient-containment requirements.

The argument requires only covering dimension at most one. It does not require local connectedness, finite first cohomology, or a neighborhood deformation retraction onto an embedded graph.

## 7. Lifting the graph and the movability quantifiers

For a connected finite graph G and any g:G→N, choose a spanning tree and a path from its image basepoint to p∈K. Contract the tree image to p through a homotopy in N. The homotopy extension property for a graph and its tree extends this to the whole graph. Each remaining edge is then a based loop at p.

The surjection π₁(W₀,p)→π₁(N,p) supplies a representative in W₀ of each of these finitely many loop classes. Equality in π₁ means a based homotopy in N. These homotopies paste over the edges because they agree at every vertex throughout. The resulting graph map g_W has image in W₀ and is homotopic to g in N. This needs no section of the manifold inclusion and no control of higher homotopy groups: the only domain being lifted is a graph.

The order of choices is correct:

1. Given any open O containing K, choose a refined N⊂O.
2. Choose one open neighborhood V of K and one factorization V→G→N using Lemma 4. V is now fixed.
3. Given any open W containing K, take the component containing K of W∩Int N and perform the graph replacement there.
4. Compose the graph homotopy with f and concatenate with the previously chosen inclusion-to-gf homotopy.

This gives H:V×[0,1]→N⊂O, starting at inclusion and ending in W. V depends on O and not on W. The assertion holds even for all open W containing K, which includes the smaller target neighborhoods required in the usual definition of movability.

For finitely many components, the refined block has disjoint components corresponding to them. Each such block component isolates its corresponding invariant component. Apply the connected argument in each and choose V_i inside its interior. Their finite disjoint union is open and contains all of K. The component homotopies paste continuously, remain in O, and end in the prescribed W. No uniform construction over infinitely many components is asserted.

## 8. Acceptance boundary

The argument establishes actual movability in the stated isolated, finite-component, covering-dimension-at-most-one class, including examples with infinite-rank first Čech cohomology. Its nonabelian step is independently justified by entry-complement geometry, controlled relative collars, van Kampen, and finite-time-safe flow homotopies.

The following remain outside this acceptance:

- infinitely many connected components;
- covering dimension two or three;
- replacement of an arbitrary compact invariant set by an isolated one;
- existence, for every arbitrary flow/A/U, of a compact invariant movable enlargement B between A and U;
- any novelty or comprehensive literature claim.

The unrestricted original problem remains unresolved by this theorem. The audit found one corrected exceptional-case error, not a gap requiring a new research program. The source checks here concern the exact standard facts already used in the existing proof. Original artifacts and their conditional verdict remain preserved.

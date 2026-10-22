# Calegari Question 6.1: restricted criteria and the unresolved containment step

## Disposition and conventions

Problem 10300011 / AMR-102-0011, rank 1004. The original task asks:

> Characterize those essential laminations which contain genuine sublaminations.

This is Question 6.1, printed page 11, in Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, arXiv:math/0209081v1. **The general task is unsolved by this work after five substantive approaches.** The present report establishes only the restricted results below. It does not assert exhaustive current openness, novelty, or human peer review.

Throughout our theorems, M is a closed connected oriented 3-manifold. Sublaminations are nonempty closed unions of whole leaves; equality with the original lamination is allowed. Complementary components always mean their abstract metric completions, so distinct boundary sides are not identified merely because they project to the same leaf. An I-bundle must respect the horizontal boundary given by the lamination. Two-sidedness is imposed where expressly stated, not on every lamination in the original problem.

Essentiality and genuineness are used as in Calegari's Definitions 1.3–1.4. We use the classical fact that sublaminations of essential laminations are essential: Gabai–Kazez, Lemma 1.6, explicitly invokes this consequence of Gabai–Oertel. Closed two-sided incompressible surfaces of positive genus in an irreducible manifold are standard essential-lamination examples. The elementary interval-bundle classification and the usual classification of compact surfaces are also classical inputs.

The source already gives a hyperbolic/quasigeodesic sufficient condition and excludes genuine sublaminations from R-covered or one-sided-branching foliations. None is claimed here as a discovery. Brittenham's fully carried essential-branched-surface criterion is credited in Section 5. These statements must not be confused with a solution of the fixed-lamination containment problem.

## 1. Cutting along finitely many compact leaves

**Theorem 1.** Suppose Lambda is an essential lamination consisting of finitely many two-sided compact connected leaves. Then Lambda contains a genuine sublamination if and only if Lambda is genuine.

**Proof.** Only the nongenuine case requires work. Cut M open along all leaves. Every resulting piece N is compact, connected and, by nongenuineness, an I-bundle whose entire boundary is horizontal. Its base is therefore a closed connected surface: a boundary component of the base would give a nonempty vertical boundary, which is absent here.

An orientable total space over an orientable base is the product I-bundle, with two horizontal boundary components. An orientable total space over a nonorientable base is the twisted I-bundle, with one connected horizontal boundary component, the orientation double cover of the base. This follows from w_1(TN)=p^*(w_1(Tbase)+w_1(vertical line)); orientability forces the two classes to agree. Equivalently it follows from the elementary orientation classification of interval bundles. Thus each piece has either two boundary components (product) or one (twisted).

Form the dual multigraph G: one vertex for each piece and one edge for each leaf. A loop counts twice toward degree. The graph is connected because M is connected. Its vertices have degree one or two. Since Lambda is nonempty, there is at least one edge and no isolated vertex. A finite connected multigraph with those degrees is a path or a cycle, including a one-edge loop and a two-edge cycle. The degree-one endpoints of a path correspond to twisted pieces; all other pieces are products.

Choose a nonempty collection of leaves to retain. Removing the other leaves glues their incident pieces across the corresponding edges. Components of the subgraph consisting of removed edges describe the new complementary pieces. Because at least one edge remains, no such component contains a whole cycle; in the path case no such component contains both original endpoints. Every component is consequently a chain of product pieces, possibly with exactly one twisted piece at an end.

A finite chain of products glued along horizontal boundaries is again a product: identify each successive surface using its attaching homeomorphism and concatenate the interval coordinates. This absorbs arbitrary attaching maps; no identity or foliation-preserving attaching map is assumed. Attaching product collars to the horizontal boundary of a twisted I-bundle gives the same twisted I-bundle, up to bundle homeomorphism after rescaling a collar. Therefore every new complementary piece is an I-bundle. The selected nonempty sublamination is essential by inheritance and is nongenuine. This proves the assertion. QED.

This proof establishes a restricted classification without asserting that an essential lamination lying in an I-bundle is already the product foliation. Brittenham's *Essential laminations in I-bundles* illustrates why that stronger assertion would be unsafe.

**Corollary 1.1 (one compact leaf).** Let S be a connected two-sided closed incompressible surface of positive genus in a closed oriented irreducible M, and regard S as a one-leaf lamination.

- If S is nonseparating, S is nongenuine exactly when it is a fiber of a surface bundle M over the circle.
- If S separates M, it is nongenuine exactly when both components cut off by S are orientable twisted I-bundles with horizontal boundary S. This is the usual semifiber situation.

For the first assertion, the cut manifold is connected with two horizontal boundary components and must be S times I; regluing is a mapping torus. The converse follows by cutting a mapping torus at its fiber. For the second, both cut components have one boundary component and the preceding classification applies. These are classical fiber/semifiber phenomena; compare Gabai–Kazez, Remark 0.2(iii).

A readily checked sufficient obstruction in the nonseparating case is b_1(N;Q) != 2 genus(S), where N is M cut along S: a product has exactly that first Betti number. Equality is not claimed to imply a product. This is a consequence, not an additional author turn.

**Limit of Approach 1.** A general lamination can have infinitely many noncompact leaves and noncompact completed complementary regions. The finite cut-piece graph and finite collar gluing no longer supply the classification. Theorem 1 does not extend to arbitrary foliations, some of which do contain genuine sublaminations despite not themselves being genuine.

## 2. Holonomy dynamics: all sublaminations of a circle suspension

Let Sigma be a closed oriented surface of genus at least two, let G=pi_1(Sigma), and let rho:G -> Diff^2_+(S^1) be an action. Form the suspension

E_rho=(Sigma_tilde times S^1)/G,

using deck transformations on the first factor and rho on the second. Its horizontal foliation F_rho is taut: a circle fiber over any base point is a closed transversal meeting every horizontal leaf. It is therefore essential.

**Theorem 2.** Nonempty closed sublaminations of F_rho are in bijection with nonempty closed rho(G)-invariant sets K in S^1. Every such sublamination is nongenuine. Consequently F_rho contains no genuine sublamination.

**Proof.** The lifted foliation has leaves Sigma_tilde times {z}. A saturated subset is therefore Sigma_tilde times K; it is closed exactly when K is closed and descends exactly when K is invariant. Conversely these conditions plainly construct a sublamination. This proves the bijection.

If K=S^1, there are no complementary components. Otherwise let J be a component of S^1 minus K, and let H be its stabilizer in G. The union of translates of Sigma_tilde times J descends to one complementary component, and distinct orbits of gaps give distinct components. This component is

(Sigma_tilde times J)/H.

Its abstract completion is the associated closed-interval bundle over Sigma_tilde/H obtained by adjoining two endpoint sides to J. If the two endpoints coincide as points of S^1, they still define distinct sides in the abstract completion. The H-action on J is order preserving and extends to its two ends. Thus the completed component is an oriented I-bundle, necessarily a product over its base. One can use the usual interval-bundle classification; in the smooth case, a positive fiberwise density and integration from the lower endpoint also give the product coordinate. The base may be noncompact, which causes no problem for local triviality or this construction.

Every complementary completion is therefore an I-bundle. Essentiality follows from the taut-foliation/sub-lamination input already stated, and genuineness fails. QED.

This is a direct proof in an explicitly described class and a classical special case of the R-covered exclusion in the original source, not a new general exclusion theorem.

**A fixed-ambient contrast.** Set M=Sigma_g times S^1, g>=2. The product foliation by Sigma_g fibers contains no genuine sublamination by Theorem 2. In this SAME manifold, let c be a nonseparating essential simple closed curve in Sigma_g and T=c times S^1. This is a two-sided incompressible torus. The product manifold is irreducible, and hence T is an essential one-leaf lamination. Its cut manifold is

N=Sigma_{g-1,2} times S^1.

Here b_1(N;Q)=(2(g-1)+2-1)+1=2g, whereas b_1(T^2 times I;Q)=2. Because g>=2, N is not a product T^2 times I. Its boundary has two components, excluding an orientable twisted I-bundle as well. Thus T is genuine. Incompressibility follows directly from the injection of the infinite cyclic subgroup generated by c into pi_1(Sigma_g), multiplied by the identity on Z.

It follows that no criterion depending only on the ambient manifold, its fundamental group, or its homology can decide the target for all specified laminations in that manifold. The lamination itself matters. This does not rule out criteria using both manifold and lamination data.

**Limit of Approach 2.** The existence of a global transverse circle fibration is essential to the proof. An arbitrary essential lamination need not be a horizontal suspension. No such reduction is supplied.

## 3. Transverse-weight equations do not remember complementary topology

**Proposition 3.** Intrinsic unbranched-carrier topology, its sector incidence equations, and a positive transverse weight do not by themselves determine whether its specified carried lamination contains a genuine sublamination.

**Proof.** Consider the same abstract one-sector unbranched carrier B=T^2 in two embeddings.

(A) M_0=T^2 times S^1, with Lambda_0=T^2 times {point}.
(B) M_1=Sigma_2 times S^1, with Lambda_1=c times S^1 as in Section 2.

In both cases B has one sector and no branch equations. Its nonnegative weight cone is exactly R_{>=0}. The single leaf has transverse atomic weight 1. Thus all data stipulated in the proposition agree, including the intrinsic surface and its fundamental group.

In (A), cutting produces T^2 times I, so the one-leaf lamination is nongenuine. A nonempty sublamination of a single connected leaf is the leaf itself, so it has no genuine sublamination. In (B), the preceding computation gives a genuine one-leaf lamination. This establishes opposite answers with identical stated weight data. QED.

The use of different ambient manifolds here is deliberate: the proposed inadequate input omits the embedding. Section 2 supplies the distinct fixed-manifold obstruction. Neither example disproves a criterion allowed to use the embedded carrier's complementary pieces, holonomy, or an adequate coding of the particular lamination. No arbitrary matrix has been asserted to be realizable as an embedded branched surface.

**Limit of Approach 3.** Adding positivity, rationality, or linear feasibility to transverse-weight equations cannot repair this loss of embedding information. A genuinely embedding-sensitive criterion remains necessary; no complete such criterion is derived.

## 4. Finite covers and descent of witnesses

**Theorem 4.** Let p:M_hat -> M be a finite regular covering of closed connected oriented 3-manifolds, and let Lambda be an essential lamination of M. Suppose Gamma is a genuine sublamination of p^{-1}(Lambda) invariant under the deck group. Then p(Gamma) is a genuine sublamination of Lambda.

**Proof.** A finite covering is closed, so p(Gamma) is closed. It is saturated: a path in a leaf of Lambda starting at p(x), x in Gamma, lifts to a path in a leaf through x, and that entire leaf belongs to Gamma. Path connectedness of leaves shows that the whole projected leaf belongs to p(Gamma). Deck invariance gives p^{-1}(p(Gamma))=Gamma. Essentiality of p(Gamma) follows from the classical inheritance theorem, since it is a sublamination of Lambda.

Suppose p(Gamma) were nongenuine. Each of its completed complementary regions would be an I-bundle. The components upstairs cover these regions, with the covers extending across the abstract boundary sides by local lamination charts. Every connected cover of an I-bundle is an I-bundle: the original bundle deformation retracts onto its base, so the covering is the pullback of the corresponding base covering, with the same interval fiber. Hence every complementary completion of Gamma would be an I-bundle, contradicting its genuineness. QED.

We have used the implication that a cover of an I-bundle is an I-bundle. We have NOT asserted the reverse implication or a general ascent theorem for genuineness.

**Corollary 4.1.** In the same finite REGULAR cover, suppose there is a genuine sublamination Gamma of p^{-1}(Lambda) consisting of finitely many two-sided compact leaves. It need not initially be deck invariant. Then Lambda contains a genuine sublamination.

**Proof.** Take the union U of all deck translates of Gamma. Because all translated leaves lie in the same lamination p^{-1}(Lambda), they coincide or are disjoint; they do not acquire transverse intersections. U is a nonempty finite union of two-sided compact leaves, is closed, is essential by inheritance, and is deck invariant. If U were nongenuine, Theorem 1 would make its sublamination Gamma nongenuine. Thus U is genuine, and Theorem 4 applies. QED.

The regular-cover condition is not silently removed by passing to a normal closure: doing so would require a separate genuineness-ascent statement, which has not been proved here.

**Limit of Approach 4.** For an arbitrary noncompact witness upstairs, its finite deck orbit union is still a sublamination, but this proof supplies no general guarantee that the union is genuine. Theorem 1 only treats finite compact leaves. Neither an equivariant witness-selection theorem nor a general algorithm to find one has been obtained.

## 5. Recognition versus containment: the attempted finite-certificate search

A classical theorem already addresses a nearby finite question. Brittenham, *Small Seifert-fibered spaces and Dehn surgery on 2-bridge knots*, Section 1 Proposition (author preprint pp3–5), says that if an essential lamination is fully carried by an ESSENTIAL branched surface B, nongenuineness is equivalent to all exterior pieces of its fibered neighborhood being I-bundles with the prescribed horizontal/vertical boundary pattern. Essentiality of B and full support are hypotheses, not incidental details. This recognizes genuineness of that fully carried lamination; it does not by itself classify sublaminations of a nongenuine one.

Agol–Li's *An algorithm to detect laminar 3-manifolds*, Theorem 4.6 and Theorem 5.2, provides ambient existence algorithms for essential laminations and Reebless foliations. No algorithm for the present fixed-lamination target is claimed by those statements, and Reebless must not automatically be replaced by taut in the toroidal setting.

Our fifth approach was to enumerate finite legal splitting histories, candidate essential carriers, and carrying maps, then apply a genuine-complement certificate to each fully carried candidate. For any specified finite encoding with effective local validation, dovetailing such finite candidates semidecides the existence of a VALID CERTIFICATE OF THAT FORM. It does not establish that every genuine sublamination yields an enumerated certificate, that the certificate realizes a subset of the prescribed Lambda, or that a negative search terminates.

The containment issue is real even at the simplest representative level. In an unbranched neighborhood S times [-1,1], both S times {0} and S times {1/2} are fully carried by S, and are disjoint. The assertion that a carrier carries Gamma does not imply that this Gamma is literally a subset of a different specified carried lamination. These parallel slices are isotopic, so this example only invalidates the literal representative shortcut. It does not refute a valid isotopy/realization theorem, an adequate splitting criterion, or an algorithm using richer input.

The missing step is therefore stated precisely: obtain a sound and complete finite relation connecting the proposed splitting/carrier certificates to genuine closed saturated subsets of the GIVEN essential lamination, and supply a terminating negative decision method if a decision algorithm is desired. The original source explicitly discusses finite descriptions and splitting relations; simply restating that program is not a solution. No completeness or termination theorem has been proved in this approach.

## Overall remaining gap

The general lamination may have infinitely many noncompact leaves, no transverse circle fibration, and no supplied effective coding that makes genuine-sublamination containment decidable. The compact-cut theorem, suspension computation, weight-data obstruction, and finite-cover descent do not characterize all such inputs. The fifth approach leaves the exact realization/completeness/termination step open. Accordingly the author disposition is **unsolved, 5/5**, with the five approaches recorded in APPROACH_LEDGER.json.

The executable checks verify finite graph bookkeeping, arithmetic in the explicit surface examples, metadata, input rejection, and byte integrity. They neither formalize the topological proofs nor turn a bounded test into a universal theorem. Independent mathematical review is still required before publication acceptance.

## Public references

1. Danny Calegari, *Problems in foliations and laminations of 3-manifolds*, arXiv:math/0209081v1, Definitions 1.3–1.4 and Question 6.1. https://arxiv.org/abs/math/0209081
2. David Gabai and William H. Kazez, *Group negative curvature for 3-manifolds with genuine laminations*, Geometry & Topology 2 (1998), 65–77, Remark 0.2(iii), Lemma 1.6. https://arxiv.org/abs/math/9805152
3. Mark Brittenham, *Small Seifert-fibered spaces and Dehn surgery on 2-bridge knots*, author preprint, Section 1; published as *Exceptional Seifert-fibered spaces and Dehn surgery on 2-bridge knots*, Topology 37 (1998), 665–672. https://markbrittenham.github.io/UNL_webpages/papers/pdf/sm2br5.pdf
4. Mark Brittenham, *Essential laminations in I-bundles*, Transactions AMS 349 (1997), 1463–1485. https://markbrittenham.github.io/UNL_webpages/papers/pdf/surfxi5m.pdf
5. Ian Agol and Tao Li, *An algorithm to detect laminar 3-manifolds*, Geometry & Topology 7 (2003), 287–309, Theorems 4.6 and 5.2. https://arxiv.org/abs/math/0201310
6. Danny Calegari, *Promoting Essential Laminations*, arXiv:math/0210148v3, Definition 3.4.1 and Lemma 3.4.2. https://arxiv.org/abs/math/0210148

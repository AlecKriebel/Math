# Independent degree-two derivation

Original head: `86d076dae3e3fa8b7cda7fd9c6a822c3d7392c14`.

This derivation was written from the two current proof files and the three mathematical support lemmas, fresh primary bodies, and a newly authored checker, before consulting historical audits or acceptance conclusions. It treats each asserted conclusion as a hypothesis. The review estimates are recorded in RESEARCH_LOG.md. Source bodies, extracted text, and rendered pages are confined to `sources/raw/`.

## Exact category and controlling question

The objects are smooth unframed ordered proper interval embeddings in a rounded `D²×I`, fixed at matching marked endpoints and standard in endpoint collars. Each interval is oriented bottom to top; its height need not be monotone. Ordinary rational finite type includes self-crossing and mixed-crossing resolutions. Write `V_≤n(k)` for the full vector space including constants. The test set consists of objects whose **actual three-dimensional** exterior has abstract free group `F_k`; a bottom-meridian basis is not required.

Ohtsuki's 2002 collection, printed p.408/PDF p.36, asks separately whether the vanishing kernel is nontrivial and whether it and the Milnor subspace span. This is a parameterized question, not a request answered by giving one invariant or by showing all finite-type invariants detect some nonfree example. The degree-two family tests these precise conclusions:

* `V_≤2(2) ∩ Q[all µ_I] = span_Q(1,ell,ell²)`, with all lengths and repeated indices permitted.
* Component Conway `a_1` is outside `M_2(2)+N_2(2)`.
* `N_≤2(k)=0` for every integer `k≥2`, and therefore `N_≤n(k)=0` for `0≤n≤2`.

A counterexample at `(k,n)=(2,2)` refutes unrestricted spanning. It does not decide spanning at larger n. The zero-kernel conclusion is likewise restricted to n≤2. Orders 3–6 and the higher-order classification remain unresolved by this family; the order-seven family requires separate topology and integration review.

## Complete low-order coordinate space

Let `c(K)` denote Conway's z² coefficient, `a_i=c(individual closure of i)`, and `w_ij=c(two-string plat of i,j)-a_i-a_j`. The plat joins the two bottom ends and separately the top ends with fixed short caps. Fresh Meilhan v2, Definitions 1.1–1.3, §2.1, and Theorem 2.4/PDF p.5, use this ordinary category and supply the full expansion

`v=Q((ell_ij)) + Σ_{i<j<h} d_ijh µ_ijh + Σ_i b_i a_i + Σ_{i<j} e_ij w_ij`,

where `deg Q≤2`. Q includes constants, all linear linking terms, all squares, all pair products sharing a label, and all pair products on four different labels. No support pattern is omitted. For k=2 this becomes

`v=A+B ell+C ell²+D a_1+E a_2+F w`.

The source formula is an actual spanning theorem for functions, not only an associated-graded statement. Its 1T framing-independence relation is visible on p.2. Its p.3 definitions give `c(U)=0`, `c(trefoil)=1`, and the same plat correction. Rational coefficient division is legitimate.

## Entire Milnor algebra: the concordance mechanism

Fresh Meilhan–Yasuhara v1 §2.1.4/PDF p.4 defines µ_I for possibly repeated indices. Section 5.1/PDF p.22 gives the relative interval-times-interval concordance convention and asserts their concordance invariance. Thus **every finite polynomial in any of these functions**, even with arbitrarily long generators, is concordance invariant. This does not infer order bounds from a polynomial's weighted degree. Cancellation of its displayed high-order terms is irrelevant once the resulting function lies in `V_≤2`.

Take a long trefoil T and the long square knot `S=T#(-T)`, where `-T` is reversed mirror. Smooth concordance-group inverses give a null-concordance. A standard ribbon inverse construction can be cut along a product strip at a chosen boundary arc to give a long rectangle fixed in endpoint collars; one can choose product collars at both concordance levels. This is smooth concordance in an ordinary product four-manifold, not exotic or merely topological concordance. Fresh Cochran–Harvey pp.1–2 distinguish these categories and give the required smooth convention.

The normalized Conway skein identities give orientation invariance, `∇mirror(K)(z)=∇K(-z)`, and connected-sum multiplicativity. Hence `∇S=(1+z²)²`, so `c(S)=2`. It is not being claimed that Conway c is concordance invariant.

Insert S locally on strand 1 of the trivial two-string link, away from strand 2. The concordance fits in the local ball times I; keep the second strand fixed. The new link J_1 is null-concordant, with linking 0, component coordinates `(2,0)`, and plat coefficient 2; thus `w=0`. Likewise J_2 has `(0,2,0)` in the `(a_1,a_2,w)` coordinates.

For the third test choose a product-collared null-concordance rectangle A for S. Its oriented rank-two normal bundle is trivial. Prescribe a nonzero normal field on the top edge and the two endpoint sides to give the usual separated top identity strands and fixed endpoints. These three sides are one contractible boundary arc, so extending the field creates no full-boundary winding obstruction. Do **not** prescribe the bottom framing independently. A section extends over the disk and can be chosen constant on collars. In the product bottom collar the normal plane is spatial, so bottom push-offs lie in the bottom three-ball; the analogous fact holds at the top. Small tubular push-offs ±ε are disjoint embedded rectangles with the prescribed endpoints. Scaling and a collar identification place the separation at the fixed marked positions.

Their bottom is C(S). It is concordant to identity, so its pairwise linking is zero. Each component closure is S. Restricting the field to the bottom produces an embedded narrow ribbon disk with long sides the two bottom strands; the standard endpoint field makes its short sides the fixed caps. Its boundary is the plat. This knot bounds an embedded disk in the three-ball, hence is the unknot. Consequently C(S) has `(a_1,a_2,w)=(2,2,-4)`. This is a disk boundary argument, not a claim that a general cable closure is trivial.

Every concordance-invariant rational order-two function expanded in the six coordinates must therefore obey

`2D=0`, `2E=0`, `2D+2E-4F=0`.

The 3×3 test determinant is -16; D=E=F=0. This proves the upper inclusion for the entire Milnor algebra. Conversely constant 1, `ell=µ_12`, and ell² belong to that algebra and have respective orders ≤0,≤1,≤2. Pure braids realize every integer linking value, so these functions are independent. This proves the exact intersection. None of J_1,J_2,C(S) is asserted to have free exterior, and the argument does not require this.

## Free-exterior witnesses and marking

Fresh complete Nogueira Coimbra preprint 14–09, received 27 February 2014, Appendix pp.14–15 and full Figures 9–10, constructs a two-arc tangle using a trefoil unknotting tunnel and sliding its ends to the boundary. Its appendix explicitly supplies the actual handlebody exterior and the individual capped knot types: first trefoil, second `T(3,-4)`. The drawing has all relevant crossing interruptions and the blue second arc. The review uses the source's existential tunnel construction; it does not claim a independently recognized marked Wirtinger diagram. The source statement is about the ball tangle, rather than the main theorem concerning essential surfaces in later closed knots.

A finite tame PL arc system smooths by rounding corners and straightening collars in disjoint small neighborhoods. An orientation-preserving sphere isotopy moves the four individually chosen ordered endpoints to the fixed bottom/top destinations; it extends through a collar. Thus this is a construction of an ordinarily marked smooth link L. It preserves its actual exterior. A two-arc ball exterior has boundary Euler characteristic -2 and connected genus-two boundary, so the asserted handlebody has group F_2.

After discarding the other component, the boundary sphere has only the two surviving endpoints. Every embedded boundary cap joining them is isotopic rel these endpoints to every other cap. Thus the individual knot type survives any such orientation-preserving marking. It would be false to assert arbitrary cap-system equivalence on the four-punctured sphere; it is not used. Therefore `a_1(L)=1`, `a_2(L)=5`. Fresh Willerton p.1 fixes the Conway normalization and p.5 gives `(p²-1)(q²-1)/24`; substituting (3,-4) gives 5. An independent symmetric Alexander-polynomial identity also gives 5 in the checker. Mirroring/reversing has no effect on this even coefficient.

A product disk diffeomorphism interchanging the two marked basepoints, applied to a separate copy with carried components assigned the new labels, constructs L^s in the same fixed-endpoint ordered category. Its group is still F_2 and its component values are (5,1). This is not an identification of L with L^s within the ordered isotopy category. Their linking and plat values remain arbitrary and need not agree.

For R take the explicitly pictured rational tangle `[1]+1/[2]`. The fresh Kauffman–Lambropoulou DNA p.30/Figure 20 supplies the trefoil numerator. Their classification v2 p.6 gives ball-pair rationality, p.7 the elementary crossing convention, p.9 the two numerator caps, and Theorem 6/pp.39–41 the odd/even vertical connectivity. Direct endpoint tracing gives NW–SW and NE–SE, with no closed component. The fraction is 3/2. Mark these as vertical components and choose the ball identification to carry **both numerator caps** to the fixed plat caps. Two disjoint cap arcs have disk neighborhoods whose complement is an annulus; matching those neighborhoods and the annulus by an orientation-preserving sphere diffeomorphism, and extending over the ball, produces this marking. Its collar straightening is harmless.

The rationality homeomorphism need not fix that cap system; it is used solely for the pair's topology. It carries the exterior to pair-of-pants×I, a genus-two handlebody. Each component is boundary-parallel before and after the marking, so after forgetting the other strand its individual standard closure is unknot. The cap-preserving marking makes the plat the cited trefoil. Thus `(a_1,a_2,w)(R)=(0,0,1)` with actual free group F_2. This does not assert the same plat for every four-point re-marking.

## Negative spanning at (2,2)

For P_j take a pure two-braid with j full twists, chosen for linking j. A height-dependent disk isotopy trivializes its exterior as twice-punctured disk×I, giving actual F_2. Its individual strands are unknotted, so a_1(P_j)=0. On P_0,P_1,P_-1, a proposed equality `a_1=A+B ell+C ell²+u`, where u vanishes on all free exteriors, forces A=B=C=0. On L it then forces 1=0. The four-row determinant on columns `(1,ell,ell²,a_1)` is 2 for every possible unknown linking t of L: expanding in the last column removes all dependence on t. No braid matching of all Milnor data or deformation of L is required.

## Pure braid detection of all higher-strand low-order terms

For any pure k-braid the actual exterior is k-punctured disk×I. All individual knots are unknotted. Deletion to two strands gives a pure two-braid; its two-plat has one bridge, equivalently each successive twist slides against a cap, so it is unknot. Therefore all a_i and w_ij vanish on pure braids.

Let `A=σ_1²`, `B=σ_2²`, `β=ABA^-1B^-1`. Use `Φ_AB=Φ_A∘Φ_B` and the submitted Artin generator convention. The new checker composes these maps from generator substitutions, derives conjugators by cyclic reduction, and then removes the own-meridian exponent. It independently obtains exactly the three displayed submitted words. Their degree-two standard Magnus leading terms are respectively

`X_2X_3-X_3X_2`, `-X_1X_3+X_3X_1`, `X_1X_2-X_2X_1`.

Thus selected µ_123 is ±1; all linear terms and linking numbers are 0. Reversing the longitude conjugation convention changes a sign, leaving the test nonzero. Bar-Natan's source uses a different exponential Magnus convention and reduced-group discussion; the review imports only the explicit braid exterior and parallel/Wirtinger interpretation. The standard 1+X convention is used in the new integer checker.

Deleting any strand of β cancels one generator and its inverse, giving the identity braid on the other two. In the algebra checker the remaining meridians and **surviving-component** conjugators reduce to identity. The deleted component's own longitude need not reduce to identity; demanding it would be an invalid extra test, corrected in this review's checker. No claim depends on this invalid test.

For any chosen triple of labels, embed a small disk containing exactly them, braid inside it, and keep the others vertical. Local meridians become conjugates of ambient meridians, retaining linear term X_i. Since the longitude begins in degree 2, substitution by such conjugates and conjugating the longitude itself preserve that leading degree; outside variables cannot appear there. Deletion to a different triple leaves at most two active strands and gives identity. Thus each coefficient d_ijh is isolated by a test with all linking zero and other distinct-index triples zero. This is valid for nonadjacent labels too.

For any pair, a thin disk neighborhood of an arc joining the two points and avoiding the finite other points supports a full twist. It changes that linking coordinate by 1 and no other. Integer powers and products realize the full lattice `Z^(choose(k,2))`. Once d's are killed by the triple tests, evaluation on this lattice kills Q: a polynomial over Q vanishing there is zero by repeated use of the one-variable root theorem. This is a proved finite-degree mechanism; it does not import all-order faithfulness or a converse characterizing braids by abstract free exterior.

## Separated insertion: written group and plat proof

Choose a proper base-disk arc δ cutting off exactly a chosen pair. A thin neighborhood of an embedded tree joining the pair to a boundary interval, avoiding all other points, constructs it even for nonadjacent labels. Put S in that subdisk×I and keep all other strands vertical in the complementary disk×I. The properly embedded separator Δ=δ×I is disjoint from strands and their chosen regular neighborhoods. Cutting the compact exterior along Δ gives E(S) and the trivial `(k-2)`-string exterior. Collar-open these pieces to apply van Kampen; their overlap deformation retracts to Δ, a disk. Hence

`π_1(E(J_ij(S))) ≅ π_1(E(S))*F_(k-2)`.

For S=L,L^s,R, this is F_k. At k=2 the outside piece has trivial group. No unspecified annulus gluing or stacking is involved, and deletion is not claimed to preserve freeness.

The active component values survive; inactive component values are zero. For the active pair, delete all other strands before choosing the standard caps. In the unpunctured endpoint disks the transported caps isotope to the chosen standard caps, retaining w_ij(S).

For one active and one outside strand, after deleting others arrange each top/bottom cap to cross δ once. Complete Δ through the outside closing ball to an embedded separating sphere. It meets the plat exactly twice, once on each cap, and cuts its two sides into the individual knot summands. Thus this plat is the connected sum of the component closures, possibly reversing a summand's orientation. Conway additivity yields `c(plat)=a_active+a_outside`; therefore w=0. Outside/outside pairs are trivial. This explicitly proves every cross-pair value used to isolate e_ij.

Evaluate a remaining `v=Σ b_i a_i+Σ e_ij w_ij` on J_ij(R). Its sole nonzero w-coordinate is w_ij=1, so e_ij=0. Next J_ij(L) and J_ij(L^s) give `b_i+5b_j=0`, `5b_i+b_j=0`. Determinant -24 forces both zero. Pairs (1,j) kill every component coefficient for k≥2. Therefore N_2(k)=0.

For k=2 the full six-row matrix with pure braids, R,L,L^s is block lower triangular after subtracting the first three rows' linking-polynomial interpolation from the final rows. The linking block determinant is 2. The remaining 3×3 block on `(a_1,a_2,w)` is

`[[0,0,1],[1,5,u],[5,1,v]]`,

whose determinant is -24 regardless of u,v. The complete determinant is -48, independently of r,s,t,u,v. The exact checker evaluates many rational negative controls; this written block argument proves the all-value identity.

## Limits of verification

The new checker certifies finite free-word, Magnus, rational determinant, and Alexander arithmetic. Source hashes certify which bytes were read. Neither certifies topology, the truth of cited classifications, or an algorithmic recognition of the Nogueira drawings. Those interfaces are separately justified above as mathematical source-backed and geometric arguments. The strongest verified conclusions are the three scoped degree-two claims stated at the beginning. This family supplies no conclusion about N_3 through N_6, no higher-order spanning theorem, no degree-seven promotion, and no novelty determination.

## Post-derivation adversarial addendum: unrestricted whiskers and k=1

After recording the independent derivation, I read the historical degree-two audits. Their fuller whisker formula prompted an additional direct check; no historical verdict was used to certify it. If a basing change introduces `Φ(q)q^-1`, every displayed conjugator has zero linear term and lies in Γ₂, so `Φ(x_j)=x_j mod Γ₃`. This holds for inactive generators as well. Consequently `Φ(q)q^-1∈Γ₃` for every q and cannot change the degree-two Milnor coefficients. The more general changed conjugator `Φ(q)c_jq^-1` is `(Φ(q)q^-1)(q c_jq^-1)`, whose leading quadratic term is still that of c_j. New explicit integer/Magnus checks include outside meridians and verify a nonzero degree-three control. The original supported-disk construction admits a whisker constant outside the braid support, but this unrestricted argument removes a possible hidden basing concern.

The k=1 exception is real and does not conflict with the theorem. Close a proper arc through a trivial arc in the outside ball. The overlap of the two arc exteriors is an annulus, whose fundamental group maps isomorphically to the outside solid-torus group; van Kampen therefore preserves the original arc group. A rank-one free group gives a cyclic closed-knot group. Fresh Papakyriakopoulos Theorem 3(i), printed p.170/PDF p.3, gives the unknot. The ordinary Conway coefficient vanishes on this test set and is nonzero on the trefoil. This verifies the stated boundary distinction without extending the k≥2 mechanism.

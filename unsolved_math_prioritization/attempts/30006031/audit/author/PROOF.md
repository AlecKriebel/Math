# Five scoped approaches and the remaining gap

## Scope and conventions

The desired conclusion is an action of an operad with the homotopy type of the unframed little 3-disks operad on the intended operadic homotopy center. The word "action" must be distinguished from a commutative multiplication on components, an E2 action, and an action on a replacement of the underlying homotopy type. An E3 algebra need not be group-like. A triple loop space with its usual multiplication is group-like.

Write D_n for the unital topological little n-disks operad, including the empty configuration in arity zero. An E_n operad means an operad weakly equivalent to D_n in a suitable operadic homotopy theory. Our topological examples use compactly generated spaces; our strict algebraic examples use sets. These are conventions for the arguments below, not hypotheses recovered from the OWR conjecture. A weak equivalence of spaces does not by itself install a literal D_3 action on a chosen point-set model.

The primary definition gap in `SOURCE_GATE.md` is operative throughout. None of the independently defined centers below is asserted to equal the report's homotopy center.

## Approach 1  Strict central unary operations

For a one-colored nonsymmetric operad P in sets with its usual unary identity, define

Z_u(P) = {z in P(1) : z composed with p = p composed with (z,...,z) for every n >= 0 and p in P(n)}.

Here n=0 is included: z composed with a nullary operation must equal that nullary operation. Empty arities are allowed. Operadic unitality means the unary identity exists; it does not require a chosen nullary operation or a multiplicative map from the terminal nonsymmetric operad Ass.

### Proposition 1

Z_u(P), with unary composition, is a commutative unital monoid. As a discrete space it admits an action of D_n for every n >= 1, with multiplication its unary composition.

**Proof.** The operadic identity is central. If x and y are central and p has arity n, associativity and the two centrality equations give

(xy)p = x(yp) = x(p(y,...,y)) = (xp)(y,...,y) = p(xy,...,xy).

This also holds for n=0, since then both sides equal p. Thus Z_u(P) is closed under composition. For x,y in Z_u(P), apply centrality of x to the unary operation y to obtain xy=yx. Associativity and the identity are inherited from P(1).

There is a unique map of operads D_n -> Com, where Com has one operation in every arity. Define Com's k-ary operation on Z_u(P) to be the product of k entries and its zero-ary operation to be the identity. The commutative monoid axioms prove all operad axioms; precomposition supplies the asserted D_n action. Since the operation is independent of the disk configuration and the center is discrete, continuity is immediate. QED.

### Exact scope and failed extension

For an arbitrary monoid M, define its unary operad U(M) by U(M)(1)=M and U(M)(n)=empty for n!=1. Then Z_u(U(M)) is exactly the ordinary monoid center. U(M) is a unital nonsymmetric operad, but there is no map Ass -> U(M), because Ass(2) is nonempty and U(M)(2) is empty. Thus "unital operad" cannot be silently replaced by "multiplicative operad."

For the full endomorphism operad of a nonempty set X, each x in X is a nullary operation. The n=0 centrality condition forces z(x)=x for every x. Hence its strict unary center is the singleton identity. This is a useful nullary boundary test, not a derived computation.

This approach settles only the explicitly defined strict object. Homotopy coherence involves more than strict equations: replacing an equalizer by a derived construction may introduce additional components and higher homotopy. No equivalence between Z_u(P) and the target homotopy center has been constructed. Consequently the easy E-infinity action above does not answer the question.

## Approach 2  Triple delooping and its group-like limitation

Let Z be a specified space. Suppose there are a pointed space Y and an equivalence of homotopy types Z ~= Omega^3 Y. Then the homotopy type of Z has an E3 structure. This statement is about transported structure, not a strict point-set action on an arbitrary chosen representative.

**Construction.** Represent Omega^3 Y by based maps from I^3/partial I^3 to Y. For k disjoint little 3-cubes inside I^3, insert k such maps on the cubes using their affine coordinates, and send their complement to the basepoint. Boundaries match because every input is based on its boundary. Nested affine inclusions give exactly the operad composition law; the unit cube gives the identity and the empty configuration gives the constant map. This is the standard little-cubes action. Little cubes give an E3 model. Transport the algebra object across the specified equivalence in the infinity-category of spaces. If one wants a strict algebra on a replacement, the chosen operadic model category and its admissibility/transfer hypotheses must be supplied separately.

If Z and Y vary in a category and the equivalence is a coherent natural equivalence to the triple-loop functor, this construction is natural after transport. Unrelated objectwise equivalences do not establish this stronger statement.

The literature reduction in `SOURCE_GATE.md` produces such a triple loop space from certain multiplicative hyperoperads. To apply it here one must actually construct, for every target P, a hyperoperad A_P and a comparison between the intended Z_h(P) and its homotopy limit, verify the required contractibility and retraction conditions, and prove the necessary naturality. None of these follows from saying that nonsymmetric operads are one stage in the Baez-Dolan sequence.

### Proposition 2  A limit on this proof strategy

Suppose a candidate center assignment Z_h comes with a specified multiplication and, for the unary operad of the additive monoid N, its monoid of components is N with addition. Then Z_h(U(N)) is not equivalent as a multiplicative homotopy type to a triple loop space with its loop multiplication.

**Proof.** The monoid of components of Omega^3 Y is pi_3(Y), a group (indeed abelian). The monoid N has no additive inverse for 1. An equivalence preserving multiplication would give a monoid isomorphism between these two component monoids, impossible. QED.

The premise concerning pi_0 is explicitly conditional and is not attributed to the undefined center in the report. Nor does this rule out an E3 action: N itself, as a commutative discrete monoid, is an E-infinity algebra. It rules out the indiscriminate replacement of a potentially nongroup-like center by an ordinary triple loop space while preserving the stated product. Group completion would change that problem.

## Approach 3  Condensation, missing fibers, and an indexing control

This approach uses the circled-tree construction in the 2025 paper, qualified in `SOURCE_GATE.md`. Its three pairwise positions are horizontal separation, vertical separation, and containment. On a linear tree there is only one branch, so two subtrees cannot be horizontally separated. Consequently the category of binary circled-tree configurations constrained to have horizontal complexity at most zero is empty. Its nerve is empty and cannot be weakly equivalent to a point. This is the paper's Remark 3.6 obstruction, recast as the precise failed hypothesis of the proposed fiberwise argument. It does not prove that every possible E3 construction fails, nor that the total condensation has a particular homotopy type.

The following independent calculation protects against an off-by-one reinterpretation of the same paper.

### Proposition 3  Binary level posets

For q>=1, let P_q have elements (r,s), with 0<=r<q and s in {+,-}. The only strict order relations are (r,s)<(t,u) when r<t. Then the order complex of P_q is homeomorphic to S^(q-1). In particular P_2 has H_1=Z, while P_3 has H_1=0 and H_2=Z.

**Proof.** A nonempty chain chooses some nonempty subset of the q levels and exactly one of the two elements at each chosen level. This is precisely the abstract join of q copies of the discrete two-point complex S^0. More concretely, map (r,+) to the r-th positive coordinate vector and (r,-) to its negative in R^q. The possible simplices are exactly the boundary faces of the q-dimensional cross-polytope: a face contains no antipodal pair. This gives a simplicial identification with its boundary, homeomorphic to S^(q-1) by radial projection. The integral homology follows. QED.

For q=2 label the first-level vertices a,b and the second-level vertices c,d. The chain

z=[a,c]-[b,c]+[b,d]-[a,d]

is a 1-cycle. There are no 2-simplices, so this nonzero chain is not a boundary. In P_3 let e be either third-level vertex. Then

t=[a,c,e]-[b,c,e]+[b,d,e]-[a,d,e]

satisfies boundary(t)=z, by direct cancellation. Thus adding the third level kills the displayed degree-one class. This integral chain identity is independently reproduced by the verifier.

The arity-two complete-graph order in the cited paper is P_q when its set of allowed labels has q elements. The visually checked page 4 prints K_m labels {0,...,m}; taken literally this gives K_2(2)=P_3. The visually checked page 8 calls B(K_2) an E2 operad. Those two statements are incompatible, since D_2(2) has the homotopy type S^1, not S^2. Using q actual levels avoids the ambiguity. The natural dimension convention for an E_m binary model uses m levels, such as {0,...,m-1}; that is an explicit normalization here, not a claim that the source was corrected.

Neither this indexing issue nor its repair yields an E3 action. In particular the empty horizontal fiber remains empty. The finite calculations verify the poset statements only; they do not verify the entire condensation theorem or compute the target center.

## Approach 4  Why an E2 action cannot simply be upgraded

Dunn additivity is useful only after supplying actual coherently commuting actions, equivalently an algebra over the appropriate derived Boardman-Vogt tensor of E1 and E2 operads, together with a suitable additivity equivalence to an E3 model. This is additional structure. Associativity, commutativity on pi_0, or an E2 action alone does not supply it. The following elementary obstruction is stronger than a warning by analogy.

### Proposition 4  A concrete obstruction to extension

There exists a D_2 algebra whose specified D_2 action does not extend, even up to homotopy on binary evaluation, to a D_3 action along the standard inclusion D_2 -> D_3.

**Proof.** Let X={a,b} be a discrete two-element space, and let F be the free unital D_2 algebra on X:

F = coproduct over k>=0 of D_2(k) times_(Sigma_k) X^k.

The generators a,b lie in the k=1 summand via the identity unary disk. In the k=2 summand, the part with one a label and one b label is homeomorphic to D_2(2): every orbit has a unique representative with label ordering (a,b), since the two labels are distinct. Binary evaluation at (a,b) is exactly this homeomorphism onto that summand. The summand is open and closed in F, so its nonzero H_1 injects into H_1(F;Z).

For n>=2, D_n(2) is homotopy equivalent to the ordered configuration space of two centers in the open n-ball: the possible positive radii over fixed distinct centers form a nonempty convex set, and a continuous small-radius section contracts the fibers. The open ball is homeomorphic to R^n, whose two-point configuration space is R^n times (R^n minus {0}), up to the usual midpoint-and-difference coordinates. It follows that D_n(2) ~= S^(n-1). In particular H_1(D_2(2);Z)=Z and H_1(D_3(2);Z)=0.

If the D_2 action were the restriction of a D_3 action, evaluation at (a,b) would factor as

D_2(2) -> D_3(2) -> F.

This composite is zero on H_1 because the middle H_1 vanishes. The actual evaluation is nonzero on H_1 by the mixed-label summand description. The contradiction remains if the evaluations agree only up to homotopy, since homotopic maps induce the same map on homology. QED.

This is not a counterexample to the OWR problem: F has not been realized as its intended homotopy center. It also does not forbid an unrelated E3 action on the underlying space. It disproves the proposed automatic extension of an existing E2 action. To use the 2025 E2 result as input to the target question, a genuine additional compatibility construction or some center-specific vanishing mechanism is required.

The conditional additivity route is therefore blocked at exactly that construction, rather than completed by renaming the tensor product or appealing to iterated centers.

## Approach 5  Naturality and the newer Swiss-cheese route

The later Swiss-cheese source offers a broad Hochschild construction, described in `SOURCE_GATE.md`. Its E3 conclusion requires an actual E2 algebra input and the particular Hochschild object in its theorem. A collection P(n) carrying nonsymmetric operad substitutions is not, merely by that fact, a specified one-colored E2 algebra. Applying a colored construction to the operad encoding nonsymmetric operads does not make that encoding operad weakly equivalent to a one-colored E2 operad. No requisite comparison of these inputs or their Hochschild objects was established here.

Even the naturality required of a proposed comparison must be stated carefully. It is not automatically covariance under all operad maps with the evident action on central elements.

### Proposition 5  The naive covariance requirement fails

There is no functor on all monoids that assigns to M its ordinary center as a submonoid of M and sends each central element z along an arbitrary homomorphism f:M->N to f(z).

**Proof.** Let G=S_3 and let H={identity,(12)} be its order-two subgroup. H is abelian, so (12) belongs to Z(H). Its image under inclusion into S_3 is not central: (12)(23) and (23)(12) are distinct 3-cycles. Thus the proposed image does not belong to Z(S_3), so the claimed map Z(H)->Z(S_3) is not even well-defined. QED.

The corresponding unary operads give the same obstruction for the strict center in Approach 1. It does not prohibit a different higher functoriality involving bimodules, correspondences, or changes of coefficients, and the OWR report does not assert this naive covariance.

There are useful positive controls. A surjective monoid map sends central elements to central elements because every target element has a preimage. More generally a levelwise surjective map f:P->Q of set-valued nonsymmetric operads sends Z_u(P) into Z_u(Q): lift an arbitrary q in Q(n) to p in P(n), apply centrality upstairs, and apply f. An operad isomorphism induces an isomorphism of these strict centers, by also applying the inverse. Composition is preserved. These restricted naturality statements are proved, whereas covariance for all maps is false.

This approach does not supply the absent homotopy-center comparison or its coherent naturality. Its exact contribution is to distinguish a legitimate restricted comparison from an impossible naive one.

## The unresolved mathematical task

No tested approach establishes the requested action. A complete solution needs all of the following:

1. A precise definition of the intended Z_h(P), including enrichment, arity-zero and unit conventions, weak equivalences, and the derived replacement construction.
2. A construction of an E3-operad action on that object or a clearly specified equivalent model, with operadic substitution, units, symmetry, and all homotopy coherences.
3. An explicit comparison to any hyperoperad, Hochschild, or iterated-center model used, with its additional hypotheses proved for every P in the proposed scope.
4. If naturality is asserted, its actual domain and variance and a coherent comparison there. If an existing multiplication or E2 action must be extended, a proof of that compatibility.

The five families above provide constraints and conditional reductions. They are not five proofs of special cases of the undefined derived center. No full solution, general counterexample, historical priority, or novelty is claimed.

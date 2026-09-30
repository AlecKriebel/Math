# A cofiber criterion and a free-group example for the isomorphism S-construction

**Target:** 30005678 / OWR-14297744-011.  
**Status:** candidate partial result; separate adversarial review pending.  
**Scope:** the simplicial space obtained from the maximal groupoids of the ordinary Waldhausen S-construction. No classification for arbitrary weak-equivalence realizations is claimed. Priority is unestablished.

## 1. Source and conventions

The imported target asks for a characterization of fully 2-Segal Waldhausen S-constructions and natural left-but-not-fully-2-Segal examples. The underlying contribution is Julie Bergner, *General inputs for the S•-construction*, [OWR 34/2023, pp. 1945–1946](https://ems.press/content/serial-article-files/47483?nt=1). Its question is an open-ended discussion of extending the construction from exact to Waldhausen inputs, rather than a formally quantified characterization problem. “Fully” means the comparison for **every triangulation of a polygon**, not an iterated or multidirectional S-construction. The source does not specify which weak-equivalence variant is intended.

This distinction matters. Carawan's [2024 paper](https://arxiv.org/abs/2405.11561), §§7–9, treats the groupoid realization, the categorical constructions, and arbitrary weak-equivalence realizations separately. Proposition 7.1 proves the left condition for the groupoid realization; Proposition 7.7 gives only a reduction under additional hypotheses for general weak-equivalence realizations. Proposition 9.1 supplies a sufficient pullback/pushout criterion for the categorical construction. We use the first result and do not transfer the other conclusions between variants.

Let C be an essentially small **category with cofibrations**: it has a zero object 0, all isomorphisms and maps 0→A are cofibrations, cofibrations compose, and the pushout of a cofibration along any map exists and is a cofibration. No monomorphism, exactness, cylinder, or factorization axiom is assumed. Work in a small equivalent model if necessary.

An object of S_n C is the usual array A_ij, 0≤i≤j≤n, with A_ii=0, horizontal arrows cofibrations, and the squares expressing A_ik/A_ij≅A_jk pushouts. Write G_n=(S_n C)^≃ for its maximal groupoid and X_n=N G_n for its nerve, regarded as a space. Thus X• models |iS• C|. If weak equivalences are precisely isomorphisms it also models |wS• C|.

For a triangulation T of the ordered polygon 0,…,n, X(T) is the homotopy limit of its triangle, edge, and vertex diagram. The comparison X_n→X(T) uses the face maps. “Left 2-Segal” here means equivalence for the fan with all diagonals incident to 0, in every degree. “2-Segal” requires this for every T. All limits of spaces below are homotopy limits.

## 2. An exact cofiber-factorization criterion

Fix a cofibration i:A→X and a choice of quotient q:X→X/A=0⊔_A X.

Define two groupoids, using only C and its cofibrations:

* Fact(i) has objects A —u→ C —v→ X with u,v cofibrations and vu=i. A morphism is an isomorphism θ:C→C′ with θu=u′ and v′θ=v.
* Sub_cof(X/A) has objects cofibrations j:B→X/A. A morphism from j to j′ is an isomorphism β:B→B′ with j′β=j.

Taking the quotient by A defines

    Q_i : Fact(i) → Sub_cof(X/A),   (A→C→X) ↦ (C/A→X/A).

Indeed, the square with top C→X and bottom C/A→X/A is a pushout, by the universal property of these quotients. Its bottom arrow is a cofibration. Choices of quotients give canonically isomorphic functors and do not affect equivalence.

**Theorem 1.** X• is 2-Segal if and only if Q_i is an equivalence of groupoids for every cofibration i in C.

The criterion requires both existence and the complete isomorphism-lifting condition; merely finding one intermediate C for each j is insufficient. It is a small-diagram criterion, not an algorithm or a list of all such categories.

### Proof, step 1: the quadrilateral comparison

Forgetting quotient entries gives equivalences

    G_2 ≃ {cofibrations A→X and their isomorphisms},
    G_3 ≃ {two composable cofibrations A→C→X and their isomorphisms}.

To verify this, reconstruct each missing entry as a pushout by 0. Its possible choices form a contractible groupoid, and every map between the first-row diagrams extends uniquely to the quotient entries. This is also Carawan's Lemma 7.2.

The comparison for the diagonal 13 of the quadrilateral 0123 is

    Φ : G_3 → G_{013} ×^(2)_{G_{13}} G_{123},

where ×^(2) denotes the groupoid 2-pullback: its objects include an isomorphism between the two copies of the shared edge. Its nerve models the homotopy pullback of nerves. By transporting along that isomorphism and then forgetting quotient choices, its target is equivalent to the groupoid E of pairs

    (i:A→X, j:B→X/A),

where i and j are cofibrations. An isomorphism in E consists of isomorphisms on A, X, and B commuting with i and j, with the map on X/A induced by those on A and X. Under these equivalences Φ sends the chain A→C→X to (i,C/A→X/A).

Both the chain groupoid and E project to the groupoid K of cofibrations i:A→X and isomorphisms between them. These projections are isofibrations. For the chain projection, transport along (a:A→A′,x:X→X′) by replacing u with ua⁻¹ and v with xv. For E, transport j by the induced isomorphism X/A→X′/A′. Quotient choices can equivalently be retained throughout; their contractible groupoids make no difference. Their fibers over i are Fact(i) and Sub_cof(X/A), and the induced fiber functor is Q_i.

For completeness, a functor between groupoids over K, with both projections isofibrations, is an equivalence exactly when all these fiber functors are equivalences. In one direction, essential surjectivity in a fiber follows from total essential surjectivity followed by transport along its isomorphism in K; total full faithfulness then gives full faithfulness in the fiber. In the other direction, transport an arbitrary arrow in K to reduce its lifting to a fiber. Fiber full faithfulness lifts every target isomorphism uniquely, and fiber essential surjectivity gives total essential surjectivity. Thus Φ is an equivalence if and only if every Q_i is.

### Proof, step 2: why one quadrilateral condition suffices here

We use the following elementary polygon lemma.

**Lemma.** If a simplicial space is left 2-Segal in every degree, it is 2-Segal if and only if the comparison for the other diagonal of 0123 is an equivalence.

Only sufficiency needs proof. Both comparisons from X_3 to the two triangulations of a quadrilateral are then equivalences. Suppose T and T′ differ by flipping one diagonal. Erase that diagonal, leaving a dissection D with one quadrilateral and all its other cells triangles. Define X(D) using X_3 on that quadrilateral and X_2 on the remaining triangles, glued over their common edges and vertices. The maps

    X(D) → X(T),     X(D) → X(T′)

are equivalences: each replaces only the quadrilateral by its two-triangle homotopy limit. This is a homotopy base change of the corresponding degree-three comparison, with the same boundary-edge maps. Homotopy limits preserve equivalences of diagrams. The maps from X_n to these three membrane spaces commute. Hence if X_n→X(T) is an equivalence, so are X_n→X(D) and X_n→X(T′), by two-out-of-three.

Every polygon triangulation is connected to the fan at 0 by flips. One direct proof is to consider a nonboundary edge on the frontier of the union of triangles incident to 0. Its two incident triangles form a quadrilateral. Flipping that edge adds an edge incident to 0 and removes none already incident to 0. If the triangulation is not a fan such a frontier edge exists. The finite number of diagonals makes this process terminate at the fan. Starting from the left comparison, propagate its equivalence along these flips. This proves the lemma.

Carawan's Proposition 7.1 gives the needed left comparisons for X•. In the present groupoid model this can also be seen directly: G_n is the groupoid of first-row chains A_01→A_02→⋯→A_0n, while the fan membrane consists of precisely these successive cofibrations, with isomorphisms identifying each adjacent shared object. Transport along those isomorphisms turns such data into a chain, uniquely up to its groupoid of isomorphisms. Thus the fan comparison is an equivalence. Step 1 and the lemma prove Theorem 1. ∎

### Monomorphism specialization

Suppose all cofibrations of C are monomorphisms. Every morphism in either of the two groupoids defining Q_i is then uniquely determined if it exists, and every automorphism is the identity. Thus both groupoids are equivalent to discrete sets of isomorphism classes.

Consequently, in this case Theorem 1 says precisely that taking C/A gives a **bijection** from intermediate cofibration subobjects A→C→X to cofibration subobjects of X/A. Here “intermediate” requires both arrows to be cofibrations, and the isomorphism class is taken under the fixed A and over the fixed X. This does not mean taking isomorphism classes of unmarked flags before fixing A and X.

## 3. A natural algebraic example

Let F be the category of finitely generated free groups and **all group homomorphisms**. Its zero object is the trivial group. A cofibration is a homomorphism isomorphic, under its source, to the standard inclusion

    A → A * F_r,     r≥0.

Equivalently, it is an injective map whose image is a free factor with finite-rank free complement. Specify weak equivalences to be isomorphisms.

**Proposition 2.** This is a Waldhausen category. Its simplicial space |iS• F|=|wS• F| is left 2-Segal but is not 2-Segal.

### Verification of the Waldhausen axioms

The trivial group is both initial and terminal. Every map from it to a finite-rank free group and every isomorphism is a cofibration. Composing A→A*F_r with an inclusion into (A*F_r)*F_s again gives a free-factor inclusion, proving composition closure after transport by isomorphisms.

For an arbitrary homomorphism f:A→B the pushout of A→A*F_r along f is B*F_r: a homomorphism from B*F_r to a group D is exactly a homomorphism B→D and a homomorphism F_r→D, equivalently a compatible cocone on the original span. This is a finite-rank free group when B is one, and B→B*F_r is a cofibration. Thus the required pushouts exist in F. Isomorphisms compose, contain all isomorphisms, and satisfy the Waldhausen gluing axiom, since an isomorphism of pushout spans induces an isomorphism of pushouts. No cylinder axiom is being imposed or asserted.

### Two intermediate subobjects with identical quotient data

Use free bases

    A=F(a),    C=F(a,d),    X=F(a,b,c),
    B=F(b),   Y=F(b,c),    Z=F(c).

Let u:A→C send a to a. Define two embeddings

    v₀(a)=a,  v₀(d)=b,
    v₁(a)=a,  v₁(d)=b[c,a],       [c,a]=cac⁻¹a⁻¹.

Both are cofibrations: v₀ is standard, and v₁=αv₀, where

    α(a)=a,   α(b)=b[c,a],   α(c)=c

is an automorphism of X. Its inverse fixes a,c and sends b to b[c,a]⁻¹. Also v₀u=v₁u is the same inclusion i:A→X.

For both factorizations the map C/A→X/A is exactly the inclusion B=F(b)→Y=F(b,c), identifying the image of d with b. Indeed, after killing a the commutator [c,a] becomes trivial. Likewise both quotients X/v_k(C) are Z=F(c): the normal closure of a and b[c,a] equals the normal closure of a and b. These statements follow directly from the displayed relations, not from an abelianized calculation.

The two objects of Fact(i) are not isomorphic. An isomorphism over X would identify their images. But the reduced word

    b c a c⁻¹ a⁻¹

belongs to v₁(C) and does not belong to the subgroup <a,b>=v₀(C), since a reduced word in that free factor uses no c or c⁻¹. Thus Q_i is not full: the identity between its two identical image objects has no preimage. Theorem 1 shows the failure of 2-Segality. Left 2-Segality is the general result of Carawan.

### Explicit missing loop in the homotopy comparison

The same defect can be seen without using Theorem 1. Start with the S_3 flag given by v₀. Its right-triangulation data are

    (A→X→Y,  B→Y→Z).

The automorphism α of X above, together with the identity on A, B, Y, and Z, is an automorphism of this data: α fixes A pointwise and becomes the identity after quotienting by A. It therefore gives an automorphism in the groupoid 2-pullback, with identity on its shared-edge identification.

If this automorphism lifted to the S_3 flag, its component θ on C would satisfy v₀θ=αv₀. Evaluating at d would put b[c,a] in <a,b>, a contradiction. Hence the comparison functor is not full. A functor between groupoids induces a weak equivalence of nerves exactly when it is an equivalence of groupoids; equivalently, this displayed target automorphism is missing from the induced map of fundamental groups at the chosen flag. This directly proves the assertion for the homotopy pullback of spaces.

The distinction about markings is essential. The two complete flags **are** isomorphic if the ambient map on X is allowed to be α. That observation does not lift the identity of the fixed target data, and does not repair the missing automorphism. We make no claim that these are different unmarked isomorphism classes of flags.

## 4. Extent of the result and remaining target

Theorem 1 is a necessary-and-sufficient criterion for the isomorphism-groupoid S-construction of every category with cofibrations. Proposition 2 supplies a natural left-but-not-fully-2-Segal Waldhausen example, with the failure already in a rank-three free group. The example also applies to the weak-equivalence realization because its specified weak equivalences are exactly isomorphisms.

For a general Waldhausen category with a larger class w, the realization |wS_n C| need not be a groupoid nerve. Isomorphism lifting in Q_i does not control its homotopy fibers, and categorical 2-pullbacks do not automatically compute the required homotopy pullbacks of spaces. We have not proved a criterion for those arbitrary |wS• C|. In particular, we do not assume their left condition merely from the Waldhausen axioms.

Accordingly, the broadly phrased imported characterization remains **unresolved/source-qualified**, despite the complete criterion for the explicitly stated iS variant and the example. No classification of all enhanced homotopical variants, recognition algorithm, minimal rank, or novelty claim is made. The elementary polygon argument and the criterion may have prior formulations; the targeted literature search did not establish priority.

## 5. Exact checks and their limits

The accompanying standard-library verifier checks free-group substitutions, inverse automorphisms, quotient maps, and the non-lifting word, and checks small polygon flip graphs. It also checks the corresponding positive interval property for finite pointed sets with injective cofibrations. These are diagnostics for the displayed constructions. They do not prove the all-degree categorical theorem, the universal Waldhausen axioms, or a current-literature absence claim; the proofs above carry those mathematical assertions.

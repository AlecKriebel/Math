# Coxeter boundaries of rational dimension one: frozen partial results

## Disposition and exact scope

**Original research target unresolved. Five substantive approaches completed. No solution, counterexample to the general existence question, or novelty claim.** This is an author packet awaiting independent audit.

The target is UnsolvedMath 6200010 / AMR-061-0010, rank 807. The 2005 date refers to the AIM workshop. The inspected Kapovich PDF is dated October 24, 2007; its printed page 4, Section 3, Problem 10 concerns a finitely generated Coxeter system and the visual boundary of its Davis complex. In normalized notation the objective is to obtain groups W_n with

    dim(∂Σ(W_n)) = n,       dim_Q(∂Σ(W_n)) = 1,

in the nontrivial range n ≥ 3, and ultimately unbounded/arbitrary n. The source's preceding paragraph already provides dimension-two examples. Dranishnikov's original 1997 paper explicitly identifies n ≥ 3 as the unresolved range. Consequently a dimension-one circle or a known dimension-two Pontryagin example is not treated as resolving this question.

Here dim is covering dimension; dim_R is relative Čech cohomological dimension. This clarifies the workshop list's phrase “rational homological dimension.” The question does **not** require W_n to be Gromov hyperbolic. Imposing a no-induced-square condition would unnecessarily narrow the task. No result below confuses a CAT(0) visual boundary with an arbitrary compactum or with the nerve itself.

The exact live problem URL returned an access error in the web tool and HTTP 403 in a read-only download. Its current rendered wording/status was not verified. The complete supplied archive record, its report, and catalogue hashes match the expected identity; the actual mathematical statement and surrounding conventions were independently recovered from the primary PDF and page 4 was visually inspected. No current published resolution of the n ≥ 3 target was found in the scoped literature search. This is a search outcome, not a proof of worldwide open status.

## Imported facts and notation

Let L be the finite spherical nerve of a Coxeter system W. For a simplex σ of L, including the empty simplex, write L−σ for the full subcomplex on vertices outside σ. Its realization is a deformation retract of the complement of the closed geometric simplex: normalize the barycentric coordinates outside σ. For R = Z or Q put

    D_R(L) = max { j : reduced H^j(L−σ;R) ≠ 0 for some σ in L }.

Only nonnegative and positive degrees are used in the obstructions below. The empty-complex degree −1 convention handles finite groups in the standard formula.

We import the Coxeter compact-support formula and the boundary formula:

    vcd_R W = D_R(L)+1,       dim_R(∂Σ(W)) = vcd_R W−1.       (1)

They are credited to Bestvina, Bestvina–Mess, Davis, and Dranishnikov, as set out in Davis §8.5 and Dranishnikov's work. Coxeter groups have torsion-free finite-index subgroups of finite type, so the indicated virtual dimensions and coefficient changes are available. For finite-dimensional compact metric boundaries, dim_Z equals covering dimension. We apply these results in their stated finite-rank Coxeter setting; we do not re-prove the entire Davis-complex theorem.

Thus the precise missing construction is a finite spherical nerve L with

    D_Q(L)=1,        D_Z(L)=n≥3.                            (2)

A finite flag complex suffices to provide such a nerve, through its right-angled Coxeter group. General nerves need not be flag.

## Approach 1: induced-subcomplex detection and the regularity formulation

A tempting simplification is to inspect only the global cohomology of L. It is insufficient. A stronger useful reformulation is to allow every induced subcomplex, while retaining the **maximum degree**, rather than individual puncture data.

**Proposition 1.** For a finite Coxeter nerve L and R = Z or Q,

    D_R(L) = max { j : reduced H^j(L|U;R) ≠ 0 for U⊆V(L) }. (3)

**Proof.** Every deleted-simplex complex is induced, so the left side is at most the right. Conversely W_U is a special subgroup of W and has nerve L|U. Choose a torsion-free finite-index subgroup Γ of W. The subgroup Γ∩W_U has finite index in W_U. Restricting an RΓ-projective resolution to R[Γ∩W_U] preserves projectivity, since the larger group ring is free over the smaller one. Hence vcd_R(W_U)≤vcd_R(W). If H̃^j(L|U;R)≠0, the empty-simplex term in (1) for W_U yields j+1≤vcd_R(W_U)≤vcd_R(W). This proves the other inequality. □

This is consistent with Constantinescu–Kahle–Varbaro (CKV), Theorem 5.2 and equation (8); their combinatorial theorem applies more generally. By Hochster's interpretation, the rational invariant D_Q+1 is reg Q[L]. The original construction goal can therefore be expressed as a finite spherical nerve whose rational Stanley–Reisner regularity is 2 but whose maximum field regularity is n+1. In the right-angled case the nerve must be flag. Changing a coefficient field, or producing high regularity without holding rational regularity fixed, does not solve this goal.

A clarification to the related public 6200004 packet is warranted: its Turn 2 warns that arbitrary vertex deletion changes the invariant. Individual puncture collections do change, but their maximum nonvanishing degree agrees by (3). Its actual deleted-simplex computations and previously stated exclusions are unaffected. We have not edited that earlier packet.

**Outcome.** Exact alternative search criterion and an efficient lower-bound witness. No suitable high-dimensional rationally 2-Leray flag complex was produced. Characteristic-sensitive examples of dimension two remain baseline examples only.

## Approach 2: singular manifold-link nerves

This approach investigates the proposed extension of nonorientable surface nerves to three-dimensional singular complexes. It gives the strongest retained obstruction.

**Theorem 2.** If a finite, three-dimensional simplicial complex L has every vertex link a closed connected triangulated surface, then D_Q(L)≥2 whenever L is a Coxeter nerve. In particular its Coxeter boundary cannot have rational dimension one.

The hypothesis permits singular vertices with nonorientable links; it is strictly broader than the closed-manifold-nerve case. The assertion is componentwise, so assume L connected.

**Case A: an orientable vertex link.** Let v have orientable link A. Then H²(A;Q)≠0. The relative cohomology identification for the star of v gives

    H³(L,L−v;Q) ≅ H̃²(A;Q) ≠ 0.

The exact sequence contains

    H²(L−v;Q) → H³(L,L−v;Q) → H³(L;Q).

Therefore H²(L−v;Q) or H³(L;Q) is nonzero. Both are allowed terms in D_Q(L), proving D_Q(L)≥2. No assumption that a non-right-angled link is full is needed.

**Case B: every vertex link is nonorientable.** Write f_i for the number of i-simplices and V=f_0. Every triangle lies in precisely two tetrahedra: fix one of its vertices and use the two-triangle incidence of the corresponding edge in that vertex's closed surface link. Thus f_2=2f_3. Counting link simplices gives

    Σ_v χ(lk_L v) = 2f_1−3f_2+4f_3 = 2f_1−2f_3,
    χ(L) = V − (1/2) Σ_v χ(lk_L v).                       (4)

A connected closed nonorientable surface has Euler characteristic at most one. Consequently χ(L)≥V/2. A three-dimensional simplicial complex has V≥4, so χ(L)≥2.

Also H_3(L;Q)=0. Indeed, a rational simplicial 3-cycle restricts at each vertex to a rational 2-cycle in its link: the signed coefficients of tetrahedra incident to v become those of their opposite triangles. The boundary-zero equations at triangles containing v are exactly the link's cycle equations. A nonorientable closed surface has no nonzero rational top cycles. Therefore all incident tetrahedron coefficients vanish at every vertex, and the original cycle is zero.

For rational Betti numbers, connectedness and (4) now give

    b_2(L) = χ(L)−1+b_1(L) ≥ V/2−1+b_1(L) > 0.           (5)

The empty-simplex term proves D_Q(L)≥2. This completes the proof. □

**All-projective-plane links.** If every link is RP², equality holds in (4), yielding χ(L)=V/2 and b_2(L)=V/2−1+b_1(L). In particular V is even. Such a simplicial complex cannot simultaneously have vanishing rational H². This addresses the specific link-prescription avenue in Dranishnikov's 1997 discussion; it is not a proof that every singular nerve is excluded.

### Extension to isolated PL singularities

A useful deletion lemma avoids hidden fullness assumptions. If v is a vertex and σ is a simplex of lk_L(v), let X=L−σ and A=lk_L(v)−σ. Relative cohomology and the exact sequence give

    H^j(X−v;Q) → H^{j+1}(X,X−v;Q)≅H̃^j(A;Q)
                         → H^{j+1}(X;Q).

A nonzero middle term forces one of the outer terms to be nonzero. Since σ and σ∪{v} are simplices of L, both are admissible punctures. Thus

    D_Q(L) ≥ D_Q(lk_L v).                                (6)

Here D_Q is defined by punctures for any finite complex; (6) is topological, before assuming it is a Coxeter nerve. Repeated application gives the same inequality for links of any face, in the positive degrees used here.

Suppose dim L=d≥4 and every vertex link is a closed PL (d−1)-manifold. For any edge e, its link is a PL sphere S^{d−2}: it is a vertex link inside a PL vertex-link manifold. Equations (6) and the empty puncture in lk_L(e) imply

    D_Q(L)≥d−2≥2.                                       (7)

Together, Theorem 2 and (7) exclude every nerve of dimension at least three with only isolated PL-manifold-link singularities. They do not cover arbitrary non-manifold links or non-isolated singularities.

### Exact finite model

The checker builds a six-vertex triangulated RP² and the cubical subcomplex of [0,1]^6 whose active-coordinate sets are its simplices. There are 64 vertices and cell counts (64,192,240,80). Each vertex has link RP². Compatible ordered-coordinate triangulations produce a genuine simplicial complex with f-vector (64,512,960,480), 480 tetrahedra, and all 64 vertex links triangulated RP². The code checks every link's surface conditions.

The integer cubical boundaries square to zero. Exact modular elimination gives boundary ranks (63,129,80) over F_3 and F_101 and (63,129,79) over F_2. The F_101 ranks also **certify rational ranks**: augmentation bounds the first rank by 63, the chain identity then bounds the second by 192−63=129, and the third has only 80 columns. Modular lower bounds attain all these rational upper bounds. Consequently

    b_*(L;Q)=(1,0,31,0),        b_*(L;F_2)=(1,0,32,1).

This exhibits exactly the unavoidable rational H² in the all-RP²-link route. We do not claim this triangulation is flag, has the desired Coxeter boundary, or supplies a solution. It is a topological control for the no-go theorem.

The checker also suspends RP². That control has no global rational H² but contains sphere vertex links. It illustrates why Case A is necessary and why the all-nonorientable hypothesis in (5) must not be dropped.

## Approach 3: flagifying high-dimensional torsion complexes

One might start with a finite complex carrying high integral torsion but little rational global cohomology, then barycentrically subdivide it to obtain a right-angled nerve. This fails before any hyperbolicity issue arises.

**Theorem 3.** If K is a finite simplicial complex of dimension d≥1 and L=sd K, then D_Q(L)≥d−1. Consequently a barycentric right-angled nerve with D_Q(L)=1 has d≤2, and its integral boundary dimension is at most two.

**Proof.** Choose a d-simplex τ of K. In sd K select exactly the vertices corresponding to nonempty proper faces of τ. A simplex on those vertices is precisely a chain of such faces. Thus the induced complex is sd(∂τ), a (d−1)-sphere. Proposition 1 forces D_Q(L)≥d−1. If d≤2 the Davis complex has dimension at most d+1≤3, hence vcd_Z≤3 and dim∂Σ≤2. If d≥3, the rational dimension lower bound is at least two. □

This excludes ordinary barycentric flagification of higher Moore complexes, high-dimensional torsion nerves, and all their iterated barycentric subdivisions. It neither excludes every flag triangulation of the same underlying space nor claims that subdivision preserves vcd. The earlier 6200004 work's induced-square obstruction required hyperbolicity; the present obstruction applies to the broader Coxeter question even when squares are allowed.

The finite control explicitly constructs the induced barycentric boundary of a tetrahedron and checks its degree-two homology. The theorem is proved for arbitrary d above; the test is not the proof.

## Approach 4: killing global rational classes by cone attachments

The all-RP²-link model suggests attaching cells to kill rational H² while retaining top integral torsion. Pure homology arithmetic is too weak for this operation.

**Proposition 4.** Let L be an induced subcomplex of a new finite Coxeter nerve L'. Then D_R(L')≥D_R(L), for R=Z or Q. In particular adding new vertices and coning subcomplexes cannot reduce an existing rational dimension obstruction, provided no new simplex supported entirely on old vertices is introduced.

**Proof.** The corresponding special subgroup embeds, so virtual cohomological dimension is monotone, as proved in Proposition 1. Equivalently (3) directly applies to the old induced complex and its induced subcomplexes. □

For a cone attachment L'=L∪(v*A), with v new, deletion of v recovers exactly L. If H²(L;Q)≠0, then the required vanishing already fails at this deleted-vertex term, even if the attachment kills H²(L';Q). Several cone attachments retain L as the subcomplex induced by its old vertices, so (3) gives the same conclusion.

In the explicit sphere-to-cone control, the global rational class vanishes and reappears upon deleting the cone apex. This is a finite illustration of the general induced-subgroup obstruction.

The obstruction does not cover modifying old-old simplices or a surgery that destroys the induced inclusion. Those changes would require rechecking every induced subcomplex and preserving the desired integral degree. No such repair was constructed here. It is therefore invalid to infer a solution from an abelian chain complex in which selected rational free summands have been killed.

## Approach 5: recursive Davis quotient/thickening constructions

Known high-dimensional Coxeter constructions are a natural way to seek a family of nerves. The particular CKV construction in §6 sends a k-large flag complex Δ to S(Δ,k), via a suitably displaced torsion-free finite quotient of the Davis complex followed by thickening. We import CKV Lemma 6.6 and Remark 6.7 only in their stated applicable setting:

    vcd_Q W(S(Δ,k)) = vcd_Q W(Δ)+1.                     (8)

The coefficient restriction is essential: their proof establishes characteristic-zero growth, and it is not a theorem fixing rational dimension while growing integral dimension. Starting with a baseline q_0=2 example, each actual iteration yields

    q_t=2+t,       dim_Q ∂Σ(W_t)=1+t.                    (9)

Thus every positive number of these iterations leaves the rational-dimension-one target. Increasing displacement does not change this conclusion. It is not necessary to recompute a large quotient to diagnose the failure, and no generalization to finite/simplex degenerate seeds is asserted.

This is a credited application of an existing general theorem, not a new construction. It also explains why recent high-dimensional fibering examples and arbitrarily large conformal dimension do not by themselves resolve the coefficient-specific question. The August 2026 Ma–Yoon–Zheng manuscript deals with Pontryagin-surface boundaries and higher-dimensional ambient hyperbolic embeddings; ambient dimension five is not boundary covering dimension five.

## Precise remaining obstruction

A solution still requires a finite spherical nerve satisfying (2), with rigorous verification of **all** induced/deleted-simplex rational cohomology, and the prescribed integral top degree. For a right-angled construction this means rational regularity exactly 2 and arbitrarily high exceptional-characteristic regularity in a flag complex. We did not construct such a complex or prove it impossible.

The exclusions leave genuinely more singular, non-manifold-link nerves and changes that do not retain old rational witnesses as induced subcomplexes. The unresolved compactum-to-group realization gap remains for general Markov compacta; the earlier 6200004 investigation already treated that approach, so it was not counted again as a new attempt here.

All five approaches are terminal author work for this packet. They establish scoped obstructions and a corrected search formulation. They do not establish nonexistence of the groups sought by Dranishnikov.

## Verification and credit limits

Run `python verify.py` or `python -O verify.py` from any working directory, supplying the path to this script. It verifies the frozen file inventory and hashes, then compares a fresh deterministic calculation with CHECK_RESULTS.json. All mathematical checker failures use explicit exceptions, not optimizable assertions. There are 32,400 finite checks, most boundary-square entries; this count is not mathematical coverage or a probability of correctness.

The general proofs are the arguments above plus the explicitly imported published theorems. The packet is neither formal proof-assistant verification nor external peer review. Fresh independent audit is required before any acceptance label. No remote mutation, publication, outreach, or external-file upload was performed by the author of this packet.

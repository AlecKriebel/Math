# An intrinsic geometric Jones construction through local system homology

Roberts Problem 1.7 · problem 10400007 · 14 October 2026

## Conclusion and scope

For every smooth oriented knot K in oriented S³, a direct geometric construction assigns its peripheral exterior a class in ordinary local-system H₀. A geometrically specified fundamental filling contracts that class. The normalized contractions give all the required roots-of-unity values of the source-normalized Jones polynomial, and finitely many of them reconstruct the entire Laurent polynomial exactly.

The local systems are the Andersen–Ueno (AU) anomaly-corrected conformal-block systems on marked surface Teichmüller spaces. The exterior class is defined first from geometric vacuum sewing, the gluing action and normalized compression projections. Only afterward does the CFT/WRT comparison identify this expression with the familiar RT exterior state and prove its independence of the chosen decomposition.

The [independent mathematical audit](pass2_audit/INDEPENDENT_AUDIT.md) accepts that theorem, and the [source-scope assessment](pass2_scope/SCOPE_ADJUDICATION.md) accepts it as an affirmative construction in the broad class supported by Roberts's informal request. This is an explicit synthesis of known CFT/WRT theory, not a newly discovered invariant or a claim of historical recognition. Ordinary H₀ on a contractible Teichmüller base is central to the statement. No positive-degree complement-configuration theorem or all-links theorem is claimed.

## The question and the adopted standard

Roberts's Problem 1.7 appears on printed page 385 of Ohtsuki's edited volume. In paraphrase, it asks for an intrinsic definition of the Jones polynomial through homology with local coefficients. The nearby discussion contrasts complement-based topology with braid/plat presentations and suggests complement configuration spaces as one possible route. It does not fix the homological degree, the coefficient rank or a compulsory configuration-space base. The preceding discussion motivates ambient three-dimensional naturality. [Primary source](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf)

The [construction contract](CONSTRUCTION_CONTRACT.md) makes the resulting obligations explicit: define the input, spaces, coefficients, homology and extraction; account naturally for equivalent knot pairs; and recover the entire polynomial without defining the local system or state from a previously computed Jones value. Auxiliary decompositions may compute an intrinsic object if independence and natural transport are proved. These are authored operational criteria, not additional quotations from the source.

The target normalization is

    V_U(t)=1,
    t^(-1)V_(L+)(t) − tV_(L−)(t)
       = (t^(1/2)−t^(-1/2))V_(L0)(t).

For knots, V_K lies in Z[t,t^(-1)]. The oriented-link coefficient ring and component/framing issues require separate care; the construction accepted here has knot-only output.

## The theorem

Let E_K=S³\int(N_K) be the compact knot exterior and T=∂E_K. Retain the oriented meridian m and preferred zero-linking longitude ℓ. The longitude fixes the preferred zero-framing. For every integer k≥1 there are:

- A geometrically defined finite-rank complex local system L_k on the marked Teichmüller space of the extended peripheral torus.
- An exterior class h_k^geom(K) in H₀(Teich(T);L_k), defined by the recipe below.
- A direct geometric filling functional f_k^geom on that homology space.
- A nonzero unknot denominator and an exact normalized value

      z_k(K)=f_k^geom(h_k^geom(K))/f_k^geom(h_k^geom(U))
            =V_K(exp(−2πi/(k+2))).

The class and filling transport naturally under orientation-preserving equivalences of the oriented knot-pair input. The recipe is independent of the relative Heegaard decomposition used to compute it. If a diagram of K has c crossings, then 4c+1 levels suffice for exact polynomial reconstruction. No Jones coefficients are supplied by that diagram.

Tame knots are understood through their standard smooth representatives. No statement about wild embeddings or arbitrary ambient three-manifolds is required.

## The local system and its homology

For an extended marked surface Σ, AU construct the sl₂ level-k vacua bundle with the abelian ghost correction, equipped with its flat connection. The correction is essential: a general curved prequantum line bundle cannot simply be called a local system. Write

    L_k(Σ)=ker ∇_k,
    W_k(Σ)=H⁰(Teich(Σ);L_k(Σ)),
    H_k(Σ)=H₀(Teich(Σ);L_k(Σ)).

The coefficient field is C, the homology is ordinary singular homology, and its degree is zero. There is no relative or Borel–Moore support condition in the main construction. Concretely, H₀ is the quotient of the direct sum of coefficient fibers by path-transport relations [y,P_γv]−[x,v]. No skein relation is inserted as a singular-chain boundary.

Since marked Teichmüller space is contractible, a horizontal section is determined by one fiber value. The canonical isomorphism

    θ_Σ:W_k(Σ)→H_k(Σ),  s↦[x,s(x)],

is independent of x and natural for the geometric flat-bundle maps. The local system has trivial fundamental-group monodromy on this base. Its mapping-class equivariance, sewing structure and distinguished exterior class carry the substantive information used here; H₀ does not manufacture additional higher homology.

AU's geometric sewing is available before any RT comparison. It comes from their convergent dual-basis sewing construction and yields factorization over labels, naturality, vacuum propagation and commuting sewings. The relevant statements are Definition 11.3, Theorem 11.4, Theorems 12.1–12.4, and the convergence and horizontal-equation results in §14.4. [AU geometric construction](https://arxiv.org/pdf/math/0306235v2)

## Defining the exterior class before comparison

Choose a relative Heegaard decomposition

    E_K=H_g∪_f C,

where H_g is a genus-g handlebody and C compresses its other genus-g boundary to the peripheral torus T. Such a decomposition exists for every knot exterior. The level-k labels are 0,1,…,k; 0 is the vacuum and 1 the fundamental label.

### Vacuum from the handlebody

Choose a complete meridian disk system D in H_g. Cut its boundary along the disk curves. The resulting sphere has 2g paired marked points. Geometric sewing maps the direct sum of its label sectors to W_k(∂H_g). Propagation identifies the all-zero sector with C. Sewing its unit defines the vector v_D.

The definition uses the sphere vacuum and geometric sewing. It does not take Z_RT(E_K), a Jones scalar or an independently computed knot invariant as input.

### Compression projection

Choose g−1 compression disks in C. Inverse geometric sewing cuts the positive boundary along those curves. Project to the all-zero label tuple and remove the vacuum points by propagation. This defines a linear map

    p_C:W_k(∂_+C)→W_k(T).

This is a specified surface-factorization operation. It is not claimed to be the pushforward associated with a single continuous map of Teichmüller spaces.

The boundary extensions matter. On the handlebody boundary use its homological-kernel Lagrangian. On T use Qm. On the compressionbody positive boundary use the inverse image of Qm under the homological correspondence through C. These rational Lagrangians have the primitive integral lattices needed for AU's convention.

### Calibration and the formula

On the standard peripheral torus, let e₀ be its meridian vacuum, ε₀ its vacuum coordinate, and S₀ the weight-zero extended meridian–longitude interchange calibrated so that the two vacuum solid tori give weight-zero S³. Define geometrically

    s_k=ε₀(W_k(S₀)e₀),  D_k=s_k^(-1).

The comparison proof will show s_k≠0. With f₀ the weight-zero extended gluing map, define

    h_k^geom(K;H,C,f,D,δ)
      =θ_T[D_k^(g−1)p_C W_k(f₀)v_D].

This is the complete rule for the knot-dependent class. The exterior contributes its actual gluing geometry; the coefficients and surface operations are independently prescribed. The compression factor D_k^(g−1) cannot be dropped.

## Defining the filling before comparison

Factor the peripheral torus along its meridian:

    F_m:W_k(T)→⊕_(λ=0)^k W_k(S²;λ,λ†).

The label-1 summand is one-dimensional. AU's normalized affine-module pairing fixes a nonzero two-point coordinate c₁. Set

    ε₁^m=c₁ pr₁ F_m,
    f_k^geom=ε₁^m θ_T^(-1).

This is a coordinate after geometric factorization, not an imported higher-genus orientation-duality pairing. Any fixed nonzero rescaling of c₁ multiplies the knot numerator and unknot denominator equally, so the ratio is unchanged. The meridian and preferred longitude fix the framing convention; a framing-changing twist is not silently treated as identical peripheral data.

The normalized ratio compares scalar contractions, so it does not require a choice identifying the two knots' torus spaces.

## Why the definition is intrinsic and correctly normalized

Only now invoke AU's structure-preserving isomorphism I from the SU(2) skein/WRT modular functor to W_k. Fix the vacuum-unit normalization. Its compatibility with sewing, propagation and extended-surface maps identifies the already defined geometric ingredients with their RT counterparts. [AU comparison, Theorem 1.1](https://arxiv.org/pdf/1110.5027v2)

The reverse-handle normalization needs more than testing one scalar. Vacuum inclusion i₀ and projection p₀ on the same cut satisfy p₀i₀=1. A cancelling 1–2 handle configuration uses dual curves and has raw coefficient p₀S₀i₀=s_k. The colored splitting form gives, on the vacuum sector,

    ⟨i₀x,y⟩_sewn=D_k⟨x,p₀y⟩_cut,

with nonvacuum sectors orthogonal. The reverse-handle map is therefore D_kp₀ on every lower-surface state. Locality supplies one such factor for each compression. This proves the all-genus normalization, rather than guessing it from the genus-one test. [BHMV, colored splitting and Corollary 4.10](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/bhmv.pdf)

The extended-manifold gluing convention subtracts the Maslov index of the three boundary Lagrangians. With the specified handlebody and compressionbody choices, the relevant entries repeat at each intermediate composition. The corrections vanish. Final exterior/filling composition has μ(Qℓ,Qm,Qm)=0 as well. Thus the expression computes a weight-zero exterior and a weight-zero closed contraction, with no suppressed projective phase. [Gilmer–Masbaum, §2](https://arxiv.org/pdf/0912.4706v3)

These checks prove, generator by generator,

    h_k^geom(K)=θ_T I_T Z_k^RT(E_K,weight 0)(1).

This equality is a theorem about an independently specified expression, not its definition. It implies independence of disk systems, handle slides, relative Heegaard isotopies, stabilizations and decompositions. An orientation-preserving knot-pair equivalence first transports the geometric expression term by term; decomposition independence then removes the auxiliary choices. The result is a naturally assigned exterior class.

The filling corresponds to the fundamental-core functional up to the one-dimensional gauge already canceled in the ratio. In the standard unitary SU(2) normalization,

    s_k=√(2/(k+2))sin(π/(k+2)),
    S₁₀=√(2/(k+2))sin(2π/(k+2)).

Both are nonzero for k≥1. The second is the unknot denominator up to the fixed nonzero gauge. These formulas verify the geometrically defined calibration; they do not replace its definition.

## Jones convention and the full polynomial

Write q=exp(2πi/(k+2)) with the AU fractional-power convention. Their framed invariant F has fundamental dimension [2], twist q^(3/4), and the corresponding framed skein relation. Removing writhe and dividing by [2] gives P_L. For an oriented link, the source-normalized variable is t=q^(-1) and the component sign is

    V_L(t)=(-1)^(number_of_components(L)−1)P_L.

For knots that sign is +1 and the zero-framing correction agrees with the total-writhe correction. Hence the geometric contraction is exactly V_K(t_k), where t_k=exp(−2πi/(k+2)). The positive two-braid trefoil calibrates to t+t³−t⁴; its mirror has the reciprocal polynomial. The detailed sign calculation remains in [the accepted PASS1 construction, Sections 5–6](pass1_skein/CANDIDATE_CONSTRUCTION.md).

For a c-crossing knot diagram, a smoothing has at most c+1 circles. The bracket's A-exponents have absolute value at most 3c; the writhe correction enlarges that to at most 6c. Since the knot Jones polynomial is in powers of A⁴, the deliberately coarse integral bound B=2c gives

    supp(V_K)⊂[−B,B].

Take k=1,…,2B+1. The t_k are distinct and nonzero. Exact Lagrange interpolation gives

    P_K(t)=t^(-B) Σ_k t_k^B z_k(K)
                     ∏_(j≠k)(t−t_j)/(t_k−t_j).

The polynomial t^B V_K has degree at most 2B and exactly these values, so P_K=V_K. This proves equality in Z[t,t^(-1)] despite the formula's complex cyclotomic presentation. It is not floating-point reconstruction. A different diagram or larger bound gives the same polynomial. When c=0, one value suffices.

## What changed after the first construction

PASS1 already established a valid formal theorem: transport the intrinsic RT exterior/filling operations through the CFT comparison and the canonical H⁰-to-H₀ identification. No missing TQFT map or normalization failure was found. Its scope assessment withheld the further explanatory interpretation because the knot-dependent state was introduced by the formula θIZ_RT(E_K).

PASS2 supplies the missing independent geometric rule: vacuum sewing, gluing action, normalized compression and label-1 extraction. Comparison is now used after the definition to prove independence and equality. The PASS1 theorem remains valid; its historical scope reservation applies to that earlier definition. It is not a retraction and is not the current verdict on the strengthened construction.

The proof still relies on established quantum-topological comparison and cobordism relations. H₀ still identifies horizontal sections on a contractible surface base. Those dependencies are visible, and the source-scope acceptance is explicitly limited to the documented broad construction class. No claim is made that this is the only possible reading of Roberts's informal request.

## Complementary results and their limits

The [results index](RESULTS_INDEX.md) collects the separately audited configuration, descent and Floer analyses. They explain why several tempting shortcuts do not produce an alternative intrinsic complement model, and identify genuine partial constructions. A no-go theorem for a full chain-complex stabilization, a specified meridional character, a classical module-with-pairing, or a coefficient-only Floer repair does not disprove Roberts's unrestricted request.

These supplementary analyses are not premises needed to define the main geometric exterior state. Their bounded failures do not weaken the accepted CFT/WRT synthesis, and their finite checks do not substitute for the quantified mathematical proofs.

## Reading the evidence

The full [direct-state theorem](pass2_skein/DIRECT_GEOMETRIC_STATE_THEOREM.md), [independent audit](pass2_audit/INDEPENDENT_AUDIT.md), and [scope acceptance](pass2_scope/SCOPE_ADJUDICATION.md) contain the detailed mathematical and source-level judgments. [Sources](SOURCES.md) supplies the primary references and public inspection metadata. [Reproducibility](REPRODUCIBILITY.md) states exactly which finite checks replay offline and which external-source validations remain receipts rather than self-contained reruns.

No external peer-review status, author endorsement, exhaustive literature closure, or historical novelty is certified by this reader.

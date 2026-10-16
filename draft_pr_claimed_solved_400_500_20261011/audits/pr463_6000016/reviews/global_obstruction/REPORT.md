# Independent verification of the global Hessian obstruction

PR #463; problem 6000016 / AMR-059-0016, Stability of Hessian Metrics. Frozen eligible head: `982fcf87d60c9f8d4ec853d5dd5f4ad6021a6649`.

Reviewer family: `/root/pr463_global_obstruction`. Verdict: **PASS for the mathematical obstruction and its stated unrestricted stability application**. Blocking issues: **0**. Unresolved mathematical gaps in this family: **0**. Required repairs to the frozen proof: **0**. This is a mathematical verification, not a priority, publication, or merge approval.

## Independence and reviewed inputs

I read the frozen candidate PROOF.md, SOURCE_GATE.md and README.md. I then recorded INITIAL_INDEPENDENT_DERIVATION.md before reading any historical audit verdict or any new peer verdict. I have not read any such verdict. I did not use the candidate's symbolic checker or its recorded results to implement the new algebra checks.

The reviewed candidate is a hypothesis throughout this report. All source and checker hashes are bound in INPUT_RECEIPT.json. Only files within this review's folder were authored. Frozen files, other review folders, QUEUE.md, the checkout, branch and Git index were not modified. No external service was mutated and no individual was contacted. This work verifies an already complete candidate; it is not a new original proof-search attempt.

## Exact statement and assumptions

For each real parameter t, equip the fixed smooth torus M=R²/Z² with the connection

    Dᵗ=D⁰+t dx⊗dx⊗Y,  X=∂x, Y=∂y.

The claim is that these connections are smooth, torsion-free, flat and complete, that (M,D⁰) admits a positive-definite Hessian metric, and that for every real t≠0 there is no smooth positive-definite metric g which is locally a Hessian in Dᵗ-affine coordinates. The universal quantifier is over all such metrics, including noninvariant metrics of any size and with arbitrary off-diagonal coefficients. No smooth dependence of a hypothetical g on t is assumed.

The metric is Riemannian: positive definite. A local potential is sufficient for the definition; a single global function on the compact quotient is not assumed. The torus is compact, oriented and has no boundary. Its vector fields X,Y and one-forms dx,dy are global even though the coordinate functions x,y do not descend.

**Success criterion:** a complete analytic contradiction for every nonzero real t and every possible positive metric, together with a genuine arbitrarily small deformation of the affine structure. Finite computations alone cannot establish this criterion.

## Verification of the connection and the deformation

The added term is a globally defined tensor, symmetric in its two input slots. Thus it gives a connection with sole nonzero coefficient Γʸₓₓ=t, and torsion vanishes. The coefficients are constant, and every product contributing to curvature contains a coefficient with a lower y-index; those coefficients vanish. The full curvature tensor is zero.

Define Fₜ(x,y)=(x,y+t x²/2) on the cover. Its Jacobian is

    J=[[1,0],[tx,1]],  det J=1,

and Fₜ⁻¹(u,v)=(u,v−t u²/2). Pullback of the standard affine connection is given by J⁻¹ times the second derivatives of Fₜ; this has exactly Γʸₓₓ=t. In particular, the sign agrees with the candidate's connection, rather than its negative.

The deck action in developing coordinates is

    ρₜ(m,n)(u,v)=(u+m,v+n+tm u+t m²/2).

Direct expansion verifies Fₜ(x+m,y+n)=ρₜ(m,n)Fₜ(x,y) and ρₜ(m,n)ρₜ(p,q)=ρₜ(m+p,n+q). Its linear part is [[1,0],[tm,1]], of determinant one. Conjugacy by the globally invertible Fₜ transfers freeness, proper discontinuity and compactness of the ordinary integer-translation quotient. It is not necessary to infer these global properties from a local Jacobian computation alone.

The developing image is all R², so the affine structure is complete. Independently, every lifted geodesic is

    x(s)=x₀+as,
    y(s)=y₀+bs−t a²s²/2,

and exists for every real s. Its developed curve is affine-linear. Completeness here concerns Dᵗ-geodesics, not the completeness of an absent noncentral Hessian metric. The form dx∧dy is Dᵗ-parallel, independently confirmed by all its covariant derivative components; the example is volume preserving.

On the fixed compact torus, Dᵗ−D⁰=t dx⊗dx⊗Y tends to zero in every smooth tensor seminorm. Fixed small quotient neighborhoods with chosen lifts admit affine charts Fₜ restricted to the lifts; their transition maps are restrictions of ρₜ(m,n), smooth in t. Developing maps and every derivative converge uniformly on compact cover sets. This supplies an ordinary smooth deformation of marked affine structures rather than merely a sequence of unrelated affine quotients.

The credited Baues–Goldman moduli period coordinate is a real cube-root function of t. That coordinate subtlety does not defeat a smooth chart deformation. If smoothness in those normalized period coordinates is additionally desired, use t=σ³: the family of connections and charts is polynomial in σ, every noncentral σ still gives t≠0, and the displayed normalized period becomes (0,−σ). A zero parameter derivative at σ=0 imposes no obstruction to a deformation.

At t=0, dx²+dy² is positive definite and is the Hessian of (x²+y²)/2 on each lifted affine coordinate neighborhood. The quadratic potential is not periodic and is not claimed to be a function on M.

## First analytic proof: a global exact positive form

Let g be any candidate positive-definite Hessian metric. On the cover write

    g=A dx²+2B dxdy+C dy².

A,B,C are smooth and periodic in both variables, because the original-cover deck transformations are translations and the original forms dx,dy are translation invariant. They are not asserted to be periodic when expressed in developing coordinates (u,v).

In flat affine coordinates, local Hessian form implies total symmetry of Dg through equality of the third derivatives of the local potential. Hence the Codazzi identity (D_Ug)(V,W)=(D_Vg)(U,W) is necessary, and tensoriality permits use of X,Y. No converse implication is needed for the obstruction.

For a covariant two-tensor, the derivative subtracts a connection term in each tensor slot. The complete derivative components are

    Dₓgₓₓ=Aₓ−2tB,   Dₓgₓᵧ=Dₓgᵧₓ=Bₓ−tC,   Dₓgᵧᵧ=Cₓ,
    Dᵧgₓₓ=Aᵧ,       Dᵧgₓᵧ=Dᵧgᵧₓ=Bᵧ,        Dᵧgᵧᵧ=Cᵧ.

Thus the two potentially nontrivial independent Codazzi equations are

    Bₓ−Aᵧ=tC,     Cₓ=Bᵧ.                         (1)

In particular, α=g(X,·)=A dx+B dy is a global one-form and

    dα=(Bₓ−Aᵧ)dx∧dy=t C dx∧dy.                 (2)

Since Y never vanishes and g is positive definite, C=g(Y,Y)>0 at every point. Smoothness and compactness imply a strictly positive integral of C against the fixed orientation form. Stokes' theorem on the compact boundaryless torus then gives

    0=∫M dα=t∫M C dx∧dy,

forcing t=0. The sign of t is irrelevant, and there is no smallness restriction beyond nonzero. The measure is the ordinary quotient area form, not the metric-dependent volume measure. The connection's parallel-volume property is true, but is not required for Stokes' theorem here.

Equivalently, integration of (1) over [0,1]² cancels the boundary derivatives by periodicity. This includes arbitrary nonconstant A,B,C; it does not first replace g by an invariant metric.

As a further invariant check, β=g(Y,·)=B dx+C dy is closed by the second equation of (1), while dα=t dx∧β. Its period on any vertical circle is ∫₀¹ C(x,y)dy>0, independent of x by closedness. Consequently the cohomology pairing of [dx] with [β] is nonzero. Exactness of t dx∧β would contradict that pairing whenever t≠0. This is a cohomological reformulation of the same obstruction, not a separate priority claim.

## A second analytic mechanism: cover potentials and commuting cocycles

This proof supplies an independent verification in affine developing coordinates. It does not rely on assuming a metric is parallel or on integrating its coordinate components over the quotient.

Because Fₜ is a global diffeomorphism, the lifted affine manifold is the standard affine plane. Let h be the corresponding positive Hessian metric on R². It is invariant under the deck maps ρₜ(m,n). The local Hessian condition gives ∂ᵢhⱼₖ=∂ⱼhᵢₖ. For each k, the one-form ∑ᵢ hᵢₖ dzᵢ is closed, hence exact on simply connected R². Write its primitive fₖ. Symmetry of h implies ∂ᵢfⱼ=∂ⱼfᵢ, so ∑ᵢ fᵢ dzᵢ is itself closed and exact. It follows that h=Hess φ for a globally defined smooth function φ on the cover. Positivity makes this potential strictly convex locally, and along every nonconstant affine line. Only existence of the cover potential is used; no quotient potential is introduced.

Use the commuting deck generators

    V(u,v)=(u,v+1),
    T(u,v)=(u+1,v+t u+t/2).

Deck invariance and the affine nature of T,V imply Hess(φ∘V−φ)=Hess(φ∘T−φ)=0. On connected R² these differences are affine functions:

    L=φ∘V−φ=a u+b v+c,
    P=φ∘T−φ=d u+e v+f.

Their coefficients are real constants. Differentiate the first identity in v:

    b=φᵥ(u,v+1)−φᵥ(u,v)=∫ᵥᵛ⁺¹ φᵥᵥ(u,w)dw>0,

since h(∂v,∂v)=φᵥᵥ>0. Because TV=VT, their two potential increments obey

    L∘T−L=P∘V−P.

The left side is a+bt u+bt/2, and the right side is the constant e. Equality at every u forces bt=0. Positivity gives b>0, so again t=0.

This commuting affine-cocycle obstruction is materially different from the direct Stokes calculation. Both reflect the same geometric shear incompatibility and should not be advertised as logically unrelated results. The Poincaré integrations are justified by the simply connected affine cover and are absent from the shorter first proof.

## Translation averaging and Fourier zero mode

Translations of the original-coordinate torus preserve Dᵗ, since its coefficients are constant. If a positive Hessian metric existed, average its pullbacks over the compact translation group. Linearity of Codazzi and differentiation under the compact integral preserve the Codazzi condition. The averaged tensor is positive definite: for each nonzero tangent vector its quadratic value is the integral of strictly positive continuous values. The average has constant coefficients Ā,B̄,C̄, with C̄>0, and its first Codazzi equation reduces to 0=t C̄.

This makes the averaging legitimate rather than a hidden invariance assumption. It is equivalent to projecting the first equation in (1) onto its zero Fourier mode. At frequencies (k,l), its symbol is 2πi(k B̂−l Â)−t Ĉ; at (0,0), only −t Ĉ remains. The second equation has symbol 2πi(k Ĉ−l B̂). These are extra checkable viewpoints; neither finite Fourier samples nor convergence assumptions replace the analytic proof.

## Adversarial and boundary checks

1. **Central and arbitrarily small parameters.** At t=0 the Euclidean metric works, while the proof excludes every nonzero t, positive or negative, however small. The existence property can therefore fail to be open; no limiting-positive-metric argument is presumed.

2. **Indefinite Hessian tensors.** The global tensor g=2dxdy has determinant −1 and signature (1,1). It is Codazzi for every t and, in developing coordinates, is the Hessian of

       φ(u,v)=uv−t u³/3.

   Indeed Hess φ=[[-2tu,1],[1,0]], whose pullback by Fₜ is [[0,1],[1,0]]. For a general deck map, the potential increment is

       φ∘ρₜ(m,n)−φ=mv+(n+t m²/2)u+mn+t m³/6,

   an affine function. Thus the metric descends although its potential does not. It has C=0 and therefore does not contradict the positive-integral proof. This confirms the necessity of positive definiteness and the cubic sign and coefficient.

3. **Local positivity on the cover.** Pulling back the affine Euclidean metric gives

       (1+t²x²)dx²+2tx dxdy+dy².

   Its determinant is 1, its first leading principal minor is positive, and it is Hessian on the cover. It satisfies Bₓ−Aᵧ=tC. Under x↦x+1 its cross coefficient changes by t and its xx coefficient changes by t²(2x+1), so it does not descend for t≠0. Integrating it as if periodic would be erroneous. The obstruction is global, not failure of local Hessian existence.

4. **Degenerate semidefinite limit.** If a global Codazzi tensor were positive semidefinite, Stokes for t≠0 would force C≡0. Pointwise semidefiniteness then forces B≡0, and (1) forces Aᵧ=0. Tensors A(x)dx² with A≥0 can survive, but are degenerate. This cannot supply a Riemannian metric.

5. **Parallel-metric shortcut.** A nontrivial unipotent shear cannot preserve a positive inner product, but this observation only rules out Dᵗ-parallel positive metrics. Hessian metrics need not be parallel. This shortcut is not used. The valid proofs explicitly handle the derivative terms of an arbitrary g.

6. **Fixed linear holonomy.** The x-generator has linear holonomy [[1,0],[t,1]], the identity exactly at t=0. Identity cannot be conjugate to a nontrivial shear. Thus this example changes linear holonomy and does not settle a restriction to fixed linear holonomy.

7. **Hyperbolic case.** A developing image equal to R² contains complete affine lines and remains all R² under any affine change of developing coordinates. It is outside the source's hyperbolic class, so there is no contradiction with the stated hyperbolic stability result.

8. **Smoothness and global forms.** The argument does not identify x,y as global functions or demand a global potential on M. It uses their descending differentials and vector fields. Smooth g yields all derivatives and Stokes regularity needed. No parameter-dependent lower bound for hypothetical metrics, uniform metric family, limiting metric or diagonal normal form enters either proof.

## Primary source scope and attribution

I downloaded and visually inspected the original [Furuhata–Matsuzoe–Urakawa article](https://www.jstage.jst.go.jp/article/iis/4/2/4_2_125/_article/-char/en), printed p.126, item 5(b). The question concerns small deformations of the affine structure of a compact Hessian manifold and separately records Koszul's affirmative hyperbolic case. The item does not impose fixed holonomy or exclude complete affine tori. The counterexample therefore answers the unrestricted positive-definite question as printed. This does not assert that the question was still historically unresolved when this PR was created.

I also visually inspected [Baues–Goldman, arXiv:math/0401257v2](https://arxiv.org/pdf/math/0401257v2), printed p.20. The displayed developing map is precisely Fₜ, under parameter a=t, and the authors treat its differentiable affine family and cube-root period coordinate. The deformation is classical and must be credited. The candidate already does so prominently. I have not conducted the full priority audit and make no assertion of novel discovery, first resolution, or absence of an older theorem implying this obstruction.

Both primary PDFs and all source-page images are retained only under private_sources; their bytes are excluded from the positive public whitelist. The independent equations and exposition in this report are authored verification material, not reproduced source text.

## Reproducible exact controls and their limits

The newly authored check_global_obstruction.py independently constructs every covariant derivative component, every Codazzi component, all torsion and curvature components, parallel area form, developing inverse and pullback connection, deck equivariance and group law, holonomy, complete geodesics, the indefinite affine potential and its descent increment, the positive cover metric and its failure to descend, averaged/zero-mode equations, central and semidefinite controls, the commuting potential cocycle, and cubic parameter substitution.

There are **140 exact checks per valid run**. Normal and optimized runs pass and have identical JSON output bytes. Guards use explicit exceptions, so Python's optimization flag cannot remove them. The recorded runtime uses Python 3.14.6, SymPy 1.14.0 and mpmath 1.3.0; the programs are portable Python and need only the pinned symbolic dependencies.

run_review_controls.py executes two valid runs and eight intentionally corrupted in-memory claim cases in each mode: reversed connection sign, reversed covariant tensor sign, dropped second covariant slot, wrong holonomy half coefficient, wrong geodesic sign, wrong cubic potential coefficient, false descent of the positive cover metric, and false positivity of the indefinite metric. All **16** actual corrupted subprocesses exit **4**, emit no success JSON, and identify an InvalidClaim. No mutation fixtures are written or published. The runner itself is also checked under optimization.

These computations check exact identities with symbolic t, rather than approximating a small-parameter limit. The displayed rational positive and negative parameter cases are edge controls only. Universal exclusion comes from the analytic proofs, not from a finite number of samples, a computer algebra certificate of positivity, or a formal proof assistant. Full counts, result hashes, source hashes and mode identities are recorded alongside this report.

## Strongest verified result and exact remaining boundary

**Verified:** the classical complete, volume-preserving shear family on the fixed torus is an arbitrarily small smooth deformation of a positive-definite Hessian structure, while every noncentral member has no positive-definite Hessian metric at all. Two analytic mechanisms verify the universal exclusion, and exact controls confirm all supporting formulae and adversarial boundaries. The frozen mathematical proof needs no repair for this claim.

**Remaining gap in this family:** none. **Outside this family's approval:** historical priority, whether repository status should remain claimed_solved after a full priority audit, preprint preparation, complete-package adversarial review, publication operations and merge. A mathematical PASS must not be interpreted as a novelty certificate or publication authorization.

Final verification checkpoint: 2026-10-12 UTC, completion **100% of this mathematical review family**, with all remaining mathematical issues **0**. Exact sealing timestamp is in RESULT.json and RESEARCH_LOG.md.

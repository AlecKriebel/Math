# Independent analytic review of 23131374

**The mathematical theorem is supported at its literal scope; the original contribution/coverage framing requires bibliographic correction, so public promotion of this claim package should be deferred.** A newly inspected earlier primary body contains the result and critical correction mechanism. This does not falsify the independent proof. No source change, extended repair or narrowed promotional substitute was made.

The actual reviewed six-page PDF has SHA256 `f900d86763266c73a5886df7edd194d275a25c31d55755c00716860d2e46e4a9`; its sole TeX has SHA256 `818f5ebb96328c2cdf418b05ff34bc5bbec5943ef508c798c715dc1fca4a7114`. Both were read in full, and every reader page was visually inspected. All 24 source-baseline files are preserved unchanged. No deposited or foreign program was executed. This assignment made no source, configuration, website, shared-core, Sheet, Git, browser or external communication change.

## Early independence and exact target

The complete reader and TeX were read first, then the universal mechanism was reconstructed in `INDEPENDENT_MECHANISM_NOTES.md`. These notes, the provisional verdict and thirteen source/read bindings were sealed at **2026-10-25 06:46:12 UTC**, before external primary bodies, package history, current or sibling reports, or source-lane scientific conclusions. The early seal has SHA256 `afa40f12f4b1c13891b404097bdf062a4cfcd8ddc4e8295c13d7ab54db19124c`. It remains immutable. No sibling or source review report was subsequently read either; only supplied raw primary objects were consulted after the seal.

The claim is that for each fixed finite integer r≥0 there is a sequence of smooth complete strictly positive-curvature metrics converging in ordinary compact-open C^r to a smooth complete positive-curvature background, but whose actual point-normalized conformal coordinate factors fail to converge in C^(r+1). The two surfaces are C and S². Maps preserve orientation, fix 0,1 on C and fix 0,1,∞ on S². The finite regularities describe topologies on smooth objects. Each r can use its own sequence.

This proves failure of inverse continuity for the specified parametrization at the displayed backgrounds. It does not assert failure at every metric, say anything about abstract homeomorphisms of the spaces, handle RP², or contradict the noninteger Hölder and smooth-topology results. Positive plane curvature is pointwise; no positive global lower curvature bound is claimed.

## Universal analytic reconstruction

### Background geometry, global maps and exact identification

For the plane, b=(1/2)log(1+|z|²), so g_*=e^(−2b)|dz|² is complete and has curvature 2/(1+|z|²)>0. Escaping-curve lengths dominate variation of arsinh|z|. For the sphere, b=log(1+|z|²)−log2 gives exactly the unit round metric. In both backgrounds Δb>0 with a positive minimum on every fixed compact disk.

Every changed metric equals g_* outside the fixed disk |z|<R=1/4. A fixed smooth positive changed metric is comparable to g_* on that compact disk and identical outside, proving completeness. On S² it extends as the original metric near infinity. Completeness of the conformal target follows from an exact onto isometry; a new asymptotic growth classification is not required.

Uniqueness of the coordinate factor is elementary. If f and ψ are two normalized orientation-preserving factors for the same metric, ψ∘f⁻¹ is a conformal automorphism of the standard plane or sphere. An affine map fixing 0,1, or a Möbius map fixing 0,1,∞, is the identity. The conformal factors then agree. Consequently the explicitly constructed f is the actual inverse factor, without invoking continuity of general Beltrami solutions. No derivative normalization is imposed at 0.

### The zero endpoint

Let θ_n(t)=θ₀η(log(R/t)/n), with a smooth step η from zero to one and θ₀∉2πZ, and set φ_n(z)=exp(iθ_n(|z|))z. It is a constant rotation near 0, identity for |z|≥R and a smooth orientation-preserving global diffeomorphism whose inverse subtracts the same radial angle. It fixes the normalization points.

Write q_n=tθ′_n(t). Then ||q_n||∞≤C/n. In orthonormal polar frames, after target rotation, Dφ_n is [[1,0],[q_n,1]]. Its Gram matrix is [[1+q_n²,q_n],[q_n,1]]. Because the background is radial, this gives the background-relative pullback metric. Its operator-norm difference from I tends uniformly to zero, and the tensor is unchanged at 0 itself. Thus φ_n*g_*→g_* in C⁰. Positive curvature and completeness hold by isometry, while Dφ_n(0)=Rot(θ₀) never tends to I. These are the actual normalized factors, so C¹ convergence fails.

### Logarithmic cancellation for every fixed r≥1

Put ρ=e^(−n), ε=1/n, S=|z|²+ρ², s=√S, L=log s, m=r+1 and

    f=z+εχ z^m L,

with a fixed smooth radial χ equal to one on |z|≤R/2 and zero outside |z|<R. Each f is smooth at 0; no singular limiting map is being admitted into the object space.

For an ordered j-th real derivative, D^jL=P_j/S^j with P_j homogeneous of degree j in x,y,ρ. Differentiation gives P_(j+1)=S∂iP_j−2j x_iP_j. Its coefficient ℓ¹ norm grows by at most 5j. Hence |D^jL|≤5^(j−1)(j−1)!s^(−j), an induction covering all finite orders. Leibniz then gives

    |D^k(z^mL)|≤C_(r,k)s^(m−k)(1+|log s|),   0≤k≤m.

For Df−I the positive power r absorbs the logarithm uniformly, giving O(ε). At the highest derivative of f_z, the exponent can be zero, but ε|log s|≤εn=1. Thus f_z is uniformly bounded in C^r, though it need not converge to one in C^r.

The anti-holomorphic derivative cancels the logarithmic term because z^m is holomorphic:

    f_bar=ε z^(r+2)/(2S)

on the inner disk. Its k-th real derivative has a homogeneous numerator of degree r+2+k over S^(k+1), hence magnitude C_(r,k)s^(r−k). For k≤r this is uniformly bounded. Cutoff derivative terms live on a fixed annulus with s≥R/2, so every needed fixed-order derivative is O(ε) there. Therefore ||f_bar||C^r=O(ε). Since |f_z|≥1/2 eventually and ||f_z||C^r is bounded, reciprocal differentiation gives a uniform C^r bound for 1/f_z. The Beltrami coefficient μ=f_bar/f_z tends to zero in C^r.

For each n, near 0, L=logρ+O(|z|²). The degree-m displacement term is εlogρ z^m=−z^m, giving the exact fixed obstruction

    ∂x^(r+1)(f−id)(0)=−(r+1)!.

This is a fixed-point witness against compact-open C^(r+1) convergence. It is not a finite-grid surrogate.

For large n, ||D(f−id)||∞<1. The lower Lipschitz estimate proves injectivity, and the contraction z↦y−(f(z)−z) proves surjectivity for every y. The Jacobian stays nonsingular with positive sign, so f has a smooth orientation-preserving inverse. Identity outside the disk implies, by injectivity, that the disk maps onto itself. Thus f fixes 0,1 and extends by identity near spherical infinity.

### Exact metric reconstruction and r≥2

Let h=log|f_z| and a be a smooth real supported correction. Define

    g_n=e^(−2(b+a))|dz+μdbar z|²,
    U=(b+a+h)∘f⁻¹.

The exact identity df=f_z(dz+μdbar z) gives g_n=f*(e^(−2U)|dw|²). The distortion eigenvalues (1±|μ|)² are positive eventually. On C the required factor is U; on S² it is U−b(w), which vanishes near infinity and extends smoothly. Once curvature positivity is established, the factor is in the stipulated admissible space, and the uniqueness argument identifies the actual normalized inverse.

For r≥2 take a=0. Smallness of μ in C^r gives g_n→g_* in C^r, hence in C². Gaussian curvature is continuous in the positive metric 2-jet. The background has a positive curvature minimum on the fixed perturbation disk; thus the changed metrics have positive curvature there for all sufficiently large n. Outside it the curvature is unchanged. This argument cannot be used at r=1.

### The full nonlinear critical case r=1

Set ℓ=1+|log s|. The second derivatives obey |D²f|≤Cεℓ. In D³(z²L), the undifferentiated logarithm is killed by D³(z²)=0; every remaining term scales as s^(−1). Hence |D³f|≤Cε/s. For h=log|f_z|, with |f_z|≥1/2,

    |Dh|≤Cεℓ,    |D²h|≤C(ε/s+ε²ℓ²)≤C′ε/s.

The elementary bounds sℓ≤1 and sℓ²≤4/e for 0<s≤1 justify the last inequality uniformly. No complex logarithm branch is needed for this real h.

To retain the exact nonlinear geometry, let J_ai=∂i f_a and H=J⁻¹. Differentiating f(f⁻¹(w))=w twice and tracing yields

    L_n v := (Δ_w(v∘f⁻¹))∘f = A_ij v_ij+B_i v_i,
    A=HHᵀ,    B_i=−H_ia f_a,jk A_jk.

The coefficient order HHᵀ is dictated by ∂w_a(f⁻¹)_i=H_ia. The full inverse-coordinate drift B is present. We have A−I=O(ε), A≥I/2 eventually and |B|≤Cεℓ. The drift need not converge uniformly to zero near the shrinking core; the estimates do not require it to.

Bounded derivatives of b and the h estimates imply

    L_n(b+h)≥Δb−C₀ε/s

with C₀ independent of n. Specifically, the background error is at most Cε(1+ℓ), the h-Hessian error at most Cε/s and the h-drift error at most Cε²ℓ². The displayed elementary suprema bound each by a fixed multiple of ε/s.

The regularized radius has

    D²s=I/s−xxᵀ/s³ ≥0,
    Δs=(|x|²+2ρ²)/s³ ≥1/s,    |Ds|≤1.

Its radial and tangential eigenvalues are ρ²/s³ and 1/s. Since A≥I/2,

    L_ns≥(1/2)Δs−Cεℓ≥1/(2s)−Cεℓ≥1/(4s)

uniformly for large n, using εsℓ→0 uniformly. Choose K>4C₀ once and set a=Kεχs. This is smooth for each n, ||a||C¹=O_K(ε), and no C²-smallness is asserted. In the inner disk,

    L_n(b+h+a)≥Δb+(K/4−C₀)ε/s>0.

On the fixed cutoff annulus all needed perturbation derivatives are O_K(ε), including f through order three and h,a through order two. With K already fixed, the full operator tends uniformly to Δb, whose annular minimum is positive. Outside the support it is exactly Δb. Smooth support transitions are covered by these estimates.

For target e^(−2U)|dw|² the curvature sign is K=e^(2U)Δ_wU. Thus, by exact isometry,

    K(g_n)=e^(2U∘f)L_n(b+h+a)>0.

Meanwhile μ→0 and a→0 in C¹ give g_n→g_* in C¹, and ∂x²(f−id)(0)=−2 blocks C² convergence of its actual factor. This proves the critical regime without assuming C¹ continuity of curvature, dropping the drift, or choosing K by numerical samples.

## Boundary and falsification checks

All constants may depend on the fixed r, cutoff and background, and the initial segment of each sequence can be discarded. No common threshold over all r is required. The origin, shrinking core, inner disk, closed cutoff annulus, support boundary and spherical infinity are covered explicitly. The plane background is unchanged at infinity, so no positivity lower bound there or new completeness theorem is hidden.

`independent_exact_checks.py` is newly written exact-rational code, with no external dependency and no deposited-code execution. Its recorded run passes 54 distinct log-derivative multiindices through order nine, 164 anti-holomorphic numerator/homogeneity controls for r=1,…,8, 36 exact inverse-Laplacian polynomial identities for six explicit nonlinear diffeomorphisms, six metric-reconstruction controls and eighteen regularized-radius Hessian/elliptic-trace cases including the origin and tiny scale. It rejects both HᵀH in place of HHᵀ and the omitted-drift operator. Mixed derivatives commute exactly. These tests corroborate particular identities and controls; the all-r proof is the written induction and estimates above.

## Direct primary interfaces

The exact published [Banakh–Belegradek body](https://www.jstage.jst.go.jp/article/jmath/70/2/70_733/_pdf), physical pp.1–4 and 15–18, was read, with critical topology/normalization pages inspected visually. It uses smooth objects with compact-open C^γ topologies; its diffeomorphism topology is one derivative higher. The normalizations are pointwise, and (8.3), (9.2), Theorem 8.4 distinguish continuous bijections from the proved noninteger Hölder homeomorphisms. The complete [2016 erratum](https://link.springer.com/content/pdf/10.1007/s00208-015-1354-1.pdf) was read and visually inspected; it explicitly corrects the integer-topology assertion to the Hölder statement. These match the reviewed formulation.

The actual [Oberwolfach report](https://ems.press/doi/pdf/10.4171/OWR/2017/3), printed pp.148–150, was read, with p.149 inspected visually. It writes pushforward whereas the reviewed paper uses pullback. These are related by inversion of the normalized diffeomorphism. The published diffeomorphism spaces are topological groups in the relevant integer regularities j≥1, so inversion preserves the homeomorphism question. This reconciles the notation without silently identifying the two formulas. The [publisher page](https://ems.press/journals/owr/articles/15208) independently gives publication on 3 January 2018 for the 2017 workshop/report.

The cited [MSS arXiv v1](https://arxiv.org/pdf/2208.02551v1), physical pp.33–36, including actual Example 5 on p.34, was read. It supplies the classical logarithmic quasiconformal example with continuous coefficient and a non-C¹ map, with book attributions. The complete cited books were not read here. Those attributions stay indirect; this review does not turn that example alone into the full smooth positive-curvature realization.

The primary/read ledger records exact bodies, versions, hashes, reading extents and provenance. These bounded readings do not reconstruct every dependency of the published uniformization theorems. The counterexample itself gives its own factors, completeness and normalization, and imports no false integer continuity theorem.

## Material antecedent and exact disposition

After the early seal, a source worker supplied only raw primary objects for [record 23062867](https://doi.org/10.5281/zenodo.23062867), dated 30 September 2026. I read its actual fourteen-page reader independently, including its full twist/logarithmic/critical-correction arguments. The API gives creation on 30 September, earlier than the reviewed PDF's 3 October date and its record's 4 October publication. The source body and its record identities are bound in the ignored cache; no foreign verification program was run.

Its Theorem 1.1 includes the reviewed existence conclusion, with stronger every-point claims, and its proof already supplies the small-C¹ regularized-radius curvature correction. The reviewed cutoff formula and inverse-coordinate positivity proof differ in presentation, but they do not establish a new existence conclusion. This is a concrete antecedent containment finding, not a general priority certificate.

`ANTECEDENT_DISPOSITION.md` identifies the exact affected original wording: the abstract's priority qualification, §1's proposed full geometric contribution and negative-search statement, the final hypothetical earlier-work limitation, and the missing reference. The negative-search sentence may accurately report what a past bounded search found; it cannot remain the current coverage account after this source is known. The result and critical mechanism must receive explicit attribution before promoting the original claim package. Theorem 1's literal existence statement remains mathematically supported.

The current protocol is to defer substantive defects or attribution gaps and move on. Therefore the disposition is **DEFER_ATTRIBUTION_CONTRIBUTION_CORRECTION**, with **SUPPORTED_AT_LITERAL_MATHEMATICAL_SCOPE** recorded separately. No manuscript correction or silently narrowed public replacement was made, and no site/page authorization is implied.

## Custody and completion

The review preserves the complete source baseline, immutable early seal, original reader renders, complete supplied foreign raw objects, primary acquisition/transfer receipts, read ledger, exact diagnostics, final verdict and a checkable manifest/seal. Full foreign text remains only inside the wholly ignored `primary-cache/`. No current sibling/source/adversarial review report was read. The prior raw TeX is bound and preserved in full, but full-TeX reading is claimed only for the reviewed paper; the prior's actual fourteen-page reader supplies the comparison.

`audit_evidence.py` rehashes source, early and final bindings and all primary/cache artifacts, and recomputes only the newly authored exact diagnostics without writing their timestamped output. It does not execute deposited or foreign source programs or access the network.

Completion is **100% of this bounded independent analytic and attribution assignment**. No central mathematical gap was found; the material outstanding issue is attribution/contribution correction before any promotion. Human/formal verification, exhaustive priority and any future revision remain outside this completion claim. Root retains the final Sheet/publication disposition.

# Independent analytic review: Global Hessian realizations of statistical manifolds

**Verdict: supported at the literal stated mathematical scope.** The global construction, dimension bound, positive Hessian neighborhood, ordered induced connections and two-torsion criterion survive this independent analytic audit. I identified no remaining central mathematical gap and no source correction to request. This is one bounded AI-assisted analytic review, not human peer review, formal certification, a priority determination or publication clearance.

The reviewed reader is the actual six-page deposited PDF, SHA256 `b874d63619ec7abbd3d9109639eb017b69435118c4cc9d5fec450605e4316e42`; the complete deposited TeX has SHA256 `97a749910fe2f340f000d82e1f1f46a4f0b26c975b1e5d54d2ce572a9cefed28`. Both were read completely, and all six rendered PDF pages were visually inspected. The source-ready seal is `449a6a692be6380e3c3e7bebab48f119cfe4da9ec0ac5524e4774a178344f7ca`. All 231 original source-baseline files are unchanged. Two later source-worker custody additions, `SOURCE_MANIFEST.json` and `SOURCE_SEAL.json`, are recorded additively in `FINAL_CUSTODY.json`; this agent did not create or alter them. No source program was executed and no source, website, shared script, Sheet, Git state or browser state was changed by this assignment.

## Independence and scope

The analytic approach reconstructs scalar-jet compatibility, fiberwise finite-dimensional lifting, an explicit smooth tubular potential, pointwise Schur positivity, and connection induction. The complete reader and TeX were read first. The substantive reconstruction in `INDEPENDENT_MECHANISM_NOTES.md` and provisional verdict were sealed at **2026-10-25 06:30:03 UTC**, before any external primary body, package history or sibling review report was read. The early seal has SHA256 `2f7598194155ce0548c9a467cffef108a1267e1cd6b7d6d091cb7a7163c4ac92`. The notes and all thirteen early bindings remain unchanged.

No current sibling or adversarial report was read at any stage. After the early seal, a source worker supplied paths and byte identities for two raw retained primary PDFs; I copied only those bodies, independently matched them to their original archived raw copies, and read them. Historical download timestamps remain supplied provenance, not a fresh successful download. No old review or authoring opinion was consulted. This preserves the distinction between independent mathematical reconstruction and later primary-source verification.

The exact target is a smooth Hausdorff second-countable boundaryless manifold of fixed finite dimension, with positive Riemannian metric and two prescribed mutually dual torsion-free connections. For dimension n≥1 the target dimension is N=binom(2n+4,3). Required outputs are a proper smooth embedding into one open U⊂R^N, one smooth globally defined Ψ on U with positive ordinary Hessian G, exact induced metric, and the exact ordered input pair induced by G-orthogonal projection from standard D and its G-dual D*. Both ambient connections must be torsion-free and flat on all of U.

No connectedness, compactness, completeness or uniform bounds are assumed. U can depend on the data and can be nonconvex and incomplete. Global injectivity of the gradient coordinates, a fixed probability model, dimension optimality and an indefinite or boundary extension are outside the claim. The zero-dimensional and empty cases are checked separately below. The manuscript expressly avoids historical-firstness and present-openness claims.

## The complete analytic chain

### 1. The ordered statistical pair is exactly metric plus cubic

Let L be Levi–Civita and K=∇−L, K*=∇*−L. The tensor T(X,Y,Z)=g(K_XY,Z) is symmetric in X,Y because ∇ and L are torsion-free. Duality gives T(X,Y,Z)=−g(Y,K*_XZ). Symmetry of K* in X,Z consequently also makes T symmetric in its first and third positions. These generate full symmetry. Thus K*=−K, and C=∇g=−2T. In particular,

    ∇ = L − C♯/2,       ∇* = L + C♯/2.

This determines the ordering. The signs are also checked directly by ∇g, rather than importing an α-connection naming convention.

Writing Γ_ijk=g(∇_∂i∂j,∂k), define the symmetric ordinary third-derivative array

    Q_ijk = ∂k g_ij + Γ_ijk
          = (∂i g_jk + ∂j g_ik + ∂k g_ij − C_ijk)/2.

Q is not a tensor. Under x=x(y), with X_a^i=∂a x^i and X_ab^i=∂a∂b x^i, its transformation is

    Q′_abc = X_a^i X_b^j X_c^k Q_ijk
           + g_ij (X_ab^i X_c^j + X_ac^i X_b^j + X_bc^i X_a^j).

The transformed connection contributes the first inhomogeneous term; differentiating the transformed metric contributes the other two. This is precisely the scalar third-jet law with first derivative zero and Hessian g. No term involving a third coordinate derivative remains, because the prescribed first jet vanishes.

The germ q_p(exp^L_p v)=g_p(v,v)/2−C_p(v,v,v)/12 has jets (0,0,g,Q). In normal coordinates its third derivative is −C/2; converting to other coordinates adds the three lowered Levi–Civita terms, giving Q. Smoothness of the local exponential map near the zero section gives a smooth jet-bundle section. A common injectivity radius and a complete exponential map are unnecessary.

The section is generally nonholonomic: it assigns a germ at each base point, rather than being the jet of one scalar function on M. Its zero value and first jet at every base point do not force its independently specified Hessians to vanish. The later coefficient field and ambient potential supply the actual globally defined objects.

### 2. One finite feature space lifts every pointwise scalar third jet

The proper smooth Whitney embedding e:M→R^K with K=2n+1 is an external topological input whose precise version was verified below. Let f consist of all monomials of degree at most three in the e coordinates, including the constant and all linear coordinates. There are N=binom(K+3,3) such features. A fixed linear coordinate projection recovers e; hence f is an injective immersion and topological embedding. For compact B⊂R^N, f⁻¹(B) is closed in compact e⁻¹(πB), proving properness. S=f(M) is therefore closed in R^N.

At each p, some n ambient linear functions restrict through e to local coordinates y. All polynomials of degree at most three in y−y(p) belong to the same ambient polynomial space. They realize arbitrary scalar third jets at p. Consequently E_p(c)=j³_p(c·f) is surjective at every point. This does not assert simultaneous interpolation by a single constant c over all M.

The smooth bundle map E has constant rank. Choose smooth positive bundle metrics and let R=E†(EE†)⁻¹. Surjectivity makes EE† positive definite fiberwise; matrix inversion is smooth on the invertible locus. Thus R is a globally smooth right inverse without a finite cover, a uniform smallest singular value, bounded coefficients or compactness.

For the smooth prescribed section J, set a=RJ and φ=−a. Freezing a(p) in the germ variable gives

    a·f=0,   a·f_i=0,   a·f_ij=g_ij,   a·f_ijk=Q_ijk.

Differentiation along the base point then includes derivatives of a. Differentiating the second and third identities yields

    f_i·∂jφ = g_ij,       f_ij·∂kφ = Q_ijk−∂k g_ij = Γ_ijk.

Also φ·df=0 identically. There is no period obstruction and no global primitive to glue. Positivity of g makes dφ injective on tangent spaces, but global injectivity of φ is neither proved nor needed. The manuscript's term “Lauritzen-type pair” refers to these identities; it does not silently assert the extra global embedding requirement for both components in Marugame's definition.

### 3. One smooth tubular function supplies the required first jet

Identify M with the closed embedded S. A variable Euclidean normal tube provides smooth r and ν with z=r(z)+ν(z), ν(z)∈N_r(z)S. At S, dr=P_T and dν=P_N for Euclidean orthogonal projections. This step requires no normal-bundle trivialization or constant tube radius.

Define Ψ₀(z)=φ_r(z)(ν(z)). Since φ annihilates TS, Ψ₀|S=0 and its ambient differential on S is exactly φ. Differentiating the ambient covector components along S gives

    (Hess Ψ₀)(f_i,·) = ∂iφ.

Thus its tangent block is exactly g. Along each fixed normal fiber r is fixed and Ψ₀ is linear, so its normal-normal block vanishes. In Euclidean orthonormal tangent/normal frames the Hessian at S is therefore [[A,B],[Bᵀ,0]], with A positive definite. B can be nonzero and unbounded.

The Euclidean normal bundle here constructs the potential; it is not asserted to equal the eventual G-normal bundle used for connection induction. Nonzero mixed block B is fully allowed. In particular, the conormal first jet need not vanish. Constant Ψ|S is consistent with positive tangent ambient Hessian because differentiating the restriction twice includes φ·f_ij=−g_ij.

### 4. Pointwise Schur positivity handles the entire noncompact image

Regard A and B intrinsically as bundle endomorphism/map using the Euclidean metric, and set

    t = tr(A⁻¹) ||B||²_HS ≥ 0,       λ=1+t,
    Ψ = Ψ₀ + λ(r)|ν|².

The trace and Hilbert–Schmidt norm are independent of orthonormal frame choices. Their values are smooth and finite at each point, even if unbounded over S. Because ν vanishes on S, the correction has zero value and first jet, and its on-S Hessian is exactly 2λP_N. Derivatives of λ do not introduce on-S Hessian terms.

For each normal w,

    ⟨BᵀA⁻¹Bw,w⟩ ≤ ||A⁻¹||op ||B||²_HS |w|² ≤ t|w|².

Completing the square for H=[[A,B],[Bᵀ,2λI]] gives

    H(v+w,v+w)
      = ⟨A(v+A⁻¹Bw),v+A⁻¹Bw⟩
        + ⟨(2λI−BᵀA⁻¹B)w,w⟩,
    2λI−BᵀA⁻¹B ≥ (2+t)I > 0.

This proves strict positivity at every point of S, including B=0. Define U as the open positivity locus of the Hessian of this one already-defined Ψ inside the tube. It contains all S. This uses pointwise openness, not one uniform neighborhood radius or an infinite sum of separately patched potentials. Restricting Ψ to U gives the single globally defined positive Hessian potential claimed. Properness into U follows because any compact subset of U is also compact in R^N.

### 5. Both ambient connections are flat, and the ordered input pair is induced

For G_AB=∂A∂BΨ the G-dual of standard D has coefficients

    (Γ*)^C_AB = G^CE ∂A G_BE.

Third derivative symmetry makes these symmetric in A,B, so D* is torsion-free. The functions η_E=∂EΨ have invertible Jacobian G and satisfy the affine-coordinate PDE

    ∂A∂Bη_E − (Γ*)^C_AB ∂Cη_E = 0.

The inverse function theorem supplies local D*-affine coordinates at every point of U, proving flatness. Global injectivity of η is unnecessary. Standard D is already flat and torsion-free.

The unchanged first jet yields G(f_k,·)=∂kφ. The pair identities therefore give f*G=g and

    G(f_ij,f_k)=f_ij·∂kφ=Γ_ijk.

This is exactly the G-orthogonal tangential projection formula for the connection induced from D. Thus the first induced connection is the prescribed ∇. Restricting ambient duality to tangent fields removes the G-normal terms. The second induced connection is the g-dual of ∇; uniqueness of the metric dual makes it exactly the prescribed ∇*. This checks both exactness and ordering, with no Euclidean/G-normal identification.

For necessity in the corollary, project the ambient torsion identity separately for each torsion-free ambient connection. Each induced torsion vanishes. Sufficiency is the established construction when both given torsions vanish. Dropping either torsion hypothesis is invalid; a concrete dual-pair negative control is included in the exact diagnostics.

## Boundary and attempted falsification audit

| Potential failure | Check and result |
|---|---|
| Scalar cubic treated as a tensor | Its three inhomogeneous coordinate terms are required and derived. Three independent nonlinear two-dimensional coordinate jets reject the incorrect tensor rule. |
| Confusing a(p) frozen in a germ with a field on M | The construction distinguishes the two derivatives. Exact nonconstant one-dimensional polynomial identities verify the metric and ordered connection; reversing φ's sign fails. |
| Nonholonomic jet section mistaken for a global scalar on M | Only a smooth jet section is lifted. The genuine ambient function is constructed later from its conormal first jet. No holonomic-section assertion is used. |
| Infinite atlas requiring infinitely many ambient coordinates | Every point uses the same finite polynomial feature space; local coordinates only prove its surjectivity. |
| Unbounded right inverse or small metric eigenvalues | Smoothness is pointwise; no uniform estimates enter. The exact Schur controls include input scales down to 10⁻³⁶ and large mixed blocks. |
| One global transverse constant on a noncompact image | The actual λ is a smooth variable function. A fixed-λ negative control has negative determinant. |
| Tube self-overlap or collapsing radii | The cited theorem gives a globally injective variable tube; no constant width is inferred. Its inverse supplies smooth r,ν even when the positive radius function is merely continuous. |
| Nontrivial normal bundle | All formulas use the normal bundle, retraction, trace and norm intrinsically. No frame is chosen globally. |
| Compact S and Ψ|S=0 | A nonzero conormal derivative supplies the extrinsic second derivative term; there is no minimum-on-S contradiction. The domain can be nonconvex. |
| Gradient coordinates fail to be globally injective | Flatness follows in local gradient charts. No global dual chart or convexity conclusion is needed. |
| Disconnected/noncompact/incomplete input | The proper embedding, bundle metrics, variable tube and positivity locus each apply without connectedness or completeness. Fixed dimension is retained. |
| Arbitrary torsionful dual pair | Both torsions are necessary by projection, separately. A positive-metric example with exactly one nonzero torsion rejects a weaker condition. |
| n=0 | A second-countable zero-manifold is countable discrete. Enumerate it properly into a subset of nonnegative integers; Ψ=z²/2 on R realizes its zero tangent data. Finite inputs and empty input are harmless. |
| Boundary, indefinite metric, finite regularity, fixed probability model or optimal N | Outside the literal theorem. This review supplies no such extension. |

The tempting route “import an arbitrary global Lauritzen pair, then extend it” remains unsupported unless that global pair is independently supplied. A local pair-extension equivalence cannot provide the missing global pair or an unrestricted uniform transverse constant. Likewise, an unrestricted finite-simplex theorem cannot simply be inferred from a compact-input theorem or a broad abstract. Those shortcuts transfer the central difficulty; they are not the route used to validate this paper. The explicit finite-feature/jet construction is the materially different mechanism that closes it here.

## Primary-source interfaces and limits

The detailed acquisition/read ledger and hashes are in `PRIMARY_READ_LEDGER.json`. Raw PDFs, extractions, challenge responses and primary-page renders are wholly under the ignored `primary-cache/` directory. The ledger explicitly distinguishes fetched bodies, retained bodies, metadata and unavailable bodies. These are bounded checks of the interfaces used here, not claims to have read every page of every cited work.

| Source actually inspected | Exact interface and outcome |
|---|---|
| [Whitney, 1936](https://people.math.osu.edu/davis.12/courses/6701/whitney36.pdf), printed 646–647, 654, 665; actual scanned pages | The countable-atlas manifold convention allows disconnected input; C^r includes smooth r=∞. Theorem 1 and Lemma 19 give embedding in R^(2n+1). Footnote 32 removes finite image-limit points by reciprocal-radius inversion, yielding the proper version in the same dimension. This verifies the imported version; the full original proof and every subsidiary lemma were not re-proved. |
| [Gualtieri, course notes part 11](https://www.math.toronto.edu/mgualt/courses/17-1300/docs/17-1300-notes-11.pdf), Definition 3.53 and complete Theorem 3.54 proof, printed 43–44 | The Euclidean normal-addition map is a diffeomorphism on a positive variable-width neighborhood for a regular embedded submanifold. Compactness is not required. The radius may be continuous; the addition inverse is smooth on its open domain. This supplies precisely the retraction/displacement used above. |
| [Lauritzen, IMS chapter](https://doi.org/10.1214/lnms/1215467061), printed 179–184, 187, retained actual body | The metric/cubic statistical framework, conjugate connections and induced connections by metric orthogonal projection match the conventions after the displayed sign calculation. This IMS chapter is distinct from the separate Lancaster pair note. |
| [Matumoto, 1993](https://doi.org/10.32917/hmj/1206128255), complete six-page body, printed 327–332 | Theorem 1 gives a contrast on M×M for a statistical metric/cubic. Its proof realizes compatible diagonal third-order data, then patches contrast functions. The discussion explicitly distinguishes flat statistical embedding as a further question. This is an antecedent, not a theorem giving the present global ambient positive-Hessian embedding. Cubic signs require matching ordered conventions. |
| [Amari, 1997](https://bsi-ni.brain.riken.jp/database/file/166/169.pdf), printed 81–85 and 87 | Dually flat requires zero torsion and curvature of both dual connections; affine and dual coordinates are used locally. The finite-dimensional compatible-embedding question on p.87 has the broad geometric scope used here. This reading verifies the historical formulation, not its current openness. |
| [Marugame, arXiv v1](https://arxiv.org/pdf/2103.10102v1), §§2.1–2.4, physical pages 3–6 | Definition 2.1 asks for a pair of embeddings; Theorem 2.2 is explicitly local. Its local primitive and transverse quadratic extension do not supply an arbitrary global pair or a uniform noncompact extension constant. The manuscript independently proves the weaker pair identities it needs and constructs its own global variable extension. The publisher body was not obtained here. |
| [Loi–Matta, arXiv v1](https://arxiv.org/pdf/2110.06145v1), physical pages 2, 6–7 | Theorem 1 starts from already N-induced data and proves generic robustness there. Proposition 6 chooses a minimum-norm inverse after a freedom hypothesis. These are valid antecedents to lifting methods; they do not by themselves realize arbitrary prescribed data. No publisher-version identity is assumed. |
| [Lê, arXiv v6](https://arxiv.org/pdf/math/0506163v6), physical pages 14–15, 22–23 | The Main Theorem, Theorems 5.1 and 5.6 explicitly assume compact input. The proof on p.15 uses compactness to choose a uniform scaling constant. This verifies the stated compact-input distinction. It is not identification with either final 2006 or final 2007 body, and the full theorem proofs were not audited here. |

The separate Lauritzen Lancaster note was not obtained; the author's institutional bibliography supplies metadata only. The final Lê 2006 article, final 2007 chapter, complete 2017 AJLS book chapter including p.239, and Abe's original body were not independently obtained/read in this assignment. The old MPI gluing discussions, Osipov curvature-class theorems, AJLS preview claims, and author-accepted versions were not separately re-audited here. Those are declared limits of this analytic review, rather than implied agreement with an unread account. The parallel source review remains responsible for its own complete literature comparison. None of these bodies is a deductive import in the explicit proof audited above. Their absence does not establish novelty or absence of earlier solutions.

Fresh DOI requests for Matumoto and Lauritzen IMS returned HTTP 200 anti-bot HTML, not bodies. No bypass was attempted. Later supplied raw retained PDFs matched both the current source-worker raw copies and the original archived raw files byte for byte. The original historical download pin was reported as 2026-10-15 11:45:12 UTC; I verified current byte identity, not the original network event. The failed current responses remain preserved and are never labelled successful body retrievals.

## Checkable diagnostics and evidence

`independent_exact_checks.py` is newly written diagnostic code using standard-library exact rational arithmetic. It does not execute deposited programs or import a package proof. Its recorded run is `independent-exact-checks.json`, with all checks passing:

- Three nonlinear coordinate second jets, each comparing all eight ordered third components from scalar composition, transformed metric/connection and the explicit inhomogeneous formula; the incorrect tensor rule is rejected.
- A noncompact real-line family with g(t)=1+t² and C(t)=t³+2t²+1, realized in the 1,t,t²,t³ feature subspace. Four polynomial jet identities plus exact metric and ordered-connection identities hold. A wrong-sign φ fails.
- Fifty-four exact Schur block cases across tangent/normal ranks one through three, input diagonal scales as small as 10⁻³⁶, mixed factors up to 10¹² and zero mixed blocks. Positive definiteness and the stronger tI−BᵀA⁻¹B semidefinite bound are checked by exact principal minors. The fixed-λ counterexample is detected.
- A positive Euclidean metric dual-pair example in dimension two with exactly one nonzero torsion demonstrates why both torsion conditions must be stated.

These finite checks are diagnostic corroboration with negative controls. The universal assertion rests on the derivations and the two verified differential-topology imports, not sample counts or floating-point tolerances. The exact program can be rerun in a disposable copy, since its normal invocation writes the result JSON with a new timestamp. `audit_evidence.py` is the read-only custody checker for the sealed review; it rehashes the original source baseline, immutable early seal, all retained primary/cache artifacts and the final manifest. It does not execute source programs or access the network.

## Final disposition

The strongest supported conclusion is the theorem and torsion corollary exactly as stated: global smooth, finite-dimensional, positive ordinary Hessian realization on one allowed open Euclidean domain, with proper embedding, exact metric and exact ordered induced pair. No central analytic repair, extra compactness condition, hidden period condition or global Legendre-coordinate hypothesis is needed.

This assignment is complete at **100% of the bounded independent analytic review**. No claim is made that the overall research program, historical comparison, adversarial convergence, editorial/publication process or any other paper is complete. Root retains publication authority and the separate adversarial/source reviews. The remaining limits are human/formal verification and the explicitly bounded primary coverage above; they are not silently converted into mathematical or novelty conclusions.

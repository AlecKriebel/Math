# Source-first independent scope record — frozen initial stage

UTC: 2026-11-17T05:05:24.520240+00:00. Best-guess completion toward this review family's full scientific task: **25%**. This is a work estimate, not a probability that the theorem is correct. No verdict, promotion, or publication decision is made at this stage.

## Independence and permitted inputs

This SCOPE family began with the parent's procedural source pins, title, version, asset sizes, page counts, and instructions. I remember no prior mathematical reading of this same manuscript or its upstream proof. I read the goal attachment and repository AGENTS.md, then the two terminal source custody files, source-tree path/size/hash/mode inventory, full native record JSON, the complete outer `main.tex`, and a fresh extraction and actual fresh render of all five native PDF pages. The broad initial filename search incidentally displayed names of other inventory folders; I did not read their contents. Filenames within the allowed source manifest disclose that dependency audits and formal artifacts exist; their mathematical contents have not been read.

Before freezing this record I have read **no** archive support prose, README, dependency ledger, old review, code, diagnostic result, upstream mathematical body, root review, opposite family review, or external primary mathematical source. No scientific program, native verification helper, old helper, proof assistant, compiler, or source script has executed. Only filesystem bookkeeping and ordinary read-only PDF information, extraction, and rendering ran. No external communication or network write occurred. No Git, website, spreadsheet, deployment, release, installation, or repair action occurred.

## Source authentication and controlling manuscript

The source root is `/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23203323/sources`. Exact observed inventory: **65 regular files, 11 child directories**, with all 63 payload entries and all directory modes matching SOURCE_MANIFEST.json. The two exact terminal names are SOURCE_FINAL.json and SOURCE_MANIFEST.json. There are eight `.tex` candidates by inventory, consisting of the outer single-file main and seven upstream build files; only the outer controlling file was read before this freeze.

* SOURCE_FINAL.json: 827 bytes, SHA256 `b81e34b2b75e26492b8e0111fbdce690666c640c1f365c749e58e01021f1450a`.
* SOURCE_MANIFEST.json: 14150 bytes, SHA256 `b5c7287bfd977986e3e4da06a69fc74dba88641e6e2fa16798f254e5403503c2`.
* Native `assets/paper.pdf`: 73988 bytes, SHA256 `5dfd859739d34d77eb97680ec11bb94439d793238d852bf6b99ab18d68281209`, **five pages**.
* Native `assets/source-and-verification.zip`: 510611 bytes, SHA256 `7fd3d023876a5957fcdf3166561f53e057788a20059cec122ddbcc0e6aa44e59`.
* Controlling `published-source/container-001/tree/main.tex`: 16157 bytes, **327 lines**, SHA256 `a42fed44cc32b314857963c2abbf525b30fc5cc52827eab16c61a4cb397cea61`. It contains no input/include directives and ends after its seven-item bibliography and document terminator.
* Distinct embedded `sources/family370/paper.pdf`: 406257 bytes, SHA256 `bb18015a30854675bec22e3183996625dac9be5046f81838c0bf9fbfa88806dc`. Its known 20-page inventory is distinct from the controlling five-page native PDF. I have not read its body and assert no version equivalence or substitution.

Full native text and all actual fresh page images were personally read. The outer TeX and native PDF agree in title, author/ORCID/date, full abstract, five section headings and order, equations (1)–(5), Theorem 1, Lemma 2, proofs and disclosures, and seven references. Page 1 contains the title through the provenance paragraph; page 2 contains Theorem 1 through the doubling selection; page 3 continues the selection and contains sections 3 and the first boundary-blow-up part of 4; page 4 completes section 4, section 5, and references 1–2; page 5 contains references 3–7. Mathematical bars on closures, superscripts, and function-space indices were checked in pixels rather than inferred from extraction, which loses some overlines and reorders some superscripts. This establishes substantive manuscript/source correspondence, not byte-identical recompilation of a PDF. No recompilation was attempted.

The source guard records every source file's byte count, SHA256, mode, every directory mode, and root mode. A second complete comparison after reading showed no changes. Fresh PDF tool stdout, stderr, and exit files, including zero-byte outputs, are retained. All five PNGs are fresh at 125 dpi and listed in the initial finite manifest.

## Full native metadata and rights scope

Record 23203323, concept 23203322, published state, version **1.0.0**, original publication date **2026-10-06**, DOI **10.5281/zenodo.23203323**, concept DOI **10.5281/zenodo.23203322**. Native metadata identifies a preprint in English, open access, **CC BY 4.0** (`cc-by-4.0`), creator `Kriebel, Alec`, ORCID `0009-0001-9320-500X`, and **affiliation null**. Record creation is 2026-10-07T04:57:16.797046+00:00 and modification 2026-10-10T21:26:53.821856+00:00, revision 5; these do not replace the publication date. Both native asset keys and sizes match the authenticated payloads, with the PDF listed first and ZIP second.

I read the complete native Description. It presents the work as a consequence note for all n at least 3 and p,q greater than 1 strictly below the Lane–Emden hyperbola; lists arbitrary proper-domain pointwise/gradient estimates, exterior decay, unrestricted zero-Dirichlet half-space nonexistence, and fixed C2-domain bounds and strong compactness; attributes the central entire theorem to OpenAI 2026 and transfer reductions to PQS/QS; disclaims an independent base-conjecture solution, new reduction, and first-priority claim. It says the upstream analytic proof was independently audited, actual Lean semantics inspected, complete kernel/axiom reproduction not achieved, and the follow-on not claimed formalized. It discloses extensive AI use and absence of conventional human peer review at publication. Diagnostics are explicitly not numerical proof certificates. These are author descriptions to assess, not independently established review outcomes. Native related identifiers give the OpenAI commit `adc7f1241b42e322a6451854ab7e4b4c146bf78a`, PQS DOI `10.1215/S0012-7094-07-13935-8`, and arXiv `2407.04154`.

CC BY 4.0 above is the native record-level rights statement. Upstream source licensing/attribution and any archive-specific rights still require their own later reading; native rights are not silently projected onto all embedded sources.

## Exact original claim treated as the target hypothesis

Let n be an integer at least 3, p,q>1 real, and

`1/(p+1) + 1/(q+1) > (n-2)/n`.

Set `alpha=2(p+1)/(pq-1)`, `beta=2(q+1)/(pq-1)`. A domain is nonempty, connected, open in R^n. A solution pair is nonnegative, C2 in the domain, and satisfies `-Delta u=v^p`, `-Delta v=u^q` pointwise. The original target includes **all** the following:

1. For every proper domain Omega != R^n, a universal C(n,p,q) bounds u by C d^-alpha, v by C d^-beta, |grad u| by C d^(-alpha-1), and |grad v| by C d^(-beta-1), with d the distance to the boundary. No boundary condition or boundary regularity is required.
2. If such a domain contains `{|x|>R}`, R>0, the same four estimates hold with d replaced by |x| for |x|>=2R, after changing C.
3. Every nonnegative pair in C2(H) intersect C(closure H), H={x_n>0}, with zero boundary values is zero, without a boundedness/growth assumption.
4. On each fixed bounded C2 domain, every nonnegative zero-Dirichlet classical pair continuous on the closure has a uniform L-infinity bound C(Omega,n,p,q).
5. For every fixed 1<r<infinity and 0<gamma<1, that entire solution set is bounded and sequentially compact in `[W^{2,r} intersect W^{1,r}_0]^2` and `[C^{1,gamma}(closure Omega)]^2`, in norm topologies. Norm constants may depend on r or gamma and the fixed domain.
6. If boundary regularity is C^{2,theta}, 0<theta<1, the set is bounded in C^{2,theta} and sequentially compact in C^{2,eta} for every fixed 0<eta<theta. It does not assert C2-on-closure solely from C2 boundary regularity.

Critical/supercritical exponents, p<=1 or q<=1, n<3, weighted equations, variable coefficients, weak/distributional solution regularity, parabolic statements, and the larger asymptotically-power extension are outside the original target. Reducing to n=3 or 4, radial solutions, bounded half-space solutions only, or selected already-classical exponent regions would leave the full original goal unresolved.

## Independent hand derivation from the original alone

This family emphasizes scaling, boundary limits, and the claimed exact function spaces. The following is my own checkable reconstruction. It deliberately exposes, rather than assumes proven, the imported entire/half-space inputs.

### A. Parameters and normalization

Since p,q>1, pq-1>0 and alpha,beta>0. Direct calculation gives

`p beta-alpha=2[p(q+1)-(p+1)]/(pq-1)=2`,

and similarly `q alpha-beta=2`. Thus for lambda>0, `U(y)=lambda^alpha u(x+lambda y)` and `V(y)=lambda^beta v(x+lambda y)` satisfy the same equations. Also `alpha+beta>n-2` is equivalent to the strict hyperbola: multiplying its two positive denominators leaves `2(p+q+2)>(n-2)(pq-1)` in both cases. This equivalence is an algebra check, not a proof of nonexistence.

If either nonnegative component has an interior zero, the strong maximum principle for its superharmonic equation makes that component zero on the connected domain; its equation then makes the other zero. Consequently every nonzero pair has both components positive. With `M=u^(1/alpha)+v^(1/beta)`, M scales by lambda. Choosing lambda=1/M(x) gives `U(0)^(1/alpha)+V(0)^(1/beta)=1` exactly. A normalization of U+V without exponents would not have this property when alpha!=beta.

### B. Exact conditional entire-to-domain implication

Write **T(n,p,q)** for: every bounded nonnegative classical entire pair is zero. T is an unresolved imported input at this source-only stage, not a new assumption added to the original theorem.

Suppose the quantity M d has no bound across all allowed domains/solutions. For every integer k choose y0 with M0 d0>2k. If the ball of radius k/Mj about yj contains a point with M>2Mj, move to such a point. Then

`M(j+1)>2Mj`, `d(j+1)>=dj-k/Mj`, hence `M(j+1)d(j+1)>2k` whenever `Mjdj>2k`.

Total movement before any step is `<2k/M0<d0`; an infinite sequence has a limit strictly inside the initial domain, whereas Mj tends to infinity, contradicting local boundedness. It stops at xk with M(xk)d(xk)>2k and M<=2M(xk) on its k/M(xk) ball. Rescaling gives a solution on B_k, bounds `0<=Uk<=2^alpha`, `0<=Vk<=2^beta`, and the nonzero normalization above.

For each fixed ball, bounded right sides give W2r bounds; take r large to obtain C1,gamma bounds. The power maps are Lipschitz on bounded nonnegative intervals because p,q>1, so their compositions have a uniform Holder bound, and interior Schauder estimates give C2,gamma bounds on smaller balls. A diagonal subsequence yields a bounded entire classical solution with retained normalization, violating **T**. Therefore **T** implies `M d<=K(n,p,q)`, and then the two pointwise estimates. This deduction does not prove T.

For rho=d(x)/2, the distance is >=rho throughout B_rho(x). Rescaling with lambda=rho bounds both components and RHS on B1. The Poisson gradient estimate at its center bounds `|grad U(0)|` by `C(||U||infinity+||V^p||infinity)`. Since `grad U=lambda^(alpha+1)grad u`, the claimed gradient exponent follows. The exterior-domain condition places every boundary point in the closed R-ball, so `d(x)>=|x|-R>=|x|/2`; all four radial decay powers follow. Properness matters because distance to an empty boundary is not the stated finite normalization.

### C. Boundary blow-up conditional on the full half-space theorem

Write **H(n,p,q)** for the unrestricted nonnegative zero-Dirichlet half-space nonexistence claim. The manuscript imports **T => H** from PQS Theorem 4.2. I have not read that primary proof yet. The distance estimate alone is inadequate near x_n=0, where it diverges. There is no derivation here replacing the unrestricted H by a bounded-only assertion without explanation. For the fixed-domain contradiction the eventual limit happens to be bounded, but the original published theorem additionally claims H for arbitrary growth and that claim remains part of success.

Assume **T** and **H**, plus the standard global/local Poisson regularity used below. If fixed-domain suprema diverge, let `Ak=max_closureOmega Mk`, choose xk attaining this maximum, and put lambda_k=1/Ak. Since the boundary values are zero, xk is interior for every nonzero pair. Then `0<=Uk,Vk<=1` and the correct nonzero normalization holds.

If `d(xk)/lambda_k` tends to infinity along a subsequence, the limit is the forbidden bounded entire pair. Otherwise extract a finite limit t>=0 and nearest boundary points bk. On a fixed bounded C2 domain, compactness supplies finitely many uniform boundary charts and a positive tubular scale. At sufficiently small scales xk is along the inward normal from bk. If the graph is phi_k with phi_k(0)=Dphi_k(0)=0 and uniform second derivative bound L, its rescaling psi_k obeys on any fixed |y'|<=R:

`|psi_k|<=L lambda_k R^2/2`, `|Dpsi_k|<=L lambda_k R`, `|D2psi_k|<=L lambda_k`.

Thus flattening gives a fixed half-space locally, top-order coefficients tending uniformly to the identity, first-order coefficients tending to zero, and uniformly controlled C1,1 charts. Local boundary W2r and embeddings yield C1,gamma control up to the boundary; interior estimates give C2 convergence away from it. Extract a bounded nonnegative half-space solution with zero trace. The normalization at the moving point (0,tk) passes by uniform C1 control: if t=0 it conflicts with the zero trace, and if t>0 it conflicts with H. Both branches are needed. Consequently T and H imply the fixed-domain supremum bound. No uniform boundary regularity over a varying arbitrary collection of domains was used or claimed.

### D. Exact strong compactness after the supremum bound

For one classical pair continuous on the compact closure, both components/RHS are bounded. On a bounded C2 (therefore C1,1) domain, solve the linear zero-Dirichlet Poisson problem in W2r intersect W1r_0, choosing first r>n to ensure continuity on the closure. Its difference from the classical component is harmonic with zero boundary values, so the maximum principle identifies them. The usual global estimate then applies for every finite r>1.

Uniform component bounds therefore give uniform W2r bounds for every fixed finite r. Given a fixed gamma<1 choose r so that `1-n/r>gamma`; the compact Sobolev embedding supplies a subsequence converging in C1,gamma, retaining nonnegativity and trace. Its powers converge uniformly by the bounded-interval Lipschitz property. The limit solves the equations distributionally and then classically in the interior. For each fixed finite r, the zero-Dirichlet estimate on differences gives

`||uk-u||W2r <= Cr ||vk^p-v^p||Lr -> 0`

and the analogous other component. This proves the asserted **norm** compactness, provided the supremum bound and standard elliptic estimates hold. A separate compact-embedding argument in W2r alone would not prove this conclusion.

For a fixed C2,theta boundary, uniform C1,gamma estimates give a uniform Lipschitz bound on components. Their powers are then uniformly Lipschitz and in particular C0,theta on the closure; global Schauder estimates give C2,theta bounds. Compactness in C2,eta follows only for eta<theta as claimed. No claim of compactness in the bounded endpoint C2,theta is introduced. Similarly neither gamma=1 nor r=infinity is claimed. Constants need not be bounded as any excluded endpoint is approached.

### E. Falsifiable boundary check

The strictness of the hyperbola has a concrete necessity check. At p=q=(n+2)/(n-2), take `a=(n-2)/2` and `w(x)=A(1+|x|^2)^(-a)`, with `A=[n(n-2)]^((n-2)/4)`. Differentiating radially gives `-Delta w=n(n-2) A (1+|x|^2)^(-(n+2)/2)=w^p`. Thus (w,w) is a bounded positive entire pair. Restricted to balls of radii tending to infinity, its fixed positive value at zero contradicts any domain-independent d^-alpha estimate there. This checks that extending the original claim to equality would fail; it is not a counterexample within the original strict range. The zero pair, all positive alpha/beta, t=0 boundary normalization, and exponent symmetry p<->q with u<->v were also checked by hand.

## What is established and the precise remaining task

The strongest result currently verified by this family is the source correspondence plus the algebra and the explicit **conditional** transfer chain above, including the boundary alternatives and strong compactness mechanism. The full original theorem has not been independently established. The central unresolved dependency is **T(n,p,q) throughout the original full strict hyperbola**, attributed to the unweighted corollary of the OpenAI pinned preprint. The supplied note's statement that an audit succeeded is not evidence substituted for this family's own primary proof review. The full substantive primary proof must later be read and checked, including the mechanism that actually supplies T, not just a theorem label, abstract, or low-dimensional known case. The exact PQS implication T=>H without growth, and its parameter/regularity compatibility, must likewise be read in its primary proof before completing this scope assessment. Standard elliptic inputs must be checked against their actual hypotheses. Archive support, licensing, diagnostics, and formal status remain unread pending the parent's explicit release.

Success means validating or locating a substantive gap in **every** part of the full original target at its native version, without silently shrinking the exponent/dimension range. If an upstream step simply restates or presupposes the central nonexistence problem, that route is blocked until a materially new proof mechanism is supplied. Current statements here are initial deductions and a work plan, not a verdict. This INITIAL stage is now frozen and held; no further scientific or support reading proceeds until explicitly resumed by the parent.

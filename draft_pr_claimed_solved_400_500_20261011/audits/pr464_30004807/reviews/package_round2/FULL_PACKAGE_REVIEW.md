# Second fresh independent full-package adversarial review: PR464 / 30004807

**Verdict: PASS for the frozen, qualified unrefereed preprint package. Blocking issues: 0. Required corrections: 0. Mathematical gaps within the stated theorem: 0.**

Reviewer: `/root/pr464_package_adversary2`. Round: 2. The target is `PACKAGE_REVIEW_INPUT_2.json`, SHA-256 `6354507a17d9eca504e5db085621b645fc4afb9cd00291e74ee0e5a145c8a352`, at original eligible head `97b2ed225574ca61bd03cb8db021a533e04938dc`. All eight final file hashes and sizes remain unchanged. This is a content, mathematics, provenance, reproducibility, PDF and metadata review. It does not approve an unreviewed publication helper, make a service write, or bypass the root's separate operations gate.

## Independence, hypothesis and success criteria

I read the entire current manuscript and publication descriptions, independently reconstructed its mathematical mechanism, fetched the primary sources, inspected their relevant pages and rendered all six manuscript pages before considering the first package review. I recorded `INDEPENDENT_INITIAL_CONCLUSION.md` before reading round 1. Its provisional conclusion was already zero required issues. Only afterward did I compare the earlier full report and the bounded priority ledger. Agreement did not replace reconstruction or fresh execution.

The exact hypothesis is a counterexample to the report's geometric regular-negative-mass-ZAS implication, under the explicitly specified natural static foliation and retained-boundary smooth vector-test convention. A successful counterexample must actually satisfy those geometric definitions, be a genuine timelike curvature singularity, contain an admissible compact test, and have an absolutely convergent complete contraction with nonzero value. Potential falsifiers include an omitted source premise; a coordinate-only area check; a wrong mass or causal limit; an old metric falsely claimed new; an incorrect Einstein tensor, index placement or flux sign; integration of divergent summands; substitution of a different test smooth structure; inadequate optimized guards; contaminated archives; or mismatched metadata and displayed equations. I actively checked these routes.

I created no original proof-search attempt, modified no frozen candidate/source/plan/helper, touched no index or branch, contacted no individual, and performed no external service write. Foreign PDFs, extracted foreign text, all renders, working environments and altered fixtures remain private and excluded from the positive output list. The available pinned interpreter was used read-only, not bundled.

## Primary-source scope and classical attribution

I independently retrieved and visually inspected the [official OWR report](https://ems.press/content/serial-article-files/46918), printed pages 2232–2233, including the conjecture across the page break. Geometric admissibility is regular negative-mass ZAS on spacelike slices. The later matter/evolution program is discussed separately; these pages state no independent NEC requirement or prescribed electromagnetic theory. The short wording does not formalize every possible foliation interpretation. The note explicitly states the cited static framework and declines to certify unstated author intent or stronger arbitrary-slice formulations. That qualification is substantive and present in the abstract, introduction and conclusion. The [publisher](https://ems.press/journals/owr/articles/8415343) confirms the distinction between volume/workshop year 2021 and publication on 26 November 2022.

[BKTZ v3](https://arxiv.org/pdf/1901.00813v3), Sections 1.3–1.4, page 6 footnote 3 and page 9 Definition 2.1/equation (2.5), uses the retained sphere and allows boundary-reaching vector support with a nonzero radial trace. I visually checked the latter pages and read the ensuing boundary calculation. The inhomogeneous formulation permits its limiting flux; the homogeneous identity additionally requires zero. Compact support confined to the open punctured interior, smoothness after collapsing the sphere, and independently smooth covectors are different requirements. The exhibited radial test satisfies even the optional angular-independent spherical-component restriction.

[Bray–Jauregui v2](https://arxiv.org/pdf/0909.0522v2), Definitions 3–4, 6–7 and 10, agrees with the paper's C1 graph convergence, smooth positive resolution, inward normal and mass. I visually inspected pages 5, 6 and 8 and read the time-symmetric setting and Section 6.6. These support the natural static-slice statement. They do not justify a universal arbitrary-tilt assertion, which is expressly excluded.

The [DKMV original](https://arxiv.org/pdf/gr-qc/0109069), visually checked pages 3–4, already contains the metric and stress formulas. Its substitution `(m,bar r,kappa,lambda)=(-2a,rho,A,B)` gives precisely the current family on `rho>a`. In particular its radial-pressure convention, rather than a tension convention, gives the present positive radial and negative angular coefficients at negative mass. Its subsequent wormhole classification assumes positive mass; the manuscript does not attribute the later negative-mass ZAS/Bianchi application to that classification. The [APS record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.65.064004) confirms Mukherjee spelling and publication on 7 February 2002. The construction and tensor are correctly credited before their use, including in the abstract.

After my independent reconstruction I read the entire earlier priority report, decision and 40-query ledger. Its exact older-metric dictionary and mandatory global-credit repair are reflected in the current source, metadata, README, current publication notes, portable scope note and root reconstruction. Two supplementary primary-domain searches for the exact regular weak-Bianchi counterexample and the DKMV/ZAS connection returned no result. Those empty searches are no proof of absence. I establish no historical first priority, continued-openness certificate or exhaustive literature coverage. The modest contribution described in the paper is the convergent counterexample application, not a new metric, tensor or general Stokes theorem.

## Independent mathematical reconstruction

### Resolution, full area quantifier and mass

For `a>0`, `phi=1-a/rho` is smooth on the retained exterior, positive on its interior, zero only on the boundary, and has inward Euclidean derivative `1/a`. Its Euclidean Laplacian vanishes. Thus `(delta,phi)` is a positive smooth harmonic resolution of `h=phi^4 delta`; this is stronger evidence than recognizing the standard spatial Schwarzschild example.

The C1 condition concerns approaching graphs over the compact boundary sphere. In the radial collar, write such a graph as `rho=a+u_n(omega)` with `u_n` and its first angular derivatives uniformly tending to zero. Its Euclidean area density is

    (a+u_n)^2 sqrt(1+|grad_S2 u_n|^2/(a+u_n)^2) dOmega.

This stays uniformly bounded. The maximum of `phi^4` on the graphs tends to zero, so all permitted physical areas tend to zero. Smooth changes of collar preserve the C1 definition. There is no restriction to coordinate spheres. The regular mass is

    -(1/4)[(1/pi)(4pi a^2)(1/a)^(4/3)]^(3/2)=-2a.

Zero shift and time-independent `h` give `K=0` on every natural static slice. The main lapse is strictly positive, and the spatial and time coefficients have the stated inverse-radius differentiated decay at infinity. No nondegenerate physical metric at the inner boundary is assumed.

### Curvature and parameter dictionary

The area radius satisfies `r=rho phi^2`, `dr/d rho=1-a^2/rho^2>0`, and `f=1+4a/r=((rho+a)/(rho-a))^2`. This coordinate change is used only on the smooth interior; it is not a boundary-smooth diffeomorphism after collapse. The spatial Ricci mixed eigenvalues are `(4,-2,-2)a/r^3`. Differentiating `q=sqrt(f)` yields the displayed derivatives and `Hess_h q=q Ric(h)`, `Delta_h q=0`.

The static warped-product formulas then give `R_g=0`, no time row/column of the mixed Einstein tensor, and spatial tensor `(A/N)Ric(h)` for `N=A+Bq`. These statements were also recovered by my own direct spherical-coordinate Christoffel/Ricci program, with no candidate-code import. Its sixteen component checks hold symbolically, not through parameter sampling. At `A=B=1/2`, `N=phi^-1` and the tensor is

    diag(0,2a/(rho^3 phi^5),-a/(rho^3 phi^5),-a/(rho^3 phi^5)).

The invariant square is `6a^2/(rho^6 phi^10)`, diverging positively; scalar flatness does not make the spacetime flat or removable. The angular null orthonormal vector gives `T(k,k)<0` because energy density is zero and angular pressure is negative. The disclosed NEC failure is correct.

### Genuine timelike singular end

For the main member, the optical radial coordinate has `s'=phi^3` and `s~(rho-a)^4/(4a^3)`. The radial metric becomes `phi^-2(-dt^2+ds^2)`, so its limiting radial conformal boundary is timelike. Nearby constant-radius tubes have spacelike normal and Lorentzian induced metric. Conserved energy `E=phi^-2 dt/dlambda` gives `|d rho/dlambda|=E/phi` and remaining affine length

    (rho-a-a log(rho/a))/E ~ (rho-a)^2/(2aE).

It is finite. Combined with invariant blow-up, this is a genuine singular end in exactly the limiting sense stated. The paper does not infer a smooth four-dimensional conformal completion from the two-dimensional radial picture.

### All-vector convergence: an independent harmonic-Hessian mechanism

The weighted spatial tensor is

    D^i_j=N phi^6 G^i_j=(Aa/rho^3)(6n_i n_j-2delta_ij).

My independent reconstruction identifies the useful identity

    D=2Aa Hess_delta(1/rho).

Since `1/rho` is smooth and harmonic on the closed exterior `rho>=a>0`, this immediately gives symmetry, zero trace and zero Euclidean divergence. This is independently checked symbolically in `independent_analytic_checks.py` and does not depend on trusting a shipped success flag.

For the conformal spatial connection, symmetry and tracelessness give

    D^i_j Gamma^j_ik=(2/phi)[tr(D)phi_k+D^i_k phi_i-D^k_j phi_j]=0.

The time row/column of `G` vanishes and `Gamma^j_it=0`. Consequently the complete ordinary interior scalar density for an arbitrary smooth test is exactly `D^i_j partial_i psi^j dt d^3x`. On compact support both factors are bounded up to the boundary and the Euclidean measure is finite. This proves absolute convergence for every specified time- and angle-dependent field, without spherical pole issues. Raising the first index of `G_munu nabla^mu psi^nu` is legitimate on the smooth interior. Lowering test indices by the singular metric is not used to change the boundary class.

Individual connection terms can have opposite nonzero logarithmic residues. The proof combines ordinary smooth summands before integration; it does not separately integrate divergent terms, use a principal value, or multiply distributions. The scalar absolute-integrability statement is precisely the one needed, not a claim of absolute integrability of all tensor components.

### Exact oriented defect and admissible test

The inner outward normal of a truncated exterior is `-n`. The radial eigenvalue is `4Aa/rho^3`, so integration by parts and the smooth boundary trace give

    I_N(psi)=-(4A/a^2) integral_(R x S_a) psi_spatial dot n dt dA_delta.

The cutoff field `psi=eta(t)chi(rho)partial_rho`, with time integral one and `chi=1` near `a`, is smooth on the entire retained boundary because `partial_rho=x^i partial_i/rho` and `a>0`. Its normal component need not vanish for a tangent-bundle section. Its spherical components are angular independent. Its complete density is `4Aa eta partial_rho(chi/rho)`, confirming both sign and factors independently. The endpoint gives `-16pi A`, hence `-8pi` in the main case.

### Endpoint and scope challenges

- `A=0,B>0` is the negative-mass Schwarzschild vacuum after time rescaling; the entire Einstein tensor and functional vanish. Sharing its spatial metric does not make the main lapse vacuum.
- `B=0,A>0` remains Lorentzian, and the same weighted density proves convergence even though the individual curvature exponent is stronger. The main order-minus-five assertion is not incorrectly applied to this endpoint.
- `A=B=0` and lapse-zero signed parameters are excluded. The lapse positivity hypotheses are explicit.
- `a=0` is excluded. A shrinking-sphere radial field is not a fixed smooth origin-crossing vector. There is no flat-space contradiction from taking a limit in a changing test class.
- The uniformly spacelike local tilt has resolved radial coefficient `1-q^2>0`, inward derivative `1/(a sqrt(1-q^2))`, and mass `-2a/(1-q^2)`. The nearly null tilt produces `phi^6` radially; any simple smooth defining factor leaves a zero radial resolved eigenvalue. The paper correctly declines all-arbitrary-tilt regularity.
- `lim_(x->0)x^5 G^rho_rho=2a^3` is nonzero. BKTZ's strict positive-power improvement is absent, so its sufficient theorem cannot be the proof. The separate exact cancellation supplies the missing convergence.
- Open-interior tests yield the ordinary zero identity. Collapsed-point tests, independently smooth covectors, added energy conditions and specified matter models are outside the theorem. These exclusions recur in all current claims and are not hidden assumptions.

No circular step or replacement of the central difficulty by an unsupported equivalent assertion was found. The analytic proof supplies the surface and test-space universal quantifiers; finite checks are supporting falsification evidence.

## Complete archive and provenance audit

`check_package_integrity.py` passed 1,941 explicit conditions: the eight frozen top files and three internal source/math/install-plan bindings; all 181 unique ZIP entries; exact positive inventory equality and CRC; all 180 payload hashes/sizes and equality to local package bytes; all 138 selected origins; all 13 original snapshot files; all 11 extant historical payload references; the unattested digest distinction; exact canonical metadata and the two upload names. Path traversal, canonical aliases, symlinks, private folders, environments and foreign binary sources are absent from the actual archive selection.

`check_supplement_inventory.py` passed 8,265 explicit conditions, including duplicate-key parsing of every one of the 54 JSON entries and complete validation of all 185 proposed install entries. Each destination is the exact matching relative payload under this problem's preprint folder. The union is exactly the frozen archive payloads/manifest plus final outputs. These are content checks only; no remote branch update was attempted. All 181 entries decode as authored UTF-8 text. All 13 Python entries parse; they comprise nine unique sources, each read at source level, including the two historical checkers and two archived development runners. The source import inventory contains no network or credential library. High-specificity credential signature scans have zero hits; such scans are supplementary, not a universal secret oracle.

The old standalone author-manifest hash has no supplied bytes or path. It remains explicitly `UNATTESTED`; no twelfth payload reference or reconstructed manifest is claimed. The separately bound thirteen-file history remains intact. Historical omission of DKMV attribution is explicitly superseded by current attribution notes. Assignment-time pending-gate text and earlier repair requirements remain history, not a competing current publication verdict.

One archived historical replay receipt contains an informational absolute interpreter path. It contains no environment or credential and is not a runtime dependency of the portable core. The 35 positively listed core payloads and current replay outputs have no such local path requirement. This is an informational provenance observation, not a required repair.

The hash structure is noncircular: the ZIP contains its 180-payload manifest without hashing that manifest into itself; the outer frozen review independently binds manifest, ZIP and PDF. No future self-DOI is fabricated or inserted into its own checksum. The package accurately states that hashes enable received-byte comparison, not independent authentication of an entirely replaced bundle.

## Fresh complete reproduction and independent rejection probes

I extracted the delivered ZIP into a fresh private temporary directory whose name contains spaces. Full normal and optimized entry-point executions used the read-only Python 3.14.6 interpreter with SymPy 1.14.0 and mpmath 1.3.0. Both exited zero with empty stderr and produced exactly 9,728 bytes matching the shipped full result, SHA-256 `8e46c0fdb6a61ca4ec1be99573e3e2aa97fa3507afb1fc64beae5f36d3503ce8`. The result profile is `full`, not the explicitly narrower dependency-free profile.

The actual results contain all four guarded historical executions (17 and 35 checks in each mode), rational independent counts 396, 1,557 and 2,916, the 72 Cartesian points, 67 symbolic checks with exact names, all 16 false-claim families actually rejected in both modes for 32 subprocess rejections, and the 13 driver guard controls. The false-claim executions require exit code 4 and the exact intended `InvalidClaim` diagnostic; crashes do not count. All generated fixtures and working copies were removed. The driver rechecks received payloads and history after execution and writes only to private temporary work.

The portable driver and all nine unique Python sources were inspected. The rational programs independently build metric jets and connection/Ricci contractions, retaining essential second angular derivatives. The symbolic route starts from a generic lapse, chooses the positive branch explicitly, and transports radial vector components. The historical author's final assertion disappears under optimization, but the current wrapper actively checks actual Booleans, exact names/counts, byte output, subprocess status and diagnostics through explicit exceptions. No universal assertion is proved merely by checking these finite points.

My independently authored symbolic checker passes 42 exact deductions normally and optimized, with identical output bytes. In addition to all Einstein components it checks the harmonic-Hessian density mechanism, connection contraction, divergence, normal flux, main invariant, endpoint controls, borderline coefficient, optical and affine orders, harmonic resolution and tilt formulas. It imports no candidate checker.

`check_guard_rejections.py` runs 47 probes per mode: two valid controls and 45 intended rejections. It independently challenges false/non-Boolean flags and checks, missing/substituted/extra names, Boolean/float/string or wrong counts, duplicate outer/nested JSON keys, unsafe canonical paths and symlinks. Eight cases in each mode exercise the actual copied-package CLI: changed/missing/symlinked payload, duplicated manifest path, Boolean byte count, noncanonical path, forbidden-environment path, and duplicate manifest JSON key. Every actual CLI rejection exits 2 with empty stdout and an intended `VerificationError`, not a traceback or accidental crash. Only valid result receipts are delivered; altered fixture bytes stay private and are removed. Normal and optimized probe outputs are identical.

## PDF, metadata and global consistency

I independently rendered and viewed all six bound PDF pages at 100 dpi. The title, author/ORCID/version, classical attribution, full geometric and analytic proof, coefficient/sign formulas, scope limitations, AI disclosure and all four references are readable and complete. I found no clipping, overlap, missing glyph, unresolved citation, broken formula or omitted proof paragraph. The PDF's displayed mathematics agrees with the source. The source/PDF hashes are recorded in `PDF_QA.json` and remain exactly the frozen ones.

`metadata.json` and `deposit.json` contain exactly the same metadata object, canonical title, sole creator Alec Kriebel and ORCID, preprint type, version 1.0, date 12 October 2026, English, open access and CC BY 4.0. The two selected uploads are exactly the paper and verification ZIP. The description, current note, README, portable scope note, root reconstruction and manuscript agree on classical attribution, static/boundary test scope, NEC violation, bounded priority and extensive AI use. They do not claim a new metric/tensor, a general new boundary theorem, formal proof certification, independent human peer review, journal acceptance or first historical priority. The unrefereed status is visible in the paper and metadata.

## Comparison, final disposition and remaining process

Only after recording my independent initial conclusion did I read the complete first-package report and RESULT. It is bound to the same final eight files and manifest. Its zero-required-issue conclusion is consistent with my own reconstruction and probes; no overlooked repair emerged from the comparison. Earlier priority requirements are correctly implemented in current publication claims. Historical stage text remains labeled history.

**Required content corrections: none. Blocking content/math/provenance/PDF/metadata issues: none.** The result is acceptable as the explicitly qualified concise unrefereed note. This is not a certificate for unstated author intent, a stronger matter/tilt/test conjecture, historical first priority, human refereeing or universal formal verification.

The root separately reported archive-preparer safety findings in operations review 2. Those concern helper source and generated-output dispatch, not the unchanged frozen eight-file candidate reviewed here. I do not approve those helpers or count unresolved workflow repairs as a defect in these received mathematical publication bytes. The root must complete the new independent operations review and its final gate before any publication, tracker append or PR integration/merge. No candidate was rebuilt or modified by this review.

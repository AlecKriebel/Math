# First fresh full-package adversarial review: PR464 / 30004807

**Verdict: PASS for the frozen, explicitly qualified unrefereed preprint package. Blocking issues: 0. Required corrections: 0.**

Reviewer: independent AI subagent `/root/pr464_package_adversary1`. Review round: 1. Original candidate head: `97b2ed225574ca61bd03cb8db021a533e04938dc`. The actual input is `PACKAGE_REVIEW_INPUT_2.json`, SHA-256 `6354507a17d9eca504e5db085621b645fc4afb9cd00291e74ee0e5a145c8a352`. The superseded first package manifest was not used as the current acceptance target. This verdict concerns the mathematical/content/archive candidate; a second new full-package reviewer and the separately reviewed publication/merge operations remain required. It does not itself publish, mutate a PR, or certify human peer review or historical first priority.

## Reviewed claim, independence, and potential falsifiers

The hypothesis reviewed is that the supplied note proves a counterexample to the geometric regular-negative-mass-ZAS implication in the cited OWR report, using natural static slices and the BKTZ manifold-with-boundary vector-test convention. A falsifier would include an omitted source hypothesis, wrong slice resolution or mass, nonsingular/non-timelike inner end, wrong curvature/index contraction, inadmissible test, nonabsolute integral, wrong boundary sign, circular proof, uncredited old construction, contradictory current claims, contaminated archive, false replay acceptance, or unmatched metadata/PDF/source bytes.

I read the complete manuscript source and current package descriptions before relying on prior verdicts. I independently reconstructed its key algebra and limit arguments, fetched the four primary PDFs, inspected the actual problem/test/resolution pages, and independently rendered all six manuscript pages. The earlier mathematical and priority reports were then read as comparison evidence. I examined the complete current verification entry point and its four transferred checker programs, independently extracted the delivered ZIP, reran the full entry point normally and with optimization, inspected actual result fields/counts/bytes, and performed additional rejection challenges. No author or peer checker was imported into a new mathematical derivation. Guard probes intentionally import the current verification entry point to challenge its checks; this is separately identified and is not claimed to be an independent curvature derivation.

Parent-supplied successful replays were received only as additional evidence. The fresh executions documented below are my own. No source snapshot or current candidate input was edited. No original proof-search attempt, external individual contact, Git/index/branch operation, publication/API write, or PR mutation was performed.

## Direct primary-source and priority comparison

The independently retrieved [official OWR report](https://publications.mfo.de/bitstream/handle/mfo/3893/OWR_2021_40.pdf?isAllowed=y&sequence=1), printed pages 2232–2233, separates geometric singularity admissibility from its later matter/evolution program. Its conjecture refers to regular negative-mass ZAS on spacelike slices; these pages do not add an independent energy condition or specified electromagnetic constitutive law. The terse wording does not formalize every possible slicing interpretation. The paper states its static-foliation interpretation explicitly. The report's volume/workshop year is 2021; the [official publisher](https://ems.press/journals/owr/articles/8415343) confirms publication on 26 November 2022. I accept the expressly stated geometric implication, not an assertion about unstated author intent or every stronger interpretation.

[BKTZ v3](https://arxiv.org/pdf/1901.00813v3), Sections1.3–1.4, page6 footnote3, and page9 Definition2.1/equation2.5, support the retained inner boundary and boundary-reaching vector tests. The radial normal trace is allowed. Its homogeneous identity requires a zero functional; the inhomogeneous identity permits the limiting flux. The source's sufficient theorem requires a strict positive-power curvature improvement. The present note credits the existing flux calculation and independently proves convergence instead of applying that theorem outside its assumptions.

[Bray–Jauregui v2](https://arxiv.org/pdf/0909.0522v2), Definitions3–4,6–7,10 and Section6.6, supply the approaching-graph C1 condition, smooth positive resolution, inward normal, regular mass, and the separate status of extensions beyond time symmetry. These support the exact slice assertions made. They do not justify an all-arbitrary-tilted-slices claim, and none is made.

The known geometry and tensor are correctly credited to [Dadhich–Kar–Mukherjee–Visser](https://arxiv.org/pdf/gr-qc/0109069), equations9–15. The exact substitution is `(m,bar r,kappa,lambda)=(-2a,rho,A,B)`. On `rho>a`, the positive square-root branch gives `sqrt(1+4a/r)=(rho+a)/(rho-a)`. The old radial pressure and angular stress give precisely the present signs and coefficients. Its later wormhole classification uses positive mass; the manuscript attributes the negative-mass application to its own substitution rather than claiming that earlier classification printed the later ZAS/Bianchi conclusion. The [APS record](https://journals.aps.org/prd/abstract/10.1103/PhysRevD.65.064004) confirms Mukherjee spelling and publication on 7 February 2002, distinct from the March issue date.

The current abstract, introduction, construction, tensor calculation, bibliography, metadata, package README, publication notes, portable attribution note and root claim/reconstruction notes all retain these credits. The earlier priority reviewer required this repair; it is now implemented in all current publication claims. Immutable history is expressly superseded, not silently rewritten. No metric, tensor, general Stokes theorem, formal verification, human refereeing, historical first priority or continued-openness certificate is claimed.

I read the complete priority report and its decision/bibliography and challenged the exact old-family dictionary against the primary equations. I also ran four additional exact-conjecture/old-family searches; they produced no new primary evidence of an earlier exact refutation. This is a limited supplementary search, not a repeat of the earlier40-query corpus or an exhaustive priority certificate. The recorded full-text/index/unpublished-material gaps remain accurately disclosed. No prior exact resolution was established by this review, and the older metric alone is not proof that the later application had already appeared.

## Independent analytic challenge

### Regular geometry and quantified surface condition

Let `a>0`, `rho=|x|>a`, `phi=1-a/rho`, and `h=phi^4 delta`. The Euclidean metric extends positively to the retained sphere. The conformal factor vanishes simply, is positive outside, has inward derivative `1/a`, and satisfies `phi''+2phi'/rho=0`. Thus its harmonic resolution is direct, not inferred from coordinate-sphere areas.

For a C1 boundary graph `rho=a+u_n(omega)` approaching the sphere, both `u_n` and its first angular derivatives tend uniformly to zero. The Euclidean graph area density is

    (a+u_n)^2 sqrt(1+|grad_S2 u_n|^2/(a+u_n)^2) dOmega.

It is uniformly bounded on the compact sphere. The maximum of `phi^4` on the graphs tends to zero, so every permitted graph's h-area tends to zero. This checks the full definition's quantifier. Substitution in the regular mass formula gives

    -(1/4)[(1/pi)(4pi a^2)(1/a)^(4/3)]^(3/2)=-2a.

The lapse is positive in the stated family and the shift is zero. Since h is time independent, `K=0` on every natural static slice. The spacetime is smooth Lorentzian on the interior; no nondegenerate boundary extension is assumed. The main lapse and spatial conformal factor tend to one with differentiated inverse-radius decay, giving the stated asymptotic flatness.

### Curvature and genuine timelike singular end

The interior-only change of radius has

    r=rho phi^2, r'=1-a^2/rho^2>0, f=1+4a/r,
    h=f^(-1)dr^2+r^2dOmega^2, q=sqrt(f)=(rho+a)/(rho-a).

The spatial mixed Ricci eigenvalues are `(4,-2,-2)a/r^3`; hence their trace is zero. With `q'=-2a/(q r^2)` and `q''=4a/(q r^3)-4a^2/(q^3 r^4)`, the displayed radial/angle Hessian formulas give `Hess_h q=q Ric(h)` and `Delta_h q=0`. The static warped-product Ricci formulas follow directly from the time connection of `-N^2dt^2+h`. For `N=A+Bq`, the resulting time component is zero and spatial mixed Einstein tensor is `(A/N)Ric(h)`, with zero trace and no omitted off-diagonal terms. For `A=B=1/2`, this is exactly

    diag(0,2a/(rho^3 phi^5),-a/(rho^3 phi^5),-a/(rho^3 phi^5)).

Its Ricci-square invariant is `6a^2/(rho^6 phi^10)`, which diverges positively at the inner end. Zero scalar curvature therefore does not establish removability or flatness. The angular null frame vector gives negative `T(k,k)` because energy density is zero and angular pressure is negative. The NEC failure is correctly stated prominently, not hidden in an auxiliary report.

For the main member, `s'=phi^3` and `s~(rho-a)^4/(4a^3)`. The radial metric is `phi^(-2)(-dt^2+ds^2)` and the limiting radial boundary is timelike. Nearby constant-radius tubes have spacelike normal and Lorentzian induced metric. Conserved null energy gives `|rho_dot|=E/phi`; the remaining affine length is `(rho-a-a log(rho/a))/E`, finite and of order `(rho-a)^2/(2aE)`. Combined with the invariant divergence, this establishes the stated singular end. The manuscript carefully qualifies the timelike statement as its limiting radial causal sense, avoiding an unsupported four-dimensional smooth conformal extension.

### Absolute all-field contraction and sign

The positive volume density is `N phi^6 dt d^3x`. The weighted mixed spatial tensor is

    D^i_j=(Aa/rho^3)(6n_i n_j-2delta_ij), n=x/rho.

It is smooth on the closure, symmetric and traceless. The conformal spatial connection gives

    D^i_j Gamma^j_ik=(2/phi)[tr(D)phi_k+D^i_k phi_i-D^k_j phi_j]=0.

The time row/column of G and `Gamma^j_it` vanish, so arbitrary time and angular dependence leave the exact pointwise scalar density `D^i_j partial_i psi^j dt d^3x`. Both factors are bounded on every compact support, including its boundary trace, and the coordinate measure of that support is finite. This proves absolute integrability of the complete scalar for every stated test. It is not a proof that individual singular connection summands are integrable, and no such claim is used. The interior equality with `G_munu nabla^mu psi^nu` is legitimate index raising on a smooth metric; independently smooth boundary covectors are explicitly a different test class.

The radial/tangential eigenvalues of D are `4Aa/rho^3` and `-2Aa/rho^3`. The radial divergence expression `D_r'+2(D_r-D_T)/rho` is exactly zero. At the inner boundary of the truncated exterior, the outward normal is `-n`, producing

    I_N(psi)=-(4A/a^2) integral_(R x S_a) psi_spatial dot n dt dA_delta.

The compact smooth radial test with time integral1 and radial boundary value1 belongs to the stated tangent-bundle section space even though its normal trace is nonzero. Its whole density is `4Aa eta partial_rho(chi/rho)`. The endpoint contribution gives `-16pi A`, hence `-8pi` for the main member, independently checking orientation and all area/normal/lapse factors. This is an ordinary absolutely convergent scalar integral formed before integration, not separate divergent integrals or a principal value.

### Boundary and limiting-case challenges

- `A=0,B>0`: the whole Einstein tensor and functional vanish; this is the negative-mass Schwarzschild vacuum after time rescaling. Sharing its spatial metric does not make the main lapse vacuum.
- `B=0,A>0`: the family metric remains Lorentzian. Its stronger individual curvature singularity still cancels in the weighted whole density, so the family's stated convergence and defect remain valid. The proof does not incorrectly extend the main member's order-minus5 asymptotic to this endpoint.
- `A=B=0` and lapse-zero signed parameters are excluded. Positivity hypotheses are explicit.
- `a=0` is excluded. Shrinking the retained sphere changes the radial test; the `x/|x|` test is not a fixed smooth origin-crossing field. No anomalous flat-space defect follows.
- For a local uniform tilt, the resolved radial coefficient is `1-q^2>0` and the inward derivative is `1/(a sqrt(1-q^2))`; its mass is `-2a/(1-q^2)`. A nearly null tilt has radial coefficient `phi^6`, so dividing by any smooth simple defining factor to the fourth power leaves a degenerate radial boundary eigenvalue. These calculations justify the precise distinction; neither arbitrary-tilt regularity nor a stronger energy/matter theorem is claimed.
- Open-interior-only tests give the ordinary classical zero identity. Collapsing the sphere changes the smoothness class and does not preserve the exhibited radial test. These alternatives are explicitly excluded from the current implication.
- The main mixed radial Einstein component has exact leading value `lim_(x->0)x^5 G^rho_rho=2a^3`, so the strict improved-bound theorem cannot be invoked. The note relies on the separately proved cancellation, avoiding that possible circularity.

No unsupported claim replacing the central difficulty was found. The analytic derivation supplies the universal quantifiers; finite computations are consistently labeled supporting evidence.

## Archive, provenance, and current global material

`inspect_archive.py` independently checked all eight manifest-bound candidate inputs, all181 unique ZIP entries, exact entry-set equality, CRC, all180 payload sizes/SHA-256 values, and equality to the corresponding on-disk package bytes. All entries are authored text/code/JSON, including the one internal payload manifest. Every JSON was parsed with duplicate-key rejection. There is no foreign PDF/image, environment, credential file, invalid fixture, private directory, encrypted entry, symlink, path traversal or unexpected binary. High-specificity credential-pattern scans returned zero hits; this is supplementary to explicit selection inspection, not a claim of a universal secret-detection oracle.

All138 review-evidence selection entries match their declared origin bytes, sizes and hashes. All185 proposed branch-install payloads and destinations match their binding and remain inside the selected problem's preprint folder; this is read-only content validation, not an operations/CAS/merge authorization. The separately bound source receipt, mathematical gate and branch-install plan also match the frozen manifest's digests.

All13 historical files are byte-preserved and bound to the captured original head. The six author and five audit payload references are checkable and are actually checked. The standalone author-manifest digest has no supplied original path/bytes and is explicitly UNATTESTED everywhere relevant. No missing manifest was fabricated. Current attribution/scope notes clearly supersede old presentation omissions. Evidence reports retain their assignment-time stage and repair requirements as history; their presence does not override the current manuscript or imply that this package was reviewed before it existed.

The portable core contains35 positively listed payloads plus its nonself-hashing manifest and separate delivery whitelist. The main ZIP's internal SHA256SUMS excludes its own digest, while the outer frozen review binds that sidecar and the archive/PDF independently. The public record's future self-DOI is not inserted into its own archive and no circular self-hash is claimed. Sidecars make received-byte comparison reproducible; they do not authenticate an adversarial replacement of an entire package independently of the external frozen hash.

An archived historical reproduction receipt contains an absolute interpreter path. This is informational evidence, not a bundled private environment or an executable path dependency. The portable35-file core and its current result output contain no local path dependency. The README's corresponding core-inventory statement is true; I do not count the historical path as a required publication correction.

The original drafting source differs from the final package source only in the shortened, still-accurate reproducibility paragraph and smaller bibliography font. The theorem, proof, attribution, scope and disclosures agree. Current publication-note copies agree exactly. The root ledger/reconstruction, package landing text, metadata and portable note agree on target, coefficients, signs, historical limitations and review status.

## Fresh reproducibility and adversarial guard execution

I extracted the delivered archive into this review's ignored private directory; I did not run the live package in place. I used the available Python3.14.6 interpreter with independently pinned SymPy1.14.0 and mpmath1.3.0. Full normal and optimized driver executions each exited0 with empty stderr and produced the exact shipped9728 bytes, SHA-256 `8e46c0fdb6a61ca4ec1be99573e3e2aa97fa3507afb1fc64beae5f36d3503ce8`.

For each run I inspected the actual full profile, dependency versions,13/11/unattested history fields, four historical17/35 normal/optimized executions,396/1557/2916 independent rational counts,72 Cartesian points in the relevant expected result,67 symbolic checks and names, and all16 false-claim families in both modes. All32 subprocess rejections have required exit4 and the exact intended `InvalidClaim` diagnostic; an accidental crash is not accepted. All13 driver guard controls are also required. A summary `PASS` alone was not used as the criterion.

The entry point is read-only with respect to received payloads and history and rechecks them after execution. Generated false inputs and working copies are temporary and removed. It checks byte output equality, generated JSON equality, explicit Boolean true values, exact names/counts, actual integer types, success flags, subprocess status and unexpected diagnostics. Its exceptions remain active under optimization. The historical removable assertion is therefore accurately treated as insufficient alone and compensated by current explicit guards. The dependency-free profile is separately labeled and cannot masquerade as the full replay.

The copied checkers were inspected at source level. They derive curvature from coordinate definitions or exact metric jets, preserve angular second derivatives where needed, and do not import the author's or historical auditor's formulas. Their finite-supporting status is visible. The exact symbolic program computes a generic lapse first, selects the positive radial branch explicitly, tracks vector components under radius change, and requires the deliberately false claims to be actually false before counting rejection.

In addition to the package's own tests, `probe_guards.py` challenges the active guard functions with21 malformed flag/count/check-name/duplicate-key objects,10 unsafe-path/symlink cases, and3 real copied-package corruptions in each subprocess mode. Each probe runs normally and optimized. Every challenge is rejected; the six subprocess cases per probe have exit2 and an intended `VerificationError`, empty stdout and no traceback. Malformed fixture bytes stay private and are removed. Only valid rejection receipts are delivered. This tests failure behavior independently of trusting the shipped success flag.

## PDF and submission metadata

The bound PDF has6 letter-size pages,85,393 bytes, and SHA-256 `015c034b3ef39044823ebe56291c043f5e96752ac5e0476fde5ac739bef9608a`. I independently rendered and viewed every page. Page1 states the old-family attribution and precise scope in the abstract; page2 contains the dictionary/theorem; pages3–5 contain the complete geometry/curvature/density/flux proof; page6 retains boundaries, reproducibility, AI disclosure, unrefereed status and all four references. No clipping, overlap, missing glyph, unresolved citation/equation reference, misplaced sign, omitted proof paragraph or unreadable formula was found. Source and displayed mathematical content agree.

Canonical metadata and deposit metadata are exactly equal objects. Title, sole creator Alec Kriebel, ORCID0009-0001-9320-500X, version1.0, publication date2026-10-12, English language, publication/preprint type, open access and CC BY4.0 agree with the package. Upload inventory is exactly the PDF and supporting ZIP. The description retains classical attribution, nonzero defect, explicit test/slice boundaries, NEC failure, bounded priority and extensive AI/unrefereed/no-human-peer-review disclosure. No fabricated DOI, first-priority assertion, journal acceptance, stronger matter theorem or false human-review status appears.

## Final disposition and limits

The frozen package meets the content and reproducibility requirements for this qualified concise research note. Required corrections found by this round: **none**. Mathematical/claim/attribution/archive/PDF/metadata blocking issues: **none**. The source's informal interpretation, finite-check limitations, unattested historical digest, bounded priority coverage and absence of independent human refereeing remain disclosed limits, not hidden conclusions.

This is the first new full-package adversary only. The user's required second **new** reviewer must still evaluate the final unchanged candidate (or a freshly bound candidate after any future correction). External publication, tracker entry, PR readiness and exact-head merging require their separate root-owned gates and readback. This report does not replace those operations or the remaining batch process.

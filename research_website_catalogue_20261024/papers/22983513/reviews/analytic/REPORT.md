# Analytic review119 — original version1.0.1

The full original nonattainment theorem and its stronger strict Yang proposition pass this analytic examination on the stated class of all nonempty bounded open subsets of Euclidean space. No substantive mathematical defect was found. This is independent AI-assisted mathematical scrutiny, not human peer review or a proof-assistant certification. Priority and current worldwide openness are not certified. The accompanying computation supports algebra and explicit spectra; the general theorem rests on the analytic argument.

The reviewed object is Zenodo record22983513, DOI10.5281/zenodo.22983513, title *Nonattainment in the Harrell–Stubbe Dirichlet gap inequality*, by Alec Kriebel, version1.0.1, printed and declared23September2026. The API creation26September2026 and update10October2026 are separate dates. The actual standalone three-page PDF, its byte-identical ZIP member, and the entire173-line controlling TeX were read; all three newly rendered page images were inspected. Exact binding fields are in SOURCE_BINDINGS.json and NATIVE_CUSTODY_BINDINGS.json. This review does not substitute a newer concept version, local manuscript or archived opinion for that release.

## Complete mathematical scope

For every integer n≥1, every nonempty bounded open Ω⊂Rⁿ, and every finite integer J≥1, let 0<E₁≤E₂≤⋯ be the eigenvalues with multiplicity of the Dirichlet operator defined by the closed form ∫Ω|∇u|² on H₀¹(Ω). Set A=J⁻¹∑ⱼ₌₁ᴶEⱼ, B=J⁻¹∑ⱼ₌₁ᴶEⱼ², M₁=(n+2)A/n and M₂²=(n+4)B/n. The theorem proves

    M₁²−M₂² > (Eⱼ₊₁−Eⱼ)²/4, with j=J.

Its supporting Proposition3 proves, for every real z>E₁,

    ∑_{Eⱼ<z}(z−Eⱼ)² < (4/n)∑_{Eⱼ<z}(z−Eⱼ)Eⱼ.

Lemma2 states that xαu has infinite spectral support for every real normalized eigenfunction u and every coordinate α. All these quantifiers survive the review. Boundary regularity, connectedness, a simple ground state, and a simple Jth eigenvalue are unnecessary. The strict threshold condition z>E₁ is essential: at z≤E₁ both sums are zero.

## Independent reconstruction and why it closes

INITIAL_RECONSTRUCTION.md was sealed before foreign scientific bodies, verification code/results, archive opinions or current peer opinions were opened. It develops five checks: form/derivative-domain reasoning, an alternative finite spectral algebra argument in distributions, the absolutely convergent remainder calculation, an independent midpoint version of the quadratic argument, and an exact interval model. The two obstruction arguments share the commutation mechanism; this packet does not advertise them as two wholly blind original discoveries.

Zero extension into an enclosing box gives the Poincaré lower bound and compact embedding without a geometric boundary hypothesis. Coordinate multiplication preserves H₀¹ by smooth compactly supported approximation and is bounded on H¹ because Ω is bounded. The distribution product rule then gives xαu∈Dom H and (H−E)xαu=−2∂αu. The same approximation justifies ⟨xαu,(H−E)xαu⟩=1.

If xαu had finite spectral support, its finite expansion could be acted on twice by the interior differential expression (−Δ−E). The product/commutation calculation gives zero. Orthogonality forces every coefficient outside eigenspace E to vanish, so (H−E)xαu=0, contradicting the preceding identity. Equivalently, the manuscript’s self-adjointness argument shows that assuming xαu∈Dom H² puts −2∂αu into Dom H, where it would be an E-eigenfunction, and forces its norm to vanish. The distributional operator-domain characterization is precisely what makes this valid on irregular domains. There is no illicit assertion Dom H=H²∩H₀¹ and no assumed boundary trace for ∂αu.

The two spectral moment identities follow because xαu∈Dom H. Their first series converges absolutely by Cauchy–Schwarz, their second is a squared L² norm, and only finitely many low states occur at a fixed threshold. Low–low terms cancel in symmetric pairs and threshold terms are zero. Every low–high remainder term is nonnegative. A zero remainder at z>E₁ would eliminate every ground-state coordinate coupling above z and give finite spectral support, the contradiction just established. Thus strictness holds at all real thresholds in the claimed range, not only between simple eigenvalues.

For the final gap calculation, Q(t)=(t−M₁)²−D, D=M₁²−M₂², has Q(Eⱼ)≤0 and Q(Eⱼ₊₁)<0 when Eⱼ₊₁>E₁. With m=(Eⱼ+Eⱼ₊₁)/2 and g=Eⱼ₊₁−Eⱼ,

    [Q(Eⱼ)+Q(Eⱼ₊₁)]/2 = (m−M₁)² + g²/4 − D < 0.

This checks the strict gap implication without a possible sign error from squaring. If Eⱼ₊₁=E₁, direct substitution gives D=4E₁²/n²>0 and g=0. A prefix ending inside a multiple eigenspace is valid because omitted terms at the threshold have weight zero.

## Boundary attacks and limits

Infinitely many disconnected components in a bounded set do not destroy compactness: zero extension into the box still applies. The proof selects any real normalized ground vector and does not assume positivity on all components. Slits, cusps and other nonsmooth boundaries do not change the form-domain argument. Dimension1 and every finite J are included.

Translations only alter coefficients within the same eigenspace. Dilation by s multiplies each energy by s⁻² and the strict gap slack by s⁻⁴. Hence this theorem provides no positive absolute deficit uniform over all scales. Leading Weyl terms cancel in D, so finite nonattainment is compatible with the classical leading asymptotic sharpness. The paper supplies neither the neighboring quantitative-growth answer nor a rate or uniform normalized deficit.

Neumann boundary conditions, periodic coordinates, unbounded domains and nonconstant added potentials are outside the original claim. The coordinate-domain or derivative-commutation steps can fail there; for example a Neumann interval has E₁=0 and does not satisfy the displayed Dirichlet gap estimate at J=1. These scope controls are not defects in the stated theorem.

## Actual primary interfaces

The proof is self-contained at the level of the classical form/spectral construction. The following source passages were nevertheless personally checked, rather than inherited from the native audits:

- Harrell–Stubbe, author preprint95-431, actual TeX Theorem1 and its domain assumptions, Theorem5, and Proposition6 with its proof. The latter has the squared second moment and interval/gap bound that the present paper uses. This is an authenticated author preprint; the publisher PDF request returned403, so this review does not claim a fresh full reading of the1997 journal PDF. Primary locator: https://web.ma.utexas.edu/mp_arc-bin/mpa?yn=95-431 and DOI https://doi.org/10.1090/S0002-9947-97-01846-1.
- The actual publisher OWR2009 report, printed414–416 text and printed415 pixels. The definition of Mₚ takes a pth root, while the saturation display has an unsquared M₂. The square correction is thus an explicit source normalization, supported independently by Proposition6, not a silent reinterpretation. The target theorem answers the corrected saturation question, leaving the adjacent quantitative-growth problem untouched. Primary locator: https://ems.press/journals/owr/articles/3389, DOI https://doi.org/10.4171/OWR/2009/06.
- Ashbaugh2002, actual published title/edition page and printed12–13 text and pixels. That historical text leaves Yang’s first strictness unresolved there while discussing other strict inequalities. The copy was an authenticated preexisting raw primary cache, not a new successful publisher download; its SHA256 is recorded in PRIMARY_READ_LEDGER.json. Actual IAS403 bodies and the Springer HTML response remain preserved, so an HTML response is not mislabeled as a retrieved PDF. DOI https://doi.org/10.1007/BF02829638.

Levitin–Parnovski and Harrell–Stubbe2010 are credited as classical context by the manuscript; their complete bodies were not newly read here, nor were the current Unsolved Math page or the old priority audits. No novelty conclusion or present-day openness assertion is inferred from the checked passages. The report verifies the mathematical answer to the stated corrected question, not global historical firstness.

## Computation and reproducibility

The complete329-line native verification program was personally read. Its only routine output is a chosen JSON path. An exact isolated copy was run normally and with Python optimization; both runs passed7,016 active exact checks over1,312 certified box/J cases, including600 zero gaps,12 repeated-ground cases and3 explicit algebra/sign controls. Both results were byte-identical to the deposited results. The spectrum enumeration has a strict omitted-mode lower bound, so these are genuine complete prefixes with multiplicities. Its synthetic finite matrices check cancellation identities and explicitly cannot realize all coordinate sum rules in finite dimension. No package builder/finalizer was run and no original program or output was changed.

The reviewer’s independent_interval_checks.py checks something the supplied finite-matrix tests do not: the actual infinite sine-coordinate remainder on (0,π). Analytic integration gives the nonzero opposite-parity coefficient −8jk/[π(j²−k²)²]. For seven real thresholds, including exact spectral levels and intermediate values, a512-mode rational partial sum plus a proved tail bound encloses the exact remainder. Rational alternating arctangent bounds using Machin’s identity enclose π, so the enclosure uses no floating-point acceptance tolerance. Displayed floats are convenience only. It also independently checks the closed-form interval deficit for J=1,…,128 and the excluded-threshold/finite-trace/sign/normalization controls. Details and exact rationals are in INDEPENDENT_CHECK_RESULTS.json and CHECK_DERIVATIONS.md. This remains a bounded model check, not a machine proof for arbitrary Ω.

## Custody, disclosure and remaining gap

The whole frozen SOURCE_READY and all actual raw record/latest/versions/files objects are retained literally, together with the array-shaped ALL_TRANSPORT_RECEIPTS.json. Record files remain an array in native ZIP,PDF,SHA256SUMS order; the files endpoint’s null/default and empty order objects remain unchanged. All30 native ZIP payloads were CRC/size/SHA256 checked against the extracted bytes in original order. Old audit files were hashed mechanically, never read or used as scientific evidence. No source file, peer packet, site/core artifact, tracker, Git reference or external communication was changed by this review.

Paper, audits and original prose have the actual native CC BY4.0 grant; software has the native MIT grant. Historical SOURCE_READY acquisition read-flags are preserved literally. Later reading is recorded in this lane’s ledgers instead of rewriting that history.

There is no remaining substantive analytic gap identified in the original theorem. Review limitations are finite independent checking, standard functional-analytic prerequisites rather than formalization, selected critical primary passages rather than an exhaustive literature/priority study, and a cached rather than freshly downloaded Ashbaugh primary. Follow-up remains null. The scientific verdict is private and gated pending root119’s independent initial seal; it authorizes no editorial or public action.

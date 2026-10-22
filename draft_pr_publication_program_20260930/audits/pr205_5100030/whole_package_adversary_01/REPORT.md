# Fresh whole-publication-package adversarial review 01: PR205 / 5100030 / k601

Verdict: **CLEAN for the exact frozen package and the explicitly proper-elliptic, ordinary complete-line-distance theorem. No required repair identified.** This is the first new whole-package event. It contributes one event only, makes no publication or live-operation decision, and does not replace the required next fresh reviewer.

The independent scope was frozen at 2026-10-16T16:48:58.412531+00:00 in FROZEN_SCOPE.json before reading the theorem, proof or any earlier favorable report. The parent supplied only the target, expected artifact identities, source locations and attack topics. I first authenticated the package, read the present manuscript and primary mathematical sources, and rederived the Fourier/geometric chain. Earlier mathematical/priority reports were read subsequently as package contents and were never treated as authority for correctness or as earlier whole-package events. All writes were confined to this review's folder. No Git command, ref/index change, editor operation, external human communication, publication/service mutation, installation or dependency copy occurred.

## Exact object and custody

The reviewed parent is publication_package_v2. The binding is:

| Object | Bytes | SHA-256 |
|---|---:|---|
| ROOT_WHOLE_PACKAGE_PACKET_02.json | 2448 | c7b2d4c2b8fe93ea62775859dc156e9332f194be9aa56a0f49eb28adbd987fc3 |
| PACKAGE_SEAL.json | 8512 | 232f7b02c00946b027a3141eb3d85062a77721d2f8a5ae0b2857b76b591642d3 |
| odd_period_focal_pedal.pdf | 77757 | 768f494b52e7b0354c11fa5384154ba0f59506200dd66e7573ccad8fd90dcc0a |
| odd_period_focal_pedal.tex | 14447 | 07e3d8f8549365b2005584c5fdadc37a55ff6b865c989ace2914c7b4d941ec9c |
| verification-package.zip | 101469 | 0eb74232d1be56c2e306adc5c55b4e614a23484a7ea1fba2398b035317ce911b |

All 46 files in the seal match their exact size/SHA-256 declarations. There are no missing or unlisted files in that package directory. All 44 ZIP members match the same named outer files byte for byte, pass the ZIP CRC test, have unique relative paths, and contain no traversal, backslash path, absolute path, encryption or symlink entry. The ZIP is about 101 KB compressed and only contains the declared small text/source materials. Its inner PUBLIC_MATERIALS_MANIFEST authenticates its exact complete inventory and the external uploaded PDF. I also extracted it safely into this review's own extracted_packet/ directory, rechecked every inner pin and ran its verifier there.

All 17 archived original files, totaling 41845 bytes, match the original custody record's byte count, SHA-256 and native blob identity. The latter was recomputed as SHA1 of the native blob header plus bytes without invoking Git. The archive genuinely preserves the originals rather than silently repairing them. Original PR metadata and the exact queue-row receipt identify the same k601 statement, original HEAD e8d7e925d19698edcb75822e40ca5ac820eb4388 and the original 1/5 author-turn record. Those records are historical custody evidence, not a present merge/completion/status assertion.

PROTECTED_BEFORE.json, PROTECTED_AFTER.json, ARCHIVE_CUSTODY_CHECK.json and REVIEW_MANIFEST.json contain machine-checkable identities and preservation results. Reading-copy pins are separate. Their mtime snapshot was expressly taken after initial reading, so this review does not invent an earlier exact timestamp certificate. The package's before/after byte identities are exact.

## Original target and the domain challenge

I read the literal k601 row in the exact [arXiv v11 Table 7, p.9](https://arxiv.org/pdf/2004.12497v11) and [published Table 7 and Section 3.7, p.349](https://armj.math.stonybrook.edu/pdf-Springer-final/021-0174.pdf), including the surrounding definitions. Relevant table pages were rendered and visually inspected. Both rows give the product of the two focal pedal sums for odd N. The published definition takes ordinary lengths from the foci to pedal vertices on the original trajectory. It is neither an area invariant nor an antipedal or outer-polygon invariant. The standard pedal construction uses perpendicular projection to the side line. The manuscript explicitly resolves the source's informal word “sides” as complete supporting lines. It does not claim the source literally printed that qualifier.

Both source preliminaries use real major/minor semiaxes for the caustic, within the confocal-ellipse setup. The current statement fixes a>b>0 and 0<lambda<b^2, so alpha>beta>0 and the inner ellipse is proper and strictly nested. This is a faithful qualified resolution of that source contract, not a theorem asserting arbitrary caustic types. The original PR statement already used the same qualified geometry. The historical table does not literally state least period; an odd indexing length reduces to an odd primitive period with odd repetition multiplicity, and the elementary r^2 law restores exactly the listed quantity. No relevant odd repetition is lost.

I separately challenged whether hyperbolic caustics might hide a missing odd-period family. For a genuine hyperbola, b^2<lambda<a^2, a tangent line lX+nY=d satisfies

    d^2=(a^2-lambda)l^2+(b^2-lambda)n^2.

Necessarily l is nonzero, and its intercept at Y=0 obeys

    (d/l)^2 <= a^2-lambda < a^2-b^2=c^2.

Thus the physical chord crosses the major axis strictly inside the focal segment and connects vertices with opposite signs of Y. No endpoint can have Y=0, since an axis endpoint is at X=+/-a. Each bounce flips half-plane; a closed trajectory therefore has even period. Genuine hyperbolic caustics cannot supply an omitted odd-period counterexample. This deduction is additional domain reassurance; the current paper does not need a hyperbolic extension to prove its explicitly proper-ellipse statement.

The collapsed focal-segment, grazing and singular endpoints remain explicitly outside the assertion. I have not supplied a classification theorem for all degenerate trajectories and do not suggest the paper has proved one. The literal historical real-ellipse contract and the present explicit qualifications make that omission honest. The circle is discussed separately and correctly. No present-day openness can be inferred from the 2020/2021 question mark, and the package does not do so.

## Universal analytic proof, checked without finite extrapolation

The parameter convention is consistent: m=k^2=c^2/alpha^2, while Stachel and DLMF use a modulus in their relevant notation. Hence 0<m<1, K(m)>0 and k'=beta/alpha>0. The current Fourier expansions agree with the official [DLMF 22.11.2–3](https://dlmf.nist.gov/22.11), after replacing the modulus by sqrt(m). For real t, each trigonometric term has modulus at most one. The coefficients admit geometric majorants proportional to q^n and q^(n+1/2), where 0<q<1. The Weierstrass test therefore establishes the stated absolute uniform convergence, so interchange with the finite orbit sum is legitimate for every fixed permitted m. No unproved uniformity as m tends to one is used.

For the dn frequency n*pi/K, shifting by 4Kj/N multiplies its complex exponential by exp(2*pi*i*2nj/N). The grid filter retains N dividing 2n. Oddness makes this equivalent to N dividing n. For the cn frequency (2n+1)*pi/(2K), the multiplier is exp(2*pi*i*(2n+1)j/N); the surviving positive odd frequencies are exactly N(2s+1). This checks both the parity condition and all constants in the filtered sums. In particular, it does not incorrectly use the 2K grid for cn.

With Q=q^N, the classical nome inversion in [DLMF 22.2.1–2](https://dlmf.nist.gov/22.2) supplies the unique real transformed parameter M in (0,1) and K_M. Taking gamma=K/(N K_M), coefficient and frequency comparison gives the distinct amplitudes

    D(t)=gamma^(-1) dn(t/gamma | M),
    H(t)=sqrt(M)/(sqrt(m)*gamma) cn(t/gamma | M).

Thus the elementary square relation gives D^2-mH^2=(1-M)/gamma^2 for every real phase and every odd N>=3. Neither an assumed equal amplitude nor a separately chosen cn argument is hidden in the argument. At t=0 the filtered cn series has positive coefficients and positive prefactor, so its sum is positive; eta=1/H(0) is well defined. Evaluation at zero yields the stated dn normalization and M=m gamma^2/eta^2. The 2K and 4K dn grids agree because multiplication by two permutes residues modulo odd N and dn has real period 2K.

The proof establishes all odd integers algebraically. Finite samples only diagnose implementations. There is no circular use of the desired billiard invariant in defining M, gamma or the trace constant.

## Geometric bridge, physical law and completeness

The exact [Stachel Theorem 4.3 and Eq.4.9](https://doi.org/10.1007/s40879-021-00524-2), printed p.1614, were read and visually inspected. They supply the stated parametrization after the explicit modulus conversion. Their winding/step conventions agree with the paper. The real sign error for dn(u+2K) on p.1613 is real; the manuscript identifies it and uses the correct positive period from [DLMF 22.4](https://dlmf.nist.gov/22.4). It does not inherit the typo.

For an existing pair there is a unique h in (0,K) satisfying cn(h)=beta/b. Confocality then gives dn(h)=a beta/(b alpha), hence a=alpha dn(h)/cn(h), b=beta/cn(h). Every real tangent of C is represented by

    L_v: -sn(v) X/alpha + cn(v) Y/beta=1.

The two incident tangent phases at P(u)=(-a sn(u),b cn(u)) are u-h and u+h. The identity used to verify this incidence follows by solving the difference-addition system; its determinant 1-m sn(x)^2 sn(y)^2 is at least 1-m>0. Substitution at both endpoints is valid. The contact point is (-alpha sn(v), beta cn(v)); its strict interior nesting makes it a genuine chord tangent, not a nonexistent or external contact.

I also checked the physical law independently, instead of simply treating every conic tangent polygon as a physical billiard. The endpoint difference for the chord from P(v-h) to P(v+h) is a negative positive-magnitude multiple of (cn(v),k' sn(v)). Its directed unit velocity is therefore

    w(v)=(-cn(v),-k' sn(v))/dn(v).

At a vertex P(u), the addition formulas make w(u-h)+w(u+h) a positive multiple of the outer tangent (-a cn(u),-b sn(u)); both velocities have unit length. Their difference is normal to that sum, so their tangent components agree and their normal components are opposite. Convexity chooses the incoming/outgoing signs, giving precisely specular reflection. Positivity of cn(h), dn(u) and the addition denominators excludes the grazing/reversal branch.

At any exterior vertex the two caustic tangents are exactly those phases, so choosing one orientation advances all vertices by 2h; reversal uses -2h. The boundary parametrization is injective modulo 4K, and h is in (0,K). Primitive closure is consequently 2h=4K tau/N with gcd(tau,N)=1 and 0<tau<N/2. This supplies completeness for all admissible coprime star windings rather than only convex tau=1. A given fixed pair does not admit every arbitrary tau: the word admissible is necessary and is retained.

The normal norm is dn(v)/beta. The focus-line evaluations have the signs asserted because 1+/-k sn(v)>=1-k>0 and dn(v)>=k'>0. Thus the displayed q factors are ordinary Euclidean distances, with no use of a signed substitute or segment clipping. Independently, the unit-normal support formula gives (h-c n_x)(h+c n_x)=beta^2 and confirms the same positivity. This local product alone would not prove constancy of the product of sums; the manuscript uses the trace lemma for the missing global step.

Coprimality permutes the entire 4K/N side grid. The quarter-period identities give exactly A=D(v+K)/k' and B=-H(v+K)/k'; beta^2/k'^2=alpha^2 provides the crucial common scale. Therefore I=alpha^2(1-M)/gamma^2. At v=0 the odd sn/dn terms pair under negation, giving the claimed beta^2 times the squared reciprocal-dn sum. Reversal permutes the same complete side lines. Traversing each line r times multiplies each sum by r, and I by r^2, for every positive integer r. An even repetition of an odd primitive orbit is not a counterexample to the restriction on even primitive periods.

## Alternative proof chains preserved in the supplement

The supplement also contains more than the present Fourier argument. I checked their mathematical mechanisms as content of the whole packet, after preserving early independence.

The original addition/zeta telescope divides only by m sn(4Kr/N), for 1<=r<N. A real sn zero there would require N to divide 2r, impossible for odd N. Summing the zeta addition law gives the constant sn pair correlation because the shifted arguments permute the full grid and argument-form zeta has real period 2K. The cn/dn difference system gives dn(x)dn(y)=dn(a)-m cn(a)sn(x)sn(y) and cn(x)cn(y)=cn(a)-dn(a)sn(x)sn(y). Subtracting m times the second from the first is exactly the displayed bilinear formula; grouping all ordered index pairs counts each off-diagonal once and the N diagonal terms give N(1-m). No factor of two or zero denominator is missing. DLMF's epsilon law applies also to zeta after subtracting its linear term. The supplementary prior report correctly warns that a principal arcsin(sn) is not a globally valid replacement for the continuous argument-form zeta. This archived proof is a valid classical alternative, while its old executable controls retain the separately disclosed software defects.

For the complex proof set f=(1+k sn)/dn on the lattice 4K Z+4iK' Z. The square and shift identities give f(-z)=1/f(z), f(z+2K)=1/f(z), f(z+2iK')=-f(z). The common sn/dn poles are removable in f, with nonzero limiting values. At p=K+iK', dn has derivative i k', the numerator is two and the residue is -2i/k'; the opposite sign sn=-1/k points are exactly simple zeros by f=dn/(1-k sn). This exhausts the divisor. Modulo the stated lattice the only poles are p and p+2iK', and the only zeros are their 2K translates. The pole-set difference and imaginary sign exclude any additional translation period, even for a special modulus.

A(z)=sum f(z+jh) and B(z)=A(-z), with h=4K tau/N, have unique simple poles in each grid class. Their pole sets cannot meet for odd N, since intersection would require 2(j+l)tau=N modulo 2N. At z0=-p, f(z0+v)=-f(z0-v) and f(z0)=0. The odd finite grid therefore has sum zero. At every A pole, the analytic B factor is precisely that reindexed zero sum, and conversely. A simple pole times an analytic zero has no principal part; unchecked double poles are not being removed merely by residue cancellation. After all extensions AB is holomorphic on a compact torus, hence constant. It is positive on the real axis, and evaluation at zero gives the same reciprocal-dn squared constant. Exact simplicity of the cancelling zeros follows only afterward from that nonzero constant, so that inference is noncircular. The preserved adversarial report's all-parameter even-pole collision argument and explicit N4 difference agree with this divisor calculation. Its independent sign convention swaps the two focus labels but leaves the target product unchanged.

These supplementary routes make no new-method or global-priority claim. Their mathematical conclusions agree with the current proof; their independent-discovery language is confined to the explicitly declared local exposure histories rather than a claim of historical scientific independence.

## Exact N=4 boundary and circle

I rechecked the manuscript's exact pair with squared outer axes 3/2 and 3/4 and caustic axes 1 and 1/2. Both axis differences equal lambda=1/2. The diamond side normal (written with right-hand side one) has squared norm 2 and caustic support value one. Opposite normals cancel their focal translations, giving each four-side sum 2 sqrt(2) and I=8. Its reflection follows at each axis vertex by symmetry.

The rectangle (+/-1,+/-1/2) lies on the same outer ellipse. Its four sides are exactly the caustic's axis support tangents. At (1,1/2) the outer gradient has equal components 2/3, and the sign-reflected vertices behave likewise, proving the right-angle specular reflections. Distances from either focus to the two vertical lines sum to two, and those to the horizontal lines sum to one. Hence I=9. Both cycles have four distinct vertices and no shorter return. This is a valid exact same-pair, physical primitive counterexample, independent of numerical sweep evidence.

When c=0, both foci are the center and every tangent side has distance beta. The result N^2 beta^2 follows directly; no singular eta, zero-parameter Fourier division or degenerate torus argument is needed. No unsupported value at m=1 or at a collapsed caustic is asserted.

## Direct antecedents, bibliography and disclosure

The current manuscript honestly states that its entire special-function lemma follows from earlier mathematics. I read the exact primary [Khare–Sukhatme 0312074v1](https://arxiv.org/abs/math-ph/0312074v1) pages 4,8,10,12–13. Their normalizations alpha and alpha_1 are respectively this paper's gamma and eta. Their Eq.53 supplies M=m gamma^2/eta^2; Eqs.68–70 give the common-argument odd-order identities after the Section 3.1 identification. The dn 2K grid is permutable to the current 4K grid; the cn grid remains 4K. This is a direct antecedent, not merely related background. The paper's wording accurately credits it.

I read [0201004v2](https://arxiv.org/abs/math-ph/0201004v2), Table 1 Eq.29: it states the required all-odd pair-correlation constancies. Its discussion distinguishes low-order algebra from higher-order numerical confirmation. The manuscript carefully says those correlations were “stated,” while crediting a later general framework; it does not promote the older numerical catalog into a supplied universal proof. The [0207019v2](https://arxiv.org/abs/math-ph/0207019v2) general method and explicit dn/cn correlations in Sections 1–2 and Appendix A support that later credit. The apparent sn coefficient typo in its Eq.113 is not used by the current Fourier proof. The source caution in the supplement is appropriate.

I independently read the complete published Bialy–Tabachnikov Lemma 4.2 across pp.1349–1350 from a read-only primary copy, authenticated as 402190 bytes/SHA256 10fc931a9c0e8c656891872695157a88f21ec91860fd82b2308620518df53b0b. It literally supplies the focal support distances and pointwise beta^2 product. The next theorem concerns other products, so the current attribution does not falsely credit it with the full sum-product conclusion. A web fetch of the NSF PDF returned 502; a lawful existing identical published reading copy and its rendered pages supplied the needed direct verification. A current arXiv preprint independently confirms the same local formula.

The exact arXiv version dates in the bibliography agree with primary version histories: RGK v11 29 October 2020; 0201004v2 4 January 2002; 0207019v2 24 March 2003; 0312074v1 31 December 2003. DLMF's current official version is 1.2.8, released 15 September 2026, as cited. Published titles, author lists, DOI mappings and volume/page conventions are consistent with the inspected primary records. Online dates and later issue years are not silently equated.

I inspected the priority ledgers as bounded reports rather than rerunning an exhaustive literature search. Their positive analytic implication is now directly verified above. Their geometric comparisons explicitly distinguish Euclidean metric quantities, contact lengths, focus inversion, pedal perimeters and trace methods. Partial AST/CZ bridges are identified as incomplete and are not necessary lemmas in the manuscript. A direct attempted read of one adjacent Zenodo metadata API record was unavailable in this review; I do not independently certify that record's live metadata or discovery clock. Nothing in the present theorem or allowed editorial claim depends on that record or on a negative search.

No theorem, formula or method novelty, firstness, current openness, independent discovery or simultaneity is claimed in the paper, README or current deposit metadata. The bounded nonlocation of an earlier explicit geometric application is expressly nonexclusive. This review also makes no global absence claim. AI research, drafting, software and adversarial-review use are disclosed extensively; unrefereed status and the difference from human peer review/formal certification are clear. New-text CC BY 4.0 language leaves third-party works' rights intact. Public materials contain no third-party full papers, full-page source images or dependencies.

## Current portable code and actual checks

The public current verifier is 14419 bytes/SHA256 7fbee76b89716091b84e2ec4f99f252d7cd1b0a47f517e4f605c806f762398bd. It imports only the standard library and mpmath, enforces mpmath 1.3.0 and has zero bare asserts. Python 3.10 grammar parsing passes; the actual executions used Python 3.14.6. I used the parent-approved existing runtime read-only through a sys.path injector, with -E -S -B -P and -O only in optimized subprocesses. No installation, dependency copy or bytecode writing was required.

The physical part uses affine-circle initial tangency, forward line/ellipse intersection and Euclidean gradient reflection. It does not generate vertices from the Jacobi closing formula or project points back onto a conic. Its angle-lift shooting selects a closure parameter; separate boundary, closure, winding, tangency, reconstructed reflection, focal-product and short-return checks then validate the orbit. The target distances come from the original endpoint chords by cross products. Repetitions retain all physical checks while deliberately skipping only the primitive-length test. Circle and exact even controls are separate. I found no implementation shortcut that simply returns the analytic expected value as its physical measurement.

The public README's counts match the actual loops: eight proper configurations, six primitive traversals and two repeated traversals each, four circular traversals and two N4 traversals, totaling 70. Its 25 negative controls are required to reject; silent acceptance makes main fail. The explicit finite guards precede reductions, comparisons and JSON formatting. NaN cannot disappear inside max as in the historical candidate. Bounds, tolerance and noninterval limitations are stated accurately. Max(1,abs(expected)) is an error scaling choice, not an interval or universal error guarantee; the text does not claim one.

I actually reran the current normal and optimized programs. Both exited zero and reproduced the published JSON result files exactly, including max scaled comparison error 1.61539717061843029100893e-84, 70 traversals and 25 rejections. Normal and optimized data are identical except for the optimized flag. The optimized safely extracted ZIP run also reproduces exactly. This independently checks the archive/code/README/result-file coupling rather than trusting a receipt.

Fresh independent_checks.py adds a different endpoint-based diagnostic construction with direct cross-product distances, explicit reflected directions, tangent incidence, strict earlier-return exclusion, trace amplitudes and both constant formulas. It uses four configurations (m,N,tau)=(1e-8,15,7),(.37,11,5),(.83,9,2),(1-1e-12,9,4), two phases, scales 1e-10 and 1e10 and both directions: 32 physical traversals. The cn trace is compared relatively even when M is about 1.38778e-137, so an absolute tolerance cannot mask a zero or wrong tiny trace. Six exact rational groups independently check the manuscript's N4 conic and reflection algebra. The 2248 finite scalar checks at 180 working digits have worst scaled residual 3.663565235765046427190731e-118 against 1e-90.

Its 18 additional hostile controls exercise NaN/infinities/complex/bool scalars, nonfinite RHS/tolerance/norm, bad period/phase/direction, dependency-injected NaN elliptic functions and a deliberately corrupted finite normalized identity. Both normal and optimized runs reject all of them and agree except for the optimization flag. These are finite noninterval diagnostics, not proof by sampling or independence-of-discovery claims.

## Historical archive and presentation

The two old scripts each contain six asserts. I inspected their actual source and independently demonstrated the relevant Python behaviors: a false assert fails normally and is removed by optimization, while max(finite,NaN) retains the finite value. I did not count their historical favorable PASS reports as current validation. The package root README and materials/ORIGINAL_ARCHIVE_NOTICE.md explicitly label all 17 files as historical evidence, identify both vulnerabilities, preserve their exact bytes and point to the current verification/verify.py from the package root. The old reports' local environments and status words are not represented as current readiness. The current portable requirements correctly do not promise to execute the old sympy-based archive.

All current JSON files parse. The public manifest, outer seal, upload declarations, code hash, result summary and deposit file list agree. Source, abstract, current README and metadata state the same theorem and exclusions. I rendered all five PDF pages and visually inspected every page. Equations, theorem, proof, footnote and bibliography are legible, with no clipping, overlaps, missing glyphs or visibly broken layout. The PDF is five unencrypted letter pages with no forms or JavaScript, and its mathematical content matches the TeX. Primary source page views are confined to private_primary_views/ in this review and must not be published as supplement contents.

## Findings and exact remaining limits

There are **zero required mathematical, source, attribution, code, packaging or presentation repairs** for this exact packet. FINDINGS.json records the checked concern families and their evidence. The strongest verified conclusion is the universal proper-confocal odd-primitive complete-line focal-distance sum-product invariant, its explicit classical normalization, all admitted coprime stars/reversal/repetitions, and the exact physical N4 parity counterexample. The manuscript presents that conclusion with appropriate attribution and qualifications.

One optional explanatory improvement is to add a short domain sentence about genuine hyperbolic caustics forcing even periods, as proved above, if the coordinator wants to address that possible reader question within the paper itself. It is not needed for the currently explicit proper-ellipse theorem or source fit and is not a repair requirement. Any such change would create new bytes requiring a new seal and review binding.

The precise remaining work belongs to the parent workflow: another NEW fresh whole-package reviewer; any coordinator-requested change and resealing; then any separately authorized actual publication/tracker/merge actions with fresh live checks. This review grants none of those authorities and certifies no DOI, public deposit, merge, tracker update or next-intake cursor advance. Global novelty/firstness, exhaustive contemporary literature absence, proof-assistant certification and interval error certification remain unclaimed. Completion estimate: 100% of this bounded fresh whole-package review; no percentage of future live operations is inferred.

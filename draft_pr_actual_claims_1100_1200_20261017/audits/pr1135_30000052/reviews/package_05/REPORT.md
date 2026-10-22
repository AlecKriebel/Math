# Independent whole-package adversarial review 05

**Verdict: PASS. Actionable findings: none.** The complete negative answer and stated supplementary/control claims survive fresh reconstruction, exact independent computation, primary-source comparison, archive reproduction, source-custody review, and four-page PDF inspection. This verdict does not certify worldwide novelty, first priority, formal proof certification, human peer review or publication. It is a new independent internal AI review of the exact candidate described below; neither prior acceptance nor any clean whole-package review was used as a premise.

## Frozen candidate, independence and boundaries

Work began at2026-10-17T21:44:45Z. `sources/private/` and `tmp/` ignore rules were written before retrieval. Every authored artifact is confined to `reviews/package_05/`. I did not read package_01/02/03/04 reports. I subsequently read the candidate's dated revision receipts as shipped historical evidence, without treating their prior review decisions as authority.

The frozen source head is `e809a9c40f4ccdaced6f45f10b1dc8b7725a2119`. `START_PINS.json` freezes the six release files, PACKAGE_RECEIPT, and124 live files corresponding to all non-generated source-archive members. The two generated members are PROVENANCE and SOURCE_MANIFEST. The six identities supplied in the task all match:

| Release file | Bytes | SHA256 |
|---|---:|---|
| main.tex |11218|4e481ec84b1be42a9885df393e0fce065f489eea6f0f2e98ed0f84298f9e3d85|
| output/pdf/random-lattice-counterexample.pdf |63159|a731f3d7db3ffb3644bf6ab3898159e00508a922ce2ec8dd4e6283cf994e6810|
| output/random-lattice-counterexample-source-and-verification.zip |282131|1a344c7240f72e386f05cfb4024805469a5ff0bade7efc721b1ac6badeeb36b2|
| output/zenodo-upload-kit.zip |332943|a93a9c469ecbb0b180837bb79db53070996f44aa0276416f37eff7a0f9678415|
| zenodo-metadata.json |4157|bd80c082db707d9ee10b31b917ef76699bdf2c821bfa79ecf040a21bf4d441cb|
| zenodo-deposit.json |4488|e2e465db480c35f1c7bfb043e2803fae415f6baf6ee338ecd238dbb6cfa779d6|

I read complete main.tex; all ten historical input documents including their complete proof/audit; root mathematical, Fourier and priority notes; all three new mathematical and three priority reports; all seven pinned verification programs; portable runner and builder; README, license, provenance, metadata and manifests. Current review input pins and authoritative review manifests were checked independently, including the six classification inputs outside the portable programs' inputs. Fresh exact-head GitHub downloads authenticate all ten unchanged historical files. The old7673-byte original proof and the distributed7682-byte source-PR proof remain explicitly distinct. The historical input edition's exclusions and10October literature scope are superseded by the current release descriptions, not silently rewritten.

No live builder or TeX compiler was run, and no live candidate/source/review file was edited. All rebuilding and mutations occurred inside the ignored extracted mirror or its copies. No Git/index/refs/branch, PR/comment, deposit or tracker mutation, human outreach or other-shard communication occurred. Read-only `.git/HEAD` identifies main. Only the parent received internal progress messages. Out-of-package acceptance gates, logs and operational receipts are mutable coordination records, not members of the frozen archive or evidence that can substitute for its custody.

## Exact primary target

I freshly retrieved the official [OWR13/2004 PDF](https://ems.press/content/serial-article-files/45858), matching445532 bytes and SHA256 `2f02cd5834ed1a868d95a20be9d172ade3b35e76caf8c9ff8ab6a3adaf6f3d3e`. I read Novak's complete contribution printed696–699 and visually inspected697–698. He reports joint work with Hinrichs. The definition is normalized anchored discrepancy, and the question compares the expectation of its p-th power for even positive p. The lattice has indices0 through n−1 and product Lebesgue averaging of continuous generator and shift over the entire cube. The iid comparator is the corresponding product law on all point coordinates. There is no finite-grid, prime-n, selected-generator or no-collision condition. Thus n3,d1,p4 is admissible, and a single strict reversal settles this universal comparison negatively. The final existence/upper-bound question on699 is distinct.

## Independent universal mathematical reconstruction

### Pairwise laws, minimality, and the second moment

For each indexed j, conditional on Z, the shifted point T_j is uniform; its conditional law does not depend on Z, so T_j and Z are independent. For j≠k, the circle map Z↦{(k−j)Z} preserves uniform measure: partition into |k−j| intervals and add their equal rescaled preimage lengths. Hence T_k={T_j+(k−j)Z} is uniform conditional on T_j. Coordinate independence gives this pair law in every positive integer dimension.

For n1 the complete law is a single uniform point. For n2 the complete ordered pair is iid uniform, coordinate by coordinate; equivalently the torus inverse is Δ=T_0,Z={T_1−T_0}. Equality of whole laws implies equality of every defined measurable discrepancy functional, beyond the finitely tested exponents. Consequently n3 is the smallest possible counterexample point count.

For a box of volume v=product x_r, the normalized count has mean v and variance v(1−v)/n by pairwise independence. Integrating v and v² gives2^(−d) and3^(−d). Thus for all positive integers n,d,

    E disc_2(lattice)^2 = (2^(−d)−3^(−d))/n = E disc_2(iid)^2.

These are continuous measure arguments, not inferences from finite Fourier or grid tests. Collision parameters and tested endpoint equalities are null sets for fixed n,d; the original counting still retains every index and the weight1/n there. Closed parameter cubes give the same expectations. None is a conditioning event.

### Three points and strict gap

Set U=T_0,V=T_1. They are independent uniform variables and T_2={2V−U}. For0≤x≤1/2, on U,V∈[0,x), the raw third coordinate lies in(−x,2x). Its negative part wraps to at least1−x≥x and its nonnegative part does not wrap at one, apart from null boundaries. Third inclusion is therefore0≤2V−U<x. For fixed U∈[0,x], the allowed V interval is[U/2,(U+x)/2), contained in[0,x] with length x/2. Its area gives q(x)=x²/2 only on the lower half.

With P_k=P(N_x=k), the identities total probability1, E N_x=3x, E binom(N_x,2)=3x², and P_3=q uniquely yield

    (P_0,P_1,P_2,P_3)
    = (1−3x+3x²−q, 3x−6x²+3q, 3x²−3q, q).

Expanding the finite sum sum P_k(k/3−x)^4 gives

    F(x)=x^4−(2/3)x³+(2/27)x²+x/27+(4/9)(1−2x)q(x).

Substituting q=x²/2 gives x^4−(10/9)x³+(8/27)x²+x/27. Simultaneous reflection of Z and Δ modulo one preserves their product law and negates the centered count at reflected endpoint1−x, outside null endpoint events. Thus F(1−x)=F(x). Tonelli applies to this bounded nonnegative measurable integrand. Direct integration gives

    2 integral_0^(1/2) F(x) dx
    = 2(1/160−5/288+1/81+1/216)=19/1620.

An iid triple has q=x³. On the lower half the difference of fourth integrands is exactly(2/9)x²(1−2x)². Its reflected integral is1/540>0. Hence iid=19/1620−1/540=4/405 and the ratio is19/16. In particular pairwise independence cannot justify replacing q by x³. Reflection supplies the upper half; the lower-half expression is not extended to x=1.

For every positive n the centered Bernoulli expansion gives a=x(1−x), E Y²=a,E Y^4=a−3a². The only surviving fourth-power index patterns are the single index and two pairs, with multiplicities n and3n(n−1). Integration of a and a² gives1/6 and1/30, yielding the universal iid formula(3n−1)/(30n³). No high-n conclusion rests on testing finitely many values.

### Two empty-tail triangles and all n≥4

For n≥3, on0<Z<1/(n−1),0<Δ<1−(n−1)Z, the points lie without wrap between Δ and Δ+(n−1)Z. The two outer x intervals alone contribute[Δ^5+(1−Δ−(n−1)Z)^5]/5. This is integrated against the original density one, without dividing by triangle area. Integration in Δ and then Z gives1/[105(n−1)]. The unit-Jacobian reflection(Z,Δ)↦(1−Z,1−Δ) gives the descending no-wrap triangle with the same contribution. For n≥3 their open generator intervals are disjoint; at n3 only their closures meet. All omitted discrepancy contributions are nonnegative. The expectation is at least2/[105(n−1)].

At n4 this is2/315, greater than iid11/1920 by5/8064. For every integer n≥4, clearing positive denominators reduces strictness to4n³−21n²+28n−7>0. Substitution n=4+t gives25+52t+27t²+4t³>0 for t≥0. This establishes the infinite claim. At n3 the bound1/105 is below iid4/405, so the independent exact three-point proof remains necessary there. A fixed zero generator and its large discrepancy cannot be substituted for the full two-parameter average.

### Supplementary full n4 and independent exact control

Before reading any supplied control code, I wrote `independent_control.py` from the sorted-point defining integral. It imports no supplied or external verification module. For a deterministic sorted configuration s_1≤…≤s_n with s_0=0,s_(n+1)=1 and even p,

    disc_p^p = sum_(k=0)^n [(s_(k+1)−k/n)^(p+1)−(s_k−k/n)^(p+1)]/(p+1).

The generator is partitioned at every k/m with1≤m≤n−1. Inside a generator interval all jZ floors are constant. The shift wrap cuts1−{jZ}, together with0,1, are affine and have fixed order: any crossing would require an integer multiple mZ with m≤n−1 to be integral, already a generator cut. Between consecutive shift cuts, all modular point floors and point order are constant. These cells cover the full square up to finitely many null line segments.

On such a cell the displayed x-integrated expression has total degree at most p+1 in Z,Δ. Six interior rational interpolation nodes integrate degree5 exactly in Δ for p4. Substituting affine cell endpoints and multiplying by affine interval length makes the result a polynomial of degree at most6 in Z; seven interior rational interpolation nodes integrate it exactly. For p2 the corresponding counts are four and five nodes. The Lagrange weights are themselves generated and checked against all basis monomial integrals; nothing is fitted using the advertised fraction. Exact Fraction arithmetic avoids numerical cancellation or rounding. This is algebraically exact iterated quadrature with a proved complete cut set and degree bound, not sampling evidence.

The direct defining integrations give:

| n | p2 lattice | p4 lattice |
|---:|---:|---:|
|1|1/6|1/15|
|2|1/12|1/48|
|3|1/18|19/1620|
|4|1/24|139/17280|

The independent iid computation expands the complete binomial count distribution and integrates every rational monomial; it verifies both formulas for n1–17. Additional checks enumerate lattice additive energy and actual iid phase energy, validate the simplex coefficient and tail comparison polynomial, and retain indexed collision configurations. The supplementary n4 value139/17280 is corroborated from the defining integral and agrees with the supplied exact-cell derivation. It is unnecessary for either analytic counterexample.

The final sealed code produces78 named checks and six rejected false alternatives in each successful ordinary/optimized run, with byte-identical1061-byte JSON output, SHA256 `4425992b78f9f3b0bfeb8dd663de9ac4896800d0083772458a5c0aeec83f10ba`. Internal quadrature basis checks are additional require calls and are not included in the named78. Six adverse alternatives cover iid triple substitution, equating full n4 with the tail bound, the wrong iid phase energy, inferring n3 reversal from its insufficient tail bound, false n2 reversal and a lost triangle orientation. Both final forced runs actually change the expected n3 lattice identity to4/405; both exit1 with `19/1620 != 4/405`. This is an arithmetic rejection by the same equality check, not a fabricated successful message or an unconditional failure flag. `CONTROL_REPLAY.json` pins that final code and records exactly the four executed runs. Python3.14.6 standard library was used; no SymPy.

## Fourier bridge and priority: independently checked, properly limited

Freshly retrieved Su2000 and Anderson et al.2007 PDFs match the package's exact primary-source hashes. I read Su's cumulative coefficient proof and Kronecker application statements, and Anderson's exact kernel definition and complete relevant lemma proof. Su's added centering constant affects only frequency zero; his supremum theorem is not substituted for an L4 bound. Direct integration of each anchored indicator gives, with e(t)=exp(2πit),

    integral_0^1 F(x)e(−x) dx = sum_j e(−t_j)/(2πin).

This remains true for indexed collisions and t_j=0. Hölder on the unit interval bounds the magnitude of this coefficient by ||F||_4. The common shift in sum e(jZ+Δ) is a unit phase. Expanding and integrating the remaining kernel's fourth power retains exactly a+b=c+d, for0≤a,b,c,d<n. The triangular pair-sum multiplicities therefore give(2n³+n)/3. Thus the actual full-law anchored expectation is at least(2n²+1)/(48π^4 n³).

The upper bound π<22/7 follows from the positive integral of x^4(1−x)^4/(1+x²), which polynomial division evaluates as22/7−π. After clearing positive denominators against iid, n=234+t gives coefficients5975502/2401,33687216/2401,60, all positive. This proves reversal for all n≥234 independently of the exact small-n result. The finite controls agree. For actual iid uniform complex phases, surviving index multisets give2n²−n, hence15 at n3, whereas the lattice energy is19. I independently enumerate both; the broad129-check program now uses the correct15 baseline. The focused rotation program also separately checks15; its additional explicitly rejected n² value is a false alternative, not its claimed iid comparator.

This is a valid model-specific new audit application of classical ingredients. The inspected old primary statements do not already state the averaged anchored random-lattice fourth-moment lower bound or Novak comparison. I found no evidence in them of an older recorded full target answer. That does not establish the first recognition of this consequence.

I freshly read the relevant analytic portion of [Ferudun's14October2026 preprint](https://eulersolve.org/papers/owr-723-005/paper.pdf?v=edb268431856), matching182528 bytes and SHA256 `edb268431856eef5d6eb00e730d1a27a7e91a15d76186b506168f259dbbb174c`. It explicitly contains the same n3/n4 values and broader dimension/exponent results. Its circular-gap calculation and no-wrap progression argument are analytic full-target overlapping answers. I independently checked that sufficient analytic portion; I did not recertify all of its computer-assisted cases or its entire15-page body. Its DOI/API creation and publication dating agree with14October and version1.0.

The PR API has creation/update2026-10-10T11:34:20Z, one reviewed commit dated11:33:05Z, current public repository status and exactly the supplied head. Ten exact-head files match unchanged. These are dated records, not certified historical public visibility, first discovery/publication or evidence about awareness/dependence. The current paper, metadata, README and provenance give exact overlap credit, separate the10/14/17October dates, disclaim first priority and do not claim novelty relative to all present literature. That framing is consistent with the evidence.

The2010 author book draft repeats the exact comparison as OpenProblem41; its old open label is historical context only. This new review made twelve actual supplementary searches, precisely listed in `QUERY_LEDGER.json`, without treating noisy or absent hits as novelty evidence. All three supplied priority reports were read in full and their inaccessible full/final bodies and incomplete citation coverage remain explicit limits. I did not freshly retrieve or exclude every primary body in those reports. No exhaustive earlier-answer exclusion is certified.

## Package, manifest, reproduction and disclosure checks

`PACKAGE_INVENTORY.json` records126 unique safe source members and five upload-kit members. All CRCs pass; names are relative, traversal-free and nonsymlink; timestamps are deterministic. SOURCE_MANIFEST has125 entries covering every other source member. Every member's bytes/hash agrees with that manifest and PACKAGE_RECEIPT. All124 non-generated source members agree with their live frozen counterparts. All six review manifests cover73 authored entries with matching bytes/hashes. The historical ten-input manifest's nine nonself entries and all ten body/head identities pass. All six classification input pins and every current input pin in the other five review families also pass.

I checked the seven control specs, code/result/auxiliary pins and complete result comparisons. The extracted standalone builder ran only in ignored `tmp/extracted/`; Python3.14.6 and its current zlib reproduced all six release files byte exactly, as well as PACKAGE_RECEIPT, CONTROL_PLAN and REPLAY_RECEIPT. No extracted shipped input changed. The operative PDF was a frozen input; this does not claim a new TeX compilation. Cross-runtime compressed-byte identity is not asserted beyond the actual runtime tested.

The builder invokes all seven pinned programs verbatim in ordinary and optimized modes. All14 successful runs compare entire JSON values, with only the specified two parent historical wrappers unwrapped to their result field. No mathematical fields are dropped. Four supplied program failure modes fail in both modes. The reproduced results support the published counts:3859,11120,57837 mathematical requirements (sum72816),129 and1558 priority requirements, and76 and213 parent checks. These remain finite controls supplementing the written arguments.

I additionally tested four genuine portable-runner mutations in ordinary and optimized modes, eight rejection runs total: corrupt input, corrupt checker, false expected arithmetic result with its expected-result pin deliberately refreshed, and an inserted Python assert with its checker pin refreshed. The false arithmetic result reaches the complete output comparison and is rejected with `Result mismatch`; it is not merely a checksum failure. The other expected errors are fingerprint mismatch and optimization-sensitive assertion. These checks were isolated in ignored mirror copies. `CONTROL_REPLAY.json` records every outcome.

`PIN_REFERENCE_SCAN.json` classifies426 JSON digest occurrences matching current members and144 unmatched occurrences. All144 are explicitly historical original editions(6), dated revision pre/post history(30), or external/derived private source artifacts(108). None is an unexplained current manifest discrepancy. In particular the HEADER_CLARITY and IID_ENERGY revision records, and nested earlier “current” fields in cumulative PACKAGE_EDITORIAL_FIX, identify their own dated revisions; their hashes are not substituted for current manifests. Current root fingerprint records agree with the actual release reports/manifests.

All22 relative Markdown links in shipped authored documents resolve inside the source archive. A supplementary privacy scan finds no credential-like tokens, raw HTML bodies or email addresses in the non-PDF source members. Manual content and inventory review agrees: only authored summaries, provenance and pin receipts accompany the proof/code; third-party bodies/text/images/raw API data and private caches are excluded. CC BY4.0 is expressly limited to original authored material. Ten source-PR files remain historical and unchanged. Metadata equals the repository deposit metadata exactly; the portable kit preserves identical metadata and correctly changes only the two upload paths to flat member names. Author/title/ORCID/date/version/claim and review-status disclosures are consistent. No journal acceptance, external human review, formal proof or exhaustive priority is implied.

## Frozen PDF and links

All four operative pages were rendered with Poppler and visually inspected individually. Title, author, ORCID,17October2026, version1.0.0, equations, exact fractions, theorem/proposition numbering and three bibliography entries agree with main.tex. No clipping, overlap, missing glyph, unreadable formula or page-boundary defect was observed. Metadata has the expected author/title/subject. All19 named destinations resolve to real pages; all six internal annotation links resolve; all four external PDF annotation links are correct. All nine distinct paper/metadata/license URLs return200, including correct DOI redirects and primary-source identities. `PDF_REVIEW.json` and `LINK_CHECK.json` record the details. No PDF was rewritten or recompiled.

## Scope and final disposition

No actionable mathematical, provenance, priority-framing, metadata, privacy, license-scope, inventory, fingerprint, reproduction or PDF defect was identified. The all-n and all-d assertions have explicit universal proofs above; finite programs are corroboration. The result concerns E disc_p^p only. It does not order expected norms, settle good-generator existence, establish a first result relative to all literature, or recertify inaccessible sources or every broader claim of the later overlapping preprint.

`END_PINS.json` rechecks all start-pinned files and the six frozen identities. `ARTIFACT_RECEIPT.json` seals all authored public review artifacts except itself, private source bodies and temporary mirrors. Completion toward the assigned whole-package review:100%. No changes to the candidate are requested by this review.

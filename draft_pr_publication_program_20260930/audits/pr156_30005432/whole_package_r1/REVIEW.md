# Fresh whole-package adversarial review R1: PR156

Scientific verdict: **No substantive mathematical, source-scope, attribution, package-integrity, verification, PDF, metadata or proposed-native inconsistency was found in the frozen v1 candidate.** The direct proof is correct and answers the exact unrestricted question. This is a clean scientific assessment with the limitations below, **not publication clearance and not a seal-first blinded review**.

## Independence and process limitation

This is a newly assigned whole-package review, not a historical September review. I began from the frozen manuscript/code/package and proposed native attempt. My initial read bundle mistakenly included native_proposal_v1/PRIORITY_AUDIT.md, containing ROOT/family conclusion summaries, before the initial assessment was sealed. I disclosed the sequencing failure to ROOT immediately. FIRST_ASSESSMENT_SEAL.json was written at 2026-10-12T06:48:04.091200+00:00 with exact initial consumed-input hashes and an explicit unblinded status. Its assessment has not been retrospectively edited. No package priority_reviews bodies or private source-family verdicts had been read at that seal, but the ROOT summary had been read. Accordingly this pass cannot fulfill the requested blinded seal-first sequence. An entirely new reviewer must perform that sequence before the final gate.

The calculations, source comparisons, byte comparisons, negative controls and visual inspection below were performed by this reviewer. They do not rely on accepting ROOT or family conclusions as axioms. I did not delegate operations, contact an outside individual, alter the candidate, or perform any Git/index/ref/checkout/MAIN, author-branch, PR, Zenodo or GWS action. All review writes are in whole_package_r1. Third-party source bodies remain private and are not in the public-output whitelist.

## Exact claim and falsification criteria

The claim is that the left brace B with additive group Z×Z/4 and circle product

(n,c)∘(m,d)=(n+epsilon(c)m,c+d+2cd mod4), epsilon=(1,1,-1,-1),

has precisely S(B)=Z×{0,1} for the two original fixed-intersection indices. In particular x=(0,1) has indices2/2, while 2x=(0,2) has both infinite. It fails additive subgroup closure and lambda invariance, while S remains a normal multiplicative subgroup. The brace must satisfy the left brace axioms for every integer, fail the excluded two-sided identity, and use the original ambient additive and multiplicative groups for the two different indices.

Failure would include a wrong sign/bit convention, an invalid group or lambda law, omission of a centralizer or fixed-set condition, a false subgroup/index computation, extrapolation of infinity from finite data, a stronger hidden source assumption, or an attribution/chronology/publication claim not supported by the bounded evidence. I also checked consistency among PDF, LaTeX, code, JSON outputs, archive, metadata and native proposal.

## Independent mathematical reconstruction

1. Writing c=u+2v and d=s+2t with bits, c diamond d is the XOR of the two bit strings: the integer carry from u+s is cancelled modulo4 by2us. The second-coordinate multiplicative group is V4. The high bit gives epsilon(c)=(-1)^v, a character. Consequently circle is the genuine semidirect product over Z, with inverse(-epsilon(c)n,c). This proves associativity and inverses universally, independently of bounded integer testing.

2. The exact lambda map is lambda_(n,c)(m,d)=(epsilon(c)m,(-1)^c d). Both factors are additive units. The identity a∘b=a+lambda_a(b) therefore proves the left brace law. The star is((epsilon(c)-1)m,2cd). My independently implemented affine arithmetic compares formal coefficients of three arbitrary integer variables for every finite residue triple, and confirms the group law, brace law, lambda homomorphism, lambda/star formula, commutation equation and conjugation formula. These276 coefficient checks exhaust the finite actor coordinates while leaving the integer variables formal. The further640 direct intersection controls include zero/nonzero and positive/negative integers of100digits; they support the classification rather than establish infinity.

3. For z=(n,c), addition is abelian and

H_z={(m,d):(epsilon(c)-1)m=0,2cd=0},

K_z={(m,d):(epsilon(c)-1)m=0,(epsilon(d)-1)n=0,2cd=0}.

The K formula follows because g*z=0 gives the last two restrictions, while g∘z=z∘g is(epsilon(c)-1)m=(epsilon(d)-1)n. It is not permissible to omit this multiplicative centralizer, and the candidate does not omit it.

4. For c=0, H=B. For c=1, H=Z×{0,2}, with additive index2. For c=0,1 the four K factors, according to n=0/nonzero, are C,{0,1},{0,2},{0}, respectively. Each is a V4 subgroup, so K is the inverse image under the surjective circle projection. Its index is4/|L|, giving precisely(1,1),(1,2),(2,2),(2,4) in the stated table. This works for every nonzero integer n because the equation-2n=0 over Z forces n=0; no small-integer assumption is used.

5. For c=2,3 both H and K require m=0. H is{0}×C for c=2 and{0}×{0,2} for c=3. K has finite actor factor C/{0,1} for c=2 and{0,2}/{0} for c=3 according to n=0/nonzero. Those are legitimate multiplicative subgroups. Additive representatives(j,0) have difference(j-i,0) and are in one H coset only when i=j. Multiplicative representatives likewise satisfy(i,0)^-1∘(j,0)=(j-i,0), which belongs to K only when i=j. This provides infinitely many distinct cosets in both ambient groups. No normality of H/K or finite extrapolation is needed.

6. The resulting S is the kernel of the multiplicative character epsilon and is normal. It contains(0,1) but excludes its additive double(0,2) and lambda_x(x)=(0,3). The supplied right-distributivity counterexample evaluates to(-1,2) versus(1,2), excluding two-sidedness. The circle group D_infinity×C2 description follows from the independent high-bit actor and trivial low-bit actor.

INDEPENDENT_EXACT_RESULTS.json and independent_exact_checks.py preserve the checkable reconstruction. Both ordinary and optimized execution pass. The written coset proof remains the infinity certificate.

## Original question and neighboring source claims

I inspected the full relevant primary OWR p543 image and text and published CFT pp176–178 text, including the p177 image. OWR Question1 is about an arbitrary skew brace, independently of its preceding discussion of finite solutions. Its displayed indices use Fix^r(x) in the additive group and Fix^l(x) in the circle group. The next line omits one superscript typographically, but the display and CFT Definition3.7 fix the intended convention. CFT Example3.8 has exactly the C4/V4 finite brace. CFT Proposition3.10 is for two-sided braces, and the following text leaves the skew-brace case unresolved there. The candidate respects these boundaries and does not confuse global(S), finite lambda orbits or finite additive conjugacy with(s).

The proposed SOURCE_RECONCILIATION.md accurately distinguishes the restarted isolated Lemma3.12 statement from the preceding global(S) context. In B, the additive generators(1,0),(0,1) are(s) but do not generate B multiplicatively. The displayed f-map collision is real. My independent full enumeration of B3=(Z/3)×(Z/4) verifies Ann(B3)={0} and the distinct input cosets(1,0),(0,0) having equal f-data. That finite counterexample falsifies the displayed injectivity step even with global(S), while satisfying the finite-annihilator conclusion. It does not refute the full JKVV theorem. The available JKVV author text includes the separate finite B^(2) and additive commutator hypotheses; B has B^(2)=2Z×{0,2}, infinite, and does not meet them. The separate global(S) finite-index proof in the repaired note is sound: finite generator lambda orbits imply finite lambda image; intersecting its kernel, the common fixed subgroup and the additive center gives Ann at finite additive index. Kernel addition and multiplication agree, and its corresponding right cosets agree, justifying the index step.

Ferudun version1.1's reported personal communication is attributed to that note. It is not represented as communication by this project, nor as independently established author intent. The complete publisher JKVV body remains unread, as explicitly disclosed.

## Ancestry, overlap and chronology

The asserted old ingredients are supported by the primary texts: Bachiller Proposition2.4(iii) contains c+d+pcd on Z/p²; Smoktunowicz–Vendramin's published Corollary3.37 gives the exact semidirect product convention; Dietzel Theorem5(iv), with its binary-string convention, selects the high-bit inversion parameter in the finite cyclic-module family. Replacing that finite module by trivialZ is a standard elementary specialization. The construction method and character are not credited as new.

CPV's author-labeled v2 postprint Proposition5.17 identifies exactS with multiplicative FC for a theta_f brace. Its hypothesis holds here because addition is abelian and the lambda image has four maps. The universal conjugation formula((1-epsilon(c))m+epsilon(d)n,c) gives the same S. I independently checked the primary publisher metadata: the article was published26August2026 in Mediterr.J.Math.23,article187; the full VOR body remains inaccessible and is not claimed read. The postprint is identified separately, and the exact submission14September date is correct.

I also independently reconstructed the two supporting prior deductions. The July F2^4 finite factor has character kernel{0,1,6,7,10,11,14,15}, with6 XOR10=12 outside and lambda_8(6)=4 outside. Its infiniteZ-module variation has witness indices(2,2),(4,8), with the sum's two indices infinite. The September MSTY arbitrary-F7-module variation has exact formal group/brace/star/conjugation coefficients and S=U×F3²×{0}; the displayed two witnesses each have indices3/3 and their additive sum has actor1, giving infinitely many basis-vector cosets. My68955 exact controls pass in both ordinary and optimized modes. These are elementary deductions from older finite constructions, not evidence that those papers explicitly printed the negative property-(s) conclusion. The package makes that distinction correctly.

Ferudun v1 Theorem1.2 is an exact formula/S-set/witness overlap, directly confirmed in the cached primary text. The primary Zenodo JSON gives created2026-10-11T05:15:40.640397+00:00 and DOI10.5281/zenodo.23292254; the actual v1 PDF matches its recorded size, MD5 and package SHA256 receipt. Version1.1 adds the attributed source-lemma communication without changing this core. The package does not claim the later paper's additional classifications or positive theorems.

Cached primary GitHub JSON records PR creation2026-09-30T12:24:37Z and the supplied head aec31742f3f26c5b1e533404da57539d17dc94a1. The original proof bytes match the receipt. The commit-author/committer dates are author-supplied and are expressly distinguished from the provider PR date. All22 native historical originals match their original fetched bytes, SHA256 sizes and independently recomputed Git blob IDs. Native COUNTEREXAMPLE Sections1–5 have no changes from the preserved original. The frozen timeline's four-commit content comparison was performed by its certifier, whose mechanism and cached primary commit metadata I inspected; I did not repeat remote authenticated content fetches or certify historical public visibility. Current public visibility and the author's historical report are qualified correctly.

“Contemporaneous separate discoveries” is explicitly defined as separate disclosures in the same period and accompanied immediately by denials of certified mutual independence and literal simultaneous release. In this explicitly qualified usage it is defensible. The dates are not made into awareness, independence or exclusive-priority evidence. The bounded-search finding is not turned into historical novelty or literature absence. The unaccessed publisher bodies and word/conjugacy article remain genuine priority limitations, stated in the manuscript, support material and proposed PR. This review does not expand the bounded audit into a complete novelty census or recertify unrelated imported theorems.

## Byte integrity, reproduction and falsification

PACKAGE_INTEGRITY_AND_REPRODUCTION.json records:

- Every five-item PACKAGE_V1_PREPARATION pin matches actual bytes, including PDF/ZIP/metadata/manifest/LaTeX.
- The ZIP has17 distinct safe members, clean CRC, and exactly the MANIFEST set plus MANIFEST itself. Every declared member size and SHA256 matches the extracted bytes; extracted files equal loose package files.
- Native publication_package is an exact full byte copy, and metadata.json is exactly the metadata object of zenodo-deposit.v1.json.
- Fresh extracted ordinary and optimized runs each give33512 checks and JSON identical to the deposited records.
- Supplied wrong-sign and wrong-index mutations fail in each mode. Additional reviewer-chosen wrong-star-term, wrong-inverse and wrong-circle-action mutations also fail in each mode. The six additional stderr artifacts are preserved in own scratch.

verify_controls.py writes its diagnostic JSON outputs; README warns to use a copy. I ran it only in my extracted copy, with TMPDIR confined to own scratch. No frozen package bytes changed. The source-hash output is a byte association, not a formal LaTeX proof checker, and README states this. I found no false claim that finite computations prove infinitude or novelty. The standard-library/Python3.11+ reproduction instructions are consistent with the flags used.

The ZIP contains no third-party bodies, private retrieval headers, internal absolute paths in priority reports, or detected credential patterns. It contains original review prose, derivations, locators and chronology receipts. Scratch renderings, raw third-party inputs and transient mutants are excluded from the public-output whitelist.

## PDF, metadata and native proposal

All four rendered A4 PDF pages were inspected visually. Equations, table, title/date/author/ORCID, references, page numbers and disclosures are legible; I found no clipping, overlap, broken symbols or misleading figure. The displayed text agrees with the LaTeX, including both infinite indices, the exact definition, earlier-date qualification and credit. The standalone source is included in the support archive. This pass did not rebuild the PDF, certify its accessibility tagging or perform a binary reproducible TeX build.

Metadata title, author/ORCID, preprint/unrefereed status, CC-BY4.0,1.0.0 version,12October2026 formal date, referenced identifiers and deposit file paths agree with the package. The formal date is later than the original PR and is not backdated. The absence of a new deposit DOI is appropriate because this is still prepared work.

The active native README clearly labels publication/merge pending, points to the current manuscript, warns that the historical assert-based checker is unsafe under optimization, and does not promote historical status/reviews as current certificates. Current wrappers execute the distributed raised-check checker. Historical originals remain byte-exact. Proposed PR text preserves exact overlap, antecedents, priority limits, AI disclosure and pending operational state. No fabricated upload or merge receipt is present. Several compressed prose tokens could be spaced more readably, but this is an editorial matter and not a substantive scientific defect.

## Final disposition and limits

**Substantive findings: none. Scientific candidate: passes this adversarial audit. Publication clearance: false.** This review has an explicit independence-order failure, so a new reviewer must seal a direct first assessment and consumed-input hashes before opening ROOT/family/historical verdict summaries. That is a process requirement, not a defect in the verified proof. Missing VOR bodies, historical visibility, mutual awareness/independence, exhaustive priority, full source-theorem recertification and binary TeX reproducibility remain uncertified. Those limits are compatible with the candidate's restrained claims. Review completion100%; package promotion remains a separate gate.

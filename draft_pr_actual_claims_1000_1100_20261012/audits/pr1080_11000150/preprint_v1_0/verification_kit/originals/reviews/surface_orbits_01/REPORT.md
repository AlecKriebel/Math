# Independent mathematical and source review of PR 1080

Review family: surface topology, support orbits, and symplectic applicability. Problem 11000150 / AMR-109-0150. Reviewed head: `64b252b199f2692eef2545656190c14bcaf63889`.

**Verdict: accept the stated boundedness partial. Zero actionable P0, P1, P2, or P3 findings.** The submitted proof establishes finite ordered simultaneous-conjugacy classes and an attained finite length maximum for each fixed genus under its explicit essential-curve convention. The separating-factor exclusion and credited values M(1)=12 and M(2)=40 also pass. This is not a solution of the whole exact-maximum and classification bundle.

## Independence, custody, and scope

I read root AGENTS.md and created this dedicated review folder. Before reading the prior audit, metadata, status, README, manifest, or their conclusions, I copied and hashed all six actual Git blobs at the reviewed head and all six submitted files, and pinned the complete target tree. Actual and submitted bytes agree. I then read MATHEMATICAL_REPORT and freshly downloaded the original question and cited primary preprints. The independent reconstruction was frozen at 2026-10-14T04:04:41.866941+00:00 with SHA-256 `6d103e548e7c81b5ed07e026fcb6eb7ba17280bc3052b6a0002f8803369e1663`. Only afterward did I read and reconcile the other five files and the root's captured PR body.

The full target tree has exactly MANIFEST.json, MATHEMATICAL_AUDIT.md, MATHEMATICAL_REPORT.md, README.md, SOURCE_METADATA.json, and STATUS.json. The actual Git comparison from the captured base `f6caddda8f8be2cdb3e91494325d8f7f365bc3fc` adds exactly those six files and changes nothing else. The manifest binds its other five members correctly; the captured PR body also binds all six, including the manifest. The prior audit's report hash and size agree with the actual report. This is byte custody, not an independent attestation of historical activity described in those files.

This review covers all mathematical assertions in the six-file target and their cited source interfaces. It does not certify historical attempt accounting, exhaustiveness of prior searches, priority, present-day openness, or unavailable human review. No branch, index, commit, PR service, or publication mutation was performed. All writes are inside this review folder. Full primary sources and rendered source pages remain in ignored `sources/raw/` and `sources/rendered/`; originals and submitted files were not changed.

## Exact hypothesis and source boundary

Fix g>=1 and the compact connected oriented surface S(g,1). Mapping classes and isotopies fix its boundary delta pointwise. Each factor is a positive twist about a non-null simple closed curve, with repetitions allowed and counted in word length. Every pair of factor classes has geometric intersection at most one. Boundary-parallel classes are allowed in the broader convention. Null curves are explicitly excluded; allowing them would insert arbitrarily many identity factors.

The original [Farb volume, Wajnryb Chapter 8](https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf), printed 124-126 / PDF 131-133, was freshly retrieved and these pages were viewed. The restricted Smith question is printed 126; printed 125 asks a different unrestricted question. Repetition appears in the genus-two discussion. The later positive-Artin/Hurwitz question is distinct. The source's contextual use of nontrivial positive relations and Lefschetz monodromy supports the explicit essential-curve convention; its displayed question does not independently spell that convention out.

The verified theorem answers the restricted arbitrary-length clause negatively, and proves existence of the maximum. It supplies neither M(g) for g>=3 nor an explicit length upper bound. Extremizers, Hurwitz equivalence, positive Artin equivalence, T-moves, and A5/D6 classification remain unaddressed. Every submitted summary preserves that boundary.

## Independent mathematical verification

### Positive identity obstruction and finite alphabets

Let the arc order point toward the right. Every positive essential twist is right-veering. A nontrivial mapping class moves some boundary-endpoint-relative proper arc: otherwise a finite disjoint arc system cutting the surface to a disk can be fixed successively by isotopy, followed by the relative-boundary Alexander trick on the disk. Thus arc action is faithful. Nontrivial essential twists, including peripheral or separating twists, move an arc strictly right. The inverse sends that image arc strictly left and is not right-veering. Since right-veering maps form a monoid, an identity t1...tn=1 with n>0 would make t1^-1 a right-veering product, a contradiction.

The applicable [HKM v1](https://arxiv.org/abs/math/0510639v1) Definition 2.1 and Lemma 2.5 use homotopically nontrivial curves. Their proof covers annular twists, then separating cases by extension or positive nonseparating relations. BMVHM's narrower length convention is not needed for this broad obstruction. HKM PDF 2 and 4 were viewed, with the relevant proof text read through PDF 6. The annulus is handled directly by its integer twist number; the disk case is vacuous.

For u=s1...sm contained as a scattered subsequence in v=b0 s1 b1...sm bm, put P0=1 and Pj=s1...sj. Direct telescoping in any group gives

    v u^-1 = (P0 b0 P0^-1)(P1 b1 P1^-1)...(Pm bm Pm^-1).

A proper insertion contains at least one letter. Every conjugated letter remains a positive essential twist, because the ambient set of all such twists is conjugation invariant. Equal evaluation would therefore create a forbidden nonempty positive identity. A fixed evaluation fiber is an antichain for subsequence. The report's minimal-bad-sequence proof of finite-alphabet Higman is valid: remove the last letter, pass to an infinite common-last-letter subsequence, and every possible good pair contradicts the original badness or minimality. Empty words and repeated letters cause no exception. An infinite fiber enumerated without duplication consequently cannot exist.

No claim that a finitely generated positive monoid alone has finite fibers is made. Conjugation invariance and the identity obstruction are essential additional premises. No Artin representation injectivity is used.

### Distinct support bound

H1(S(g,1);F2) has 2^(2g) elements and alternating intersection pairing. If [c]=[d], then [c] dot [d]=[c] dot [c]=0. Geometric intersection has the same parity. Therefore i(c,d)<=1 forces i(c,d)=0 for equal mod-two classes.

Remove the sole possible boundary-parallel class. Each homology fiber is then a collection of distinct nonperipheral essential classes with pairwise zero intersection. Simultaneous disjoint realization and extension to a pants decomposition bound its cardinality by 3g-2. The zero homology class is included, so separating curves were not discarded. Restoring the possible peripheral class proves

    |support| <= 2^(2g)(3g-2)+1.

This counts distinct isotopy classes only. It leaves occurrence multiplicities completely unrestricted. In genus one the two-letter chain already has length 12, exceeding the coarse support bound 5, so interpreting this quantity as a length bound would be false. The submission explicitly avoids that interpretation.

### Simultaneous minimal position and finite embedding records

Since chi(S)=1-2g<0, use a hyperbolic metric with geodesic boundary. Each nonperipheral simple class has its simple geodesic representative. All pairwise intersections of these representatives realize the respective geometric minima at once. Distinct representatives cannot share an interval or be tangent at an intersection, because uniqueness of geodesics would force them to coincide.

At a multiple crossing, the finitely many participating local branches meet transversely in pairwise distinct directions. Their endpoints alternate for each pair. A sufficiently small generic perturbation of the branches preserving their endpoint order produces exactly one double crossing for every formerly concurrent pair and no triple crossings. Other branches can be kept outside the disk. The sum of resulting crossings is at most m(m-1)/2 for support size m; no extra forbidden intersection is created. A peripheral representative lies in a separate collar.

The union is now a bounded embedded graph: four-valent crossing vertices and one auxiliary two-valent vertex on each isolated circular component. With v4 crossings and v2 isolated-circle vertices, there are E=2v4+v2 edges. Record the cyclic ribbon order, opposite crossing pairings, and the labeled constituent curve cycles. There are finitely many such records at bounded m. The abstract intersection graph alone would be insufficient; the report uses the richer record.

The ribbon graph determines its oriented regular neighborhood R with its marked curves. Record the partition of the boundary circles of R among complementary components, each complementary genus, and the component bearing delta. Each genus is at most g, and the number of components is bounded in terms of the number of R-boundaries. The complement therefore adds only finite data.

For two embeddings with the same record, first map the regular neighborhoods preserving the marked graph. Compact oriented surface classification supplies homeomorphisms of the corresponding complements. Their prescribed boundary maps can be matched to the neighborhood map by independent collar extensions. Orientation-compatible circle gluing maps are isotopic, so no integer gluing parameter survives in an ambient-homeomorphism orbit. In particular, twists in an annular complement may alter a particular representative homeomorphism, but do not yield a new orbit of the marked support. Finally compose with an adjustment in a collar disjoint from the curves to fix delta pointwise. Disconnected supports, isolated circles, non-filling supports, annular complements, and the peripheral collar are all covered.

This establishes finiteness of support orbits for the exact relative-boundary, orientation-preserving group in the report. It makes no assertion of finiteness of raw curve classes before quotienting.

### Finite ordered conjugacy classes and attained maximum

Choose one support representative Cr from each of the finite support orbits. A support-normalizing mapping class f carries an ordered factorization to a word over the finite alphabet of twists along Cr. The word order is retained. Orientation preservation retains positivity, and boundary fixing makes t_delta central, so its evaluation is still t_delta. Each alphabet has a finite fiber by the previous algebraic argument. A finite union of finite fibers contains representatives of all ordered simultaneous-conjugacy classes.

The standard even chain of 2g curves, repeated 4g+2 times, evaluates to t_delta and has length 4g(2g+1). Adjacent curves meet once and other pairs are disjoint; repetitions meet zero. Thus the admissible length set is nonempty, finite, and has an attained maximum. This proves

    4g(2g+1) <= M(g) < infinity.

The proof is existential. It does not furnish the numerical maximum, an explicit length bound, or a search stopping rule. Finite support size alone does not control the fiber's longest word.

### Peripheral and separating factors; small genus

If a peripheral factor occurs m>=1 times, commute them to the front and cancel one boundary twist. The remaining equality is t_delta^(m-1)W=1. The positive identity obstruction forces m=1 and W empty. This argument works in every g>=1.

In genus one all nonperipheral essential curves are nonseparating. The abelianization weight is 1 per such twist and 12 for t_delta, giving length exactly 12; the two-curve chain attains it. The peripheral singleton cannot change the maximum.

For g>=2, suppose a separating nonperipheral curve c occurs. Every closed curve has even geometric intersection with c, so the <=1 condition makes c disjoint from all factor classes. After capping delta, all factor curves remain essential: if one bounds a disk afterward, that disk either avoids the attached disk, making the original curve null, or contains it, making the original curve peripheral. Both alternatives were excluded. In particular c still has positive genus on both sides.

The nonempty capped positive identity gives the usual Lefschetz fibration over S2 by attaching the ordered positive Lefschetz handles over a disk and closing by a second disk. There is one critical point per factor, so it is nontrivial. Essential capped vanishing cycles ensure relative minimality (no spherical fiber components). The original one-boundary lift supplies a section of square -1. Its intersection number with a fiber is 1; hence the fiber is homologically nonzero, and the positive Thurston-Gompf symplectic construction applies. The total space is allowed to be nonminimal: a section sphere of square -1 does not violate relative minimality.

[Smith v1](https://arxiv.org/abs/math/0011223v1) Theorem 1.3, Proposition 4.2, and Corollary 4.3 provide the no-common-invariant-essential-curve implication needed here. I read the full 13-page text and viewed PDF 1, 3-7, and 10-11, including the genus-at-least-two convention and proof bodies. Only a nontrivial genus>=2 fibration is used, not a trivial bundle or a genus-one hyperbolic model.

The singleton invariant-curve mechanism can also be checked directly: choose annular supports disjoint from c, pushing the twist about c itself to a parallel curve if needed. Lift each twist fixing a lift of c. On the circle at infinity the chosen lifts have the same directed monotonicity and fix the two endpoints of that lift. Their product, because the closed mapping-class product is the identity, induces a deck transformation. On the intervals delimited by those common fixed endpoints, a nonidentity monotone factor cannot be undone by later factors, so their product is not the identity circle action. A nontrivial hyperbolic deck transformation fixing those endpoints moves in opposite directions on the two complementary intervals. This contradicts the monotonicity. No multiple-curve induction or count of fixed points is required. Consequently a separating factor cannot occur.

The [BMVHM v2](https://arxiv.org/abs/1412.0352v2) length L counts nonseparating twists. Its Theorem A gives L(t_delta)=40 for g=2, with the finite-case proof in Theorem 6 and the final assembly on PDF 19. I read the complete 22-page preprint and viewed PDF 2, 5-9, and 19. The separating exclusion supplies the missing interface from the report's broader convention to L. The four-curve chain has length 40 and satisfies the pairwise restriction, proving M(2)=40. The same source's unrestricted infinite-length regime covers g>=3 and does not impose the pairwise restriction; there is no conflict with the theorem being audited.

## Source and prior-method reconciliation

All five newly downloaded complete primary PDFs agree exactly with the source metadata's byte counts and SHA-256 values. Pinned edition URLs and retrieval times are in SOURCE_FETCH_RECEIPTS.json; hash comparisons are in SOURCE_HASH_RECONCILIATION.json. The versions are Wajnryb's author-hosted full volume, HKM v1, Smith v1, BMVHM v2, and Cossu-Tringali v3. ArXiv metadata supports the recorded BMVHM and CT journal references; the institutional Smith publication listing supports its journal reference. No downloaded preprint is represented as byte-identical to its published journal edition. The new retrievals and inspections belong to this review and do not retroactively validate historical retrieval times.

[Cossu-Tringali v3](https://arxiv.org/abs/2208.05869v3) Theorems 4.10-4.11 and Lemma 5.7/Theorem 5.8 were text inspected and PDF 19-20, 23-24 were viewed. They document earlier Higman applications to noncommutative factorization. The submission credits this prior mechanism and proves its group/surface application directly. It does not claim an unchecked application of CT's abstract hypotheses or an unprecedented method. [Higman's publisher metadata](https://londmathsoc.onlinelibrary.wiley.com/doi/10.1112/plms/s3-2.1.326) confirms the bibliographic citation; no original full-article download is claimed or needed for the independently supplied finite-alphabet proof. The initial DOI redirect was inaccessible to the browser tool; the publisher metadata was recovered through its indexed official page.

One source detail is deliberately not adopted: Smith's literal fixed-point-count wording in Proposition 2.1 is stronger than the needed directed-motion assertion. A twist lift fixing a positive-genus complementary subsurface fixes its limit set at infinity, which can be an uncountable Cantor set. Fixed-point cardinality does not enter the invariant-curve contradiction above or any submitted proof. This is an informational source caution, not a defect in a claim or argument of this PR.

The source inspection verifies the quoted prior-result interfaces, not every theorem or every external gauge-theoretic reference in the source bibliography. No bounded search result is elevated to an exhaustive priority certificate. No novelty or continuing-openness claim is asserted by the submission or this review.

## Exact finite sanity and deliberate-fault checks

`sanity_checks.py` and SANITY_RESULTS.json contain reproducible exact computations:

- 20,685 free-group insertion identities, including 20,670 proper insertions, pass. Removing conjugations fails on the explicit u=a, v=ab case.
- 5,460 mod-two self-pairings through genus six vanish exactly.
- Ribbon chains with 2-12 curves have the expected neighborhood genus and one/two boundary pattern. An isolated circular component has an annular neighborhood. Replacing the alternating crossing ribbon order by a nonalternating order changes the boundary count from one to three, demonstrating why ribbon data are necessary.
- Exact rational perturbations of 2-16 concurrent lines produce exactly one double crossing per pair and no triple crossings. Distinct pair sums and products make collision checks exact.
- The genus-one chain falsifies the deliberately wrong interpretation of the distinct-support bound as a length bound.
- All five manifest member hashes and sizes validate.

These checks catch transcription and encoding faults; they are not an enumeration proof of Higman, support-orbit finiteness, the chain relation, or boundedness. They are newly authored review checks, not a claimed replay of omitted historical computation. No computational premise is needed for the written proof.

## Whole-package consistency and remaining gap

MATHEMATICAL_REPORT, MATHEMATICAL_AUDIT, README, STATUS, SOURCE_METADATA, MANIFEST, and the captured PR body consistently state the same hypotheses, repetition convention, peripheral singleton, finite ordered simultaneous-conjugacy conclusion, low-genus credits, and partial status. The report's Smith bridge is stronger than a naked source citation: it includes the Lefschetz construction, section, nonzero fiber class, and essentiality after capping. The six-file target contains no program, test output, imported data body, or omitted computation upon which the mathematics depends. No historical program replay is required or claimed.

The strongest verified result is fixed-genus finiteness with M(1)=12, M(2)=40, and the chain lower bound for every genus. The exact gap is M(g) for g>=3, explicit numerical length upper bounds, and any finer extremizer/equivalence classification. The whole bundle remains partial. This review is AI-assisted, unrefereed mathematical checking, with no external human or formal-assistant certification.

| Severity | Actionable findings |
| --- | ---: |
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |
| P3 | 0 |

No change to the submitted six files is required by this review.

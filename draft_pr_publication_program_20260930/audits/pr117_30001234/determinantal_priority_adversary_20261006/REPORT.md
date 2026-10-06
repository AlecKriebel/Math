# PR117 adversarial priority audit: determinantal thresholds and exact source equivalence

**Final disposition recommendation: already_solved for the exact imported target.** The mathematics is valid, but an explicit counterexample with the same three minors was published in 2013. Novel-resolution publication clearance fails. No new central proof-search turns were used.

PR117 immutable head: 8163ee0dc7a0f944570925984cef2dc0fb291ad8. Problem 30001234 / OWR-3471-008. Original candidate SHA-256: 1409e8ad35d34f3cc4a9bb14f7e42318c1dd1e0446ecba525c655fad8c978cdf. Incoming construction effort remains 1/5. This family does not perform PR closure, native assessment, merge, publication, tracker, Git/index/ref, or shared-record mutation.

## 1. Why this result is decisive

The decisive primary publication is Shunsuke Takagi, *Adjoint ideals and a correspondence between log canonicity and F-purity*, Algebra & Number Theory **7**(4) (2013), 917–942, DOI [10.2140/ant.2013.7.917](https://doi.org/10.2140/ant.2013.7.917). The actual [MSP publisher PDF](https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf) was retrieved, pinned, read in the relevant section, and visually inspected. Example 4.4 on printed p.940 explicitly gives the three minors, failure of the augmented-image hypothesis of Remark 4.3, local threshold two, and LP optimum three. Remark 4.3 on p.939 states the exact existential singleton-image condition; its matrix is (4) on p.937.

This is stronger evidence than the independent classical-threshold deduction recorded before that paper was inspected. The publication does not call its example “OWR Question 8” in the inspected passage. It nevertheless gives the exact mathematical counterexample to that question, as established by the explicit specialization and column permutation below. The conclusion does not depend on guessing the contents of a paywalled thesis or assuming a later graph LP is the original LP.

The current source's dated open-status triage omitted this 2013 publication. Its assertion of continued openness cannot support a novel open-problem-resolution claim.

## 2. Hypotheses and quantifiers: no scope mismatch

The original question concerns polynomial binomial ideals over characteristic zero, containing no monomial, and minimal binomial generating systems. Its property is existence of an optimal rational z whose augmented image differs from that of every distinct optimal z'. Shibuta–Takagi's primary Proposition 2.1 and Question 2.2, arXiv:0810.1278v3 pp.6–8, use this exact condition. The original official OWR Question 8 is on printed p.1139.

Takagi's Remark 4.3 allows a normal complete-intersection ambient X defined by c equations and adds an equality whose right-hand side is c. In Example 4.4, X is affine six-space. Therefore **c=0**, s=3, m1=m2=m3=2; the extra equality is the tautology 0=0. The ambient X is smooth, normal, a complete intersection of codimension zero, and log canonical. It is **Z**, not the ambient X, that is the determinantal subscheme. Thus the ambient-complete-intersection wording does not exclude the PR's non-complete-intersection ideal.

The nearby Theorem 4.1 imposes algebraically independent coefficients. That is not a hypothesis of Remark 4.3 or Example 4.4. The actual example uses coefficients 1 and -1, exactly as the PR does. Moving that nearby theorem's stronger coefficient hypothesis into the example would be an incorrect restriction.

Minimality and the no-monomial condition are not spelled out in the short published example, but both hold for the same ideal. At the all-ones point the three generators vanish and every nonzero monomial does not; so the ideal contains no monomial. The three degree-two binomials have six distinct monomials, and are linearly independent in degree two. Their classes generate and form a basis of I/mI, hence are a minimal polynomial generating system and remain minimal at the homogeneous maximal ideal. These elementary checks are unchanged by multiplying a generator by -1. Inverting an entry makes one generator redundant; Laurent localization is not the hypothesis of the source question.

## 3. Exact sign and coordinate bridge

The candidate's third generator is f3=x3*y1-x1*y3. The publication's third generator is -f3=x1*y3-x3*y1. This changes neither ideal nor minimality; its positive and negative monomial exponent columns are simply exchanged.

Let the candidate coordinate order be

    z=(mu1,mu2,mu3,nu1,nu2,nu3).

Takagi orders terms by generator, and its third sign is reversed. Consequently the published coordinate vector is

    sigma=(mu1,nu1,mu2,nu2,nu3,mu3).

Using zero-based candidate indices, the permutation is p=(0,3,1,4,5,2). Its complete augmented matrix is A_pub=A_candidate[:,p]; sigma=z[p]. Therefore A_pub*sigma=A_candidate*z for **all** rational coordinate vectors, not only for tested optimizers. Nonnegativity, objective sum, feasibility, distinctness, and equality/inequality of augmented images are all preserved bijectively. The last three rows in the publication are the three pair-group caps, and the first six are the same exponent rows. No constraint is discarded.

For the candidate's exact full optimal segment z(t)=(t,t,t,1-t,1-t,1-t), the publication's segment is

    sigma(t)=(t,1-t,t,1-t,1-t,t), t in Q intersect [0,1],

and A_pub*sigma(t)=1_9 identically. The criterion in Remark 4.3 is the same existence-for-all-other-optima criterion as in the original report. It is not a criterion about uniqueness of an optimizer or uniqueness of an image vector. Takagi explicitly asserts its failure for this very example, using lct_0=2 versus LP optimum 3.

These identities were separately checked in exact arithmetic. A mutation forgetting the third sign swap is rejected; so are forgotten interleaving, omitted generator caps, and conflation of ambient X with Z.

## 4. Independent classical-threshold audit, preserved before convergence

Before accessing the decisive Takagi2013 body, this family independently reached a prior-theory obstruction. That state is frozen in INDEPENDENCE_CHECKPOINT.md and INDEPENDENCE_CHECKPOINT_MANIFEST.json. No other new priority-family reports were read. The root later supplied the primary-source pointer; this family retrieved and audited the actual published passage independently.

The generic 2-by-3 size-two determinantal ideal has prior global log canonical threshold min(6/2,2/1)=2, by Docampo's primary Theorem 5.6 in arXiv:1011.1930v2 pp.21–22. The retrieved version records a 2011-02-20 arXiv version stamp and a June 2, 2018 title date; these are distinguished. The author and arXiv metadata identify the related 2013 journal article. AMS body requests returned 403, so its publisher text was not silently treated as read. Docampo credits Johnson's 2003 thesis; this family did not retrieve that thesis, and makes no earliest-2003 explicit-answer claim.

A **global** threshold alone would leave a local-at-origin gap. The independent geometric check closes it. The rank-one variety Z has a dense smooth codimension-two locus, and Z contains zero. Blowing up its smooth locus gives a divisorial valuation with ideal order one and log discrepancy two. Its center closure is Z, which contains zero. Mustata's primary local definition uses divisors whose centers contain the tested point. Thus lct_0(I)≤2. Since the source conditional theorem would imply lct_0(I)=LP optimum=3 if the singleton-fiber condition held, its strict contrapositive already gives a negative answer.

The diagnostic package also reproduces the local value two through six origin-blowup charts and two charts of the second blowup. In a representative origin chart, the residual ideal is (D,E), with D=d-ac and E=e-bc. It is smooth of codimension two and transverse to the first exceptional divisor (u=0). After the next blowup the ideal is (u²v), the composite Jacobian is u^5*v up to sign, and the two log-discrepancy ratios are 6/2=3 and 2/1=2. Row and column permutations cover every entry pivot. The unrestricted reasoning and necessary center-through-origin argument are fully recorded in the sealed checkpoint; computations verify these symbolic chart identities rather than replacing the geometric argument.

Miller–Singh–Varbaro's primary arXiv:1210.6729v2 Definition 1.1 and Theorem 1.2 independently give F-pure threshold two at the homogeneous maximal ideal, for every prime characteristic, and cite the same characteristic-zero formula. This is corroboration, not the only bridge and not an unlabelled replacement of a characteristic-zero invariant. The publisher uses issue year 2014 and publication date January 6, 2015; these differ and are retained. This later computation is not needed once the exact 2013 counterexample is read.

The distinction between the two priority mechanisms matters: the sealed classical route was a **reviewer deduction from old results**. The final source is an **explicit published counterexample with the exact same ideal and condition**. The latter removes the earlier remaining uncertainty over an explicitly stated prior negative answer.

## 5. What, if anything, the PR adds

The candidate gives a concise elementary complete-face proof, a direct prime-ideal argument, and reproducible exact diagnostics. Example 4.4 does not display the complete optimal-face parametrization in its short paragraph. That additional exposition is valid and can be retained as an audit/reproduction record, with attribution.

This audit has established no new ideal, new counterexample, stronger mathematical resolution, new threshold, or general algorithm. A first-time printed parametrization by itself would require a separate substantive novelty claim; the PR makes none and the parametrization follows immediately from the same nine inequalities. Repackaging a known counterexample with a fuller proof does not meet the program's requirement to resolve an original unsolved open problem decisively and newly.

The appropriate finding is **already_solved: exact universal question already has a published counterexample**. It is not “invalid math,” nor merely unresolved priority. It would be unfair to say that the candidate's verification files or every line of its exposition appeared in the prior paper. It is accurate to say that the central result and the same three-minor counterexample were already published.

## 6. Verification, source bounds, and release limits

The mathematical/source gate supplied by the root is actual PASS, authorized only beginning priority review, not merge/disposition. This family's final priority result is a recommendation for the root's cross-family and fresh disposition audit; it does not itself authorize or perform services.

- Independent bridge operator process 70549: normal and physical Python -O both passed 73 explicit exception checks; deliberately false guards returned nonzero in both modes. All six pivot charts, both second-blowup charts, exact LP and threshold specializations were checked.
- Exact Takagi coordinate operator process 72982: normal and -O both passed 33 explicit exception checks; false guards failed in both modes. Positive outputs match exactly between modes.
- Actual Takagi retrieval/render operator 71837 pinned the 1,075,287-byte publisher PDF, SHA-256 6ada6b6669124acda5bb4b0bd25a98d07b39808c07e7d41c1f0ae1ba49e085e5.
- Primary PDFs/text/renders remain private ignored material. Only citations, hashes, read boundaries, analysis, process metadata, and public-safe exact diagnostics are sealed. No external individual was contacted.
- This is a bounded audit of this exact claimed result, not a search for a replacement theorem. New central proof-search turns: zero; original substantive attempt ledger: unchanged 1/5.

Estimated completion of this family's bounded priority audit: **100%**. The overall PR workflow and repository goal remain the root's responsibility.

## References and inspected boundaries

1. [Takagi2013 publisher PDF](https://msp.org/ant/2013/7-4/ant-v7-n4-p06-s.pdf), DOI [10.2140/ant.2013.7.917](https://doi.org/10.2140/ant.2013.7.917): full Section4 extracted text printed935–940; visual full pages937,939,940 (physical22,24,25). Actual body is the decisive source.
2. [Shibuta–Takagi primary v3](https://arxiv.org/pdf/0810.1278v3): Proposition2.1 complete text/proof pp6–8 and Question2.2; full pages6,8 visually inspected. [Publisher metadata](https://link.springer.com/article/10.1007/s00229-009-0270-7) confirms May5,2009 online publication and September2009 issue. Publisher body not retrieved by this family.
3. [Official OWR21/2009](https://ems.press/content/serial-article-files/46224): Question8, printed1139/physical39, visually inspected. Original question scope, not a modern openness guarantee.
4. [Docampo primary v2](https://arxiv.org/pdf/1011.1930v2): printed1,4 and complete Theorem5.6 proof pp21–22, visually inspected; setup and relevant definitions read in text. [Author metadata](https://roi.docampo.xyz/) and [arXiv history](https://arxiv.org/abs/1011.1930) identify its journal reference and version history. Title date and arXiv version date are not conflated.
5. [Mustata primary v1](https://arxiv.org/pdf/1107.2676v1): local valuation definition and discrepancy normalization p5, global/local distinction and smooth-center Example1.5 p8; full pages5,8 visually inspected, Theorem1.1 text p6 read. [EMS publisher metadata](https://ems.press/books/ecr/117/2250) identifies the2012 published chapter DOI10.4171/114-1/16. The chapter publisher body was not retrieved.
6. [Miller–Singh–Varbaro primary v2](https://arxiv.org/pdf/1210.6729v2): Definition1.1 p1, Theorem1.2 and connections p2, complete threshold proof text pp4–5 and references; full pages1,2 visually inspected. [Publisher metadata](https://link.springer.com/article/10.1007/s00574-014-0074-6), DOI10.1007/s00574-014-0074-6, confirms2014 issue and January6,2015 publication. Publisher body not retrieved.


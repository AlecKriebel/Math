# Independent adversarial review of PR316's prepared priority correction

Review completed: 2026-10-04 15:20:17 UTC. Review-task completion estimate: 100%. Remote-publication finalization remains conditional as stated below. This is an independent AI-assisted mathematical/documentary audit, unrefereed and without human peer review or formal verification.

## Verdict and exact accepted claim

**Mathematical PASS; operational already_solved classification supported; prepared packet requires final acceptance wording and a byte-pinned finalization recheck before publication.** I found no counterexample to the claimed theorem and no mandatory mathematical correction. I do not certify historical firstness, that Erickson explicitly announced an answer to Thorisson's later named question, or that every admissible renewal law lacks nondegenerate scaling.

The precise accepted theorem is: for ordinary renewal with finite-a.s. strictly positive iid increments whose survival r is slowly varying and tends to zero, the classical integrated renewal asymptotic U(t)r(t)->1 implies D_t/t->infinity in probability. If D_t/phi(t) converges weakly to a proper finite law for any eventually finite positive deterministic phi, its law is delta_0. No monotonicity of phi is required. There is an explicit continuous non-lattice infinite-mean law in this class, so this defeats a universal affirmative reading of Thorisson Problem 1.2, including its proposed truncated-mean scale. Zero delay is an allowed instance, so a result for ordinary renewal suffices for the negative answer; the packet does not need to prove a statement for every delay.

The original submitted lacunary construction and every-normalizer proof are separately valid. Its tail is not regularly varying. This irregular construction is retained as a checkable construction with unestablished exact historical priority. The broader negative answer is a consequence of an authenticated 1970 premise and an elementary corollary articulated here. That is sufficient for the user's operational definition of already_solved ('the open problem was not actually open and we found a priority audit issue'). It is not evidence that an earlier author explicitly formulated or solved the later named question.

## Independence and access boundary

Before opening any candidate or prepared correction file, I froze INDEPENDENT_SOURCE_CRITERIA.md with SHA256 51e989a13290c5c3ace41717cb0e63d6a14fddf91a0cbece53218d6e001baeb9 and sent its path/hash to the root. Root explicitly released packet access afterward. The criteria bytes remain unchanged. I did not consult the root's adjudication or any fresh other-reviewer reports/conclusions.

I read all six prepared files, the preparation receipt, the snapshot manifest, original current wrappers, and all nine original author artifacts. The six inherited review artifacts were authenticated by size, SHA256, and Git blob SHA1 only; their contents/conclusions were not opened, and their checker was not run. This preserves independence while authenticating the entire original 18-file scope.

For Erickson I used only the expressly authorized original-article PDF at the local mirror path, copied into this review's evidence folder. The source binary SHA256 is 65716b4789f1f1b06400a286bb216fee368783c2eca7df750d2fe00d791b773b. Its independently indexed original-article mirror URL is https://artefacts-discovery.researcher.life/full_text/DA-2/70/701906b973143f3a95ae9d71ba1f1921/full_text/2f02b7d15c78d9518a4b31fc4f6ed046.pdf . Printed pp.264-266 were rendered and visually checked. The first four article pages were text extracted. I did not read every proof in the 29-page article and do not describe this as an AMS-domain binary retrieval. The packet's separate statement that the official AMS endpoint returned 403 is a provenance statement of the preparer; this particular reviewer observed DOI-tool inaccessibility, not that official-AMS HTTP response.

The original Thorisson preprint PDF timed out in the web tool and a preserved curl attempt. I checked indexed primary text for the definitions and Problem 1.2, and publisher metadata/abstract for the 2011 publication. No visual/full-binary preprint read, full published-text read, or preprint/published line-by-line comparison is claimed. These limitations do not affect the zero-delay counterexample under the indexed hypotheses. The packet properly retains the limitations.

Two model-capacity service failures were reported by the root during this review, after criteria were successfully written and during continuation. They are recorded in the research log as reported execution/service failures, with event timestamps unavailable. They are not mathematical failures. No model switch occurred.

## Mathematical falsification checks

### 1. Classical premise, including alpha=0

Erickson's actual Theorem 5 on printed p.265 explicitly permits 0<=alpha<=1 and relates regular variation of truncated mean m with exponent 1-alpha to regular variation of U with exponent alpha. Equation (2.2) on p.266 explicitly assigns the sine quotient value 1 at alpha=0. The article defines U([0,t]) and includes the renewal atom at zero. Thus r(t) slowly varying gives U(t)r(t)->1. This is an integrated renewal asymptotic; it does not incorrectly invoke a local strong renewal theorem at alpha=0. Both the theorem statement and the endpoint interpretation were visually checked, rather than inferred from the abstract's narrower-looking notation.

### 2. Exact straddling identity and endpoints/atoms

With S_0=0 and positive increments, there is a unique k such that S_k<=t<S_{k+1}. For x>=t,

    {D_t>x} = disjoint union_k {S_k<=t, X_{k+1}>x}.

Every event on the right crosses strictly beyond t because S_k>=0 and X_{k+1}>x>=t. Conversely the unique straddling increment of length >x appears on the right. A jump beginning exactly at t is counted; a jump ending at t is not the straddling interval. A jump with length exactly x is excluded on both sides. Independence and Tonelli give P(D_t>x)=U(t)r(x). Equality holds at x=t and at t=0. The identity does not require a density, non-lattice support, or absence of deterministic renewal atoms.

Strict positive iid increments ensure S_n->infinity almost surely; U(t) is finite. For the latter, choose delta>0 with P(X>=delta)>0 and dominate the number of increments before t by the number of trials required for floor(t/delta)+1 such successes. No unstated lower-bound assumption on general slowly varying increments is needed.

I independently tested this identity using exact fractions for three atomic toy laws, integer and half-integer inspection times, and x=t as well as larger thresholds. All 1,875 identity cases passed; a total of 1,959 exact assertions passed. These controls test the endpoint algebra, not the infinite-tail or all-scale theorem.

### 3. Every-scale obstruction, including oscillation and limit atoms

For fixed M>=1, U(t)r(Mt)->1 implies P(D_t>Mt)->1. Smaller fixed M follow by monotonicity. Hence D_t/t escapes to infinity in probability along every sequence of inspection times tending to infinity.

Suppose D_t/phi(t) has a proper weak limit. If phi(t)/t does not tend to infinity, choose t_j->infinity with phi(t_j)<=C t_j. Then for every K>0,

    P(D_(t_j)/phi(t_j)>K) >= P(D_(t_j)/t_j>KC) -> 1,

contradicting tightness. This covers bounded, vanishing, and oscillating positive scales. It forces phi(t)->infinity and eventually a phi(t), b phi(t)>t for any fixed positive a,b.

Slow variation then gives a ratio of the corresponding survival probabilities tending to 1. This ratio is well defined because r is eventually positive and U(t)>0. Boundedness by 1 makes their absolute difference tend to zero; no unbounded product is silently discarded. At positive continuity points of a candidate nonnegative limit, all survival probabilities agree. There are arbitrarily large continuity points; properness forces the common value to zero. For every x>0 one can choose a positive continuity point below x, so the limiting variable has no mass above x. The only proper law is delta_0. Positive atoms, a mixture of an atom at zero and mass elsewhere, singular distributions, and nonmonotone phi introduce no exception. Extended limits with mass at infinity are outside the question.

### 4. Explicit continuous logarithmic-tail law and bound

The packet's survival is 1 on [0,1] and 1/(1+log t) on [1,infinity). The two pieces agree at 1. There is no atom at 1; the density on x>1 is 1/[x(1+log x)^2] and integrates to 1. The law is supported in (1,infinity), finite almost surely, continuous and therefore non-lattice. Its mean is infinite: for large t,

    integral_1^t r(s) ds >= (t-sqrt(t))/(1+log t) -> infinity.

Its tail is slowly varying because (1+log t)/(1+log t+log c)->1 for each c>0.

For t>=1, the truncated first moment is exactly

    M(t) = integral_1^t dx/(1+log x)^2.

Splitting at sqrt(t), the first integral is at most sqrt(t) and the second at most t/[1+(log t)/2]^2. Dividing by t r(t) gives an upper bound

    (1+log t)/sqrt(t) + (1+log t)/[1+(log t)/2]^2 -> 0.

Thus the packet's displayed asymptotic bound is correct in the large-t regime in which it is used. For clarity it should label the displayed inequality t>=1; extending its written right side literally to all t>=0 would introduce an unnecessary singular expression at t=e^-2. The surrounding large-t context and tail definition make this a domain-annotation improvement, not a failure of the proof.

For the first X_j>t, T is the sum of preceding X_j<=t. Tonelli over geometric failure events gives E[T]=M(t)/r(t), including equality cases in the failure class. Markov implies P(T>t)<=M(t)/(t r(t))->0. On T<=t, the first increment >t straddles t, including T=t. Therefore P(D_t>t)->1 and the exact identity proves U(t)r(t)->1 for this particular law without Tauberian theory. The proposed scale satisfies exactly E[min(X,t)]=M(t)+t r(t), hence is asymptotic to t r(t), with its ratio to t tending to zero. D_t/t->infinity then defeats this scale.

### 5. Submitted irregular construction

The original mixture places residual mass uniformly on [1,2] and atoms p_n=2^(-2^n) at a_n=2^(4^n). The geometric majorant makes the atom probabilities summable and leaves at least 2/3 of the mass for the base component. Every increment is finite and >=1; the base component proves non-lattice support. The terms p_n a_n diverge, proving infinite mean.

The first-large-interval Tonelli calculation E[T_n]=M_n/q_n and the success-length probability p_n/q_n are correct. At t_n=a_n/2, T_n<=t_n with success length a_n places t_n strictly before the interval's end, even if T_n=t_n. The union/Markov bound, M_n<=a_(n-1), geometric tail bound, exponent formula, and truncated-mean identity all check. The displayed epsilon_n tends to zero. The point-concentration lemma is a valid tightness/subsequence argument for every deterministic divisor. This does not accidentally assume the scaled deterministic centers converge along the full sequence.

For non-regular variation, r(a_n/2)=q_n and r(a_n)=q_(n+1), since the base and smaller atoms are below a_n/2 and the strict survival excludes the atom at a_n. The ratio satisfies

    q_(n+1)/q_n <= p_n/(1-p_n) -> 0.

Regular variation with any finite index rho would require the factor-two ratio to tend to 2^rho, a strictly positive finite value. Thus the fixed-multiplier sequence already falsifies regular variation. No separate classification of rapid variation or proof of multiple incompatible subsequences is necessary.

The permitted author checker ran successfully and produced byte-identical original TURN_1_CHECKS.json: 7,852 exact assertions and 704 finite renewal cases. No inherited checker or fresh other-reviewer checker was run. Analytic conclusions above were independently checked from the source and author proof.

## Artifact and document consistency

The actual validation execution passed 80 artifact assertions. The preparation receipt binds exactly the six files reviewed here. Their bytes, SHA256, and Git blob SHA1 agree. The snapshot contains exactly 18 candidate files, all matching its pins. The original publication manifest's entries match the actual original files.

The proposed combined target has 19 files: the original 18 with only CURRENT_STATUS.json, README.md, and PUBLICATION_MANIFEST.json replaced, plus CURRENT_PRIORITY_NOTE.md. The prepared publication manifest binds all 18 accompanying files and correctly omits itself. All 15 historical author/review artifacts are represented by their unchanged original pins. The three old wrapper pins are correct. The author and inherited review manifest hash references are correct; substantive author count remains 1/5 everywhere checked. PR title/body are PR metadata, so their absence from the repository publication manifest is appropriate; the preparation receipt separately binds them.

Historical pending-review and claimed_solved labels remain in immutable original author/review files. The new README explicitly identifies those as historical and makes CURRENT_STATUS authoritative. The current wrappers consistently use already_solved, deny a new-resolution claim, and leave the draft unmerged under the claimed_solved-only scope. No paper, Zenodo, DOI, tracker row, or release is implied. No closing or partial-merging authorization is inferred.

The README, current note and PR body disclose extensive AI assistance, unrefereed status, and lack of human peer review/formal verification. No wording falsely attributes the later named question to Erickson. The distinction between a classical premise and the newly articulated exact implication is clear. The old general claim is not being promoted as novel; the specific irregular construction's priority remains expressly unestablished.

Bibliography: publisher metadata confirms the 2011 Thorisson title/date/pages/DOI; the indexed institutional catalog labels the differently titled preprint as 2010. The current note corrects the historical Angus-Ding article number to 108745 and DOI 10.1016/j.spl.2020.108745. I independently retrieved Crossref's publisher-deposited metadata for that exact DOI; it confirms title, Angus/Ding authors, volume 162 and article number/page 108745. The registry response is retained. The ScienceDirect page returned 403 in this review; I do not claim a full-text read or an independent reproof of the Angus-Ding result. The arXiv primary record confirms the 2015 three-page preprint authors Blanchet/Glynn/Thorisson. Cambridge metadata confirms Bingham/Goldie/Teugels authored the separate 1987 *Regular Variation* monograph. Neither contextual relative-age item is used as a theorem dependency here.

The packet also states that root/inherited/fresh controls numbered 646, 6124, 263 and 1773 passed and describes distinct current proof families. Those statements are internally consistent across the six files, but this review does not independently certify those executions or read their conclusions. Root must retain actual bound execution/report evidence for those public statements; this review's own replay and controls are precisely the 7,852 author assertions, 80 artifact assertions, and 1,959 new endpoint/tail assertions above.

## Mandatory publication finalization and bounded recheck

These are publication-finalization conditions, not findings that the provisional packet has already passed final acceptance:

1. **CURRENT_STATUS.json line 8:** after the required independent reports are actually accepted, replace the exact provisional value 'Submitted mathematics PASS; operational classical-corollary priority correction awaiting final bound acceptance before branch publication' with a factual final value. A suitable value is 'Submitted mathematics PASS; classical-corollary priority correction PASS in accepted frozen independent AI-assisted audits'. The finalization receipt must identify the accepted report/manifest hashes. Do not claim that acceptance or final-byte checking occurred before it actually did.
2. **CURRENT_PRIORITY_NOTE.md line 29:** replace the clause 'their final bound reports must be accepted before this prepared packet is published to the PR' after that condition has been fulfilled. A suitable final sentence is 'Their frozen reports were accepted before publication of this correction to the PR.' Bind the accepted report hashes in the local finalization evidence. Leave the operational distinction and no-firstness caveats intact.
3. **Regenerate PUBLICATION_MANIFEST.json** for every changed current accompanying file, retaining all 15 historical pins and the three original wrapper pins. Retain the existing preparation receipt as the historical pre-review receipt; create a distinct finalization receipt binding all six final prepared files rather than silently rewriting history. Recheck exact scope, hashes, author 1/5, and exclusions. The timestamp should describe actual finalization.
4. **Authenticate public audit/execution statements** against the root's frozen accepted reports and actual outputs, without using this reviewer to certify unobserved executions. There is no need to alter historical files or publish copyrighted source PDFs to meet this condition.

Two narrow clarifications are recommended for exact reader-facing scope: add '(t>=1)' to the log-tail displayed M(t) bound at note line 22; and replace PR_BODY.md line 5's 'This excludes every positive deterministic scale' with 'This excludes a proper nondegenerate weak limit for every positive deterministic scale'. The surrounding paragraph already forces any proper limit to zero, so the present wording is interpretable correctly in context; the replacement removes any implication that delta_0 convergence is impossible. Space concatenated bibliographic names/years and counts where practical for readability.

**A byte-pinned bounded finalization recheck can resolve all listed conditions.** It should compare the final six files to these reviewed bytes, accept only the factual acceptance wording/domain/quantifier clarifications, recompute manifests, and verify the root's accepted report/actual-output bindings. No new mathematical search or author turn is required for those changes. Any new theorem, expanded delay claim, priority certification, altered construction, changed preserved artifact, or new publication action would exceed that bounded recheck and require fresh review of the changed scope.

## Exact remaining gap and stopped routes

There is no remaining mathematical gap in the accepted slow-tail counterexample, all-scale implication, elementary log-tail proof, original lacunary construction, or tail irregularity. The remaining gap is documentary finalization and evidence binding before remote mutation. Historical priority of the specific construction and any prior explicit announcement of the later named question remain unestablished, intentionally outside the accepted claim. Classification of all infinite-mean laws and adjacent relative-age/joint/coupling questions remain outside scope.

No Git mutation, remote write, external communication, release, DOI operation, or packet edit was performed by this reviewer. Work is confined to priority_correction_review. The local primary PDF and scratch renders are evidence, not proposed public contents.

Source links: [Thorisson indexed primary preprint](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf); [Thorisson publisher metadata](https://link.springer.com/article/10.1007/s11134-011-9241-2); [Erickson DOI](https://doi.org/10.1090/S0002-9947-1970-0268976-9); [Angus-Ding deposited metadata](https://api.crossref.org/works/10.1016/j.spl.2020.108745); [Blanchet-Glynn-Thorisson primary record](https://arxiv.org/abs/1503.08374); [Bingham-Goldie-Teugels publisher metadata](https://www.cambridge.org/core/books/abs/regular-variation/contents/92ABC242FEBEDE566EA28EA26351D63B).

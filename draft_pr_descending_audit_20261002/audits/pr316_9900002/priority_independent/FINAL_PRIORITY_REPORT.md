# Final independent historical-priority audit: PR316 / problem 9900002

Closed 2026-10-04, UTC. Completion: 100% of this bounded audit; historical first-priority certification is not achieved. All scientific conclusions below follow from the sources and derivations identified here, not from the root's adjudication or other fresh review families.

**Recommendation:** treat the universal negative existence claim as **classically implied / already settled at the level of mathematical consequence**, with the explicit qualification that no earlier author announcement of a solution to the later-named Thorisson Problem1.2 has been authenticated. Do not promote the universal negative answer as a certified novel theorem on this evidence. The precise lacunary construction is a separate contribution whose first priority remains unverified.

## 1. What is being compared

The primary Thorisson preprint's indexed Section1 defines a delayed renewal process with independent nonnegative delay, independent identically distributed strictly positive recurrence times, a non-lattice law in the sense P(X in dZ)<1 for every d>0, and infinite mean. Its full interval length is D_t=X_{N_t}=A_t+B_t with N_t=inf{n>=0:S_n>t}. Problem1.2 asks for a nondecreasing deterministic scale giving a nondegenerate distributional limit of D_t/phi(t), and specifically proposes E[min(X,t)]. Zero delay is allowed.

The exact negative target is ONE allowed, finite-a.s. interarrival law for which EVERY positive finite eventual deterministic nondecreasing scale fails to give a proper finite nondegenerate full weak limit. A result excluding all positive deterministic scales also suffices. Failure under time normalization, a particular truncated-mean scale, or an age/total-life ratio does not suffice. Finite mixed limits with mass at zero must be excluded.

Primary statement evidence is the web-indexed text of the [UBA institutional preprint](https://cms.dm.uba.ar/depto/public/Some%20Open%20Problems-preprint.pdf), Section1, indexed pp.1–2; publisher identity is [Thorisson, Queueing Systems68,313–319(2011), DOI10.1007/s11134-011-9241-2](https://link.springer.com/article/10.1007/s11134-011-9241-2). The UBA index labels the preprint2010, the publisher gives online1July2011, and the institution record gives issueAugust2011. These are different publication stages. No full Thorisson binary or visual page has been obtained; no line-by-line preprint/published equivalence is claimed. Finite-a.s. real-valued recurrence times are implicit in the indexed source's random-variable setup, rather than an independently printed finiteness clause; both examples below satisfy finiteness explicitly.

## 2. The strongest verified historical implication

Put r(t)=P(X>t), U(t)=sum_{n>=0}P(S_n<=t), and take zero delay. Erickson's1970 Theorem5, printed pp.265–266, includes the regular-variation boundary alpha=0 and gives U(t)r(t)->1 when r is slowly varying. This differs from the local strong-renewal assertions whose abstract highlights positive alpha. The alpha=0 convention is explicitly present in equation(2.2).

The old premise plus an elementary exact renewal identity entails the whole required obstruction:

\[
P(D_t>x)=r(x)U(t)\qquad(x\ge t).
\]

For every fixed K>=1, slow variation gives P(D_t>Kt)->1. Thus any tight normalized family D_t/phi(t) requires phi(t)/t->infinity, even when phi oscillates. Thereafter, for all fixed a,b>0,

\[
P(D_t>a\phi(t))-P(D_t>b\phi(t))\longrightarrow0.
\]

Tightness forces those tails to vanish, so every tight normalization tends to zero in probability. Therefore **every proper finite weak limit is delta_0**, and no nondegenerate one exists. No monotonicity assumption is used. All positive scale regimes, possible atoms at zero, and escape to infinity are covered.

The complete proof, endpoints, hypotheses, an equivalent tightness criterion, and boundary examples are in [SLOW_VARIATION_COROLLARY.md](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr316_9900002/priority_independent/SLOW_VARIATION_COROLLARY.md). A fresh history-free adversary independently confirmed the conditional theorem; its entire report was read and its hashes checked in the proper directory. The adversary used the asymptotic as a supplied premise and performed no bibliography audit.

An explicit continuous law with r(t)=1/(1+log t) for t>=1 satisfies every source assumption. The companion note gives an elementary first-large-increment proof of U(t)r(t)->1 for this law, so the exact negative answer has an independently checkable proof even without the old article. Its proposed truncated-mean scale fails along the full limit.

This is a current explicit deduction of a statement entailed by old mathematics. It is not evidence that Erickson or any other earlier author recognized or published the later exact all-scale question.

## 3. Three priority propositions, kept separate

| Proposition | Independent assessment | Exact remaining gap |
|---|---|---|
| A classical1970 premise entails a negative answer to the all-scale total-life question | Verified, with a complete additional proof. There is also an elementary admissible logarithmic-tail example. | General old premise obtained as an original article scan on a public mirror, not an authenticated official-host binary; explicit example removes that dependency for correctness. |
| An earlier author explicitly resolved Thorisson Problem1.2 | Not authenticated. No read primary passage states that exact later-named result or announcement. | Inaccessible/incompletely inspected sources and non-exhaustive literature coverage; first-explicit-solution credit remains undetermined. |
| The submitted lacunary atomic construction itself was already published, or is first | No verified exact predecessor located. First priority is not certified. | Need comprehensive construction-level predecessor comparison; absence of a located matching example does not prove originality. |

Operationally, if the project's already_solved category includes conclusions that are straightforward consequences of established theorems, it applies to the universal existence question with the qualification in the first paragraph. If that category instead requires a prior explicit publication announcing the exact solution, this audit does not establish that stricter criterion. The wording “Erickson solved Thorisson Problem1.2 in1970” is unsupported. “The negative answer follows from a classical index-zero renewal theorem by the displayed all-scale argument” is supported.

## 4. Comparison with the original candidate

The released TURN_1.md was read completely, independently of later review reports. It constructs

\[
p_n=2^{-2^n},\qquad a_n=2^{4^n},
\]

with the remaining probability assigned to Uniform[1,2]. For inspection times t_n=a_n/2, the first interval of length at least a_n has length a_n with probability p_n/q_n->1, and its start occurs before t_n with probability tending to1. The displayed error bound implies P(D_{t_n}=a_n)->1. Proper weak convergence under any deterministic positive scale would then force a point mass, by tightness and concentration at deterministic values. This mechanism excludes all scales without requiring a renewal limit theorem. The candidate also directly rejects the suggested truncated-mean scale.

The prior slowly varying route does not contain the candidate's law as a special case. For its survival function,

\[
r(a_n/2)=q_n,\qquad r(a_n)=q_{n+1},\qquad
r(a_n)/r(a_n/2)\to0.
\]

No finite regular-variation index has a zero limiting doubling ratio. The candidate's interval-length concentration on a single atom at selected deterministic times is materially different from scale-insensitive slowly varying tails. This distinction preserves possible value of an explicit nonregularly varying example, but does not establish novelty of its construction or the standard first-large-increment technique.

TURN_1 itself expressly makes no historical-priority claim. Its broad title/negative-existence conclusion should not be counted as a certified new resolution without the classical implication qualification. The narrower construction can be assessed separately, with priority still open. No candidate, queue, repository, PR, branch, or publication was changed in this audit.

## 5. Verified primary-source scope and page coverage

Primary-host links are provided even where the successful artifact was a mirrored copy; failures are not concealed.

| Source and date | Actual accessed evidence / inspected pages | What it supports, and what it does not |
|---|---|---|
| [Dynkin1955, Izv.Akad.NaukSSSR19:4,247–266](https://www.mathnet.ru/eng/im3572), received29April1954 | Complete20-page primary MathNet PDF; substantive OCR read on247–250; visually inspected247 and249. | Defines age, residual and total life. On249, c(kx)/c(x) must have finite nonzero limits for every k>0, with eventual continuity: regular-variation normalizers. Theorem2 is about residual life; Theorem4 includes total life under x normalization. It is not arbitrary scale exclusion for total life. |
| [Lamperti1958, Some Limit Theorems for Stochastic Processes, J.Math.Mech7:3,433–448](https://www.iumj.indiana.edu/IUMJ/FTDLOAD/1958/7/57027/pdf) | Complete primary16-page PDF; all pages OCRed; visually verified436,439,440; relevant continuous-time extension read by OCR on445–446. | Age/time iff condition, joint age/residual time scaling, total-life/time law. “Suitable normalization” in the nearby footnote refers to the counting variable. No arbitrary-total-life-scale assertion verified. |
| [Lamperti1961 Stanford report, An Invariance Principle in Renewal Theory](https://purl.stanford.edu/nn078xw6398) | Complete primary19-page scan. Viewed two cover/title pages, undated postscript, body pp.1–2 (PDFpages1–5). | Cover31May1961; current scan includes a postscript citing a June1961 thesis. Verified introduction concerns age/time and an invariance principle under0<alpha<1. The full report was not exhaustively visually read. |
| [Lamperti1962, Ann.Math.Stat33:2,685–696](https://projecteuclid.org/journals/annals-of-mathematical-statistics/volume-33/issue-2/An-Invariance-Principle-in-Renewal-Theory/10.1214/aoms/1177704590.pdf) | Complete primary12-page scan; visually read685–687,695–696. | Fixed-time age normalization and process invariance under regular variation. No exact all-scale total-life obstruction on inspected pages. |
| [Lamperti1961, A Contribution to Renewal Theory, Proc.AMS12:5,724–731, DOI10.1090/S0002-9939-1961-0125663-5](https://doi.org/10.1090/S0002-9939-1961-0125663-5) | AMSPDF403; JSTOR route HTMLchallenge; [Stanford primary report metadata](https://statistics.stanford.edu/technical-reports/contribution-renewal-theory) only, identifying reportLAMNSF5,September1960 and physical library access. | Bibliographic lead only. Theorem scope not authenticated. Distinct from the1961/1962 invariance paper. |
| [Erickson1970, TransactionsAMS151,263–291, DOI10.1090/S0002-9947-1970-0268976-9](https://doi.org/10.1090/S0002-9947-1970-0268976-9) | Official AMSPDF403 and webpage internal error. Complete original29-page article scan from public Researcher.life artifact host; embedded AMS copyright/footer. Text extracted; visually verified265–267 and286; title/date263 read from extraction. | Theorem5/equation(2.2) explicitly supply the index-zero renewal premise. Printed286 separately describes Dynkin's regularly varying normalization necessity for age/residual life. Neither inspected passage states our arbitrary-normalizer total-life corollary. PublicationSeptember1970; received4October1969. No official-host byte comparison available. |
| [Blanchet–Glynn–Thorisson arXiv1503.08374](https://arxiv.org/abs/1503.08374) | Complete primary3-page PDF text read. Primary submission29March2015; current retrieved body date10November2021 while margin stillv1/2015. | Ratio A_t/D_t under an eventually regularly varying density and0<alpha<1. This differs from deterministic scaling of D_t. Do not infer exact historical theorem version from conflicting internal dates. |
| [Kabluchko–Marynych2016, TheoryStoch.Proc21(37):2,14–21](https://tsp.imath.kiev.ua/files/2120/art2120_03.pdf), [arXiv1605.02659](https://arxiv.org/abs/1605.02659), submitted9May2016 | Complete primary8-page journal PDF and author preprint; extracted texts read in relevant portions; visually verified journal17 Theorem2.4; journal15 statement read in extraction. | Nonlinear scaling of renewal epochs with slowly varying tails. Printed15 attributes arbitrary affine-normalization degeneracy for sums S_n to Darling1952; that is a different observable. Neither inspected result explicitly states the all-scale obstruction for D_t. |
| [Angus–Ding2020, Stat.Prob.Lett162,108745](https://www.sciencedirect.com/science/article/abs/pii/S0167715220300481), DOI10.1016/j.spl.2020.108745 | Primary publisher indexed abstract, introduction and concluding scope; full PDF not acquired. [JMM primary abstract](https://jointmathematicsmeetings.org/amsmtgs/2247_abstracts/1163-60-624.pdf) indexed text, received10September2020. | Ratio current age/total life for indices0<=alpha<=1, including degenerate0 atalpha0. Claim of answering a Thorisson problem is explicitly qualified to that ratio. July2020 article number is108745; historical SOURCE_GATE's108747 is erroneous. No all-normalizer total-life solution authenticated. |
| Darling1952, The influence of the maximum term in the addition of independent random variables | Exact AMSPDF route attempted and returned403; no substantive original paper acquired. Its scope here is only the attribution in the read primary2016 paper. | Do not transfer its asserted sums result to total life without proof; not a directly verified original theorem in this audit. |
| Recent RWTH institutional thesis, Renewal processes with random time | Primary-host indexed ratio discussion surfaced; native official PDF route returned248-byteHTML with200status. No full source/metadata date authenticated. | Search lead only; not used as theorem or priority evidence. |
| Cambridge extreme-renewal-process paper | Primary publisher page opened at first stage; no substantive full theorem audit. | Unclosed lead, not accepted evidence for or against priority. |

The table states page coverage, rather than claiming full visual/source access from obtaining a binary. Other primary records and indexed text are retained in numbered evidence files.

## 6. Independence chronology and exposure disclosure

The source-first stage read only parent SOURCE_FIRST_CRITERIA.md and source_inputs/problem_payload.json locally. That criteria file contained prior-source cautions, which were not treated as accepted mathematical conclusions. Primary research preceded any candidate reading.

SOURCE_ONLY_FIRST.md was content-frozen at14:42UTC, together with its24-file manifest. Root reported verifying all pins at2026-10-04T14:43:06.174466Z and explicitly released candidate reading. The first-stage report and manifest bytes have remained unchanged. Their original hashes are respectively:

- e9b3ceb53a44b9177ce4744e37a218011c3580fbdea9fbad08d917541026f537
- 776a00b7f75a506f628fafa5e2f2b26c58fc9747a43a2c184742b29ca2c79a20

After release, I read only the original historical TURN_1.md and SOURCE_GATE.md. I did not open later preprints, original other-family review files, the root's new scientific conclusions, queue material, or other chats.

Root supplied an explicitly labeled slowly-varying-tail PRIORITY HYPOTHESIS. I independently derived the all-scale implication and sent it to root before finding the old theorem's precise page support. This was a directed hypothesis check, not a blind independent discovery of that route.

**Incidental limitation:** around14:52UTC I called collaboration.list_agents solely to check capacity before a fresh adversary. The response unexpectedly included completed fresh-family final summaries, including normalization and renewal PASS summaries. I could not unsee them, immediately disclosed the exposure to root, and did not open those families' files or rely on their conclusions. My source-only freeze and the independently sent slowly-varying derivation predated the exposure. The subsequently spawned fresh slow-tail adversary received no conversation history and only the stated corollary/premise.

Root later informed me a different fresh reviewer recommended an operational already_solved category. That unsolicited review summary was received after my core conclusion; it is advisory context, not evidence supporting this report. My recommendation follows the displayed proof and independently read old-source pages. Root's adjudication remains separate.

## 7. Evidence, failed accesses, and audit limits

The evidence directory preserves full substantive returned web outputs, downloaded originals, extracted text, viewed page images, the historical submitted inputs, and native download results with actual timestamps/statuses/errors. Numbered records001–008 belong to the unchanged first freeze;009–036 document subsequent work. Native programs are saved alongside the reports. The first report lists exact first-stage queries; late028/030/033 files include exact request arguments. Some middle web captures preserve the complete returned outputs but not a separate literal request object; the corresponding tool calls remain in task history. No claim of a filesystem-only reproduction of every middle search input is made.

Preserved failed actions include the native original-source SSLhandshake timeout, Springer HTMLredirect, AMS403s, JSTORHTMLchallenge, one actual Windows1252/UTF8 decoding failure with correction, RWTH200HTMLresponse, and an adversary checksum invocation from the wrong working directory. That invocation was corrected: the proper directory verified both hashes. It is not evidence the agent report changed. Internal web-open failures are preserved as returned.

Record027's manually entered UTC label is approximate, not an exact captured call time; native timestamps and late tool-clock records supply actual times. Research-log timestamps explicitly use minute/range precision when an exact time was not captured.

Remaining documentary gaps are exact earlier publication of the all-scale corollary, construction-level predecessors, inaccessible1961 Contribution and1952 Darling originals, full2020paper, complete Stanford-report inspection, full Thorisson source binary, and non-exhaustive current literature/citation coverage. These gaps prevent a first-priority certificate; they do not invalidate the complete elementary all-scale proof. Absence of a found predecessor is not absence of all predecessors. No outside contact, outreach preparation, or publication occurred.

The final freeze receipt and manifest record actual permission changes, including644->444 where applicable. Every first-stage pin is reverified before closure. This freeze is local evidence preservation, not publication.

# Independent priority audit: BKV and contact-process literature

Authored 2026-10-12 UTC for PR262 / problem30005044 / OWR-9790363-003. Research attribution: Alec Kriebel, ORCID https://orcid.org/0009-0001-9320-500X. This is an internal audit artifact. No external individual communication, provider mutation, publication, branch change, commit or push was performed.

## Disposition

**HOLD for novelty, firstness, or present-day openness; conditional GO for a bounded, explicitly credited quantitative/expository note.** The central existential result is a valid short corollary of the existing BKV growing-degree infection-ray proof. The published proposition states global survival, not simultaneous finite-time explosion. It is nevertheless insufficient credit to describe BKV only as a related survival method. The timing and recovery argument is written out in [BKV_PROOF_IMPLICATION.md](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/BKV_PROOF_IMPLICATION.md) and independently adversarially verified in [timing_adversary/REPORT.md](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/timing_adversary/REPORT.md).

The candidate's deterministic horizon, concrete offspring law, chosen degree thresholds, and numerical lower bound are not stated in the sources examined here. That bounded observation does not establish novel quantitative content. A note can accurately present an explicit construction illustrating the historical existential question, with prominent acknowledgment that existence follows from BKV's prior mechanism and a short timing addendum. Do not call it a new solution mechanism or certify that the question remained open until this construction. Almost-every-tree positivity for all positive rates is also a routine hereditary and monotonicity consequence once annealed explosion is established.

The full-body gap for Valesin's 2024 book was closed after the mechanism comparison was independently frozen. A whole-body Pemantle–Stacey 2001 retrieval gap remains; primary-indexed material indicates a bounded-degree setting, but it is not a full-paper absence certificate. No essential unresolved body is silently treated as read. Broader priority clearance stays HOLD; the positive BKV derivability finding does not rely on that missing body.

## Inputs and independence

The root acceptance receipt SHA256 is `542f4233d8d696fe9804a42120b1c2e3e9cd164ed85c785d349544edd105bf13`. It accepted mathematical and original-source scope, not priority. The frozen scoped candidate v02 manifest SHA256 is `3bad9b517356b93a5339c776ebfde1825492b21c171d881f06c67946897fcea8`. I read actual AGENTS.md, PROOF.md, TARGET.md, SOURCE_GATE.md, source_manifest.json, and preserved historical source claims as historical only. Input paths and hashes appear in [INPUT_MANIFEST.json](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/INPUT_MANIFEST.json).

The BKV proof implication was authored before any other priority-family report was read and frozen in [INDEPENDENCE_FREEZE.json](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/INDEPENDENCE_FREEZE.json). The two delegated readers were my own distinct full-manuscript and timing-adversary subtasks. Their assigned scopes were deliberately separated. After this freeze, Root supplied a primary Valesin-book file path from another family's folder; I copied and rehashed the body and read it independently. I did not inspect that family's report or adopt its interpretations. No other priority-family report was read for this audit.

## Exact claim being compared

The candidate uses a Galton–Watson tree with finite positive integer offspring and tail
\[
P(\xi\ge m)=m^{-1/4},\qquad m\ge1.
\]
Each realization is locally finite, is infinite without conditioning on nonextinction, and has infinite offspring mean. The process starts with only the root infected. Ordered edge arrows have rate \(\lambda\), recoveries rate 1, all independently. Infection at a given vertex/time means existence of a finite root-originating graphical infection path, equivalently the increasing coupled finite-ball construction. It asserts
\[
P\{|X_{1/(2\lambda)}|=\infty\}\ge(7/30)e^{-3/(2\lambda)}
\quad\text{for every }\lambda>0.
\]
The candidate also asserts that on one full-measure set of trees, every positive rate has positive quenched probability of explosion at some finite time. That time and probability may depend on the tree and rate. Finite fitnesses \(F_v\ge1\), with arrows \(\lambda F_uF_v\), inherit the assertion by graphical monotonicity. No uniform quenched deadline, probability-one graphical explosion, uniqueness of an explosive extension, or universal classification of infinite-mean offspring is claimed.

Printed OWR 2022 p619 asks whether explosion can occur when the offspring mean is infinite. It is an existential question. Its model on p618 admits constant fitness 1 because the fitness law is supported on \([1,\infty)\). The historical question is not a claim that every infinite-mean law must explode. The adjacent discussion of closing mixed-moment gaps and weakening the fitness lower bound concerns additional questions; answering this existential subquestion does not answer all of them. I independently read printed pp618–620 (PDF pp42–44). The printed p618 moment descriptions have reversed inequality signs compared with the later published paper; this does not alter the p619 explosion question and should not be copied as a current theorem.

## BKV: actual published body and chronology

The fresh published primary PDF, *Degree-penalized contact processes*, Forum of Mathematics, Sigma 14 (2026), e6, DOI [10.1017/fms.2025.10144](https://doi.org/10.1017/fms.2025.10144), has 85 pages and 1,386,512 bytes. SHA256:
`320fea7622aadb9658130c5ebad7dba12bef171bbf379400c625f45c19f59922`.
A local copy and an independent publisher fetch have identical hashes. This is not the unreproduced historical submitted hash `63b61b351c86d9f9c43be90063838090de065fb34bb956c5b0107a4d6bba2700`. No content identity or historical full-reading inference is made between those versions.

The primary Crossref record reports online publication on 2026-01-15; the PDF gives receipt on 2024-02-20 and revision/acceptance on 2025-09-01. Its bibliographic year is 2026. The arXiv primary record lists v1 on 2023-10-10 at 22:00:22 UTC. I independently pinned the 71-page v1 and read its complete essential pp38–41; it is not byte-identical or page-identical to the journal body. Chronology is bounded to the actual versions and records inspected, not a claim about the earliest private knowledge or all talks.

**Honest full-read boundary.** I personally read all of fresh journal pp1–18,45–48,82–85 in nontruncated outputs, rereading pp4–5 after a truncation. I visually inspected full pp17,46–48. My delegated remaining-pages reader fully read pp19–45 and49–82 in twelve complete nontruncated chunks and inspected 23 rendered pages for formula disambiguation. The union is all 85 pages, with overlaps at 45 and 82. This is a collective full read, not a claim that I personally reread every peripheral proof. Extraction alone was not counted as reading. The delegated section-level report records author-omitted proofs and references that were not themselves read.

### Published statement, immediate corollary, and additional quantification

Definition 3.1 and equation (19), p17, use finite infection paths; the surrounding text expressly allows finite-time explosion. Definition 6.1, p46, removes upward arrows to create a down-directed process dominated by the original one. Proposition 6.2, pp46–48, states positive global survival for weak-power-law offspring exponent \(\alpha>0\), positive offspring, and max penalty \(f(x,y)=\max(x,y)^\mu\), when \(\alpha+\mu<1\), for every positive rate and almost every tree.

The section introduction is aimed at \(\mu\in[1/2,1)\), but the **published proposition and its proof do not impose that lower restriction**. With the paper's nonnegative penalty convention, \(\mu=0\) is directly included. The 2023 v1 proposition explicitly imposes \(\mu\in[1/2,1)\). Even under that narrower version, the candidate is covered at \(\mu=1/2\), since \(1/4+1/2<1\); the classical process dominates that penalized process. Thus a possible objection based only on the section heading or the old lower bound on \(\mu\) does not restore novelty.

BKV find eligible children with offspring in \([L^{s_1},L^{s_2}]\), \(1<s_1<s_2\), and at least a constant times \(L^\gamma\) such children, where
\[
\gamma=1-\alpha s_1-\varepsilon s_1>0,
\qquad \delta=\gamma-\mu s_2>0.
\]
The total eligible-arrow rate is at least \(c\lambda L^\delta\). Their selected ray has offspring at least \(K^{s_1^m}\), with summable count/race failure probabilities. Their instruction to choose any child infected before the parent recovers permits the first eligible arrow.

The precise extra argument is small but necessary. Let \(W_m\) be that arrow wait and \(H_m\) the independent rate-one recovery wait. On stage success \(W_m<H_m\),
\[
E[W_m1_{\{W_m<H_m\}}\mid\text{selective past,rates}]
=R_m/(R_m+1)^2\le1/R_m.
\]
Zeroing failed-prefix contributions and using \(R_m\ge c\lambda K^{\delta s_1^m}\) gives weighted summability
\[
\sum_m(m+1)W_m<\infty
\]
on the positive-probability infinite successful ray. Hence arrival times converge to a finite \(S_\infty\).

Cumulative infection alone is not the final conclusion. The unused recovery residuals \(H_m-W_m\), conditioned on the **selective ray skeleton**, are iid exponential variables of mean one, independent of the successful waits and winners. Future ray steps use fresh descendants and never reveal these parent residuals. Conditioning on the full contact-process history instead would destroy this assertion; the source-compatible first-arrow exposure is material. Since
\[
\sum_m(S_\infty-S_{m+1})=\sum_{j\ge1}jW_j<\infty,
\]
conditional Borel–Cantelli leaves all but finitely many ray vertices infected simultaneously at \(S_\infty\). Each endpoint is reached by an ordinary finite infection path; an infinite path ending at a vertex at infinity is not used.

For a deterministic \(h>S_\infty\), the independent residual-survival probabilities are at least \(e^{-h}\), so infinitely many ray vertices are also infected at \(h\). A countable union over integer horizons produces some deterministic finite \(h\) of positive annealed probability. Large \(K\) can force a positive chance of passage before a prescribed positive horizon; BKV's unstated constants do not yield the candidate's displayed numerical lower bound.

The almost-every-tree explosion assertion requires its own short step, rather than an appeal to the global-survival proposition alone. Call a tree good when the conservative down-directed process (using degrees \(D_v+1\), including the root) has positive probability of finite-time explosion. A good child subtree makes its parent tree good by infection across a finite bridge with positive probability and future independent graphical marks. If \(q\) is the probability of a bad offspring tree, then \(q\le E[q^D]\). Annealed positivity gives \(q<1\); positive offspring and \(P(D\ge2)>0\) force \(q=0\). A countable intersection over rational rates and monotonicity handles every positive rate on one full-measure set. Finite fitnesses at least one only add arrows. No uncountable intersection, uniform quenched time, or restart at an explosive stopping time is needed.

Restoring actual degrees \(D+1\) in the source's offspring-based rate display and rounding the noninteger eligible count changes only the constant \(c\), for example to \(2^{-\mu}/8\) at large \(K\). It does not change any positive exponent or summability. These bookkeeping repairs are not a substantive new mechanism.

**Conclusion:** the existing published proof itself, with a short explicit timing/memoryless addendum and elementary quenched upgrade, proves the same existential simultaneous-infection phenomenon in the candidate's class. It is not merely evidence of fast cumulative infection and not merely an abstract survival theorem. It does not state the candidate's exact deterministic lower bound.

### Other mechanisms in the full BKV manuscript

The full remainder materially rules out a mistaken alternative interpretation. Section 6.2 uses a single fixed large star size \(K\), fixed connecting length, and fixed positive time window \(T_K=\exp(c\lambda^2K^{1-2\mu})\). Lemma 6.8 obtains returns at times \(yT_K\to\infty\). That particular lower process has bounded degree and finite range at every finite time, as independently proved in the delegated report by pure-birth domination. Its local-survival conclusion is not explosion.

Sections4–5 provide BRW/counting extinction bounds. Local extinction at each fixed vertex is not one uniform extinction time for the whole graph; a divergent upper BRW expectation would not prove lower CP explosion. Sections7–8 are finite configuration-model metastability, with cutoffs/star sizes fixed before \(n\to\infty\); large finite populations and exponentially long survival do not establish infinitely many simultaneous infections on one locally finite tree. Peripheral literal formula slips and author-omitted external proofs are recorded in the full-read report; they are not used to manufacture a priority conclusion.

## Older primary mechanisms and citation chains

The machine-readable comparison is [IMPLICATION_MATRIX.json](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/IMPLICATION_MATRIX.json); the source pins and exact page-reading bounds are [SOURCE_MANIFEST.json](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/SOURCE_MANIFEST.json).

**Pemantle (1992), author archival arXiv body uploaded2004.** I read the introductory/model pages and the full relevant GW/star-return theorem body in the 41-page archive, using its archive pagination rather than falsely assigning the published 28-page pagination. Its Theorem 3.2 is a local-survival/star-support result with fixed-degree and return time constructions. Proposition3.1 is early source credit for the hereditary zero-one idea. Introductory p4 broadly says a finite initial population stays finite and explicitly declines a formal construction/proof; it is not a proved general nonexplosion theorem on arbitrarily rapidly growing locally finite trees. The known source-compatible explosion construction cannot be dismissed by importing that informal sentence as a universal theorem.

**Huang–Durrett (ALEA2020).** Theorem1.4 gives zero local-survival threshold under subexponential offspring. I read the essential introductory/star statements and the complete GW proof in Section3, printed pp172–176. The mechanism uses large fixed stars, repeated persistence and return, with fixed finite passage/return parameters. No summable-time construction appears in those read proofs. Even when an infinite-mean law can be handled by truncation/comparison, local survival remains a different predicate from finite-time simultaneous infection. Their oriented once-infected comparison also deserves antecedent credit, without being mislabeled an explosion theorem.

**Mountford–Valesin–Yao (2013; pinned arXivv2 dated2012).** The locally finite model and two-stage GW limit are read in pp1–8. The nonroot size-biased degree tail has exponent \(a-2\), including the heavy infinite-mean range. The complete first-infection/SIR branching calculation, pp14–15, counts vertices ever infected in each generation and proves global survival. It does not bound their common arrival deadline or remaining simultaneous infection. Its comparison process predates BKV and the candidate; however, the generation-survival calculation alone is not an immediate finite-time explosion theorem without further clock analysis. Root/nonroot laws and minimum-degree conventions differ from the candidate, so a precise extension is needed rather than equating the models wholesale.

**Linker–Mitsche–Schapira–Valesin (Annals of Probability2021).** I pinned the actual primary published 35-page body from an author's institutional host. The full lower-bound ray proof at printed1491–1492 (PDF12–13) repeatedly infects fresh higher-height/higher-degree vertices before recovery, with exponentially decreasing race errors. The graph is random hyperbolic, not an iid-offspring GW tree. Printed1507 (PDF28) explicitly reasons that finite-time escape infects infinitely many vertices and that residual lifetimes keep the process alive at later times. Thus both the general increasing-degree ray and the residual-life observation have earlier primary antecedents. The published theorem is a survival-probability/critical-exponent theorem in another graph class. I do not claim it directly states the candidate GW result or its explicit constants, nor that this audit separately completed every detail of a hyperbolic explosion theorem.

**Valesin (Ensaios Matemáticos40,2024).** After source assistance authorized by Root, the body was rehashed independently:115pages,1,615,572bytes, SHA256`20e356bfaf29386cf8eec007be1e673b333219b5a42dd6124acdce20a090603d`. Complete read pp20–23 give the locally finite graphical definition and expressly allow explosion from finite infection on rapidly growing graphs. This is a generic acknowledgment, not a specific GW theorem. Read pp77–85 develop first-infection/SIR survival bounds, credited to MVY2013. They use generation counts, not summable arrival-time bounds. The literal printed power-law display(5.2) has a sign issue: it divides by \(k^\alpha\) with positive \(\alpha\), incompatible with a probability mass; intended decay is independently established by the original MVY body and surrounding tail calculations. I do not silently cite the empty literal hypothesis as an exact theorem applying to the candidate. This is selected essential-page review, not a full 115-page review.

**Can–Schapira (2015).** The infinite-mean result concerns finite configuration graphs and full initial occupancy, yielding exponentially long survival/metastability. Read pp1–3 explicitly emphasize failure of the relevant local convergence in the infinite-mean regime. It supplies neither a root-only locally finite infinite-tree explosion statement nor an automatic transplantation from finite dense cores.

**Cardona-Tobón–Ortgiese (2021v1 and published2026).** I independently pinned/read model pp4–5 of v1 and published pp1–5,8–10. The original lower bound on fitness is1; the newer paper allows positive fitness and degree/fitness dependence, but still assumes finite offspring mean throughout. Its Theorem 3 (published p10) explicitly states nonexplosion under that finite-mean assumption and is outside the candidate's infinite-mean regime. Published fitness monotonicity supports the candidate's domination extension. The paper's survival/star conclusions must not be relabeled an infinite-mean explosion result, and its present finite-mean assumption is not proof that the historical infinite-mean question remains open.

**Jahnel–Lüchtrath–Mönch (WIAS3199,2025).** Independently pinned21-page primary institutional preprint and read all definitions/main results pp1–9 and references20–21. The main claims relate survival in local limits to metastability/finite-graph phase thresholds. The paper cites LMSV2021, Huang–Durrett2020, Valesin2024, and newer subcritical finite-graph work. No target theorem is asserted in the read main results. This is a recent citation-chain check, not full-paper proof verification or a proof of no newer explosion source.

**Pemantle–Stacey (2001) body retrieval.** Repeated author-host retrieval is403; Euclid responses are HTML challenges. Those bytes are stored as responses, not mislabeled PDFs. Primary search-indexed pp1563–1565 identify bounded-degree graph scope and refer to explosion at a single site for a BRW state space. That is not simultaneous infection on the candidate's unbounded-degree locally finite tree. Because I have not obtained/read the body, this remains explicitly limited evidence. No contact with authors was attempted.

## Credit and feasible scope

A reviewable note should say, in substance:

> The construction gives explicit constants for a power-law example illustrating the explosion question recorded in OWR2022. The existence phenomenon follows from the infection-ray argument of Bartha–Komjáthy–Valesin, Proposition 6.2 and proof, after adding a short timing and residual-recovery argument. We spell out deterministic windows and a numerical probability bound for the chosen offspring law.

This is proposed internal credit language, not a submitted or published document. Cite the actual journal version and, where chronological comparison matters, separately cite the 2023v1. Earlier SIR/growing-degree and residual-lifetime antecedents can be described through MVY2013, LMSV2021, and Valesin2024. Do not claim that those earlier survival theorems explicitly state the candidate's bound. The standard almost-every-tree upgrade can cite Pemantle's hereditary idea or be proved directly, and should not be advertised as an independently novel strengthening solely because it is absent from BKV's displayed annealed calculation.

A general new classification of all infinite-mean laws, a sharp quantitative lower bound, or a firstness claim would require materially more evidence than this audit provides. The explicit bound is a real checked mathematical statement under Root's acceptance, but priority value and publication significance remain separate decisions. No earlier theorem with exactly the displayed constant and deadline was found in the pages actually read; that is the strongest warranted negative statement.

## Evidence, reproducibility, and remaining gaps

[SEARCH_AND_READ_LEDGER.md](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/SEARCH_AND_READ_LEDGER.md) distinguishes full reading, lexical screening, metadata, failed retrieval, and unpinned search leads. Raw primary/search responses are retained locally; malformed quote searches were excluded from absence reasoning and properly formed final search requests were saved. The audit never treats search-engine nonreturn as proof of absence or survival as explosion.

[verify_locators.py](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/verify_locators.py) verifies primary PDF hashes/page counts, decisive textual locators, candidate source/receipt hashes, the collective page-read union, and admissible \(\alpha=1/4\) parameters both for \(\mu=0\) and \(\mu=1/2\). It records a geometric majorant for the weighted waiting-time series. This is a reproducibility control, not an automated proof of priority or a test of every published theorem. [LOCATOR_CONTROLS.json](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/LOCATOR_CONTROLS.json) records the replay result. [OUTPUT_MANIFEST.json](/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr262_30005044/initial_review_20261011/priority_contact_literature_20261012/OUTPUT_MANIFEST.json) freezes local authored outputs and source evidence.

Remaining gaps are bounded: the 2001 primary body is unavailable in this run; selected older bodies are not fully read; no exhaustive world-literature/citation database scan or newest-version absence certificate is possible from these searches; no original exact-bound novelty is established. These gaps keep broader priority GO withheld. They do not weaken the positively verified BKV proof corollary or the requirement for stronger attribution.

Completion estimate: **100% of the assigned bounded BKV/contact-family implication audit; case estimate55% remains a heuristic, with final case disposition owned by Root.** Priority clearance for a novel contribution is not achieved.

# Independent branching / explosive first-passage priority audit

Recorded 2026-10-12 UTC. Candidate: PR262 / problem30005044 / OWR-9790363-003. This family remained independent of every other priority-family output, including after its primary analysis was frozen. The adversarial verification of the bridge below is a separate mathematical task, not a priority-family convergence exercise.

## Bounded verdict

The candidate's qualitative affirmative example is an **elementary corollary of a published general theorem**, with a short contact-process coupling supplied in this audit. Specifically, Amini–Devroye–Griffiths–Olver (ADGO, Annals of Probability 2013) prove explosion for appropriate weights on plump Galton–Watson trees. Independent thinning to vertices having no recovery marks through a fixed horizon preserves plumpness. Exponential arrow waits satisfy the published criterion. Every reached retained vertex then has a finite graphical infection path and is still infected at that same horizon. This bridges the simultaneous-infection issue; an appeal only to cumulative epidemic explosion would not do so. [ADGO, version3](https://arxiv.org/pdf/1102.0950v3), reprint/PDF pp6–7, proof pp14–22.

**Classification:** old printed ADGO theorem + unstated elementary contact-process corollary proved here. This audit has not located an old printed theorem expressly stating the candidate's exact contact-process assertion. It also has not established that the coupling itself was never previously written down. Absence of a located exact statement is not novelty clearance. The qualitative existential answer should therefore receive established-theory/corollary credit, rather than be promoted as a new discovery.

The candidate's explicit estimate

\[
 \mathbb P(|X_{1/(2\lambda)}|=\infty)
 \ge {7\over30}\exp\!\left(-{3\over2\lambda}\right)>0
\]

is a separate, candidate-specific quantitative specialization. None of the fully read primary sources below supplies this constant, time, or exactly the tail \(\mathbb P(\xi\ge m)=m^{-1/4}\). That observation does **not** establish priority for the bound. The parent has already accepted the frozen candidate's mathematics/source gate; this family supplies the priority classification and a checkable alternative qualitative derivation.

A concise, credited historical-answer note is truthful if it explicitly presents the qualitative assertion as this standard corollary, credits earlier explosive branching/FPP mechanisms and contagious-period robustness, gives the direct proof and estimate as a concrete specialization, and makes no firstness or present-openness claim. This family does not recommend a research-novelty claim.

## Exact target and scope

The frozen law is almost surely finite positive integer offspring with \(\mathbb P(\xi\ge m)=m^{-1/4}\), \(m\ge1\). It has infinite mean, no leaves, no extinction, and produces a locally finite infinite rooted GW tree. Infection begins only at the root. Each ordered adjacent pair has an independent rate-\(\lambda\) Poisson arrow process; each vertex has an independent rate-one recovery process. The accepted minimal extension counts ordinary finite root-originating paths and is the increasing union of finite-ball processes. For \(F=1\), the target is a positive probability of infinitely many vertices infected **simultaneously** at a finite time, plus an almost-every-tree, every-positive-rate positive-probability conclusion at some finite time. Finite \(F\ge1\) comparison belongs to the parent-accepted model/proof.

The audit never assumes explosion of every infinite-mean law, a uniform quenched horizon/probability, dynamics probability one, or a unique continuation after explosion. The 2022 workshop question, printed in the report released in 2023, asks an existential “can” question. Its exact model/source acceptance was supplied by the parent receipt; current openness and firstness are not premises here.

Input pins (all were read):

| Input | SHA256 |
|---|---|
| Root mathematics/source acceptance receipt | `542f4233d8d696fe9804a42120b1c2e3e9cd164ed85c785d349544edd105bf13` |
| Candidate manifest | `3bad9b517356b93a5339c776ebfde1825492b21c171d881f06c67946897fcea8` |
| Candidate PROOF.md | `a6591115624a5b64a9199cddd8a278ebc51dbdde4d055cf904b9c54776d1e7dc` |
| Candidate TARGET.md | `732f684d428ff8814a8c738fae14dce8cb43da8a4ccc89f69c0403410a194c56` |
| Candidate SOURCE_GATE.md | `b0e64d0f47d4982160482366cfa0a39088e3ae6aa8cda410e853e752bf33171c` |
| Candidate source_manifest.json | `2541796644ebd73a067c91f8c6551ba5df3df8fa4e9722942ebcfea42abda793` |

The primary analysis was frozen at `2026-10-12T00:45:07.186558+00:00`, before any other priority output was read. Freeze markdown SHA256: `091fcc6091f80efe537fd9006cc5cd7a64f3ea7708664567cbfa915f872390cd`. The final derivation replaces the frozen informal \(h(n+1)\ge h(n)^3\) quantile estimate by the safely rounded \(h(n+1)\ge h(n)^2\); this strengthens the rigor without changing the summability conclusion. The freeze is preserved unchanged.

## Checkable fixed-horizon corollary

**Claim proved in the audit.** For the frozen law, every \(\lambda>0\) and every deterministic \(H>0\) satisfy

\[
             \mathbb P(|X_H|=\infty)>0.
\]

This annealed statement supplies the qualitative target at \(H=1/(2\lambda)\), but does not furnish the numerical lower bound. It uses only the printed ADGO theorem and elementary independent thinning, GW regeneration, and finite graphical paths.

### 1. Root conditioning and the retained offspring law

Let \(O_v\) indicate that the recovery process at \(v\) has no marks in \([0,H]\). Then \((O_v)\) are iid Bernoulli \(p=e^{-H}>0\), independent of the physical GW offspring and arrow fields. Work conditional on \(O_o=1\), which has probability \(p\). Retain the root and exactly the descendants whose entire root path has open labels.

For a retained vertex \(v\), its existence and open status depend on ancestors and \(O_v\), not on its own offspring count \(\xi_v\), its children's open labels, or their future offspring. Its retained child count is

\[
                  \eta_v=\sum_{j=1}^{\xi_v}O_{vj}.
\]

The unrevealed variables in this expression are independent between retained vertices when exposed generation by generation. The retained rooted component therefore has the **unconditioned** GW offspring law \(\eta\mid\xi\sim\operatorname{Bin}(\xi,p)\). The only initial conditioning is that the root is open; it does not size-bias the root's physical offspring or condition the retained component to survive. Survival conditioning is imposed later solely to apply ADGO.

The retained law is almost surely finite. For \(p<1\), \(\mathbb P(\eta=0)=\mathbb E(1-p)^\xi>0\), so it may become extinct even though the original physical tree never does. Also \(\mathbb E\eta=p\mathbb E\xi=\infty\). Positive survival can be seen without an infinite-mean technical shortcut: for some finite \(M\), \(\mathbb E[\min(\eta,M)]>1\); this bounded supercritical GW process embeds in the retained one. ADGO's theorem is explicitly conditional on survival, so positive extinction probability is allowed. [ADGO](https://arxiv.org/pdf/1102.0950v3), PDF p6, Equivalence theorem and Claim1.2.

### 2. Thinning preserves the heavy tail and plumpness

For integer \(m\ge1\), put \(k=\lceil2m/p\rceil\). Conditional binomial stochastic monotonicity and a Chernoff bound give

\[
\begin{aligned}
 \mathbb P(\eta\ge m)
 &\ge\mathbb P(\xi\ge k)\mathbb P(\operatorname{Bin}(k,p)\ge m)\\
 &\ge k^{-1/4}(1-e^{-m/4})\\
 &\ge (p/3)^{1/4}m^{-1/4}(1-e^{-m/4}).
\end{aligned}
\]

Indeed, \(kp\ge2m\), and \(k\le3m/p\). Thus \(\mathbb P(\eta\ge m)\ge m^{-1/3}\) for all sufficiently large \(m\), after absorbing a fixed positive constant. In particular, the plump condition \(\mathbb P(\eta\ge r^{1+\epsilon})\ge1/r\) holds with some \(\epsilon>0\) (for example \(\epsilon=1\) after rounding and increasing the threshold). This verifies the actual hypothesis; infinite mean alone would not.

### 3. Exponential FPP satisfies the printed criterion

On the retained tree, attach independent weights \(W_e\sim\operatorname{Exp}(\lambda)\). Choose ADGO's initial quantile threshold large enough. If \(h\) is large, the previous tail estimate yields

\[
 \mathbb P(\eta\ge\lceil h^2\rceil)
 \ge(\lceil h^2\rceil)^{-1/3}>1/h.
\]

Consequently \(F_\eta^{-1}(1-1/h)\ge\lceil h^2\rceil\), under the generalized quantile convention. The quantile recursion in ADGO Theorem1.3 therefore grows at least by squaring eventually. For \(h\ge2\),

\[
 F_W^{-1}(1/h)={-\log(1-1/h)\over\lambda}\le {2\over\lambda h}.
\]

Hence \(\sum_nF_W^{-1}(1/h(n))<\infty\). ADGO's Equivalence theorem and Theorem1.3 say that the weighted retained GW tree has a ray of finite total weight almost surely conditional on survival. This gives positive unconditioned explosion probability. [ADGO](https://arxiv.org/pdf/1102.0950v3), PDF pp6–7; definitions of explosion/FPP PDF p2; proofs PDF pp14–22.

For indexing, initialize \(h(0)=m_0\) and apply the recurrence for \(n\ge0\). The literal displayed statement on p7 says \(n\ge1\), leaving \(h(1)\) unstated; the recurrence recalled on p12 has no such restriction. This is an indexing omission, not a new theorem assumption. Strict tail slack and the rounded quantile estimate above avoid an equality-convention issue.

### 4. Positive probability before this exact horizon

Let \(V\) be the infimum of weights of infinite root rays, and set \(V=\infty\) on extinction. For **any** \(a>0\), \(\mathbb P(V<a)>0\). A direct proof avoids importing assumptions from a general CMJ process:

Suppose \(\mathbb P(V<a)=0\). Use the countable Ulam–Harris labels. For any label \(v\), conditional on its existence in the retained tree, its descendant offspring and downward weights have the original retained-GW FPP law, independent of the data establishing existence. Thus \(\mathbb P(v\text{ exists and }V_v<a)=0\). The countable union over all labels is null. But a finite-total-weight root ray, which has positive probability by step3, has tail sum tending to zero. At some descendant \(v\), that ray's tail has weight less than \(a\), so \(V_v<a\), a contradiction.

Apply this with \(a=H\) to the law \(\eta=\operatorname{Bin}(\xi,e^{-H})\). It is permissible that this law itself depends on \(H\): the argument is made after fixing \(H\), not uniformly over a varying model. General arbitrarily-fast explosion statements were already proved by Grey Theorem3 (Bellman–Harris setting) and Komjathy Claim2.3 (CMJ setting), but neither is needed for this regeneration proof. [Grey1974](https://link.springer.com/content/pdf/10.1007/BF00533364.pdf), printed p131 / PDF p3; [Komjathy2016](https://arxiv.org/pdf/1602.01657v1), pp11–12.

### 5. Adaptive arrow waits really are iid exponential FPP weights

Use only arrows directed from parent to child. Put \(t_o=0\) and, recursively at every finite generation, let \(t_{vj}\) be the first arrow time on \(v\to vj\) strictly after \(t_v\); set \(W_{v,vj}=t_{vj}-t_v\).

The unique tree path to \(v\) has finite length. Therefore \(t_v\) is a measurable function solely of finitely many ancestor/incoming-edge Poisson processes. It does not inspect the outgoing process on \(v\to vj\). Conditional on all previously exposed generations, the outgoing processes are independent Poisson processes; shifting their independent time origin to these arrival times gives independent \(\operatorname{Exp}(\lambda)\) waits with a conditional law not depending on the previous data. Induction over generations verifies joint iid exponential distribution for every finite edge collection, hence for the countable weight field. Conditioning on retained labels does not affect these arrows because labels depend only on recovery processes.

This construction is well-defined at every finite vertex even on explosion: each \(t_v\) uses a finite sum of finite waits. No global next-event enumeration and no infinite recursive arrival is required. Extra upward arrows or reinfections can only add legal paths; the lower process already supplies the needed paths.

### 6. Simultaneity and ordinary finite witnesses

On \(O_o=1\), every retained vertex \(v\) reached at \(t_v\le H\) has a finite path of downward arrows from \((o,0)\) to \((v,t_v)\). Every vertex on that path has no recovery marks in \([0,H]\). Extending the last vertical segment to \(H\) is therefore a legal finite infection path to \((v,H)\). It stays inside the finite ball of radius \(\operatorname{depth}(v)\), which is finite because the original tree is locally finite. Thus \(v\) belongs to the finite-ball contact process at \(H\), and hence to the prescribed minimal union.

If \(V<H\), a finite-weight infinite ray of weight less than \(H\) exists (or one may take a ray with weight strictly between \(V\) and \(H\)). Its infinitely many finite prefixes reach infinitely many distinct retained vertices before \(H\). **Each vertex has its own ordinary finite witness at the common horizon**. The infinite ray is a device for proving the presence of infinitely many such witnesses; it is never admitted as an infinite-jump infection path. Therefore

\[
 \mathbb P(|X_H|=\infty)
 \ge e^{-H}\,\mathbb P_{\operatorname{GW}(\eta),\operatorname{Exp}(\lambda)}(V<H)>0.
\]

This is the genuine bridge absent from a bare cumulative SIR statement.

### 7. Quenched eventual positivity and all rates

The candidate's weaker-in-time quenched statement can be recovered by a standard hereditary GW argument. Fix \(\lambda\), and call a physical rooted tree good if, for some positive integer \(N\), its conditional probability of \(|X_N|=\infty\) is positive. Step6 at \(H=1\) gives positive probability of a good tree. If a child subtree is good, so is its parent tree: force no recovery at parent or child on \([0,1]\), and at least one downward parent-to-child arrow there. This has positive probability \(e^{-2}(1-e^{-\lambda})\). At time1 the child is infected; the child's future subtree field after time1 is independent and has the original law. If the child has positive explosion probability at integer \(N\), prepend this finite initial transmission and dominate the process started from that child at time1. The parent then has positive probability of \(|X_{N+1}|=\infty\). This fixed-stage argument avoids any assumption that an arbitrary random explosion time can simply be replaced by an integer horizon.

Let \(b\) be the probability a physical tree is bad. Parent-bad implies every child-subtree bad, so \(b\le\mathbb E[b^\xi]\). Because \(\xi\ge1\) a.s. and \(\mathbb P(\xi\ge2)>0\), \(\mathbb E[b^\xi]<b\) for \(0<b<1\). Positive annealed probability excludes \(b=1\); hence \(b=0\). Intersect the full-measure sets for positive rational rates. Monotonicity under additional arrows extends the result to every real \(\lambda>0\). This yields positive conditional probability at some finite time, with no uniform quenched horizon or lower bound and no dynamics probability-one assertion. A closely related survival inheritance argument is printed in Valesin2024 Lemma4.4, pp64–65, but the explosion adaptation here is stated and proved explicitly. [Valesin2024](https://ensaios.sbm.org.br/wp-content/uploads/sites/8/sites/8/2024/12/em_40_valesin.pdf).

## Primary-source implication / counterimplication matrix

| Primary source and actual read scope | Exact process / explosion notion | Already established | Relation to candidate and exact gap |
|---|---|---|---|
| **Grey1974**, full9pp; printed129–137 | Bellman–Harris: individual lives for G-time, produces its entire family at death; independent family sizes/lifetimes. Number alive becomes infinite at finite time. | Theorems1–3 minimal fixed point and arbitrarily-fast explosion; Cor4.1 printed132 compares near-linear lifetime CDF to Markov explosion; Example2 printed135–136 power-law offspring. | Shows classical heavy-tail explosive branching is old. Its common-parent reproduction-at-death clock is not the iid per-child-arrow CP. Independent recovery is not built into this process. No direct CP embedding was established from Grey alone. |
| **ADGO2013**, full36pp reprint | Locally finite GW tree, iid nonnegative **edge** weights; finite-total-weight infinite ray. | Plumpness, explosion=min-summability conditional on survival, explicit quantile iff criterion, high-degree/minimal-weight path algorithm. | **Decisive:** exact iid exponential FPP input for the recovery-free retained tree. Qualitative simultaneous CP target follows with the audit's coupling above. No candidate time/probability constant supplied. |
| **Gulikers thesis2014 / arXiv2015v2**, full80PDFpp | Forward age-dependent epidemic with iid potential offspring D, independent transmission ages G, parent contagious duration C shared across siblings; count \(N^f(t)\) is the coming generation, not active infectives. | Theorems1.16–1.18 printed19 / PDF20: contagious periods preserve explosion under stated conditions. Theorem3.13 printed51 / PDF52: exponential transmission with power-law PGF and nonzero C. Proof1.16 printed50–51 controls a product along a finite-total ray. | Prior recovery/contagious robustness is explicit. Taking G=Exp(lambda), C=Exp(1) embeds the downward first-infection epidemic in CP before parent recovery, but its cumulative/coming-generation explosion alone does not prove simultaneous infection. Our independent whole-horizon thinning supplies that missing bridge. No exact candidate law/constant. |
| **Komjathy2016v1**, full41pp | CMJ iid reproduction point processes; Definition1.1 pp7–8 uses \(D(t)\), all individuals born by t. It explicitly leaves death unspecified. Example4.2 p18 puts births within parent's contagious interval. | Claim2.3 pp11–12 arbitrary-fast explosion; Cor4.19 p24 nonzero contagious period preserves power-law explosion; Theorem5.11(b) p28 independent binomial thinning preserves explosion, Remark5.12 plump extension. | Very close general mechanism and explicit thinning prior art. **D(t) is not the active infected set.** The audit proves simultaneity using a separate whole-horizon event. Do not label this preprint a journal publication without further bibliographic evidence. |
| **Iyer2024**, full13pp arXivv2; published ECP29 paper46 | General CMJ birth-time-labelled tree; inherited properties, infinite ancestral path at finite time. Applications to recursive trees with fitness. | Proposition3.1 pp5–6 conditional0–1 inherited properties; Theorem3.2/Cor3.3 pp7–8 sufficient criteria via summable time scales and expanding offspring; rates/fitness examples pp9–12. | Later continuation of explosive growing-family/ray techniques and standard inherited arguments. Does not contain independent CP recovery/active population. No located contact target or candidate bound. |
| **Lodewijks2026**, full16pp arXivv2; JAP63(3)1244–1262 | Pure birth CMJ in random environment, genealogy stopped at explosion. Main assumptions force individual infinite offspring; infinite stars or paths. | Theorem2.5 p4 infinite star; Cor2.7 p5 preferential-attachment criterion; comparisons with path theorem p6; proofs pp8–15. | Main infinite-star result violates candidate's a.s.finite degree. Path result concerns genealogy without independent recoveries. No direct CP implication. Retains ADGO and Komjathy as foundational citations in p16 references. |
| **Valesin2024**, partial context only: frontpp1–4,7; pp20–23,64–66 | Locally finite graphical CP; remarks on degrees growing rapidly and simultaneous infection. | Printed/PDF p22 expressly acknowledges finite-time CP explosion without excluding it. Lemma4.4 pp64–65 gives survival annealed-to-quenched inheritance. | Explicit prior discussion of the phenomenon, but the inspected remark supplies no GW example/proof. This is not clearance for an exact prior theorem or exhaustive review of115pp. |
| **van der Hofstad2017 draft**, partial context only: PDF1–2,136–139,154 | Survey/lecture derivation of Markov/Bellman–Harris/FPP explosion; citations to Grey, ADGO, Gulikers, Komjathy. | Printed128–131 exponential/quantile explosion discussion; printed146 epidemic interval citation chain. | Citation-chain context only; not the authority for the bridge. Some displayed survey claims overstate or mistype the cited primary criterion, so primary bodies control. No independent CP active-set theorem in inspected sections. |
| **Jahnel–Lüchtrath–Mönch2025 WIAS3170**, partial context only PDF1–6 | Spatial CP survival threshold; printed2 footnote discusses infecting a vertex of infinite degree. | Standard survival/percolation comparisons and a nonlocally-finite explosion observation. | Infinite-degree footnote is excluded by the candidate's local finiteness; survival at arbitrarily small rates is not finite-time simultaneous explosion. |

Important failed implications, each deliberately excluded:

1. Explosion of a **dominating** branching random walk does not imply explosion of the smaller CP. A lower embedded process is needed.
2. Cumulative epidemic explosion, a finite-weight transmission ray, or an infinite coming generation does not by itself imply an infinite active infected set at one time. The whole-horizon recovery-free coupling supplies actual finite witnesses.
3. Min-summability on a general tree does not imply explosion. ADGO pp4–5 give nonplump counterexamples; the plump hypothesis is verified rather than inferred from infinite mean.
4. Zero survival threshold or a heavy degree tail is not a finite-time explosion theorem.
5. A vertex producing infinitely many children at one time is not a locally finite physical-tree example.
6. Explosion probability one conditional on retained-tree survival is not probability one under the original contact dynamics.

## Chronology and credit

| Date / version | What the checked evidence establishes |
|---|---|
| 1963–1970 | Harris1963, Ikeda–Nagasawa–Watanabe1968/69, Savits1969, Sevastyanov1967/70 are cited by the fully read primary bodies. Their actual bodies were not obtained/read in this family, so earliest priority is **not** adjudicated. No claim they prove the contact corollary is made. |
| Received15Jun1973; publishedJune1974 | Grey's primary journal body supplies classic age-dependent/Markov explosion and power-law examples, including arbitrarily-fast explosion. |
| ADGOv1 4Feb2011, v2 11Jun2012, v3 14Jun2013; journal2013 | The exact printed general theorem used for the qualitative contact corollary: AnnProb41(3B)1864–1899, DOI10.1214/12-AOP806. Version history checked from arXiv metadata. |
| Thesis3Nov2014; arXivv1 12Oct2015, v2 23Oct2015 | Gulikers' cover and arXiv history establish contagious-period work preceding the workshop question. Version2 says references added. |
| Komjathyv1 4Feb2016; manuscriptdated5Feb2016 | General CMJ, contagious-interval and thinning results. Author publication list and later2026 primary references still identify an arXiv preprint; no journal claim made. |
| Draft12Jul2017 | van der Hofstad lecture draft already aggregates Grey/ADGO/contagious interval sources. |
| Workshop2022; reportpublished11Mar2023 | Historical source asks existential possibility for infinite mean; parent source gate supplies exact printed619 interpretation. Older general theories already permit the affirmative specialization through the audit's coupling, without asserting the question's current status. |
| Iyer arXivv1 21Dec2023; v2 19Nov2024; ECP2024 | Further explicit expanding-family/path and inherited-property mechanisms. Publisher PDF retrieval failed at one slug; arXivv2 full body recovered and fully read. |
| ValesinNovember2024 preface; Ensaios2024vol40 | Prior printed graphical-process discussion expressly recognizes simultaneous CP explosion on rapidly growing degrees, inspected p22. |
| WIAS3170 submitted29Jan2025 | Infinite-degree explosion and zero survival-threshold comparisons give boundary cases, not this local-finite theorem. |
| Lodewijksv1 27Nov2024; v2 19Jan2026; online13Apr2026; printSeptember2026 | Current inspected continuation of CMJ explosion, infinite stars and preferential attachment. Main model has no active recovery state. |
| BKV and original-model2026 revisions | Candidate source manifest/parent acceptance record these separately. This family deliberately did not read the other priority family's outputs or duplicate its exact BKV comparison. No result from that uninspected body is used to clear novelty. |

Recommended credit language, as a **possible future note** rather than an outgoing draft:

> The example is a concrete affirmative specialization of the historical existence question. Its qualitative conclusion follows from the plump Galton–Watson explosion criterion of Amini, Devroye, Griffiths and Olver through the recovery-free thinning coupling proved here. Earlier contagious-period robustness results of Gulikers and Komjathy provide related epidemic context. The direct graphical proof also gives the displayed quantitative bound.

This wording must accompany the actual coupling and the quantitative proof; it must not become “first solution”, “previously open”, or a claim that ADGO expressly printed the CP theorem. This report prepares no outreach to anyone.

## Search, retrieval, reading and reproducibility

`SOURCE_MANIFEST.json` lists all nine retrieved primary PDFs, precise URLs, byte counts, SHA256, text SHA256, absolute local PDF/text paths, actual full/partial read scopes and pagination notes. Six essential manuscript bodies were fully read: ADGO36pp, Komjathy41pp, Gulikers80pp, Grey9pp, Iyer13pp and Lodewijks16pp. This includes proofs, examples, discussion and references. Three longer/context sources were explicitly only partly read. No claim of full reading follows from bulk text extraction or text search.

`READ_LOG.md` distinguishes actual read chunks, extraction and search, and transparently records repaired truncated chunks in the80page thesis. `SEARCH_LOG.md` records the actual query families and limits. Raw returned search results are retained in `search_002` through `search_010` JSON files; the first search was not saved raw and is expressly reconstructed only from its actual query record. The Crossref title lookup is saved separately. Search results are discovery aids; substantive claims above rely on the actual primary bodies and the proved coupling.

Critical locators were visually checked from PDF page PNGs after text reads: ADGOp6/p7; Komjathyp8/p11/p18/p24/p28; GulikersPDF19/20/52/53; GreyPDF3/4/7; Iyerp7; Lodewijksp4; Valesinp22; WIASPDF4. `LOCATOR_MANIFEST.json` pins those image bytes, PDF pages, printed pages and textual needles. `verify_locators.py` checks pinned input hashes, source bytes/page counts, independently regenerated page extraction and those locators. It verifies provenance and locator reproducibility, not the mathematical truth of a theorem by string matching. The bridge proof and fresh adversarial verdict carry the mathematical verification.

## Remaining gaps and disposition

- **Exact prior contact-process statement:** not located in this bounded family. Do not turn this into a negative claim over the literature. Other independent families and parent integration may find one.
- **Earliest classical source:** not established; older works cited by Grey/ADGO/CMJ were not fully read. This does not affect the decisive published2013 corollary baseline.
- **Quantitative-bound priority:** not established. The inspected sources do not give the candidate constant, but bounded absence is insufficient for a novelty claim.
- **Recent uninspected bodies:** Iyer–Lodewijks2023 full61page body was only inspected through primary abstract/version metadata, not full-read; several2025/26 pure-birth/critical-immediate-offspring leads and a2026 TUM thesis listing were discovery leads only. No absence-of-contact-theorem conclusion is drawn from them. Essential inputs to the positive implication are all available and fully read, so no HOLD is needed for that corollary; a claim of exhaustive exact-statement priority remains on HOLD.
- **Adversarial verification:** completed by a fresh independent agent after a slot opened. `bridge_adversary/verification.md` proves the full fixed-horizon corollary and checks root conditioning, positive extinction and survival, quantile rounding, unconditioned descendant regeneration, adaptive iid arrow waits and simultaneous finite-path witnesses. It found no mathematical gap. Necessary wording safeguards have been incorporated here. The hereditary quenched extension in step7 is this family's separate elementary argument; the fresh verifier's assigned scope was the annealed fixed-horizon corollary.

No paper, PR, main branch, Git remote, DOI/Zenodo, provider, GWS or external-individual mutation was performed. All artifacts are private audit files within this family's dedicated folder. Research progress checkpoints are recorded in `RESEARCH_LOG.md`; a100% family estimate will mean completion of this bounded audit, not proof of a novel research contribution or exhaustive priority clearance.

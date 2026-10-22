# Independent priority and materiality review: PR280

Original head: `091bdecef6f84154f5d5c205a4b07eeb6391b8f8`. Review date:2026-10-21UTC. Assigned bounded audit:100% complete. This percentage measures work completed, not a probability of novelty.

**No verified earlier exact negative application was found. The2011 four-author body remains unrecovered. A new, checkable comparison shows that the qualitative full solution is a short consequence of earlier primary results. Accordingly, no new-construction, new-arithmetic, first-resolution, or current-unsolved claim is cleared by this audit. The exact application may be an unrecorded observation, but that historical point remains unresolved.**

## Exact2004 assertion

I independently read the complete two-page author version and visually checked its first page. Conjecture1 says: “The limit (1) exists for any bi-rational map L.” Its equation(1) weights uniformly chosen affine points, divides periods byp, and takes an ordinary prime limit. Suitable positive-density reduction primes precede that assertion. The genus-one discussion is a later heuristic; the single-reversing-family hypothesis is attached to a refinement; prime averaging belongs to a separately definedp²-scaled statistic. The candidate's forward map is polynomial, and forp=3mod4 its inverse is defined on every affine point, so it is a valid literal target comparison. [Original contribution](https://webspace.maths.qmul.ac.uk/f.vivaldi/research/Oberwolfach.pdf), [institutional report, pp2944–2945](https://ems.press/content/serial-article-files/45972?nt=1).

The exact candidate is

    L(u,v)=(u,(u²+1)v),
    D_p(x)=p^(-2) #{z : T_p(z)<=px}, p=3mod4.

The accepted quantitative claim is limsupD_p(x)=1 and liminfD_p(x)<=23/24 for each fixed1/2<=x<1. This review independently checks the qualitative nonlimit through the primary-result chain below; it does not replace the fresh full mathematical audits of the original quantitative proof.

## New exact comparison: all nontrivial inputs already available

The detailed derivation is in `CLASSICAL_COROLLARY_COMPARISON.md`. It adds a mechanism missing from the old hold record: a continuous empirical distribution forbids convergence on **any subset of primes of positive relative upper density**.

| Prior primary body | Exact relation to the candidate | What the body does not supply |
|---|---|---|
| Ostafe–Shparlinski, arXiv0902.3884v3 (14Mar2009), §2.1 equation(1) | Setm=1,a=1,b=0,g0=X1²+1,h0=0; exchange(X0,X1)=(v,u). This is exactlyL. | Their construction/degree-growth results do not state the ordinary cycle-CDF negative application. |
| Booker–Cohen–Sutherland–Trudgian, arXiv1803.01435v2 (22Mar2018), §2 equations(5)–(6), Lemma1 | TakeQ=t²+1,e1=1,e2=p−1. Their character-sum estimate already givesP_p/p=theta_p+o(1), whereP_p counts primitiveQ-values andtheta_p=phi(p−1)/(p−1). | No fixed birational map or OWR counterexample is discussed in these statements. |
| Deshouillers–Hassani, J.Austral.Math.Soc.93(2012), online16Jan2013, Proposition2.1 and equation(2.1),m=2 | Gives a continuous empirical distribution oftheta_p over odd primes, with underlying theorem credited to Kátai1968. | This is an empirical scalar distribution, not itself a theorem about the ordinary CDF of a fixed map. |

[Exact map family](https://arxiv.org/pdf/0902.3884v3), [primitive-value estimate](https://arxiv.org/pdf/1803.01435v2), [continuous scalar distribution](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/85266A1CBFB0DE0E70C723D2EDF847AB/S1446788712000250a.pdf/a-note-on-the-distribution-function-of-varphi-lowercase-p-1-lowercase-p-1.pdf).

Here is the complete short bridge. On each nonzero vertical coordinate the period isord_p(u²+1). For fixed1/2<=x<1, the only omitted periods arep−1, eventually. Thus

    D_p(x)=1−(p−1)P_p/p²=1−theta_p+o(1).

The Booker specialization gives explicitly

    |P_p−theta_p(p−1)|
      <=theta_p (2^omega(p−1)−1)(sqrt(p)+1).

Its nonzero-discriminant hypothesis holds. Q has no zero forp=3mod4;u=0 hasQ(u)=1 and does not contribute a primitive value, so its exclusion from the source's N(1,p−1) causes no discrepancy. The candidate's elementary2^omega(N)<=64N^(1/4) makes the erroro(p).

If theta_p converged toc along a prime subsetS with positive relative upper densitydelta, every fixed interval(c−epsilon,c+epsilon] would eventually contain all but finitely many theta-values fromS. The limiting total prime frequency of that interval would be at leastdelta. Continuity of the classical distribution as epsilon tends to zero gives a contradiction. This includesS={p=3mod4}, and any further positive-density thinning ofS. Consequently the qualitative full negative answer follows from the old results and these elementary identifications. The particular23/24 gap adds an explicitly coarse quantitative consequence of the old mean input.

This is a **new audit deduction from old theorems**, not evidence that a prior author published the final application. It also means that dressing up the density calculation as a new map or arithmetic mechanism would be misleading. There is no unsupported primitive-root conjecture or unsolved analytic step in this comparison.

## New retrieval/version work

The earlier coverage was read before selecting new routes. This audit did not simply repeat the prior62-query search. New routes included the complete HAL public surname-Viallet metadata response (413records), current LPTHE/QMUL primary author lists, Baake's current group/preprint pages and an actual2012 homepage capture, and bounded unlinked-origin filename probes. None recovered the2011 body. HAL/list omissions and404/503responses are not absence evidence. Exact URLs, HTTP outcomes and byte hashes are in `NEW_RETRIEVAL_RECEIPTS.json`.

New body comparisons closed or bounded additional leads:

- **Grammaticos–Halburd–Ramani–Viallet2009:** the [Newton institutional preprint NI09060](https://api.newton.ac.uk/website/v0/events/preprints/NI09060) was recovered (301053bytes, SHA256452479e1a0e2a93078c9de313463b6e433685b4d319182949a2ed01dd962fec0). Complete §4.6, printed34–35, discusses Hasse-Weil bounds and maximum/average orbit-length diagnostics. It does not state a period-CDF nonlimit. This is the41-page preprint, not an asserted identity with the30-page final version.
- **Llorens–Mañosa genus-zero paper:** independently read Proposition1, Theorem2/proof and context, PDF1–6. The normal formP_h(t)=(h,t),M_h(t)=(h²+1)t is routine in that framework. The read results concern real/complex Möbius dynamics and Lie symmetries, not varying-prime CDFs. The [returned arXiv version](https://arxiv.org/pdf/1502.03737v1) carries a2015v1 header but a2018 body date; it is not silently equated with the2015 final body.
- **Hutz–Patel:** [arXiv1710.07821v1](https://arxiv.org/pdf/1710.07821v1), Definition2.3, Proposition5.1 and Theorem5.3 require independent coordinate factors; L has a second coordinate depending onu. Their total-periodic-point/tail statistics do not specialize directly to the present period CDF. The2017preprint was read in the specified scopes; both2022publisher PDF endpoints returned a PDF Access Denied HTML page. The final22-page body remains unread.
- **Siu2019:** Theorem6.3.9 and context countphi(t)/2 parameter choices at a fixedp for a family of linear plane maps. This is not automatically the fixed planar map in the candidate; retaining that family's parameter as a coordinate increases dimension. Only the declared passages were reread here.

Complete read extents, exact version cautions, and source hashes are in `READING_RECEIPTS.json`. A download, keyword screen, or abstract read is not represented as a whole-body exclusion.

## The2011 manuscript: how material is it?

The strongest positive evidence remains actual-body citations: Roberts2011p220ref9, the [published NRV12](https://web.maths.unsw.edu.au/~jagr/NRV12.pdf) ref5, and [Neumärker2012](https://noah.nrw/ubbihs/download/pdf/5124915) p91ref63. I independently read the relevant2012introduction/conclusion and thesispp81–82. The thesis describes numerically observed distributions and work in progress. These passages support an experimental project in preparation, but do not inventory all of an unseen manuscript's theorems or later versions.

The candidate cannot be excluded from that project's broad subject merely by calling it triangular: G(u,v)=(u,1/v) satisfiesGLG=L^(-1) rationally. G has a pole onv=0, and L has extra commuting scalings; this distinguishes later full-affine/single-family positive theorems, but does not exclude every reversible-birational manuscript.

I challenge the strongest interpretation of the old hold. **Unrecovered access alone is not a logical reason to classify an explicit theorem as known, or to reject every adequate bounded novelty assessment.** No audit can infer worldwide absence from a finite search. The appropriate state is a disclosed, close, unresolved source/version lead. Conversely, the2012experimental wording does not justify declaring its contents irrelevant. The gap is material to any unqualified first-resolution or historical-current-open claim.

The novel-contribution issue now has an additional concrete basis beyond missing access: the complete qualitative conclusion follows through the short old-result bridge above. A genuinely new question application can sometimes be a contribution, even when elementary, but **this audit has not established that historical application novelty**. It would be improper either to claim novelty because the final sentence was not found verbatim, or to assert prior publication because the audit can synthesize it.

## Verdict and exact remaining gap

- Bounded audit and source comparison:complete100%.
- Earlier exact target-negative theorem located:false.
- All original construction/arithmetic novelty:rejected; precise attribution required.
-2011body/version history:unrecovered and unresolved.
- Exact application novelty:neither established nor falsified by a located prior application.
- First-resolution/current-unsolved framing:not cleared.
- Full-solution novelty promotion under the user's stronger contribution gate:not cleared by this audit. No diluted publication is proposed.

The exact remaining question is whether the short application to the2004ordinary fixed-map statistic had already been made or recognized, and whether that application is a sufficiently independent contribution for this project's goal. The missing manuscript is one close historical lead, not evidence of an earlier proof and not the sole reason for the uncleared judgment. Repeating the same title searches is not a new mechanism. A recovered original body/version, an explicit prior equivalent application, or concrete new primary historical evidence would materially change the assessment.

No individual was contacted, no outreach was drafted, and no Git/PR/Sheets/Zenodo state was modified. Further outside access to the missing body could help; only the human user may communicate externally. No publication or promotion authority is granted by these research notes.

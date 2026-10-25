# Primary interfaces and model boundaries

These readings use only raw primary bodies and source receipts, not other reviewers' mathematical opinions. Two retained PDFs are explicitly not fresh public downloads.

## Exact historical model

Norros's original contribution in OWR 48/2010, printed pp.2782–2783 (PDF pages38–39), describes the deterministic-first-chunk strategy and states the stochastic stability conjecture despite an unstable large-system limit. Its opening model uses Poisson arrivals, independent rate-one sampling clocks, one permanent seed, instantaneous successful downloads and immediate departure at completion. This fresh EMS PDF was read at the complete contribution.

Norros–Reittu–Eirola arXiv:0910.5577v1, Section3.2/Figure2 (printed pp7–9) has precisely the six rates in the current paper, but Conjecture3.4 is the opposite high-load-instability conjecture. The fresh PDF and its live arXiv version metadata were checked. It is not an interchangeable conjecture citation for the later stability statement.

The retained HAL-wrapped author proof identifies `QUES9209_source.tex; 5/01/2011; 11:31`, with HAL identifier00781341 and a cover recording submission26January2013. Read its stability definition on printed p5, Section3.2/Figure2/Proposition3.5 on printed pp10–11, and Conjecture3.6 on printed p12 (PDF pages11–13 for Section3.2). The figure was also visually inspected. The four internal rates and two λ/2 arrows agree exactly. The paragraph explicitly explains invisible empty waiting rooms and denominator X+Y+1. The stability conjecture is explicit and stability is defined as irreducibility plus positive recurrence. The fluid statement belongs to the displayed large-system limit, not an assertion of instability of the stochastic CTMC.

The HAL and publisher acquisition attempts did not return PDFs in this session. The retained raw proof was independently read, but its downloaded-public identity was not freshly authenticated. Neither the current paper nor this review replaces that author proof with the final publisher body. The model itself is independently pinned also by the fresh2009 Figure2.

## Continuous-time Foster–Lyapunov interface

Meyn–Tweedie, *Stability of Markovian processes III*, fresh author-host PDF, printed pp522–523 and529–531, gives localized extended-generator/Dynkin requirements and condition(CD2). Theorem4.2 on printed p529 (PDF page12, visually checked) requires a nonexplosive right process, drift bounded above by `-c f + d 1_C`, a closed petite set C, and V bounded on C; it concludes positive Harris recurrence and π(f)<∞.

For this countable CTMC with the discrete topology:

- Finite rates, the independent Poisson arrival construction and the workload jump-count bound establish nonexplosion; the minimal process is a right Markov process.
- The published drift is `LV≤-1` outside finite F. Since F and its one-step neighborhood are finite, LV is finite and bounded above on F. Therefore choose f≡1, c=1 and finite `d≥1+max_F LV` (enlarged to be positive). This is(CD2).
- Every state of F has a finite positive-rate path to zero. Require its holding times to fit a common finite T and then no departure from zero until T. The finite minimum of these positive probabilities yields `P_T(s,{0})≥ε` for all s∈F. Thus F is small, hence petite, and closed. V is finite and bounded on it.
- Localized generator-domain requirements hold on each finite stopped set because jump neighborhoods and all rates/function values are finite. No global stationary V-integrability is assumed. The paper's stopped-Dynkin/trial/regeneration proof independently supplies the same continuous-time conclusion.

This application uses f≡1. The integrability conclusion π(f)<∞ is normalization only, not a finite mean population or π(V)<∞ assertion. Neither a rate of convergence nor uniformity over λ follows from this use.

## Common Chunk comparison

Read the complete retained five-page Allerton2012 body, printed pp915–919, including the entire-population sampling definition, Definition3.1 and protocol, Lemmas4.1–4.2, operative Theorem4.3 proof and final rare-chunk discussion. Its three-sample contact rule includes all peers, including seed and the sampler, with replacement. It is a different generator. At the population {seed{1,2}, peer{1}}, all sampled profiles contain chunk1; the departure rule succeeds if at least one of the three samples is the seed. Exactly7 of8 equally likely triples succeed. Thus its departure rate is7/8, compared with1/2 for the current six-rate chain at(a,b,x,y)=(0,0,1,0). Constant positive arrival rates preclude repairing this difference by a mere state-dependent time scaling while preserving the same arrival clock under the natural state comparison. No universal claim about arbitrary abstract chain isomorphisms is needed.

The retained Allerton PDF's public download identity is not freshly authenticated. The supplementary Berkeley2012 technical report was acquired by scope, but this review does not claim a full read of that alternative version or of the final2015 journal extension. No conclusion about worldwide novelty or continued openness is drawn from any inaccessible or unread body.

## Aggregate seed capacity

In the six-rate model, the seed-origin component summed over downloads is `(a+b+x+y)/(x+y+1)`. At(a,b,x,y)=(2,3,0,0), the first-download total equals5. Thus a uniform capacity-one seed condition is incompatible with the literal rates. The current paper states this limitation immediately after Theorem1; it is not a defect hidden in the proof. The all-load conclusion must retain this model boundary.

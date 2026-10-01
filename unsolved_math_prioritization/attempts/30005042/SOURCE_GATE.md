# Source gate: weak moments for a coupled branching-process limit

**30005042 / OWR-9790363-001, rank280. Source verification only: 0/5 substantive author turns.** No full or partial new theorem is asserted here.

## Original model and the two questions

The complete pinned record was read; its exact imported prior report is empty. The original contribution is Cécile Mailler, joint with Jean-François Marckert, “Parametrised Galton-Watson trees: a functional version of Kesten and Stigum's theorem,” OWR12/2022, printedpp592–593. Both pages were visually inspected. The workshop took place6–12March2022; the imported citation's2023 wording does not change the actual report identifier. [Official PDF](https://ems.press/content/serial-article-files/46949).

X(λ) is a nondecreasing integer-valued offspring process with E X(λ)=λ. The full paper expressly requires càdlàg paths. Independent copies X_(n,i) define Z_0(λ)=1 and Z_(n+1)(λ)=sum_(i=1)^(Z_n(λ)) X_(n,i)(λ). Here n is discrete generation and λ is the coupled parameter. Work is restricted to I⊂(1,∞); this is not an age-dependent continuous-time branching or explosion model.

The limit question concerns W_n(λ)=Z_n(λ)/λ^n as a random element of D(I,[0,∞)), with the Skorokhod J1 topology on each compact subinterval, and convergence in probability on the given coupling. Pointwise almost-sure scalar martingale convergence is already known and is insufficient.

Writing Δ2=X(λ2)−X(λ1), Δ3=X(λ3)−X(λ2), the report's hypothesis(H) imposes, locally uniformly,

- E[Δ2² Δ3²]≤C(λ3−λ1)^(2κ)
- E[Δ3 X(λ3)^3]≤C(λ3−λ2)^κ

for κ∈(1/2,1] and a≤λ1<λ2<λ3≤b within I. Theorem1 gives functional convergence under that hypothesis. The two listed open questions ask whether one can replace it by an X log X-type condition and whether the distributional fixed-point equation yields a useful description of the limiting process law.

A natural weak hypothesis to examine is E[X(λ)log^+X(λ)]<∞ for each λ∈I. Monotonicity means the endpoint b dominates this moment on every compact[a,b]⊂I. The source does not prescribe a unique exact replacement condition, so any additional uniform or increment assumption must be declared rather than silently inserted.

## Known primary work and scope limits

The full [arXiv2106.01426v1 manuscript](https://arxiv.org/pdf/2106.01426) was recovered. Definition1.2 specifies the coupling; (HReg)/(HMom), Lemma1.5, Proposition1.6 and Theorem1.7 distinguish marginal convergence from functional tightness. Section1.3 and Lemma1.9 already characterize finite-dimensional laws as mean-one finite-second-moment smoothing fixed points by a Wasserstein contraction. The coupled equation uses the same offspring vector and the same iid descendant process copies at all parameter values; separate scalar equations do not specify their dependence.

Section2 treats binary, geometric and Poisson couplings. Its Open question1 asks for simple descriptions of their full limiting processes. Thus merely repeating a known abstract fixed-point uniqueness statement is not a full answer to the distribution-description request.

The report's introductory Kesten–Stigum shorthand omits the necessary X log X qualification for a nonzero mean-one scalar limit; the full manuscript's Theorem1.1 states it. The critical deterministic exception is also outside the intended supercritical compact intervals. These omissions must not be used to misstate the weak-moment target.

The article was published in *Stochastic Processes and their Applications*152(2022),339–377, DOI10.1016/j.spa.2022.06.010, as verified in the author's institutional publication record and publisher metadata. Full final mathematical text was not verified: the publisher page was inaccessible through the web tool, and Bath's linked “accepted manuscript” has the correct bibliographic cover but contains the unrelated *The Stable Graph*, arXiv2002.04954v3, in its body. That file is retained only as local access evidence and excluded from mathematical reliance. The complete correct arXiv manuscript and original report are the inspected mathematical sources. A bounded current primary search did not locate a later weak-moment resolution; this is not proof of historical openness or novelty.

## Prior campaign gate and accounting

Exact-ID and branching-process all-state PR searches, the exact branch search, both established main attempt-path histories, and the local all-ref path history found no prior exact attempt. The related-target group list contains no30005042. The current row was queued0/5. The neighboring30005044 explosion question is a different abstract and model and remains a separate assignment.

Source retrieval and this scope gate consume no substantive proof turn. Any subsequent author theorem must distinguish finite-dimensional/integrated results, J1 tightness, convergence in probability, and a genuinely useful process-law description. No queue regeneration, outreach or unrecognized executable was used. PDFs, extracted texts, images and complete imported records remain excluded from public checkpoints.

# Verified positive priority: an earlier explicit construction

The parent introduced the source-family positive lead after this family's independent candidate verification seal. I freshly retrieved [Ni, Zhang and Zhang, *On questions of Pogorelov and Toponogov*, arXiv:2606.29231v1](https://arxiv.org/abs/2606.29231v1), submitted 28 June 2026, and fully read its applicable introduction and §2, printed pp. 1–3. The PDF is 329660 bytes, SHA-256 `0ec8ff7da6224ece69f2beee6e71a39697a2fbc4a0aacb01b384755e69f9bbd2`. This is an earlier public preprint, not a journal-refereed certificate. This audit does not claim to verify its other surface constructions or appendix.

Section 2 explicitly constructs the graph Σ:(x,y)↦(x,y,x⁴−y⁴), prints its unit normal

n(x,y)=(-4x³,4y³,1)/sqrt(1+16x⁶+16y⁶),

and prints the closed asymptotic family

γ_a(t)=(a cos t,a sin t,a⁴(cos⁴t−sin⁴t)), a>0.

Its printed Hessian/curvature calculation and the asymptotic equation x²dx²−y²dy²=0 are exact. The graph has K≤0, with K=0 on the coordinate axes. The closed curve meets those axes, so the strictly negative-curvature subclass of Ghomi–Raffaelli is not satisfied.

The following consequences are verified here, and are not falsely attributed as prose statements in their paper. The graph normal is globally injective: n₁/n₃=-4x³ and n₂/n₃=4y³ recover x and y because n₃>0. Along the printed curve, direct differentiation gives

γ_a'×γ_a''=a²(-4a³cos³t,4a³sin³t,1).

Hence its unit Frenet binormal is exactly n(γ_a(t)), is one-to-one, and is smooth even at the four stationary binormal points. The center curve is embedded and has positive curvature.

Choose a=4^(-1/3), so a³=1/4. Positive isotropic ambient scaling by 1/a sends γ_a to

(cos t,sin t,(cos²t−sin²t)/4),

exactly the supplied candidate in `CANDIDATE_LINKING_CERTIFICATE.md`. The scaled Frenet unit binormal is unchanged and becomes (-cos³t,sin³t,1)/sqrt(1+cos⁶t+sin⁶t). Ambient scaling is an orientation-preserving diffeomorphism and maps γ_a+δB_a to the candidate plus (δ/a)B. Therefore, for every 0<δ<a/3, the original prior curve has an embedded disjoint binormal push-off with linking zero, by the complete independently checked disk certificate. This proves the full literal counterexample consequence of the earlier explicit construction, including linking, rather than merely matching one displayed formula.

The source does not explicitly state that its example answers Ghomi 2019 Problem 1.4, and does not use the phrases “injective binormal” or “zero linking” for this example. Accordingly the correct attribution is **an elementary verified consequence of their earlier explicit construction**, not “their theorem explicitly resolves Ghomi's question.” That construction removes a claim to a new construction or a first counterexample in this PR. Historical recognition of the implication is not certified by this bounded source check.

For the user's workflow, this supplies a positive priority issue supporting an `already_solved` disposition for the broad literal target, with a credited accepted partial/prior-result package and no new paper. The original one-turn unresolved artifact should be archived as historical, while current target status, findings, readiness and review scope reflect this new source. Root's second substantive attempt is retained as 2/5 even though priority prevents a new-result claim; verification adds zero attempts. The distinct strictly negative-curvature embedded-surface Problem 1.1 and Nirenberg rigidity are not declared solved.

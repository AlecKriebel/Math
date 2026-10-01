# 30002011 / OWR-11581-002: exact empirical-Bayes source gate

**Source recovery only: zero substantive author turns. Original selector question remains unresolved in this checkpoint.** The title in the imported record is a generated description. The exact source is Lawrence Brown, joint work with Eitan Greenshtein and Yaacov Ritov, *Poisson Compound and Empirical Bayes Estimation, Revisited*, OWR14/2012, printed pp.819–821. The workshop took place March11–17,2012; the report was published14November2012. The complete report and the rendered p.820 were read.

## Model, loss and exact estimator

Use n for the number of coordinates, because the short report overloads p as both this number and the later thinning probability. Observations are independent Y_i~Poisson(λ_i), λ_i≥0. The compound-decision loss is n^(-1) sum_i(δ_i−λ_i)². In the empirical-Bayes model the λ_i are iid from an unknown prior G on R_+, with oracle δ_G(y)=E_G[Λ|Y=y]. Its marginal-mixture formula is

δ_G(y)=(y+1)P_G(y+1)/P_G(y).

Write N_Y(k)=#{i:Y_i=k} and P_hat_Y(k)=N_Y(k)/n. Ordinary Robbins uses (y+1)N_Y(y+1)/N_Y(y), evaluated at observed values. The source's adjusted estimator Δ_h has three distinct steps:

1. Add independent Poisson corruption Q~Poisson(h), h>0, to an observation. Estimate the corrupted marginal by convolution

P_tilde_h(z)=sum_(j=0)^z P_hat_Y(j)e^(−h)h^(z−j)/(z−j)!.

Set d_(h,1)(z)=(z+1)P_tilde_h(z+1)/P_tilde_h(z)−h when the denominator is positive, and zero otherwise. The subtraction removes the added mean h. This is not contamination by adversarial outliers, and h is not the thinning probability.

2. Rao–Blackwellize the auxiliary corruption:

d_(h,2)(y)=sum_(j≥0)e^(−h)h^j/j! d_(h,1)(y+j).

The resulting function depends on the whole empirical count histogram, even when evaluated at one observed y.

3. Apply least-squares isotonic projection on the observed domain D(Y)={Y_1,...,Y_n}. The full Brown–Greenshtein–Ritov paper specifies the objective sum_i[d(Y_i)−d_(h,2)(Y_i)]² under d(Y_i)≤d(Y_j) whenever Y_i≤Y_j. Thus repeated values have their empirical multiplicity as weight. The final fitted values are Δ_h(Y_i). An arbitrary extension to unobserved values is not part of this original in-sample definition.

The full2013 source also uses the separately defined endpoint h=0, which is monotone Robbins. It expressly warns that Δ_(h>0) need not converge to Δ_0 when h decreases to zero: missing count bins can leave a nonzero gap-filling contribution. This warning rules out an automatic continuity argument from the known endpoint to a positive-h method.

## What “inbred cross-validation” actually means

Let α∈(0,1) be a thinning probability close to one. Conditional on Y, draw independent U_i~Binomial(Y_i,α) and set V_i=Y_i−U_i. For fixed λ, U_i~Poisson(αλ_i) and V_i~Poisson((1−α)λ_i) are independent. Fit the entire adjusted family using U, so its fitted values estimate αλ_i. The2013 paper gives the validation criterion

ρ(h;U,V)=n^(-1)sum_i[Δ_h^U(U_i)−αV_i/(1−α)]².

It suggests choosing h from a finite candidate set by minimizing this score, then constructing a corresponding estimator from the original Y sample. The OWR description also mentions rescaling estimates of αλ to estimates of λ. Averaging the score conditional on Y over repeated thinnings is another proposed Rao–Blackwell step; the short report and full paper differ in which simulations use it. These distinct output protocols must not be identified without analysis.

The source does not fix an asymptotic schedule for α, a universal candidate grid H_n, tie-breaking, truncation, Monte Carlo replication count, or a theorem transferring the selected h from U to the refitted Y estimator. Any new theorem must state these choices and its parameter class. A result about a single split estimator of αλ is not automatically a rate-sharp result for the refitted full-data estimator of λ.

## Original wording and rate normalization

The short report says that choosing h remains to be done, proposes moderate fixed h or inbred CV, and then states an informal rate claim for **ordinary Robbins**. It does not display a precise conjecture asserting a particular CV protocol is rate-sharp. The imported question combines those passages into a research objective; the source supports the objective but not omitted algorithmic quantifiers.

The short report has visible formula issues that must be normalized using the full source: the corrupted marginal displays e^h rather than the Poisson probability factor e^(−h); a consistency sentence gives the wrong limiting symbol; and the printed rate is inconsistent with its earlier average-risk normalization. These are not new statistical results. The full Brown–Greenshtein–Ritov2013 paper, §9 Theorem1, uses a Poissonized number of observations and **total regret** of order (log ν/log log ν)² under its stated bounded triangular-prior assumptions. Average regret divides by ν. Modern fixed-sample results give the familiar bounded-prior minimax order

r_n = (log n/log log n)²/n

per coordinate; this is the scale relevant to a clearly specified bounded-prior rate question, not the unnormalized display in the OWR abstract.

The full2013 §6 calculation decomposes the CV score into training loss, an h-independent validation-noise term and a centered cross term. That h-independent term is irrelevant to choosing h but cannot be silently discarded in an absolute score-equals-loss assertion. The displayed cross term has a sign convention inconsistent with the expansion, though its variance and comparison role are unchanged. The discussion aims at uniform o_P(1) comparison under a thinning/grid condition; it does not prove the much smaller regret-scale error or the proposed full-data-refit transfer. These distinctions will be retained rather than treating an informal consistency claim as the missing sharp theorem.

## Later results and proper credit

- Brown, Greenshtein and Ritov, *The Poisson Compound Decision Problem Revisited*, JASA108(502)(2013),741–749, DOI10.1080/01621459.2013.771582. Complete arXiv1006.4582v2,28January2013, was read for the actual estimator, endpoint discontinuity, CV equations and Robbins asymptotics. Publisher metadata records online publication1July2013. The final journal-layout PDF was not compared. One institutional older PDF endpoint returned403; the full arXiv edition was available without that endpoint.
- Jana, Polyanskiy and Wu, *Optimal empirical Bayes estimation for the Poisson model via minimum-distance methods*, Information and Inference14(4)(2025),iaaf027, DOI10.1093/imaiai/iaaf027, published7October2025. Both complete arXiv2209.01328v3 and a full42-page journal-layout copy hosted by a coauthor were obtained. The introduction explicitly distinguishes the older smoothing/monotonicity modifications from its own minimum-distance/NPMLE estimators and does not establish sharp regret for the original Δ_h selector. Exact theorem and regret conventions distinguish in-sample total regret from new-observation regret and use an explicit leave-one-out comparison where needed. The parameter denoted h as a support bound in that paper is unrelated to the corruption h here.
- Jana, Polyanskiy, Teh and Wu, *Empirical Bayes via ERM and Rademacher complexities: the Poisson model*, COLT2023, PMLR195:5199–5235. A complete author version was read for §1.1–1.4 and the main estimator/rate statements. Its ERM minimizes the empirical criterion f(X)²−2Xf(X−1) over monotone functions, on an enlarged grid including X_i−1. It is not the least-squares projection of d_(h,2) from the source. The paper also expressly credits the regret guarantee for monotone Robbins as a known side observation and cites older monotone-smoothing work. No new claim of that endpoint guarantee is appropriate here.
- Shen–Wu, *Poisson empirical Bayes estimation: When does g-modeling beat f-modeling in theory (and in practice)?*, Annals of Statistics54(1)(2026),146–175, DOI10.1214/25-AOS2560. The complete arXiv2211.12692v2 was read for the model, main theorem scopes and concluding discussion; the published issue metadata was verified. Its heavy-tail comparison concerns Robbins and proper g-modeling, with a discussion of monotone ERM. It does not supply a theorem for the corruption/CV/refit protocol. The final journal-layout article was not compared.

Current primary-source searches through1October2026 did not identify a completed theorem for this exact selector. This is a dated literature assessment, not a proof of historical openness or novelty. Known optimal NPMLE, ERM and monotone-Robbins alternatives are useful benchmarks, not replacements for the specified source family and selector.

## Gate and research state

Numeric-ID and source-code all-state PR searches returned zero. Both possible attempt-path histories, the dedicated branch prefix and local all-ref target history were empty. The queue row is rank312, queued0/5. No exact source-code upstream report was present. The raw imported record is retained for reading but excluded from the public packet.

The first substantive turn will start only after this source checkpoint. The retained objective is a precise analysis of h choice and the specified Poisson-thinning validation mechanism at the relevant regret scale, with all changes to the protocol or prior class labeled. No rate-optimality conclusion has yet been claimed. Source PDFs, extracted text and rendered pages are excluded from publication.

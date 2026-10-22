# Independent adversarial review: physical-clock condensation obstruction

## Verdict

**PASS_SCOPED_PHYSICAL_CLOCK_OBSTRUCTION. No mandatory mathematical correction.**

This review covers `CLOCK_OBSTRUCTION.md`, SHA-256
`69b774f175abbaf05297b7c03956a9c71c7f0e8b41e0b00b34990ab9927322e5`.
The necessary Gamma-rate theorem and its positive-mutation example are correct for the stated physical-time branching model. The theorem rules out the precise printed rate-one profile in that model. It does **not** establish existence, shape, or universality of a clock-corrected condensate profile.

Recommended conservative status: **unsolved, one substantive approach**, with the source-normalization qualification retained. This is a separate adversarial AI review, not human peer review or certification of historical priority.

The submitted verifier reproduces its receipt byte for byte: **21,490 assertions pass**. Distinct independent controls give **52,751 passing exact assertions**. The probabilistic proof, rather than these finite controls, supports the theorem.

## 1. Exact source and clock audit

I read the complete three-page contribution by Peter Mörters in [Oberwolfach Report 35/2015](https://ems.press/content/serial-article-files/46582), printed pp.1997--1999, and visually inspected the rendered model definition and conjecture. The model is continuous time: every immortal individual of fitness f produces a single child at rate f, and the child mutates with probability beta. Thus its clonal birth rate is **c f**, where c=1-beta. The normalized empirical measure is explicitly defined on p.1997. The family-sum display on p.1998 omits its normalization; the candidate correctly retains the earlier normalized definition.

The condensation mass on p.1998 is rho=1-beta I, with I the integral of 1/(1-f). The conjecture on p.1999 uses the window (1-x/t,1) and a rate-one Gamma expression with shape alpha. No intervening time change is announced. The page does not specify a convergence mode for this particular display. The candidate precisely rules out convergence in probability to that deterministic profile, and therefore also convergence in distribution to the same deterministic value and stronger usual deterministic-limit modes. It makes no claim about an expectation-only interpretation.

I also checked [Dereich--Mailler--Mörters, arXiv:1601.08128v2](https://arxiv.org/abs/1601.08128), dated 30 January 2017. Its Example 1 on p.2 identifies the physical model with the clonal parameter gamma=1-beta. Its regular-variation assumption on p.5 uses tail exponent alpha. Conjecture 8.1 on p.20 displays shape alpha+1 and the same rate-one physical-time form. I visually inspected that display. The candidate correctly distinguishes these shapes and does not identify the largest-family observable with the collective normalized condensate.

The theorem reviewed here applies to the single-offspring house-of-cards case beta+gamma=1, rather than asserting a theorem for every member of that paper's larger class. The Kingman generation model and subsequent largest-family results are distinct and are not proof dependencies. Bounded current source searches corroborated the presence of the conjecture in an author-hosted accepted manuscript, but do not certify the absence of all later corrected results.

## 2. Renewal estimate: no hidden population asymptotic

The first-mutant decomposition is exact. From a founder of fitness f, its nonmutant descendants form a Yule family of rate c f. Its mutation stream has mean intensity beta f exp(c f s), and each mutant starts an independent full population with fitness drawn from mu. Thus

\[
m_f(h)=e^{cfh}+\beta f\int_0^h e^{cfs}m_\mu(h-s)\,ds.
\]

After discounting by exp(c h), the averaged equation is u=a+K*u with the candidate's a and K. Nonexplosion follows from domination by a rate-one Yule process. Classifying finite-time individuals by their finite number of mutation edges gives the nonnegative convolution series without an unproved renewal theorem or a missing remainder term.

The exact norms are

\[
\|a\|_1=I/c,\qquad
\|K\|_1=(\beta/c)(I-1),\qquad
1-\|K\|_1=\rho/c>0.
\]

Tonelli gives ||u||_1=I/rho. Substitution into the fixed-fitness identity yields

\[
e^{-ch}m_f(h)\le 1+\beta I/\rho=1/\rho.
\]

This estimate is uniform in every starting fitness in (0,1), not merely mu-almost surely. Cutting the population at time t and applying the branching property therefore gives the advertised conditional bound for **every realized finite population**. No precise polynomial correction to N(t) has been assumed.

As an independent diagnostic I formed the exact backward first-moment matrices for 74 rational finite-type distributions and parameter choices. Their discounted resolvents, averaged integrated means, scalar renewal transforms, and twelve derivatives at zero agree. These finite-type examples do not have essential supremum one; they are tests of the renewal algebra only, not substitutes for the continuous-tail example.

## 3. The old/late partition and conditional estimates

A possible pitfall is that immortal individuals alive at t can be ancestors of other individuals also alive at t. The proof handles this correctly. Cut every genealogical edge created before t; each individual present at t becomes a separate future root. A later individual either has no mutation on its post-t ancestral path, or has a most recent mutation on that path. This partitions the population into old-root clonal descendants and clonal families founded by post-t mutations, without overlap.

Future Poisson birth streams of distinct cut roots are independent. Mutation births do not remove their parents and do not alter their clonal streams. Hence the sum of old high-fitness clone counts has conditional variance at most N(t) exp(2c h). Dividing by N(t)^2 exp(2c h) leaves 1/N(t). The initial immortal individual has positive fitness almost surely and produces infinitely many births over infinite time, so N(t) tends to infinity almost surely. Dominated convergence then justifies the unconditional probability estimate.

For late mutations the marked birth compensator has intensity beta times the current total fitness times mu(df) ds. Conditional expectation of each new founder's future clonal size is exp(c f (qt-s)). The proof's use of the compensator is valid even though the mutation rate is coupled to the random current population. Bounding total fitness by N(s), and then using the conditional growth estimate, gives exactly

\[
\frac{\mathbb E[L_t(x)\mid\mathcal F_t]}{N(t)e^{c(q-1)t}}
 \le \frac\beta\rho(q-1)t\,\mu(1-x/(qt),1).
\]

Finite I implies that the last tail is o(1/t): its ratio to the window width is bounded by the integrable endpoint tail of 1/(1-f). Conditional Markov's inequality proves negligibility in probability. The proof has not substituted an expected population for a random denominator.

My independent exact genealogy tests cover 153 recursive rooted trees and 5,774 cuts/mutation assignments. Separate clonal traversal and backward most-recent-mutation classification give the same disjoint partition, including repeated fitnesses across different mutant roots. Exact mixture-tail checks corroborate the endpoint estimate beyond the author's single beta-density family.

## 4. The random normalization is derived, not assumed

For the deterministic band at time qt, the normalized old-clone conditional mean is exactly the exponentially tilted mass of nu_t on (0,x/q). This proves the candidate's equation (8), with an error normalized by the **time-t** random population. The left side uses the same random ratio

\[
R_t(q)=\frac{N(qt)}{N(t)e^{c(q-1)t}}
\]

for every choice of x.

The assumed profile is used only from this point. The candidate's Stieltjes integration-by-parts formula is correct even when nu_t has atoms at interior points or at the excluded upper endpoint. There is no atom at zero since all fitnesses are strictly below one. Boundedness by one upgrades each pointwise convergence in probability to convergence in L1; Fubini and dominated convergence then justify the ordinary integral limit. No uniform convergence of the random distribution functions is needed.

The limiting Gamma mass is strictly positive at each fixed x>0, so division gives a deterministic probability limit J_q(x)/H(x) for R_t(q). Uniqueness of a limit in probability forces that ratio to be independent of x. There is no circular appeal to a pre-existing growth-ratio theorem.

Differentiating the resulting deterministic identity gives

\[
r(q)=q^{-k}\exp\{(\lambda-c)(q-1)x/q\}.
\]

Because q>1 and x ranges over positive numbers, this is constant exactly when lambda=c. Then r(q)=q^{-k}. The calculation is valid for every real k>0, not just integral shapes. Independent exact controls include half-integral shapes and the corresponding logarithmic derivative identity.

## 5. The concrete contradiction and scope boundary

For mu(df)=2(1-f)df and beta=1/4, the exact values are

\[
\mu(1-\varepsilon,1)=\varepsilon^2,\quad I=2,\quad
\rho=1/2,\quad c=3/4.
\]

All original strict-condensation hypotheses hold. The printed OWR Gamma shape is two and its rate is one, contradicting the necessary rate 3/4. For q=2 the alternative direct ratio has limits 1/4 and 16/49 at zero and infinity, respectively. This is a comparison of a deterministic function after establishing the fixed-x probability limit; it does not exchange t and x limits.

The change s=c t sends a possible rate-c variable t(1-f) to a unit-rate variable s(1-f). Thus the repaired unit-rate window is precisely 1-x/(ct). This clock conversion is correct. It does not prove that the repaired profile converges or decide its shape. The conservative unsolved status and the distinction from a full original-profile solution must remain prominent in publication.

## 6. Reproducibility and publication contents

- Submitted verifier SHA-256: `654354a5365e703371f21a896088050690054435fd2d573b5ca304ab97284d93`
- Submitted receipt SHA-256: `8a8d2dc0cba2698862c1deb342deb3830ce5fe42abf503bb19bd5e3b41b48bbf`
- Submitted receipt replay: byte-identical, 21,490 assertions
- Independent controls: 52,751 exact assertions; Python standard library only
- No author mathematics or public repository state was edited by this reviewer

Run the submitted checker inside `author_replay/`; it prints its receipt. Run `independent_checks.py` from the review directory; it writes `independent_results.json`. Retain the frozen author artifact in `author_replay/`, since the independent checker hashes that exact dependency. The publication list in `review_summary.json` excludes full third-party sources and the redundant replayed receipt.

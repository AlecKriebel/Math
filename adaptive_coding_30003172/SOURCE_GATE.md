# Source gate: simultaneous adaptive universal source coding

## Verdict and scope

Ordered row 1842, ID 30003172, source key OWR-14741-004. Source recovered and identity verified. The catalogue target is underspecified as a standalone research problem: it does not designate the collection of subclasses. The source introduces a general adaptive-coding framework, then studies a particular collection of countable-alphabet envelope classes. Do not silently replace its motivating question with a conjecture of exact adaptation for every conceivable collection, or with exact adaptation over all regularly varying envelopes.

The original report already proves simultaneous adaptation up to an envelope-dependent multiple of log log n on its specified regular-variation family. This does not establish a fixed-factor or asymptotically exact result. No later primary source resolving those stronger questions was located in this bounded literature search. That is a search result, not proof of present-day openness.

## Identity and provenance

- Original report: Learning Theory and Approximation, Oberwolfach Reports 13 (2016), no. 3, pp. 1875–1941, DOI https://doi.org/10.4171/OWR/2016/33 . EMS item https://ems.press/journals/owr/articles/14741 . EMS lists publication 22 April 2017; 2016 is the report/workshop year.
- Relevant contribution: Stéphane Boucheron, joint work with Anna Ben-Hamou and Elisabeth Gassiat, “Adaptive compression against countable alphabets,” printed pp. 1921–1925.
- Full related manuscript: Anna Ben-Hamou, Stéphane Boucheron, Elisabeth Gassiat, “Pattern Coding Meets Censoring: (almost) Adaptive Coding on Countable Alphabets,” https://arxiv.org/abs/1608.08367 . Version 1 submitted 30 August 2016; version 2 dated 1 September 2016 on arXiv. This is contemporary elaboration, not a subsequently proved exact-adaptivity result.
- Existing local catalogue freshly rehashed: unique problems.json ID/key match; research_results.json has no matching key. Public hashes and byte counts are in DATASET_METADATA.json. No dataset contents are included in this package.

## Benchmark and quantifiers

The model in the contribution is lossless binary coding of stationary memoryless sources on a countably infinite alphabet, concretely positive integers. A marginal probability P generates the product law P^n. Coding distributions Q_n on sequences correspond to uniquely decodable codes up to bounded rounding overhead.

Use base-2 logarithms for coding lengths. Expected redundancy is D(P^n || Q_n), the KL divergence in bits. Define

R(Q_n,C^n) = sup_{P in C} D(P^n || Q_n),
R(C^n) = inf_{Q_n} R(Q_n,C^n).

This is maximum expected redundancy, NOT pointwise/worst-sequence regret. Minimax regret appears in the related proof technology, but is a different benchmark. Coding only a pattern while discarding the actual symbol dictionary is also a different task.

For a fixed specified collection (C(a))_{a in A}, exact asymptotic adaptation means there exists ONE sequence (Q_n), independent of a, such that for EVERY fixed a,

R(Q_n,C(a)^n) <= (1 + o_a(1)) R(C(a)^n), as n tends to infinity.

The little-o and its onset may depend on the class. This is not uniform convergence over a. The source also allows a larger adaptation factor, which can depend on a. A fixed-factor goal means a finite factor independent of n, not necessarily independent of a. Having an optimal code separately for each class is only universality and does not satisfy the quantifier order. Nontrivial minimax redundancy in the manuscript means o(n); mere nontriviality alone is not a structural assumption guaranteeing adaptation of arbitrary collections.

## Exact envelope assumptions

The source takes an envelope function f: N_+ -> (0,1], nonincreasing, with 1 < sum_j f(j) < infinity. C(f) consists of ALL marginals p with p(j) <= f(j) for each labeled integer j. The source p itself need not be monotone or regularly varying. Label order matters; replacing labeled probabilities by an unknown permutation of their sorted values is not an authorized equivalent.

Set ell_f = min{ell >= 1: sum_{j>=ell} f(j) <= 1}. The associated envelope distribution is F(k)=1-sum_{j>k}f(j) when k+1 >= ell_f, and zero otherwise. Let f_j = F(j)-F(j-1). The manuscript defines its counting function using these envelope probabilities:

N_f(x) = #{j >= 1: f_j >= x}.

The hypothesis is N_f(1/t) regularly varying as t -> infinity, with index rho in [0,1). Equivalently N_f(1/(ct))/N_f(1/t) -> c^rho for each c>0. The source's abbreviated notation “f in RV_rho” should not be read as asserting that the original sequence f(j) has positive regular-variation index. Use the counting-function formulation to avoid that ambiguity.

The code is independent of both f and rho. There is no assumption that every class is discretely indexed or nested. Rho=0 includes slowly varying counting functions; rho=1 is expressly outside the PC adaptive-code theorem.

## What the source actually proves

Define the scale

R_f(n) = (log_2 e)/2 times integral from 1 to n of N_f(1/t)/t dt.

OWR Theorem 1, p.1924 (full manuscript Theorem 6) asserts that the Pattern Censoring code Q_n satisfies, for each rho in [0,1) and every allowed f of counting index rho, some constants a_f,b_f>0 with

a_f + o_f(1) <= R(C(f)^n)/R_f(n)
             <= R(Q_n,C(f)^n)/R_f(n)
             <= (b_f + o_f(1)) log log n.

Thus R(Q_n,C(f)^n)/R(C(f)^n) = O_f(log log n). This diverging bound is not a fixed constant, and it is not 1+o_f(1).

Full-manuscript Theorem 5: minimax redundancy is comparable to R_f for 0<=rho<1; asymptotic equivalence with coefficient one is explicitly obtained for rho=0. Do not claim coefficient-one equivalence for all positive indices. The manuscript separately discusses rho=1, where R_f is not the correct comparable scale; this is another reason not to include that endpoint in the adaptive result.

The PC algorithm interleaves dictionary and pattern encoding: new symbols are censored and integer-coded; seen symbols are encoded by their insertion ranks using a growing-alphabet mixture. The manuscript attributes its log log n upper-bound loss to the residual part of the Elias code. This explanation is NOT a lower bound proving that such a loss is necessary for every adaptive code.

## Known restricted results and literature check

- Finite known alphabet of size k: standard i.i.d. minimax redundancy is (k-1)/2 log_2(n/(2 pi e)) + O_k(1). This does not solve unknown countably infinite envelope adaptation. Even the integral heuristic with eventual counting function k has k/2, not (k-1)/2, so “scales like” must not be promoted to exact finite-alphabet equivalence.
- Bontemps, Boucheron, Gassiat (2014), “About adaptive coding on countable alphabets,” IEEE TIT 60(2), 808–821: exact asymptotic adaptation of the AC code for envelope distributions with finite nondecreasing hazard rate, a restricted light-tail family. Primary earlier conference source: https://dmtcs.episciences.org/2995/pdf .
- Boucheron, Gassiat, Ohannessian (2015), “About Adaptive Coding on Countable Alphabets: Max-Stable Envelope Classes,” https://arxiv.org/abs/1402.6305 : ETAC obtains near-adaptation with a logarithmic factor for heavy-tailed max-stable envelopes. This does not prove exact/fixed-factor adaptation over the whole regular-variation collection.
- The PC manuscript improves coverage and its factor to log log n. The author's publication list, inspected 21 October 2026, still labels this manuscript submitted (2016): https://www.imo.universite-paris-saclay.fr/~elisabeth.gassiat/liste-publi.html . This is evidence of publicly stated manuscript status, not a guarantee that no later resolution exists.
- Searches for the exact title, regular-variation adaptive coding, envelope-class constant-factor adaptation, and 2023–2025 developments did not locate a stronger primary theorem. A 2023 LQG application concerns a different control problem and is not a resolution. Unverified aggregator claims of a necessary log log n loss were not accepted.

## Safe next research direction

Specify whether the goal is (a) a theorem characterizing which collections permit adaptation, (b) an obstruction to the literal arbitrary-collection reading, or (c) removal of the log log n factor for the stated regular-variation envelope family. These are different mathematical questions. A counterexample to (a)'s unrestricted formulation must not be presented as resolving (c). Conversely, a known restricted positive theorem must not be presented as solving the unrestricted catalogue question.

Copied PDFs and extracted source text are excluded. SOURCE_METADATA.json records downloaded-source hashes, sizes and inspection method; no visual-page verification is claimed.

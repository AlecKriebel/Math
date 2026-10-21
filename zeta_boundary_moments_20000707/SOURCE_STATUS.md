# Source and status gate: AIM 8.1 (queue 1862)

Audit date: 2026-10-21. ID 20000707 / AIM-ANALYTIC_NUMBER_THEORY-0071.
Verdict: **original broad problem recovered; generated specialized claims are not a solution of it.** Fixed-sigma smoothing and the endpoint polynomial-window term are consequences of classical results. The varying-sigma assertion is only a reduction. No global novelty or completeness claim is supported.

## Original versus generated scope

The archived official AIM page identifies Problem 8.1 in “Miscellaneous,” workshop “Moments of zeta and correlations of divisor sums,” as a question of T. Wooley about calculating zeta moments nearer the line sigma=1 and finding endpoint lower-order terms. K. Soundararajan's accompanying remark concerns retaining nonzero shift variables in Conrey–Keating heuristics. The dataset's original_statement matches the archived official body exactly. The generated title is not an original AIM title: the official name field is empty. The dataset omits the known proposer (proposed_by=null). Its partially_solved label describes the imported attempt, not an official AIM resolution; the archived official status is empty.

Source: http://aimpl.org/zetamoments/8/ . Fresh requests on the audit date timed out or returned 502; an existing saved official HTML was inspected, including its structured problem and remark records. Thus current live page status was not newly certified.

The original question does not prescribe moment order, a weight, support, interval, uniformity, a conductor limit, or a family of Dirichlet/automorphic L-functions. It is about the Riemann zeta function. The report makes the following additional choices:

- Second moment only, |zeta(sigma+it)|^2.
- Fixed 3/4<sigma<1; fixed real/complex psi in C_c^2((0,infinity)), supported in fixed [c,d] with 0<c<d. Averaging weight psi(t/T), with T tending to infinity. Constants depend on sigma and psi.
- Endpoint sigma=1: integrate from 1, or over [T^a,T^b] with fixed 0<a<b. There is no conductor parameter.
- Transition: sigma_T=1-lambda/log T with fixed lambda>0; this is a separate unproved uniformity problem, not included in a fixed-sigma theorem.

## Precisely verified classical input and generated consequences

Put q=2-2sigma and C_sigma=(2pi)^(2sigma-1) zeta(q)/q. Define

F_sigma(X)=integral_0^X |zeta(sigma+it)|^2 dt
         =zeta(2sigma) X+C_sigma X^q+E_sigma(X).

This is an exact decomposition **by the definition of E_sigma**, not an error-free exact moment evaluation. Lau's paper uses precisely the primitive from zero (p.446), not the endpoint primitive from one.

Lau, Corollary 1, pp.447–448, proves for each fixed 3/4<sigma<1:

integral_1^X E_sigma(t) dt = -2pi zeta(2sigma-1)X+O_sigma(sqrt(X)).

At sigma=3/4 the stated remainder is O(sqrt(X) log X). The paper explicitly allows implied constants to depend on sigma. Full PDF inspected. DOI: https://doi.org/10.5802/jtnb.553 .

Two integrations by parts with the specified compactly supported C^2 weight therefore give the report's formula:

integral_0^infinity psi(t/T)|zeta(sigma+it)|^2 dt
= zeta(2sigma)T integral psi(u)du
+ (2pi)^(2sigma-1)zeta(2-2sigma)T^(2-2sigma) integral psi(u)u^(1-2sigma)du
+ O_sigma,psi(T^(-1/2)).

The linear mean-error term vanishes because integral u psi''(u)du=0; an integration constant also vanishes. The formula is asymptotic, with absolute (not normalized) error. No positivity or unit integral of psi is required. It is a straightforward consequence of Lau, not certified novel progress. The endpoint sigma=3/4 would carry a logarithm in this argument; the report correctly excludes it.

Balasubramanian–Ivić–Ramachandra (1992) give the endpoint remainder, in the normalization

R(X)=integral_1^X |zeta(1+it)|^2dt-zeta(2)X+pi log X,
R(X)=O((log X)^(2/3)(log log X)^(1/3)).

DOI: https://doi.org/10.5169/seals-59479 . The original publisher download returned a verification HTML, not a PDF; it has been labelled accordingly. The normalization and bound were additionally checked in Matsumoto's 1994 research exposition, p.15: https://www.kurims.kyoto-u.ac.jp/~kyodo/kokyuroku/contents/pdf/0886-02.pdf . The author-uploaded 1992 paper text explicitly warns that a zero lower integration limit is impossible at sigma=1. We have not falsely recorded a fresh full original-PDF inspection.

Subtracting two endpoint formulas gives exactly the report's asymptotic lower term -pi(b-a)log T on [T^a,T^b], with error of the same logarithmic order. This error is o(log T), but not o(1). Consequently it does NOT isolate the constant -pi log 2 on an unsmoothed [T,2T] window. Moving the lower endpoint of the primitive changes an additive constant only. An endpoint integral including t=0 with a nonvanishing weight diverges from the pole of zeta.

## Boundary-layer identity and what it does not prove

For fixed lambda>0 and q_T=2lambda/log T, the secondary-term increment is

[(2pi)^(1-q_T) zeta(q_T)/q_T] [exp(2b lambda)-exp(2a lambda)].

The elementary identities zeta(0)=-1/2 and zeta'(0)=-log(2pi)/2 cancel its linear numerator term. Thus its leading coefficient of log T is

Phi(lambda)=-pi [exp(2b lambda)-exp(2a lambda)]/(2lambda),

with Phi(0)=-pi(b-a) by continuity. This calculation checks the report's coefficient and sign. The corresponding moment asymptotic is equivalent to

E_(1-lambda/log T)(T^b)-E_(1-lambda/log T)(T^a)=o(log T).

The equivalence is an algebraic reformulation, not a bound on this increment. Neither Lau's fixed-sigma estimate nor an unspecified sigma-dependent constant proves it, even for one fixed lambda. Uniformity over compact lambda-sets would be an additional assertion. No claimed proof of that increment was verified in this search.

## Endpoint smoothing and current-literature checks

Ivić's ICM 2010 contributed abstract, printed p.82, announces integral_1^X R(t)dt=BX+O(X/log X), and an analogous square mean with C>0. Full abstract PDF inspected:
https://www.mathunion.org/fileadmin/IMU/ICM2010/offline/www.icm2010.in/wp-content/icmfiles/abstracts/Contributed-Abstracts-5July2010.pdf .

It supplies neither a full proof nor explicit numerical/formula values of B,C. No full proof was located by this audit. The generated conditional smoothing consequence has coefficient -pi integral psi(u)/u du and error O_psi(1/log T). It is correctly conditional **on the announced estimate as a verified input**, not conditional on RH. B disappears under the integrations by parts; it need not be known for that implication. An announcement alone should not be upgraded to a fully audited theorem.

A relevant omitted publication is A. V. Zobnin, “On square of the Riemann zeta function modulus in the critical strip and estimates of means,” Sbornik: Mathematics 216:4 (2025), 485–493, published June 17, 2025: https://doi.org/10.4213/sm10113e ; full publisher HTML https://www.mathnet.ru/eng/sm10113 . Theorem 2 gives a Laplace-transform estimate for E_sigma for each fixed 1/2<sigma<1. Theorem 3 treats normalized Gaussian averages with exp(-t^2/Delta^2), explicitly nonuniformly in sigma, and remainder O(T Delta^(-2sigma-1))+O(Delta^(-2sigma)). Its preliminary prose sometimes writes Delta rather than Delta^2; use the theorem's normalization. Neither result establishes this report's sigma=1 transition or compact-support endpoint constant. The exact representation in its Theorem 1 should not be confused with an exact two-term moment formula.

Bettin's arXiv:1111.0925 (full PDF inspected) requires real shifts O(1/log T), while allowing large imaginary shifts. It does not license real shifts approaching 1/2 to move zeta to sigma=1. The imported bibliographic title adds wording not identical to the journal/arXiv abstract title; identify by DOI/arXiv ID rather than that generated title. https://arxiv.org/abs/1111.0925 .

Dutta–Ghoshal–Rajkumar, arXiv:2408.04247v1 (2024), is another omitted shifted-moment preprint: https://arxiv.org/abs/2408.04247 . Its displayed theorem has small real shifts and power-sized errors, not an o(log T) near-one boundary theorem. It is not a substitute for the missing increment estimate. Its criticism of Bettin is an author claim, not adjudicated here.

BIR (1993), Theorem 1, establishes fixed complex-power endpoint leading moments with constant sum_n |d_k(n)|^2/n^2 and logarithmic error: https://doi.org/10.4064/aa-65-1-45-51 . Lamzouri's 2008 distribution paper compares endpoint mixed moments with a random Euler product: https://arxiv.org/abs/0801.3692v2 . These support known endpoint leading-order theory; neither a leading-order comparison nor a large relative-error estimate detects a logarithmic/constant secondary term. General L-function statements in related literature are not the original problem's prescribed family.

Conrey–Keating I: https://arxiv.org/abs/1506.06842 . Equal shifts give the two formal densities zeta(2sigma) and (t/(2pi))^(1-2sigma)zeta(2-2sigma); the latter becomes -pi/t at sigma=1. Agreement of densities is not a uniform error proof.

## Disposition

Retain the broad AIM question as unresolved by this attempt. Accept the fixed-sigma smoothing and polynomial-window endpoint statements as classical consequences, and the transition formula only as a correctly labelled reduction. Do not claim the boundary estimate is globally open merely because this audit did not find a proof. Searches through the audit date found no verified complete solution; that is a bounded search result, not a proof of absence. No new mathematical research result is claimed.

# Acceptance report: harmonic LCM avoidance, 2344 / EP-856

This is an AI-assisted, unrefereed authored mathematical audit edition. Acceptance means an independent internal AI audit of the precisely scoped written arguments and their explicitly retained standard and external dependencies. It is not external human peer review, journal acceptance, formal proof-assistant certification, or a novelty or priority claim.

This is not a computational reproduction package. The complete ten-section mathematical reconstruction and full ancillary correction note are retained, including all parameter orders, supremum qualifications, density substitutions, dependencies and limitations. Executable code, raw calculation outputs or datasets, copied source documents or text, source images and private coordination material are not distributed.

Retrieval, inspection and mathematical-check statements describe the original audit of October 11, 2026 UTC. Editorial preparation performed no new scholarly-source retrieval, source-body inspection, literature survey or mathematical execution. Historical finite checks supplement the written proofs; they do not establish asymptotic claims or numerically evaluate the exponent.

## Accepted existing core

For every fixed integer k≥3, the reciprocal-sum maximum f_k(N), forbidding k distinct integers with equal pairwise LCMs, has logarithmic exponent gamma_k. The weighted sunflower pressure Lambda and cosunflower pressure Ltilde obey the accepted descriptions

    gamma_k = lim_(z→∞)(Lambda(z)−z)
            = inf_(z>0)(Lambda(z)−z)
            = sup_(z>0) z log(Lambda(z)/z)
            = sup_(u>0) log Ltilde(u)/u
            = lim_(u→0+)(Ltilde(u)−1)/u.

The exact finite-block elimination is

    gamma_k = sup_(n≥1, 1≤r≤n) r M_k(n,r)^(1/r)/(e n).

These are accepted as prior arguments of the cited manuscripts, after independent reconstruction. The accepted scope also includes complete-layer bounds, monotonicity in k and the consequence gamma_k→1 as k→∞ after each fixed-k exponent has been established. This is not uniform-in-k asymptotics for f_k(N).

AUDIT.md retains the entire mathematical reconstruction. Uniformity of tensor factors is essential; arbitrary nonuniform products are not closed. The upper transfer handles prime powers through valuations, whereas the lower construction is explicitly squarefree. Blow-ups handle repeated projections and use k≥3. Fixed z, delta, eta and lambda precede the N-limit. The unbounded-z squeeze constrains the already defined liminf and limsup, with no interchange of N and z limits. The two suprema range over one Cartesian product, rather than invoking minimax, compactness or optimizer attainment.

## Accepted ancillary repairs

Tang–Zhang Lemma 5.6's missing factor is restored as −log(n+1). With 0<epsilon≤1/10, c=1/ceil(1/epsilon²) and delta=epsilon c/10, enlarge K(epsilon) so that log(W/c+1)+c+1≤[(log 2−1/5)epsilon−c]W for every W≥K. The right coefficient is positive, so the lemma's original lower bound is recovered without endorsing its printed equality or isolated numerical threshold.

The literal all-n H(beta,k) hypothesis fails at beta=2, k=3, n=1. This is not an arbitrarily large counterexample. The direct substitute in section 9.3 and PROOF.md derives dense middle layers from mu_k^S=2, then uses conditioning and averaging to obtain every fixed proportional-rank layer at exp(−o(n)) relative density. All-large-n quantifiers and distinctness are preserved. This supplies the input needed by Tang–Zhang's lemma and Chojecki's optional proposition. The full-density consequence survives; an alternative pressure proof avoids the dropped-factor calculation entirely. The log(N²)=2 log N scale typo has no effect on the claimed big-O bound.

The central weighted exponent existence and finite-block proof are independent of these two defective ancillary passages. No core gap was found in the accepted reconstruction.

## Dependencies and exclusions

Standard Mertens prime reciprocal and logarithmic first-moment estimates remain core analytic inputs. The reconstructed elementary weighted squarefree harmonic estimate bypasses Selberg–Delange and the ancillary Sathe–Selberg input. The general Sathe–Selberg theorem used in Tang–Zhang's appendix is cited, not reproved. The sharper gamma_3 numerical interval retains the 1997 capacity lower construction and 2017 capacity upper theorem as external dependencies not independently re-audited. Neither is needed for the elementary 1/e≤gamma_k≤1 or the core equality.

No numerical evaluation even of gamma_3, closed formula for all gamma_k, attained finite maximizing block, effective approximation stopping certificate, determination from the single unweighted capacity, bounded multiplicative error, effective rate, or full multiplicative asymptotic equivalent is accepted. The estimate f_k(N)=(log N)^(gamma_k+o(1)) permits nonconstant subpower factors. The original estimation problem is not declared completely solved.

## Historical inspection and finite verification

The complete written texts of Tang–Zhang (19 pages including Appendix A), Chojecki (14 pages) and Luo–Yang–Zhu (9 pages) were read. Listed critical pages were visually checked. All three freshly retrieved primary PDFs matched the originally inspected bytes. Erdős's original target page, the relevant Alon–Shpilka–Umans density argument and Lichtman's equation (4.9) were inspected only at the recorded scope. The 2026 sources were inspected as a hosted manuscript and an arXiv preprint; no peer-reviewed status is inferred.

Historical independent finite checks covered uniform two-block products through four points, nonuniform index-family blow-ups through three points with two-element buckets, arithmetic tuples through m=500, and exact M_k(n,r) through n=5 for k=3,4,5, together with the reported negative controls and decimal substitutions. Normal Python, -O and -OO result bytes agreed. These finite checks supplement the proofs and cannot establish asymptotics. No source-author code was executed. No mathematical checks or scholarly-source inspections were repeated during editorial preparation. Verification metadata is not a computational reproduction package; cryptographic identity establishes bytes, not mathematical truth.

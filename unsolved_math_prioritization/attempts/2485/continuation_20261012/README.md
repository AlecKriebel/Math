# EP1095 continuation with an eventual bound below the lcm

12 October 2026. AI-assisted authored mathematics and independent AI proof reviews. The principal accepted result is

\[
\limsup_{k\to\infty}\frac{\log g(k)}{k}\le\frac{813}{875}<0.93<1,
\qquad g(k)<\exp(0.93k)<L_k\quad\text{for all sufficiently large }k,
\]

where

\[
g(k)=\min\{n>k+1:p\nmid\binom nk\text{ for every prime }p\le k\},
\qquad L_k=\operatorname{lcm}(1,\ldots,k).
\]

The proof uses the prime number theorem and an explicit Brun/Bonferroni lower sieve on a reduced lattice, including every prime-square local condition and the complete growing CRT endpoint-error budget. It proves an actual initial-interval survivor. A full-period density heuristic is not used to locate the first admissible integer.

The original problem remains unsolved. No effective numerical starting value, all-k lcm comparison, subexponential bound, conjectured exp(Theta(k/log k)) scale, or successive-ratio conjecture is proved. Independent AI acceptance is not external human peer review, formal proof-assistant certification or journal acceptance. No priority or best-known claim is made.

## Read the complete principal argument

- [Reduced-lattice proof](REDUCED_LATTICE_BOUND_v1.md), including the finite sieve theorem, three local prime ranges, asymptotic estimates, complete endpoint budget and self-contained rational margin certificate
- [Full independent reduced-lattice audit](REDUCED_LATTICE_AUDIT_v1.md)
- [Independent mathematical reconstruction](REDUCED_LATTICE_INDEPENDENT_DERIVATION.md), preserved as a dated pre-acceptance reconstruction; its conditional acceptance wording is historical, and the full audit supplies the later decision
- [Acceptance and scope](ACCEPTANCE.md)

## Earlier square-root overhead result

The development first established

\[
\limsup_{k\to\infty}\frac{\log g(k)-\log L_k}{\sqrt{k}}\le13/5.
\]

That valid but weaker result and its complete review are preserved:

- [Full square-root proof](BONFERRONI_BOUND_v1.md)
- [Self-contained rational constant certificate](CONSTANT_CERTIFICATE_v1.md)
- [Classical sieve credit supplement](SIEVE_CREDIT_SUPPLEMENT_v1.md)
- [Full independent square-root audit](BONFERRONI_AUDIT_v2.md)

Its statements that its full-lcm construction does not imply g(k)<L_k refer to that earlier argument. The later reduced-lattice theorem above establishes the eventual comparison by a different construction. The square-root theorem is expressed relative to log L_k; the PNT alone does not justify replacing log L_k by k with an O(sqrt(k)) error.

## Exact structural results and a preserved real correction

- [Complete corrected transport proof v2](EXACT_TRANSPORT_v2.md)
- [Full independent structural review](TRANSPORT_INDEPENDENT_PROOF_REVIEW.md)
- [Correction history and exact counterexample](TRANSPORT_CORRECTION_HISTORY.md)
- [Full rejected v1 for comparison](EXACT_TRANSPORT_v1_SUPERSEDED.md)
- [Targeted structural source scope](TRANSPORT_SOURCE_SCOPE.md)

The accepted v2 proves the quotient-lcm identity, the all-factor smooth-part criterion, exact composite valuation defects, filtered boundary transport, and five properly restricted first-minimum consequences. The reviewer also gives a separate partial-fraction proof of the lcm identity. V1's fifth consequence omitted n>K+1 and is genuinely false: K=4, R=1, n=5 is a counterexample. V1 is not accepted as written. Its mathematical text is retained in full under an explicit warning.

Thirteen finite boundary minima were independently checked; those boundary minima must not be substituted for actual g(k). The structural audit retested 46 prior witnesses but freshly checked global minimality only for the 21 values within its bounded grid. The prior independent actual-minimality scope remains k<=46; no larger computational frontier is claimed here.

## Credit and literature limits

The lattice construction is credited to Ecklund, Erdős and Selfridge (1974). The finite lower sieve is classical Brun/Bonferroni machinery. Farhi's coefficient-row lcm identity and the previously known composite lattice are explicitly credited.

[Source scope and dated reconciliation](SOURCE_SCOPE.md) explains which source was inspected at each stage. [The full bounded literature comparison](LITERATURE_COMPARISON.md) distinguishes the actual minimum from the reciprocal-density approximant. It found no subsuming unconditional actual-minimum upper bound in the inspected sources, but does not establish novelty, priority or exhaustive coverage. Its reference to an earlier unaccepted coefficient near 0.936 describes an earlier candidate, not the final accepted 813/875 theorem.

## Preservation and distribution

The complete mathematical arguments, substantive independent reviews, counterexamples, aggregate diagnostic counts, source qualifications and limitations are included. Changes to structural texts only remove undistributed diagnostic identities, distinguish public-edition hashes, and make the actual correction history explicit. No mathematical step was shortened or replaced by a summary. The strongest proof, its audit, the square-root proof, its certificate and audit are byte-identical to their reviewed authored originals.

This is a prose edition, not an executable replay package. It contains no checker programs, raw diagnostic records or case certificates, source datasets, copied third-party PDF/text/images, or private coordination material. Its manifest hashes only actual members of this public directory; it does not inventory excluded evidence.

This appendix supplements the [earlier public partial-results packet](../README.md) in draft PR #1316. The earlier material remains historical and unchanged. In particular, its former statement that eventual g(k)<L_k was unresolved is superseded by the principal theorem here; the broader scale and ratio problems remain open.

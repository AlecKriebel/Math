# Source scope and dated reconciliation

12 October 2026. This authored account reconciles the source checks recorded in the included proof reports, independent audits and bounded literature comparison. It does not claim new retrievals during editorial preparation, a comprehensive priority search or a proof audit of every cited source.

## The actual-minimum baseline and classical sieve

E. F. Ecklund Jr., P. Erdős and J. L. Selfridge, *A New Function Associated with the Prime Factors of (n choose k)*, Mathematics of Computation 28 (1974), 647–649, [primary PDF](https://www.renyi.hu/~p_erdos/1974-01.pdf). Printed pp.648–649 give the classical lattice and the bound g(k)<k^2 L_k P_l with l=floor(6k/log k) for sufficiently large k. Its displayed construction gives secondary overhead (6+o(1))k/log k above log L_k and principal exponent 1. It also discusses the then-unproved lcm comparison. The square-root theorem sharpens the overhead of that construction. The reduced-lattice theorem separately gives the principal coefficient 813/875 and the eventual strict lcm comparison. Neither comparison by itself establishes literature-wide novelty.

Kevin Ford, *Sieve Methods Lecture Notes, Spring 2023*, Theorem 1.5 and Lemma 1.6, [author PDF](https://ford126.web.illinois.edu/sieve2023.pdf), and Terence Tao, *254A, Notes 4: Some Sieve Theory* (2015), equation (5), Exercise 9 and equation (13), [author notes](https://terrytao.wordpress.com/2015/01/21/254a-notes-4-some-sieve-theory/), supply the established Brun truncation and CRT remainder framework. Both were inspected. The finite sieve principle is not new here.

## The 2020 paper and 2021 addendum are distinct sources

Sorenson, Sorenson and Webster, *An Algorithm and Estimates for the Erdős–Selfridge Function*, Open Book Series 4 (2020), 371–385, [published article](https://doi.org/10.2140/obs.2020.4.371), [publisher PDF](https://msp.org/obs/2020/4-1/obs-v4-n1-p23-s.pdf). The bounded comparison inspected the published PDF, including text from Sections 1, 2, 5 and 6 and rendered printed pp.377–379. The actual-minimum comparison in Theorem 5.1 is conditional on the Uniform Distribution Heuristic; the unconditional fixed-k counting and reciprocal-density results do not locate the first admissible integer at the desired scale.

The [ANTS-hosted author manuscript](https://www.math.auckland.ac.nz/~sgal018/ANTS/papers/Sorenson-Sorenson-Webster.pdf) is marked submitted 3 June 2020. It is a submitted conference version, not the final published artifact. Separate proof and audit retrievals used it after the publisher endpoint provided no inspectable text. Their historical access limitations are preserved in the original reports; the later published-PDF inspection resolves that particular comparison gap.

The [arXiv v3 addendum](https://arxiv.org/abs/1907.08559v3), [full HTML](https://arxiv.org/html/1907.08559v3), [PDF](https://arxiv.org/pdf/1907.08559v3), is dated 1 June 2021. The actual document is a six-page addendum, even though abstract metadata describes a longer work-in-progress manuscript. Earlier reports checked only the abstract; later comparison and reduced-lattice audit checked the full addendum. Its asymptotic coefficient approximately 0.7884305 concerns log of the reciprocal-density approximant on the k/log k scale, not log of actual g on the k scale. Its ratio statement likewise concerns the approximant. Repository or arXiv availability does not establish editorial acceptance of an update.

## Structural antecedents and the narrow source correction

R. Scheidler and H. C. Williams, *A Method of Tabulating the Number-Theoretic Function g(k)*, Mathematics of Computation 59 (1992), 251–257, [author PDF](https://cspages.ucalgary.ca/~rscheidl/Papers/gk.pdf), explicitly retains the leading-digit filter.

R. F. Lukes, R. Scheidler and H. C. Williams, *Further Tabulation of the Erdős–Selfridge Function*, Mathematics of Computation 66 (1997), 1709–1717, [author PDF](https://cspages.ucalgary.ca/~rscheidl/Papers/es.pdf), contains the general finite residue-set sieve and the known composite lattice, the latter on printed p.1715 with credit to earlier work. The full structural review inspected that page and credits the lattice. The earlier correction of printed Lemma 3.8 remains narrow: an automatic-filter assertion fails, while the implementation retained filters. No table-wide failure is inferred.

Bakir Farhi, *An identity involving the least common multiple of binomial coefficients and its application*, [author preprint v2](https://arxiv.org/pdf/0906.2295v2), Theorem 1, gives the binomial-row lcm identity. Farhi, *Nontrivial lower bounds for the least common multiple of some finite sequences of integers*, Journal of Number Theory 125 (2007), 393–411, [author preprint](https://arxiv.org/pdf/0803.0290), Theorems 11–12 and the latter proof on preprint pp.14–15, supplies related interval-lcm and product-of-binomials arguments. The exact quotient-lcm presentation was not located in these targeted checks; that failure to locate it is not evidence of novelty.

## Bounds of the search

The [full bounded literature comparison](LITERATURE_COMPARISON.md) preserves the searches and classifications in detail. It includes Konyagin's 1999 lower-bound work only with an explicit full-text inspection gap; a 2026 van Doorn–Tang paper whose new theorem concerns EP451; and the Eastwood repository's reported finite tabulation through 400. These are not accepted substitutes for an unconditional actual-minimum upper theorem.

The original direct problem-page access failed; the 1993 Erdős–Lacampagne–Selfridge full text was not obtained in that pass; the full Konyagin paper was not inspected; no exhaustive citation-index search, author correspondence or inquiry into unpublished work was made. These gaps remain material. No source-author code was executed, and no copied source bodies are distributed.

The comparison's paragraph about an unaccepted principal-coefficient candidate near 0.936 is a preserved earlier-stage statement. The later frozen reduced-lattice proof and its full independent audit, both included here, accept the exact coefficient 813/875. The comparison itself is not an acceptance report.

# Source and status gate: AIM-CRYPTOGRAPHY-0028

Checked 2026-10-21. Queue 1865; database ID 20001341. This is an authored source-recovery and scope audit, not a new research result, solution, or novelty claim.

## Source identity and current disposition

The primary 2019 AIM workshop report, *Quantum algorithms for analysis of public-key crypto*, page 4, Miscellaneous, attributes to Dan Bernstein a request to compute short units in the ring of integers of the specific field defined by x^312−x^156−1, including achievable shortness and speed. The AIMPL locator is section 6, item 4; direct retrieval of its HTTPS page timed out, but the independently retrieved AIM report verifies the mathematical statement. The report's schedule identifies 4–8 February 2019. Search-engine crawl/publication timestamps are not the workshop date.

Primary source: https://aimath.org/pastworkshops/quantumalgrep.pdf
AIMPL locator: http://aimpl.org/quantumalg/6/

The source does NOT specify a norm, height, logarithmic weighting, regulator objective, non-torsion restriction, number of independent units, or target approximation factor. It specifies one field, not an arbitrary-degree input-field problem. The generated title describes a proposed elementary partial calculation; it is not the original question's title or a primary-source theorem.

Disposition: source identity passes; metric and completion gate remains open. This audit found no primary source resolving the exact fixed-field optimization question. That limited negative search is not proof of open status, nor does it justify declaring an exact shortest-unit problem solved. There is no source basis to silently select the easiest norm as the intended meaning.

## What the elementary radical calculation does and does not establish

Let phi=(1+sqrt(5))/2, alpha=phi^(1/n) positive real, and L_n=Q(alpha). The existing all-n calculation is mathematically consistent at the elementary checkpoints below; this audit does not certify originality or a complete unit-group computation.

- Irreducibility must precede treating the quotient as a field. Over K=Q(sqrt(5)), its ring of integers has units ±phi^k. Hence phi is not a q-th power in K for any prime q: a putative root is an integral unit and its exponent would satisfy qk=1. The exceptional binomial obstruction for 4 dividing n is also absent: phi cannot belong to −4K^4, either by the positive real embedding or by the inert valuation at 2. The binomial criterion yields degree n over K, hence degree 2n over Q. A complete research proof should cite a precise statement of that criterion rather than rely on the name alone.
- Both parities give exactly two real embeddings; signature is (2,n−1). At n=156 this is degree 312, signature (2,155), unit rank 156. The real embedding forces roots of unity to be ±1. The fields are not totally real for n>1, and are not cyclotomic.
- Alpha is integral from its monic polynomial, and alpha^(-1)=alpha^(2n−1)−alpha^(n−1) is an integral inverse. This establishes a unit of Z[alpha] and therefore of the full ring of integers without proving Z[alpha] maximal.
- The power-order discriminant is (−1)^(n−1)5^n n^(2n). Possible index primes divide n, by the relative discriminant over Q(sqrt(5)); for the fixed instance these are 2,3,13. No maximal-order identification or exact index has been checked here.
- There are n conjugates of modulus phi^(1/n) and n of reciprocal modulus. Writing a=log(phi), the canonical Minkowski squared norm, counting all embeddings or equivalently weighting real/imaginary complex coordinates by sqrt(2), is 2n cosh(2a/n).
- AM–GM gives a universal Minkowski length lower bound sqrt(2n) for units. Equality is torsion, here ±1. Comparing alpha to this lower bound gives a factor sqrt(cosh(2a/n)) above the optimum non-torsion Minkowski unit, but does not show alpha attains that optimum. At n=156 the factor is approximately 1.0000095153, and alpha's length is approximately 17.6636898064.
- House is phi^(1/n), absolute logarithmic Weil height is a/(2n), and Mahler measure is phi. These are different objectives, not alternative labels for the Minkowski calculation.
- A logarithmic embedding weighted sqrt(2) at complex places has length sqrt(2n)a/n; the product-formula embedding weighted 2 there has length sqrt(4n−2)a/n. At n=156 these are approximately 0.0544865098 and 0.0769319756 respectively. Neither is accompanied by a field-specific shortest-vector certificate or near-minimality ratio in that metric.
- A coefficient vector of length 1 in the displayed power order is representation-dependent. It says nothing about an arbitrary integral basis of the maximal order.
- The displayed unit can be output immediately in a prescribed representation. O(n) dense coordinate output and sparse descriptions are not a uniform algorithm for solving shortest-unit problems in arbitrary input number fields, nor a gate-count analysis of quantum unit algorithms.
- Divisor-indexed elements 1±alpha^m can be verified using geometric-series inverse identities when m divides n. Such a list by itself supplies neither rank 156 nor saturation, a fundamental system, or the regulator. The regulator is a covolume/determinant of a full-rank logarithmic unit lattice, not the length of a single short vector.

The near-1 Minkowski ratio is partly a baseline phenomenon: every unit's norm starts at sqrt(degree). It must not be transferred to the logarithmic norm, house excess above 1, height, or regulator. Taking roots of a unit changes the field and degree; the construction is applicable here because the actual AIM polynomial has this radical structure. It is not a solution for arbitrary prescribed fields.

## Current primary-literature check

1. Eisenträger, Hallgren, Kitaev, Song, *A quantum algorithm for computing the unit group of an arbitrary degree number field*, STOC 2014. The author-hosted paper states complexity polynomial in degree and log discriminant. Its unit-group output is not an exact shortest logarithmic-unit certificate for this field.
   https://doi.org/10.1145/2591796.2591860
   https://www.cse.psu.edu/~sjh26/units-stoc.pdf
2. Biasse and Song, *An efficient quantum algorithm for computing S-units and its applications*, arXiv:2510.02280v2, 24 November 2025, long version of SODA 2016. Theorem 1 supplies compact S-unit representations; applications to class groups have stated hypotheses. The revised introduction discusses a coefficient-size typo and competing complexity analysis. This source must not be reduced to a claim that every cryptographic short-vector or fixed-field exact-SVP question is solved.
   https://arxiv.org/abs/2510.02280
   https://arxiv.org/html/2510.02280v2
3. Bernstein and Lange, *Non-randomness of S-unit lattices*, IACR ePrint 2021/1428. The archive lists it as a preprint/minor revision. It studies short-vector and reduction behavior and warns against spherical models for S-unit lattices. The abstract is not a solution to the fixed AIM field.
   https://eprint.iacr.org/2021/1428
4. Dobrowolski, *On a question of Lehmer and the number of irreducible factors of a polynomial*, Acta Arithmetica 34 (1979), 391–401, DOI 10.4064/aa-34-4-391-401. Degree-dependent lower bounds concern Mahler measure/height, not a full regulator or a shortest-unit certificate for one field.
   https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/34/4/102213/on-a-question-of-lehmer-and-the-number-of-irreducible-factors-of-a-polynomial
5. Dimitrov, *The Schinzel–Zassenhaus conjecture*. The publisher currently lists acceptance on 27 August 2026 and forthcoming publication; its house bound is degree-dependent. This is distinct from Lehmer's proposed uniform positive bound on log Mahler measure. In this radical family h(alpha) tends to zero while (2n)h(alpha)=log(phi) and M(alpha)=phi stay constant. Consequently this construction neither disproves nor solves Lehmer's problem. No inference of a current Lehmer resolution is made from isolated preprint titles.
   https://annals.math.princeton.edu/articles/22975
   https://arxiv.org/abs/1912.12545

## Evidence and boundaries

The fixed field and attribution were checked against the original report's last page. Bounded exact-field searches did not locate a resolving primary paper; this is not proof of open status. General quantum algorithm references were checked separately. This package contains authored analysis and public bibliographic metadata, not copied source documents.

Before further research: explicitly choose or condition on the meaning of short; distinguish non-torsion vectors from torsion; specify whether one vector, independent units, a basis, or regulator is sought. A full acceptance claim requires that chosen target and a certificate appropriate to it, not merely the existing root-of-unit construction.

### Additional workshop-context inspection

The workshop companion page https://pqcrypto.org/2019-aim.html was also inspected. Its glossary defines SVP generically, and its schedule lists a talk on unit groups and lattice-attack working groups, but gives no metric for Bernstein's fixed-field problem and no additional independence or non-torsion requirement. No slide link is supplied there for the unit-group talk. The adjacent Miscellaneous questions in the report concern sphere covering, HHL, and Simon's algorithm, not a convention defining short units. The report ends immediately after the fixed-field question. Therefore logarithmic intent is plausible cryptographic context, not a recovered explicit specification. A repeated HTTP AIMPL fetch redirected to HTTPS and timed out again.

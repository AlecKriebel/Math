## Accepted partial results; full absolute-bound target unresolved

For B_n=binom(2n,n), let f(n)=sum 1/p over primes p<=n with p not dividing B_n.
This prose-only edition preserves the complete substantive mathematical proof
and independent audit. No substantive mathematical correction was required.

- Exact valuation, digit and residue criteria characterize nondivisibility.
- The contribution at n=q^r rules out every summable all-n envelope depending
  only on shell depth, even after deleting any fixed finite prime set.
- Testing only L(n)=o(log n) common carry levels gives an unbounded relaxation.
  For each fixed c>0, testing floor(c log(2n)) levels differs from f by at most
  the reciprocal sum of the finitely many odd primes p<exp(1/c).
- For every fixed r, F_r(n) tends along all integers to
  2^(-r) log(1+1/r), derived from Sander's published exponential-sum estimate.
  Constants and thresholds may depend on r; no uniformity or infinite-sum
  interchange is claimed.
- With c0=sum_{k>=2} log(k)/2^k, the EGRS first moment gives liminf f(n)=c0.
  The prime-3 subsequence gives liminf f(3^m)>=c0+1/3, and the published EGRS
  two-base theorem strengthens this to limsup f(n)>=c0+8/15.

The two-base hypothesis is non-strict and includes bases 3 and 5 at equality.
There is no extension here to arbitrary finite prime sets. The cutoff
construction does not produce actual simultaneous nondivisibility. Deep-shell
reciprocal mass remains uncontrolled: sup_n f(n)<infinity is neither proved
nor refuted. The empty prime set in the sublogarithmic theorem is explicitly
clarified as vacuous; this is an editorial clarification, not a theorem change.

Published inputs are credited to
[Erdős, Graham, Ruzsa and Straus, On the prime factors of (2n choose n)](https://www.renyi.hu/~p_erdos/1975-27.pdf),
[Sander, On primes not dividing binomial coefficients](https://doi.org/10.1017/S0305004100075927), and
[Sander, Prime power divisors of binomial coefficients](https://doi.org/10.1515/crll.1992.430.1).
Standard earlier analytic results are accepted published inputs. No novelty,
priority, exhaustive literature coverage or full solution is claimed.

“Accepted” means an independent internal AI audit of these partial results.
This AI-assisted edition is unrefereed. No external human peer review,
journal acceptance or formal proof-assistant certification is claimed.

Historical independent finite checks covered 1,797,533 valuation/digit/residue
pairs through n=5000, 48,013 literal-binomial comparisons through n=700, and
14,340,272 exact integer-cutoff comparisons. Independent normal/-O/-OO receipts
are byte-identical; 16 inventory controls passed per mode. These checks do not
prove asymptotic statements. Decimal values are approximations, not interval
certificates. The advertised 10^8 computation was not repeated.

Executable code, raw datasets, full certificates, detailed receipts, copied
third-party sources and private coordination are excluded. This is not an
executable reproduction package. Preparation verified source-package byte
integrity and publication structure without a new mathematical test run or
scholarly-source inspection. Original proof and audit packages are unchanged.

Exactly eight public proof/audit/acceptance and source/verification metadata
files are additions under attempts/2083. QUEUE.md and all unrelated paths
remain unchanged.

## Exact public-file identities

- `ACCEPTANCE.json`: 2,369 bytes; SHA-256 `a9de247ba2cc0cf7cb54b67b285a49197285278579842adc4c3469e0021a8dfa`.
- `ACCEPTANCE.md`: 3,457 bytes; SHA-256 `239c6e4c6399d16708012ca404bf3587eaeecc14e5cfc1d3cd2bff9c4c1031a9`.
- `AUDIT.md`: 16,362 bytes; SHA-256 `13a8e0d280b42651795b203d954c83e80cbda72d91698a700c7bb006bd18a4c0`.
- `MANIFEST.json`: 1,643 bytes; SHA-256 `26909f0aa02e65c53d2e415096cea3f8aa8ed27ba4daf28205661853bb599099`.
- `PROOF.md`: 15,065 bytes; SHA-256 `6785a6badab8b09e65439544e1cdea095af96593829d827155d28814145b2c10`.
- `README.md`: 3,549 bytes; SHA-256 `534c082004ff94224a35dcb1459c3fe1fbf24b193f0bf2c466581a6d4419828f`.
- `SOURCES.json`: 3,731 bytes; SHA-256 `b9ca4e88658034bd2b3fd0bb559b1f5867f082f0c65a475fef55f928f79dcfce`.
- `VERIFICATION.json`: 2,364 bytes; SHA-256 `441a3ea52ecb6d5374faca9d51af24490205efd422d0415b13326ef77b17d7ed`.

MANIFEST.json lists all eight members and hashes the other seven; this body independently pins its digest.


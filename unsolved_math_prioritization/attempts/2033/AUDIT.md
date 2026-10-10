# Independent audit: harmonic-coprime partial avoidance

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the explicitly stated partial theorems; no external human peer review, journal acceptance, or formal proof-assistant certification is claimed. The complete substantive proof and independent mathematical audit are retained. No mathematical correction was required. Historical finite tests and rigorous arithmetic bounds are described, but executable programs, detailed receipts, full computational certificates, raw datasets, and copied source documents are omitted. This edition is not an executable reproduction package. Edition preparation did not rerun mathematical tests or newly inspect scholarly sources.

## Verdict and exact scope

**ACCEPTED AS AN UNCONDITIONAL PARTIAL RESULT.** Theorem A, Corollaries A1–A2, and Theorem B of the frozen candidate are mathematically justified. No proof correction is required for those statements. In particular:

- Every fixed finite set of primes can be excluded from `q_n = gcd(L_n H_n,L_n)` on arbitrarily long intervals having endpoint ratio `6/5`.
- The corresponding finite-prime survivor set has positive lower natural density.
- The set avoiding only leading digit `p−1`, for every odd prime with `p <= n`, has lower logarithmic density strictly greater than `283/2000 = 0.1415`.

This is **not acceptance of a solution to EP-291 / problem 2033**. Infinitude of `q_n=1` remains unresolved by this packet. The non-universal harmonic zero digits are uncontrolled. No novelty, priority, exhaustive literature search, formal proof-assistant verification, or world-record computation is certified.

The original candidate was unchanged throughout the audit. Its original proof document is 12,997 bytes, SHA-256 `fe0b1380a12f57732ee6d5e237ae42366d3c0df15df7d816b41391f6d106fa41`. The candidate manifest and author freeze matched the separately supplied anchors:

- Manifest: `01f53eae04b81c5d59c4ffcfd5d0a5b75a2a0915463cd5cc4e3c8fbcc8a46021`
- Author freeze: `fe5853437721d4b9af2699fbff7a7d2897a2d669d22dee5d1602559c654aadc8`

Historically, all 13 listed candidate members, all 8 original public members, and all 9 archived public entries matched their pinned identities. Those original distributions are distinct from this prose-only edition. Hash matching authenticates bytes; the mathematical acceptance below comes from independent reasoning and arithmetic.

## 1. Local obstruction criterion reconstructed

Let `H_n=c_n/d_n` be reduced. Since `d_n` divides `L_n`, set `q_n=L_n/d_n`. Then `L_n H_n=c_n q_n`, so

`gcd(L_n H_n,L_n)=q_n gcd(c_n,d_n)=q_n`.

For a prime `p <= n`, choose the unique integer `e >= 1` with `p^e <= n < p^(e+1)` and put `m=floor(n/p^e)`. Thus `1 <= m < p`. Write `L_n=p^e M`, with `p` not dividing `M`. An index `j <= n` with `p^e` not dividing `j` has strictly smaller p-adic valuation, so `L_n/j` is divisible by `p`. The remaining indices are `r p^e`, for `1 <= r <= m`, and contribute `M/r` modulo `p`. Consequently

`L_n H_n ≡ M sum_{r=1}^m r^(-1) (mod p)`.

The factor `M` must be retained; it is a unit and can be canceled for the zero test. Because `p` divides `L_n`, the zero test is equivalent to `p | q_n`. This establishes exactly the candidate's interval union over harmonic zero digits and exponents `e >= 1`.

There are two important boundary checks:

1. For `p=2`, only `m=1` is possible and its reciprocal sum is nonzero. Thus every `q_n` is odd. Pairing inverses to show that `p−1` is a zero digit applies only to odd primes.
2. If `p>n`, then `p` cannot divide `q_n`, even when the single-digit value `n` happens to have harmonic numerator divisible by `p`. For example, `p=3,n=2` is not an obstruction. Allowing exponent zero would misstate the exact criterion.

This agrees with Shiu's Theorem 2, including its odd-prime and positive-exponent conventions. The candidate has corrected both source-transcription hazards.

## 2. Quantitative finite-prime avoidance

Fix a nonempty finite odd-prime set `S`, size `r`, maximum `P`. Put `eta=log(6/5)` and choose an integer `Q >= log(P)/eta`. For `X >= 2P`, partition the unit r-cube into `Q^r` half-open cubes. Among the `Q^r+1` vectors with coordinates `k log(X)/log(p) mod 1`, two lie in one cube. Their difference supplies

`1 <= j <= Q^r`, and integers `b_p` satisfying `|j log X − b_p log p| < eta`.

No rational independence statement is involved. The integers `b_p` are positive: otherwise the absolute difference would be at least `log X >= log(2P) > eta`.

For any real `n` in `[(5/4)X^j,(3/2)X^j]`, the preceding strict error estimate gives

`25/24 < n/p^(b_p) < 9/5 < 2 <= p`.

Thus `p^(b_p)` is the largest p-power below `n` and the leading digit is exactly 1. The local criterion excludes every prime in `S`. The real interval length is `X^j/4`, which tends to infinity at least as fast as `X/4`; relative to its left endpoint the length is `1/5`. Including endpoints causes no problem because the ratio bounds are strict.

Adding the harmless prime 2 gives Corollary A1. This argument fixes `S` before choosing arbitrarily large `X`; it makes no assertion about excluding primes that grow with the output integer.

## 3. Positive lower natural density without higher-order independence

Let `Phi(t)=(t/log p mod 1)_{p in S}` and let `G` be the closure of its image in the finite torus. The image is a subgroup, so `G` is a compact subgroup. For the symmetric open identity neighborhood given by coordinate distances `< eta/log p`, orbit translates cover `G`: density gives a translate containing each point. Compactness gives a finite subcover centered at `Phi(t_i)`. Set `B=max |t_i|`.

For every real `t`, some `u=t−t_i` lies in `[t−B,t+B]` and is within `eta` of integer multiples of every `log p`. For sufficiently large `t` those multiples have positive exponents. Therefore the complete interval `[(5/4)e^u,(3/2)e^u]` is good.

Given large `x`, choose `t=log(2x/3)−B`. Its good interval is below `x`, and its length is at least `x e^(−2B)/6`. A real interval of length `ell` contains at least `ell−1` integers. Dividing by `x` and taking the lower limit proves lower natural density at least `e^(−2B)/6 > 0`.

The argument uses recurrence near the identity of the actual closure. It never replaces that closure by the full torus. Possible rational relations among three or more reciprocal logarithms do not invalidate it. If the prime set is empty after discarding 2, all positive integers survive directly.

## 4. Universal-digit logarithmic density

For an odd prime `p`, let `C_p` be the union of integer intervals `[(p−1)p^e,p^(e+1))`, `e >= 1`, and put `delta_p=log(p/(p−1))/log p`.

### Fixed-prime and pairwise averages

After a bounded initial interval in logarithmic time, membership in `C_p` is periodic with period `log p` and occupied length `log(p/(p−1))`. This gives logarithmic density `delta_p`.

For distinct primes `p,l`, a nonzero integer relation `h/log p+k/log l=0` would force a rational ratio of prime logarithms and hence an equality of positive powers of distinct primes. Unique factorization excludes that. Every nontrivial character of the two-dimensional continuous flow consequently has time average zero, by direct integration of an exponential of nonzero frequency. Trigonometric approximation and rectangle-boundary measure zero then give the joint density `delta_p delta_l`.

This is continuous-time equidistribution, so the condition concerns vanishing frequency, not an extra independence condition involving 1. Only pairs are used. The relevant instance is

`delta(C_p \ C_3)=(1−delta_3)delta_p`, for `p >= 5`.

Discrete harmonic averages match continuous logarithmic averages: obstruction endpoints are integers, so the indicators are constant on each `[n,n+1)`. The total error is bounded by the convergent positive series `sum (1/n−log(1+1/n))`. A final partial unit interval contributes a bounded, vanishingly normalized endpoint error. The same applies to intersections and differences.

### Infinite tail and order of limits

For integers `A<B`, comparison with an integral gives

`sum_{A <= n < B} 1/n <= log(B/A)+1/A`.

At most `log x/log p` positive-exponent intervals for `C_p` meet `[1,x]`. The endpoint errors sum to at most

`sum_{e>=1} 1/((p−1)p^e)=1/(p−1)^2`.

Hence the candidate's uniform bound

`sum_{n<=x, n in C_p} 1/n <= delta_p log x + 1/(p−1)^2`

is valid, including a truncated final obstruction interval.

For `m=2^j`, each prime in `(m,2m]` divides the integer binomial coefficient `binom(2m,m)<4^m`. If there are `k` such primes, their product exceeds `m^k`; therefore `k < 2m/j`. Also, `log(p/(p−1))<1/(p−1)<=1/m` and `log p>j log 2`. The block sum is consequently less than `2/(j^2 log 2)`. This proves convergence of the entire sum `D=sum delta_p` without invoking the prime number theorem.

Using `log 2>2/3` and monotone integral comparison,

`sum_{p>2^20} delta_p < 3 sum_{j>=20} j^(−2) <= 3(1/400+1/20)=63/400`.

For any cutoff `y`, sum the uniform bound over `p>y`. At fixed `x`, only finitely many sets are nonempty, because their first point is `p(p−1)`. The endpoint-error sum is nevertheless bounded uniformly in `x` by the convergent sum over all `p>y`. After division by `log x` and then taking `limsup`, the upper logarithmic density of the tail union is at most `sum_{p>y}delta_p`, which tends to zero. Thus the infinite-union passage is justified; there is no interchange of an uncontrolled infinite sum and a density limit.

### Final lower bound

For a finite cutoff use the set inclusion

`union C_p ⊆ C_3 union union_{5<=p<=y}(C_p\C_3) union union_{p>y}C_p`.

Apply the finite union bound, the established pairwise difference densities, and the vanishing upper-density tail. The result is

`lower_delta(U) >= (1−delta_3)(1−D+delta_3)`.

The exact finite computation below gives `sum_{3<=p<=2^20}delta_p<47/50`, so `D<439/400`. Integer-power comparisons give `1/3<delta_3<2/5`. Both factors are positive, and hence

`lower_delta(U) > (3/5)(1−439/400+1/3)=283/2000>7/50`.

All strict inequalities needed for the advertised strict bound are preserved.

## 5. Historically recorded independent exact bounds and finite checks

The original auditor read the candidate Python as text but did not execute or import it. The independently authored checker used a different prime sieve (Euler least factors), a different high-precision logarithm enclosure (directed power recurrence), and a different obstruction sieve (prefix inverses and interval difference arrays). Programs, detailed receipts, masks and full computational certificates are omitted from this prose-only edition; the following describes historical verification, not executable reproduction from the distributed files.

The logarithm certificate starts from the elementary positive series for `2 atanh z`, with `z=(a−b)/(a+b)`. At scale `10^36`, a lower and an upper integer enclose each successive scaled odd power. Multiplication by the exact nonnegative rational `z^2` and directed rounding preserve that enclosure. Each positive term is rounded outward, and the entire remaining tail is bounded geometrically. Forty terms give rigorous numerator and denominator intervals. Dividing a lower numerator by an upper positive denominator and conversely gives directed quotient bounds.

The resulting independent enclosure is

`934535274480325630534232545311397126 / 10^36`

`<= sum_{3<=p<=1048576} delta_p <=`

`934535274480325630534232545311755307 / 10^36`.

It lies inside the candidate's stated interval. A separate auditor-authored exact-term rounding reconstruction also reproduced both candidate endpoints verbatim:

`934535274480325630395660 / 10^24`, and

`934535274480325643460226 / 10^24`.

The prime inventory contains 82,025 primes, including 82,024 odd primes; its largest member is 1,048,573. Trial division independently checked primality classification through 2,000. Exact `Fraction` calculations checked the analytic partial-sum and remainder enclosures at six ratios including 1, 2, and the near-1 large-prime ratio.

Additional checks:

- Reduced rational harmonic numbers and independently incremented unreduced `L_n H_n` agree through 2,000. All 329,253 eligible `(n,p)` local-criterion comparisons pass; every `q_n` is odd.
- All complete-sieve counts through 1,000,000 agree. There are 2,641 coprime values through 10,000 and 138,902 through 1,000,000. Both full one-million-entry mask hashes match the candidate, beyond just matching aggregate counts.
- The universal-digit sieve is generated independently of the harmonic zero-digit list, preventing the distinction between the two from being hidden by a shared construction.
- All five stored finite-prime interval witnesses are verified by exact integer inequalities over the whole real interval. Their exponents satisfy `j<=Q^r` for certified `Q=7,9,11,14,15`, respectively. No enormous harmonic numbers or floating-point logarithms are needed for these checks.
- `n=33` is in `U` but `q_33=11`; the exceptional leading digit for 11 is 3 and `H_3=11/6`. This conclusively blocks identifying `U` with the full coprime set.

Historically recorded normal, `-O`, and `-OO` independent runs produced identical deterministic mathematical results. The computation tests finite arithmetic and proof ingredients; it is not a replacement for the infinite arguments in Sections 2–4.

## 6. Literature and source-version review

During the original audit, the principal retained PDFs were read as complete local text, their byte hashes and page counts were rechecked, and the decisive theorem pages were visually inspected. Official web records/PDFs current at that time were also checked. The edition retains this inspection history without claiming a new source inspection.

- Peter Shiu, *The denominators of harmonic numbers (Revised)*, arXiv:1607.02863v2, revised 30 July 2024. The actual PDF has eight pages, despite the arXiv comments field saying seven. Theorem 2 is the positive-exponent local criterion; Theorem 3 is the fixed-prime logarithmic density. Theorem 4 is stated with a finite-family logarithmic-independence hypothesis. The coprime counting estimate is explicitly conjectural. None of the candidate's unconditional steps relies on the conditional alignment theorem. [Versioned record](https://arxiv.org/abs/1607.02863v2), [PDF](https://arxiv.org/pdf/1607.02863v2).
- Bing-Ling Wu and Xiao-Hui Yan, *On the denominators of harmonic numbers. IV*, Comptes Rendus Mathématique 360 (2022), 53–57, DOI 10.5802/crmath.282. Its six PDF pages include a cover. Conjecture 1 concerns finite-family rational independence of reciprocal prime logarithms; Theorem 2 is conditional upper natural density one for smaller reduced denominators, equivalently `q_n>1`. It is not a theorem on full density, coprime infinitude, or an unconditional conclusion. The official article landing page failed in this audit's web tool, but the complete [official PDF](https://comptes-rendus.academie-sciences.fr/mathematique/item/10.5802/crmath.282.pdf) was accessible.
- Carlo Sanna, *On the p-adic valuation of harmonic numbers*, J. Number Theory 166 (2016), 41–46, DOI 10.1016/j.jnt.2016.02.020. Theorem 1.3 of the [institutional author manuscript](https://iris.unito.it/bitstream/2318/1622121/1/padicharm.pdf) provides logarithmic density greater than 0.273 for a fixed-prime maximal-valuation set. Its leading-digit lemmas are relevant prior work, and do not themselves yield simultaneous control of every prime. This was a web inspection; no new local PDF hash is represented for that source.

The earlier seven-page source description was corrected to eight pages, consistently with the actual PDF. The prior direction/hypothesis corrections concerning Wu–Yan and the prime-2 exception are retained correctly. Direct access to the maintained EP-291 tracker failed, so no fresh full tracker inspection is certified. Bounded search does not establish novelty or exclude all intervening literature.

## 7. Residual problem and verification limitation

Writing `R_p` for the intervals arising from zero digits other than `p−1`, the exact full target is unboundedness of

`U \ union_p R_p`.

No estimate in the candidate controls that last union within `U`. Positive lower density for each fixed finite-prime survivor set does not survive passage to infinitely many full obstructions without uniform estimates. Pairwise independence does not supply multiwise product formulas. Positive logarithmic density of `U` does not imply anything comparable for its smaller coprime subset. These limitations are accurately stated in the candidate.

There is one nonblocking engineering warning: the original candidate integrity verifier and arithmetic checker use Python `assert` statements for checks. Python optimization removes those guards, so their optimized execution must not be used as an integrity certificate. No candidate code was executed for the original independent audit. The independently authored audit tools instead use explicit exceptions; their historical normal, `-O`, and `-OO` passes and controlled rejection tests are recorded in the original audit. Its verifier requires an externally supplied manifest hash and checks archive membership and byte identity. These programs and detailed receipts are omitted here. VERIFICATION.json preserves historical verification identities and this limitation; the public MANIFEST.json authenticates this edition's prose and metadata, not mathematical truth.

**Acceptance is limited to the frozen partial theorems and the finite verification claims listed here. Full EP-291 remains open within this work; no proof patch is necessary for the accepted scope.**

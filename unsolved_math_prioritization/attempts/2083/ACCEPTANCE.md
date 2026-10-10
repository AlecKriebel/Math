# Acceptance of EP377 / 2083 partial results

This prose-only edition is AI-assisted and unrefereed. “Accepted” means an
independent internal AI audit of the stated partial results. No external human
peer review, journal acceptance or formal proof-assistant certification is
claimed. No novelty or priority is claimed. The absolute-bound target remains
unresolved by this work.

Source inspection and finite computations described below are historical
activities of the original proof and independent audit, not new work performed
to prepare this edition. No new mathematical test or scholarly-source inspection
was performed during edition preparation. Executable code, raw datasets,
detailed receipts, full computational certificates and copied third-party
sources are excluded. This is not an executable reproduction package.

## Accepted mathematical scope

No substantive mathematical correction was required by the independent audit.
The exact valuation, residue and digit criteria are proved, including exclusion
of prime 2. For odd q and r >= 1, the moving contribution at n=q^r rules out
every summable all-n majorant depending only on shell depth, even after any
fixed finite set of primes is removed. This is not unboundedness of f.

The common cutoff H_L is unbounded when L(n)=o(log n). The construction first
fixes a nonempty finite prime set and then takes sufficiently large powers of
its product. The empty set is vacuous and is explicitly clarified editorially.
For each fixed c>0, L_c(n)=floor(c log(2n)) differs from the full predicate only
at odd primes p<exp(1/c), with total error at most their reciprocal sum. No
uniformity in c or classification of arbitrary oscillating cutoffs is claimed.

For every fixed r, the all-integer limit is
F_r(n) -> 2^(-r) log(1+1/r). The proof derives this from Sander's published
exponential-sum estimate using fixed endpoint trimming, fixed Fourier
frequencies, partial summation, Mertens' theorem, boundary approximation and
then removal of the trimming. The constants and thresholds need not be uniform
in r, and no interchange with the infinite shell sum is permitted.

Writing c0=sum_{r>=1} 2^(-r) log(1+1/r)=sum_{k>=2} 2^(-k) log k, the fixed-shell
limits and the EGRS first moment give liminf f(n)=c0. The prime-3 subsequence
gives liminf f(3^m)>=c0+1/3. The published EGRS two-base theorem, whose
non-strict hypothesis includes bases 3 and 5 at equality, gives the stronger
limsup f(n)>=c0+8/15. There is no extension here to arbitrary finite prime
sets and no sharpness claim. Density convergence is compatible with failure
of ordinary convergence.

The all-n absolute-bound target sup_n f(n)<infinity remains unresolved.
Historical exact finite checks corroborate predicates and examples only;
normal, -O and -OO independent receipts agree. No 10^8 computation was
repeated. Decimal values are approximations, not interval certificates.

## Exact edition binding

- PROOF.md: 15,065 bytes; SHA-256 `6785a6badab8b09e65439544e1cdea095af96593829d827155d28814145b2c10`.
- AUDIT.md: 16,362 bytes; SHA-256 `13a8e0d280b42651795b203d954c83e80cbda72d91698a700c7bb006bd18a4c0`.

ACCEPTANCE.json preserves the original accepted claims and limitations, and adds these editorial edition identities. MANIFEST.json enumerates the complete eight-file public selection. SOURCES.json preserves the public bibliographic, byte-identity and historical inspection evidence for EGRS75, Sander93 and Sander92.

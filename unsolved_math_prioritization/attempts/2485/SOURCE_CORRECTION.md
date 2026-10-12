# Leading-digit filters cannot be dropped

Authored mathematical correction, 12 October 2026. This addresses one printed lemma and its density calculation. It does not challenge the source's numerical table or assert a paper-wide failure.

Source: R. F. Lukes, R. Scheidler and H. C. Williams, *Further tabulation of the Erdős–Selfridge function*, Mathematics of Computation 66 (1997), 1709–1717. Author-hosted primary PDF: https://cspages.ucalgary.ca/~rscheidl/Papers/es.pdf . The definitions are on printed p.1710, Lemma 3.8 on p.1712, and the implementation's filter-retention description on p.1714. The actual PDF pages were rendered and inspected; the capture and exact quotation are retained privately.

## 1. A counterexample satisfying the sieve definition

For each prime p<=k, put a=floor(log_p k). The paper first retains the digits below position a, then filters on the digit in position a. The assertion in Lemma 3.8 that this second test is automatic at a prime parameter is false as printed.

Take the prime parameter k=q=3 and the candidate n=5. The domain condition n>=k+2 holds. At p=2, k=11_2 and n=101_2: the lower digit is 1, so the sieve condition holds, but the digit in position 1 is 0<1, so the filter fails. At p=3, k=10_3 and n=12_3: the lower digit 2>=0 and the leading digit 1>=1 both pass. Hence n satisfies every lower-digit congruence required for a candidate, yet C(5,3)=10 is divisible by 2.

The failure is systematic. For every k>=2, n=k+L_k is a lower-sieve candidate: n is congruent to k modulo p^{floor(log_p k)} for every p<=k. Let a=floor(log_2 k). The binary digit of k at position a is 1, while v_2(L_k)=a. Adding L_k preserves every lower binary digit and changes the digit in position a to 0. Thus the leading binary filter fails. In particular every prime parameter has such a false candidate. This is an infinite family of failures of the claimed automatic filter, not just a low-index anomaly.

## 2. The local density argument can be repaired

The defect does not prevent the intended density comparison. Let delta(k) be the exact density of integers satisfying all prime constraints at parameter k. Fix a prime q>=3. For p<q, write q-1 in base p and let d_p=(q-1) mod p. Incrementing q-1 to q causes no base-p carry, because p does not divide q. Thus the units digit changes from d_p to d_p+1, and all higher digits, including the leading digit and its filtering factor, remain the same. Therefore the ratio of the *full* local densities is

\[
\frac{\delta_p(q)}{\delta_p(q-1)}
=\frac{p-d_p-1}{p-d_p}.
\]

There is also the new prime q itself. Since the base-q expansion of q is 10, its full local density is (q-1)/q. Multiplying the independent CRT factors gives the exact identity

\[
\frac{\delta(q)}{\delta(q-1)}
=\frac{q-1}{q}\prod_{p<q}\frac{p-d_p-1}{p-d_p}
\le \prod_{p<q}\left(1-\frac1p\right).
\]

Every denominator is positive, and d_p<=p-2. This proves the desired comparison without suppressing any leading-digit filter. By Mertens's product theorem it yields the reciprocal-density model's logarithmically large prime-step ratio. It does not imply that ratio for actual g.

## 3. Narrow consequence for the source

Two errors are visible in the printed proof: n>p does not ensure that floor(n/p^a) remains positive after reduction modulo p; and q=p+(q-p) is not a valid two-digit base-p expansion for arbitrary p<q. The explicit counterexample is sufficient regardless of the proof discussion.

Section 5 explicitly says that candidates passing the lower congruences were checked against the leading-digit condition by an on-line filter, with further off-line filters for folded congruences. Therefore the printed lemma alone does not establish an error in the implementation or published table. No source-author code was executed here, no table was invalidated, and no claim is made that this correction is previously unknown.

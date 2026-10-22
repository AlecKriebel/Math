# Independent audit: actual bounds for the Erdős–Selfridge function

Date: 2026-10-12. Scope: the three analytical claims below and a supplemental review of the exact-minimum verifier for k <= 46.

## Verdict

**PASS, with explicit scope qualifications.** The prime-transition characterization and finite union-bound construction are correct. The proposed asymptotic consequence follows after making the fixed-epsilon limiting argument explicit. Lemma 3.8 in Lukes–Scheidler–Williams (1997) is false as printed; its precise hypotheses admit the counterexamples below. The paper expressly retains the relevant filter in its implementation, so this defect alone does not invalidate its table.

These are partial results and a correction to a printed lemma. They do not settle the conjectured exponential scale exp(Theta(k/log k)), the eventual inequality g(k) < lcm(1,...,k), or either successive-ratio conjecture. No novelty or first-discovery claim is certified.

## 1. Exact transition at a prime

Write A_k(n) for the conjunction n > k+1 and p not dividing C(n,k) for every prime p <= k. Fix a prime q >= 3 and an integer n > q+1, and put m=n-1. Then

A_q(n) if and only if A_(q-1)(m), gcd(n, product_{p<q} p)=1, and n mod q^2 >= q.

**Proof.** Put X=C(n,q), Y=C(n-1,q-1). The identity nY=qX gives, for each prime p<q,

v_p(n)+v_p(Y)=v_p(X).

All valuations are nonnegative integers. Therefore v_p(X)=0 is equivalent to both v_p(n)=0 and v_p(Y)=0. The remaining prime q divides neither condition for A_(q-1). By Lucas's theorem, q does not divide C(n,q) exactly when the coefficient of q in the base-q expansion of n is nonzero, equivalently n mod q^2 >= q. The domain n>q+1 implies m>q, precisely the required domain for A_(q-1).

Taking n=g(q) proves g(q) >= g(q-1)+1. This is an actual-minimum inequality, not a density heuristic. It establishes neither unbounded ratios nor divergence of the gaps.

## 2. Exact finite upper-bound construction

Fix an integer k>=3 and a real cutoff 0<=y<=k. Define

- L=lcm(1,...,k), P_y=product_{p<=y} p, M=L P_y;
- a_p=floor(log_p k), b_p=floor(k/p^{a_p});
- D=sum_{y<p<=k} b_p/p and B=sum_{y<p<=k} b_p.

If D<1 and the integer T satisfies T>B/(1-D), then at least one n=tM-1 with 1<=t<=T satisfies A_k(n). Consequently g(k)<=T L P_y-1. Specifying the index set for B avoids ambiguity; a larger B obtained by summing over every prime <=k is also safe, but weaker.

**Proof.** For p<=y, M is divisible by p^{a_p+1}, so the lowest a_p+1 digits of n are p-1 and every Lucas requirement for k is automatic. For y<p<=k, write M=p^{a_p}c_p, with p not dividing c_p. The lowest a_p digits of n are p-1. Its remaining relevant digit is

floor(n/p^{a_p}) mod p = (t c_p-1) mod p.

It fails precisely when t c_p mod p belongs to {1,...,b_p}. Thus exactly b_p nonzero residue classes of t modulo p fail. Each residue class contributes at most T/p+1 integers in [1,T], so the total number of failed candidates is at most TD+B<T. At least one survives. The domain n>k+1 is automatic: L_3-1=5>4, and for k>=4, L_k>=k(k-1), hence L_k-1>k+1.

**Asymptotic consequence.** Fix epsilon>0 and set y=(1+epsilon)k/log k. For sufficiently large k, sqrt(k)<y<k, so a_p=1 on the tail. Partial summation of the prime number theorem yields

D <= k sum_{p>y} p^{-2} = (1+o(1)) k/(y log y) = 1/(1+epsilon)+o(1) < 1.

Moreover B<=k pi(k)=o(k^2), so T=k^2 meets the strict finite inequality for all sufficiently large k, with epsilon fixed. Using theta(y)=log P_y~y gives

log g(k) <= log L_k + (1+epsilon+o(1)) k/log k.

Since this holds for every fixed epsilon>0, the upper limsup of (log g(k)-log L_k)/(k/log k) is at most 1. This is equivalently the claimed upper bound

log g(k) <= log L_k + (1+o(1)) k/log k.

One must not silently treat a fixed epsilon as an o(1) quantity. No effective threshold, explicit vanishing epsilon(k), or uniform quantitative PNT error is supplied here.

**Prior-art limitation.** Ecklund–Erdős–Selfridge (1974), printed pp.648–649, already uses the same family t L_k P_y-1, T=k^2, and y approximately 6k/log k, and notes that its constant can be reduced. The finite exact digit count sharpens the bookkeeping of that classical construction. The coefficient-1 secondary term is mathematically justified but is not certified as new. Since log L_k~k, the main exponential order remains the classical exp((1+o(1))k).

## 3. Printed Lemma 3.8: exact hypotheses and counterexamples

**Source pin.** R. F. Lukes, R. Scheidler and H. C. Williams, *Further tabulation of the Erdős–Selfridge function*, Mathematics of Computation 66 (1997), 1709–1717, DOI [10.1090/S0025-5718-97-00864-8](https://doi.org/10.1090/S0025-5718-97-00864-8). The supplied original PDF has 177,371 bytes and SHA-256 4faa018e64beb39e2c7863540062bb5a0eb22427cdf3b9409b4656f3a62c45cf.

- Printed pp.1710–1711 (physical PDF pages 2–3), Section 2: for each prime p<=k, m=floor(log_p k); (2.3) tests digits 0 through m-1, while (2.4) separately tests digit m. Search candidates have n>=k+2. The full condition requires both tests for every prime.
- Printed p.1712 (physical PDF page 4): Lemma 3.8 assumes k=q is prime, and asserts automatic satisfaction of (2.4) for every solution candidate for either g(q) or g(q-1). The original page was visually inspected; this is not an OCR-only reading.

**First branch, every hypothesis checked.** Choose q=k=3 and n=5.

1. q is prime; n=5>=k+2=5.
2. At p=2, m=1 and k=(11)_2. Condition (2.3) requires n mod 2=1, which holds.
3. At p=3, m=1 and k=(10)_3. Condition (2.3) permits every residue modulo 3, including n mod 3=2. Thus all lower-digit congruences hold.
4. At p=2, floor(5/2) mod 2=0<1, violating (2.4). Equivalently C(5,3)=10 has prime divisor 2<=3.

This directly refutes the g(q) branch under the paper's candidate definition. There is no extra assumption in the statement restricting candidates to n below a prime square.

**Second branch.** The same prime q=3 also admits k=q-1=2 and n=4. Its domain n>=k+2 holds. The only lower-digit sieve, for p=2, imposes no restriction because k=(10)_2. But floor(4/2) mod 2=0<1. Thus the g(q-1) branch is false as well.

**Uniform family.** For every integer k>=2, n=k+L_k has n>k+1 and n congruent to k modulo p^{floor(log_p k)} for every prime p<=k. Every lower-digit sieve therefore holds. If a=floor(log_2 k), then v_2(L_k)=a. Adding L_k leaves the lower a binary digits unchanged but changes the digit at position a from 1 to 0. The top binary filter fails. This covers prime and nonprime parameters without any numerical-search assumption.

**Faults in the printed proof.** An inequality n>p does not ensure that floor(n/p^m) reduced modulo p is positive. Also, the expression q=p+(q-p) is not generally a valid two-digit base-p expansion: q-p need not lie between 0 and p-1. The first issue already invalidates the proof at q=3.

**Implementation caveat.** Printed p.1714 (physical PDF page 6), Section 5, explicitly describes a filter checking (2.4) on every value surviving (2.3); residue-folding losses receive an additional software filter. This original page was also visually inspected. The lemma defect does not establish an implementation error or invalidate any tabulated value. Conversely, this description is not a replay of the implementation and does not independently certify the whole historical table. The subsequent probability argument's use of Lemma 3.8 needs a replacement justification; failure of that justification is not by itself a counterexample to every resulting inequality.

## 4. Independent checks and supplemental certificate audit

A separately retained independently written checker uses no author-packet implementation. The aggregate record in VERIFICATION.json reports passing checks of 25,708 prime-transition cases against exact binomial integers; the counterexample family for 2<=k<=1000; and all 2,669 cutoff pairs with D<1 for 3<=k<=80 and integer 0<=y<=k. Its bad-residue checks cover 614,438 residues. These are regression checks, not replacements for the proofs above.

The supplemental exact-minimum verifier was inspected and replayed. For each prime p it uses the least power Q=p^e>k, builds the full local admissibility table from exact C(r,k) modulo p for 0<=r<Q, and counts valid residues in exclusion intervals using complete periods and an inclusive prefix count. Periodicity follows from (1+X)^Q congruent to 1+X^Q modulo p, because k<Q. For r<k the coefficient is zero, correctly represented by the table.

Its required interval partition starts at k+2, is contiguous, and ends at the proposed n. Every interval has a prime p<=k dividing every represented binomial coefficient. The endpoint is separately checked with exact C(n,k). This proves minimality for each accepted record. The replay passed all 46 records, with 2,562,964 exclusion intervals. The author's advance routine is also logically consistent: it raises the highest failed base-p digit and resets all lower digits to their componentwise minima. The verifier does not depend on that reasoning or import that routine. No source-author code was executed in this audit.

Scope of this replay: k=1,...,46 only. It does not independently certify later minima or the 1997 implementation. Original input hashes and aggregate replay results accompany this report in ORIGINAL_INPUT_PINS.json and VERIFICATION.json; executable programs and raw interval certificates are not distributed.

## References and source-status qualification

- Ecklund, Erdős and Selfridge, *A New Function Associated with the Prime Factors of C(n,k)*, Math. Comp. 28 (1974), 647–649: [original PDF](https://users.renyi.hu/~p_erdos/1974-01.pdf).
- Lukes, Scheidler and Williams (1997), cited above: original supplied PDF, visually inspected pp.1712 and 1714; Section 2 and surrounding discussion checked in extracted text. A fresh web-tool retrieval of the AMS PDF/DOI was unavailable; conclusions use the pinned supplied original.
- Sorenson, Sorenson and Webster, *An algorithm and estimates for the Erdős–Selfridge function*, Open Book Series 4 (2020), 371–385: [original PDF](https://msp.org/obs/2020/4-1/obs-v4-n1-p23-s.pdf). Its pp.371–372 distinguish the genuine function from the density approximant and the uniform-distribution heuristic.
- The [Eastwood repository](https://github.com/AlexanderEastwood/erdos-selfridge) README, as inspected for this 12 October 2026 audit, reports a complete table through 400 and distinguishes witness checks from paired exhaustive-scan evidence. It was read only for source status in this audit; no new minimum from that repository was replayed here. Avoid presenting 375 as the present computational frontier.

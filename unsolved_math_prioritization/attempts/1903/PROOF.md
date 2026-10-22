# Whole-fiber transport and an explicit lower bound for least totient preimages

**Scope.** Write \(\mathcal V=\varphi(\mathbb N)\), \(F(a)=\{n\ge1:\varphi(n)=a\}\), \(m(a)=\min F(a)\), and \(R(a)=m(a)/a\). Erdős's question asks whether \(R(a)\) is unbounded on \(\mathcal V\). This note does **not** settle that question. It proves an unconditional infinite-family bound strictly stronger than 2, using a classical whole-fiber theorem and an independently checked finite seed. The finite divisor classification was verified locally; its complete certificates and executable checks are not distributed in this prose edition. No claim of priority for the transport theorem or its elementary consequences is made.

## 1. Results

Put
\[
 D=575651577856=2^{17}\cdot23\cdot257\cdot743,
 \qquad M=1177105133055=3\cdot5\cdot17\cdot47\cdot257^2\cdot1487,
\]
and
\[
 r_* =\frac{M}{D}=\frac{4580175615}{2239889408}
      =2.044822212490233\ldots .
\]

**Theorem.**
1. \(m(D)=M\), and \(F(D)\) has exactly nine elements, classified in Section 3.
2. For all but \(o(x/\log x)\) primes \(p\le x\),
   \[
   F(D(p-1))=pF(D),\quad m(D(p-1))=pM,
   \quad R(D(p-1))=r_*\frac p{p-1}>r_*.
   \]
   Consequently an infinite set of totients has ratios tending to \(r_*\) from above. In particular,
   \[
   \limsup_{a\in\mathcal V,\ a\to\infty}R(a)\ge r_* >2.0448.
   \]
3. More generally, every attained value \(R(d)\) is a limit of ratios at arbitrarily large totients from above. The global supremum equals the limsup at infinity, and both are strictly greater than every individually attained value (with the extended-real interpretation if unbounded).
4. Using the stronger published counting lemma in Section 4, there is a constant \(c_D>0\) such that, for all sufficiently large \(x\),
   \[
   \#\{a\in\mathcal V:a\le x,\ R(a)>r_*\}\ge c_D\,\#(\mathcal V\cap[1,x]).
   \]
   No useful explicit value for \(c_D\) is asserted.

Parts 2–4 are deductions from existing scholarly theorems, not new analytic-number-theory inputs. Part 1 is established independently by the elementary argument and finite deterministic classification described below. The omitted classification certificates can be reconstructed from the stated divisor formula; their contents are not part of this edition.

## 2. The classical whole-fiber input

Erdős, *Some remarks on Euler's φ function*, Acta Arithmetica 4 (1958), 10–19, proof of Theorem 4, pp. 15–18, establishes the following: for every fixed totient \(d\), outside \(o(x/\log x)\) primes \(p\le x\), the solutions of \(\varphi(y)=d(p-1)\) are exactly \(y=pn\) with \(\varphi(n)=d\). See the [original scan](https://renyi.hu/~p_erdos/1958-18.pdf), especially the start and end of the proof.

The original theorem's headline concerns multiplicity, but the proof establishes this stronger fiber identity. For \(p>d+1\), every old preimage is coprime to \(p\), because a prime \(q\) dividing an old preimage satisfies \(q-1\mid d\), hence \(q\le d+1\). Thus all scaled old solutions exist; Erdős proves that additional solutions occur for only the stated exceptional set. The finite exclusion \(p\le d+1\) does not affect the asymptotic statement.

Pollack–Pomerance–Treviño explicitly restate the whole-fiber interpretation in the introduction of *Sets of monotonicity for Euler's totient function*, Ramanujan Journal 30 (2013), 379–398. Their term is that \(p\) is “convenient” for \(d\): [author-hosted paper, p. 2](https://math.dartmouth.edu/~carlp/MonotonePhi.pdf).

Taking minima in the fiber identity proves Part 2, including its quantifier over **all** preimages. Distinct primes give distinct values \(D(p-1)\), which tend to infinity. The exact factor \(p/(p-1)\) tends to 1. The number of these family members at most \(X\) is asymptotic to \(X/(D\log X)\), by the prime number theorem and the exceptional-set estimate.

For Part 3, apply the same argument with any fixed \(d\). If \(S=\sup_{a\in\mathcal V}R(a)\) and \(L\) is the limsup at infinity, then \(L\ge R(d)\) for every \(d\), while \(L\le S\); hence \(L=S\). Select one convenient prime \(p>2\) and set \(d'=d(p-1)\). Since \(R(d')>R(d)\), applying the result once more gives \(L\ge R(d')>R(d)\). A finite global supremum, if it exists, is therefore not attained.

## 3. Exact finite fiber: no census assumption

If \(q\) is prime and \(q\mid n\) with \(\varphi(n)=D\), then \(q-1\mid D\). Enumerate all 144 divisors
\[
 2^i23^j257^k743^\ell,\qquad
 0\le i\le17,\quad j,k,\ell\in\{0,1\}.
\]
The prime values of one plus these divisors are exactly
\[
2,3,5,17,47,257,1487,11777,65537,188417,380417,6086657,279986177.
\]
This finite classification of all 144 divisor-plus-one candidates was independently verified locally. For every rejected candidate, a proper integer factor was checked; the 13 retained candidates were proved prime by deterministic trial division through the integer square root, without a probable-prime assumption. The complete factor tables, JSON certificates, and executable checking code are excluded from this prose edition. A reader can reconstruct the classification by generating exactly the divisors in the displayed formula and applying deterministic trial division to each divisor plus one. This finite verification remains a proof dependency; this edition does not distribute all of its computational certificates. The proof below would also work with a superset of candidate primes, provided the rejected cases all have proper factors.

Their predecessor factorizations are:

| Prime q | q−1 |
|---:|:---|
| 2 | 1 |
| 3 | 2 |
| 5 | 2² |
| 17 | 2⁴ |
| 47 | 2·23 |
| 257 | 2⁸ |
| 1487 | 2·743 |
| 11777 | 2⁹·23 |
| 65537 | 2¹⁶ |
| 188417 | 2¹³·23 |
| 380417 | 2⁹·743 |
| 6086657 | 2¹³·743 |
| 279986177 | 2¹⁴·23·743 |

No \(q-1\) on this list is divisible by 257. The factor 257 in \(D\) must therefore come from the prime-power term \(q^{e-1}\) in the totient formula, forcing \(257^2\Vert n\). All other odd candidate primes occur at most once: none of them divides \(D\). (The primes 23 and 743 divide \(D\), but they are not candidate prime divisors of \(n\).)

The forced factor \(257^2\) consumes eight of the seventeen powers of 2 in \(D\). The remaining budget is nine. A factor 23 must come from one of 47, 11777, 188417, or 279986177; a factor 743 must come from one of 1487, 380417, 6086657, or 279986177. The common carrier 279986177 costs fourteen powers of 2 and cannot occur. Every carrier other than 47 and 1487 costs at least nine, and the other required carrier costs at least one. Thus **47 and 1487 are forced**, and the other carriers are excluded. The factor 65537 also exceeds the remaining budget.

Put \(C=47\cdot257^2\cdot1487\). Every preimage consequently has the form
\[
 C\,2^e\prod_{q\in T}q,\qquad T\subseteq\{3,5,17\},\ e\ge0.
\]
Write \(s(T)=\sum_{q\in T}v_2(q-1)\), with weights 1, 2, 4. The residual totient equation is
\[
 \max(e-1,0)+s(T)=7.
\]
For \(e=0\), binary uniqueness forces \(T=\{3,5,17\}\). For even preimages, \(e=8-s(T)\) for each of the eight subsets. Therefore the complete fiber is
\[
 F(D)=\{255C\}\ \cup\
 \left\{C\,2^{8-s(T)}\prod_{q\in T}q:T\subseteq\{3,5,17\}\right\}.
\]
The odd member is \(255C=M\). Every even member is at least \(256C\), because
\[
 2^{8-s(T)}\prod_{q\in T}q
 =256\prod_{q\in T}\frac q{q-1}\ge256>255.
\]
This proves both minimality and completeness, without any upper search cutoff on \(n\).

The sorted fiber is

1177105133055, 1181721231616, 1255578808592,
1477151539520, 1569473510740, 1772581847424,
1883368212888, 2215727309280, 2354210266110.

### Relation to the earlier finite seed

The same argument with \(d_0=387383296=2^{16}\cdot23\cdot257\) and \(C_0=47\cdot257^2\) gives \(m(d_0)=791597265=255C_0\) and the same nine-element formula. Thus
\[
 F(D)=1487F(d_0),\qquad D=1486d_0.
\]
For the older seed, enumerate the 68 divisors 2^i23^j257^k with 0≤i≤16 and j,k∈{0,1}, and classify one plus each divisor by deterministic trial division. All 68 cases were independently verified locally, as were the 144 cases for D. The finite identity follows from these two classifications and the displayed fiber argument; the excluded factor tables and certificates can be reconstructed from these formulas. It does not require the asymptotic transport theorem to apply at the small prime 1487. This distinction matters because “almost all primes” supplies no certificate for a particular small prime.

The older seed was reported on the [August 2026 SciNet claim page](https://api.scinet.pub/f/2c289002-70f6-45bd-8624-440601935d9a). That page labels its results partial and awaiting independent review. Its ratio-2 theorem and large census are not used here. The cited seed motivated the calculation, and its full fiber has been independently re-established above. No claim is made that the larger explicit seed is a global computational record.

## 4. Positive lower relative density

The second imported input is Lemma 4.1 of Pollack–Pomerance–Treviño, together with their Section 4 comparison \(V(x)\asymp Z(x)\), where \(V(x)=\#(\mathcal V\cap[1,x])\). For fixed totients \(d_1,d_2\) and fixed \(B\ge\max(d_1,d_2)\), it supplies \(\gg_B V(x)\) integers \(u\) with \(\varphi(u)\le x/B\) and exact fiber scaling for both seeds. The lemma also bounds \(u/\varphi(u)\), which is unnecessary here. This is an unconditional published lemma, used as a black box; its underlying Ford estimates are not reproved in this note.

Set \(d_1=d_2=B=D\). For each supplied \(u>1\), put \(a=D\varphi(u)\le x\). Fiber scaling gives
\[
 m(a)=Mu,\qquad R(a)=r_*\frac u{\varphi(u)}>r_*.
\]
The map \(u\mapsto a\) is injective on these convenient integers: equal \(a\)'s would have equal least preimages, hence \(Mu=Mv\) and \(u=v\). Removing \(u=1\) discards at most one value. Thus the number of distinct qualifying totients is \(\gg_D V(x)\), proving Part 4. More generally, the same argument works above every attained seed ratio.

## 5. Local verification, distribution limits, and remaining gap

The local verification used three routes: residual-divisor inverse-totient recursion, fixed-support prime-power enumeration, and the closed fiber formula. Both enumeration methods cover the entire fiber, by the factorization formula for φ. All three agreed for both seeds. Small inputs \(a\le100\) were independently compared against every \(n\le20000\). This small check is complete because \(\varphi(n)\ge\sqrt{n/2}\): each odd prime-power factor contributes at least 1 to \(\varphi(n)^2/n\), and the 2-primary factor contributes at least 1/2. Hence \(\varphi(n)\le100\) implies \(n\le20000\). These checks support the elementary proof; they do not certify the imported analytic theorems by computation.

The verification was run normally and under Python `-O` and `-OO`; its required checks did not use removable `assert` statements. Missing divisor rows, false primality, invalid proper factors, and changed candidate identities were rejected. These are reports of local verification. The executable checks, detailed outputs, factor tables, and JSON certificates are not distributed here; the reader is left to reconstruct the finite classifications as described in Section 3. The complete proof dependencies include those classifications and the expressly imported scholarly theorems.

**Why this is still partial.** For a fixed seed the transported ratios converge to a finite constant. Repeatedly choosing convenient primes produces strict increases, but Erdős's theorem is for each fixed seed and gives no uniform bound on how large the next usable prime may have to be. It does not show that the successive reciprocal increments have divergent sum. Nor does the density constant above have a seed-independent positive lower bound. There is no proved sequence of seeds with ratios tending to infinity. The least-preimage divergence problem remains unresolved by this work.

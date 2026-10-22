# Density-zero representability and coprime failures in three ranges

Row 1671 / problem 2497 / Erdős Problem 1110. Independent elementary reconstruction and scope correction, 11 October 2026. This is a bounded partial result already attributed to Yu–Chen (2022), not a novel theorem or a resolution of the entire problem.

## Definitions and precise result

Fix coprime **integers** $p>q\geq 2$; neither base is assumed prime. Put

\[
 S_{p,q}=\{p^kq^\ell:k,\ell\in\mathbb Z_{\geq0}\}.
\]

A positive integer is representable if it is the sum of a finite set of distinct members of $S_{p,q}$, no two of which divide one another. Write $R_{p,q}(N)$ for the number of representable positive integers at most the positive integer $N$. Thus coefficients are one, exponents may be zero, all summands are positive, and a singleton is allowed. Allowing an empty sum would add only zero and would not affect any density assertion.

**Theorem.** In each of these ranges,

1. $q\geq4$;
2. $q=3$ and $p\geq7$;
3. $q=2$ and $p\geq11$,

there are constants $C>0$ and $0<\alpha<1$, depending at most on the bases, such that $R_{p,q}(N)\leq C N^\alpha$ for every $N\geq1$. Representable integers consequently have natural density zero, and non-representable positive integers have natural density one. There is also an infinite strictly increasing sequence of non-representable integers that are pairwise coprime and each coprime to $pq$.

The exact pairs outside these three ranges, under the stated integer and coprimality hypotheses, are

\[
 (3,2),\ (5,2),\ (7,2),\ (9,2),\ (4,3),\ (5,3).
\]

The pair $(3,2)$ is separately fully representable. The other five pairs are **outside this proof's density conclusion**; this wording makes no claim that they are all globally unresolved. In particular, $(4,3)$ must not be omitted merely because $4$ is composite.

## 1. Divisibility is the product order

For nonnegative integers $a,b,c,d$,

\[
 p^a q^b\mid p^c q^d\quad\Longleftrightarrow\quad a\leq c\text{ and }b\leq d.
\]

The reverse implication is immediate. For the forward implication, choose any prime $r\mid p$. Coprimality gives $r\nmid q$, so comparison of $r$-adic valuations gives $a v_r(p)\leq c v_r(p)$, hence $a\leq c$. A prime dividing $q$ similarly gives $b\leq d$. This also proves uniqueness of the exponent pair representing a member of $S_{p,q}$. The argument works unchanged when a base is composite or a proper prime power.

## 2. Count the antichains

Set $K=\lfloor\log_pN\rfloor$ and $L=\lfloor\log_qN\rfloor$. In a representation of a positive integer $n\leq N$, positivity implies that every summand is at most $N$. Each exponent pair therefore lies in

\[
 P=\{0,\ldots,K\}\times\{0,\ldots,L\}.
\]

The preceding equivalence identifies a pairwise non-dividing set of summands with an antichain in the coordinatewise order on $P$.

An antichain of size $s$ has $s$ distinct first coordinates: two points with the same first coordinate would be comparable. It likewise has $s$ distinct second coordinates. After choosing the two coordinate sets and listing the first coordinates increasingly, the second coordinates must decrease strictly. This reverse pairing is both necessary and sufficient for incomparability, so there is exactly one antichain for each such pair of coordinate sets. Consequently the number of antichains, including the empty one, equals

\[
 A(K,L)=\sum_{s\geq0}\binom{K+1}{s}\binom{L+1}{s}
       =\binom{K+L+2}{K+1}.
\]

Here binomial coefficients outside their usual ranges are zero. For the last identity, put $r=K+1,c=L+1$, replace $\binom cs$ by $\binom c{c-s}$, and count the $c$-element subsets of a disjoint union of sets of sizes $r,c$, according to how many elements are chosen from the first set. This is the elementary Vandermonde identity.

Every representable positive integer at most $N$ is the sum of at least one counted antichain. A single antichain has only one sum. Different antichains can have the same sum, and some counted antichains have sums exceeding $N$, but both facts only make this an overcount. Thus

\[
 R_{p,q}(N)\leq A(K,L)=\binom{K+L+2}{K+1}.
\]

No injectivity of the map from antichains to sums is required.

## 3. The power saving, with exact arithmetic

Fix $0<t<1$. One term of the nonnegative binomial expansion of $(t+(1-t))^{K+L+2}=1$ gives

\[
 \binom{K+L+2}{K+1}t^{K+1}(1-t)^{L+1}\leq1.
\]

As $K\leq\log_pN$, $L\leq\log_qN$, and the bases $1/t,1/(1-t)$ exceed one,

\[
 R_{p,q}(N)\leq\frac{1}{t(1-t)}
 N^{\alpha(p,q,t)},\qquad
 \alpha(p,q,t)=\frac{\log(1/t)}{\log p}
             +\frac{\log(1/(1-t))}{\log q}.
\]

The following choices give strict inequalities without relying on floating-point logarithms.

### Range 1: $q\geq4$

Because $p>q$ are integers, $p\geq5$. Choose $t=1/2$, so $C=4$. Then

\[
 \alpha\leq\log_5 2+\log_4 2<\tfrac12+\tfrac12=1,
\]

where $\log_5 2<1/2$ is exactly $2^2<5$.

### Range 2: $q=3, p\geq7$

Choose $t=1/3$, so $C=9/2$. Since

\[
 3^5=243<343=7^3,\qquad 3^5=243<288=3^2 2^5,
\]

we have $\log_7 3<3/5$ and $\log_3(3/2)<2/5$. Therefore

\[
 \alpha=\log_p3+\log_3(3/2)
 \leq\log_7 3+\log_3(3/2)<1.
\]

### Range 3: $q=2, p\geq11$

Choose $t=1/4$, so $C=16/3$. The exact inequalities

\[
 4^{12}=16,777,216<19,487,171=11^7,
\]
\[
 4^{12}=16,777,216<17,006,112=2^5 3^{12}
\]

give $\log_{11}4<7/12$ and $\log_2(4/3)<5/12$. Hence

\[
 \alpha=\log_p4+\log_2(4/3)
 \leq\log_{11}4+\log_2(4/3)<1.
\]

All monotonicity comparisons keep the logarithm argument fixed and greater than one, while increasing its base.

## 4. Densities and the coprime sequence

For each fixed allowed pair, division by $N$ gives

\[
 0\leq R_{p,q}(N)/N\leq C N^{\alpha-1}\longrightarrow0.
\]

The number of non-representable positive integers at most $N$ is exactly $N-R_{p,q}(N)$, so its quotient by $N$ tends to one. This proves existence as well as the values of the natural densities.

For any fixed positive integer $M$, the integers coprime to $M$ occupy exactly $\varphi(M)$ residue classes modulo $M$. Their count up to $N$ is therefore

\[
 \frac{\varphi(M)}{M}N+O(M).
\]

Subtracting the at most $C N^\alpha$ representable integers leaves at least

\[
 \frac{\varphi(M)}{M}N-O(M)-C N^\alpha
\]

non-representable integers coprime to $M$. For fixed $M$, this expression tends to infinity.

Start with the empty list. If $n_1<\cdots<n_s$ have already been chosen to be non-representable, pairwise coprime, and coprime to $pq$, set

\[
 M=pq\prod_{i=1}^s n_i.
\]

The preceding count supplies a non-representable $n_{s+1}>\max(1,n_s)$ coprime to $M$; for the empty list use the threshold $1$. It is coprime to $pq$ and to every earlier choice. Repeating this step constructs the asserted infinite sequence. No uniform estimate in $M$ is needed: $M$ is fixed at each finite induction step. Positive density alone for the failure set would not justify this argument, since, for example, all its elements could share a prime divisor.

## 5. The separately known pair $(3,2)$

For completeness, here is the classical induction underlying the exceptional representable case. The integers $1,2$ are singleton sums. Suppose representations are available for smaller positive integers. An even $n=2m$ is represented by multiplying a representation of $m$ by $2$; multiplying all terms by the same positive integer preserves non-divisibility. For odd $n$, let $3^a\leq n<3^{a+1}$. If $n=3^a$, use a singleton. Otherwise $n=3^a+2m$ with $0<m<3^a$ and $m<n$. Double the terms in a representation of $m$ and adjoin $3^a$. All doubled terms are even, so none divides the odd term $3^a$. If $3^a$ divided a doubled term $2u$, it would divide $u\leq m<3^a$, which is impossible. This proves every positive integer representable for $(3,2)$. This argument is classical, not an original claim here; see Erdős–Lewin, Proposition 1, printed p. 837.

## Attribution and limits

Erdős–Lewin (1996), printed p. 840, posed the density and coprime-failure questions. The current search-indexed Erdős Problem 1110 page attributes the three density ranges above to Yu–Chen (2022). This note independently proves that bounded result, so the density direction does not depend on obtaining Yu–Chen's full theorem text. The imported statement that **non-representables** have density zero in these ranges must instead say **representables** have density zero, equivalently failures have density one.

The tracker reports coprime-failure results also for $(4,3)$ and $(7,2)$. Those two extensions are not proved here. Yu–Chen's publisher metadata and abstract were available through search indexing, but the full paper was not obtained or inspected; no theorem number, exact theorem quotation, or inspection of their proof is claimed. The tracker is used only to report its attribution and status, not as the mathematical justification for this proof. No conclusion here resolves all parameter pairs or determines the density in any of the five uncovered pairs.

References:

- P. Erdős and Mordechai Lewin, *d-Complete Sequences of Integers*, Mathematics of Computation 65 (214) (1996), 837–840. Inspected primary facsimile: https://www.brand.site.co.il/riddles/201507a_files/2153618.pdf
- Wang-Xing Yu and Yong-Gao Chen, *On a conjecture of Erdős and Lewin*, Journal of Number Theory 238 (September 2022), 763–778. https://doi.org/10.1016/j.jnt.2021.09.018 ; publisher record https://www.sciencedirect.com/science/article/pii/S0022314X21003358
- T. F. Bloom, Erdős Problem 1110, https://www.erdosproblems.com/1110 . Search-indexed record checked 11 October 2026; live direct page fetch returned HTTP 403. Its displayed last-edit date was 1 April 2026, which is not a guarantee that the index reflects every subsequent change.

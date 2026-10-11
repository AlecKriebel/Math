# Independent, table-free certificate for the unweighted parity conjecture

## Result and attribution

The unweighted conjecture is false. This is an independent verification and elementary reconstruction of the prior counterexample of Olga Katkova, Boris Shapiro, and Anna Vishnyakova, *In search of Newton-type inequalities*, Section 5, arXiv:2403.12200v1, p. 20. That work was published in *Journal of Mathematical Analysis and Applications* 538(1) (2024), article 128349, DOI [10.1016/j.jmaa.2024.128349](https://doi.org/10.1016/j.jmaa.2024.128349). No new-disproof or priority claim is made. The quantitative root splitting below is a robustness certificate for the same published obstruction.

The statement being tested is Conjecture 10 on p. 4 of Boris Shapiro, [*Problems around polynomials: the good, the bad and the ugly ...*, arXiv:1503.05295v1](https://arxiv.org/pdf/1503.05295v1). For a degree-n polynomial with positive coefficients, set

\[
 c_k=a_k^2-a_{k-1}a_{k+1},\qquad a_{-1}=a_{n+1}=0.
\]

Select every k in {0,...,n} for which c_k is nonnegative, in increasing order. Let v be the number of changes of parity between consecutive selected indices. The conjectured upper bound on the number of real roots is v. In particular, zero differences would be selected. Both endpoint differences are strictly positive. The source labels the selected indices k_1,...,k_m but prints i=0 under its parity sequence; we use the ordered list actually defined, with i=1,...,m. No undefined k_0 is added.

## 1. The published seed, normalized to integer coefficients

Consider

\[
 P(x)=(1+x)^{13}(38x^2-89x+83).
\]

It is 720720 times KSV's polynomial Q_15 on p. 20: their quadratic coefficients are 19/360360, -89/720720, and 83/720720. Positive scalar multiplication preserves roots, coefficient signs, and the signs of every c_k.

Put B_k=binom(13,k), with B_k=0 outside 0<=k<=13. The coefficient of x^k is

\[
 a_k=83B_k-89B_{k-1}+38B_{k-2}
     =\binom{15}{k}\big((k-9)^2+2\big),\qquad 0\le k\le15.
\]

Indeed, division by binom(15,k) gives the numerator

\[
83(15-k)(14-k)-89k(15-k)+38k(k-1)
 =210(k^2-18k+83)
\]

over 210. This identity also holds at the endpoints under the zero-extension convention. It proves that every coefficient is strictly positive without an expansion table.

The quadratic discriminant is

\[
 (-89)^2-4\cdot38\cdot83=-4695<0.
\]

Thus the quadratic has no real zero. Its value at -1 is 210, so -1 has multiplicity exactly 13 in P. Consequently P has exactly 13 real zeros counting multiplicity, and exactly one distinct real zero.

For 1<=k<=14 define the positive ratio

\[
 q_k=\frac{a_k^2}{a_{k-1}a_{k+1}}
 =\frac{(k+1)(16-k)}{k(15-k)}
   \frac{((k-9)^2+2)^2}{((k-10)^2+2)((k-8)^2+2)}.
\]

Since the denominator a_{k-1}a_{k+1} is positive, c_k<0 if and only if q_k<1. Substitution gives

\[
 q_8=\frac{27}{28},\qquad q_9=\frac{140}{243},\qquad
 q_{10}=\frac{99}{100}.
\]

These ratios are positive, not negative. Their differences from 1 are respectively -1/28, -103/243, and -1/100. Therefore c_8,c_9,c_10 are negative.

For completeness, the claim that these are the only negative differences has a table-free proof too. Write t=k-9. Direct subtraction yields

\[
 q_k-1=\frac{N(t)}{k(15-k)(t^4+2t^2+9)},\quad
 N(t)=14t^4-6t^3+177t^2+15t-206.
\]

The denominator is positive. At t=-1,0,1 the numerator is respectively -24,-206,-6. If |t|>=2, then t^2(14t^2-6t)>0. Also, with u=|t|>=2,

\[
 177t^2+15t-206\ge177u^2-15u-206
 \ge\frac{339}{2}u^2-206\ge472>0,
\]

where 15u<=(15/2)u^2 was used. Hence N(t)>0 for all other relevant integer t. The endpoints satisfy c_0=a_0^2>0 and c_15=a_15^2>0. There are no zero differences.

The selected sequence is therefore 0,1,...,7,11,12,...,15. The first block has seven parity changes; the gap from 7 to 11 has none; the last block has four. Thus

\[
 v(P)=11<13.
\]

This disproves the multiplicity-counted formulation.

## 2. A parity-deletion lemma

The distinct-root proof will need only the three strict exclusions, rather than the signs of all other differences. Removing an interior entry from any finite binary sequence cannot increase its number of changes: for binary values u,w,z,

\[
 \mathbf1_{u\ne z}\le\mathbf1_{u\ne w}+\mathbf1_{w\ne z}.
\]

Iterating this inequality proves that a subsequence has no more parity changes than the original sequence. In degree 15, every selected list that omits 8,9,10 is a subsequence of 0,1,...,7,11,12,...,15. Hence its parity-change count is at most 11. The endpoint convention ensures 0 and 15 remain selected.

## 3. An explicit polynomial with thirteen distinct real roots

Set D=10^7 and define

\[
 P_D(x)=(38x^2-89x+83)\prod_{j=1}^{13}\left(x+1+\frac jD\right).
\]

Its linear roots are -(1+j/D), for j=1,...,13. They are distinct, negative, and separated by 1/D. The quadratic is unchanged and has no real roots. Therefore P_D has exactly 13 distinct real roots, all simple. It remains to establish coefficient positivity and the three exclusions rigorously.

Let b_k be the coefficient of x^k in the product of the linear factors, with b_k=0 outside 0<=k<=13. Each b_k is an elementary symmetric sum of order 13-k in the numbers 1+j/D. It has B_k terms, and every term lies between 1 and (1+13/D)^(13-k). Thus, putting

\[
 E=\left(1+\frac{13}{D}\right)^{13}-1,
\]

we have

\[
 0\le b_k-B_k\le E B_k
\]

for every integer k, including the zero-extended indices.

By the binomial theorem, binom(13,r)<=13^r and 169/D<1 give

\[
 E\le\sum_{r=1}^{13}\left(\frac{169}{D}\right)^r
 \le\sum_{r=1}^{\infty}\left(\frac{169}{D}\right)^r
 =\frac{169}{D-169}<\frac1{50000}.
\]

The strict final inequality is the exact integer comparison

\[
169\cdot50000=8450000<9999831=D-169.
\]

Write a'_k for the coefficient of x^k in P_D. The quadratic convolution and triangle inequality imply

\[
 |a'_k-a_k|\le E s_k,
 \qquad s_k=83B_k+89B_{k-1}+38B_{k-2}.
\]

A second binomial calculation gives, for 0<=k<=15,

\[
 \frac{s_k}{\binom{15}{k}}=
 \frac{32k^2-1110k+17430}{210}\le83,
\]

because k(32k-1110)<=0 on that interval. Since a_k/binom(15,k)=(k-9)^2+2>=2,

\[
 \frac{|a'_k-a_k|}{a_k}\le\frac{83}{2}E
 <\frac{83}{100000}<\frac1{1000}.
\]

In particular,

\[
 \frac{999}{1000}a_k<a'_k<\frac{1001}{1000}a_k
\]

for every k. Every perturbed coefficient is strictly positive.

For k=8,9,10 these same estimates give

\[
 q'_k=\frac{(a'_k)^2}{a'_{k-1}a'_{k+1}}
 <q_k\left(\frac{1001}{999}\right)^2
 \le\frac{99}{100}\left(\frac{1001}{999}\right)^2<1.
\]

The largest of the three seed ratios is 99/100. The strict final inequality is certified by

\[
99\cdot1001^2=99198099<99800100=100\cdot999^2.
\]

Consequently the three perturbed differences at 8,9,10 remain strictly negative. The deletion lemma gives v(P_D)<=11, whereas P_D has 13 distinct real roots. This disproves the distinct-root formulation as well, without relying on any interpretation of repeated roots, floating-point computations, or coefficient tables.

If integer coefficients are desired, replace each linear factor by Dx+D+j. The resulting integer polynomial is D^13 P_D; the multiplier is positive, so the argument is unchanged.

## Sources and verification limits

The inspected mathematical sources are Shapiro's [version 1, p. 4](https://arxiv.org/pdf/1503.05295v1) and KSV's [version 1, Section 5, p. 20](https://arxiv.org/pdf/2403.12200v1). Local copies were hashed and the specified pages freshly rendered and visually checked. KSV's journal publication metadata was checked on [Shapiro's publication list](https://staff.math.su.se/shapiro/Articles/) on 11 October 2026; that list records volume 538, issue 1, 1 October 2024, article 128349. Institutional search metadata also records the same article and DOI as published/refereed. The publisher endpoint returned HTTP 403 in this audit, so no inspection of the journal-version PDF is claimed.

The accompanying independently authored standard-library checker corroborates the exact arithmetic for the seed, D=10^7, and the separate frozen screen's D=10^6 integer witness. The proof above does not depend on running that checker. No source-author program or pre-existing input checker was executed. KSV's higher-degree primitive construction and the separate weighted conjecture are outside this certificate's scope.

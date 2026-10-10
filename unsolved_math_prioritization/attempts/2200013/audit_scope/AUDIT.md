# Independent scope and mathematical audit: binomial tropical-corner counterexample

## Verdict and scope

**PASS.** No fatal flaw or required mathematical correction was found. The specified polynomial is a valid counterexample to the literal binomial-multiplication, distinct-corner statement of Shapiro's 2015 Conjecture 8.

This report preserves an independent audit completed on 2026-10-08. The complete supplied proof was read, its inequalities were independently rederived, and the three cited primary papers were checked. The packet's tests were not run, and the author files were not modified. This is a mathematical review, not a formal proof-assistant certificate or a high-degree root computation.

The report contains authored analysis and public citations, not copies or extracts of source documents. It makes no novelty, priority, minimal-degree, exact-root-count, or comprehensive-literature-search claim.

## Witness under review

Let

- v = 10^(-6);
- Q(x) = (1+x^5)(1+x^15)(1+x^25)(1+x^55) + v^2(x+1)^3 + v^6(x+1)^2 + v^12(x+1);
- K = 10^20, an even integer;
- N = 2K+100;
- lambda_i = binom(N,i);
- delta = 2^(-N^2);
- F(x) = x^K Q(x) + delta sum(x^i/lambda_i, 0<=i<=N, i not in {K,K+100}).

Write Q(x) = sum(q_j x^j, j=0,...,100) and C = q_0.

The audited claim is that every coefficient of F is strictly positive, its actual degree is N, it has at least four distinct negative real roots, and max_i(log(lambda_i a_i)+it), where a_i is its coefficient of x^i, has exactly three distinct corners.

## 1. Exact target and counting conventions

Shapiro's Section VII, Conjecture 8, uses max_i(log(a_i) + it + log binom(n,i)). Thus the weighting is multiplication. Its proposed bound counts points of the tropical variety, explicitly identified with corners. There is no slope-jump weighting or additional coefficient restriction beyond positivity. The supplied construction meets that statement with n equal to its actual degree N. See [Shapiro, Conjecture 8](https://arxiv.org/pdf/1503.05295).

Four distinct negative roots suffice under either distinct-root or algebraic-multiplicity counting. There is no ambiguity here that rescues the conjecture.

## 2. Seed coefficients

The subset sums of {5,15,25,55} are exactly

0, 5, 15, 20, 25, 30, 40, 45, 55, 60, 70, 75, 80, 85, 95, 100.

They are distinct, so the product has coefficients zero or one. The added terms affect only indices 0,1,2,3:

- q_0 = C = 1+v^2+v^6+v^12;
- q_1 = 3v^2+2v^6+v^12;
- q_2 = 3v^2+v^6;
- q_3 = v^2.

Consequently q_100=1, 1<C<2, and 0<=q_j<=1 for all 1<=j<=99. No hidden coefficient collision occurs.

## 3. Five sign samples

Define H(x) as the product of (1+x^e)/(1+x) over e in {5,15,25,55}, with each quotient interpreted as a polynomial at x=-1.

For x=-r, with r in [1-v,1+v], oddness of each exponent gives

(1+x^e)/(1+x) = 1+r+...+r^(e-1),

including its polynomial continuation at r=1. Hence

1 <= H(x) <= 103125(1+v)^96 <= 103125/(1-96v) < 200000.

The geometric-series bound is valid because 96v<1.

Writing y=x+1, the factorization is exactly

Q(x)=y B(y), where B(y)=H(x)y^3+v^2y^2+v^6y+v^12.

Independent substitutions give:

- B(-v) <= -v^3+v^4+v^12 < 0.
- B(-v^3) = v^8[1-(H+1)v+v^4] > 0, since (H+1)v<0.200001.
- B(-v^5) = v^11[-1+2v-Hv^4] < 0.
- B(-v^7) = v^12[1-v+v^4-Hv^9] > 0. Indeed, v+200000v^9<1.
- B(v^7)>0 term by term.

Multiplication by y yields the Q-sign sequence +,-,+,-,+ at

-1-v, -1-v^3, -1-v^5, -1-v^7, -1+v^7.

All five sample points are negative and strictly increasing.

## 4. Rational lower bound and perturbation

Every coefficient of Q has denominator dividing 10^72. Every sample t has denominator dividing 10^42. Since deg Q=100, 10^4272 Q(t) is an integer.

The proved nonvanishing therefore gives |Q(t)|>=10^(-4272). Also |t|>1/2, so

|t^K Q(t)| >= 2^(-K) 10^(-4272) > 2^(-K-17088),

using 10<16.

For the filler E=F-x^KQ, binom(N,i)>=1 and |t|<2 give

|E(t)| <= 2^(-N^2)(N+1)2^N <= 2^(-N^2+2N).

The omitted indices only reduce this estimate. The inequality N+1<=2^N holds for N>=1.

The required exponent comparison holds with an enormous strict margin. Since N=2K+100,

N^2 > 4K^2 > 5K+17288 = 2N+K+17088

for the stated K. Thus the perturbation cannot change any sample sign.

K is even, so t^K is positive. The intermediate value theorem supplies four roots in four disjoint negative intervals. This proves at least four distinct negative roots; it neither needs nor claims an exact root count or simplicity.

## 5. Strict positivity, degree, and zero roots

At indices K and K+100 the retained coefficients are C and 1. At every other index the filler contributes delta/binom(N,i)>0, possibly in addition to a nonnegative seed coefficient.

In particular a_0=a_N=delta>0. Therefore:

- every coefficient is strictly positive;
- deg F=N, exactly;
- zero is not a root;
- no positive real number is a root.

The K-fold zero of the intermediate x^KQ plays no role in the final real-root count.

## 6. Weighted central block

Let B=binom(N,K). Symmetry gives binom(N,K+100)=B, precisely because N=2K+100.

For 1<=j<=99,

binom(N,K+j)/B = product over r=1,...,j of (K+101-r)/(K+r).

Every factor is at most 1+100/K. Therefore

binom(N,K+j)/B <= (1+100/K)^100 <= 1/(1-10000/K) <= 1+20000/K.

Both geometric estimates have positive denominators, and the last inequality follows from 10000/K<=1/2.

After multiplying the coefficients of F by their binomial weights, the filler becomes exactly delta. Thus

b_(K+j)/B <= 1+20000/K+delta/B.

The numerical margin is valid:

- 20000/K = 2 times 10^(-16);
- v^2/1000 = 10^(-15);
- v^2/200 = 5 times 10^(-15).

Since delta<2^(-50)<10^(-15) and B>=1,

b_(K+j)/B < 1+1.2 times 10^(-15) < 1+5 times 10^(-15) = L.

Finally,

L^100 <= 1/(1-v^2/2) <= 1+v^2 < C.

The second inequality follows by multiplying through and using 0<v^2<1. Therefore L<C^(1/100), and, because C>1,

b_(K+j)/B < C^((100-j)/100).

This is exactly the strict weighted-chord inequality. It covers every interior index, including all nonzero seed coefficients and all newly filled zero coefficients.

## 7. Four hull vertices and exactly three corners

The four candidate vertices are

(0,log delta), (K,log(CB)), (K+100,log B), (N,log delta).

Their consecutive slopes are

- m_1 = (log(CB)-log delta)/K > 0;
- m_2 = -log C/100 < 0;
- m_3 = (log delta-log B)/K.

Since B>=1 and C<2,

m_3 <= -N^2 log 2/K < -log 2/100 < m_2.

The middle strict inequality uses 100N^2>K. Thus the three hull-edge slopes are strictly decreasing.

Every nonvertex outside the central block has height log delta and lies strictly below its outer segment. Every central nonvertex lies strictly below its central segment by the preceding inequality. Hence the upper hull has exactly the four asserted vertices.

Equivalently, the corner locations are exactly

- (log delta-log(CB))/K;
- log C/100;
- (log B-log delta)/K.

Their strict ordering is established by the slope comparisons. At each corner exactly two coefficient lines maximize; no hidden collinear or triple-maximizer term exists.

The ordinary corner count is therefore three. Maximizing-term multiplicities are each one. Standard slope-jump multiplicities are K,100,K and sum to N; that different count is not the target.

## 8. FNS implication and literature limits

FNS Theorem 11 expressly supplies three tropical roots versus four negative roots under sufficiently small log-weight curvature. This is stronger than merely asserting failure of essential-root preservation. Equation (4) uses multiplication weights. Its proof starts with a nonnegative seed; the explicit filler here independently resolves strict positivity. See [FNS, Theorem 11 and its proof](https://arxiv.org/pdf/1510.03257).

For binomial weights, direct cancellation gives

log(lambda_j^2/(lambda_(j-1)lambda_(j+1))) = log((1+1/j)(1+1/(N-j))).

On j=K,...,K+100 this is at most 2 log(1+1/K)<2/K. Thus the theorem applies for sufficiently large K. Its unspecified constant alone does not certify K=10^20; the explicit proof above does.

An [author-hosted version](https://www.wisdom.weizmann.ac.il/~dnovikov/Papers/RealTropicalExample.pdf) retains Theorem 11 and calls maximizing-term multiplicity Descartes' multiplicity.

The 2024 paper repeats the exact target as Conjecture 1, then explicitly presents counterexamples to Conjectures 2 and 3. It does not claim to disprove Conjecture 1. See [Katkova-Shapiro-Vishnyakova, Section 5](https://arxiv.org/pdf/2403.12200).

## 9. Recommended conclusion

Accept the displayed witness as a rigorous negative resolution of the literal target, with the classification **literature-derived obstruction with an explicit reconstructed witness**.

Retain the limitations: no minimal-degree claim, no exact total root count, no novelty or priority claim, and no assertion that the 2024 authors announced this disproof. The unexplained later repetition is a bibliographic-status discrepancy, not a mathematical gap in this witness.

## Public references

1. B. Shapiro, *Problems Around Polynomials: The Good, The Bad and The Ugly*, arXiv:1503.05295, Section VII, Conjecture 8. https://arxiv.org/abs/1503.05295
2. J. Forsgard, D. Novikov, B. Shapiro, *A tropical analog of Descartes' rule of signs*, arXiv:1510.03257v1, equation (4), Theorem 11, Lemma 27 and the proof of Theorem 11. https://arxiv.org/abs/1510.03257
3. The same FNS paper, author-hosted version, Theorem 11; its auxiliary seed statement is numbered Lemma 28. https://www.wisdom.weizmann.ac.il/~dnovikov/Papers/RealTropicalExample.pdf
4. O. Katkova, B. Shapiro, A. Vishnyakova, *In search of Newton-type inequalities*, arXiv:2403.12200v1, Section 5. https://arxiv.org/abs/2403.12200

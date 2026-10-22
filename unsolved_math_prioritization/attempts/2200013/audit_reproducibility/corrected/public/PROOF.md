# A strict-positive counterexample to the binomial tropical-corner bound

## Result and scope

For the binomial-multiplication convention in Shapiro's 2015 Conjecture 8, the proposed universal upper bound is false. The construction below has at least four **distinct negative** roots and exactly three **distinct tropical corners**. Every coefficient, including the constant and leading coefficients, is strictly positive. The degree is very large; no minimal-degree assertion is made.

This is a literature-derived negative resolution, with an explicit independently checkable reconstruction. The small-curvature obstruction is already present in Forsgård–Novikov–Shapiro (FNS), Theorem 11. No novelty claim is made. The 2024 paper by Katkova–Shapiro–Vishnyakova repeats the target as its Conjecture 1, but the counterexamples it labels in Section 5 concern its Conjectures 2 and 3. That later status wording does not change the calculation below.

## 1. The finite seed

Put v = 10^(-6), and define

Q(x) = (1+x^5)(1+x^15)(1+x^25)(1+x^55)
       + v^2(x+1)^3 + v^6(x+1)^2 + v^12(x+1).

Write Q(x) = sum(q_j x^j, j=0,...,100), and put C = q_0 = 1+v^2+v^6+v^12.
Then q_100=1, 1<C<2, and 0<=q_j<=1 for 1<=j<=99.
Indeed, the sixteen subset sums of 5,15,25,55 are distinct. The product therefore has only zero-one coefficients; its nonconstant terms have degree at least 5. The only other coefficients are

- q_1 = 3v^2+2v^6+v^12;
- q_2 = 3v^2+v^6;
- q_3 = v^2.

Each is less than 1.

There are alternating signs at the following five increasing, negative rational numbers:

| point | sign of Q |
|---|---|
| -1-v | + |
| -1-v^3 | - |
| -1-v^5 | + |
| -1-v^7 | - |
| -1+v^7 | + |

Here is a direct proof of these signs. Set y=x+1 and

H(x) = product((1+x^e)/(1+x), e in {5,15,25,55}),

interpreting each quotient as its polynomial continuation at -1. Then

Q(x) = y [ H(x)y^3 + v^2 y^2 + v^6 y + v^12 ].

For x=-r and 1-v<=r<=1+v, each quotient is 1+r+...+r^(e-1). Consequently

1 <= H(x) <= 103125(1+v)^96 <= 103125/(1-96v) < 200000.

The middle inequality follows by bounding the binomial coefficients by 96^j in the binomial expansion. Denote the expression in square brackets by B(y). At y=-v it is negative because

B(-v) <= -v^3+v^4+v^12 < 0.

At y=-v^3 it equals v^8[1-(H+1)v+v^4]>0. At y=-v^5 it equals v^11[-1+2v-Hv^4]<0. At y=-v^7 it equals v^12[1-v+v^4-Hv^9]>0. At y=v^7 all its terms are positive. These signs and the sign of y give the table. All numerical inequalities here are strict rational inequalities.

## 2. A compactly specified positive polynomial

Fix the even integer K=10^20, let N=2K+100, and set

lambda_i = binom(N,i),     delta = 2^(-N^2).

Define a polynomial by the finite formula

F(x) = x^K Q(x)
       + delta sum(x^i/lambda_i, 0<=i<=N, i not in {K,K+100}).

This is a completely specified rational polynomial, not a limit or a floating-point approximation. Its coefficients need not be expanded to define it. It has degree exactly N, constant coefficient delta, and every coefficient is strictly positive. The two omitted terms retain coefficients C and 1 at indices K and K+100. In particular F(0) is nonzero and F is positive on the positive real axis.

The large degree and the tiny rational delta are used only through the displayed inequalities. The verifier does not enumerate N+1 coefficients, form binom(N,K), or materialize delta.

## 3. At least four distinct real roots

At each sample point t in the table, 1/2<|t|<2. Each coefficient of Q has denominator dividing 10^72; each t has denominator dividing 10^42. Thus Q(t) has denominator dividing 10^4272. The sign proof gives Q(t)!=0, so

|t^K Q(t)| >= 2^(-K)10^(-4272) > 2^(-K-17088).

Because lambda_i>=1, the absolute value of the added term is at most

delta (N+1)2^N <= 2^(-N^2+2N).

We used N+1<=2^N, valid for every integer N>=1. Our parameters satisfy

N^2 > 2N+K+17088.

The perturbation is therefore strictly smaller than the absolute value of the original term at all five points. Since K is even, F has the same alternating signs as Q there. The intermediate value theorem gives a root in each of the four disjoint open intervals between adjacent sample points. All are negative and distinct. Counting algebraic multiplicities can only increase their number.

## 4. Exactly three distinct corners

For the tropical calculation multiply coefficient a_i of F by lambda_i; set b_i=lambda_i a_i. Let B=binom(N,K). Symmetry gives binom(N,K+100)=B. The two distinguished weighted coefficients are

b_K=CB,     b_(K+100)=B.

Every coefficient outside that block has weighted value delta. For 1<=j<=99,

b_(K+j)/B = q_j binom(N,K+j)/B + delta/B.

The binomial ratio is a product of j factors (K+101-r)/(K+r), for r=1,...,j. Each is at most 1+100/K. Bounding the binomial expansion by a geometric series yields

binom(N,K+j)/B <= (1+100/K)^100
                 <= 1/(1-10000/K) <= 1+20000/K.

The last inequality uses 10000/K<=1/2. Put L=1+v^2/200. The same elementary estimate gives

L^100 <= 1/(1-v^2/2) <= 1+v^2 < C.

Also delta<2^(-50)<v^2/1000, and

20000/K + v^2/1000 < v^2/200.

Since q_j<=1 and B>=1, we obtain the strict chord inequality

b_(K+j)/B < L < C^(1/100) <= C^((100-j)/100).

Hence every interior point (K+j, log b_(K+j)) lies strictly below the segment joining (K,log(CB)) and (K+100,log B).

The upper hull of all points (i,log b_i) has exactly the four vertices

(0,log delta), (K,log(CB)), (K+100,log B), (N,log delta).

To check this last assertion, the first segment has positive slope and the middle segment has slope -log(C)/100. The last segment has slope (log delta-log B)/K. Its slope is strictly less than the middle slope: use C<2, B>=1, delta=2^(-N^2), and 100N^2>K. Outside the block all other points have height log delta and lie strictly below the corresponding outer segment. Inside the block the strict chord inequality applies.

The maximum of the lines log(b_i)+i t therefore has exactly three corners, one for each upper-hull edge. At each corner precisely two terms attain the maximum. Their slope jumps are K,100,K.

Thus F has at least four distinct real roots but only three distinct binomial-weighted tropical corners. This disproves the proposed bound.

## 5. Conventions and limitations

- The weighting is multiplication by binom(N,i), not division. The divisions in the small filler are deliberately canceled when computing weighted coefficients.
- N is the actual degree. We do not keep an old degree parameter after multiplying by x^K.
- No zero coefficient, zero constant term, or zero root is used in F. Zero coefficients occur only in the intermediate seed.
- The three corners are geometric points. FNS's alternative multiplicity (number of maximizing terms minus one) is also one at each of these corners. The usual tropical slope-jump multiplicities sum to N and would give a different, trivial bound.
- We do not infer an ordinary-corner bound from a bound involving only essential tropical roots. The four-vertex computation establishes ordinary corners directly.
- Replacing natural logarithms with a consistent logarithm of base greater than one rescales the horizontal corner locations and leaves their number unchanged. Multiplying F by a positive constant or replacing x by a positive multiple of x likewise preserves the comparison.
- The finite verifier checks the rational inequalities supporting this proof. It is not a generic high-degree root solver and does not certify the exact total number of real roots. Neither is needed here.
- There is no remaining mathematical gap in the displayed counterexample, subject to independent audit. The history of why the target was still printed in 2024 remains unexplained. This report makes no claim that its explicit degree is optimal or previously unpublished.

## References and literature reconciliation

1. B. Shapiro, *Problems Around Polynomials: The Good, The Bad and The Ugly*, Arnold Mathematical Journal 1 (2015), 91–104, Section 7, Conjecture 8. https://arxiv.org/abs/1503.05295 ; https://doi.org/10.1007/s40598-015-0008-4
2. J. Forsgård, D. Novikov, B. Shapiro, *A tropical analog of Descartes' rule of signs*, arXiv:1510.03257v1 (2015), Theorem 11, equation (4), and Lemma 27/proof of Theorem 11; published in IMRN 2017(12), 3726–3750. https://arxiv.org/abs/1510.03257
3. O. Katkova, B. Shapiro, A. Vishnyakova, *In search of Newton-type inequalities*, arXiv:2403.12200v1 (2024), Section 5; JMAA 538(1), 128349. https://arxiv.org/abs/2403.12200 ; https://doi.org/10.1016/j.jmaa.2024.128349

FNS's obstruction has an absolute c>0 and applies if 101 consecutive log-weight curvatures are below 2c. For binomial weights that curvature is log((1+1/j)(1+1/(N-j))), tending uniformly to zero on a fixed-length central block. This already implies the negative result. Its written construction first has nonnegative coefficients; the explicit filler above supplies strict positivity while preserving strict hull and root-sign margins. The independent construction also removes reliance on an unspecified constant c.

The later paper restates the target, and does not assert its disproof. Accordingly the classification here is “disproved by an existing obstruction, with an explicit reconstructed witness,” not “the 2024 paper solved Conjecture 8.”

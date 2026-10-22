# A degree 24 reconstruction of the weighted parity counterexample

The weighted parity conjecture of Forsgård and Shapiro, recorded as [Conjecture 9 in Shapiro's problem list](https://arxiv.org/pdf/1503.05295v1#page=4), is false. The disproof and primitive family are due to [Katkova, Shapiro and Vishnyakova, *In search of Newton-type inequalities* (2024), Section 5](https://arxiv.org/pdf/2403.12200v1#page=20). This note reconstructs a finite example and gives an explicit simple-root perturbation. It makes no novelty or minimum-degree claim.

This is an AI-assisted mathematical proof with a separate AI-assisted audit. Acceptance here does not mean external human peer review, journal acceptance of this reconstruction, or formal proof-assistant certification. The proof below is self-contained; the omitted raw finite certificates are supplemental.

## The proposed bound

For a real polynomial \(f(x)=\sum_{k=0}^{n}a_kx^k\) with every \(a_k>0\), extend by \(a_{-1}=a_{n+1}=0\), and put

\[
c_k(f)=(k+1)a_k^2-ka_{k-1}a_{k+1}.
\]

Select the indices \(k\) for which \(c_k(f)>0\), in increasing order. Let \(v(f)\) count changes between consecutive parities of these indices. The proposed upper bound on real zeros is \(v(f)\). Endpoints are selected because \(c_0=a_0^2>0\) and \(c_n=(n+1)a_n^2>0\). The source's parity-sequence subscript starts at an undefined \(k_0\); here the sequence is the expressly defined \(k_1,\ldots,k_m\).

We will exhibit a degree-24 polynomial with 22 distinct simple negative roots and \(v\leq20\), settling either interpretation of root multiplicity.

## The repeated-root polynomial

Write \(Q(x)=38x^2-188x+326\) and

\[
P(x)=(x+1)^{22}Q(x)=\sum_{k=0}^{24}a_kx^k.
\]

Binomial expansion gives the particularly simple formula

\[
a_k=\binom{24}{k}\bigl((k-18)^2+2\bigr)>0.
\]

For example, this follows by expressing
\(326\binom{22}{k}-188\binom{22}{k-1}+38\binom{22}{k-2}\)
as a multiple of \(\binom{24}{k}\). Define \(q_k=a_k^2/(a_{k-1}a_{k+1})\). Direct substitution gives

\[
q_{17}=\frac{108}{119}<\frac{17}{18},\qquad
q_{18}=\frac{133}{243}<\frac{18}{19},\qquad
q_{19}=\frac{18}{19}<\frac{19}{20}.
\]

Thus \(c_{17},c_{18},c_{19}<0\). The increasing list
\(0,1,\ldots,16,20,21,22,23,24\)
has 20 parity changes. The selected index sequence is a subsequence of that list. Removing entries from a binary sequence cannot increase its number of changes: for binary \(u,v,w\), the indicator of \(u\ne w\) is at most the sum of the indicators of \(u\ne v\) and \(v\ne w\). Hence \(v(P)\leq20\); no signs at other indices are needed for this argument.

The discriminant of \(Q\) is \(-14208<0\). Therefore \(P\) has exactly 22 real roots with multiplicity, at −1. This already disproves the multiplicity interpretation.

## An explicit simple-root perturbation

Set \(D=10^6\), \(\delta_j=j/D\) for \(1\leq j\leq22\), and

\[
F(x)=Q(x)\prod_{j=1}^{22}(x+1+\delta_j),\qquad R(x)=D^{22}F(x).
\]

Thus \(R(x)=Q(x)\prod_{j=1}^{22}(Dx+D+j)\) has integer coefficients. We prove its coefficients stay positive and its weighted differences at 17, 18 and 19 stay negative, using explicit rational bounds.

Let \(r_k\) be the coefficient of \(x^k\) in \(F\), and put

\[
S=\sum_{j=1}^{22}\delta_j=\frac{253}{10^6}.
\]

First consider \(H(x)=Q(x)(x+1)^{21}\). For \(0\leq k\leq23\), its coefficient is

\[
h_k=\frac{\binom{23}{k}}{506}
       (552k^2-19032k+164956)>0.
\]

The quadratic in \(k\) has positive leading coefficient and discriminant \(-2005824<0\), which proves the stated positivity. Extend \(h_{-1}=h_{24}=0\). Since \(P=(x+1)H\), we have \(a_k=h_k+h_{k-1}\), so \(0\leq h_k\leq a_k\).

Let \(e_s\) be the elementary symmetric function of degree \(s\) in the positive numbers \(\delta_1,\ldots,\delta_{22}\). Expanding around \(x+1\) yields

\[
F(x)=\sum_{s=0}^{22}e_s Q(x)(x+1)^{22-s}.
\]

Here \(e_0=1\), \(e_1=S\), and \(e_s\leq S^s/s!\). For every \(s\) and \(k\), the absolute value of the coefficient of \(x^k\) in \(Q(x)(x+1)^{22-s}\) is at most

\[
T_k=326\binom{22}{k}+188\binom{22}{k-1}+38\binom{22}{k-2},
\]

using zero for out-of-range binomial coefficients. Indeed, each smaller-top binomial coefficient is at most the corresponding one with top 22. Moreover,

\[
\frac{T_k}{a_k}
 =1+\frac{376k(24-k)}{552((k-18)^2+2)}
 \leq1+\frac{376\cdot144}{552\cdot2}<51.
\]

Since \(S<1\),

\[
\sum_{s=2}^{22}e_s
 \leq\sum_{s=2}^{\infty}\frac{S^s}{s!}
 \leq\frac{S^2}{2(1-S)}.
\]

Combining these bounds gives, at every index,

\[
\frac{|r_k-a_k|}{a_k}
 \leq S+\frac{51S^2}{2(1-S)}
 =\frac{169712147}{666498000000}
 <\frac1{2000}.
\]

In particular, all \(r_k\) are strictly positive. Their ratios satisfy

\[
\frac{r_k^2}{r_{k-1}r_{k+1}}
 <\left(\frac{2001}{1999}\right)^2q_k.
\]

The three exact rational comparisons

\[
\left(\frac{2001}{1999}\right)^2\frac{108}{119}<\frac{17}{18},\qquad
\left(\frac{2001}{1999}\right)^2\frac{133}{243}<\frac{18}{19},\qquad
\left(\frac{2001}{1999}\right)^2\frac{18}{19}<\frac{19}{20}
\]

show \(c_{17}(F),c_{18}(F),c_{19}(F)<0\). Thus the same subsequence argument proves \(v(F)\leq20\). Positive scaling gives \(v(R)=v(F)\) and preserves coefficient positivity.

The real roots of \(R\) are exactly

\[
-1-\frac{j}{10^6},\qquad 1\leq j\leq22.
\]

They are pairwise distinct, simple and negative. The quadratic contributes two distinct nonreal roots because its discriminant is negative. The actual degree is 24. Therefore \(R\) has 22 distinct real roots, also 22 with multiplicity, and

\[
22>20\geq v(R).
\]

This explicitly disproves the conjecture under either real-root convention.

## Relation to the credited construction

KSV starts with

\[
Q_{15}(x)=\frac{(x+1)^{13}}{720720}(38x^2-89x+83)
\]

and takes repeated primitives based at −1. With \(t=x+1\), put

\[
P_n=t^{n-2}(38t^2-11nt+n(n-1)).
\]

Direct differentiation gives \(P_n'=nP_{n-1}\) and \(P_n(-1)=0\), while \(P_{15}=720720Q_{15}\). Consequently

\[
Q_n=\frac{15!}{720720\,n!}P_n,
\]

and the polynomial \(P\) above is \(P_{24}\). The normalization is positive.

For accurate finite-degree reconstruction, the primitive coefficient recurrence gives

\[
q_{n-5}=\frac9{10}\frac{n-4}{n-5},\quad
q_{n-6}=\frac{14}{27}\frac{n-5}{n-6},\quad
q_{n-7}=\frac67\frac{n-6}{n-7}.
\]

The finite product endpoints printed on pp. 20–21 of the inspected arXiv:2403.12200v1 are shifted; these corrected expressions follow by telescoping \(q_{k+1}(Q_{n+1})=q_k(Q_n)k(k+2)/(k+1)^2\). Their limits agree with KSV's argument. The explicit proof above uses direct coefficient formulas and rational bounds and therefore does not rely on those misindexed finite products.

This finite-product correction applies only to the inspected arXiv version. The publisher PDF was not inspected, and no claim is made about whether its displayed endpoints were corrected.

# Partial bounds for Rippon's iterated-exponential coefficient problem

## Status and scope

**The universal problem is unresolved in this work.** No counterexample and no universal coefficient estimate are claimed. No novelty or priority claim is made for the partial observations.

Put
\[
 F_0(t)=-1,\qquad F_{n+1}(t)=\exp(tF_n(t))-1,\qquad
 a_{n,k}=[t^k]F_n(t).
\]
Rippon's question, recorded as Problem 7.54 in Hayman–Lingham, asks whether
\[
 |a_{n,k}|\leq1\quad(n\geq1,\ k\geq0).
\]
Every fixed iterate is entire. All series manipulations below are also valid in \(\mathbb Q[[t]]\).

The accompanying exact certificate proves the following partial statement.

**Theorem (limited coefficient ranges).** The proposed bound holds whenever at least one of these conditions holds:

1. \(0\leq k\leq200\), with arbitrary \(n\geq1\);
2. \(0\leq k-n\leq100\), with arbitrary \(n\geq1\);
3. \(1\leq n\leq4\), with arbitrary \(k\geq0\).

Coefficients with \(k<n\) vanish. Thus the region not covered here is precisely
\[
 n\geq5,\qquad k\geq201,\qquad k-n\geq101.
\]
This describes the gap in this certificate, rather than claiming that every coefficient in that region is unknown in the literature.

## 1. An exact integer recurrence

Define \(A_{n,k}=k!a_{n,k}\), with \(A_{0,0}=-1\) and \(A_{0,k}=0\) for \(k>0\). For one iteration set
\[
 E(t)=\exp(tF_n(t))=\sum_{k\geq0}B_k\frac{t^k}{k!}.
\]
Then \(B_0=1\). Since \(E'=(tF_n)'E\), multiplication of exponential generating series gives, for \(k\geq1\),
\[
 B_k=\sum_{j=1}^{k}\binom{k-1}{j-1}
       j A_{n,j-1}B_{k-j}.                    \tag{1}
\]
Set \(A_{n+1,0}=0\) and \(A_{n+1,k}=B_k\) for \(k\geq1\). In particular all \(A_{n,k}\) are integers. Formula (1) is triangular in \(k\), so truncation at degree \(D\) computes all coefficients through \(D\) exactly, independently of higher coefficients.

Induction on \(n\) gives
\[
 F_n(t)=-t^n+O(t^{n+1}).                     \tag{2}
\]
Indeed the linear term in \(\exp(tF_n)-1\) is \(tF_n\), while all other terms have strictly higher order. Consequently the zero terms omitted by the implementation of (1) really vanish.

The verifier evaluates (1) for \(1\leq n\leq200\), \(0\leq k\leq200\), and checks the integer inequalities
\[
 |A_{n,k}|\leq k!.
\]
There are 40,200 such pairs. An independent implementation computes the powers in the truncated ordinary series \(\sum_{m\geq1}(tF_n)^m/m!\), using rational arithmetic, and cross-checks every pair \(0\leq n,k\leq24\).

For \(n>200\), all coefficients of degree at most 200 vanish by (2). This proves item 1. Within the computed rectangle the largest modulus off the leading diagonal is \(2663/4480\), attained at \((n,k)=(6,13)\), where the coefficient is negative. This maximum is only a finite-rectangle statement.

## 2. Stabilization of diagonal coefficients

Define \(H_n=-F_n/t^n\), including \(H_0=1\). Equation (2) makes \(H_n\) a formal series with constant term 1. The recurrence becomes
\[
 H_{n+1}=H_n+\sum_{m\geq2}
 \frac{(-1)^{m+1}}{m!}t^{(m-1)(n+1)}H_n^m. \tag{3}
\]
Hence
\[
 H_{n+1}-H_n\in t^{n+1}\mathbb Q[[t]].      \tag{4}
\]
For each fixed \(j\geq0\), the coefficient \([t^j]H_n\) is therefore constant for \(n\geq j\).

For \(n\leq100\) and \(0\leq j\leq100\), the coefficient \(a_{n,n+j}\) was checked in Section 1 because \(n+j\leq200\). For \(n>100\), (4) gives
\[
 a_{n,n+j}=a_{100,100+j}\qquad(0\leq j\leq100).
\]
This proves item 2, including every iterate rather than merely a finite sample.

There is a coefficientwise formal limit \(H_\infty\), but (4) does not bound its coefficients at arbitrarily large offsets. Even a bound for that limit alone would leave the transient cases \(n<j\) untreated.

## 3. Cauchy estimates for all degrees of the first four iterates

For an entire \(F_n\), Cauchy's coefficient formula on a circle of radius \(R\) gives
\[
 |a_{n,k}|\leq M_n(R)R^{-k},\quad
 M_n(R)=\max_{|t|=R}|F_n(t)|.               \tag{5}
\]
The elementary inequality \(|e^z-1|\leq e^{|z|}-1\) supplies finite bounds on these maxima.

We use the strict rational bounds
\[
 e<\frac{87}{32}<\frac{11}{4}<3,
 \qquad e^x\leq\frac1{1-x}\quad(0\leq x<1). \tag{6}
\]
For the first inequality, the sum through \(1/3!\) is \(8/3\); the remaining terms are at most the geometric sum \((1/24)/(1-1/5)=5/96\). The inequality is strict because later successive ratios are less than \(1/5\). The second inequality follows termwise from \(1/m!\leq1\).

### Iterates 1, 2, and 3

Take \(r_0=11/10\). By (6),
\[
 e^{11/10}<\frac{11}{4}\frac{10}{9}<\frac{31}{10}.
\]
Thus \(M_1(r_0)<21/10\). Next,
\[
 M_2(r_0)<e^{231/100}-1<10,
\]
since
\[
 e^{231/100}=e^2e^{31/100}
 <\left(\frac{11}{4}\right)^2\frac{100}{69}<11.
\]
It follows that \(M_3(r_0)<e^{11}<3^{11}\). The same bound \(3^{11}\) also bounds the first two maxima. Exact integer arithmetic verifies
\[
 (11/10)^{128}>3^{11}.                    \tag{7}
\]
Equations (5) and (7) prove \(|a_{n,k}|<1\) for \(1\leq n\leq3\), \(k\geq128\). Section 1 covers the remaining degrees.

### Iterate 4

First bound the third iterate on the larger circle \(R=23/20\). We have
\[
 e^{23/20}=e e^{3/20}
 <\frac{87}{32}\frac{20}{17}<\frac{16}{5},
\]
so \(M_1(R)<11/5\). Further,
\[
 e^{253/100}=e^2 e^{1/2}e^{3/100}
 <\left(\frac{11}{4}\right)^2\frac53\frac{100}{97}<13.
\]
Here \(e^{1/2}<5/3\) follows from \(e<11/4<25/9\). Therefore
\[
 M_2(R)<12,\qquad
 M_3(R)<e^{69/5}<e^{14}< (11/4)^{14}.       \tag{8}
\]

Set \(r=21/20\), \(q=r/R=21/23\), and define the explicitly finite rational number
\[
 P=\sum_{k=0}^{200}\frac{|A_{3,k}|}{k!}r^k.
\]
By (5) and (8), the weighted absolute tail satisfies
\[
 \sum_{k=201}^{\infty}|a_{3,k}|r^k
 <\left(\frac{11}{4}\right)^{14}
   \frac{q^{201}}{1-q}.                    \tag{9}
\]
The verifier checks, by exact rational arithmetic,
\[
 \frac{4620}{1000}
 <P+\left(\frac{11}{4}\right)^{14}\frac{q^{201}}{1-q}
 <\frac{4621}{1000}<5.                    \tag{10}
\]
In particular \(M_3(r)<5\). Hence
\[
 M_4(r)< e^{21/4}<e^6<3^6.
\]
Exact arithmetic also verifies
\[
 (21/20)^{136}>3^6.                       \tag{11}
\]
Equations (5) and (11) prove \(|a_{4,k}|<1\) for \(k\geq136\). The finite calculation covers all smaller degrees. This proves item 3.

## 4. Two obstructions to simple induction

Replacing every sign by a positive sign produces the coefficientwise majorant
\[
 G_0=1,\qquad G_{n+1}=e^{tG_n}-1.
\]
It does dominate \(|a_{n,k}|\) coefficientwise, but already
\[
 [t^6]G_3=25/24>1,
\]
whereas \([t^6]F_3=1/24\). Thus this majorant loses essential cancellation.

A more explicit expression is available. Let \(S(u,v)\) denote a Stirling number of the second kind. Then
\[
 a_{n,k}=\sum_{\substack{1\leq l_1\leq\cdots\leq l_n\\
                         l_1+\cdots+l_n=k}}
 \frac{(-1)^{l_n}}{l_n!}
 \prod_{i=1}^{n-1} S(l_{i+1},l_i).         \tag{12}
\]
For justification, expansion of the exponential at each vertex describes rooted trees with all leaves at level \(n\), weight \((-1)^{\#\text{leaves}}\), a factor \(t\) for each edge, and the usual factorial divisor for unordered children. Fix level sizes \(l_0=1,l_1,\ldots,l_n\). Label vertices independently at each non-root level. The parent map from level \(i+1\) onto level \(i\) must be onto, since no earlier vertex may be a leaf; there are \(l_i!S(l_{i+1},l_i)\) choices. Dividing the product by \(\prod_{i=1}^n l_i!\) leaves exactly the weight in (12). Equivalently this is a coefficient extraction from the repeated exponential formula, so no convergence assertion is required.

The individual summands in (12) are not all at most 1: for \(n=4\) and level sizes \((3,6,9,12)\), the positive summand is
\[
 \frac{S(6,3)S(9,6)S(12,9)}{12!}
 =\frac{90\cdot2646\cdot22275}{12!}
 =\frac{2835}{256}>1.
\]
Consequently a universal argument using (12) must control cancellation between level profiles. No such uniform cancellation theorem is proved here.

## Reproduction and remaining question

Run `python3 verify.py` and compare its JSON output with `verification_output.json`. The program needs only Python's standard library and uses no floating-point arithmetic or external data. The infinite extensions depend on the proved valuation, stabilization, and Cauchy arguments above, not on extrapolating a finite computation.

The missing result is still a proof or counterexample to \(|a_{n,k}|\leq1\) in the stated remaining region. Neither the formal limit, the positive majorant, nor the signed-tree representation presently settles it.

## Reference

W. K. Hayman and E. F. Lingham, *Research Problems in Function Theory (New Edition)*, arXiv:1809.07200v2 (21 September 2018), Problem and Update 7.54, printed p.177: https://arxiv.org/abs/1809.07200v2 .

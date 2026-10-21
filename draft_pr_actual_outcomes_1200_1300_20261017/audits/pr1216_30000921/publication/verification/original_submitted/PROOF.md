# Polynomial multiplication need not preserve differentiation hypercyclicity

This is an AI-assisted, unrefereed mathematical review edition. Acceptance is an independent internal AI audit judgment, not external human peer review, journal acceptance, formal proof-assistant certification, or novelty clearance.

The full authored mathematical proof and independent audit are retained, including every written argument, formula, and counterexample. This is not a computational reproduction package: executable code, raw computational datasets, copied source PDFs/text/images, search responses, and private coordination material are not distributed. Historical finite checks support the written proof and cannot be reproduced from this edition alone.

Source retrieval, inspection, and mathematical executions described below are historical acts of the original investigation or audit. Publication preparation performed no new scholarly-source retrieval, source-body inspection, literature survey, or mathematical execution. The original proof and audit remain unchanged.

## Status and exact claim

This is a complete negative answer to OWR-1787-006 (numeric record
30000921), accepted by the independent internal AI audit reproduced in AUDIT.md.
No mathematical correction was required. No claim of novelty or historical
priority is made. The original question concerns pointwise
multiplication, not a polynomial in the differentiation operator.

Let H(C) be the space of entire functions with the topology of uniform
convergence on compact sets. Write Df=f' and

\[
HC(D)=\{f\in H(\mathbb C):\{D^n f:n\geq0\}\text{ is dense in }H(\mathbb C)\}.
\]

The question asks whether pf belongs to HC(D) for every f in HC(D) and
every nonconstant complex polynomial p. **The answer is negative, already
for p(z)=z.** In fact, each fixed nonconstant polynomial has a dense set of
counterexamples. Nonzero constant polynomials are the only polynomials
whose pointwise multiplication preserves every member of HC(D).

The principal counterexample is in Section 3. Sections 1 and 2 supply all
of its analytic existence and perturbation ingredients. Section 4 proves
the stronger fixed-polynomial statement. No computation is needed for the
infinite-dimensional conclusions.

## 1. Existence and density of hypercyclic entire functions

For R>0, put ||u||_R=max_{|z|<=R}|u(z)|. The space H(C), with these
seminorms, is a complete metrizable topological vector space and hence a
Baire space. Completeness follows from uniform convergence on every disk:
a Cauchy sequence has compatible locally uniform limits, and the
Weierstrass theorem makes their common limit entire. Polynomials with
coefficients in Q+iQ are dense, by Taylor approximation followed by
coefficient approximation. Differentiation is continuous by the Cauchy
estimates.

Let (P_j) enumerate these polynomials. For positive integers j,r,s, define

\[
U_{j,r,s}=\bigcup_{n\geq0}
 \{u\in H(\mathbb C):\|D^n u-P_j\|_r<1/s\}.
\]

Each U_{j,r,s} is open. It is dense as well. Given a nonempty open set V,
choose a polynomial Q in V. Write P_j(z)=sum_{k=0}^d b_k z^k and define

\[
I_nP_j(z)=\sum_{k=0}^d b_k\frac{k!}{(n+k)!}z^{n+k}.
\]

Then D^n(I_nP_j)=P_j. For every fixed R, each of the finitely many terms
has norm at most |b_k|k! R^{n+k}/(n+k)!, which tends to zero. Thus
I_nP_j tends to zero in H(C). If n>deg Q is large enough, Q+I_nP_j lies
in V and D^n(Q+I_nP_j)=P_j. Hence V meets U_{j,r,s}.

By Baire, the intersection of all U_{j,r,s} is dense and nonempty. Every
member has dense derivative orbit: approximate a desired entire function
on a desired disk first by some P_j and then use membership in
U_{j,r,s} for sufficiently large s. This proves the needed existence and
density of HC(D), without using any unproved assertion about a particular
explicit entire function. It is the standard Baire proof of MacLane's
phenomenon.

## 2. Tail density and perturbations with vanishing derivatives

### Lemma 2.1 (dense tails)

If f belongs to HC(D), then {D^n f:n>=N} is dense for every N>=0.

**Proof.** Let V be nonempty and open. A nonempty open subset of H(C)
cannot be finite: given u in it, sufficiently small constant perturbations
of u stay in it. The finite set F={D^n f:0<=n<N} is closed. Consequently
V minus F contains a nonempty open set. Density of the full orbit gives
an orbit point there, whose index is at least N. Thus every V meets the
tail. This also shows that, for every g in H(C), there are strictly
increasing indices n_j with D^{n_j}f tending to g: choose the j-th index
beyond the previous one and approximate g on the disk of radius j with
error less than 1/j. QED.

### Lemma 2.2 (null-orbit perturbation)

If f belongs to HC(D) and h is entire with D^n h tending to zero in H(C),
then f+h belongs to HC(D).

**Proof.** For any g in H(C), choose n_j increasing to infinity with
D^{n_j}f tending to g by Lemma 2.1. Then
D^{n_j}(f+h)=D^{n_j}f+D^{n_j}h tends to g. QED.

### Lemma 2.3 (coefficient estimate)

Let alpha be complex and suppose (c_k) is bounded and tends to zero. Then

\[
h(z)=\sum_{k=0}^{\infty}c_k\frac{(z-\alpha)^k}{k!}
\]

is entire, and its derivative orbit tends to zero. More precisely,

\[
\max_{|z-\alpha|\leq R}|h^{(n)}(z)|
\leq e^R\sup_{k\geq n}|c_k|.
\]

**Proof.** Boundedness by C gives normal convergence on every disk by
comparison with C exp(R), so the series is entire and can be
differentiated term by term. Its n-th derivative is
sum_{k>=0} c_{n+k}(z-alpha)^k/k!. Taking absolute values gives the
displayed estimate. The supremum of the tail of a null sequence tends to
zero. Disks about alpha exhaust C, so this is compact-open convergence.
QED.

## 3. A counterexample for multiplication by z

Take any f in HC(D), whose existence was proved in Section 1, and write

\[
f(z)=\sum_{k=0}^{\infty}a_k\frac{z^k}{k!},\qquad a_k=f^{(k)}(0).
\]

Define, for each k>=0,

\[
b_k=\begin{cases}
a_k,& |a_k|\geq 1/(k+1),\\
1/(k+1),& |a_k|<1/(k+1),
\end{cases}
\qquad c_k=b_k-a_k.
\]

This elementary replacement gives two simultaneous bounds:

\[
|b_k|\geq\frac1{k+1},\qquad |c_k|\leq\frac2{k+1}.
\]

Define h(z)=sum_{k>=0} c_k z^k/k! and F=f+h. Lemma 2.3 proves that h
is entire and, for every R>0,

\[
\|D^n h\|_R\leq \frac{2e^R}{n+1}\longrightarrow0.
\]

Lemma 2.2 therefore gives F in HC(D). Furthermore F^{(k)}(0)=b_k.
For n>=1 the product rule gives

\[
D^n(zF)(z)=zF^{(n)}(z)+nF^{(n-1)}(z),
\qquad
|(zF)^{(n)}(0)|=n|b_{n-1}|\geq1.
\]

For n=0, (zF)(0)=0. Thus the entire derivative orbit of zF misses the
nonempty open set

\[
\mathcal V=\{u\in H(\mathbb C):|u(0)-1/2|<1/4\}.
\]

Indeed its zeroth value at 0 is distance 1/2 from 1/2, while every later
value w satisfies |w-1/2|>=|w|-1/2>=1/2. Evaluation at 0 is continuous,
and the constant function 1/2 lies in V. Hence zF is not in HC(D).

This proves the required negative answer with the permitted nonconstant
polynomial p(z)=z. The proof does not infer hypercyclicity from finitely
many coefficient blocks or numerical experiments.

### Two immediate refinements

1. Replacing 1/(k+1) by eta/(k+1), for any eta>0, gives
   ||h||_R<=2 eta e^R. Consequently every neighborhood of every f in
   HC(D) contains an F in HC(D) for which zF is not hypercyclic. Together
   with Section 1, the counterexamples are dense in all of H(C).
2. The same F from the construction with eta=1 satisfies z^m F not in
   HC(D) for every integer m>=1. For n<m, (z^mF)^{(n)}(0)=0. For n>=m,
   its modulus at 0 is at least
   n! / ((n-m)! (n-m+1)), which is at least 1. The same open set V works.
   This claim concerns monomials, not every polynomial simultaneously.

## 4. Each fixed nonconstant polynomial has dense counterexamples

### Theorem 4.1

Fix a nonconstant p in C[z]. For every f in HC(D) and every neighborhood
W of f in H(C), there exists F in W intersect HC(D) such that pF is not
in HC(D).

**Proof.** By the fundamental theorem of algebra, p has a root alpha.
Let its multiplicity be m>=1 and write

\[
p(z)=\sum_{j=m}^{d}q_j(z-\alpha)^j,\qquad q_m\ne0.
\]

Put a_k=f^{(k)}(alpha). Fix a parameter eta>0, to be made small at the
end. We construct c_0,c_1,... recursively. Suppose c_0,...,c_{k-1} have
already been chosen, and put n=k+m and

\[
A_k=q_m\frac{(k+m)!}{k!},
\]

\[
S_k=A_ka_k+
\sum_{j=m+1}^{\min(d,k+m)}
 q_j\frac{(k+m)!}{(k+m-j)!}
 (a_{k+m-j}+c_{k+m-j}).
\]

An empty sum is zero. Each correction index in the sum is nonnegative
and strictly smaller than k, so S_k is determined by the previous steps.
Choose

\[
c_k=\begin{cases}
0,& |S_k|\geq\eta,\\
(\eta-S_k)/A_k,& |S_k|<\eta.
\end{cases}
\]

The complex number A_k is nonzero. In both cases

\[
|S_k+A_kc_k|\geq\eta,
\qquad
|c_k|\leq \frac{2\eta}{|A_k|}
=\frac{2\eta}{|q_m|(k+1)(k+2)\cdots(k+m)}.
\tag{4.1}
\]

In the second case the first expression equals the positive real number
eta, and the second inequality follows from |eta-S_k|<=eta+|S_k|.
Thus the sequence of corrections is bounded and tends to zero. The
function h(z)=sum_{k>=0}c_k(z-alpha)^k/k! is entire, with D^n h tending
to zero by Lemma 2.3. Hence F=f+h belongs to HC(D).

For every n>=m, multiplying the two convergent Taylor series at alpha
gives the exact finite coefficient formula

\[
(pF)^{(n)}(\alpha)=
 \sum_{j=m}^{\min(d,n)}q_j\frac{n!}{(n-j)!}
 (a_{n-j}+c_{n-j}).
\tag{4.2}
\]

Taking n=k+m makes (4.2) equal S_k+A_kc_k. Therefore its modulus is at
least eta for every n>=m. For 0<=n<m it is zero because pF has a zero
of order at least m at alpha. The orbit misses the nonempty open set

\[
\{u\in H(\mathbb C):|u(\alpha)-\eta/2|<\eta/4\}.
\]

Consequently pF is not hypercyclic. Finally (4.1) and Lemma 2.3 imply

\[
\max_{|z-\alpha|\leq R}|h(z)|
\leq\frac{2\eta e^R}{|q_m|m!}.
\]

As eta tends to zero these bounds tend to zero on every fixed disk,
regardless of the dependence of the chosen coefficients on eta. Given W,
choose eta small enough for F=f+h to lie in W. QED.

### Corollary 4.2 (universal polynomial multipliers)

For a polynomial p, the implication

\[
f\in HC(D)\ \Longrightarrow\ pf\in HC(D)
\quad\text{for every }f
\]

holds exactly when p is a nonzero constant. The nonconstant case is
Theorem 4.1; p=0 fails; for p=c!=0, multiplication by c is a
homeomorphism and sends the derivative orbit of f onto that of cf.

## 5. Quantifiers, relation to sources, and limits of the conclusion

Costakis's 2008 contribution, "Which maps preserve universal functions?",
poses the exact pointwise-product question as Question 5 on printed page
330 (PDF page 34). Theorem 6 on that same page states that a residual
subset G of H(C) consists of functions f for which pf belongs to HC(D)
for every nonzero polynomial p. Our dense counterexample sets do not
contradict that assertion: a dense set can be meagre and disjoint from a
residual set. We do not replace the universal question by the residual
statement. The 2008 result is not needed to prove the counterexample.

The later 2018 paper by Bernal-González, Conejero, Costakis, and
Seoane-Sepúlveda discusses polynomial composition P composed with f,
convolution operators Phi(D), selected multiplicative groups, and
composition-operator hypercyclicity. Those operations and existential
quantifiers do not imply the universal pointwise-product assertion.
Costakis's 2010 paper on common Cesàro hypercyclic vectors gives a
residual set for the sequences (n^b D^n), simultaneously over real b;
that is likewise a generic statement, not a claim about every
D-hypercyclic function.

Theorem 4.1 fixes p before constructing F. It does not assert one F fails
for all nonconstant polynomials simultaneously. The monomial assertion
in Section 3 is the explicitly proved simultaneous special case.

This manuscript establishes an analytic counterexample conditional only
on standard elementary complex analysis, Baire's theorem, and the
fundamental theorem of algebra (the latter used only in Section 4).
The independent internal AI audit accepted the complete negative answer with
no mathematical correction. Historical novelty remains unestablished. The
original bounded searches did not establish priority or prove that the question
was still open in 2026; their raw responses are not distributed here.

## References

1. George Costakis, "Which maps preserve universal functions?", in
   *Mini-Workshop: Complex Approximation and Universality*, Oberwolfach
   Reports 5 (2008), 328–331. Report DOI:
   https://doi.org/10.4171/OWR/2008/06 . Original whole report:
   https://ems.press/content/serial-article-files/46147 . Exact target:
   PDF page 34, printed page 330, Question 5; comparison: Theorem 6.
2. Luis Bernal-González, J. Alberto Conejero, George Costakis, and Juan B.
   Seoane-Sepúlveda, "Multiplicative structures of hypercyclic functions
   for convolution operators", *Journal of Operator Theory* 80:1 (2018),
   213–224. DOI: https://doi.org/10.7900/jot.2017sep27.2162 . Whole paper:
   https://jot.theta.ro/jot/archive/2018-080-001/2018-080-001-011.pdf .
3. George Costakis, "Common Cesàro hypercyclic vectors", *Studia
   Mathematica* 201:3 (2010), 203–226. DOI:
   https://doi.org/10.4064/sm201-3-1 . Publisher download:
   https://www.impan.pl/shop/en/publication/transaction/download/product/90964 .

All source claims above are paraphrases. Whole-file hashes, exact
inspection scope, and publication boundaries are recorded separately in
SOURCES.json. The source bodies and images are not distributed.

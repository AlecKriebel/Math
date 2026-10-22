# Composite least-prime-factor overshoot: a density theorem

## Publication and review scope

This is an unrefereed AI-assisted prose-only edition. “Accepted” means an independent internal AI audit of the partial density theorem, with no external human peer review, journal acceptance, or formal proof-assistant certification claimed. The complete substantive mathematical proof and audit are retained. Only an inline-math formatting typo was corrected before the original candidate was sealed; no mathematical correction is required. Eventual positivity and pointwise divergence remain unresolved by this work. The variance estimate is classical, recorded by Montgomery (2010) and attributed there to Hausman and Shapiro (1973); no novelty or priority of the density corollary is claimed. Executable programs, raw datasets, detailed execution receipts, full computational certificates, and copied source documents are omitted. This is not an executable reproduction package. Edition preparation performed byte-integrity and publication-structure checks, with no new mathematical test execution or scholarly-source retrieval or inspection.

## Scope and result

For every integer $n\geq5$, define

\[
F(n)=\max_{\substack{4\leq m<n\\m\text{ composite}}}\bigl(m+p(m)\bigr),
\qquad G(n)=F(n)-n,
\]

where $p(m)$ is the **least** prime divisor. The restriction to composites,
the strict inequality $m<n$, and the plus sign are used throughout.

**Theorem.** For every fixed real $K\geq0$,

\[
\lim_{X\to\infty}\frac1X\#\{5\leq n\leq X:G(n)\leq K\}=0. \tag{1}
\]

Thus $G(n)$ tends to infinity **in natural density**. This does not prove
that $F(n)>n$ eventually, nor that $G(n)\to\infty$ pointwise. The
exceptional set in (1) is not proved finite for even one fixed $K$.

This is an elementary consequence of the classical second-moment estimate
for reduced residues. That estimate is explicitly recorded in H. L.
Montgomery, *The combinatorics of moment calculations*, Hardy-Ramanujan
Journal 33 (2010), 2--22, Section 3, printed p. 7, immediately after (15).
Montgomery attributes the exact second-moment formula to M. Hausman and
H. N. Shapiro, *On the mean square distribution of primitive roots of
unity*, Communications on Pure and Applied Mathematics 26 (1973),
539--547. The density conclusion here is a direct corollary of that
established estimate; no novelty claim is made. For independent checking,
a self-contained proof of the special case needed here follows.

## 1. An exact finite probability model

Let $Q\geq2$ be even and squarefree, let

\[
v=\frac{\varphi(Q)}Q=\prod_{p\mid Q}(1-1/p),
\]

and let $H\geq1$ be an integer. Choose $a$ uniformly from the $Q$
residue classes. Put

\[
S(a)=\sum_{h=1}^H 1_{\gcd(a-h,Q)=1}.
\]

No independence of the $H$ summands is assumed. Each has expectation
$v$, so $\mathbb E S=Hv$.

**Lemma 1 (classical reduced-residue variance bound).**

\[
\operatorname{Var}(S)\leq Hv. \tag{2}
\]

**Proof.** Write

\[
C=\prod_{\substack{p\mid Q\\p>2}}\frac{p(p-2)}{(p-1)^2},
\qquad
g(r)=\prod_{p\mid r}\frac1{p-2}\quad(r\mid Q/2),
\]

with empty products equal to 1. For a positive integer $d$, let $J(d)$
be the probability that both $a$ and $a-d$ are coprime to $Q$.
The Chinese remainder theorem gives

\[
J(d)=\prod_{\substack{p\mid Q\\p\mid d}}(1-1/p)
     \prod_{\substack{p\mid Q\\p\nmid d}}(1-2/p).
\]

If $d$ is odd, its factor at $p=2$ is zero. If $d$ is even, factoring
out the value for an odd prime not dividing $d$, and expanding a finite
product, gives

\[
J(d)=2v^2C\sum_{\substack{r\mid Q/2\\2r\mid d}}g(r). \tag{3}
\]

Formula (3), with an empty sum, is valid for odd $d$ as well. Indeed the
relative factor for an odd $p\mid d$ is

\[
\frac{p/(p-1)}{p(p-2)/(p-1)^2}
=\frac{p-1}{p-2}=1+\frac1{p-2}.
\]

There are $2(H-d)$ ordered pairs of distinct positions in
$\{1,\ldots,H\}$ with difference of absolute value $d$. Therefore

\[
\begin{aligned}
\mathbb E[S(S-1)]
&=2\sum_{d=1}^{H-1}(H-d)J(d)\\
&=4v^2C\sum_{r\mid Q/2}g(r)
  \sum_{\substack{\ell\geq1\\2r\ell<H}}(H-2r\ell).
\end{aligned} \tag{4}
\]

All sums here are finite and all terms nonnegative. Since
$t\mapsto\max(H-2rt,0)$ is nonincreasing on $[0,\infty)$,

\[
\sum_{\substack{\ell\geq1\\2r\ell<H}}(H-2r\ell)
\leq\int_0^{H/(2r)}(H-2rt)\,dt
=\frac{H^2}{4r}. \tag{5}
\]

The finite Euler product cancels exactly:

\[
C\sum_{r\mid Q/2}\frac{g(r)}r
=\prod_{\substack{p\mid Q\\p>2}}
\frac{p(p-2)}{(p-1)^2}
\left(1+\frac1{p(p-2)}\right)=1. \tag{6}
\]

Combining (4)--(6) gives $\mathbb E[S(S-1)]\leq H^2v^2$.
Consequently

\[
\operatorname{Var}(S)
=\mathbb E[S(S-1)]+Hv-(Hv)^2\leq Hv.
\]

This proves (2), for every $H$, including $H\geq Q$. $\square$

**Corollary 2.** The proportion of residue classes with $S(a)=0$ is at
most $1/(Hv)$. More generally, the proportion with $S(a)<Hv/2$ is at
most $4/(Hv)$.

**Proof.** In the first event, $(S-Hv)^2=(Hv)^2$; in the second it exceeds
$(Hv)^2/4$. Average these inequalities and apply (2). Bounds larger
than 1 are allowed and simply uninformative. $\square$

## 2. Two elementary estimates, with no prime-distribution hypothesis

Let $y\geq2$ be an integer, $Q_y=\prod_{p\leq y}p$, and
$v_y=\varphi(Q_y)/Q_y$.

**Lemma 3.** $v_y\geq1/(2\sqrt y)$.

**Proof.** Let $R=\lfloor(y-1)/2\rfloor$. Enlarging the set of odd primes
to all odd integers from 3 to $2R+1$ can only decrease a product of
positive factors smaller than 1. Thus

\[
v_y\geq\frac12\prod_{j=1}^R\frac{2j}{2j+1}.
\]

Each squared factor satisfies
$\bigl(2j/(2j+1)\bigr)^2\geq(2j-1)/(2j+1)$. Multiplication telescopes, giving

\[
\left(\prod_{j=1}^R\frac{2j}{2j+1}\right)^2
\geq\frac1{2R+1}\geq\frac1y.
\]

The argument includes $R=0$ by the empty-product convention. $\square$

**Lemma 4.** The primes have natural density zero.

**Proof.** For each fixed $z\geq2$, all primes exceeding $z$ are
coprime to $Q_z$. Counting complete residue periods gives

\[
\limsup_{X\to\infty}\frac{\pi(X)}X\leq v_z.
\]

Also the convergent geometric expansion of the finite Euler product
contains every term $1/j$ with $1\leq j\leq z$, so

\[
v_z^{-1}=\prod_{p\leq z}(1-1/p)^{-1}
\geq\sum_{j=1}^z\frac1j\longrightarrow\infty.
\]

Let $z\to\infty$. No prime number theorem is required. $\square$

## 3. Transfer to composite witnesses and the order of limits

Fix $K\geq0$. Choose an integer $H\geq\max(1,\lceil K\rceil)$, set
$y=2H$, and **hold $H,y,Q_y$ fixed while $X\to\infty$**.

For an integer $n>H+1$, if $S(n)>0$, there is an $h\in\{1,\ldots,H\}$
such that $m=n-h>1$ is coprime to $Q_y$. If this $m$ is composite,
its least prime factor satisfies $p(m)>y$, and

\[
F(n)-n\geq p(m)-h>y-H=H\geq K. \tag{7}
\]

The strict $m<n$ is guaranteed by $h\geq1$. The **only alternative**
for $m>1$ is that $m$ is prime. Accordingly, for $n>H+1$,

\[
\{n:G(n)\leq K\}
\subseteq\{n:S(n)=0\}\ \cup\
\bigcup_{h=1}^H\{n:n-h\text{ is prime}\}. \tag{8}
\]

The first set on the right is periodic modulo the fixed $Q_y$; its
natural density is at most $1/(Hv_y)$ by Corollary 2. Each of the
finitely many shifted-prime sets has density zero by Lemma 4. The finitely
many $n\leq H+1$ also have density zero. Hence

\[
\limsup_{X\to\infty}\frac1X\#\{5\leq n\leq X:G(n)\leq K\}
\leq\frac1{Hv_{2H}}
\leq\frac{2\sqrt2}{\sqrt H}. \tag{9}
\]

Now, **after taking the upper density for each fixed $H$**, let $H$
tend to infinity. The right side tends to zero. This proves (1).

There is no interchange of a growing modulus with an unproved uniform
prime-density estimate. In particular, (9) does not say that every large
integer avoids the exceptional residue classes.

## 4. A finite two-parameter inequality

The same argument gives a checkable finite inequality, useful for making
the quantifiers explicit. Let $K\geq0$, let $H\geq1$, and choose an
integer $y\geq\max(2,\lceil H+K\rceil)$. Set $Q=Q_y$ and $v=v_y$.
For an integer $X\geq5$, let

\[
B_K(X)=\#\{5\leq n\leq X:G(n)\leq K\}.
\]

Then

\[
B_K(X)\leq H+1+\frac{X+Q}{Hv}+H\pi(X), \tag{10}
\]

and also

\[
B_K(X)\leq H+1+\frac{4(X+Q)}{Hv}+\frac{2\pi(X)}v. \tag{11}
\]

For (10), count zero-survivor residue classes over at most
$\lfloor X/Q\rfloor+1$ periods and use (8). For (11), separate
$S(n)<Hv/2$, controlled by Corollary 2, from $S(n)\geq Hv/2$.
At a bad $n>H+1$, every one of its $S(n)$ survivors must be prime by
(7), now with $p(m)-h>y-H\geq K$. Across all $n\leq X$, the total
number of prime incidences $n-h$ is at most $H\pi(X)$. Thus the latter
class has size at most $2H\pi(X)/(Hv)=2\pi(X)/v$. The added $H+1$
covers all small-$n$ endpoint issues. No computational data are used in
(10) or (11).

## 5. An exact obstruction to a bounded-prime approach

**Proposition 5.** Fix $y\geq2$. If $Q_y\mid n$ and $m<n$ is
composite with $p(m)\leq y$, then $m+p(m)\leq n$.

**Proof.** Write $p=p(m)$. Then $p\mid Q_y\mid n$ and $p\mid m$,
so the positive integer $n-m$ is a multiple of $p$. It is at least
$p$, which is precisely the assertion. $\square$

There are arbitrarily large multiples of each fixed $Q_y$. Therefore
no strategy that restricts all its positive-gap witnesses to a fixed
finite set of least prime factors can prove eventual positivity. This
does **not** make those multiples counterexamples to the original
problem: a witness whose least prime factor exceeds $y$ may exist.
The related short-window primorial obstruction is already discussed in
Tao's 2024 article; the proposition above states the bounded-prime
obstruction with no auxiliary prime-distribution theorem.

For the density proof, when $Q_y\mid n$ and $1\leq H\leq y$, the
coprimality count $S(n)$ is exactly 1: $h=1$ survives, while each
$2\leq h\leq H$ has a prime divisor at most $y$. Whether $n-1$ is
composite remains essential. This illustrates why the proof controls
proportions, not every exceptional residue.

## 6. Endpoint and scale checks

For every $n\geq5$, $F(n)\geq n$: if $n$ is odd use the composite
$n-1$, with least prime factor 2; if $n$ is even use the composite
$n-2$, again with least prime factor 2. Every $m+p(m)$ is even.
Moreover, if $n$ is even and $n-1$ is composite, its least prime
factor is at least 3 and $F(n)\geq n+2$. Consequently $F(n)=n$ is
possible only when $n-1$ is an odd prime.

For every admissible $m$, $p(m)\leq\sqrt m$, so

\[
F(n)\leq n-1+\lfloor\sqrt{n-1}\rfloor<n+\sqrt n. \tag{12}
\]

This is the correct orientation of the elementary upper bound; it is
not the reversed inequality printed in the 1979 scan.

If $q$ is prime and $n=q^2+1$, the witness $m=q^2$, together with
(12), yields the exact identity

\[
F(q^2+1)=q^2+q,\qquad G(q^2+1)=q-1. \tag{13}
\]

In particular the normalized limsup of $G(n)/\sqrt n$ is 1. This
subsequence assertion also does not imply either requested universal
statement.

## 7. Residual and acceptance boundary

The attempted route ends at the density theorem (1), the finite bounds
(10)--(11), and the exact obstruction in Proposition 5. It provides no
upper bound on the largest exceptional $n$, and no proof that such a
largest $n$ exists. To settle either original target, one must control
the sparse exceptional integers left by the average argument. A
uniform rough-composite witness theorem at intermediate scales would
suffice, but is not established here. The stronger semiprime-gap
conditions discussed by Tao are conditional routes, not available
hypotheses in this proof.

No equivalence with EP-430 is used. In particular no argument here
relies on the malformed minus-sign orientation in the imported
description. The EP-430 convention about excluding the integer 1 also
does not enter the proof.

## References and attribution boundaries

1. P. Erdős, *Some unconventional problems in number theory*, Acta
   Mathematica Academiae Scientiarum Hungaricae 33 (1979), 71--80,
   printed p. 73 / PDF page 3.
   https://users.renyi.hu/~p_erdos/1979-23.pdf
2. P. Erdős and R. L. Graham, *Old and new problems and results in
   combinatorial number theory*, Monographies de L'Enseignement
   Mathématique 28 (1980), printed p. 74 / PDF page 70.
   https://mathweb.ucsd.edu/~ronspubs/80_11_number_theory.pdf
3. H. L. Montgomery, *The combinatorics of moment calculations*,
   Hardy-Ramanujan Journal 33 (2010), 2--22, Section 3, printed p. 7 /
   PDF page 6; historical attribution on printed p. 21 / PDF page 20.
   https://hrj.episciences.org/168/pdf
4. M. Hausman and H. N. Shapiro, *On the mean square distribution of
   primitive roots of unity*, Communications on Pure and Applied
   Mathematics 26 (1973), 539--547. Historical attribution verified in
   [3]; this attempt did not inspect the original 1973 article.
   https://doi.org/10.1002/cpa.3160260407
5. T. Tao, *Erdos problem #385, the parity problem, and Siegel zeroes*,
   19 August 2024. Used for contextual obstructions and attribution,
   not as a hypothesis for (1).
   https://terrytao.wordpress.com/2024/08/19/erdos-problem-385-the-parity-problem-and-siegel-zeroes/

The source search identified the variance estimate as classical. It did
not establish priority for the elementary density corollary. The
present contribution is an authored, self-contained derivation and
auditable scope statement, not a claimed solution of EP-385.

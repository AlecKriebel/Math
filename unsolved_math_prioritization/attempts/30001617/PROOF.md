# An L2 counterexample to the unrestricted dyadic tail LIL

## Result, scope, and attribution

There exists a real function \(f\in L^2([0,1))\), with dyadic interval
averages \(f_n=\mathbb E(f\mid\mathcal F_n)\), such that
\[
 Q_n(x)=\sum_{j=n+1}^{\infty}(f_j(x)-f_{j-1}(x))^2>0,
 \qquad Q_n(x)\longrightarrow0,
\]
and, for almost every \(x\in[0,1)\),
\[
 \limsup_{n\to\infty}
 \frac{|f(x)-f_n(x)|}{\sqrt{Q_n(x)\log\log(1/Q_n(x))}}=+\infty. \tag{1}
\]
The logarithmic expression is used for sufficiently large \(n\), when
\(Q_n<e^{-e}\). In fact, the construction has total realized square
function at most one on every binary path. Extending \(f\) by zero outside
\([0,1)\) gives a real, globally integrable, locally integrable function
on \(\mathbb R\) disproving the unrestricted question recorded by
Artur Nicolau in Oberwolfach Report 49/2010, printed p. 2872 [1].

The negative phenomenon is prior work of Santosh Ghimire. His 2011
Prairie Analysis Seminar presentation [2], PDF pp. 51-69, presents a
repeated-block counterexample, and his 2012 Kansas State dissertation
[3], Section 3.3, printed pp. 50-59 (PDF pp. 59-68), gives an extended
construction. The proof below is a self-contained all-positive-block
reconstruction of that mechanism. It does not assert novelty and does
not import the numerical estimates or exponential inequalities in those
sources. The dissertation's final normalization, printed p. 59, is
\(S'_n\sqrt{\log\log(1/(S'_n)^2)}\), where \((S'_n)^2=Q_n\).

## 1. Deterministic parameters

Throughout, \(\log\) is the natural logarithm. For an integer \(k\ge1\)
and \(0<a<e^{-e}\), put
\[
 \ell(a)=\log\log(1/a^2),\qquad
 m_k(a)=\lceil64k^2\ell(a)\rceil,
\]
\[
 L_k(a)=\lceil 2^{m_k(a)}(k+2)\log2\rceil,
 \qquad b_k(a)=L_k(a)a^2. \tag{2}
\]
All are finite, and \(m_k(a),L_k(a)\) are positive integers. For fixed
\(k\), \(b_k(a)\to0\) as \(a\downarrow0\). Indeed, if
\(t=\log(1/a^2)\), the ceiling bounds give
\[
 2^{m_k(a)}\le2t^{64k^2\log2},
\qquad
 b_k(a)\le e^{-t}\bigl(2(k+2)\log2\,t^{64k^2\log2}+1\bigr)\to0.
\]
Here \(k\) is fixed during the limit. No estimate uniform in \(k\)
is needed.

Inductively choose \(a_k\in(0,e^{-e})\) so small that, writing
\(m_k=m_k(a_k)\), \(L_k=L_k(a_k)\), \(\ell_k=\ell(a_k)\), and
\(b_k=L_ka_k^2\),
\[
 b_k\le 2^{-k}\min(1,a_1^2,\ldots,a_{k-1}^2). \tag{3}
\]
The minimum for \(k=1\) is one. At every step its value is strictly
positive, and the preceding limit guarantees a choice. In particular,
\[
 \sum_{k\ge1}b_k\le1,
\qquad a_k^2\le b_k\le2^{-k},
\qquad a_k\to0. \tag{4}
\]
For every fixed \(k\), each \(j>k\) in (3) has
\(b_j\le2^{-j}a_k^2\). Thus
\[
 B_k:=\sum_{j>k}b_j\le
 a_k^2\sum_{j=k+1}^{\infty}2^{-j}=2^{-k}a_k^2. \tag{5}
\]
This deterministic bound, rather than an average over successful paths,
will control all future increments.

## 2. A predictable dyadic martingale

Use \([0,1)\) with Lebesgue probability measure. Let \(r_j\) be the
independent fair signs supplied by the binary digits, and let
\(\mathcal F_n=\sigma(r_1,\ldots,r_n)\). Its atoms are the standard
half-open dyadic intervals of length \(2^{-n}\). Choose the terminating
binary expansion at dyadic rationals; changing that null set does not
affect any assertion. Let \(\mathcal F_0\) be the trivial sigma-algebra.

Set \(M_0=0\) and
\[
 M_k=M_{k-1}+m_kL_k.
\]
Stage \(k\) uses digits \(M_{k-1}+1,\ldots,M_k\), partitioned into
\(L_k\) consecutive potential blocks of length \(m_k\). For a block
\(h\in\{1,\ldots,L_k\}\), write
\[
 s_{k,h}=M_{k-1}+(h-1)m_k,
\qquad
 H_{k,h}=\{r_{s_{k,h}+1}=\cdots=r_{s_{k,h}+m_k}=+1\}.
\]
These potential events are defined even if the block is never active.
Define the block's activation indicator by
\[
 A_{k,h}=\prod_{u<h}\mathbf1_{H_{k,u}^{\,c}},
\]
with empty product one. For \(1\le v\le m_k\), set
\[
 d_{s_{k,h}+v}=\frac{a_k}{\sqrt{m_k}}\,A_{k,h}\,r_{s_{k,h}+v}. \tag{6}
\]
Thus every increment in an active block is used, even if an earlier
sign in that same block was negative. Stopping occurs only after the
whole block, and only when it is all positive. The next stage resets
to active independently of the preceding stage's outcome.

The indicator \(A_{k,h}\) is \(\mathcal F_{s_{k,h}}\)-measurable. In
particular it is known before every digit to which it is applied.
Consequently \(d_j\) is \(\mathcal F_j\)-measurable, bounded, and
\(\mathbb E(d_j\mid\mathcal F_{j-1})=0\). Define
\[
 f_0=0,\qquad f_n=\sum_{j=1}^n d_j.
\]
This is an ordinary dyadic martingale. Its differences need not be
independent; only the fresh signs and the potential-block events are
independent.

An active whole block contributes exactly \(a_k^2\) to
\(\sum d_j^2\). Hence for every binary path,
\[
 \sum_{j=1}^{\infty}d_j^2
 \le\sum_{k=1}^{\infty}L_ka_k^2
 =\sum_{k=1}^{\infty}b_k\le1. \tag{7}
\]
More precisely, ignoring all stopping gives deterministic coefficient
squares whose sum is \(\sum b_k\). Their deterministic tails tend to
zero. This observation also deals with indices inside a stage.

## 3. L2 and almost-sure convergence to one terminal function

For \(i<j\), the martingale difference property gives
\[
 \mathbb E(d_i d_j)
 =\mathbb E\{d_i\mathbb E(d_j\mid\mathcal F_{j-1})\}=0.
\]
Tonelli's theorem and (7) imply
\(\sum_j\mathbb E d_j^2\le1\). Therefore
\[
 \mathbb E|f_m-f_n|^2=\sum_{j=n+1}^m\mathbb E d_j^2\to0
 \quad(m,n\to\infty).
\]
Completeness of \(L^2\) gives a real \(f\in L^2\) with
\(f_n\to f\) in \(L^2\) and \(\|f\|_2^2\le1\).

For completeness, almost-sure convergence follows from a finite
martingale maximal inequality with the hypotheses already checked.
If \(X_i=f_i-f_N\), \(N\le i\le m\), and \(E_i\) is the event
that \(i\) is the first time \(|X_i|>\lambda\), then the \(E_i\)
are disjoint and \(E_i\in\mathcal F_i\). The conditional mean of
\(X_m-X_i\) at time \(i\) is zero, so
\[
 \mathbb E(X_m^2\mathbf1_{E_i})
 =\mathbb E(X_i^2\mathbf1_{E_i})
   +\mathbb E((X_m-X_i)^2\mathbf1_{E_i})
 \ge\lambda^2\mathbb P(E_i).
\]
Summing and then increasing \(m\) proves
\[
 \mathbb P\{\sup_{i\ge N}|f_i-f_N|>\lambda\}
 \le\lambda^{-2}\sum_{j>N}\mathbb E d_j^2. \tag{8}
\]
Choose increasing deterministic \(N_l\) for which the last tail sum
is at most \(2^{-4l}\), and set \(\lambda=2^{-l}\). The right side
of (8) is at most \(2^{-2l}\), which is summable. The first
Borel-Cantelli lemma shows that \((f_n)\) is Cauchy almost surely.
Its almost-sure limit equals its \(L^2\) limit \(f\), since convergence
in \(L^2\) implies convergence in probability.

For each fixed \(n\) and every \(m\ge n\), the martingale identity
gives \(\mathbb E(f_m\mid\mathcal F_n)=f_n\). Conditional expectation
is a contraction on \(L^2\); passing to the limit gives
\[
 f_n=\mathbb E(f\mid\mathcal F_n). \tag{9}
\]
On each positive-measure dyadic atom this conditional expectation is
its interval average. Thus the entire sequence is the sequence of
dyadic averages of a single terminal function, not merely an abstract
pointwise-convergent martingale. All identities for countably many
indices may be imposed on one full-measure set.

## 4. Success eventually occurs, and the future tail is small

For fixed \(k\), the events \(H_{k,h}\), \(1\le h\le L_k\), use
disjoint digit sets, so they are independent, with common probability
\(p_k=2^{-m_k}\). The actual stage succeeds if and only if at least
one of these potential events occurs: until the first such event all
blocks are active. Hence
\[
 \mathbb P(\text{stage }k\text{ has no success})
 =(1-p_k)^{L_k}
 \le e^{-p_kL_k}
 \le e^{-(k+2)\log2}=2^{-(k+2)}. \tag{10}
\]
The sum of these probabilities is finite. The first Borel-Cantelli
lemma implies success at every sufficiently large stage almost surely.
It does not require independence between stages.

At the deterministic stage end, let \(R_k=f-f_{M_k}\). L2 convergence,
orthogonality, and the pathwise bound on future stages give
\[
 \mathbb E R_k^2
 =\sum_{j>M_k}\mathbb E d_j^2
 \le\sum_{h>k}b_h=B_k\le2^{-k}a_k^2. \tag{11}
\]
Chebyshev's inequality yields
\(\mathbb P(|R_k|>a_k)\le2^{-k}\). Applying the first
Borel-Cantelli lemma again shows
\[
 |R_k|\le a_k\quad\text{for all sufficiently large }k,
 \quad\text{almost surely}. \tag{12}
\]
There is no conditioning on the eventual successful block, no assertion
of independence of the events in (12), and no optional sampling.

## 5. The divergent subsequence

On a successful stage, let \(h_k\) be its first all-positive block
and let \(n_k=s_{k,h_k}\), the index just before that block. This
index is chosen using future signs and is not asserted to be a stopping
time. Only pathwise identities are used at this index.

The successful block has \(m_k\) positive increments of size
\(a_k/\sqrt{m_k}\), and all later increments in that stage vanish.
Therefore
\[
 f-f_{n_k}=a_k\sqrt{m_k}+R_k, \tag{13}
\]
\[
 a_k^2\le Q_{n_k}=a_k^2+\sum_{j>M_k}d_j^2
 \le a_k^2+B_k\le2a_k^2. \tag{14}
\]
The final upper bound is deliberately loose; (5) is stronger.

For \(0<q<e^{-e}\), differentiation gives
\[
 \frac{d}{dq}\bigl(q\log\log(1/q)\bigr)
 =\log\log(1/q)-\frac1{\log(1/q)}>0.
\]
Indeed \(\log(1/q)>e\), so the first term exceeds one and the
second is less than \(1/e\). Also
\(2a_k^2<2e^{-2e}<e^{-e}\), and
\(\ell_k>\log(2e)>1\). By (14) and monotonicity,
\[
 Q_{n_k}\log\log(1/Q_{n_k})
 \le2a_k^2\log\log(1/(2a_k^2))
 \le2a_k^2\ell_k. \tag{15}
\]
On the common full-measure set of eventual success and (12), (13)
and (2) give
\[
 |f-f_{n_k}|\ge a_k(\sqrt{m_k}-1)
 \ge a_k(8k\sqrt{\ell_k}-1).
\]
Combining this with (15),
\[
 \frac{|f-f_{n_k}|}{\sqrt{Q_{n_k}\log\log(1/Q_{n_k})}}
 \ge\frac{8k-1/\sqrt{\ell_k}}{\sqrt2}
 \ge\frac{8k-1}{\sqrt2}\longrightarrow+\infty. \tag{16}
\]
Each stage has finite, positive length, and
\(n_k\in[M_{k-1},M_k-m_k]\); successive successful stages therefore
give strictly increasing indices tending to infinity.

By (7), \(Q_n\to0\). Moreover, every later stage has an active first
block even if it never succeeds, so \(Q_n>0\) for every finite \(n\)
on every path. Thus the denominator is eventually defined and positive,
not only along the chosen subsequence. Equation (16) proves (1).

## 6. Exact match to the real-line question

Define \(F=f\) on \([0,1)\) and \(F=0\) elsewhere. Since
\(\|f\|_1\le\|f\|_2\), \(F\in L^1(\mathbb R)\), in particular
\(F\in L^1_{\mathrm{loc}}(\mathbb R)\). For \(x\in[0,1)\) and
\(n\ge0\), the standard dyadic interval of length \(2^{-n}\)
containing \(x\) lies in \([0,1)\); its average of \(F\) is \(f_n(x)\).
There is no boundary-crossing error.

The source square function has index
\(\sum_{k\ge n}(F_{I_{k+1}(x)}-F_{I_k(x)})^2\), which equals
\(\sum_{j>n}d_j(x)^2=Q_n(x)\) after \(j=k+1\). For
\(0<Q_n<e^{-e}\),
\[
 |\log|\log Q_n||=\log\log(1/Q_n).
\]
The normalized limsup in the source therefore equals the one in (1)
almost everywhere on \([0,1)\). Failure on this measure-one subset
is sufficient to disprove an assertion stated to hold almost everywhere
on \(\mathbb R\); no claim about the undefined zero-over-zero expression
outside the support is needed.

## 7. Why the conditional positive theorem does not apply

Ghimire's dissertation Theorem 29 (printed p. 34), the presentation's
PDF p. 50, and Acharya-Ghimire's 2016 Theorem 1 [4] all explicitly
require one finite constant \(C\) controlling
\(S'_n(x)/S'_n(y)\) for every pair in each generation-\(n\) dyadic
interval. Here \(S'_n=\sqrt{Q_n}\). The all-\(n\) conclusion they
state is conditional on this hypothesis. It is not an unconditional
tail theorem for arbitrary dyadic martingales.

Our construction violates this hypothesis directly. Fix a stage
\(k\ge2\) and any atom \(I\) of \(\mathcal F_{M_{k-1}}\). The
subevent of \(I\) where the first block succeeds has positive measure
and on it
\(Q_{M_{k-1}}\le a_k^2+B_k\). The subevent where all \(L_k\)
potential blocks fail also has positive measure and on it
\(Q_{M_{k-1}}\ge L_ka_k^2\). Thus the square-root tail ratio for
points in the same atom can be at least
\[
 \sqrt{\frac{L_k}{1+2^{-k}}}\longrightarrow\infty.
\]
Both subevents retain positive measure after deleting any null set.
This excludes even an essential-version uniform comparison bound.

The 2016 paper also states a result along special selected times
(Theorem 2, PDF p. 2). A bound along one selected subsequence does not
bound the full limsup; we neither need nor certify that theorem's proof.
No positive LIL theorem is imported in the present construction.

## References

1. *Operator Theory and Harmonic Analysis*, Oberwolfach Report 49/2010,
   DOI 10.4171/OWR/2010/49, Artur Nicolau's first question, printed p. 2872,
   PDF p. 60. [Report](https://ems.press/content/serial-article-files/46308).
2. Santosh Ghimire, *Law of the iterated logarithm for tail sums*,
   Prairie Analysis Seminar, Kansas State University, October 21-22, 2011.
   Conditional theorem: PDF p. 50; counterexample: PDF pp. 51-69.
   [Presentation](https://www.math.ksu.edu/about/events/conference/pas/2011/talks/Prairie%20Analysis%20pause.pdf).
3. Santosh Ghimire, *The law of the iterated logarithm for tail sums*,
   Ph.D. dissertation, Kansas State University, 2012. Section 3.3,
   printed pp. 50-59; Theorem 29, printed p. 34.
   [Record](https://hdl.handle.net/2097/13647),
   [institutional PDF](https://krex.k-state.edu/bitstreams/988fff3e-b27c-42e4-b215-308672e268fa/download).
4. Ananta Acharya and Santosh Ghimire, *A Law of the Integrated Logarithm
   for the Tail Sums of Dyadic Martingales Using Stopping Times*,
   *Journal of Advanced College of Engineering and Management* 2 (2016),
   Theorems 1 and 2, PDF p. 2.
   [Article PDF](https://www.nepjol.info/index.php/JACEM/article/view/16100/13051).

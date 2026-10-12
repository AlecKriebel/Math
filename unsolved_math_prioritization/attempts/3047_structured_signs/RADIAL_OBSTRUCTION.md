# Finite structured sign changes retain the partition growth constant

## Public edition reading note

Read this proof with the governing [final radial caveat](GENERAL_RADIAL_CAVEAT.md) and [independent scope supplement](RADIAL_SCOPE_SUPPLEMENT.md). They establish, by Güntürk's cited theorem and elementary harmonic amplification, that finitely many arbitrary active factors can already achieve suppression stronger than the partition radial-growth threshold. This supersedes any impression from section 6's historical heading or closing wording that radial suppression alone remains the missing obstacle. Section 6's necessary-condition inequalities remain valid; bounded Taylor coefficients remain unproved. Every word of the original proof is retained below. This added notice only identifies the governing later supplement.

## Scope

This note concerns the independently signed unrestricted-partition product
\[
P(q)=\prod_{m\ge1}\left(1+\sum_{j\ge1}\epsilon_{m,j}q^{mj}\right),
\qquad \epsilon_{m,j}\in\{-1,1\}.
\]
Only a finite set \(S\) of factors is active here: outside \(S\), all signs are +1. An active factor can contain infinitely many changed coefficients. That condition is different from changing only finitely many coefficients in the whole product.

The theorem below rules out bounded coefficients for two precisely specified classes of active factors. It does not rule out arbitrary sign sequences in a fixed finite collection of factors, and it does not settle Newman's unrestricted problem. It is independent of the accepted degree-86 obstruction for at most two arbitrary active factors.

Write
\[
f_m(z)=1+\sum_{j\ge1}\epsilon_{m,j}z^j \quad(m\in S),
\qquad E(q)=\prod_{m\ge1}(1-q^m)^{-1}.
\]
Then
\[
P(q)=E(q)\prod_{m\in S}(1-q^m)f_m(q^m). \tag{1}
\]
All these expressions define analytic functions for \(|q|<1\), in addition to their formal-series meaning. The positive partition product converges there, and only finitely many factors are replaced.

## Theorem

Suppose each active \(f_m\) is of either of the following two types, with arbitrary mixing between factors.

**Binary-digit multiplicative type.** There are independent signs \(\sigma_{m,k}\in\{-1,1\}\), \(k\ge0\), such that
\[
f_m(z)=\prod_{k\ge0}(1+\sigma_{m,k}z^{2^k}). \tag{2}
\]
Equivalently, if \(j=\sum_{k\ge0}d_k2^k\) with \(d_k\in\{0,1\}\), then
\[
\epsilon_{m,j}=\prod_{k:d_k=1}\sigma_{m,k}.
\]
There is no periodicity assumption on the sequence of digit signs. Unique binary expansion proves that every coefficient of (2) is exactly +1 or −1. This class is a genuine restriction on the independently assignable coefficients of the original problem.

**Rational type.** The series \(f_m\) is a rational function, still with constant coefficient 1 and every nonconstant coefficient in \(\{-1,1\}\). This is equivalent to its coefficient-sign sequence being eventually periodic; the equivalence is proved below.

Write \(P(q)=\sum_{n\ge0}a_nq^n\), and use natural logarithms. Then
\[
\lim_{t\downarrow0}t\log|P(e^{-t})|=\frac{\pi^2}{6}, \tag{3}
\]
and
\[
\limsup_{n\to\infty}\frac{\log\max\{1,|a_n|\}}{\sqrt n}
=\pi\sqrt{\frac23}. \tag{4}
\]
In particular, the coefficients are unbounded and are not bounded by any fixed polynomial in \(n\). Thus no finite collection of active factors of these specified types solves the unrestricted sign problem. As a special case, changing finitely many coefficients anywhere cannot solve it.

No Hardy–Ramanujan asymptotic or Tauberian theorem is required for the proof. In particular, possible negative coefficients are handled using absolute-value bounds.

## 1. The partition product on the positive radius

For \(t>0\), absolute convergence of nonnegative sums gives
\[
\log E(e^{-t})
=\sum_{m\ge1}\sum_{\ell\ge1}\frac{e^{-tm\ell}}{\ell}
=\sum_{\ell\ge1}\frac{1}{\ell(e^{t\ell}-1)}. \tag{5}
\]
Since \(e^x-1\ge x\),
\[
0\le\frac{t}{\ell(e^{t\ell}-1)}\le\frac1{\ell^2}.
\]
For fixed \(\ell\), the left-hand expression tends to \(1/\ell^2\). Dominated convergence and the classical Basel sum imply
\[
\lim_{t\downarrow0}t\log E(e^{-t})
=\sum_{\ell\ge1}\frac1{\ell^2}=C,\qquad C=\frac{\pi^2}{6}. \tag{6}
\]
The same calculation gives the global bound
\[
\log E(e^{-t})\le C/t. \tag{7}
\]

## 2. A uniform lower bound for every binary digit-sign choice

Put \(a=\log2\), \(C_0=e/(e-1)^2\). For any sequence of digit signs, let
\[
B_\sigma(z)=\prod_{k\ge0}(1+\sigma_kz^{2^k}).
\]
For \(0<u\le1\), set \(L=\log(1/u)\). We claim the explicit uniform bounds
\[
-\frac{L^2}{2a}-\frac32L-a-C_0
\ \le\ \log B_\sigma(e^{-u})
\ \le\ L+\log2. \tag{8}
\]
The value on this radius is positive: every factor is positive, and the sum of the deviations of the factors from 1 is finite for each fixed \(u>0\), so their infinite product is nonzero.

For every sign choice,
\[
1-e^{-2^ku}\le1+\sigma_ke^{-2^ku}.
\]
Consequently it suffices for the lower bound to consider the all-negative product. Let
\[
J=\left\lceil\frac{L}{a}\right\rceil.
\]
Then \(1\le2^Ju<2\), except that the lower endpoint includes the cases of equality. For \(k<J\), the argument \(v=2^ku\) satisfies \(0<v<1\), and
\[
1-e^{-v}\ge v/2.
\]
For example, this follows from \(e^{-v}\le1-v+v^2/2\le1-v/2\) on \([0,1]\). Thus
\[
\sum_{k=0}^{J-1}\log(1-e^{-2^ku})
\ge-JL+\frac{aJ(J-1)}2-Ja. \tag{9}
\]
For the remaining terms, write \(k=J+h\). Their arguments are at least \(2^h\ge1\), so
\[
-\log(1-e^{-2^ku})
\le\frac{e^{-2^ku}}{1-e^{-2^ku}}
\le\frac{e^{-2^h}}{1-e^{-1}}.
\]
Since \(2^h\ge h+1\), summing gives
\[
-\sum_{k=J}^{\infty}\log(1-e^{-2^ku})
\le\frac1{1-e^{-1}}\sum_{h\ge0}e^{-(h+1)}=C_0. \tag{10}
\]
This treats the transition near \(2^ku=1\) without extending the small-argument estimate outside its range.

To simplify (9), write \(J=L/a+\theta\), \(0\le\theta<1\), with \(\theta=0\) when \(L/a\) is integral. The negative of its right-hand side equals
\[
\frac{L^2}{2a}+\frac32L+\frac a2(3\theta-\theta^2)
\le\frac{L^2}{2a}+\frac32L+a.
\]
Combining with (10) proves the lower bound in (8). The upper bound follows directly from the coefficient bound:
\[
0<B_\sigma(e^{-u})\le\sum_{j\ge0}e^{-uj}
=\frac1{1-e^{-u}}\le\frac2u.
\]
In particular, uniformly over all digit-sign choices,
\[
\lim_{u\downarrow0}u\log B_\sigma(e^{-u})=0. \tag{11}
\]

## 3. Rational factors and the distinction from arbitrary factors

A nonzero rational \(f\) has a finite integer order at \(z=1\): in a neighborhood of that point,
\[
f(z)=(1-z)^\nu g(z),\qquad \nu\in\mathbb Z,\quad g(1)\ne0,
\]
where \(g\) is analytic and nonvanishing nearby. Hence, for real \(u\downarrow0\),
\[
\log|f(e^{-u})|=\nu\log u+O(1),
\qquad u\log|f(e^{-u})|\longrightarrow0. \tag{12}
\]
Possible zeros elsewhere in the disk are irrelevant: the displayed local factorization supplies a zero-free punctured real neighborhood of 1. The constant coefficient 1 ensures that \(f\) is not identically zero.

For completeness, an eventually periodic sign sequence gives a rational generating function by summing its periodic tail as a geometric series. Conversely, a rational generating function gives, after a finite initial segment, a fixed linear recurrence that uniquely determines the next coefficient from a fixed finite number of previous coefficients. Because those coefficients take only the two values ±1, there are finitely many possible state tuples. Some state must recur, and determinism then forces eventual periodicity. No assertion of eventual periodicity is made for arbitrary nonrational signed factors.

If only finitely many coefficients in the whole original product are changed, only finitely many factors are active, and each such factor is eventually all-positive. Its series is rational, so this case is covered. By contrast, allowing arbitrary signs at infinitely many positions inside each of a finite number of factors is a strictly broader case not settled by this theorem.

## 4. Radial growth of the modified product

For each fixed active index \(m\), substitute \(u=mt\) into (11) or (12). It follows that
\[
t\log|f_m(e^{-mt})|\longrightarrow0.
\]
Also \(t\log(1-e^{-mt})\to0\). Since there are only finitely many active factors, (1) and (6) give
\[
t\log|P(e^{-t})|
=t\log E(e^{-t})
 +\sum_{m\in S}t\log\left|(1-e^{-mt})f_m(e^{-mt})\right|
\longrightarrow C.
\]
Every binary factor is positive on this radius, and every rational factor is nonzero sufficiently near 1. Thus the logarithm is defined for all sufficiently small positive \(t\), proving (3).

## 5. A Laplace estimate and signed coefficient growth

We first prove the elementary estimate, for every real \(A\ge0\),
\[
\lim_{t\downarrow0}t\log\sum_{n\ge0}e^{A\sqrt n-tn}=A^2/4. \tag{13}
\]
For any fixed \(0<\delta<1\), completing the square gives
\[
A\sqrt n-(1-\delta)tn\le\frac{A^2}{4(1-\delta)t}.
\]
Therefore
\[
\sum_{n\ge0}e^{A\sqrt n-tn}
\le\frac{\exp(A^2/[4(1-\delta)t])}{1-e^{-\delta t}}.
\]
Multiply its logarithm by \(t\), take the upper limit, then let \(\delta\downarrow0\); the result is at most \(A^2/4\). If \(A>0\), retaining just the term with \(n=\lfloor A^2/(4t^2)\rfloor\) gives the matching lower bound, since \(t\sqrt n\to A/2\) and \(t^2n\to A^2/4\). If \(A=0\), the sum equals \((1-e^{-t})^{-1}\), giving zero. This proves (13).

Each coefficient \(a_n\) is a sum of exactly \(p(n)\) partition contributions, and every contribution is +1 or −1. Consequently
\[
|a_n|\le p(n). \tag{14}
\]
Positivity of the coefficients of \(E\) and (7) imply, for every \(t>0\),
\[
p(n)\le\exp(nt+C/t).
\]
For \(n\ge1\), choose \(t=\sqrt{C/n}\). This gives
\[
\log\max\{1,|a_n|\}\le2\sqrt{Cn}, \tag{15}
\]
so the upper limit in (4) is at most \(2\sqrt C\).

For the reverse inequality, suppose that upper limit were strictly below \(2\sqrt C\). Choose a number \(A\) strictly between them. After absorbing the finitely many initial terms in a constant \(K\ge1\),
\[
|a_n|\le K e^{A\sqrt n}\quad(n\ge0).
\]
The triangle inequality and (13) then give
\[
\limsup_{t\downarrow0}t\log|P(e^{-t})|
\le\limsup_{t\downarrow0}t\log\left(K\sum_{n\ge0}e^{A\sqrt n-tn}\right)
=A^2/4<C.
\]
This contradicts (3). This argument never treats signed coefficients as nonnegative and never uses a signed Tauberian implication. Equations (14)–(15) and the Laplace bound prove (4).

## 6. The exact missing step for arbitrary finite active sets

The finite-active-set identity (1) remains valid for arbitrary independently chosen signs. If its final coefficients were bounded, then \(|P(e^{-t})|\le M/(1-e^{-t})\) for some fixed \(M\). Equations (1) and (6) would force
\[
\limsup_{t\downarrow0}t\log\left|\prod_{m\in S}f_m(e^{-mt})\right|\le-C, \tag{16}
\]
where a zero product is interpreted as logarithm \(-\infty\). More explicitly, for every \(0<c<C\) and all sufficiently small \(t>0\),
\[
\prod_{m\in S}|f_m(e^{-mt})|\le e^{-c/t}. \tag{17}
\]
For nonempty \(S\), at each such \(t\), at least one of the \(K=|S|\) factors must obey
\[
|f_m(e^{-mt})|\le e^{-c/(Kt)}. \tag{18}
\]
The identity of that factor may depend on \(t\); these inequalities do not justify a fixed factor being uniformly exponentially small on an entire interval.

The preceding theorem rules out (17) for the stated binary and rational classes by a **proved lower bound** for every factor. Merely knowing \(|\epsilon_{m,j}|=1\), or the upper estimate \(|f_m(r)|\le(1-r)^{-1}\), supplies no such lower bound. No lower-bound theorem for all arbitrary signed series is proved or assumed here. Excluding or constructing a product with behavior (17), while also satisfying all coefficient constraints, remains the obstacle to this radial strategy for unrestricted finite active sets.

## Source and status notes

The motivating unrestricted problem is [Newman's Open Problem Garden question](https://www.openproblemgarden.org/op/dividing_up_the_unrestricted_partitions). The binary-product class is naturally suggested by the identities in [Andrews–Newman, *Binary Representations and Theta Function*, Integers 18 (2018), A34](https://math.colgate.edu/~integers/s34/s34.pdf). That paper's identities use their specified sets of dilates. They are not invoked as identities for the full unrestricted product here. All estimates and coefficient-growth arguments used in this note are proved above. No novelty claim is made.

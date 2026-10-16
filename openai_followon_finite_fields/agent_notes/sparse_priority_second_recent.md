# Exact primary-source comparison: recent sparse factoring and perfect powers

Checkpoint: 2026-10-07 05:36 UTC. Assigned source audit completion: 100%.
Scope: independent comparison of four named sources; no external communication,
publication, Git operations, or edits to frozen research documents.

## Target and conclusion

Target under comparison: complete univariate factorization over
\(\mathbb F_{p^m}\), including multiplicities written in binary, within
\(\operatorname{poly}(t,\log N,m,\log p,D_{\rm out})\) bit operations, where
\(D_{\rm out}=\sum_i\deg h_i\) for the distinct dense irreducible factors.
The four inspected papers do not state that result. This finding does not
establish novelty against other literature or against compositions of other
theorems. Their degree symbols must not be substituted for \(D_{\rm out}\).

## Huang–Cao–Qiu–Gao

[arXiv:2607.02364v1](https://arxiv.org/abs/2607.02364v1), submitted
2026-07-02 16:06:29 UTC; the inspected
[primary HTML](https://arxiv.org/html/2607.02364v1) displays August 24, 2026
on its title page, although the arXiv history lists only v1.

Theorem 5.2, §5 (HTML lines 801–843), is deterministic exact-root
testing/extraction for a **supplied** integer \(e\ge2\):

\[
\operatorname{poly}(s^{O(D_{\rm in}d)},n,d,D_{\rm in})+sR(e),
\qquad d=\operatorname{indeg}(f),\quad D_{\rm in}=\operatorname{tdeg}(f).
\]

It treats positive characteristic, including \(p\mid e\), by inverse Frobenius
before reconstruction. Theorem 3.4 gives
\(\|g\|_0\le s^{D_{\rm in}(2d+2)/e+1}\).
Proof lines 842–843 condition scalar-cost absorption on available polynomial-cost
deterministic scalar-root routines; there is no explicit unconditional
\(\log p\) bit bound for \(R(e)\). For univariate input,
\(d=D_{\rm in}=N\), so the displayed arithmetic bound is
\(\operatorname{poly}(s^{O(N^2)},N)+sR(e)\).
Final ordinary sparse powering explains why supplied large \(e\) does not remove
this numerical-degree dependence. §6 explicitly leaves full irreducible
factorization open. Arbitrary unequal binary multiplicities are outside this
theorem's exact-power task.

## Chuyoon–Shpilka

[arXiv:2603.07589v1](https://arxiv.org/abs/2603.07589v1), submitted
2026-03-08 11:18:32 UTC;
[primary HTML](https://arxiv.org/html/2603.07589v1).

Theorem 1.9 outputs sparse divisors of an input whose **individual degree is
bounded by \(d\)** in deterministic
\(\operatorname{poly}(n,d!,s^d)\) time. Theorem 1.12 gives complete irreducible
factorization for that input class in
\(\operatorname{poly}(n,s^{d^2\log n})\) time. Its proof in §9.1 explicitly
works regardless of characteristic; these displayed bounds suppress field
factorization cost.

§2.2, Theorem 2.7 (HTML lines 446–449), uses deterministic finite-field
univariate factorization in
\(\operatorname{poly}(p,\log q,d)\), \(q=p^k\).
Theorem 2.8 transfers that cost to multivariate calls.
Thus “arbitrary fields” does not assert bit complexity polynomial in \(\log p\).

Theorem 1.10 reconstructs a blackbox product of \(\ell\), possibly repeated,
irreducible \((n,s,d)\)-sparse polynomials. Its large-characteristic bound is
\(\operatorname{poly}(n,d^d,s^{d\log\ell},\ell^d)\), requiring
\(p>2d\); the arbitrary-field alternative includes
\((d^2)!\), \(s^{d\log\ell+d^3}\), and \(\ell^d\).
Repeated factors contribute to \(\ell\), so \(\ell\) is not the number of
distinct output factors. For univariate sparse input, the input-degree
parameter is \(N\); these statements do not provide the target compressed
multiplicity bound.

## Bhattacharjee–Kothary–Rai–Saraf

[arXiv:2606.27293v1](https://arxiv.org/abs/2606.27293v1), submitted
2026-06-25 17:12:57 UTC;
[primary HTML](https://arxiv.org/html/2606.27293v1).

Theorem 1.1 / 4.1, for input individual degree \(d\) and \(p>d\) (or
characteristic zero), produces an \(s^d\)-size **candidate circuit list**
containing all factors without monomial divisors; spurious circuits are allowed.
Time is \(\operatorname{poly}(s^d,d!,n)\), multiplied by the suppressed
univariate factorization cost \(\mathcal T(\mathbb F,d)\) (Remark 4.2).

For arbitrary fields and input individual degree \(N\), Theorem 1.7 / 5.1
outputs a list containing the factors of individual degree at most \(d\), again
allowing spurious elements. The exact displayed bound is
\[
\operatorname{poly}\!\left(s^{d^2\log n},
\binom N{\le d}^{\log s},n\right)\mathcal T(\mathbb F,N).
\]
The factor \(\mathcal T\) is explicit in Remark 5.2. Theorem 2.13 supplies
\(\mathcal T(\mathbb F_{p^m},N)=\operatorname{poly}(N,m,p)\);
the following paragraph warns that numerical \(p\) can make the algorithm
super-polynomial in input bit length. The finite-field specialization in
Remark 5.2 additionally says \(p>d\), while Theorem 1.7 itself says arbitrary
fields. Neither reading repairs the numerical \(N,p\) dependence. Taking
\(d=D_{\rm out}\) still leaves this dependence and a candidate-list task.

## Giesbrecht–Roche

[arXiv:0901.1848v2](https://arxiv.org/pdf/0901.1848v2), dated
2010-12-03; published in JSC 46(11), November 2011, pp.1242–1259
([DOI](https://doi.org/10.1016/j.jsc.2011.08.006)).
An independent internal agent checked the exact primary statements.

Algorithm IsPerfectPowerGF / Theorem 2.12, PDF p.11, requires
\(N=\deg f<\operatorname{char}\mathbb F_q\).
It is Monte Carlo detection, returning a prime exponent \(r\) without its root;
the theorem's bound is
\(\widetilde O(t^3(\log q+\log N))\) field operations.
The stronger introductory summary should not replace this theorem.

Newton extraction in §3.2, pp.16–18, also requires characteristic zero or
greater than \(N\). Theorem 3.2 proves correctness. Theorem 3.5's complexity
depends on Conjecture 3.3 and includes numerical \(r\):
\(O((t+r)^4\log r\log N)\) field operations, plus
\(O((t+r)^4\log r\log^2N)\) bit operations, excluding scalar-root finding.
The unconditional output-sensitive Theorem 3.1 (p.15) is over
\(\mathbb Z/\mathbb Q\), not finite fields.
The specified-prime algorithm / Corollary 2.4 reverse a characteristic
inequality typographically; the main theorem/global assumptions consistently
require characteristic greater than \(N\).

## Checkable scope witness

For odd \(p\), put \(P=p^k\) and work over \(\mathbb F_{p^m}\). Frobenius gives
\[
f=(x-1)^P(x+1)^{P+1}
 =(x^P-1)(x^P+1)(x+1)
 =x^{2P+1}+x^{2P}-x-1.
\]
Thus \(t=4\), \(D_{\rm out}=2\), and \(N=2P+1\). The multiplicities \(P,P+1\)
are coprime, so \(f\) is no nontrivial exact power, despite arbitrarily large
binary multiplicities. It also has \(p<N\). This is a direct algebraic witness
that exact-power detection/extraction and a characteristic-\(>N\) theorem
do not by themselves supply the target's arbitrary-multiplicity scope.

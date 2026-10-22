# Approach 3: sharpen the monomial height annihilator

Let \(E(u)\in W(k)[u]\) be an Eisenstein polynomial of degree \(e\). In the Caruso–Liu construction, the integer \(N\) must satisfy

\[
u^N=0\quad\text{in }A_{n,r}:=W_n(k)[u]/(E(u)^r).
\tag{1}
\]

Their general choice is \(N=ern\). Their §2.4 already gives better choices. This approach derives a useful exact case and investigates whether setting \(N=er\) could remove the extra \(n\) in the weight parameter for all inputs.

## Divisible weights give the desired bound

**Lemma.** If \(p^{n-1}\mid r\), then \(u^{er}=0\) in \(A_{n,r}\).

**Proof.** Write \(E(u)=u^e+pH(u)\). Expanding,

\[
u^{er}=(E(u)-pH(u))^r
=E(u)^r+\sum_{j=1}^{r}(-1)^j
\binom rj p^j H(u)^j E(u)^{r-j}.
\]

For \(1\leq j\leq r\), the identity
\(j\binom rj=r\binom{r-1}{j-1}\) implies

\[
v_p\binom rj\geq v_p(r)-v_p(j).
\]

Since \(j-v_p(j)\geq1\), every summand after the first has coefficient valuation at least \(v_p(r)+1\geq n\). The first vanishes modulo \(E(u)^r\). This proves the lemma. ∎

Take \(N=er\). If \(b<1\), \(s=n+a\) strictly satisfies the Caruso–Liu level condition

\[
s>n+\log_p\frac{N}{e(p-1)}.
\]

The relative-field conclusion and transitivity detailed in Approach 2 yield

\[
v_K(\mathcal D_{L/K})<1+e(n+a+b)-p^{-s}=B.
\]

If \(b=1\), Approach 1 supplies this conclusion without invoking the strict level condition at equality. Consequently the target holds for **all** \(p^{n-1}\mid r\), for arbitrary \(e\), rank, and perfect residue field. In particular, every \(n=1\) case was already covered by Caruso–Liu's original theorem.

This is a consequence of their established method; it is consistent with, and subsumed by, their Lemma 2.4.1. The elementary proof is included to expose exactly what happens to the coefficient \(n\), not to claim a new result.

More generally, let \(R=p^{n-1}\lceil r/p^{n-1}\rceil\). The same calculation gives \(u^{eR}\equiv E(u)^R\pmod{p^n}\), and \(E(u)^r\mid E(u)^R\). Hence \(N=eR\) is always valid. This recovers that cited annihilator estimate directly.

## Exact scalar obstruction

Even the simplest Eisenstein polynomial shows that the substitution \(N=er\) is false in general. Suppose \(E(u)=u^e-p\), and introduce \(z=u^e-p\). The ring in (1) is isomorphic to

\[
\left((\mathbb Z/p^n\mathbb Z)[z]/(z^r)\right)[u]/(u^e-z-p)
\]

when \(k=\mathbb F_p\); the same coefficient argument works over \(W_n(k)\). It is free over \((\mathbb Z/p^n\mathbb Z)[z]/(z^r)\) on \(1,u,\ldots,u^{e-1}\). Thus

\[
u^{em+t}=u^t(z+p)^m,\qquad0\leq t<e,
\]

vanishes if and only if every coefficient

\[
\binom mj p^{m-j},\qquad0\leq j\leq\min(m,r-1),
\]

is divisible by \(p^n\). Define

\[
M(p,n,r)=\min\left\{m\geq r:
m-j+v_p\binom mj\geq n\text{ for all }0\leq j<r\right\}.
\tag{2}
\]

The exact minimal nilpotence exponent of \(u\) is \(eM(p,n,r)\). Indeed no \(m<r\) can work because the coefficient of \(z^m\) is one. For \(m\geq r\), the displayed coefficient criterion is necessary and sufficient, and the free \(u^t\)-basis proves that no intermediate exponent works.

We have \(r\leq M\leq r+n-1\), since for \(m=r+n-1\) each \(m-j\geq n\). At \(m=r\), put \(k=r-j\). Then

\[
\min_{1\leq k\leq r}\left(k+v_p\binom rk\right)=1+v_p(r).
\tag{3}
\]

The same binomial estimate proves the lower bound, and \(k=1\) attains it. Consequently

\[
\boxed{M(p,n,r)=r\ \Longleftrightarrow\ n\leq1+v_p(r).}
\tag{4}
\]

Thus the divisible-weight condition is exactly sharp for this proposed scalar annihilator, even in an unramified base field with \(e=1\). Failure of (4) is **not** a counterexample to the ramification inequality. It only invalidates this attempted simplification of its proof.

For example, at \((p,n,r)=(3,2,7)\), formula (2) gives \(M=8\), not 7. The coefficient of \(z^6\) in \((z+3)^7\) is 21, which is not zero modulo 9. The generalized Caruso–Liu bound with \(N=8\) and \(e=1\) is

\[
1+(2+2+4/9)-1/81=440/81,
\]

which still exceeds the target \(871/162\) by \(1/18\). Thus actual optimization of the old scalar parameter helps but does not resolve this test case.

## Monotonicity prevents concealing the loss

For real \(x>1/p\), write \(x=p^a b\) with \(1/p<b\leq1\), and set

\[
H(x)=1+e(n+a+b)-p^{-(n+a)}.
\]

Within each interval \(p^{a-1}<x\leq p^a\), \(H\) is strictly increasing. At the right endpoint, its right-hand jump is

\[
e/p+(p-1)p^{-(n+a+1)}>0.
\]

Therefore replacing \(r\) by a strictly larger effective height \(N/e\) produces a strictly larger numerical bound; it does not prove the target by a change of notation.

**Outcome:** the exact divisible-weight case, an explicit optimized scalar algorithm, and a rigorous obstruction to the naive \(N=er\) substitution. The arbitrary-weight problem remains unresolved.

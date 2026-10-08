# Precise question and conventions

Let \(p>2\) be prime, let \(k\) be a perfect field of characteristic \(p\), let \(K_0=W(k)[1/p]\), and let \(K/K_0\) be finite and totally ramified of degree \(e\). Fix an algebraic closure \(\overline K\). The residue field is not required to be finite. We normalize \(v_K\) on \(\overline K\) by \(v_K(K^\times)=\mathbb Z\), hence \(v_K(p)=e\).

Let \(V\) be a finite-dimensional semistable \(\mathbb Q_p\)-representation of \(G_K\), let \(\Lambda\subset V\) be a \(G_K\)-stable \(\mathbb Z_p\)-lattice, and let \(T_n=\Lambda/p^n\Lambda\), with \(n\geq1\). Let \(L\) be the finite Galois extension fixed by the kernel of \(G_K\to\operatorname{Aut}(T_n)\). Crystalline representations are a subclass of semistable representations. Every chosen lattice, not just the rational representation or the semisimplified residual representation, is part of the problem.

The source uses nonnegative Hodge–Tate weights \(0,\ldots,r\), where \(r\geq1\) is integral. In the contribution's convention a cyclotomic Tate twist has weight \(+1\). Other authors use the opposite sign. Taking the contragredient changes the sign and preserves the kernel of the action on the dual finite free \(\mathbb Z/p^n\mathbb Z\)-module. Thus statements formulated for \([-r,0]\) can be compared after dualization, but a Tate twist must not silently be used as if it preserved the kernel.

There is a unique integer \(a\geq0\) such that

\[
(p-1)p^{a-1}<r\leq(p-1)p^a.
\]

Define \(b=r/((p-1)p^a)\) and \(s=n+a\). The natural numbers in the source must include zero: for \(1\leq r\leq p-1\), \(a=0\). Equivalently \(a=\lceil\log_p(r/(p-1))\rceil\); the inequalities, not floating-point logarithms, define it here. A proposed input \(r=0\) does not admit the displayed normalization and must be treated separately. This packet states no formula using an undefined \(a,b\) at \(r=0\).

The different \(\mathcal D_{L/K}\) is an ideal of \(\mathcal O_L\). If it equals \(\mathfrak m_L^d\), then

\[
v_K(\mathcal D_{L/K})=d/e(L/K).
\]

It is not the integer exponent \(d\), and it is not the valuation of the discriminant ideal in \(K\). If \(L/K\) has residue degree \(f\), the discriminant exponent is \(fd=[L:K]v_K(\mathcal D_{L/K})\). Confusing these quantities destroys rank-independent comparisons.

We use Fontaine's shifted upper numbering \(G_K^{(\mu)}\), as do Caruso–Liu, Caruso and Hattori in the cited ramification statements. Its relation to the standard Serre convention is \(G_K^{(\mu)}=G_K^{\mu-1}\) for the relevant positive parameters. The largest shifted break is denoted \(\mu_{L/K}\). For a ramified finite Galois extension,

\[
v_K(\mathcal D_{L/K})<\mu_{L/K}.
\]

For an unramified extension the different valuation is zero. A theorem asserting triviality for all \(\mu>U\) proves \(\mu_{L/K}\leq U\), not triviality at the endpoint. The strict different inequality above is enough for our deductions; no endpoint triviality is presumed.

The source's Conjecture 3 asks

\[
v_K(\mathcal D_{L/K})\leq B(p,e,n,r),\qquad
B(p,e,n,r)=1+e(n+a+b)-p^{-(n+a)}.
\]

The published Caruso–Liu Conjecture 1.2(2) asks the strict version. In that paper the torsion module may more generally be a quotient of two stable lattices in the same semistable representation. Such a quotient killed by \(p^n\) is a quotient of \(\Lambda/p^n\Lambda\), so its splitting field is a subfield and every bound proved for the latter descends to it. No claim is made that every torsion étale cohomology module is a quotient of semistable lattices with the required weight bound.

The report's final crystalline-improvement question is separate from Conjecture 3. The supplied record's literature paragraph conflates them. We preserve both scopes: the mathematical approaches address the full semistable source question and thus also supply valid partial results for its crystalline restriction.

# Independent recheck of the EP730 fixed-depth Fourier argument

## Verdict and scope

**ACCEPT for the stated fixed-depth lemma and its first-power application.** The discrepancy constant

\[
C_r=(2r+3)3^{2r}
\]

is valid for every fixed positive integer \(r\), odd prime \(p\), integral phase \(F(t)=p\alpha t^2+\beta t+\gamma\) with \(p\nmid\alpha\beta\), and the ordinary digit boxes specified below. In particular, the discrepancy is \(o_r(p^r)\) as \(p\to\infty\). The application in the original proof uses only \(a=1\), fixes \(r\) before taking its limit, and controls growing depths by a separate elementary bound. No hidden uniformity in \(r\) is needed.

This is a focused independent mathematical review of Sections 6–7, with the relevant polynomial and exact-valuation facts in Section 3 checked for their use here. It is not a second audit of every part of the positive-density theorem. No Lean, Lake, author scripts, imported code, or other third-party executable was run. A valid conventional proof is not a claim that a formal kernel has been replayed.

The original source, not merely the first auditor's reconstruction, was inspected: Will Blair, *A positive-density solution of Erdős #730*, Sections 3, 6 and 7, at [commit f297d710018270c66b296082766334974260bcbc](https://github.com/williamjblair/lean-proofs/blob/f297d710018270c66b296082766334974260bcbc/ErdosProblems/Erdos730/compute/full_density/proof.md). Its retained bytes have SHA-256 `23f69d9b69fe7099d9451c9ef38b47609c99211201ab76433735b89af8adb9d0` and length 17,246. The independent derivation below supplies the details compressed into the original proof's geometric-sum, layer-cake, and digit-induction steps.

## 1. Definitions, endpoints, and normalization

Write \(e_Q(x)=\exp(2\pi i x/Q)\), \(d=2r\), \(q=p^d\), \(N=p^r\), and \(H=(p+1)/2\). Let

\[
\mathcal A=\left\{\sum_{j=0}^{d-1}a_jp^j:a_j\in E_j\right\}\subseteq\{0,\ldots,q-1\},
\]

where each \(E_j\) is a consecutive integer interval contained in \(\{0,\ldots,p-1\}\). One has cardinality \(H-1\); the others have cardinality \(H\). Thus \(|\mathcal A|=(H-1)H^{d-1}\). An interval of \(N\) inputs means exactly \(M,M+1,\ldots,M+N-1\), with integer \(M\), including negative starts. Digits are the unique representatives of the output residue in \(\{0,\ldots,q-1\}\).

These are ordinary, non-wrapping digit intervals. The proof does not silently replace an interval that wraps from digit \(p-1\) to digit \(0\) by a single ordinary interval on a shifted Fourier grid. No wrapping interval is needed in the application. For the P,Q branches the exact-valuation deletion leaves units digits \(1,\ldots,H-1\); for R,S it leaves \(0,\ldots,H-2\). Higher digits are \(0,\ldots,H-1\). These endpoints give exactly the advertised cardinalities even at \(p=3\).

Use the unnormalized transform

\[
\widehat f(h)=\sum_{y=0}^{q-1}f(y)e_q(-hy),\qquad
f(y)=\frac1q\sum_{h=0}^{q-1}\widehat f(h)e_q(hy).
\]

Consequently the count is

\[
\frac1q\sum_{h=0}^{q-1}\widehat{1_{\mathcal A}}(h)
\sum_{t=0}^{N-1}e_q(hF(M+t)).
\]

The frequency \(h=0\) contributes \(N|\mathcal A|/q=|\mathcal A|/p^r\), as claimed. Translation replaces \(\beta\) by \(\beta+2p\alpha M\), and \(\gamma\) by an integer. It preserves the unit conditions and \(\alpha\), so henceforth take \(M=0\).

## 2. A shifted-grid estimate with the stated constants

For a consecutive integer interval of length \(L\ge1\), its exponential sum at real frequency \(x\) has absolute value at most

\[
B_L(x)=\min\left(L,\frac1{2\|x\|}\right),
\]

where the second quantity is interpreted as infinity at integers. This follows from the finite geometric sum and \(|\sin \pi x|\ge2\|x\|\). A change of the interval's starting point contributes only a complex factor of absolute value one.

Consider the \(K\) points \(\theta+j/K\pmod1\), \(0\le j<K\), with arbitrary real \(\theta\). For every \(u\ge1\), at most \(K/u+2\) of them have distance less than \(1/(2u)\) from an integer. Indeed, the relevant circular arc has length \(1/u\); splitting at zero if necessary gives at most two intervals, each containing at most its length times \(K\), plus one, grid points. Strict versus weak endpoints affect at most endpoint points and are covered by the two additive units. This also covers the whole-circle case at \(u=1\).

Because \(B_L\ge1\), layer cake on this finite set gives

\[
\begin{aligned}
\sum_{j=0}^{K-1}B_L(\theta+j/K)
&=K+\int_1^L\#\{j:B_L(\theta+j/K)>u\}\,du\\
&\le K(1+\log L)+2(L-1).
\end{aligned}
\]

In particular, when \(1\le L\le K\), the mass is at most \(K(3+\log L)\). No constant depends on the shift, on proximity to an integer, or on interval endpoints. This one estimate will be used twice, with \((K,L)=(Q/p,N)\) and \((p,|E_j|)\).

## 3. Effective frequencies and the complete quadratic sum

Every nonzero frequency has the unique form \(h=p^{2r-m}u\), where \(1\le m\le2r\) and \(u\) is a unit modulo \(p^m\). Its phase sum is

\[
S_m(u)=\sum_{t=0}^{N-1}e_{p^m}(uF(t)).
\]

The identity

\[
F(x)-F(y)=(x-y)\bigl(p\alpha(x+y)+\beta\bigr)
\]

has a unit second factor. Thus it induces an injection, hence a permutation, modulo every \(p^m\). If \(m\le r\), the \(N\) consecutive inputs are an integral number of complete residue systems modulo \(p^m\); each complete system has sum \(\sum_z e_{p^m}(uz)=0\). Therefore \(S_m(u)=0\) exactly.

Suppose now \(r<m\le2r\) and put \(Q=p^m\). For each \(s\bmod Q\), define

\[
C(s)=\sum_{z=0}^{Q-1}e_Q\bigl(up\alpha z^2+(u\beta+s)z+u\gamma\bigr).
\]

Translate \(z\) by \(p^{m-1}\). The quadratic changes by a multiple of \(Q\), while the linear part multiplies the sum by \(e_p(u\beta+s)\). Hence \(C(s)=0\) unless \(s\equiv-u\beta\pmod p\). This residue class is nonzero modulo \(p\), although the subsequent grid bound would also be valid for the zero class.

On the surviving class write \(u\beta+s=pb\). Reducing the variable modulo \(P=p^{m-1}\) gives

\[
C(s)=p\,e_Q(u\gamma)\sum_{z\bmod P}e_P(u\alpha z^2+bz).
\]

For completeness, the exact magnitude of this last Gauss sum requires no appeal to a bound with an unspecified constant. If \(A\) is a unit modulo the odd number \(P=p^{m-1}\), then

\[
\begin{aligned}
\left|\sum_{z\bmod P}e_P(Az^2+bz)\right|^2
&=\sum_{v\bmod P}e_P(Av^2+bv)
  \sum_{y\bmod P}e_P(2Avy)\\
&=P.
\end{aligned}
\]

The inner sum is zero unless \(P\mid2Av\), and since \(2A\) is a unit that means \(v=0\bmod P\). Therefore

\[
|C(s)|=p\sqrt{p^{m-1}}=p^{(m+1)/2}
\]

on precisely the surviving class. This proves both the vanishing and the magnitude, including odd and even exponents \(m-1\). Oddness of \(p\) and \(p\nmid\alpha\) are used exactly here.

## 4. Completion and the incomplete-sum estimate

Set \(D_N(s)=\sum_{v=0}^{N-1}e_Q(-sv)\). Orthogonality gives the exact normalization and signs:

\[
S_m(u)=\frac1Q\sum_{s\bmod Q}C(s)D_N(s).
\]

Indeed, on expanding the right side the inner \(s\)-sum is \(Q\) when \(z=v\bmod Q\) and zero otherwise. Since \(N<Q\), each input is counted once.

There are \(K=Q/p\) surviving values \(s=s_0+pj\), and their real frequencies are \(s/Q=s_0/Q+j/K\). Since \(m\ge r+1\), one has \(N=p^r\le K\). The grid estimate in Section 2 therefore yields

\[
\sum_{s\equiv-u\beta\ (p)}|D_N(s)|
\le\frac Qp(3+\log N).
\]

Combining this with the exact complete-sum magnitude and the completion factor gives

\[
|S_m(u)|\le\frac1Q p^{(m+1)/2}\frac Qp(3+\log N)
=p^{(m-1)/2}(3+r\log p).
\]

As \(m\le2r\), this is at most

\[
p^{r-1/2}(3+r\log p)
\le(2r+3)p^{r-1/2}(1+\log p).
\]

The last constant is deliberately generous: subtracting its left coefficient from its right coefficient leaves \(2r+(r+3)\log p\ge0\). No extra factor \(p\), \(Q\), number of frequency classes, or interval length has been omitted.

## 5. Digitwise Fourier mass

For a digit interval \(E\), write \(D_E(x)=\sum_{a\in E}e^{2\pi i ax}\). With \(1\le|E|\le p\), the shifted-grid estimate gives, uniformly in real \(\theta\),

\[
\sum_{b=0}^{p-1}|D_E(\theta+b/p)|\le p(3+\log p).
\]

The digit transform factors exactly as

\[
\widehat{1_{\mathcal A}}(h)
=\prod_{j=0}^{d-1}D_{E_j}(-h/p^{d-j}).
\]

Here is the explicit induction behind its L¹ bound. Decompose \(h=a+bp^{d-1}\), with \(0\le a<p^{d-1}\) and \(0\le b<p\). In the \(j=0\) factor this gives the shifted grid \(-a/p^d-b/p\). For every \(j\ge1\), the extra term in its argument is the integer \(-bp^{j-1}\), so those factors are unchanged. Summing over \(b\) costs at most \(p(3+\log p)\); the remaining sum over \(a\) is exactly the corresponding Fourier-mass expression for the \((d-1)\)-digit box \(E_1,\ldots,E_{d-1}\) modulo \(p^{d-1}\). The zero-digit expression is one. Induction proves

\[
\sum_{h\bmod q}|\widehat{1_{\mathcal A}}(h)|
\le[p(3+\log p)]^d
\le q\,3^d(1+\log p)^d.
\]

This argument actually works for arbitrary ordinary nonempty digit intervals of length at most \(p\); the specified half lengths determine the main term, not the validity of the mass bound.

## 6. The resulting discrepancy and its quantifiers

Remove the zero frequency in the count and use exact vanishing for \(m\le r\). Bounding the remaining terms by the largest estimate in Section 4 and then by the full nonnegative Fourier mass gives

\[
\begin{aligned}
\left|\#\{0\le t<N:F(M+t)\bmod q\in\mathcal A\}
-\frac{|\mathcal A|}{p^r}\right|
&\le\frac1q\sum_{h\ne0}|\widehat{1_{\mathcal A}}(h)|\,
 (2r+3)p^{r-1/2}(1+\log p)\\
&\le (2r+3)3^{2r}p^{r-1/2}(1+\log p)^{2r+1}.
\end{aligned}
\]

Dividing by \(p^r\) gives \(C_rp^{-1/2}(1+\log p)^{2r+1}\to0\) for every fixed \(r\). The estimate is uniform in the integral start, the unit coefficients, the constant coefficient, the choice and position of the shorter digit interval, and the permitted digit-interval endpoints. It is not claimed to be \(o(p^r)\) when \(r\) grows arbitrarily with \(p\). The latter conclusion would not follow from this estimate and is not used.

## 7. Verification of the first-power application

For each \(p\le\sqrt X\), there is exactly one integer \(r\ge1\) with

\[
p^{r+1}\le X<p^{r+2},\qquad
V=X^{1/(r+2)}<p\le U=X^{1/(r+1)}.
\]

At an exact prime-power endpoint the prime belongs to the band with the weak upper endpoint. For example \(X=p^k\) gives \(r=k-1\). Hence these bands cover the indicated prime range without overlap or omission.

The source's root progression for \(a=1\) has phase

\[
G(k)=3024T^2p\,k^2+(pu_L+b_L)k+v_L,
\quad T=3\cdot41\cdot43,
\]

with \(b_L\in\{-246T,246T,258T,-258T\}\). The prime divisors of \(3024T^2\) are among \(2,3,7,41,43\); those of the \(b_L\) are among \(2,3,41,43\). For fixed \(r\), the lower endpoint \(V\) tends to infinity, so eventually every prime in the band exceeds 43 and both required unit conditions hold. The coefficient and the starting point may vary with the prime and the progression; the proved uniformity permits this. In particular, no Gauss estimate with a nonunit quadratic coefficient is applied to \(p=7\).

The exact-valuation digit box has density

\[
\delta_{p,r}=\frac{(H-1)H^{2r-1}}{p^{2r}}
=4^{-r}(1-p^{-1})(1+p^{-1})^{2r-1}.
\]

Let \(K\) be the actual length of the root progression and \(W=X/p\), so \(K\le W+1\) and \(N=p^r\le W\). Write \(K=fN+s\), \(0\le s<N\). Each full block has upper bound \(N\delta_{p,r}+D\), with the lemma's discrepancy \(D\), and the last block contributes at most \(s\). Thus

\[
\begin{aligned}
E_{L,p,1}(X)
&\le K\delta_{p,r}+fD+s(1-\delta_{p,r})\\
&\le(W+1)\delta_{p,r}
  +2C_rX p^{-3/2}(1+\log p)^{2r+1}+p^r.
\end{aligned}
\]

Here \(f\le(W+1)/N\le2W/N\); a terminal block is bounded trivially, not treated as a full block with a false length normalization.

For fixed \(r\), the discrepancy divided by \(X\), summed over its band, is at most

\[
2C_r\sum_{n>V}n^{-3/2}(1+\log n)^{2r+1}=o_r(1),
\]

since this is the tail of a convergent positive series. The terminal blocks sum to at most

\[
U^r\pi(U)\le\frac{2(r+1)X}{\log X}=o_r(X)
\]

for sufficiently large \(X\), using the source's stated prime-counting input. Extra main-term units are at most \(\pi(U)=o(X)\). Finally

\[
\delta_{p,r}=4^{-r}(1+O_r(p^{-1})),
\]

and summing the correction after division by \(p\) costs \(O_r(\sum_{n>V}n^{-2})=o_r(1)\). The stated reciprocal-prime Mertens estimate therefore yields

\[
\limsup_{X\to\infty}\frac{E_{L,r}(X)}X
\le4^{-r}\log\frac{r+2}{r+1}.
\]

Every occurrence of a depth-dependent constant in this calculation is inside a fixed-depth limit.

## 8. The independent uniform depth tail

The summation over depths uses a different argument, with no Gauss sum. The source's polynomial difference identity remains a unit-times-difference identity for every allowed branch prime, including 7. Thus it permutes residues modulo \(p^r\) even when \(p\mid3024T^2\). In a padded block of \(N=p^r\) inputs, at most \(H^r\) outputs have all the first \(r\) digits permitted. Exact valuation may be ignored for this upper bound.

With the same \(K,W,N\) as above, padding uses at most \(K/N+1\) blocks. Hence, with \(\rho_p=H/p\),

\[
E_{L,p,1}(X)\le(K+N)\rho_p^r
\le(W+1+N)\rho_p^r\le3(X/p)\rho_p^r.
\]

For the relevant odd primes, \(\rho_p\le2/3=:\vartheta\). Let

\[
J=\left\lfloor\frac{\log X}{2\log3}\right\rfloor-2.
\]

When \(1\le r\le J\), the lower band endpoint is at least 9, since \(r+2\le\log X/(2\log3)\). The Mertens estimate at both endpoints is therefore applicable and gives

\[
\sum_{V<p\le U}\frac1p
\le\log\frac{r+2}{r+1}+\frac{8(r+2)}{\log X}.
\]

For any fixed cutoff \(R\), summing the resulting bound over \(R<r\le J\) gives at most

\[
\sum_{r>R}\vartheta^r\log\frac{r+2}{r+1}
+\frac8{\log X}\sum_{r>R}(r+2)\vartheta^r.
\]

The second term tends to zero with \(X\); the first tends to zero with \(R\). For \(r>J\), disjointness of the prime bands gives

\[
\sum_{r>J}\sum_{p\text{ in band }r}\frac{\rho_p^r}{p}
\le\vartheta^{J+1}\sum_{p\le\sqrt X}\frac1p=o(1).
\]

Indeed, \(\vartheta^{J+1}=O(X^{-c})\) for \(c=-\log\vartheta/(2\log3)>0\), whereas the reciprocal-prime sum is \(O(\log\log X)\). Therefore

\[
\lim_{R\to\infty}\limsup_{X\to\infty}
\sum_{r>R}\sum_{p\text{ in band }r}\frac{\rho_p^r}{p}=0.
\]

All fixed primes move beyond any fixed depth cutoff as \(X\to\infty\). More specifically, 5 and 7 eventually lie beyond \(J\), because \(\log p<2\log3\) for \(p<9\). They are consequently handled by the permutation tail, not by the fixed-depth Gauss calculation. Other fixed small primes are covered by the same cutoff/tail argument even if they are not beyond \(J\).

For finite \(R\), summing the fixed-depth limsups is valid. The displayed uniform tail then permits \(R\to\infty\), giving the single-branch bound \(\sum_{r\ge1}4^{-r}\log((r+2)/(r+1))\), and multiplying by four gives the source's bound for the four branches. There is no interchange of an uncontrolled infinite family of Fourier error terms.

## 9. Boundaries of this acceptance

- The exact stated numerical discrepancy constant is accepted; no enlargement is required.
- The accepted asymptotic is fixed \(r\), \(p\to\infty\), uniform in the other parameters listed above.
- The application audited here is \(a=1\). A general \(a\ge2\) completion problem would require a different argument; it is not smuggled into this lemma.
- Ordinary digit intervals are enough, and the exact-valuation deletions really are endpoint deletions. A claim for cyclically wrapping digit intervals would need separate treatment and is not part of the accepted statement.
- The tail is proved separately from the Fourier lemma and is uniform in depth. It covers the exceptional small prime that divides the quadratic coefficient.
- The asymptotic conclusion follows from the mathematical proof, not from finite experiments. No numerical experiment has been used as evidence for an infinite limit.
- This review did not reproduce formal verification, independently establish every other section of the density proof, or make a novelty or priority claim.

**Final disposition:** no consequential gap found in this focused Fourier step or in the order of limits used to apply it.

## Review notice for this edition

This focused review is unrefereed internal AI mathematical review. Its acceptance is limited to the stated Fourier lemma, its first-power application and the separate uniform depth tail. It is not external human peer review, journal acceptance, formal kernel certification or a new-solution claim. No third-party source program, raw finite certificate, dataset or private coordination material is included in this edition.

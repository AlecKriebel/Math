# Independent verification by a Baire-category argument

Checkpoint: 2026-09-23T04:05:04Z. Independent verification of the abstract amplification theorem: **100% complete**. This checkpoint does not certify the original problem's standing assumptions or bibliographic priority; those are separate audits.

## Claim and verdict

Let \(1\le p<\infty\), let \(c=(c_j)_{j\in\mathbb Z}\) be positive weights, and suppose the forward translation

\[
(Sa)_j=a_{j+1}
\]

is bounded on \(Y=\ell^p(\mathbb Z,c)\). For every nonzero **separable** complex Banach space \(E\) and every set \(\Gamma\subseteq\mathbb C\), scalar \(S\) is \(\Gamma\)-supercyclic if and only if its coordinatewise amplification \(S_E\) on \(Y_E=\ell^p(\mathbb Z,c;E)\) is \(\Gamma\)-supercyclic.

**Verdict: proved.** A bounded inverse is unnecessary. The proof below replaces the candidate's infinite gluing construction by a two-open-set argument and Baire's theorem. It also simplifies the necessity argument by using one nonzero coordinate of a scalar universal vector.

Here \(\Gamma\)-supercyclic means that some vector has dense set \(\{\lambda S^n x:\lambda\in\Gamma,n\ge0\}\). All estimates concern the actual chosen scalars in \(\Gamma\); no quotient, closure, multiplication, or regularity property of \(\Gamma\) is used.

## 1. Exact finite-block criterion

Write \(\Gamma^*=\Gamma\setminus\{0\}\). Consider the condition

\[
\tag{C}
\forall\ F\subset\mathbb Z\text{ finite nonempty},\ \eta>0,\ L\ge0,
\quad\exists\ n>L,\ \lambda\in\Gamma^*:
\quad
\frac{(\sum_{j\in F}c_{j+n})^{1/p}}{|\lambda|}<\eta,
\qquad
|\lambda|(\sum_{j\in F}c_{j-n})^{1/p}<\eta.
\]

We prove scalar universality implies (C), and (C) implies vector-valued universality. This also proves the claimed exact criterion.

### Scalar universality implies (C)

Let \(x\in Y\) be \(\Gamma\)-supercyclic. Its support is unbounded above: otherwise every \(S^n x\) would vanish on all coordinates above one fixed index, so the entire \(\Gamma\)-orbit would lie in a proper closed coordinate subspace.

Fix finite nonempty \(F\subset\mathbb Z\). Choose \(k\ge\max F\) with \(x_k\ne0\). Set

\[
v=\sum_{j\in F}e_j.
\]

For every nonempty open set \(U\subset Y\) and every \(N\), some point \(\lambda S^n x\) with \(n>N\) lies in \(U\). Indeed, the finite union \(\bigcup_{n=0}^N\mathbb C S^n x\) is closed with empty interior in the infinite-dimensional Banach space \(Y\). A nonempty open subset of \(U\) avoids that finite union, and density supplies an orbit point there.

It follows that we can find \(n_r\to\infty\) and \(\lambda_r\in\Gamma^*\) such that

\[
\delta_r:=\|\lambda_r S^{n_r}x-v\|_c\longrightarrow0.
\]

After discarding finitely many terms, \(\delta_r<\frac12\min_{j\in F}c_j^{1/p}\). Therefore

\[
|\lambda_r x_{j+n_r}|>\tfrac12\qquad(j\in F),
\]

and hence

\[
\frac{(\sum_{j\in F}c_{j+n_r})^{1/p}}{|\lambda_r|}
\le 2\left(\sum_{j\in F}c_{j+n_r}|x_{j+n_r}|^p\right)^{1/p}
\longrightarrow0.
\]

The last limit follows directly from \(x\in\ell^p(\mathbb Z,c)\), since the finite translated sets \(F+n_r\) eventually escape every fixed bounded interval. Pairwise disjointness of those sets is not required.

For large \(r\), \(k-n_r\notin F\); the error at this one coordinate gives

\[
|\lambda_r|c_{k-n_r}^{1/p}|x_k|\le\delta_r.
\]

Set \(M=\|S\|>0\). Boundedness implies, for \(d\ge0\),

\[
c_{t-d}^{1/p}=\|S^d e_t\|_c\le M^d c_t^{1/p}.
\]

Apply this with \(t=k-n_r\) and \(d=k-j\ge0\). Then

\[
|\lambda_r|\left(\sum_{j\in F}c_{j-n_r}\right)^{1/p}
\le
\left(\sum_{j\in F}M^{p(k-j)}\right)^{1/p}
\frac{\delta_r}{|x_k|}
\longrightarrow0.
\]

Both limits hold along the same sequence with the same \(\lambda_r\in\Gamma^*\). They prove (C), with arbitrarily large \(n\).

### (C) implies the two-open-set property on \(Y_E\)

For a finitely supported \(b\in Y_E\), define its formal right translation \(R_n b\) by

\[
(R_n b)_j=b_{j-n}.
\]

It is finitely supported, belongs to \(Y_E\), and satisfies \(S_E^nR_n b=b\). We do not assume \(R_n\) extends to a bounded map on all of \(Y_E\).

Let \(U,V\subset Y_E\) be nonempty open sets. Finite-support sequences are dense, so choose finite-support \(a\in U,b\in V\), and \(\rho,\sigma>0\) such that the corresponding balls lie in \(U,V\). Choose finite nonempty \(F\) containing both supports and

\[
A=\max\{1,\|a_j\|_E,\|b_j\|_E:j\in F\}.
\]

Use (C) with \(\eta<\min(\rho,\sigma)/A\), obtaining \(n,\lambda\). Define

\[
z=a+\lambda^{-1}R_n b.
\]

The first tail inequality gives

\[
\|z-a\|_c\le\frac{A}{|\lambda|}\left(\sum_{j\in F}c_{j+n}\right)^{1/p}<\rho,
\]

so \(z\in U\). The second gives

\[
\|\lambda S_E^n z-b\|_c
=|\lambda|\|S_E^n a\|_c
\le A|\lambda|\left(\sum_{j\in F}c_{j-n}\right)^{1/p}<\sigma,
\]

so \(\lambda S_E^n z\in V\). Thus for every pair \(U,V\) there is a map in the family \(\{\lambda S_E^n\}\) carrying a point of \(U\) into \(V\).

### Baire produces one universal vector

Since \(E\) is separable and \(p<\infty\), \(Y_E\) has a countable base \((V_q)_{q\ge1}\). For each \(q\), let

\[
G_q=\bigcup_{n\ge0}\ \bigcup_{\lambda\in\Gamma}
\{z\in Y_E:\lambda S_E^nz\in V_q\}.
\]

Each \(G_q\) is open, since each map \(\lambda S_E^n\) is continuous. Each is dense by the two-open-set property. Baire's theorem implies \(\bigcap_qG_q\) is a dense \(G_\delta\). Every point in this intersection has a dense \(\Gamma\)-orbit. The possibly uncountable union over \(\Gamma\) is harmless: an arbitrary union of open sets is open.

This proves (C) implies \(\Gamma\)-supercyclicity of \(S_E\).

## 2. The reverse implication

Choose \(e\in E\setminus\{0\}\) and \(\ell\in E^*\) with \(\ell(e)=1\). The coordinatewise map

\[
Q:Y_E\to Y,\qquad (Qz)_j=\ell(z_j)
\]

is continuous, onto (take \(z_j=a_je\)), and obeys \(QS_E=SQ\). If \(z\) has dense \(\Gamma\)-orbit, then its image under \(Q\) is dense: for nonempty open \(U\subset Y\), the inverse image \(Q^{-1}(U)\) is nonempty open and therefore meets the dense orbit. Thus \(Qz\) is scalar \(\Gamma\)-supercyclic.

The forward implication and this quotient argument establish the theorem.

## 3. Assumption audit and boundary cases

- **Separability is essential.** A \(\Gamma\)-orbit lies in \(\bigcup_{n\ge0}\mathbb C S_E^n z\), a separable set (each complex line is separable). Its closure is separable. Therefore a nonseparable \(Y_E\) cannot admit a \(\Gamma\)-supercyclic vector. The coordinate embedding of \(E\) into \(Y_E\) shows \(Y_E\) is nonseparable whenever \(E\) is. For example, \(c_j=2^{-|j|}\) and \(\Gamma=\{1\}\) satisfy (C) for scalar \(Y\), but their amplification to nonseparable \(E\) cannot be hypercyclic.
- **A bounded inverse is unnecessary.** The proof uses only \(\sup_j c_{j-1}/c_j<\infty\), equivalent to boundedness of \(S\). The inverse-translation expressions used on finite-support vectors are always defined.
- **Nonzero \(E\) is necessary.** The zero space behaves differently: its singleton orbit is already dense, including when \(\Gamma=\{0\}\). If \(\Gamma=\varnothing\), its empty orbit is not dense even in the zero space under the usual definition.
- **\(\Gamma\subseteq\{0\}\).** Neither operator on the nonzero infinite-dimensional spaces is \(\Gamma\)-supercyclic; (C) is false because \(\Gamma^*\) is empty.
- **No restriction on the arguments of scalars.** The two-open-set construction uses the complex inverse of the chosen \(\lambda\), which need not belong to \(\Gamma\). That inverse is a coefficient in the constructed vector, not an orbit scalar. The orbit scalar itself is always in \(\Gamma\).
- **No reliance on a generic-family equivalence.** A dense orbit does not imply the two-open-set property for every arbitrary family of maps. Here that implication is proved specifically using the weighted translation and (C).
- **\(p<\infty\) matters.** The proof uses finite-support density and countable-base separability. It makes no claim for the full \(\ell^\infty\) space.

## 4. Relation to the submitted candidate

The candidate's scalar tail argument and inductive construction are compatible with this independent proof. I found no flaw in the abstract amplification claim under its stated nonzero separable \(E\) assumption.

The original report resolves the essential separability issue: the talk introducing this problem explicitly starts its definitions with “Let \(X\) be a separable Banach space” (report p. 1081; local extracted text sources/source_OWR_2024_19.txt, lines 457–458). In that setting \(L^p(W)\) is separable because extension by zero identifies it with the closed subspace of \(L^p(X)\) supported on \(W\). A standalone theorem should preserve this assumption explicitly. Without it, the unrestricted application would be false for the reason recorded in Section 3.

No numerical verifier can certify the quantification over all \(\Gamma\), all weights, or all open sets; the proof above supplies that certification. Finite numerical examples can only check identities or illustrate the criterion.

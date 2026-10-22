# Independent verification: Nikula–Gaussian implication

Checkpoint: 2026-10-17 18:27 UTC. Completion: **100% of the assigned mathematical implication audit**. Historical byte-level provenance remains unverified as specified below. No other priority family/report was inspected. No Git, publication, or outreach action was taken.

**Verdict: VALID.** The stated Gaussian construction gives, almost surely, a frequently hypercyclic entire function whose product with every nonconstant complex polynomial fails hypercyclicity. The assertion is simultaneous over all such polynomials. Raw Gaussian samples do not satisfy the proposed eventual lower bound \(n^{-1/2}\), but an elementary radial clipping argument additionally gives dense frequent hypercyclicity in every fixed annular coefficient space described in §5.

## 1. Source and scope

Nikula, *Frequent hypercyclicity of random entire functions for the differentiation operator*, Theorem 1, pp. 2–3 of the supplied PDF, assumes IID complex coefficients with full-plane support and a tail bound 

\[
\limsup_{r\to\infty}(\log r)^{1+\beta}\Pr(|X|\ge r)<\infty
\quad\text{for some }\beta>0.
\]

Its conclusion is almost-sure entire convergence and frequent hypercyclicity of \(F(z)=\sum_{n\ge0}X_nz^n/n!\) for differentiation on \(H(\mathbb C)\). This verification takes that cited theorem as input; it does not reprove its full probabilistic argument. The [official version-specific PDF](https://arxiv.org/pdf/1209.6209v1), checked on 2026-10-17, displays the same hypothesis and conclusion.

Local input SHA-256 digests:

```text
nikula2012v1.pdf b24a6e7469325963d5bc343aca141b2e40b7d578c41e56023e6f984ed4c27e2b
nikula2012v1.txt 65b95e5e00e7f2b530c071617c58b6b07bf619209b0c823ef6c5a1154dcda23f
```

## 2. Gaussian event and universal polynomial obstruction

Normalize the standard complex Gaussian by density \(\pi^{-1}e^{-|z|^2}\). Then

\[
\Pr(|X|<t)=1-e^{-t^2}\le t^2,
\qquad \Pr(|X|>t)=e^{-t^2}.
\]

It has full-plane support and satisfies Nikula's tail condition for every \(\beta>0\). Both sums

\[
\sum_{n\ge0}\Pr\{|X_n|<(n+1)^{-3/4}\}<\infty,
\qquad
\sum_{n\ge0}\Pr\{|X_n|>\log(n+e)\}<\infty
\]

converge: their summands are bounded by \((n+1)^{-3/2}\) and \(e^{-\log^2(n+e)}\), respectively. The first Borel–Cantelli lemma, requiring no independence, therefore supplies a single measurable probability-one event on which

\[
(n+1)^{-3/4}\le |X_n|\le\log(n+e)
\quad\text{for all sufficiently large }n. \tag{1}
\]

Intersect this event with Nikula's probability-one frequent-hypercyclicity event. On any resulting sample path, let \(p(z)=\sum_{k=0}^d a_kz^k\), where \(d\ge1\) and \(a_d\ne0\). For \(n\ge d\), the exact identity is

\[
(pF)^{(n)}(0)=\sum_{k=0}^d a_k(n)_kX_{n-k},
\qquad (n)_k=\frac{n!}{(n-k)!}.
\]

Once \(n\ge2d\) and (1) applies to all \(n-k\), the degree-\(d\) term has modulus at least \(c_d|a_d|n^{d-3/4}\), with \(c_d=2^{-d-3/4}>0\). The sum of the other terms has modulus at most

\[
\left(\sum_{k<d}|a_k|\right)n^{d-1}\log(n+e)
=o(n^{d-3/4}).
\]

The reverse triangle inequality gives 

\[
|(pF)^{(n)}(0)|\longrightarrow\infty. \tag{2}
\]

This is a deterministic consequence of the same event (1), for **every** polynomial \(p\) of positive degree; the eventual starting index may depend on \(p\). No uncountable intersection of probability-one events, countability restriction on coefficients, or independence of nearby leading/remainder terms is used. Constant nonzero multiples are necessarily excluded: they remain frequently hypercyclic. The choice \(3/4\) can be replaced by any exponent strictly between \(1/2\) and \(1\).

Because evaluation at zero is a continuous surjection \(H(\mathbb C)\to\mathbb C\), a hypercyclic differentiation orbit must have dense scalar evaluations there. A scalar sequence tending in modulus to infinity, together with its finite initial segment, cannot be dense. Thus (2) proves that every nonconstant \(pF\) is not hypercyclic.

## 3. Full support, density, and polynomial additions

The Gaussian law of \(F\) has full support in \(H(\mathbb C)\). Here is a direct proof independent of the claimed obstruction. To approximate an entire target on \(|z|\le R\), choose its Taylor polynomial of degree \(N\) with sufficiently small deterministic remainder and choose \(N\) also so that

\[
\mathbb E\sum_{n>N}|X_n|R^n/n!<\varepsilon/6.
\]

Markov's inequality makes the random tail smaller than \(\varepsilon/3\) with positive probability. A sufficiently close match to the target's first \(N+1\) normalized coefficients also has positive probability. Finite-dimensional Gaussian full support and independence of the head and tail make their intersection positive. This proves the assertion for each basic compact-open neighborhood. Consequently every nonempty open neighborhood meets the probability-one good event above, giving density of the simultaneous counterexamples.

For every polynomial \(q\), \(D^n(F+q)=D^nF\) for all sufficiently large \(n\); finite changes in visit sets do not alter their lower densities. For every polynomial \(p\), \(p(F+q)-pF=pq\) is also a polynomial, so its sufficiently high jets vanish. Hence both frequent hypercyclicity and (2) persist under addition of **any** polynomial \(q\), pathwise and simultaneously. This does not require \(F+q\) still to have an IID coefficient law. The set \(F+\mathbb C[z]\) is itself dense, which supplies a second proof of density without using probabilistic full support.

## 4. Raw Gaussian versus the proposed annular condition

For \(n\ge1\),

\[
\Pr(|X_n|<n^{-1/2})=1-e^{-1/n}\sim1/n.
\]

These events are independent and have divergent probability sum. The second Borel–Cantelli lemma gives infinitely many violations almost surely. Thus the unmodified Gaussian construction has probability zero of belonging to any fixed or eventual class with lower bound \(n^{-1/2}\). Its weaker lower bound (1) already gives the same polynomial-obstruction conclusion, but it must not be identified with literal membership in that annular class.

## 5. Additional bridge: each fixed annular space

For precision define, for an integer \(M\ge1\),

\[
X_M=\left\{g(z)=\sum_{n\ge0}b_nz^n/n!:
 n^{-1/2}\le|b_n|\le u_n:=\log(n+e)\text{ for every }n\ge M\right\},
\]

with unrestricted earlier coefficients and the relative compact-open topology. The logarithmic upper bound ensures entire convergence. This space is closed in \(H(\mathbb C)\) because all derivative evaluations are continuous; in particular it is a Baire space. Replacing \(n^{-1/2}\) by \((n+1)^{-1/2}\) changes nothing in the proof.

Leave \(Y_n=X_n\) for \(n<M\). For \(n\ge M\), project \(X_n\) radially to the closed annulus \([n^{-1/2},u_n]\), choosing an arbitrary fixed angle at the null event \(X_n=0\). Put \(G_M(z)=\sum Y_nz^n/n!\). Coordinatewise transformation preserves independence. Each transformed coordinate has full support on its closed annulus, including both boundary circles: every relative neighborhood contains a nonempty open planar patch inside the annulus, with positive Gaussian probability. The early coordinates retain full-plane support.

Almost surely upper clipping occurs at only finitely many indices, by §2. Lower clipping changes a coefficient by at most \(n^{-1/2}\to0\). Thus \(\delta_n=Y_n-X_n\to0\), and for \(H_M=G_M-F\),

\[
\sup_{|z|\le R}|D^kH_M(z)|
\le e^R\sup_{n\ge k}|\delta_n|\longrightarrow0
\quad\text{for every }R>0. \tag{3}
\]

Frequent hypercyclicity survives (3): for a target ball of radius \(\varepsilon\), use visits of \(D^kF\) to the concentric ball of radius \(\varepsilon/2\), and discard the finitely many \(k\) before the perturbation is smaller than \(\varepsilon/2\). The surviving visits still have positive lower density. This works simultaneously for all targets because it is a deterministic implication of frequent hypercyclicity and convergence (3), not a target-indexed probabilistic intersection. Hence \(G_M\) is almost surely frequently hypercyclic.

The law of \(G_M\) has full support **relative to \(X_M\)**. Given \(g=\sum b_nz^n/n!\in X_M\), \(R>0\), and \(\varepsilon>0\), choose \(L\ge M\) so that

\[
2\sum_{n>L}u_nR^n/n!<\varepsilon/2.
\]

This bounds the tail of \(G_M-g\) deterministically. By finite-coordinate support and independence, the event

\[
\sum_{n=0}^L|Y_n-b_n|R^n/n!<\varepsilon/2
\]

has positive probability. It puts \(G_M\) in the required relative neighborhood. The random function is measurable as a locally uniform limit of measurable partial sums; no product-to-function topology issue arises. Every relative neighborhood therefore intersects the one probability-one event of frequent hypercyclicity, proving density of frequent hypercyclic vectors in every \(X_M\).

Finally, every \(g\in X_M\), independently of hypercyclicity, satisfies the polynomial obstruction by the argument of §2 with leading lower bound \(c_p n^{d-1/2}\) and remainder \(O_p(n^{d-1}\log n)\). Thus Nikula plus the clipping step gives dense frequently hypercyclic simultaneous counterexamples in each fixed \(X_M\). Since hypercyclic vectors form a \(G_\delta\) in \(H(\mathbb C)\) (use a countable open basis and \(\bigcap_j\bigcup_{n\ge0}D^{-n}U_j\)), their intersection with \(X_M\) is a dense \(G_\delta\) there. This argument asserts **density of frequent hypercyclicity**, not residual frequent hypercyclicity.

Fixed-\(M\) relative density, eventual-annulus membership \(\bigcup_{M\ge1}X_M\), and ambient density are different statements. Each is available here: §5 gives the first and hence the second; §3 gives the third. Adding a polynomial may move a function from \(X_M\) to a later \(X_{M'}\), so polynomial addition alone is not a proof of density within a fixed \(X_M\).

## 6. Date qualification and exact remaining gap

The [official version record](https://arxiv.org/abs/1209.6209v1) gives v1 submission as **27 September 2012, 12:45:47 UTC**. Both the supplied text and the currently served official v1 PDF display the internal line **“Date: August 2, 2018.”** That establishes the mismatch is also present in the official version-specific PDF currently served. An automatically generated compilation date is a plausible explanation, but it was not authenticated here from the original source or historical archive. Do not describe that internal line as a verified compilation date, infer a 2018 first-publication date from it, or claim a byte-identical 2012 PDF has been authenticated.

There is no remaining mathematical gap in the assigned corollary or the fixed-annulus bridge, conditional on Nikula's Theorem 1. The historical byte-level/provenance qualification remains as stated. This verification establishes a checkable deduction from the cited source; it does not by itself establish whether that deduction was explicitly recorded in earlier literature.

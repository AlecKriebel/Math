# Independent review of bounded Brownian concatenations

**Verdict: PASS for the stated approximation theorem and its explicitly unresolved disposition.** No mandatory mathematical correction was found. The full random-time-origin question remains unresolved; neither the fixed-junction diagnostic nor the scaling limit is a counterexample or a solution.

- Problem: 9500008, Burdzy Problem 8
- Date: 30 September 2026
- Reviewer: separate gpt-6-astra agent, xhigh effort
- Reviewed artifact: `PARTIAL.md`
- Frozen SHA-256: `3ad42fdecc5a30ef00d6fec6c18d1f2b8299be999d609711459bb67823af9bc1`
- Source artifact was not edited; the reviewed copy is byte-identical

## Source and quantifiers

[Burdzy's author-maintained Problem 8](https://sites.math.washington.edu/~burdzy/open_mathjax.php) defines the desired property using a random finite time origin. The two centered half-paths at that origin must be independent standard Brownian motions. The origin need not be a stopping time or an endpoint of a piece. The uniform bound on durations is one deterministic finite constant. The two-sided sequence consists of independent stopped pairs, not necessarily identically distributed pairs, and the sums of durations diverge in each direction. Zero durations are permitted.

These details agree with Definitions 2.1–2.2 of [Burdzy–Scheutzow, *Forward Brownian Motion*](https://arxiv.org/abs/1302.6958), current v4 of 29 March 2013, published in 2014. The fixed-origin law is denoted $2BM(0)$ there. Theorem 5.1 proves the random-origin property for iid stopped pairs with finite mean duration. Theorem 5.3 supplies, for each prescribed finite moment order, a nonidentical example satisfying a uniform bound at that order but not even backward Brownian motion. It is not a bounded-duration counterexample. In v4, the older Theorem 5.2 was renumbered 5.3; the artifact uses the current numbering correctly.

The separate Problem 7.7 allows an almost surely finite random supremum of the durations and asks about failure of the backward-Brownian property. Both that quantifier and that conclusion differ from the author's Problem 8. The artifact correctly keeps them separate. The [Pitman–Tang 2015 discussion](https://www.columbia.edu/~wt2319/Slepian.pdf), printed p. 3, is supplementary context; the exact assumptions and theorem statements are checked against Burdzy–Scheutzow itself.

## Brownian law of the reordered pieces

The definition of $W$ uses the negative-index stopped pieces in order $-1,-2,\ldots$, changes their signs, and does **not** reverse them internally. The duration of a piece is still a stopping time for the same filtration after changing the sign of its Brownian path. Brownian symmetry therefore preserves each stopped Brownian-pair law. Independence of the stopped pairs is preserved as well.

For clarity, one can justify the concatenation without assuming the entire original Brownian trajectories are mutually independent beyond their stopping times. For a fixed $J$, concatenate the first $J$ independent stopped pairs and append an independent Brownian continuation. Repeated strong-Markov splicing shows that this finite concatenation with its continuation is Brownian. It agrees with the infinite concatenation on $[0,A_J]$. For any fixed $L$, divergence $A_J\to\infty$ gives

$$\mathbb P(A_J\le L)\longrightarrow0.$$

The laws on $C([0,L])$ of the infinite concatenation and the finite Brownian splice therefore differ in total variation by at most this probability. The infinite concatenation is Brownian on every finite interval, hence on the half-line. The auxiliary continuation is only a way to verify the law; the actual $W$ in the proposition is the explicit function of the original negative stopped pieces and exists on the original probability space.

Zero-length pieces cause no problem. The formulas agree at repeated junction times, and divergence of the sums means that any fixed time interval is covered after finitely many indexed pieces. One need not condition on the positive-duration indices or assume that deleting zeros somehow preserves arbitrary independence statements.

The positive half of $X$ uses only indices $k\ge0$ and is Brownian by the same splicing argument. The construction of $W$ uses only $k<0$. Independence of these two sigma-fields proves independence of the two entire half-paths, not merely zero covariance. Thus the constructed $Z$ genuinely has law $2BM(0)$.

## Rotation identity and the pathwise estimate

At the $j$th negative junction, both $X_{-A_j}$ and $W_{A_j}$ equal the negative sum of the first $j$ negative-piece terminal values. In a piece of duration $T$ starting at $a=A_{j-1}$, the source indexing gives

$$X_{-(a+u)}=W_a+W_{a+T}-W_{a+T-u},\qquad 0\le u\le T.$$

Subtracting $W_{a+u}$ gives the difference of the two increments displayed in the artifact. Each increment has length $u\le T<c$. If $a+u\le R$, all endpoints lie in $[0,R+c]$, even when $R$ cuts through the middle of the last piece. The triangle inequality gives the exact bound

$$\sup_{0\le t\le R}|X_{-t}-W_t|\le2\omega_W(c;R+c).$$

There is no missing correction at junctions and no change in the order of the negative pieces. Brownian time reversal of a stopped piece is not being asserted. The factor $2$ comes from comparing the two increments, not from an independence estimate.

The piece-rotation mechanism is already visible in Burdzy–Scheutzow's proof of Theorem 5.2, preprint p. 20. The artifact appropriately credits it. This review does not establish priority for the bounded-duration corollary.

## Almost sure logarithmic error

For $R_m=c2^m$, any interval of length at most $c$ in $[0,R_m+c]$ is contained in some $[jc,(j+2)c]$ with $0\le j\le2^m+1$. The last such containing interval is allowed to extend beyond the target interval; $W$ is defined there. If an increment exceeds $r$, at least one endpoint differs from $W_{jc}$ by more than $r/2$.

For Brownian motion over time $2c$, reflection and the Gaussian tail bound give

$$\mathbb P\!\left(\sup_{0\le u\le2c}|W_{jc+u}-W_{jc}|>r/2\right)
\le4\exp\!\left(-\frac{r^2}{16c}\right).$$

Union over the $2^m+2$ intervals yields the artifact's bound. Independence of these overlapping intervals is not needed. Substituting $r=8\sqrt{cm}$ gives $4(2^m+2)e^{-4m}$, a summable sequence. Borel–Cantelli, followed by the monotonic comparison between consecutive dyadic radii, proves the claimed almost sure $O(\sqrt{\log(2+R)})$ estimate.

This argument is uniform in the number of pieces encountered. No lower duration bound, renewal-rate estimate, or iid assumption is hidden in the proof. In particular, very short pieces and arbitrarily many zero-duration pieces do not affect the deterministic time-interval cover.

For each fixed finite $L\ge0$, the error divided by $\sqrt r$ on $[-rL,rL]$ tends to zero almost surely. Brownian scaling gives the exact fixed law of $r^{-1/2}Z_{r\cdot}$, so the asserted convergence in distribution in the uniform topology follows. Almost sure convergence of those rescaled Brownian paths to a single limiting path is neither required nor asserted.

## Fixed-junction diagnostic and the missing shift

For $T=\min(\tau_{-1},1)$, the event $\tau_{-1}<1$ has positive probability. Before its first hit of $-1$, Brownian motion is strictly above $-1$, so the last reversed negative piece is strictly positive on some nonempty initial interval. Brownian motion starting at zero has probability zero of that event: for every deterministic positive interval its running minimum is negative almost surely, and a countable union over intervals of lengths $1/n$ covers the asserted event.

Thus the example is not $2BM(0)$. Nevertheless its stopped pairs are iid, bounded, have positive finite mean, and have divergent duration sums. Theorem 5.1 says it **is** $2BM$ after an appropriate random origin. The artifact explicitly draws this conclusion and does not mislabel the example as a negative answer.

The periodic-law observation also checks out when periodicity is for the entire stopped-pair law, as stated. Grouping one period of consecutive pieces produces independent identically distributed stopped Brownian blocks. Their total stopping durations have finite mean and satisfy the required divergence; Theorem 5.1 applies. Periodicity of durations alone would not justify this step, but that weaker assumption is not used.

The approximation modifies the path within infinitely many pieces. It supplies no exact equality after one finite time translation. Likewise, Brownian windows obtained by moving a deterministic observation point arbitrarily far to the right do not produce a finite random origin on the whole original path. The stationary marked-renewal coupling used in the iid theorem requires the common conditional path law; bounded nonidentical pieces do not automatically supply it. The remaining gap is accurately identified.

## Checks and final scope

The submitted verifier was copied before replay, so the author's files were not rewritten. Its 12,288 finite configurations and 48 exact prefix-law checks pass. The independent verifier checks 144 additional piecewise-linear configurations with zero durations and cut-through horizons, 2,256 rotation equalities, 16 exact prefix laws with randomized zero-duration stops, and the tail/scaling algebra. All 12 named check groups pass. These are diagnostics, not simulations or substitutes for the Brownian-law and almost-sure arguments above.

From this directory run `python3 submitted_verify.py` and `python3 independent_checks.py`; Python 3 and SymPy 1.14.0 were used. Results are recorded separately.

**Required corrections: none.** Preserve the full target's **unsolved** status, credit the existing rotation and iid results, and retain the absence of a priority claim. This independent AI review is unrefereed and covers the displayed frozen snapshot only.

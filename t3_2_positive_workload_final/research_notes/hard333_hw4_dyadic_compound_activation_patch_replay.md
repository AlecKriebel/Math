# Independent replay of the patched hard-\(H_w\) four theorem

**Replay date:** 2026-08-11 (America/Los_Angeles)  
**Canonical payload:**
`57608cbc0912802e526b5555631ffcfcaacd8eba2c26852439971babf5ea4aa7`

## Verdict and scope

**PASS** for the local common-factorial stopped-episode theorem on the exact
four hard \(H_w\) supports, for every strongly connected orientation and
every fixed positive rate vector.

This replay does **not** by itself promote the four pair-recurrence rows and
does not certify global T3-2.  Those conclusions require the separate pair
composition and global verification gates.  The canonical candidate
correctly leaves all nine analytic, pair, and global flags false.

The earlier audit of payload
`11a9c09fcb9ad032aaebfad1d707d038480777dd9f1b5c7a2e4b87c013dcc04d`
remains byte-stable and retains its strict FAIL-as-written verdict: that
payload asserted an unproved Green corrector.  The present payload replaces
that step by the independently derived event-skeleton/source-balance lemma.

## Frozen bytes

\[
\begin{array}{c|c}
\text{artifact}&\text{SHA-256}\\ \hline
\text{canonical note}&
\mathtt{df392304c5c0b5476584175c4601fd2e3d7f80e41154ae03c7ab1bd9de54b518}\\
\text{canonical source}&
\mathtt{bbe1bd66769c14c88930bb28a3402abba980b6d0422ce2201c83c1ea28be6a8f}\\
\text{canonical test}&
\mathtt{cf273a011d38b26f455b6490ba52d43dfde2962e34a749094f2cea0ba59ebb54}.
\end{array}
\]

The selector hash is
`4b24d4d3437351daf8e1d9b0e84e3d38e5e77147141a44fd9b68f6e1bba68716`,
the geometry-row hash is
`e80426c2363dca89d51a7a7e7cf845f64c807a8df76971c35c15941311d1ec70`,
and the 1,606-mask cut-profile hash is
`2f48ace8a269e1a8ab2c6eb7e770b7d69f9f20a8d396b9468368b1c1d3a5a54f`.

## Replay results

1. **Exact finite geometry — pass.**  The two resistance-two rows use
   \(R=2Y+C\), the two resistance-one rows use \(R=Y+2C\), and in the
   common parametrization the heights of
   \(\{2P,XU,PU,2U\}\) are \(\{2,2,3,4\}\).  Exhaustion of every strong
   four-node digraph gives 1,234 both-direct masks, 186 only-pure-direct
   masks, and 186 only-carrier-direct masks.  Every nondirect minimum node
   has the required zero edge to the direct node.

2. **Event-skeleton ascent — pass.**  In a dyadic band the aggregate
   minimum propensity is at least \(cr^2\), while the ratio of every
   high-source/lower exceptional clock to that aggregate clock is at most
   \(C(\varepsilon+r^{-1})\).  The exact pathwise source balances

   \[
   m_B\le U_0+2m_A+2e,
   \qquad
   2m_A\le P_0+2m_B+2e
   \]

   cover the respective single-direct cases.  Fixed conditional branching
   at the direct source and adaptive Chernoff bounds then force order \(r\)
   strict cuts in order \(r\) reaction events.  High-source reactions which
   repeatedly recreate the carrier-rich phase are charged to \(e\), so the
   hostile one-way configuration is included rather than hidden in a
   bounded reaction word.

3. **Dyadic exit and duration — pass.**  A lower exit requires order \(r\)
   bad reactions and has probability at most \(Ce^{-cr}\).  On the
   complementary event the strict cuts force the upper or activation exit.
   The order-\(r^2\) aggregate holding clock and the reaction-count tail give
   \(\mathbb E e^{crS_r}\le C\) and all fixed moments at scale \(r^{-1}\).
   No drain of a carrier-rich phase to \(U=0\) is assumed.

4. **Establishment and restart — pass.**  The contracted fixed-\(K\) chain
   includes every high-source slow competitor and has no closed
   unsuccessful class.  One or two physical seeds have a uniform positive
   trial probability.  A failed high dyadic block restarts a full attempt at
   its actual endpoint; it is not claimed to return to the fixed finite
   phase.  Uniform conditional success and attempt-duration bounds give the
   geometric and birth-count exponential moments.

5. **Deterministic service — pass.**  The largest invariant subset of
   \(C=0\) is exactly the dormant \(X\)-vertex.  Every other boundary
   trajectory enters the relative interior.  The activated compact shell is
   separated from that vertex.  Theorem 4.2 of Boros and Hofbauer,
   [*Permanence of Weakly Reversible Mass-Action Systems with a Single
   Linkage Class*](https://arxiv.org/abs/1903.03071), applies: the top network
   is weakly reversible, has one linkage class, fixed positive (hence
   bounded) kinetics, and a positive rank-two stoichiometric class.  It
   yields infinite service integral; continuity and compactness give one
   finite uniform fluid window.  Density convergence and the exact death
   compensator transfer this to the full stochastic chain.

6. **Negative macroincrement — pass.**  The proof uses the pathwise
   comparator

   \[
   Z=B-D_{\rm pre}-D_{\rm win}\le B-D_{\rm win}.
   \]

   Both terms on the right have uniform exponential moments, and the service
   threshold makes their conditional mean negative by a fixed margin.
   Uniform Taylor control—not negative mean alone—therefore gives the
   contracting exponential supermartingale.

7. **Stopped sums and common endpoint — pass.**  The supermartingale gives
   an exponentially unlikely upper population exit and an episode-count
   tail at scale \(n_0\); the fixed \(p>8\) duration bound follows by the
   standard stopped martingale estimate.  The upper crossing overshoot is
   controlled jointly with the rare event using the same exponential
   supermartingale and the episode's positive-tail bound.  On the lower
   branch, the multinomial factorial envelope converts
   \(n_\tau\le\rho n_0\) into a negative increment of order
   \((n_0\log n_0)^4\).  The rare upper branch and duration are negligible
   on that scale.  This is the same shifted physical factorial potential
   used by the other branches.

## Mechanical verification

The canonical and independent focused suites pass 9/9.  Both sources and
tests compile.  The canonical note has 33 display openings, 33 display
closings, and 33 distinct equation tags.  Pandoc with the
`tex_math_single_backslash` extension and Tectonic renders a nine-page PDF
without an error.

No exact orientation/rate counterexample and no T3-2 counterexample was
found in this replay.

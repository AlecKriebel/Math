# Independent audit of the guard-free (H_b) twelve

## Scope and verdict

**PASS**, strictly for the descriptor-local stopped common-W block in
`hard333_hb12_global_shell_resolvent`.  This does not certify recurrence of
the twelve pairs, the common-(W) 317 composition theorem, or the global
T3-2 claim.  All analytic, recurrence, and global flags remain false.

The frozen upstream hashes are

~~~text
rows     3999b185f5626b0999d72e9c10d3cdf082054f70cd84af8cd43a52aa6f286c7a
payload  f750d01ff8c0ea884df27cf8e4625f6d6ef020f8d335c6086f6c1147c0934417
audit    4dfbfe2aacf6dfaaf4d3c53c9c30be3b65b0d8e2f62cd31495f3e53ec8d84ed3
~~~

The frozen canonical bytes are

~~~text
note    8e6988149d6a889582ead592e47c05c3ca9a02f27da6e68182eea9959d55c513
source  01c99b0a5cb872be68d0adce6b7ffabd5cd499ded63b5c8d3b2b9df0801ddeaa
test    b6634246517734714cd990bb68a95e036a1a254a425cb383b8467b57217f1f6e
~~~

The six focused upstream tests replay, as do the focused tests for this
audit record.

## Replay of the two post-audit corrections

The common-potential grammar in (3.2) is now exact.  With
\(\ell=-\log\theta\),

\[
 -\log\pi_Q(x)=\log Z_Q+\sum_i\log(x_i!)+\ell\cdot x,
 \qquad
 G_\ell(x)=-\log\pi_Q(x)+c_Q,
 \quad c_Q=K_\ell-\log Z_Q.
\]

Only \(c_Q\), which rewrites the normalized shell law, depends on the
shell.  The physical function
\(G_\ell=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\) has one rate-dependent
\(K_\ell\), independent of \(Q\), and can be made at least one globally.
Thus \(W_\ell=G_\ell^4\) is genuinely common across shell and dimensional
handoffs.

The outside-core split is also corrected.  On the large reversible
top-flux branch, the top factorial drift absorbs only its own carré and
higher binomial terms.  On the complementary branch, the lower high-cut is
pointwise negative and absorbs only its own reverse-edge and fourth-power
remainders.  No lower reward pays a top mixing error.  The false margin
\(\gamma_Q/(\bar q g_Q)\to\infty\) is explicitly withdrawn; only
\(\gamma_Q/\bar q\to\infty\) is used inside the bounded-energy Kac core.

## Fatal counterexample to the withdrawn guard

For an integer \(m\to\infty\), take

\[
 B=m^2,\qquad C=2^{2m^3},\qquad A=m2^{m^3}.
\]

Then \(A^2=BC\) exactly and

\[
 2C>AC>\{2A,BC\}>C>AB>A>2B>B>0.
\]

The energy needed to reach \(B=0\) is only \(\Theta(m^2)\), while the
logarithm of the largest center coordinate is \(\Theta(m^3)\).  A guard of
fixed log-largest height therefore contains the boundary.  Uniform
pathwise (q/q_*\) control and boundary avoidance are false.  The v3
resolvent correctly uses no guard.

## Eight replay obligations

1. **Exact finite selector — PASS.**  There are twelve pairs and sixteen
   curvature incidences.  The gap-minus-kill histogram is twelve rows of
   excess one and four of excess two.
2. **Shifted factorial laws — PASS.**  A source tilt is the neighboring
   factorial-shell law shifted by its source, and products are finite
   nonnegative falling-factorial combinations.  This gives fixed moments
   of \(q/(\pi q)\) and \(q\)-size-biased shell energy.
3. **Pointwise Kac bridge — PASS.**  Removing a bounded-energy state from a
   one-dimensional strongly log-concave shell leaves a Dirichlet gap
   comparable with the shell gap.  The resulting Green and polarization
   bounds give the required cycle second and cross moments.
4. **Killed renewal quotient — PASS.**  The same-state quotient with
   \(d=\mathbb E(1-e^{-H})\) includes a kill during the first holding
   interval.  Its error is a relative
   \(O(\bar q/\gamma)=o(1)\), which remains valid for arbitrarily slow
   subpower refinements.
5. **Full endpoint and duration moments — PASS.**  The rewards
   \(h_j=\sum_e q_e|\Delta_eG_\ell|^j\) control the actual lower jump and
   the complete stopped increment through one integer \(p>8\).  Iterated
   Green bounds, with constants depending only on the fixed rate class,
   give
   \(\mathbb E e^{c\bar q\tau_R}\le C\) and hence the required duration
   moments.
6. **All stationary high cuts — PASS.**  Fourteen rows have one dominant
   source.  The other two have \(\{A,2B\}\) and \(\{A,2C\}\).  Under any
   subpower refinement, the first edge leaving the actual refined high set
   has a divergent negative factorial increment.  Every reverse positive
   contribution is bounded by \(h e^{-h}\).  This holds for every fixed
   strong orientation and positive rate vector and also yields the
   stationary \(b={\cal L}_RG_\ell\) \(L^2\) bound.
7. **Common fourth power and outside-core split — PASS.**  The physical
   function is the single positive
   \(G_\ell=K_\ell+\sum_i\log(x_i!)+\ell\cdot x\), with
   \(W_\ell=G_\ell^4\).  The terminal moment scale \(L_Q\) satisfies
   \(L_Q^2/(G_\ell g_Q)\to0\), so all nonleading fourth-power terms vanish.
   Inside the core one uses the Kac block.  Outside it, the reversible top
   flux and the lower high-cut fourth-power drift are separately negative;
   neither is charged against the other.
8. **Boundary endpoints and dependency — PASS.**  A pre-kill top path may
   hit \(B=0\) or \(C=0\).  V3 correctly routes a resulting endpoint
   through the exact two-active menu \(36+12=48\) and one-active menu
   \(36+2=38\), with the same \(W_\ell\).  Pair recurrence remains
   conditional on the common-\(W\) 317 composition theorem.

## Why no stronger same-scale margin is used

The tempting assertion

\[
 {\gamma_Q\over \bar q\,g_Q}\longrightarrow\infty
\]

is false if \(g_Q\) is also the scale in the stationary \(b\)-\(L^2\)
bound.  Let \(r_n=\lceil\log\log n\rceil\) and set

\[
 B=n,\qquad A=n^2r_n,\qquad C=n^3r_n^2.
\]

Again \(A^2=BC\), and this realizes the exact \((3,1,5)\) order.  On
\(\{0,A,2B,AB\}\), orient the fixed strong cycle

\[
 AB\to A\to0\to2B\to AB.
\]

Then \(\bar q\asymp AB\), \(\gamma_Q\asymp C\), and
\(\gamma_Q/\bar q\asymp r_n\), while both the stationary negative reward
and the \(b\)-\(L^2\) scale are \(\Theta(\log n)\), dominated by
\(AB\to A\).  Thus the displayed stronger ratio tends to zero.

This is not a counterexample to the stopped theorem.  In the core, the
Kac error is only \(O(\bar q/\gamma_Q)\) relative to the full negative
reward.  Outside the core, the separate pointwise lower high cut is
already negative, while top flux imbalance absorbs only its own discrete
curvature.  The v3 proof is valid precisely with this split.

## Reproduction

~~~text
PYTHONPATH=src python3 -B src/hard333_hb12_global_shell_resolvent_independent_audit.py
PYTHONPATH=src python3 -B -m unittest \
  tests/test_hard333_hb12_global_shell_resolvent_independent_audit.py -v
~~~

No canonical certificate or certification flag was edited.

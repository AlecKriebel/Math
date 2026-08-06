# Defect containment, overshoot, and well-founded rank

The final episode construction removes the unbounded defect-promotion
problem rather than iterating it.

For a terminal-complex template, a designated path is simple and has at most
\(|\mathcal C|-1\) edges.  The episode takes one additional terminal jump.
Therefore:

\[
1\le \tau\le |\mathcal C|
\]

in embedded-jump time.

Every complex has molecularity at most two.  Hence every coordinate changes
by at most two in one reaction and

\[
\|X_\tau-X_0\|_\infty\le2|\mathcal C|.
\]

A coordinate that is fixed along a divergent subsequence stays in one
explicit enlarged finite box during the complete episode.  A slower but
divergent coordinate also changes only by this constant; its normalized-log
status is unchanged.  No population can be promoted to a new asymptotic
layer inside one episode.

The only rank is the number of designated path edges remaining.  A
designated event lowers the rank by one.  Every non-designated event ends the
episode.  Thus the episode graph is well founded, cannot return to an
eliminated flag, and needs no global regime-cycle or seam argument.

If \(\kappa_*\) is the smallest nontrivial reaction rate, the current target
is enabled at every live phase and has an outgoing edge.  The total CTMC rate
is at least \(\kappa_*\), so episode duration is stochastically dominated by
a Gamma random variable with shape \(|\mathcal C|\) and rate
\(\kappa_*\).  In particular, for every integer \(q\ge1\),

\[
\mathbb E\tau_{\rm phys}^q
\le
\frac{\Gamma(|\mathcal C|+q)}
     {\Gamma(|\mathcal C|)\kappa_*^q}.
\]

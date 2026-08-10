# Finite carrier absorption lemma

Let \(\Phi\) be a finite carrier phase and, after division by the currently
slowest retained fast rate, let \(Q(\theta)\) be its killed generator.  The
parameter \(\theta\) ranges over one compact tied-rate cell.  Kill on service,
structural exit, or an event in the next slower source layer.

Assume that for every \(\theta\), every closed communicating class of the
unkilled fast graph has a service or structural-exit edge.  Then
\(-Q(\theta)\) is a nonsingular M-matrix.  Its inverse is nonnegative and
continuous in \(\theta\).  Compactness gives

\[
 \sup_\theta\|(-Q(\theta))^{-1}\|<\infty.       \tag{1}
\]

Thus the expected number of carrier changes and the expected scaled physical
time before service or exit are uniformly finite.

If the aggregate next-layer rate is at most \(\varepsilon_R\) times the
retained carrier rate throughout the stopped chart, compensator comparison
and (1) give

\[
 \mathbb P\{\hbox{next-layer interruption before service/exit}\}
 \le K\varepsilon_R.                            \tag{2}
\]

If (1) failed, a compact subsequence would converge to a parameter for which
the limiting fast graph has a closed nonservice class.  This is exactly the
finite class passed to the invariant/deficiency-zero/service atlas; no
informal mixing assertion is used.

The discrete form and exact Green calculation are implemented in
`src/carrier_absorption.py`.

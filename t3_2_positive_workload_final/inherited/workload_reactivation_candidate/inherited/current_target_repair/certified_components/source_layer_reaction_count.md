# Source-layer reaction-count lemma

Let a terminal chart have enabled-source layers

\[
 \mathcal F_1\gg\cdots\gg\mathcal F_m.
\]

For a killed embedded path let \(C_j(M)\) be the expected number of labelled
reactions whose source lies in \(\mathcal F_j\).  Write
\(\Lambda_j(x)\) for the aggregate physical propensity of that layer.

The complete source flag and compact tied-rate cell give, for \(i<j\),

\[
 \sup_{x\text{ in the chart}}
 \frac{\Lambda_j(x)}{\Lambda_i(x)}
 =\varepsilon_{ij}(R)\longrightarrow0          \tag{1}
\]

whenever both layers are retained in the same chart.  Disabled sources are
absent rather than assigned zero-scale rates.  Since embedded source
probabilities have the same ratio,

\[
 C_j(M)
 =\mathbb E\sum_{n<\tau_M}
    \frac{\Lambda_j(Z_n)}{\Lambda(Z_n)}
 \le \varepsilon_{ij}(R)
    \mathbb E\sum_{n<\tau_M}
    \frac{\Lambda_i(Z_n)}{\Lambda(Z_n)}
 =\varepsilon_{ij}(R)C_i(M).                  \tag{2}
\]

Inside one tied layer every source and every labelled channel with that
source carries a fixed positive fraction, bounded above and below on the
compact cell, of the layer count.

Faster recurrent zero classes are observed only through their exact return
trace.  Their phase corrections telescope; no source count is discarded.
If a layer count is bounded, its bounded reaction jumps have bounded total
endpoint displacement.  If it diverges, normalize its exact labelled counts
by that count.  Equation (2) removes strictly slower layers at that
normalization, while all faster layers have already been contracted as
complete-workload neutral.

Because the flag is finite, one obtains a first occupied changing trace.  If
all changing-layer counts were bounded, the physical workload could change
only by a bounded amount.  Faster neutral reactions remain in one finite
workload shell, so they cannot support an escaping occupation.  Hence every
escaping terminal chart has a first changing layer with diverging reaction
count.

Unfinished priority credit at the stopping boundary has uniformly bounded
mean in the strict branch by the negative credit drift of
`source_layer_current_target_theorem.md`.  Dividing by the diverging layer
count removes this boundary term.  Thus the first occupied changing trace
retains exact physical workload balance and a nonzero normalized transition
occupation.

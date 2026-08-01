# Universal Simultaneous Amplification

This research program asks whether one explicit family of finite connected
undirected weighted graphs can strictly amplify fixation, relative to the
same-order complete graph, under both birth--death (Bd) and death--birth (dB)
updating for every fitness value `r > 1`.

## Resolution

The answer is **no**, already because of dB updating.  If `s_i` is the degree
of vertex `i` in the positive-weight support, then

\[
\lim_{r\to\infty}\rho_{\rm dB}(G,r)
=\frac1n\sum_i\frac{s_i}{s_i+1}.
\]

This is strictly below the complete-graph limit unless the support is
complete.  For complete support and `n>=3`,

\[
\rho_{\rm dB}(K_n,r)-\rho_{\rm dB}(G,r)
=\frac{1}{n^2(n-2)r}
 \sum_i\sum_{\substack{j<k\\j,k\ne i}}
 \frac{(w_{ij}-w_{ik})^2}{w_{ij}w_{ik}}+O(r^{-2}).
\]

The coefficient vanishes only when every edge weight is the same, in which
case `G` is exactly the complete baseline up to irrelevant global scaling.
Thus every nonbaseline graph is dB-suppressing for all sufficiently large
finite fitness, and the baseline itself never gives a strict inequality.

This closes the weighted-complete case left open by the earlier general
transience bound for noncomplete graphs; see `notes/LITERATURE_AUDIT.md` for the
post-verification audit and its novelty caveat.

The discovery phase is deliberately first-principles: no literature search is
performed until a candidate theorem has been independently derived and
verified.  Numerical experiments are used only to generate conjectures; every
reported theorem must have an exact proof certificate.

## Layout

- `RESEARCH_LOG.md`: timestamped checkpoints and decisions.
- `notes/`: derivations and candidate-family analyses.
- `src/`: exact Markov-chain and symbolic-certification code.
- `tests/`: independent checks of transition and fixation formulas.
- `certificates/`: exact polynomial-positivity or obstruction certificates.
- `figures/`: graph diagrams used in the manuscript.
- `results/`: reproducible machine-generated summaries.

## Verification

With SymPy 1.14 installed:

```bash
PYTHONPATH=. python -m unittest discover -s tests -v
PYTHONPATH=. python verification/verify_obstruction.py
```

The final manuscript is
`output/pdf/universal_simultaneous_amplification_obstruction.pdf`; its source is
`paper/main.tex`.

# Universal Simultaneous Amplification

This research program asks whether one explicit family of finite connected
undirected weighted graphs can strictly amplify fixation, relative to the
same-order complete graph, under both birth--death (Bd) and death--birth (dB)
updating for every fitness value `r > 1`.

## Fixed-graph resolution

The answer is **no**, already because of dB updating, and the closure now
holds for directed weights. With `w_uv` denoting source `u` into target `v`,
every noncomplete strongly connected directed support is eventually
suppressing by the prior transience theorem; a source-component bound handles
non-strong supports. For complete directed support,

\[
\rho_{\rm dB}(K_n,r)-\rho_{\rm dB}(G,r)
=\frac{1}{n^2(n-2)r}
 \sum_v\sum_{\substack{u<z\\u,z\ne v}}
 \frac{(w_{uv}-w_{zv})^2}{w_{uv}w_{zv}}+O(r^{-2}).
\]

The coefficient vanishes exactly when every incoming column is constant. Such
a weighting is dB-equivalent to `K_n` for every fitness by independent column
scaling, so it ties rather than amplifies.

For undirected weights, if `s_i` is positive-support degree, then

\[
\lim_{r\to\infty}\rho_{\rm dB}(G,r)
=\frac1n\sum_i\frac{s_i}{s_i+1}.
\]

This is strictly below the complete-graph limit unless support is complete.
Thus every fixed graph is eventually suppressing or exactly ties the dB
baseline.

The complete beneficial-fitness classification is also proved for `n=3`: every
nonuniform positive weighted triangle is a strict dB suppressor for every
`r>1`, with an exact rational comparison and homogeneous SOS certificate.  On
four vertices the same conclusion is proved for the full `1+3` core--satellite
orbit family and the full `2+2` paired-class orbit family.  The unrestricted
six-edge weighted `K_4` classification remains open.
Precisely, this rules out

```text
exists N0, for every N >= N0, for every r > 1: amplification.
```

It does not settle the reversed asymptotic quantifier order

```text
for every fixed r > 1, exists N0(r), for every N >= N0(r): amplification.
```

That question is a separate continuation track.

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
- `CLAIMS_LEDGER.md`: status and provenance of every substantive claim.
- `phase1_directed/`: directed proof, source-component closure, and verifier.
- `phase2_triangle/`: exact beneficial-fitness triangle classification and hostile audit.
- `phase2_n4/`: exact symmetric `K_4` classifications and hostile audit.
- `phase3_asymptotic/`: proved support-degree and dense finite-type obstructions,
  plus the surviving quantifier gap.
- `figures/`: graph diagrams used in the manuscript.
- `results/`: reproducible machine-generated summaries.

## Verification

One-time environment setup:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Then the complete Paper I reproduction is one command:

```bash
make paper1
```

Individual checks are also available:

```bash
make test
make verify
make directed
make triangle
make n4
make phase3-check
```

The verifier checks the exact transition implementation and representative
symbolic instances.  The all-graph quantifier is proved by the displayed
support-gap and sum-of-squares identities in the paper, not by finite testing.

The final Paper I manuscript is `output/pdf/no_universal_death_birth_amplifier.pdf`;
its source is `paper/main.tex`.

Version 1.0.0 is published at
<https://github.com/AlecKriebel/Math/releases/tag/universal-db-obstruction-v1.0.0>.
Its archival DOI is <https://doi.org/10.5281/zenodo.21753405>.
The reader-facing paper page is
<https://aleckriebel.github.io/Math/papers/no-universal-death-birth-amplifier/>.
Release assets include the publication PDF, an editable manuscript-source
archive, a full reproducibility archive, and a SHA-256 manifest.

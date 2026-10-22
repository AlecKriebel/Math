# Audit of the proposed Erdős 995 bound

This packet accepts the source-scoped conclusion of Boon Suan Ho's Theorem 1.6 in [arXiv:2604.18535v2](https://arxiv.org/abs/2604.18535v2), *Counterexamples for lacunary dilates via dyadic spike blocks* (21 April 2026). It verifies an existing counterexample from Ho's unrefereed preprint. It does not claim a new disproof.

For each fixed finite real $p\ge2$, the construction supplies a real mean-zero $f\in L^p(\mathbb T)$ and one deterministic sparse dyadic sequence $n_j=2^{m_j}$ with $n_{j+1}/n_j\ge2$. On one full-measure set,

$$
\limsup_{N\to\infty}
\frac{\sum_{j\le N}f(n_jx)}{N(\log N)^{1/p-\varepsilon}}
=+\infty\qquad\text{for every }\varepsilon>0.
$$

The function and sequence may depend on $p$, but not on $x$ or the subsequent choice of $\varepsilon$. At $p=2$, this refutes the proposed universal $o(N\sqrt{\log\log N})$ bound. The term count $N$ counts the selected samples, not the dyadic exponent or the sampled integer.

## What was verified

[AUDIT.md](AUDIT.md) is the complete authored mathematical proof/audit, preserved byte-for-byte. It covers the binomial moment estimate for every finite real $p\ge2$, the explicit geometric budget and Minkowski argument, summable deterministic lower floors, binary-digit independence, trial amplification, recursive stage counts, shielding of other blocks, and the common full-measure set for all positive $\varepsilon$. Finite exact regression checks supplement the analytic proof; they are not a proof by themselves.

[ACCEPTANCE.json](ACCEPTANCE.json) records the qualified source-scoped acceptance. [SOURCES.json](SOURCES.json) records the public bibliography, pinned PDF hashes and sizes, and the bounded retrieval and inspection history. [ARTIFACT_MANIFEST.json](ARTIFACT_MANIFEST.json) lists this packet and hashes its content files. The manifest does not attempt to hash itself.

## Attribution and boundaries

Erdős's 1964 paper prints lower examples at the scale $N(\log\log N)^{1/2-\varepsilon}$ and a general upper scale $N(\log N)^{1/2+\varepsilon}$. The exact modern little-o formulation is not literally displayed on the inspected original page. The audit distinguishes those statements and credits the accepted counterexample to Ho.

No epsilon-free logarithmic endpoint or optimal secondary logarithm is claimed. The sequence is sparse; no claim is made about consecutive dyadic averages or bounded exponent gaps. The packet does not independently accept the Fourier-tail theorems, Erdős 996 consequences, or other manuscript sections outside the stated dependency chain.

## Review disclosure

This is an AI-assisted mathematical audit. It has had no external human review and no formal certification. “Acceptance” here is the audit's mathematical assessment within its explicit scope, not peer review, journal acceptance, or a mechanically checked proof. The public abstract page was inspected on 11 October 2026 and showed no journal-reference field; this does not establish absence of any later publication.

The packet contains authored exposition and public verification metadata only. Source PDFs, extracted source text, source images, datasets, raw numerical tables, executable scripts, and private coordination material are not included.

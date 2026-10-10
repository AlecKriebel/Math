# Source credit and inspection scope

Problem 30005263 / OWR-11695859-006 concerns the dimension-free global
Lipschitz bound for the quadratic optimal map from standard Gaussian measure
to a probability measure e^f times that Gaussian, for every globally Lipschitz
f and every finite dimension.

## Original conjecture

Max Fathi, “Globally Lipschitz transport maps,” joint work with Dan Mikulincer
and Yair Shenfeld, states Conjecture 1 in Oberwolfach Report 49/2022,
Heat Kernels, Stochastic Processes and Functional Inequalities, printed page
2845 (PDF page 35). The contribution begins on printed page 2844 (PDF page
34). The following theorem concerns a transport that need not be optimal.
[Original report](https://ems.press/content/serial-article-files/46987).
[Publisher record](https://ems.press/journals/owr/articles/11695859).

## Credited exact Gaussian proof

Maja Gwóźdź, Caffarelli Estimates under Lipschitz Perturbations,
arXiv:2609.04052v1, was submitted September 3, 2026, at 16:24:45 UTC.
The exact Gaussian result is credited to that preprint after the substitution
B=-f. The primary arXiv metadata retrieved October 10, 2026 listed one version
and no journal reference or acceptance statement. Journal acceptance and
peer review are not established. This finding claims no new proof, novelty,
priority over every other work or community consensus.
[Version record](https://arxiv.org/abs/2609.04052).
[Inspected v1 PDF](https://arxiv.org/pdf/2609.04052v1).

The PDF has 630,541 bytes and SHA-256
1077982c0ecae8d89b231058b6b2485fe317ce8b0eee8777f9bcef58d78b0086.
The independent retrieval matched the earlier retrieved copy byte-for-byte.

[AUDIT.md](AUDIT.md) preserves the complete substantive proof-route review:
full-space regularity and moments, the noncircular additive large-scale
bound, translated Monge–Ampère identity, compatible Schur inequalities,
noncommuting Appendix A.1 algebra, strict radial penalty, noncompact maximum,
approximation to every globally Lipschitz perturbation, reverse transport
and scalar optimization. [PROOF_DEPENDENCIES.json](PROOF_DEPENDENCIES.json)
preserves all 13 dependency nodes, their hypotheses and review qualifications,
and all 13 edges.

## Imported results and boundaries

The necessary additive modulus is checked through Gozlan–Sylvestre,
Global Regularity Estimates for Optimal Transport via Entropic Regularisation,
arXiv:2501.11382v5. The entropic-to-Brenier passage uses Nutz–Wiesel Theorem
1.1 with its product-integrable continuous nonnegative quadratic cost.
[Large-scale estimate v5](https://arxiv.org/pdf/2501.11382v5).
[Entropic convergence author PDF](https://www.math.columbia.edu/~mnutz/docs/potentialConv.pdf).

The full-space regularity result is matched by hypotheses and content in
Cordero-Erausquin–Figalli, Regularity of monotone transport maps between
unbounded domains (2019). Inspected copies label its consequence Corollary 5,
whereas Gwóźdź cites Corollary 1 of the published article; this numbering
mismatch does not substitute for content checking.
[Author record](https://cvgmt.sns.it/paper/4317/).
[Published article](https://www.aimsciences.org/article/doi/10.3934/dcds.2019297).

Brenier existence/uniqueness, classical local Monge–Ampère regularity and
the proof of Nutz–Wiesel Theorem 1.1 remain imported published foundations.
The review is not a recursive reproof of those theories. The earlier Gwóźdź
manuscript arXiv:2608.15906 is a methodological predecessor; the essential
Gaussian proof route is supplied again in the inspected v1 manuscript.

The Lemma 3.12 exceptional-line exposition issue remains explicitly recorded;
it is nonblocking for the Euclidean target via the uniform smooth bounds,
locally uniform convergence and Lemma 3.11. No blanket certification covers
the broader noncommuting anisotropic theorem, Section 6, or the later
Section 5.1 displacement proof. The reverse bound and scalar optimization
were checked as additional descriptions of Theorem 1.1.

## Inspection and editorial limits

The historical review read all essential proofs on the Gaussian dependency
route and the specified imported statements/proof links. The metadata
records the exact text coverage and 28 visually inspected pages among 35
rendered pages. Rendering alone is not visual inspection.
[SOURCE_METADATA.json](SOURCE_METADATA.json) contains source hashes, sizes,
public links, retrieval times/status and the detailed inspection record.

This authored audit is AI-assisted and unrefereed. Acceptance denotes the
bounded proof-level review, not external human peer review, journal acceptance
or proof-assistant certification. Edition preparation rechecked existing
bytes and publication integrity; it performed no new source retrieval,
substantive proof-source inspection, literature search or mathematical
computation. One backspace/beta and four vertical-tab/epsilon corruptions
were repaired as notation rendering only. No mathematical correction is
introduced. Copied third-party documents, source text, screenshots, programs,
raw outputs, datasets and private coordination material are excluded.

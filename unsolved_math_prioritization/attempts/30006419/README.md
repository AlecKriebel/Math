# Harmonic sphere energy distinctions: accepted authored resolution

Problem **30006419 / OWR-14299521-012**, rank **969**. Disposition: **claimed_solved**, **2/5 substantive author approaches**.

## Results and acceptance

- [Complete counterexample](author/PROOF.md): a smooth homeomorphism from the round sphere to a compact smooth Riemannian sphere is locally minimizing for **Reshetnyak energy**, against all same-trace Sobolev competitors on the required neighborhoods, but has essentially unbounded infinitesimal distortion. This resolves the inspected **general admissible-energy** formulation negatively. The map is neither KS/Dirichlet-harmonic nor a global homotopy minimizer.
- [Separate KS theorem](author/KOREVAAR_SCHOEN.md): a locally **Korevaar–Schoen** energy-minimizing Sobolev sphere map into a complete metric space is infinitesimally `(4 + sqrt(17))`-quasiconformal, within the stated standard metric-Sobolev differential/chain-rule framework. The bound is nonsharp; no target isoperimetric or topological condition is used.
- [Audit A](audit_a/INDEPENDENT_AUDIT.md) and [Audit B](audit_b/SECOND_INDEPENDENT_AUDIT.md), including [B's separate KS audit](audit_b/KS_APPENDIX_AUDIT.md), accept both complete arguments without mathematical corrections.

All 22 original author/audit files are preserved byte-for-byte. The nine-file author freeze retains its historical pre-audit status language. The later acceptance reports and [publication status](PUBLICATION_STATUS.json) give the current disposition. [Approaches](author/APPROACHES.md) records the two actual proof approaches; source retrieval, audits, computation and publication do not add turns.

## Source and claim limits

Exact scope is bound to [arXiv:2503.08553v1](https://arxiv.org/pdf/2503.08553v1), notably Question 1.9 and Definitions 3.1 and 6.1, and [OWR 30/2025](https://ems.press/content/serial-article-files/52249), printed p. 1625. The source ledger and both audits distinguish full-PDF retrieval from the particular text and rendered pages inspected. The author's bibliography reports the journal publication, but **the final publisher text was not retrieved or inspected**. The publication step replays the frozen evidence; it does not claim a new literature review.

This is AI-assisted, unrefereed authored mathematics with two independent mathematical audits. It is not human peer review, a proof-assistant formalization, or a historical-priority certificate. Public source metadata is included; copied source documents, source text, dataset contents and private coordination files are excluded.

## Reproduce without source documents

Use Python 3 with the versions in `requirements.txt`. Obtain the trusted SHA-256 of `PUBLIC_MANIFEST.json` from the PR description, then run from any working directory:

```sh
python3 -I -B /path/to/packet/verify_publication.py --expected-manifest TRUSTED_SHA256
python3 -I -O -B /path/to/packet/verify_publication.py --expected-manifest TRUSTED_SHA256
python3 -I -O -B /path/to/packet/mutation_tests.py --expected-manifest TRUSTED_SHA256
```

The wrapper authenticates every path, byte count and SHA-256 before executing any frozen control script, checks the externally fixed author/audit pins, and runs in disposable copies. It rejects extra or missing files/directories and symlinks. It never downloads source documents.

- Author: **257 exact algebra controls**, replayed byte-identically.
- Audit A: independent **mixed symbolic/exact and numerical** controls, with tolerances and negative controls. This is not an all-exact verification.
- Audit B: its original **675** mixed checks include **two source-PDF identity checks**. The default source-free adapter explicitly omits those two input checks and replays the other **673**, including 11 frozen-author identity checks. The unchanged audit records retain the historical full 675-check run. An optional full replay with user-supplied PDFs is available via `--sources DIRECTORY`; filenames and public identities are recorded in `audit_b/SOURCE_INSPECTION.json`. A replay of supplied bytes is not fresh retrieval or a new source inspection.

Finite controls support algebra, numerical diagnostics and integrity. The analytic arbitrary-competitor claims are addressed by the complete written proofs and audits, not certified by check counts. The external manifest pin must come from a trusted channel: a self-consistent replacement packet is not authentic merely because it hashes itself.

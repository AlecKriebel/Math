# Provenance and reproducibility

## Canonical status -- 23 August 2026

`k2p_k3p_theta_clarified/` is the sole current manuscript,
verification, submission, and archival subtree. The paper, summaries,
certificates, and verifiers outside that subtree are retained only as
pre-clarification history. They must not be treated as a parallel current
package or included in a new deposit. The former unversioned parent ZIP was
removed and replaced by the commit-pinned version `1.0.0` replay supplement
`k2p-k3p-theta-collision-4100ec652405.zip`; the removed archive remains
recoverable from Git history.

This repository is public. The pre-clarification combined package first appears
in repository history at commit `ca21a733`, dated 4 August 2026, and was linked
from the public project page by commit `85cdead2`. The clarification revision is
additive and no Git history was rewritten. A bioRxiv submission candidate and
its author-facing metadata are prepared in the canonical subtree. The frozen
source/replay snapshot is version `1.0.0`, identified by the Git tag
`k2p-k3p-theta-biorxiv-v1.0.0`. No external communication was initiated during
this preparation checkpoint.

The versioned ZIP was built from full commit
`4100ec6524054cef1e78441587abc9487d689d0b`. The builder produced byte-stable
ZIP and tar.gz forms, verified their generated metadata byte-for-byte, and
validated every internal file hash. Independent clean extraction confirmed
identical ZIP/tar contents, normal and optimized verifier success, warning-free
PDF builds, and matching extracted text and rendered pixels.

## Discovery sequence

AI-assisted analysis of a K3P follow-up first identified a possible sign-definiteness and leaf-order problem in the K2P invariant used in Lemma 5.6 of arXiv:2607.12919v2. That analysis also supplied an exact rational negative-sign point and a high-precision numerical tree/theta collision candidate, explicitly marked as requiring independent verification.

The exact results distributed here were then constructed and checked independently:

- the compact K2P collision over `Q(sqrt(71))`;
- the exact strict continuous-time K2P collision over an isolated cubic field with `sqrt(1423)`;
- the exact K2P rank-9 minors and local dimension calculation;
- the exact six-dimensional symmetric collision family;
- the integrated K3P collision, rank-15 determinant, and analytic continuous-time extension.

The package therefore does not describe the K2P direction as having arisen spontaneously during a generic final audit.

## Inherited exact materials

The package incorporates material from an earlier K2P reproduction audit and the prior K3P-only package. The K3P-only repository version is recoverable at commit `d60581d1`. The separate K2P audit directory and first-contact memo were not included in this repository. The clarification revision reconstructs its focused two-page note from the exact certificate and unified paper without overwriting the pre-clarification paper, summary, certificates, or original verifier modules.

## Independent recomputations

This package recomputes source conventions; topology and root suppression; all simple K2P edge, Fourier, pattern, minimum-probability, invariant, and rank checks; the strict continuous-time K2P field, rate, factorization, pruning, and order checks; both K2P rank calculations and the collision family; and the K3P collision, stochastic data, rank determinant, local dimension, and continuous-time tangent identities. The complete verifier suite in `src/` and `verify.py` reproduces every one of these checks from the certificates.

## Exact arithmetic

The simple K2P verifier works in `Q(sqrt(71))`. The strict continuous-time K2P verifier uses an isolated cubic element together with `sqrt(1423)`. The K3P verifier works in `Q(h)` with `5 h^4 = 1`. Required verifiers use only the Python standard library and rational interval bounds.

The cubic root and square-root intervals were tightened in this revision so that the printed child-invariant decimal values are rigorously enclosed to the displayed precision.

## Analytic versus machine-verified conclusions

Every computationally derived factorization, stochastic inequality, pattern equality, determinant, and tangent identity is replayed exactly. The nearby strict continuous-time K3P branch follows from the ordinary real-analytic implicit-function theorem after exact verification of an invertible Jacobian and the relevant tangent signs.

## AI assistance

AI-assisted mathematical research, symbolic exploration, code generation, auditing, and editorial tools contributed to discovery and preparation. The package does not expose hidden chain-of-thought or internal scratch work. Claims are presented through ordinary proofs, exact certificates, source code, and independently replayable computations.

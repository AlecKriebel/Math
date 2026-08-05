# Provenance and reproducibility

## Status

August 2026. No journal or arXiv submission has occurred. The source authors have not yet been privately notified of this construction.

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

The package starts from two preserved projects: the independent K2P reproduction audit containing the simple and strict continuous-time collisions, proof-order audit, direct-pruning verifier, and certificates; and the latest corrected K3P author-ready package containing the semi-directed formulation, exact quartic collision, rank-15 determinant, local-overlap theorem, analytic continuous-time extension, and exact certificates. Neither inherited directory was overwritten.

## Independent recomputations

This package recomputes source conventions; topology and root suppression; all simple K2P edge, Fourier, pattern, minimum-probability, invariant, and rank checks; the strict continuous-time K2P field, rate, factorization, pruning, and order checks; both K2P rank calculations and the collision family; and the K3P collision, stochastic data, rank determinant, local dimension, and continuous-time tangent identities. The complete verifier suite in `src/` and `verify.py` reproduces every one of these checks from the certificates.

## Exact arithmetic

The simple K2P verifier works in `Q(sqrt(71))`. The strict continuous-time K2P verifier uses an isolated cubic element together with `sqrt(1423)`. The K3P verifier works in `Q(h)` with `5 h^4 = 1`. Required verifiers use only the Python standard library and rational interval bounds.

The cubic root and square-root intervals were tightened in this revision so that the printed child-invariant decimal values are rigorously enclosed to the displayed precision.

## Analytic versus machine-verified conclusions

Every computationally derived factorization, stochastic inequality, pattern equality, determinant, and tangent identity is replayed exactly. The nearby strict continuous-time K3P branch follows from the ordinary real-analytic implicit-function theorem after exact verification of an invertible Jacobian and the relevant tangent signs.

## AI assistance

AI-assisted mathematical research, symbolic exploration, code generation, auditing, and editorial tools contributed to discovery and preparation. The package does not expose hidden chain-of-thought or internal scratch work. Claims are presented through ordinary proofs, exact certificates, source code, and independently replayable computations.

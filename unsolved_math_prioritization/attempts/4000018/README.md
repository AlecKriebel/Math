# L2 Bonnet–Myers and dimension: audited partial results

Target 4000018 / AMR-039-0018 (rank 663), Yann Ollivier's Problem R.
**The original problem remains unsolved after five substantive approaches.**

The frozen author packet and complete portable independent audit are preserved
byte for byte. The independent audit accepts seven precisely scoped results and
finds no mandatory mathematical correction. Its additional boundary result is
retained in full. This is an AI-assisted, unrefereed research packet, not human
peer review, a formal proof certificate, or a claim of historical novelty.

## Results and essential qualifications

1. An explicit nonlocal reset semigroup satisfies the displayed unequal-time W1
   estimate with kappa = 1, C = 16 D^2, and horizon 1/4.
2. Its sharp finite-dimensional BE profile on an atomless space is K_N = 1-4/N.
   Failure of BE(1,N) for finite N does not mean failure at all lower curvatures:
   finite N is available at every K < 1.
3. The same transport data occur on compact geodesic examples of arbitrarily
   large and infinite Hausdorff dimension, with full-support reversible measure.
   The reset generator is nonlocal and noncanonical. This does not settle a
   canonical diffusion, intrinsic-metric, or RCD equivalence question.
4. Under the precise EKS or Kuwada finite-dimensional heat-flow hypotheses,
   the W2 estimate implies the W1 estimate with C = 2 N exp(K T). No converse,
   sharpness, or attained endpoint constant is asserted.
5. Exact time and metric scaling distinguish admissible constants from intrinsic
   dimension and from optimal constants.
6. Standard Brownian motion yields n-1 <= C_* <= n, with C_* > 0 on the line.
   This is a zero-curvature calibration.
7. Ornstein–Uhlenbeck equal-time contraction and infinite-dimensional BE do not
   ensure any finite uniform unequal-time coefficient on the unbounded space.

Crucially, the reset estimate uses kappa = 1, whereas its optimal equal-time
W1 contraction rate is 2. The audit proves that no finite unequal-time correction
works at kappa = 2 on the uniform unit interval. These constants cannot be
silently interchanged. Despite the target's L2 label, Problem R uses W1.

## Review and preserved records

- [Complete authored proofs](author_packet/authored/FULL_PROOFS.md)
- [Assumptions and source conventions](author_packet/authored/SOURCE_AND_ASSUMPTIONS.md)
- [Five approaches](author_packet/authored/APPROACH_LOG.md)
- [Remaining gaps](author_packet/authored/LIMITATIONS.md)
- [Full independent audit](independent_audit/AUDIT_REPORT.md)
- [Audit result](independent_audit/AUDIT_RESULT.json)

The author freeze predates review and retains its historical audit-required
wording. The complete separate audit supplies the current review outcome.
Public source hashes, byte counts, inspection history, and bibliographic links
are retained; scholarly PDFs, source extracts, source-page images, dataset
contents, and private coordination records are excluded.

Author archive: 26,133 bytes, SHA256
`82f9acc92840eaef8ad85c7473817ed3eca5107ba4c851aaabd23c874eb2714e`.
Audit archive: 14,956 bytes, SHA256
`d3507a9a8767eda60109f851f442445b1ee2baac4bcd0435b35d0912da8a8690`.

## Reproduce

From this directory, run `python3 verify_release.py`. Python 3.8+ standard
library only; no installation, network, credentials, or private input needed.
The strict manifest verifies all files, both archives, exact archive-to-directory
equality, and author/audit internal manifests. The author program reproduces
28,156 exact assertions and the independent program 52,820, with parsed output
equal to the frozen records. Counts corroborate the written proofs; they do not
replace analytic review or settle the full problem.

Primary sources: [Problem R](https://www.yann-ollivier.org/rech/publs/problems_curvmarkov.pdf),
[Ollivier Proposition 52](https://www.yann-ollivier.org/rech/publs/curvmarkov.pdf),
[EKS v2](https://arxiv.org/pdf/1303.4382v2),
[Kuwada v2](https://arxiv.org/pdf/1308.5471v2).

Only this problem's queue Status and Turns cells change. All other queue bytes,
including the existing header, Findings and links, remain unchanged. No merge,
release, DOI deposit, or outreach is part of this draft publication.

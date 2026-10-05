# Ordinary Dirichlet series with exactly one zero: audited partial results

**30002507 / OWR-12866-017, rank 722. Unsolved after 5/5 substantive approaches.**

This AI-assisted, unrefereed checkpoint contains restricted and conditional deductions, not a complete solution, novelty certification, or certification of global openness. The independent AI audit accepts the retained arguments within their stated scope, with no mandatory mathematical corrections. It is not external human refereeing or formal proof verification.

## Strongest verified partial result

Frequency rounding and exact-zero correction, applied to the credited Broucke–Vindas generalized-series example, produce ordinary Dirichlet series converging on Re(s)>1/2, allowing conditional convergence. For sufficiently large q the zero at 1 is exact and simple. For every fixed prescribed compact K avoiding 1, a sufficiently large q(K) gives nonvanishing on K. The convergence abscissa is at most 1/2; equality is not established.

The missing step is one ordinary coefficient sequence excluding every additional zero throughout one entire open convergence half-plane containing 1. The parameter depends on K. Local nonvanishing, escaping-zero tests, and a generalized-series limit do not establish global uniqueness.

The other approaches give restricted recurrence and representation obstructions, a sparse-prime perturbation theorem, and a conditional Möbius construction whose required power-saving hypothesis remains unproved. No sixth proof-search approach was added during verification.

## Read and reproduce

- [Frozen author packet](author/safe/README.md), including all five complete arguments.
- [Independent audit](independent_audit/AUDIT.md), including analytic stress tests, exact quantifiers, and remaining gaps.
- [Current publication status](PUBLICATION_STATUS.json) and [validation scope](VALIDATION.json).
- [Primary-source verification metadata](author/safe/SOURCE_VERIFICATION.json) and [independent source binding](independent_audit/SOURCE_BINDING.json).

The frozen author packet's pending-audit wording records its historical state. This wrapper and the included audit record completion of that review without rewriting either frozen input. The included base64-encoded author ZIP contains only the same 18 safe files. The wrapper decodes it into a disposable replay copy and verifies its original 29,837 bytes and SHA-256 before running the independent frozen-archive checks. Text encoding permits byte-for-byte remote readback through the connector without source downloads.

From any working directory, run:

```sh
python3 -B /path/to/30002507/verify_publication.py /path/to/30002507 EXPECTED_PUBLICATION_MANIFEST_SHA256 --replay
python3 -B -O /path/to/30002507/verify_publication.py /path/to/30002507 EXPECTED_PUBLICATION_MANIFEST_SHA256 --replay
python3 -B /path/to/30002507/test_publication_integrity.py /path/to/30002507 EXPECTED_PUBLICATION_MANIFEST_SHA256
python3 -B -O /path/to/30002507/test_publication_integrity.py /path/to/30002507 EXPECTED_PUBLICATION_MANIFEST_SHA256
```

Use the publication-manifest digest recorded in the draft PR. The replay runs direct normal and optimized child interpreters, from a relocated temporary package and unrelated working directory, and compares exact outputs. Author controls cover 67,207 finite predicates and 12 damaged packages; independent controls cover 192,572 predicates, 6 mathematical negative cases, and 18 frozen-binding corruptions per mode. These supplement the written analytic proofs; they neither prove all-height zero exclusion nor certify the target.

## Source and publication boundaries

The [2014 publisher question](https://ems.press/content/serial-article-files/46499), printed p.390, was inspected. The exact problem website and missing raw imported statement/prior AI report were not inspected. [Broucke–Vindas v2](https://arxiv.org/abs/2102.08478v2), Proposition 1.4 and Theorem 3.1, supplies credited generalized-series input; its underlying probabilistic theorem is not reproved here. The [Hilberdink–Saias claim](https://arxiv.org/abs/1812.11880) was withdrawn in 2024 with an irreparable error in the main proof, so it is not treated as a resolution. Seip's continuation results are not substituted for ordinary convergence.

Only authored arguments, audit, reproducibility code, safe package files, and public verification metadata are added. Source PDFs, full extracts, images, raw imported records, and private coordination material are excluded. The queue change is limited to this target's Status and Turns; Findings, Chat, DOI, and every other byte are preserved.

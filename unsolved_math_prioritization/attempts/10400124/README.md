# Flat-connection growth exponents: audited partial results

Problem 10400124 (AMR-103-0124), catalog rank 846. This is an AI-authored, independently AI-audited, unrefereed partial-result and formulation note. The full-target gate is **unsolved, 3/5 substantive approaches used**. No general solution or novelty is claimed.

## Verified mathematical scope

- Jeffrey's exact SU(2) formula gives an identically zero grouped zero-Chern-Simons sector for L(25,2), at every integral shifted level r = k + 2 >= 2, including levels divisible by 5. Both signed root-of-unity sums vanish exactly, so this is all-orders cancellation.
- The same argument applies to L(ell^2,q) for primes ell >= 5 with q nonzero and not +/-1 modulo ell. The zero-phase fiber has generic half-cohomology difference -1/2.
- This obstructs the strict requirement of a nonzero amplitude at every classical phase in the original Conjecture 7.7 package. It is **not a counterexample to conditional Conjecture 7.9** when a stipulated nonzero-sector expansion is a hypothesis, nor to a convention allowing absent sectors or assigning formal exponents to zero series.
- For M_g = #^g(S1 x S2), with M_0 = S3, the exact invariant is (sqrt(2/r) sin(pi/r))^(1-g), and the genuine leading exponent is 3(g-1)/2. The calculation includes central, reducible noncentral, and irreducible representations. The normalization is Z(S1 x S2)=1 and Z(S3)=sqrt(2/r) sin(pi/r); S3-normalization shifts nonzero exponents upward by 3/2.
- A conditional component-aggregation lemma identifies the exact noncancellation requirement. It supplies neither general stationary-phase asymptotics nor a general noncancellation theorem.

Read the [author proof](author/proof.md), [scope and literature assessment](author/status.md), [independent audit](audit/audit.md), and [acceptance](audit/acceptance.json). The audit required no correction patch; the author freeze is unchanged.

## Immutable artifacts

| Artifact | Bytes | SHA-256 |
| --- | ---: | --- |
| FLAT_CONNECTION_10400124_AUTHOR_SAFE_FREEZE.zip | 10575 | 232a49f83dd1fc6f79cf82c09a2d8d50fba28a02a716d26ae06f361672b1a172 |
| FLAT_CONNECTION_10400124_INDEPENDENT_AUDIT_SAFE.zip | 11447 | 55c53efe71b18257558d6fc12efb4f38158b9836bfe4de0c559c92d37cbf967a |

Both archives and their external manifests are preserved byte-for-byte. The author/ and audit/ directories are exact, individually hash-checked unpacked copies. Statements such as “pending” or “no publication performed” inside immutable historical artifacts describe their original stage; this wrapper records the later draft-publication stage without rewriting that history.

## Verification and limitations

[PUBLICATION_CHECKS.json](PUBLICATION_CHECKS.json) records fresh archive/member/inventory checks and fresh reruns of the audit-owned diagnostic in five isolated Python modes: normal, optimized, relocated, hostile-import environment, and hostile plus optimized. All five outputs were byte-identical. All ten corruption controls were rejected; exact cyclotomic calculations, all 25 level residues, ten nonzero phases, 284 admissible q-classes over 13 primes, and excluded-q controls were reproduced.

These are data-integrity and exact finite-arithmetic diagnostics, not a formal proof checker. **No executable checker or runner is packaged.** The infinite-family and connected-sum results rest on the written proofs and audit. Source retrieval, visual formula inspection, complete statement/review-pair hashing, and bounded literature searches in the original artifacts are explicitly inherited audit history; the publication check did not repeat them. This is not an exhaustive current-status or novelty search.

Public payloads consist only of authored mathematics, mathematical audit/acceptance, public scholarly citations, and verification metadata. No source PDFs, copied third-party prose, raw corpus contents, private sources, or private coordination files are distributed.

[QUEUE_DELTA.json](QUEUE_DELTA.json) identifies the sole queue changes: this row's Status from queued to unsolved and Turns from 0/5 to 3/5. Every other queue byte is preserved. Canonical corpus/catalog/status files are untouched. Publication is a draft PR only; no merge, release, DOI, or outreach is part of this package. Exact remote-head readback and CI observations are recorded separately after publication; zero reported CI checks must not be called a passing CI run.

## Primary sources

- T. Ohtsuki (ed.), [Problems on invariants of knots and 3-manifolds](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf), Section 7.2, pp. 478-479.
- L. C. Jeffrey, [Chern-Simons-Witten invariants of lens spaces and torus bundles, and the semiclassical approximation](https://webhomes.maths.ed.ac.uk/~v1ranick/papers/jeffrey.pdf), Theorem 3.4 and equation (5.3).
- J. E. Andersen, [The Witten-Reshetikhin-Turaev invariants of finite order mapping tori I](https://arxiv.org/abs/1104.5576v1).
- Andersen and Jorgensen, [On the Witten-Reshetikhin-Turaev invariants of torus bundles](https://arxiv.org/abs/1206.2552v2).
- Andersen et al., [A proof of Witten's asymptotic expansion conjecture for WRT invariants of Seifert fibered homology spheres](https://arxiv.org/abs/2510.10678v1). Its stated degree bound is not a general equality theorem.

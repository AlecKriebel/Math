# Absolute linear Harbourne constants: bounded partial theorem

Problem 30003087 / OWR-14222-015. Status: **UNRESOLVED, 1/5 shared approaches used**; the same approach is shared with broader targets 30003086 and 30004521.

For a prime power q≥4, put N=q²+q+1 and d=N−i. The [complete proof](APPROACH1.md), relative to explicitly cited published inputs, establishes the original source value over all fields for:

- 0≤i≤q;
- i=2q−1;
- i=q+1+a, 0≤a≤q−3, when U_q(a)<L_q(a), where U_q(a)=floor[a(a−1)/(2(q−1))], L_q(a)=q−a for even q, and L_q(a)=ceil[(q−a)(q+1)/(q−1)] for odd q.

This covers the complete stated bands q=4,5,7,8,9,11,13. The q=4,5 bands and q=2,3 values were already known in DHS. The literal q=2 endpoint formula is false and is excluded, with the discrepancy explained. No novelty claim is made.

The first unsettled case **within these bands and this method** is q=16,a=13,d=243; this is not a claim that all d<243 are settled. Gaps between the bands, such as d=32,…,43, remain outside the result. The general conjecture remains unresolved. The proof identifies the exact residual positive-degree-excess realizability obstruction without asserting a counterexample.

The [complete independent mathematical audit](INDEPENDENT_AUDIT.md) accepts this bounded partial theorem. It does not independently certify the entire EMSS paper, worldwide novelty, human peer review or proof-assistant verification.

- [Scoped acceptance](ACCEPTANCE.json) and [status](STATUS.json)
- [Source/claim ledger](SOURCE_LEDGER.md) and [public-source identities](SOURCE_MANIFEST.json)
- [Edition provenance](PROVENANCE.md), [research log](RESEARCH_LOG.md) and [file manifest](MANIFEST.json)

Only authored proof, mathematical review and public-source metadata are included. Source copies, computational materials and private coordination material are excluded.

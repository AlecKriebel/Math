# PR718 / 30004324 research log

## 2026-10-13T03:11:12.267520+00:00 — Mathematical and reproduction checkpoint (estimated PR completion: 20%; overall shard: 3%)

Exact PR head: `8edfe0bf37d07814c5503107b9029e506b6046ea`. Eligibility: status exactly `claimed_solved` at this head, not inferred from the title. Snapshot preserves all 49 attempt files and both author archives. Candidate proof SHA-256: `dcad7d7677b1fff7fe1b659fd5b2f2c97e4daa0f0fe7b914a7752f19ad89c5a8`.

Exact target: smooth integral projective X of dimension n>=1 over an algebraically closed field of arbitrary characteristic; epsilon(T_X;x)>0 at one specified arbitrary closed point implies X is projective n-space. Success requires the full target, with no Fano, nef-tangent, characteristic-zero, or general-point hypothesis added.

Original OWR53/2019 conjecture, printed p.3289, and FM arXiv Conjecture5.9 checked directly. The preprint counterpart Corollary5.6 produces a rational curve through the specified point; Proposition5.8(1) is the established Fano case in arbitrary characteristic. Final journal numbering differs and is being verified directly.

Primary reproduction: `verify_publication.py` with external top-level manifest binding passed normal and optimized Python, including relocated and exact patched reconstructions, author and independent finite controls, integrity mutations and preserved historical adverse finding. Both stdout/stderr receipts are saved. These computations certify packet consistency and finite controls; they do not prove the algebraic geometry.

Independent approach families:

| Family | Mechanism | Evidence/status | Exact remaining gap |
|---|---|---|---|
| Pointed geometry | Global ample-degree minimum, one-marked stable maps, trivial inertia, projective actual evaluation fiber, smooth evaluation | Fresh independent reviewer checking primary foundations, no preliminary fatal gap | Final written verdict pending |
| Picard/Fano | Curve-normalized minimum slope, contracted section, fiberwise line-bundle descent, arbitrary-curve lifting, numerical ampleness, established Fano case | Separate fresh reviewer independently auditing | Final written verdict pending |
| Reproducibility | Exact frozen-file manifest and portable finite controls | Root replay PASS in normal and optimized modes | No geometric inference made from computation |

No result accepted, merged, or submitted to Zenodo. Priority audit and manuscript authoring follow mathematical clearance. Next stage: integrate independent reports, resolve any gaps, then check priority against primary literature.

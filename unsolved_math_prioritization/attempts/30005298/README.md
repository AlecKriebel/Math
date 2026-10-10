# Partial dimension results for general Weddle loci

Problem **30005298 / OWR-11695864-003**, from Luca Chiantini's Question 1 in OWR 54/2022. The original all-parameter problem remains **OPEN**. This AI-assisted, unrefereed proof-only edition contains accepted partial results over C for general distinct points, without a novelty claim.

Let N=binomial(d+n-1,n-1). The target is the reduced closure of centers outside Z where the dimension of degree-d cone forms through Z exceeds its generic minimum.

- For n>=2,d>=2 and N<=r<=N+n-1, the locus is nonempty of dimension n+N-r-1; it is empty for r>=N+n.
- For n>=3,d>=2 and r=N-1, its dimension is n-2.
- In P3, for every d>=2, the complete table is: empty at r=1; dimension 1 for 2<=r<=N-1; dimension 2 at N; dimension 1 at N+1; nonempty dimension 0 at N+2; empty for r>=N+3.
- The elementary P1, degree-one, small-cardinality and P2 regimes are proved, including the exact 3*binomial(r,4) point count for P2 at r=d+2.

The conservative residual is n>=4,d>=2,d+2<=r<=N-2, except values otherwise settled. This is not a claim that every residual case is independently open. No conclusion about the entire determinantal scheme, degree outside the stated elementary P2 case, multiplicity, ACM structure, irreducibility or complete component decomposition is made.

## Included documents

- [PROOF.md](PROOF.md): complete incidence, projective-intersection, common-factor pencil and monotonicity arguments, with every boundary and edge regime.
- [MATHEMATICAL_AUDIT.md](MATHEMATICAL_AUDIT.md): complete substantive independent audit and historical supplementary checks, including adverse mathematical examples.
- [ACCEPTANCE.json](ACCEPTANCE.json): scoped acceptance bound to the exact distributed proof, audit and source review.
- [SOURCE_REVIEW.md](SOURCE_REVIEW.md): source attribution, conditional scheme assertions and the corrected authored reading of Conjecture 5.4.
- [SOURCE_METADATA.json](SOURCE_METADATA.json): public source URLs, PDF hashes and sizes, dated retrieval/inspection history and supplementary match metadata.
- [STATUS.json](STATUS.json): accepted ranges and remaining boundary.
- [MANIFEST.json](MANIFEST.json): eight-file inventory, hashing the other seven members; the draft PR body independently pins the manifest.

## Source and review limits

The [original OWR report](https://doi.org/10.4171/owr/2022/54) and [Weddle schemes, v1](https://arxiv.org/abs/2606.25060v1) supply the definition and projection interpretation. The proof does not assume the latter's Theorem 5.1, Propositions 5.2, 5.3 or 5.6, or Conjecture 5.4. Its conditional ACM and degree claims remain conditional here. The inspected preprint says “expected codimension, namely 2”; an earlier authored dimension reading is withdrawn. All inspected representations agree, with no established source discrepancy or current typo.

Acceptance is an AI-assisted mathematical audit, not external human peer review, journal acceptance or formal proof-assistant certification. Historical finite certificates are supplementary and the universal proofs do not depend on them. Programs, generated certificates, raw outputs, datasets, copied source documents/text/images and private coordination material are excluded. Edition preparation rechecked byte identities and publication integrity without new scholarly retrieval, source-text inspection, literature search or mathematical-program reruns. QUEUE.md and unrelated repository content remain unchanged.

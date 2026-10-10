# GREEN-012 / ID102: audited computer-assisted partial result

**Accepted partial scope; unrestricted target unresolved.** This is an unrefereed AI-assisted exposition and independent internal AI mathematical, source, and computational audit. “Accepted” describes that internal audit, not external human peer review, journal acceptance, or formal proof-assistant certification. No novelty-priority claim is made.

## Exact result

For every finite abelian group \(G\), with \(N=|G|\), and every subset \(A\) of density \(\alpha\geq20/23\), the number of ordered tuples
\((x_0,\ldots,x_4,y_0,\ldots,y_4)\in G^{10}\) satisfying
\(x_i+y_{i+j}\in A\) for every \(i\in\mathbb Z/5\mathbb Z\) and \(j\in\{0,1,2\}\) is at least \(\alpha^{15}N^{10}\). Coordinates may coincide. No asymptotic error, cyclic-group restriction, prime-order restriction, or Fourier-uniformity hypothesis is used.

The stronger exact criterion is \(F(r)\leq5\), for \(r=(1-\alpha)/\alpha\leq1\) and \(0<\alpha<1\), with \(F\) defined in the full proof. The approximate endpoint \(0.86946194679\) is explanatory only. The exact rational endpoint is \(20/23\).

The proof also establishes subgroup-coset and complement-of-coset cases and quotient/product closure. Independent exact enumeration checked every subset of the 25 abelian group types of order at most 16: 398,350 subsets, with no violation. That bounded-order result does not extend itself to arbitrary group order or solve the unrestricted problem.

## Computer-assisted dependency and reproduction boundary

The all-group high-density theorem has a **load-bearing computer-assisted classification** of the fixed graph's 624 nonempty leaf-free subgraphs among its 32,768 edge subsets. A separate local checker reconstructed the graph and verified every witness. This is not a hand classification or a universal conclusion drawn from searching small groups.

The full substantive proof and audit are included. The code, machine-readable witnesses, certificates and raw computational data are excluded from this publication scope. Consequently this prose-and-hash packet is **not a standalone executable or publicly reproducible machine-checkable proof**. The audit documents independent local verification, and the metadata records the identities and scope of those retained materials. Hashes do not substitute for their contents.

## Source interpretation

The modulo-5 reading of [Green's Problem 12, page 9](https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf) is qualified as a [publicly reported author clarification](https://leanprover-community.github.io/archive/stream/252551-graph-theory/topic/Sidorenko%27s.20Conjecture.20and.20Green%27s.20Open.20Problem.2012.html). The inspected PDF does not explicitly print that convention. No private correspondence or amended-PDF claim is made.

The needed three-function inequality is proved in the manuscript and related to [Lovász, *Subgraph densities in signed graphons and the local Sidorenko conjecture*, Lemma 2.3](https://arxiv.org/abs/1004.3026). The neighboring [Deng–Tidor–Zhao paper](https://doi.org/10.1017/S0305004125000106) concerns Green's Problem 13, not a negative solution of Problem 12. Recorded source-inspection scopes, public URLs, PDF byte counts and hashes appear in SOURCE_METADATA.json and AUDIT.md. Edition preparation added no source retrieval, source inspection or literature search.

## Reading order and edition history

- RESULT.md gives the short result and its boundary.
- PROOF.md contains the complete accepted proof with the exact delimiter-only correction applied.
- AUDIT.md preserves the complete independent audit verbatim.
- TYPESETTING.patch is the exact supplied presentation patch, applied to isolated copies of the original public/PROOF.md and public/RESULT.md. It repairs inline delimiters and changes no mathematical text or displayed equations.
- ACCEPTANCE.json records exact acceptance scope and explicit exclusions.
- VERIFICATION_METADATA.json preserves candidate verification metadata with its status updated; AUDIT_VERIFICATION_METADATA.json preserves audit metadata verbatim.
- SOURCE_METADATA.json is unchanged. VERIFICATION_SUMMARY.md explains the recorded verification boundary.
- MANIFEST.json lists all eleven packet members and hashes the other ten; its own digest is recorded separately in the exact publication allowlist.

The only additional edits are acceptance/status framing. Sealed originals are unchanged. The public packet contains authored prose, the authored correction patch, audit, acceptance and public source/verification metadata, with no copied third-party documents, executable code, raw data, machine-readable certificates, private sources, private personal data or private coordination material.

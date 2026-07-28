# Second hostile release audit: order-13 parameter three

Date: 2026-07-28 PDT

## Verdict

**UNCONDITIONAL PASS — no additional publication blocker found.**

This review is bound to release tag
`gamma-theta-order13-k3-v1.0.0` (commit
`883e796cb163f360d8052e94ae507d3cbb3e6599`) and to the exact manuscript
and PDF hashes in `evidence.json`.

The paper's main theorem is stated at exactly the certified scope:

> No finite simple graph on 13 vertices satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).

It does not claim a complete order-13 exclusion, an all-order
parameter-three theorem, or a resolution of the universal conjecture.
Parameters four and five at order 13 remain explicitly open.

## Mathematical audit

The proof's reductions and branch composition were checked directly from
the final source.

- The paper uses the standard one-guard-moves model: only unoccupied
  vertices are attacked, one occupied adjacent guard moves, and the
  one-swap successor is retained and dominating.
- The parameter chain correctly turns the theorem hypothesis into
  \(\gamma=i=\alpha=\gamma^\infty=3\).
- The maximum-independent-state argument correctly places the chosen
  independent triple in every eternal family of triples.
- The restoration, frozen-projection, singleton-safety,
  two-response-replication, physical-representative, and pure-signature
  doubling arguments are valid under the stated hypotheses. In
  particular, the frozen projection explicitly proves both closure and
  domination of every projected two-state before invoking the
  parameter-two theorem.
- For the chosen independent triple, every outside response list is
  nonempty. The full-list and no-full-list cases are therefore exhaustive.
- In the no-full branch, two distinct exact two-list types yield four
  distinct named nonneutral vertices with the stated pure signatures.
  The four-neutral certificate gives \(|Q|\leq3\), and the residual
  signature normalization then covers every remaining candidate.
- The main order-13 \(k=3\) theorem is unconditional on the published
  lower-order results. The later \(k\in\{4,5\}\) corollary is correctly
  labeled as relative to the through-order-11 and separately certified
  order-12 premises.

The corrected historical paragraph accurately distinguishes the original
Klostermeyer--MacGillivray assertion, the gap identified and explicit
question posed by Klostermeyer--Mynhardt, and the later
\(\gamma\)--\(\theta\) terminology. Alec Kriebel is identified consistently
as author and project lead. Heavy ChatGPT assistance and the lack of
external peer review are disclosed without ambiguity.

## Certificate and coverage bindings

All decisive artifact bytes still match the manuscript:

| branch | variables | clauses | instance SHA-256 | proof SHA-256 |
|---|---:|---:|---|---|
| full response | 9,802 | 85,409 | `d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13` | `653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910` |
| four neutral | 1,222 | 24,694 | `3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0` | `c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee` |
| residual no-full | 9,802 | 84,614 | `76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1` | `c985ce0a602a91a0d323594e3aeecf210fa5131027ef4b6c9b6e4d4b628f1848` |

The addition-only four-neutral and residual proofs contain respectively
78,697 and 156,205 lines, contain no deletion records, and end in the empty
clause. The existing independent results record byte-identical formula
reconstruction, strict RUP replay, the six anchor permutations, all 1,716
sorted residual signature multisets, the sharp three-neutral equality
control, and the satisfiable theta-gap ablation.

The full-response positive-control graph6 string is correctly escaped in
the TeX source as `LF\|ul\XzVsaqJ`; the three-neutral control is
`LDZZa^g|fkw[iH`.

## Release artifact audit

A fresh deterministic build in an isolated temporary directory reproduced
the tagged PDF byte for byte:

`6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4`

The final log contains no undefined references, TeX errors, overfull boxes,
or underfull boxes. The PDF has 10 letter-size pages, author metadata
`Alec Kriebel`, the correct title and subject, no encryption, no forms, no
JavaScript, and no suspicious embedded content. The public-site PDF is
byte-identical to the manuscript PDF.

No additional release defect was found.

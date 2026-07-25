# Graph-class restriction audit

## Purpose and current status

This file prevents provisional literature recollections from silently becoming
search axioms.  None of the rows marked `PENDING` below should be used to claim
complete coverage or to exclude a graph from a certified search until a
primary-source audit records:

1. the exact theorem statement and graph conventions;
2. that the parameter is the standard **one-guard-moves**
   \(\gamma^\infty\);
3. whether attacks are restricted to unoccupied vertices (or an explicitly
   proved equivalent convention);
4. whether the conclusion is unconditional
   \(\gamma^\infty=\theta\), or only the implication
   \(\gamma=\gamma^\infty\Rightarrow\gamma=\theta\);
5. the meaning of class terms such as \(C_4\)-free (subgraph-free versus
   induced-\(C_4\)-free), planar, and series-parallel.

The logical translations in the last column are elementary and valid **if**
the source theorem in the middle column is verified.

| Class/restriction | Status | Exact source statement still required | Conditional consequence for a counterexample |
|---|---|---|---|
| Perfect graphs | `VERIFIED-MATHEMATICALLY`; historical source pending | No class-specific eternal-domination theorem is needed: perfection gives \(\alpha(G)=\theta(G)\), contradicting the strict counterexample gap | Exclude perfect graphs directly. |
| Circular-arc graphs | `PENDING` | Verify whether every circular-arc graph satisfies \(\gamma^\infty=\theta\), and locate the primary proof rather than a survey assertion | Exclude circular-arc graphs. |
| Series-parallel / \(K_4\)-minor-free graphs | `PENDING` | Verify the precise class equivalence used by the source and whether the theorem is unconditional \(\gamma^\infty=\theta\) | Exclude the verified class. |
| Outerplanar graphs | `PENDING` | Verify the primary theorem and whether it is subsumed by the audited \(K_4\)-minor-free theorem | Exclude outerplanar graphs; do not count this as an independent restriction if already subsumed. |
| Subcubic graphs | `VERIFIED-PRIMARY` | Klostermeyer--Mynhardt (2015), Theorem 6.3: if \(\Delta(G)\leq3\) and \(\gamma=\gamma^\infty\), then \(\gamma^\infty=\theta\); isolated vertices are removed in the proof | Deduce \(\Delta(G)\geq4\). |
| \(C_3\)-free / triangle-free graphs | `VERIFIED-PRIMARY` | Klostermeyer--Mynhardt (2015), Theorem 6.6: if \(G\) is triangle-free and \(\gamma=\gamma^\infty\), then \(\gamma^\infty=\theta\) | Deduce that a counterexample contains a triangle. |
| \(C_4\)-free graphs | `PROVISIONAL` | Taletskii cites an unavailable Klostermeyer--Krop--MacGillivray 2018 manuscript; in Taletskii's terminology, \(C_4\)-free means no \(C_4\) subgraph | Do not use as a hard filter; a 4-cycle remains only a literature-supported lead. |
| Planar graphs (current theorem) | `VERIFIED-PRIMARY-STATEMENT`; proof audit pending | Taletskii, arXiv:2412.20120v2, Theorem 3: every planar \(G\) with \(\gamma=\gamma^\infty\) has \(\gamma^\infty=\theta\), in the one-guard model | Deduce nonplanarity only subject to the outstanding adversarial audit of the long preprint proof. |

## Conditional combination

Once the last four relevant rows have been verified in their required forms,
the deductions combine as follows:

> If every planar, subcubic, triangle-free, and \(C_4\)-free graph satisfying
> \(\gamma=\gamma^\infty\) also satisfies \(\gamma=\theta\), then every
> counterexample is nonplanar, has maximum degree at least \(4\), contains a
> triangle, and contains a \(4\)-cycle (with “contains” interpreted according
> to the audited \(C_4\)-free definition).

This paragraph is a conditional implication, not yet an accepted campaign
claim.

## Audit hazards

- A theorem about \(\gamma_m^\infty\), \(\gamma_{\rm all}^\infty\), mobile
  eternal domination, eviction, total domination, or connected domination
  cannot fill any row.
- A finite computation on a graph class cannot be promoted to an all-orders
  theorem.
- “Series-parallel” is used with more than one convention in the literature.
  Record the source's convention before deriving redundancy with outerplanar
  graphs.
- A theorem for induced-\(C_4\)-free graphs would yield a stronger and
  differently worded witness condition than a theorem for graphs containing
  no \(C_4\) subgraph.  Do not blur them.
- If the planar result is only announced, accepted, or computational, record
  that status exactly; only a complete checkable proof supports the universal
  filter.

# Final hostile review: order-13 parameter-three manuscript

Date: 2026-07-28 PDT

## Verdict

**PASS — unconditional, with no additional publication blocker found.**

The tagged manuscript and certificate package support exactly the stated
finite theorem:

> No graph \(G\) on 13 vertices satisfies
> \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\).

The universal \(\gamma\)--\(\theta\) conjecture remains unresolved.  The
paper correctly leaves the order-13 parameters four and five open and does
not claim an all-order parameter-three result.

This review is bound to release tag
`gamma-theta-order13-k3-v1.0.0`, commit
`883e796cb163f360d8052e94ae507d3cbb3e6599`.  The tagged manuscript source
and PDF are byte-identical to the reviewed working-tree copies.

## Mathematical audit

I checked every displayed theorem and proof in `main.tex` against the exact
one-guard model.

- The parameter chain, forced-independent-state lemma, and
  induced-subgraph monotonicity argument are valid.  The latter correctly
  maximizes occupancy in the induced subgraph, preventing a response from
  entering it from outside.
- The odd-antihole attack sequence uses only unoccupied attacks and one
  adjacent guard.  Together with the Strong Perfect Graph Theorem it proves
  the parameter-two lemma in the required one-guard model.
- The restoration lemma is valid because independence of the anchor triple
  prevents an already restored anchor guard from answering a later anchor
  attack.
- In the frozen-projection lemma, restoration prevents the frozen anchor
  from moving.  The current tagged text also explicitly proves that each
  projected two-state dominates the induced graph.  Thus the use of the
  parameter-two theorem to obtain a bipartite complement is justified.
- The singleton-safety, at-least-two-types, two-response-replication,
  physical-representative, and pure-signature-doubling proofs were checked
  line by line.  Every attack is unoccupied; every prohibited move is
  prohibited by a complement edge or a nondominating successor; and every
  forced response is one guard traversing a graph edge.
- The full/no-full division is exhaustive because every response list at
  the retained independent triple is nonempty.  A full list is covered by
  Theorem 4.1, while all remaining lists have size at most two and are
  covered by the no-full reduction and residual certificate.

Theorem 1.1 has **no hidden dependence on lower-order enumeration**.  Its
assembly uses only the universal preliminary lemmas and the three
order-13 certificates.  Lower-order results appear only in the explicitly
relative Corollary 7.1.

Corollary 7.1's remaining set \(\{4,5\}\) is justified.  Parameter one is
excluded by the equality collapse \(\alpha=1\), which makes the graph
complete; parameter two is excluded by Lemma 2.6; and parameter three is
excluded by Theorem 1.1.  The through-order-12 exclusions make any
order-13 counterexample minimum-order, so the companion
no-simplicial-vertex theorem yields connectedness and minimum degree at
least two.  McCuaig--Shepherd then gives
\(\gamma\le\lfloor 2(13)/5\rfloor=5\); its seven exceptions have orders
four and seven and are irrelevant.  The word “Relative” in the corollary
correctly records these dependencies.

## Certificate, coverage, and model audit

The independent checker in this directory verified the exact CNF headers,
clause counts, byte sizes, variable ranges, proof-line counts, terminal
empty clauses, hashes, frozen replay verdicts, and tagged bytes.

The three decisive formula/proof pairs match the manuscript:

| branch | variables | clauses | formula SHA-256 | proof SHA-256 |
|---|---:|---:|---|---|
| full response | 9,802 | 85,409 | `d5a2f17ad6e61cb7ca5cb9d2930b6a0738fec32ee1d9956207dc67bb297dcb13` | `653b01e904b97c01bfa25fbbea29fbadee603918dbaff0ea41b7ad09460fb910` |
| four neutral | 1,222 | 24,694 | `3d1a1379eb2a90ffd399e5a830b1a81881ed527c6e9db06574a390085cb5c1e0` | `c4f1989ac80474a86b75ba939e494bde5928b2727fd61297eb695f3937222eee` |
| residual no-full | 9,802 | 84,614 | `76ff2768c7afd95ee535f8684515b0b15319b1f5ca69085447a1f7eba66393e1` | `c985ce0a602a91a0d323594e3aeecf210fa5131027ef4b6c9b6e4d4b628f1848` |

The addition-only proofs have exactly 78,697 and 156,205 lines,
respectively, contain no deletion lines, and end in the empty clause.  The
already independent branch checkers report clean-room byte reconstruction
and RUP-only replay with zero RAT lemmas.  The compact C097 aggregate replay
was freshly rerun by a separate reviewer and passed; this audit binds that
result to the same proof bytes.

The formula semantics are in the correct graph direction:

- edge variables encode \(H=\overline G\);
- no \(K_4\) in \(H\) enforces \(\alpha(G)\le3\);
- an outside common \(H\)-neighbor for every pair enforces
  \(\gamma(G)\ge3\);
- closure obligations concern only \(r\notin D\);
- each response selector names one occupied guard, requires a \(G\)-edge,
  and retains the unique one-guard successor; and
- the complete anchored coloring bank proves
  \(\chi(H)=\theta(G)>3\), not a coloring assertion about \(G\).

The full-response sorter is sound under the residual \(S_9\) action.  In
the no-full branch, two ordered distinct response types have six anchor
normalizations.  Their pure-signature pairs occupy four named nonneutral
vertices; the neutral bound leaves at most three neutral vertices among the
six residual labels.  Sorting those labels covers all
\(\binom{13}{6}=1,716\) signature multisets, and requiring the fourth sorted
signature (label 10) to be nonzero is exactly the at-most-three-neutral
condition.  No candidate orbit is omitted.

I independently decoded and evaluated both displayed graph6 controls:

- `LF\|ul\XzVsaqJ` has
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\) and 157 states in
  its greatest eternal triple-family.
- `LDZZa^g|fkw[iH` has the same parameter tuple and 139 states in its
  greatest eternal triple-family.

Thus both graph6 records and their reported statistics are correct.

## Attribution, scope, and publication integrity

The revised history is accurate against the retained primary sources:
Klostermeyer--MacGillivray (2009) asserted the implication;
Klostermeyer--Mynhardt (2015) identified the gap and reopened it as an
explicit question; MacGillivray--Mynhardt--Virgile (2022) describes the
later conjectural formulation as the \(\gamma\)--\(\theta\) conjecture and
reports the through-order-11 computation.  Bibliographic metadata and DOI
records in `references.bib` are consistent with the local audit.

Alec Kriebel is identified as author and project lead.  The disclosure
plainly states heavy ChatGPT 5.6 Sol assistance, no outside expert review,
and that certificate checking is not peer review.  The manuscript makes no
priority overclaim.

The tagged PDF has SHA-256
`6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4`.
It is a ten-page, unencrypted Letter PDF with no forms, author metadata
`Alec Kriebel`, and the correct title.  The final log has no LaTeX warning,
undefined-reference, overfull/underfull-box, or fatal-error report.  I
rendered and visually inspected all ten tagged pages: equations, tables,
hashes, graph6 strings, citations, page numbers, and disclosure text are
legible, with no clipping, collision, missing glyph, or placeholder.

## Reproduction

From the campaign directory:

```text
python3 -I -B -W error reviews/order13_k3_manuscript_hostile/checker.py
```

The checker uses independent ordinary-set, complement-coloring, and
greatest-fixed-point code for the two graph controls; it does not import a
search generator.

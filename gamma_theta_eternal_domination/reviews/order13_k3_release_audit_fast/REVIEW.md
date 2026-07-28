# Fast hostile release audit: order 13, parameter three

## Verdict

**PASS.** I found no publication-blocking mathematical, computational,
reproducibility, attribution, disclosure, or rendering defect in the exact
audited manuscript bytes:

- `paper/order13_k3_complete/main.tex`:
  `56afff0796fb602589d38714793e42b6864a5454d71d8da51b559daa3daea8f2`
- `paper/order13_k3_complete/main.pdf`:
  `6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4`

An initially detected historical-attribution error was corrected before this
verdict. The current text accurately says that Klostermeyer--Mynhardt (2015)
identified the gap in the 2009 argument and reopened the implication as an
explicit question, while subsequent literature uses the
\(\gamma\)--\(\theta\) name.

## Exact theorem and dependency audit

The paper proves only
\[
  \nexists\,G,\quad |V(G)|=13,\qquad
  \gamma(G)=\gamma^\infty(G)=3<\theta(G).
\]
It repeatedly and correctly leaves open order-13 parameters four and five,
parameter three at arbitrary order, every parameter at order 14, and the
universal conjecture.

The proof of Theorem 1.1 has no hidden dependence on the through-order-11
enumeration or the order-12 certificates. Its dependency chain is:

1. the general parameter chain and independent-state forcing;
2. the certified full-response exclusion C-090;
3. for no-full lists, the human response-list/projection lemmas;
4. the four-neutral certificate C-096; and
5. the normalized residual certificate C-097.

The full/no-full split is exhaustive because every outside response list is
nonempty, and therefore is either the full three-list or has size at most two.
Lower-order results enter only Corollary 7.1. That corollary is explicitly
conditional on the published through-order-11 result and the separately
certified order-12 theorem; under that premise an order-13 counterexample is
minimum-order, so the cited minimum-counterexample structural bound and the
order-13 domination bound leave exactly \(k=4,5\).

## One-guard semantic audit

I checked every human attack argument in the parameter-chain proof,
independent-state forcing, odd-antihole lemma, restoration lemma, frozen
projection, singleton safety, two-response replication, and pure-signature
doubling.

In every case:

- the attacked vertex is unoccupied in the displayed state;
- a response replaces exactly one occupied guard by the attacked vertex;
- a claimed legal move uses adjacency in \(G\);
- moves excluded as impossible are either nonadjacent or lead to a
  nondominating/nonretained successor; and
- no argument silently uses occupied-vertex attacks or simultaneous guard
  motion.

The CNF descriptions agree with the same model. A true response variable names
one occupied guard and one unoccupied attack; multiple true selectors encode
alternative single-guard moves, not a simultaneous move.

## Certificate, census, and hash binding

All headers, sizes, and hashes match the paper, `CLAIMS.md`, and
`results/order13_k3_complete_acceptance.json`.

| Claim | Variables | Clauses | Instance SHA-256 | Decisive proof |
|---|---:|---:|---|---|
| C-090 full response | 9,802 | 85,409 | `d5a2f17a...cb13` | 19,874,489 bytes, `653b01e9...b910` |
| C-096 four neutral | 1,222 | 24,694 | `3d1a1379...c1e0` | 78,697 additions, no deletions, `c4f1989a...2eee` |
| C-097 residual | 9,802 | 84,614 | `76ff2768...93e1` | 156,205 additions, no deletions, `c985ce0a...1848` |

Both addition-only proofs end in the empty clause. The residual category census
sums to 84,614. The six anchor permutations cover every ordered pair of
distinct types; the residual sort covers exactly
\(\binom{13}{6}=1,716\) signature multisets, including ties; and label 10 is
nonzero exactly when at most three of the six residual vertices are neutral.

I independently decoded and evaluated both printed Graph6 controls:

- `LF\|ul\XzVsaqJ` has
  \((\gamma,i,\alpha,\gamma^\infty,\theta)=(3,3,3,3,3)\), with all 157
  dominating triples in its greatest eternal triple-family.
- `LDZZa^g|fkw[iH` has the same five parameters, with 139 dominating triples
  and a 139-state greatest eternal triple-family. Its independent nauty
  canonicalization is `L][DKgF@zZjum{`, exactly the canonical string in the
  acceptance record.

The advertised replay files all exist at the stated campaign-relative paths.
The paper accurately distinguishes the compact C-097 no-full aggregate replay
from the separately listed C-090 full-response checker.

## Citations, disclosure, and limitations

The bibliography metadata and substantive attributions checked against the
retained primary sources are accurate. In particular:

- the 2015 source explicitly identifies the error in the 2009 proof and asks
  the counterexample-form question;
- MMV (2022) calls the later formulation the
  \(\gamma\)--\(\theta\) conjecture and reports no counterexample through
  order 11;
- the Strong Perfect Graph Theorem citation supports Lemma 2.6; and
- the McCuaig--Shepherd exceptions have orders four and seven, so its
  \(2n/5\) domination bound applies at order 13.

The manuscript clearly discloses heavy ChatGPT 5.6 Sol assistance, human
authorship and direction, lack of external expert review, the distinction
between certificate checking and peer review, and the lack of a worldwide
priority claim.

## Build and PDF QA

Two fresh isolated builds using

```text
SOURCE_DATE_EPOCH=1785231600 tectonic --keep-logs --keep-intermediates main.tex
```

were byte-identical to each other and to the distributed PDF. All three hashes
were
`6768cecf0d46672f7d56cbda2715b49ef18470e5d60b3c7912fc9999843ae5a4`.
Both builds had empty stderr. The final log has no undefined
citations/references, overfull or underfull boxes, or TeX/package warnings.

PDF metadata correctly records the title, Alec Kriebel as author, the intended
subject and keywords, deterministic creation time, ten letter-size pages, no
encryption, and no JavaScript. Rendering all ten pages at 140 dpi found no
clipping, overlap, malformed hash/Graph6 text, broken table, missing glyph, or
other visual defect.

## Release gate

The advertised remote tag `gamma-theta-order13-k3-v1.0.0` did not yet exist
during this pre-release audit. This is an expected operational gate, not a
manuscript defect: commit the audited source, PDF, certificates, replay
programs, and review evidence, then create and push that exact tag before
making the PDF public. The paper must not be published while its claimed
frozen-tag link is unresolved.

Machine-readable details and the read-only checker are in `evidence.json` and
`audit.py`.

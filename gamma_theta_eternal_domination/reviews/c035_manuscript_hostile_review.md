# Hostile review of the C-035 manuscript

**Verdict: ACCEPT.** I found no mathematical, certificate-binding, citation,
scope, reproducibility, or layout blocker in the reviewed bytes.

## Bytes reviewed

- `paper/c035_order12_k3/main.tex`  
  SHA-256
  `dddf4a1b4aebed71a1f44a7f30b39b2c5855e72fd797bd4439283d358e122204`
- `paper/c035_order12_k3/main.pdf`  
  SHA-256
  `f84430ee4319a3c914cfe4f6182cf62d9fc840d26e8d0501b863bd2cc995864e`

Two clean builds with

```text
SOURCE_DATE_EPOCH=1785047581 tectonic --keep-logs --keep-intermediates main.tex
```

produced PDFs byte-identical to each other and to the retained PDF. The logs
contain no actual warning, error, undefined-reference, overfull-box, or
underfull-box report. I rendered and visually inspected all nine pages; I found
no clipping, collision, broken table, unreadable path or hash, or other layout
defect.

## Adversarial findings

1. **Claim and scope.** The proved claim is exactly the certified finite slice:
   no graph of order 12 has
   \(\gamma(G)=\gamma^\infty(G)=3<\theta(G)\). The proof covers disconnected
   graphs. It explicitly does not claim the \(k\geq4\) slice, any order at least
   13, verification through order 12 for all parameters, or resolution of the
   universal conjecture.

2. **Model.** The definition and encoding use attacks only at unoccupied
   vertices, move exactly one guard along one edge, require the successor
   configuration to be selected, and require every selected configuration to
   dominate. No all-guards-move theorem or transition rule is imported.

3. **Human-readable proof.** The parameter chain, induced-subgraph
   monotonicity, component additivity, minimum-parameter argument, odd-hole /
   odd-antihole reduction, odd-wheel exclusion, and exhaustive
   \(C_5,C_7,C_9\) template split are sufficient and noncircular. The
   disconnected case is not silently assumed away: additivity and the common
   total value three force any gap-bearing component to carry the entire
   parameter.

4. **Encoding and counts.** The common variable count is correctly
   \(66+660+220+5940=6886\). The manuscript's formula statistics agree with
   the accepted C-035 artifacts:

   | branch | clauses | literals | CNF bytes | proof additions | proof bytes |
   |---|---:|---:|---:|---:|---:|
   | \(C_5\) | 23,968 | 192,169 | 754,323 | 247,981 | 6,337,621 |
   | \(C_7\) | 21,718 | 148,551 | 621,864 | 284,317 | 18,093,724 |
   | \(C_9\) | 20,200 | 117,841 | 530,053 | 4,705 | 65,906 |

   I checked every printed CNF/proof hash and every Appendix path against the
   accepted artifacts. The pinned `drat-trim` hash, accepted commit, source/run
   revision, and twelve run-artifact hashes also agree with the acceptance
   record.

5. **The \(C_9\) subtlety.** The \(C_5\) and \(C_7\) branches use complete
   coloring banks of 3,645 and 1,701 clauses. The \(C_9\) formula contains only
   the 170 recorded valid coloring cuts. The manuscript now states this
   accurately: the abstract says “valid coloring clauses implied by the
   obstruction,” Remark 4.2 disclaims completeness, and Lemma 4.1 needs only
   the sound direction that every non-three-colorable target satisfies every
   appended valid clause. No completeness of the 170-row list is used.

6. **Proof certificates and replay.** The reported C-035 proof formats,
   addition counts, deletion handling, strict RUP status, final empty clauses,
   and checker division agree with the accepted records. Appendix A gives the
   correct fail-closed full-replay command and correctly distinguishes
   `PASS_FULL_C035_REPLAY` / `CERTIFIED-FINITE` from the metadata-only fast
   mode's `NO_MATHEMATICAL_CLAIM`. I ran the fast metadata audit and obtained
   `PASS_METADATA_ONLY`; as instructed, I did not repeat the full proof replay.

7. **Citations and provenance.** The cited sources support the uses made of
   them, including the original statement, later identification of its gap,
   the order-11 computational frontier, the planar preprint, the Strong Perfect
   Graph Theorem, and DRAT checking. I found no one-guard/all-guards variant
   confusion. The AI-assistance disclosure is unusually clear and does not
   substitute model output for checked evidence.

## External-submission gate

There are no remaining research blockers. Before external submission, the two
deliberate placeholders must be replaced:

1. supply the author metadata; and
2. insert the permanent public archive identifier in the data-availability
   statement.

These are administrative release requirements, not defects in the certified
finite theorem.

# Clarified K2P and K3P theta-trinet collision package

This is the public clarification revision of the exact K2P/K3P tree--theta-trinet collision package. It makes the displayed-tree edge placement and the derivation of the four-switching matrix `M` explicit. No mathematical parameter, theorem, rank calculation, continuous-time result, or K3P result has changed.

The source authors have been contacted and are auditing the construction. This remains a provisional research package; no journal or arXiv submission has occurred.

## Replay

Only Python 3 and the standard library are needed.

```bash
python3 verify_k2p_simple.py
python3 verify_k2p_displayed_trees.py
python3 verify.py
```

The graph-based verifier first applies the same descendant-label rule to an exact rational 3-sunlet test and reproduces the five Fourier coordinates written explicitly in Lemma 4.1 of the source paper. It then begins with the rooted arc list and the explicit endpoint-to-vector placement. For each retained-parent choice it deletes the two unselected reticulation arcs, computes labelled descendants, derives the Fourier edge labels and core monomial, and independently performs ordinary-state Markov pruning. Successful output includes:

```text
[source convention] PASS  descendant-label rule reproduces all five explicit 3-sunlet coordinates of Lemma 4.1
[displayed trees] PASS  four monomials reconstructed from retained edges
[direct pruning] PASS  all 64 network/tree probabilities agree exactly
ALL DISPLAYED-TREE CHECKS PASSED
```

The complete replay ends with `ALL EXACT CHECKS PASSED`.

## Main files

- `k2p_displayed_tree_clarification.tex` / `.pdf`: compact two-page clarification note.
- `combined-paper-clarified.tex` / `.pdf`: revised unified paper.
- `technical-summary-clarified.tex` / `.pdf`: revised two-page summary.
- `verify_k2p_displayed_trees.py`: exact source-convention, graph-reconstruction, and direct-pruning verifier in `Q(sqrt(71))`.
- `verification_report_displayed_trees.txt`: transcript of the new focused audit.
- `verification_report_complete.txt`: transcript of the complete suite.
- `SOURCE_CONVENTION_CROSSCHECK.md`: the five-formula Lemma 4.1 convention audit.
- `CHANGELOG.md` and `PROVENANCE.md`: precise revision and public-history records.
- `manifest.sha256`: hashes of the released files.

The pre-clarification paper, summary, certificates, and original verifier modules remain in the parent directory. Its navigation and provenance files were updated to identify this clarification.

# Reviewed prior-literature response: canonical basepoints

Problem 11000020 / AMR-109-0020, Farb Problem 2.19. Current disposition: **already_solved, 1/5**, in the scope-qualified sense described below. Date: 2026-10-03.

## Accepted response and credit

Prior literature refutes the explicit nilpotent uniqueness example. MSSV's 2002 classification gives at least four distinct genus-9 surfaces whose **full holomorphic automorphism groups** are nilpotent of order 128. The classical nilpotent bound makes 128 maximal in that genus. The checked implication and an elementary reconstruction of the upper bound are in [RESULT.md](RESULT.md).

Prior literature also supplies the requested kind of positive automorphism-theoretic criteria. Reyes-Carocca–Speziali, Theorem 3.1, gives uniqueness from the existence of an automorphism subgroup of order 3g for odd g>=3 except g=21, and of order 3g+3 for even g>=4 with g not congruent to 2 modulo 3. These are subgroup-existence conditions, not assertions that the full group has those exact orders.

This is a credited prior-literature response, not a new discovery. The label does not claim exhaustion of the open-ended canonical-basepoint programme. There is no least-counterexample-genus claim, exact count of all nilpotent maximizers, new classification, or Hurwitz-surface counting result.

## Independent review

The separate [review](review/REVIEW.md) passes the negative certificate and accepts a scope-qualified prior-literature resolution for this concrete record. Its final assessment withdraws an initial provisional partial recommendation that had imposed an unstated requirement to exhaust the research programme. The positive criteria remain subject to their precise genus restrictions. No definite additional requested subproblem was identified by the final review.

- Frozen author commit: 1792dcf4b4a04fc072d6f311cb349de6c1c5052a
- Author manifest SHA-256: 441c21fe437955edfaedf0a13f32c25115d1ce1cc0f849c2e4a5b8c1b3941794
- Review manifest SHA-256: a65c535c7cdc26fb9e3e1ed2ff6c90f1691a41a42e41778243d35c0df432e870
- Author controls: 69 assertions, exact output replay
- Independent controls: 115 assertions, exact output replay

The nine author files and seven review files are preserved unchanged. Statements that review is pending in the frozen author packet describe its historical state and are superseded by this supplement. The historical 1/5 author-turn count is unchanged; review consumed no author turn.

## Evidence limits

MSSV's published existence/fullness classification is an explicit dependency. The author and reviewer did not reconstruct its BRAID computation. The arithmetic controls supplement proofs and source inspection; they do not prove that classification. The original 1985 Zomorrodian PDF was unavailable, while the later primary theorem statement and the direct upper-bound reconstruction were checked. The exact Farb primary page was checked despite the live UnsolvedMath retrieval failure.

OpenAI tools assisted source research, drafting, and independent mathematical review. This is an AI-assisted, unrefereed record, not formal verification or external human peer review.

## Reproduction

Run `python3 verify.py` for the author arithmetic controls. Run `python3 replay_review.py --source-dir /path/to/source-pdfs` for the complete frozen independent suite. Supply the six files with the exact names and hashes in source_manifest.json; they can be retrieved from its public primary-source links. This wrapper stages the original sibling-directory layout without changing any frozen file. Raw PDFs are not included in the repository.

Without `--source-dir`, the wrapper checks all frozen author and review bindings and replays the 69 author assertions, while explicitly reporting that the source-dependent 115-assertion suite was not run.

# Circular assume–guarantee reasoning for linear systems

**30001199 / OWR-3394-009: already_solved, 3/5 substantive author turns. Independent review PASS for a complete alternative proof of the exact source-model theorem.**

Kerber and van der Schaft already stated the affirmative rule as Theorem 4 of *Compositional analysis for linear systems* (2010), DOI [10.1016/j.sysconle.2010.08.002](https://doi.org/10.1016/j.sysconle.2010.08.002). This packet credits that published conclusion and supplies a complete replacement proof. It makes no claim of first theorem discovery or historical novelty of the proof mechanism.

## The result

For finite-dimensional continuous-time LTI systems with freely varying auxiliary disturbances and full linear simulation relations, the two closed-feedback premises

- P1||Q2 is simulated by Q1||Q2
- Q1||P2 is simulated by Q1||Q2

imply that P1||P2 is simulated by Q1||Q2. Feedback is u1=-y2, u2=y1, and the ordered output pair is observed. The construction covers all initial states and every implementation disturbance, without injectivity, controllability, stability or disturbance-rank assumptions.

The proof first takes disturbance-compatible output-nulling quotients. The reduced premise relations become graphs with coupling maps E and H. Their stable-image identity forces EH to be nilpotent, and the finite inverse of I-EH gives both a full initial-state relation and compatible target disturbances. The quotient bisimulations then lift the result to the original specifications.

This is the precise linear/free-disturbance model in the [2009 OWR source](https://ems.press/journals/owr/articles/3394), printed pp.655–658. It does not establish a circular rule for arbitrary nonlinear systems, transition systems, constrained disturbances or other composition semantics.

## Read and verify

- [Complete proof](TURN_3.md), with [quotient details](TURN_2.md)
- [Full result, source credit and boundaries](FINAL_RESULT.md)
- [Independent source and proof review](review/ADVERSARIAL_REVIEW.md)
- [Current reviewed status](CURRENT_STATUS.json)
- [Exact source gate](SOURCE_GATE.md) and [narrow auxiliary-lemma diagnostic](DEPENDENCY_CHECK.md)

The diagnostic concerns the displayed instantaneous-kernel enlargement in the indexed 2010 Lemma 1, equation (22), and Appendix A. Both main premises can be identity simulations in that example: it is not a counterexample to Theorem 4. The present proof does not depend on that enlargement. The 2009 pages were visually verified; the 2010 source was checked in indexed primary text, while its binary PDF was inaccessible. This access qualification is retained.

Run `python check_dependency.py`, `python verify_turn1.py`, `python verify_turn2.py`, and `python verify_turn3.py`: all 7,375 exact author assertions reproduce their receipts. Run `python review/independent_checks.py` for 8,428 independently written exact controls. Finite controls supplement the universal written proof; the historical finite-field search is bounded proposal evidence only.

All 30 frozen author files and nine independent-review files are preserved byte-for-byte. Their historical candidate or unresolved statuses record earlier checkpoints; this README and CURRENT_STATUS.json give the reviewed disposition. The public manifest binds the complete publication packet. Primary PDFs, screenshots and raw imports are not redistributed. AI-assisted review is not formal verification or human peer review.

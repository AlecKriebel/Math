# AI assistance disclosure

**First repository release timestamp (UTC):** `2026-07-25T23:14:47Z`

This research note, its LaTeX version, and much of the accompanying
verification software were produced with substantial assistance from
OpenAI language models operating through Codex.

AI assistance included:

- searching and organizing the repository's pre-existing calculations;
- proposing normal forms, case splits, and algebraic elimination routes;
- drafting and revising mathematical prose;
- writing symbolic and dependency-free exact-arithmetic checkers;
- constructing mutation tests and fail-closed wrappers;
- comparing theorem hypotheses with the frozen taxonomy and its 45
  coefficient pivots; and
- helping inspect the cited degree-bounded plane theorem and its
  applicability.

The systems were also used adversarially: separate sessions reconstructed
key calculations without importing the candidate implementations, tested
omitted branches and coefficient specializations, and injected deliberate
faults. These checks reduce some transcription and coverage risks, but they
do not turn the work into a formal proof or a peer-reviewed result.

## Responsibility and limitations

The mathematical claims remain the responsibility of the human author.
Readers should verify the proof, the retained exact identities, the
normal-form coverage, and the literature citations independently.

In particular:

- Exact computer algebra verifies only the formulas and finite case ledgers
  that were encoded. It cannot establish that an unencoded hypothesis or
  branch was unnecessary.
- “Hostile audit” is an internal workflow label. It does not mean review by
  an independent human mathematician and must not be described as peer
  review.
- The source-specific prior-art search is not exhaustive and is not a
  guarantee of novelty or priority.
- Moh's plane bounded-degree theorem and the injective-étale theorem are
  literature inputs. The repository checks their stated hypotheses and
  application here; it does not reprove those theorems.
- The result excludes one of fourteen frozen quartic leading-form rows. It
  does not prove the full degree-four case of the Jacobian Conjecture.

No person outside the project was contacted, messaged, or asked to review
the work by an AI system. External communication and any decision to
release the manuscript remain exclusively with the human researcher.

## Reproducibility

The aggregate entry point is
[`verify_all_strict.sh`](verify_all_strict.sh). It replays the retained
exact calculations, methodologically separate hostile checks, negative
controls, coverage audit, quadratic-component regression check, and final
post-freeze bridge wrapper. A passing run is computational evidence about
the checked artifacts; it is not a substitute for peer review.

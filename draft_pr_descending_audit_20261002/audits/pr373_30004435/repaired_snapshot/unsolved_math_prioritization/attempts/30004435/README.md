# Problem 30004435: probability-only tail-field partials

**Reviewed disposition: unsolved, 5/5. Independent full scoped audit: PASS.**

Steif's original Question C asks for a probability-only proof, without entropy theory, of the equality of the remote-past and remote-future tail fields of every stationary two-sided finite-alphabet process. The general equality is already known through entropy-based arguments. This five-turn packet does not supply the unrestricted requested method.

- [Final scope and limitations](RESULT.md)
- [Exact source normalization](SOURCE_NORMALIZATION.md)
- [Independent full source/proof audit](final_review/ADVERSARIAL_REVIEW.md)
- [Original source, printed632](https://ems.press/content/serial-article-files/46847)

## Proven subclasses and reductions

1. [Finite stationary Markov chains](TURN_1.md): all three tails equal the recurrent-class/periodic-phase field; an exact L² defect formulation and approximation barriers are included.
2. [Finite hidden Markov observations](TURN_2.md): the surviving observable tail is a conditional-law quotient, with a proved finite word-length certificate.
3. [Complete-connections kernels](TURN_3.md): uniform overlap and summable continuity give both one-sided zero-one laws and a quantitative coupling bound.
4. [Finitary codes](TURN_4.md): finite mean coding radius gives corresponding tail inclusions; two-sided finite-mean isomorphisms transfer equality.
5. [Non-atomic mixtures and rotation](TURN_5.md): conditional mixing with a common stationary skeleton identifies the random-law tail, while binary irrational rotation explicitly shows a nonmixing common tail outside that reduction.

All hypotheses remain essential to the stated results. Alpha-mixing alone is not used to infer bilateral-tail triviality. No general finite-state, coupling, coding or conditional-mixing representation has been established. Classical Markov, coupling, observable-space and rotation ingredients are credited; no novelty claim is made.

## Reproduction

Python3.10+ standard library only, no third-party packages:

    python REPLAY_ALL.py
    python final_review/verify_review.py --author-dir .

The first command reproduces all210,974 author assertions byte-for-byte and checks166 author manifest bindings. The second validates the unchanged seven-file independent review, all42 frozen author blob identities and9,334 separate exact controls. Optional `python REPLAY_ALL.py --sources PATH` verifies the four source PDFs if they have been obtained separately; they are not redistributed here.

The written infinite-probability arguments were independently audited; finite controls alone do not prove tail equalities. The audit is AI-assisted, not external peer review or a historical novelty certification. All42 frozen author files and seven frozen review files are unchanged. Earlier pending-review wording remains part of that history; this additive wrapper records the completed scoped PASS.

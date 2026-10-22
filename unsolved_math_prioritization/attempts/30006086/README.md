# Loop invariants: accepted scoped partial results

Problem **30006086 / OWR-14298797-002**, queue rank **960**. Full target: **UNSOLVED, 5/5**.

The independent mathematical audit accepts the frozen author packet without a proof correction. Read [the result](audited/author/RESULT.md), [full independent audit](audited/audit/AUDIT_REPORT.md), and [acceptance record](audited/audit/ACCEPTANCE.json).

Accepted scope:
- A direct all-dimension generation proof through degree 4, extended by exact computation and polarization through degree 8.
- The stronger binary linear formula through degree 13.
- An all-degree distinct-letter area-product obstruction and exterior-power injection.
- Sharp identity detection at degree 2m when the first nonzero logarithm degree is m >= 3, actual piecewise-linear loops with unbounded detection delay, and the bounded-variation tree-like identity class.

The unrestricted shuffle-generation conjecture and geometric classification of arbitrary nontrivial loop pairs remain unresolved. The other clauses of DPR Conjecture 4.16 are not proved. There is no novelty, worldwide-openness, human-peer-review, or proof-assistant certification claim.

## Artifact preservation

`audited/` preserves all 25 files of the independently frozen audit packet, including every original author file, the original author archive, the full audit, and completed calculation outputs. `AUDITED_PACKET.zip` is the original 65,604-byte audited archive. Earlier statements that review or publication was pending describe those preserved historical freezes. This wrapper records the later publication stage.

The package contains authored mathematics, code, mathematical calculation outputs, public source metadata and hashes. It contains no copied source PDFs/text/images, corpus contents, or private coordination records. Dataset hashes and record counts are verification metadata only.

## Portable verification

Python 3.11+ and the standard library, with no network:

    python3 -B verify_publication.py

This checks the sealed inventory, exact original archives, saved 109-case independent and author rank results, 2,137 author controls, and 319 supplemental controls. It freshly replays 29 author and 29 independent rank cases, all 319 supplemental controls, three expected optimized-mode rejections, and ten mutation controls. Replay writes occur only in an isolated temporary directory. Expensive completed 109-case calculations were inspected before choosing bounded fresh replays rather than needlessly repeating them.

The wrapper also uses explicit checks under `python3 -B -O verify_publication.py`. Its algebra subprocesses run without optimization; three separate `-O` algebra runs **must fail**. A successful wrapper is never an optimized-algebra pass.

Use `--integrity-only` for hashes and inventory, or `--full-replay` to recompute both complete 109-case rank suites; the latter can take substantially longer. The publication stage does not claim it repeated the full calculations. Finite computations support the mathematical arguments and do not settle the unrestricted conjecture.

## Public references

- Diehl, Preiß and Reizenstein, *Conjugation, loop and closure invariants of the iterated-integrals signature*, [arXiv:2412.19670v1](https://arxiv.org/abs/2412.19670).
- Rosa Preiß, *Loop invariants and conjugation*, in *Directions in Rough Analysis*, [Oberwolfach Report 49/2024](https://doi.org/10.4171/OWR/2024/49), printed pp. 2936–2937.
- Hambly and Lyons, *Uniqueness for the signature of a path of bounded variation and the reduced path group*, [Annals of Mathematics 171 (2010), 109–167](https://doi.org/10.4007/annals.2010.171.109).

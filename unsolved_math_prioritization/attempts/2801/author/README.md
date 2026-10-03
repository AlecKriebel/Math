# KP-3.3: a recent attributed geometric-triangulation theorem

Research record for UnsolvedMath ID **2801**, ranked **477** in the observed queue.
Checked on **3 October 2026**.

## Result and qualification

Huabin Ge's **Theorem 1.1**, *Geometric ideal triangulations of hyperbolic
3-manifolds*, [arXiv:2609.27635v1](https://arxiv.org/abs/2609.27635v1), submitted
**23 September 2026**, states the full affirmative answer to the catalogued
question. Its scope is every **complete, noncompact, finite-volume hyperbolic
3-manifold**, including the nonorientable case. The resulting finite ideal
triangulation consists of nondegenerate tetrahedra and realizes the given complete
metric.

The attached source verification reconstructs the relevant proof in Sections 2–4
and finds no mathematical gap. This is an **attributed prior-preprint result**,
not a new result of this research campaign. The arXiv record currently lists v1
only; no journal publication or refereed acceptance was verified. A fresh,
independent complete audit and the final publication gate are still required
before administrative acceptance of this record.

**Original substantive proof-attempt turns used: 0/5.** Literature retrieval,
verification of someone else's proof, exact controls, review and packaging do
not consume original proof-attempt turns. No novel proof, first-priority claim,
new paper, or new DOI is proposed.

## Contents

- `SOURCE_STATUS.md`: exact problem identity, source correction, chronology,
  hypotheses, prior-attempt evidence and retrieval limits.
- `PROOF_AUDIT.md`: a detailed attributed audit of the proof needed for KP-3.3.
- `verify_affine_controls.py`: independently written exact rational controls.
- `verification_results.json`: the recorded output, 64 checks passed.
- `TURN_LEDGER.json`: zero-turn accounting and the pending external gate.

Run the controls with Python 3 and SymPy:

    python verify_affine_controls.py

The controls verify finite affine examples and stress cases, not the universal
hyperbolic theorem. The universal justification is the written proof audit with
the classical Epstein–Penner decomposition as an explicitly identified input.

## Source and disclosure safeguards

The exact numeric UnsolvedMath URL returned HTTP 403 during this check. Problem
identity is therefore tied to the hash-verified imported ID record, the indexed
public alias, and the visually checked K3 statement; this is not represented as
a successful current-page read. The original book, articles, screenshots and
imported corpus are not included in the author package.

This record and its verification code were prepared with extensive AI assistance.
It is not a formal proof-assistant certificate or a substitute for expert review.
The mathematical construction belongs to Huabin Ge. The detailed discussion is
an attributed adaptation of the proof in his CC BY 4.0 preprint, with additional
audit explanations and independently written controls; see `PROOF_AUDIT.md`.
